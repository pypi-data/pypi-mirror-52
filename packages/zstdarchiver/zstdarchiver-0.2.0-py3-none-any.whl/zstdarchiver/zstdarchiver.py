# coding: utf-8

# The MIT License (MIT)

# Copyright (c) 2019 Martin Bammer, mrbm74 at gmail dot com

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software - recordclass library - and associated documentation files
# (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom
# the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# distutils: language=c++
#cython: boundscheck=True
#cython: wraparound=True
#cython: initializedcheck=True
#cython: cdivision=True
##cython: optimize.use_switch=True
##cython: optimize.unpack_method_calls=False
##cython: unraisable_tracebacks=True

"""
    Fast compression module with some special features.
"""

import os
import io
import gc
import time
import struct
import fnmatch
import itertools
import shutil
import importlib
from collections import deque
from typing import Optional, Deque, TypeVar

import fastthreadpool
import msgpack
import zstandard as zstd

TupleStr = TypeVar('TupleStr', tuple, str)
TupleList = TypeVar('TupleList', tuple, list)
TupleListSet = TypeVar('TupleListSet', tuple, list, set)

#c cdef size_t BLOCKSIZE
KB: int = 1024
MB: int = KB * KB
BLOCKSIZE: int = 16 * MB     # Default block size for compression

ZARID: bytes = b"ZAR\0"      # ZAR archive version 0

ZARFLG_OK: int = 0x01        # ZAR archive creation was successfull
ZARFLG_ENCCONT: int = 0x02   # Contents (file data) is encrypted
ZARFLG_ENCTOC: int = 0x04    # TOC is encrypted
ZARFLG_ENCMETA: int = 0x08   # Metadata is encrypted
ZARFLG_ENC: int = ZARFLG_ENCCONT | ZARFLG_ENCTOC | ZARFLG_ENCMETA

ZARFLG2SYM = {ZARFLG_OK: "OK", ZARFLG_ENCCONT: "Contents encrypted", ZARFLG_ENCTOC: "TOC encrypted",
              ZARFLG_ENCMETA: "Meta data encrypted"}

# File types
FTYPE_EMPTY: int = 0
FTYPE_ROOT: int = -1
FTYPE_DIR: int = -2
FTYPE_SLINK: int = -3
FTYPE_HLINK: int = -4
FTYPE_DEV: int = -5
FTYPE_PIPE: int = -6

bPosix: bool = os.name == 'posix'

path_basename = os.path.basename
path_islink = os.path.islink
path_join = os.path.join


# noinspection PyPep8Naming
class mdict(dict):
    """
    Dictionary with multiple values per key.
    """
    # noinspection PyMissingConstructor
    def __init__(self, mapping, **kwargs):
        self.update(mapping, **kwargs)

    def __setitem__(self, key, value):
        self.setdefault(key, []).append(value)

    def update(self, mapping, **kwargs):
        if isinstance(mapping, dict):
            mapping = mapping.items()
        for key, value in mapping:
            self.setdefault(key, []).append(value)
        for key, value in kwargs.items():
            self.setdefault(key, []).append(value)


#c cdef os_fspath, os_scandir
os_fspath = os.fspath
os_scandir = os.scandir


def walk(top, bFollowSymlinks=False):
    top = os_fspath(top)
    dirs = []
    files = []
    try:
        itScanDir = os_scandir(top)
    except OSError:
        return
    with itScanDir:
        while True:
            try:
                entry = next(itScanDir)
            except StopIteration:
                break
            except OSError:
                continue
            try:
                if entry.is_dir():
                    dirs.append(entry)
                else:
                    files.append(entry)
            except OSError:
                files.append(entry)
    yield top, dirs, files
    for entry in dirs:
        pathName = f"{top}/{entry.name}"
        if bFollowSymlinks or not entry.is_symlink():
            yield from walk(pathName, bFollowSymlinks)


#c cdef tuple stats2Tuple(stats):
def stats2Tuple(stats) -> tuple:  #p
    return stats.st_ctime, stats.st_atime, stats.st_mtime, stats.st_size, stats.st_uid, stats.st_gid, stats.st_mode


class ZAR(object):
    """
    The Z-Archiver class
    """

    # noinspection PyShadowingNames
    def __init__(self, zarPathName: str, mode: str = "r", password: Optional[str] = None, level: int = 11,
                 blockSize: int = BLOCKSIZE, cryptPluginName: str = None, bEncryptToc: bool = False,
                 bEncryptMeta: bool = False, metaPluginName: Optional[str] = None,
                 refArchives: Optional[list] = None) -> None:
        """
        zarPathName: Path to ZAR archive.
        mode: 'r' = Open archive for reading
              'w' = Overwrite existing archive
              'a' = Append new files to archive. Existing files will be replaced and old file contents removed.
              'k' = Append new files to archive. Existing files will be replaced but old file contents kept.
                    This avoids some possible copy operations which would slow down the archiving process.
        """
        self.zarPathName = zarPathName
        self.__zarId = ZARID
        if mode not in ('r', 'w', 'a', 'k'):
            raise ValueError("invalid mode (must be 'r', 'w', 'a' or 'k')")
        self.__mode = mode
        if not(8 * MB <= blockSize <= 64 * MB):
            raise ValueError("invalid block size (must be 8..64)")
        self.__blockSize = blockSize
        if not(1 <= level <= 22):
            raise ValueError("invalid compression value (must be 1..22)")
        self.__level = level
        self.__flags: int = ZARFLG_OK
        if mode == 'r':
            if not os.path.exists(zarPathName):
                raise FileNotFoundError("archive not found")
        if mode in ('r', 'a', 'k') and os.path.exists(zarPathName):
            self.__header = self.readHeader()  # Header of existing archive used with modes 'r', 'a' and 'k'
            cryptPluginName = self.__header.get("crypt", cryptPluginName)
        else:
            self.__header = None
            if cryptPluginName and password:
                self.__flags |= ZARFLG_ENCCONT
                if bEncryptToc:
                    self.__flags |= ZARFLG_ENCTOC
                if bEncryptMeta:
                    self.__flags |= ZARFLG_ENCMETA
        if password and not cryptPluginName:
            cryptPluginName = "default"
        self.cryptPluginName = cryptPluginName
        if cryptPluginName:
            if not password:
                raise ValueError("password is missing for encrypted archive")
            self._cryptPlugin = importlib.import_module("zar.plugins.crypt." + cryptPluginName).Plugin(password)
        elif password:
            raise ValueError("cryptPluginName is missing")
        else:
            self._cryptPlugin = None
        self.metaPluginName = metaPluginName
        if metaPluginName:
            self._metaModule = importlib.import_module("zar.plugins.meta." + metaPluginName)
        else:
            self._metaModule = None
        self.refArchives = refArchives
        self.refToc = {}  # Combined TOC of reference archives
        # Parse reference archives
        if refArchives:
            for refArchive in refArchives:
                self.refToc.update(ZAR(refArchive, cryptPluginName=cryptPluginName, password=password).readHeader()["toc"])
        # Status and errors
        self._cmpSize: int = 0  # Compressed size of archive
        self._size: int = 0  # Uncompressed size of archive
        self._totFileCnt: int = 0  # Total number of files
        self._bParseFinished: bool = False
        self._pendingFileCnt: int = 0
        self._pendingBlockCnt: int = 0
        self._curPathName: str = ""
        self.__errors = deque()
        #
        self._cpuCnt = os.cpu_count()

    @property
    def zarId(self) -> bytes:
        return self.__zarId

    @property
    def level(self) -> int:
        return self.__level

    @property
    def flags(self) -> int:
        return self.__flags

    @property
    def header(self) -> dict:
        return self.__header

    @property
    def errors(self) -> Deque:
        return self.__errors

    @property
    def cmpSize(self) -> int:
        return self._cmpSize

    @property
    def size(self) -> int:
        return self._size

    @property
    def totFileCnt(self) -> int:
        return self._totFileCnt

    @property
    def bParseFinished(self) -> bool:
        return self._bParseFinished

    @property
    def pendingFileCnt(self) -> int:
        return self._pendingFileCnt

    @property
    def pendingBlockCnt(self) -> int:
        return self._pendingBlockCnt

    @property
    def curPathName(self) -> str:
        return self._curPathName

    @staticmethod
    def getFileStats(pathName) -> tuple:
        stats = os.lstat(pathName)
        return stats.st_ctime, stats.st_atime, stats.st_mtime, stats.st_size, stats.st_uid, stats.st_gid, stats.st_mode

    @staticmethod
    def setFileStats(pathName, stats) -> None:
        st_ctime, st_atime, st_mtime, st_size, st_uid, st_gid, st_mode = stats
        if bPosix:
            os.lchmod(pathName, st_mode)
            os.lchown(pathName, st_uid, st_gid)
        os.utime(pathName, (st_atime, st_mtime))
        # TODO: Add support for Windoof

    def readHeader(self) -> dict:
        """
            Header (dict) entries:
            { "toc" : TOC (tuple of tuples),
              "meta" : { RelPathName1 : MetaData (dict), ... },
              "metaPlugin" : PluginName,
              "cryptPlugin" : PluginName,
              "ref" : ( RelPathName1, ... )
              "offset" : HeaderOffsetPos
            }
            "meta" and "metaPlugin" are only present if meta plugin was defined at creation time.
            "cryptPlugin" is only present if crypt plugin was defined at creation time.
            "ref" is only present if reference archives were defined at creation time.
                The relative paths are relative to the path of this archive.
            "offset" is added by function readHeader for later use and is not saved in archive.
        """
        with open(self.zarPathName, "rb") as I:
            self.__zarId = I.read(4)
            if self.__zarId != ZARID:
                raise ValueError(f"unknown file type '{self.__zarId}'")
            self.__flags, headerOffset = struct.unpack("<BQ", I.read(9))
            I.seek(headerOffset)
            gc.disable()
            cmpHeader = I.read()
            ZD = zstd.ZstdDecompressor()
            packHeader = ZD.decompress(cmpHeader)
            header = msgpack.unpackb(packHeader, use_list=False, raw=False)
            header["toc"] = msgpack.unpackb(ZD.decompress(header["toc"]), use_list=False, raw=False)
            if "meta" in header:
                header["meta"] = msgpack.unpackb(ZD.decompress(header["meta"]), use_list=False, raw=False)
            header["offset"] = headerOffset
            gc.enable()
        return header

    def getToc(self) -> tuple:
        """
        Contents of TOC:
        (
            (rootDirName, fileStats, FTYPE_ROOT),
            (relDirName, fileStats, FTYPE_DIR),
            (relPathName, fileStats, FTYPE_EMPTY),
            ((relPathName, fileStats, fileStart), blockStart, blockEnd), -> big file
            (((relPathName, fileStats, fileStart), (relPathName, fileStats, fileStart), ...), blockStart, blockEnd),
        )
        """
        rootEntry = None
        toc = self.__header["toc"]
        dirEntries = []
        emptyFiles = []
        fileEntries = []
        relPathNames = []
        for tocEntry in toc:
            if isinstance(tocEntry[0], tuple):
                fileEntries.append(tocEntry)
                if isinstance(tocEntry[0][0], tuple):
                    relPathNames.extend([entry[0] for entry in tocEntry[0]])
                else:
                    relPathNames.append(tocEntry[0][0])
            else:
                fType = tocEntry[2]
                if fType == FTYPE_EMPTY:
                    emptyFiles.append(tocEntry)
                    relPathNames.append(tocEntry[0])
                elif fType == FTYPE_DIR:
                    dirEntries.append(tocEntry)
                elif fType == FTYPE_ROOT:
                    rootEntry = tocEntry
                else:
                    raise ValueError(f"invalid TOC entry {tocEntry}")
                continue
        return rootEntry, dirEntries, emptyFiles, fileEntries, relPathNames

    @staticmethod
    def getFilteredFileNames(fileNames: set, includes: Optional[str] = None, includelist: Optional[TupleListSet] = None,
                             excludes: Optional[str] = None, excludelist: Optional[TupleListSet] = None) -> set:
        if includes:
            fileNames = fnmatch.filter(fileNames, includes)
        if includelist:
            fileNames = fileNames.intersection(includelist)
        if excludes:
            fileNames = fileNames.difference(fnmatch.filter(fileNames, excludes))
        if excludelist:
            fileNames = fileNames.difference(excludelist)
        return fileNames

    def getFilteredToc(self, includes: Optional[str] = None, includelist: Optional[TupleListSet] = None,
                       excludes: Optional[str] = None, excludelist: Optional[TupleListSet] = None) -> tuple:
        chain_from_iterable = itertools.chain.from_iterable
        rootEntry, dirEntries, emptyFiles, fileEntries, _ = self.getToc()
        # Filter empty files
        fileDict = mdict([(path_basename(entry[0]), entry) for entry in emptyFiles])
        fileNames = self.getFilteredFileNames(set(fileDict), includes, includelist, excludes, excludelist)
        emptyFiles = tuple(chain_from_iterable([fileDict[key] for key in fileNames]))
        relPathNames = [entry[0] for entry in emptyFiles]
        # Filter big files
        fileDict = mdict([(path_basename(entry[0][0]), entry) for entry in fileEntries
                          if not isinstance(entry[0][0], tuple)])
        fileNames = self.getFilteredFileNames(set(fileDict), includes, includelist, excludes, excludelist)
        bigFiles = chain_from_iterable([fileDict[key] for key in fileNames])
        relPathNames.extend([entry[0][0] for entry in bigFiles])
        # Filter small files
        smallFiles = []
        for tocEntry in fileEntries:
            entries, blockStart, blockEnd = tocEntry
            if not isinstance(entries[0], tuple):
                continue
            fileDict = mdict([(path_basename(entry[0]), entry) for entry in entries])
            fileNames = self.getFilteredFileNames(set(fileDict), includes, includelist, excludes, excludelist)
            entries = chain_from_iterable([fileDict[key] for key in fileNames])
            if entries:
                smallFiles.append((entries, blockStart, blockEnd))
                relPathNames.extend([entry[0] for entry in smallFiles])
        return rootEntry, dirEntries, emptyFiles, fileEntries, relPathNames

    def __initWriteMode(self) -> str:
        self.__errors.clear()
        if self.__mode == 'r':
            raise TypeError("archive is opened for reading only")
        return "wb" if self.__mode == 'w' else 'rb+'

    def __writeHeader(self, ZO, header, offset):
        ZC = zstd.ZstdCompressor(write_content_size=True, write_checksum=True, level=self.__level)
        ZO.write(ZC.compress(msgpack.packb(header, use_bin_type=True)))
        arSize = ZO.tell()
        ZO.seek(4)
        ZO.write(struct.pack("<BQ", self.__flags, offset))
        return arSize

    # noinspection PyShadowingNames
    def add(self, rootDirName: str, bFollowSymlinks: bool = False,
            includes: Optional[str] = None, includeList: Optional[TupleListSet] = None,
            excludes: Optional[str] = None, excludeList: Optional[TupleListSet] = None) -> int:
        """
        rootDirName: Path to file tree to add to the archive. If path endswith "/*" or "\\*" the base
                     path will not be included.
        """
        #c cdef size_t blockSize, fileSize

        # noinspection PyShadowingNames,PyBroadException
        def compressFile(pathName: str, fileStats, busyCnt: int) -> TupleStr:
            try:
                buf = io.BytesIO()
                with open(pathName, "rb") as I:
                    ZC = zstd.ZstdCompressor(write_content_size=True, write_checksum=True, level=self.__level,
                                             threads=2 if busyCnt > 4 else 4)
                    ZC.copy_stream(I, buf)
                cmpData = buf.getbuffer() if self._cryptPlugin is None else self._cryptPlugin.encrypt(buf.getbuffer())
                return (pathName[rootDirNameLen:], fileStats, 0), cmpData
            except Exception as exc:
                return f"Failed to compress {pathName} with error: {exc}"

        # noinspection PyShadowingNames
        def compressBlock(files: list, size: int, busyCnt: int) -> TupleStr:
            try:
                toc = []
                buf = bytearray(size)
                endPos = 0
                extractFileMetaData = getattr(metaPlugin, "extractFileMetaData", None)
                for pathName, entry in files:
                    fileStats = stats2Tuple(entry.stat(follow_symlinks=False))
                    fileSize = fileStats[3]
                    fileData = memoryview(buf)[endPos:endPos + fileSize]
                    open(pathName, "rb").readinto(fileData)
                    endPos += fileSize
                    if extractFileMetaData is not None:
                        extractFileMetaData(pathName[rootDirNameLen:], fileData)
                    toc.append((pathName[rootDirNameLen:], fileStats, endPos))
                cmpData = zstd.ZstdCompressor(write_content_size=True, write_checksum=True, level=self.__level,
                                              threads=0 if busyCnt > 4 else 2).compress(buf)
                if self._cryptPlugin is not None:
                    cmpData = self._cryptPlugin.encrypt(cmpData)
                return toc, cmpData
            except Exception as exc:
                return f"Failed to compress block with {len(files)} files with error: {exc}"

        # noinspection PyShadowingNames
        def writeResults(wait: Optional[bool]) -> None:
            extractBigFileMetaData = getattr(metaPlugin, "extractBigFileMetaData", None)
            for result in pool.as_completed(wait):
                if isinstance(result, tuple):
                    blockToc, cmpData = result
                    if extractBigFileMetaData is not None and isinstance(blockToc, tuple):
                        try:
                            pool.submit(extractBigFileMetaData, blockToc[0])
                        except Exception as exc:
                            self.__errors.append(f"Failed to extract meta data from file {blockToc[0]} with error: {exc}")
                    self._pendingFileCnt -= len(blockToc)
                    self._pendingBlockCnt -= 1
                    try:
                        if isinstance(blockToc[0], tuple):
                            self._curPathName = blockToc[0][0]
                        else:
                            self._curPathName = blockToc[0]
                        blockStart = ZO.tell()
                        ZO.write(cmpData)
                        # noinspection PyTypeChecker
                        zarToc.append((blockToc, blockStart, ZO.tell()))
                        self._cmpSize = blockStart
                    except Exception as exc:
                        self.__errors.append(f"Failed to write compressed block to archive with error: {exc}")
                elif result is not True:
                    self.__errors.append(f"Exception: {result}")

        self._pendingBlockCnt = 0
        self._pendingFileCnt = 0
        self._totFileCnt = 0
        self._bParseFinished = False
        mode = self.__initWriteMode()
        setIncludes: set = None if not includeList else set(includeList)
        setExcludes: set = None if not excludeList else set(excludeList)
        if self.__header:
            offset = self.__header["offset"]
            # zarFileNames = {}
            # for block in self.__header["toc"]:
            #    pass  # TODO: Update excludes
        else:
            offset = 0
            # zarFileNames = None
        if not bPosix:
            rootDirName = rootDirName.replace("\\", "/")
        metaPlugin = None if self._metaModule is None else self._metaModule.Plugin(rootDirName)
        rootDirNameLen = len(rootDirName) + 1
        zarToc = []
        if not rootDirName.endswith("/*"):
            zarToc.append((path_basename(rootDirName), self.getFileStats(rootDirName), FTYPE_ROOT))
        with open(self.zarPathName, mode) as ZO:
            if (mode == "wb") or (offset == 0):  # wb=Overwrite archive if it exists
                # First write ZAR ID, flags and empty Header offset
                # noinspection PyTypeChecker
                ZO.write(ZARID + b"\0\0\0\0\0\0\0\0\0")
            else:
                # First invalidate flags until new archive was written successfully
                ZO.seek(4)
                # noinspection PyTypeChecker
                ZO.write(b"\0")
                # Then seek to start of header
                ZO.seek(offset)
            # Then write compressed data
            zarDirs = {}
            # We can use a with statement to ensure threads are cleaned up promptly
            with fastthreadpool.Pool(self._cpuCnt + 2) as pool:
                smallFiles = []
                blockSize = 0
                try:
                    for baseDirName, dirs, files in walk(rootDirName, bFollowSymlinks):
                        if baseDirName != rootDirName:
                            relPathName = baseDirName[rootDirNameLen:]
                            if relPathName not in zarDirs:
                                zarDirs[relPathName] = self.getFileStats(baseDirName)
                        for entry in dirs:
                            pathName = f"{baseDirName}/{entry.name}"
                            relPathName = pathName[rootDirNameLen:]
                            if relPathName not in zarDirs:
                                zarDirs[relPathName] = stats2Tuple(entry.stat(follow_symlinks=False))
                        # Apply file filters
                        if not includes and not setIncludes:
                            if not files:
                                continue
                        else:
                            if includes:
                                files = [entry for entry in files if fnmatch.fnmatch(entry.name, includes)]
                            if setIncludes:
                                files = [entry for entry in files if entry.name in setIncludes]
                        if excludes:
                            files = [entry for entry in files if not fnmatch.fnmatch(entry.name, excludes)]
                        if setExcludes:
                            files = [entry for entry in files if entry.name not in setExcludes]
                        for entry in files:
                            pathName = f"{baseDirName}/{entry.name}"
                            fileStats = stats2Tuple(entry.stat(follow_symlinks=False))
                            fileSize = fileStats[3]
                            self._pendingFileCnt += 1
                            self._totFileCnt += 1
                            self._curPathName = pathName
                            if fileSize == 0:
                                # Empty file
                                zarToc.append((pathName[rootDirNameLen:], fileStats, FTYPE_EMPTY))
                                continue
                            self._size += fileSize
                            if fileSize < BLOCKSIZE:
                                # Small file
                                smallFiles.append((pathName, entry))
                                blockSize += fileSize
                                if blockSize > BLOCKSIZE:
                                    pool.submit(compressBlock, smallFiles, blockSize, pool.busy)
                                    self._pendingBlockCnt += 1
                                    smallFiles = []
                                    blockSize = 0
                                    writeResults(False)
                            else:
                                # Big file
                                pool.submit(compressFile, pathName, fileStats, pool.busy)
                                self._pendingBlockCnt += 1
                                writeResults(False)
                    if smallFiles:
                        pool.submit(compressBlock, smallFiles, blockSize, pool.busy)
                        self._pendingBlockCnt += 1
                except KeyboardInterrupt:
                    self.__errors.append("Cancelled")
                self._bParseFinished = True
                writeResults(None)
            self._curPathName = ""
            offset = ZO.tell()  # Start position of header
            ZC = zstd.ZstdCompressor(write_content_size=True, write_checksum=True, level=self.__level)
            # Finally write Header
            for relPathName, fileStats in zarDirs.items():
                zarToc.append((relPathName, fileStats, FTYPE_DIR))
            zarTocCmp = ZC.compress(msgpack.packb(zarToc, use_bin_type=True))
            if self.__flags & ZARFLG_ENCTOC:
                header = {"toc": self._cryptPlugin.encrypt(zarTocCmp)}
            else:
                header = {"toc": zarTocCmp}
            if metaPlugin is not None:
                header["metaPlugin"] = self.metaPluginName
                metaData = list(metaPlugin.meta)
                try:
                    meta = ZC.compress(msgpack.packb({pathName: meta for pathName, meta in metaData},
                                                     use_bin_type=True))
                except TypeError:
                    self.__errors.append(metaData)
                    raise
                if self.__flags & ZARFLG_ENCMETA:
                    meta = self._cryptPlugin.encrypt(meta)
                header["meta"] = meta
            if self._cryptPlugin is not None:
                header["cryptPlugin"] = self.cryptPluginName
            if self.refArchives:
                header["ref"] = self.refArchives
            arSize = self.__writeHeader(ZO, header, offset)
        self._cmpSize = arSize
        return arSize  # Return size of archive

    def extractEmptyFiles(self, dstDirName: str, emptyFiles: list, bFileStats: bool) -> list:
        for relPathName, fileStats, _ in emptyFiles:
            pathName = f"{dstDirName}/{relPathName}"
            open(pathName, "wb").close()
            if bFileStats:
                self.setFileStats(pathName, fileStats)
        return ["*EMPTY*"]

    def extractBlock(self, dstDirName: str, cmpData: bytes, entries: TupleList, bFileStats: bool) -> list:
        # noinspection PyBroadException
        try:
            buf = io.BytesIO(zstd.ZstdDecompressor().decompress(cmpData))
        except:
            try:
                relPathName, fileStats, _ = entries
                pathName = f"{dstDirName}/{relPathName}"
                with open(pathName, "wb") as O:
                    zstd.ZstdDecompressor().copy_stream(io.BytesIO(cmpData), O)
                    O.flush()
                if bFileStats:
                    self.setFileStats(pathName, fileStats)
                return [relPathName]
            except:
                import traceback
                traceback.print_exc()
                raise
        startPos = 0
        relPathNames = []
        for relPathName, fileStats, endPos in entries:
            pathName = f"{dstDirName}/{relPathName}"
            with open(pathName, "wb") as O:
                O.write(buf.read(endPos - startPos))
            if bFileStats:
                self.setFileStats(pathName, fileStats)
            startPos = endPos
            relPathNames.append(relPathName)
        return relPathNames

    def createDirectories(self, dstDirName: str, dirList: list, bFileStats: bool) -> None:
        relDirName, fileStats = dirList.pop(0)
        baseDirName = f"{dstDirName}/{relDirName}"
        os.mkdir(baseDirName)
        if bFileStats:
            self.setFileStats(baseDirName, fileStats)
        for relDirName, fileStats in dirList:
            dirName = f"{baseDirName}/{relDirName}"
            os.makedirs(dirName)
            if bFileStats:
                self.setFileStats(dirName, fileStats)

    def extract(self, dstDirName: str, bFileStats: bool = False,
                includes: Optional[str] = None, includelist: Optional[TupleListSet] = None,
                excludes: Optional[str] = None, excludelist: Optional[TupleListSet] = None) -> None:
        self.__errors.clear()
        result = self.getFilteredToc(includes, includelist, excludes, excludelist)
        rootEntry, dirEntries, emptyFiles, fileEntries, relPathNames = result
        if rootEntry:  # (dirName, (ctime, atime, mtime, size, uid, gid, mode), entryType)
            dstDirName = f"{dstDirName}/{rootEntry[0]}"
        if os.path.exists(dstDirName):
            shutil.rmtree(dstDirName)
        os.makedirs(dstDirName)
        if bFileStats and rootEntry:
            self.setFileStats(dstDirName, rootEntry[1])
        thrCnt = self._cpuCnt + 2
        self._totFileCnt = 0
        dirLists = {}
        for relDirName, fileStats, _ in dirEntries:
            if "/" in relDirName:
                baseDirName, relDirName = relDirName.split("/", 1)
                dirLists[baseDirName].append((relDirName, fileStats))
            else:
                dirLists[relDirName] = [(relDirName, fileStats)]
        with fastthreadpool.Pool(thrCnt) as pool:
            for dirList in dirLists.values():
                pool.submit(self.createDirectories, dstDirName, dirList, bFileStats)
        with fastthreadpool.Pool(thrCnt) as pool:
            pool.submit(self.extractEmptyFiles, dstDirName, emptyFiles, bFileStats)
            with open(self.zarPathName, "rb") as I:
                try:
                    for entries, blockStart, blockEnd in fileEntries:
                        I.seek(blockStart)
                        cmpData = I.read(blockEnd - blockStart)
                        pool.submit(self.extractBlock, dstDirName, cmpData, entries, bFileStats)
                        while pool.pending > 2 * thrCnt:
                            for result in pool.as_completed(False):
                                if isinstance(result, list):
                                    self._totFileCnt += len(result)
                                elif result is not True:
                                    self.__errors.append(f"Exception: {result}")
                            time.sleep(0.01)
                except KeyboardInterrupt:
                    self.__errors.append("Cancelled")

    def cleanup(self):
        """
        TODO: Cleanup archive by removing unused file contents (if archive has been created with mode 'k')
        """
        pass

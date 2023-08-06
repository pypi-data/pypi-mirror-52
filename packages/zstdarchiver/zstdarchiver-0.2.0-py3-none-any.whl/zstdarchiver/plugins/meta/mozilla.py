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

import traceback


class Plugin(object):

    def __init__(self, rootDirName):
        from collections import deque
        self.rootDirName = rootDirName
        self.meta = deque()

    def extractFileMetaData(self, relPathName, fileData):
        try:
            if relPathName == "browser/config/version.txt":
                if not isinstance(fileData, str):
                    fileData = str(fileData, "utf-8")
                self.meta.append(("MOZILLA_VERSION", fileData))
            elif relPathName == "toolkit/components/jsoncpp/version.txt":
                if not isinstance(fileData, str):
                    fileData = str(fileData, "utf-8")
                self.meta.append(("JSONCPP_VERSION", fileData))
        except:
            self.meta.append((relPathName, traceback.format_exc()))

    def extractBigFileMetaData(self, relPathName):
        return True

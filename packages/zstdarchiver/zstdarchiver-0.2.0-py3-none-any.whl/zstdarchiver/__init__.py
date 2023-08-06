
from .zstdarchiver import ZAR, ZARID, FTYPE_DEV, FTYPE_DIR, FTYPE_EMPTY, FTYPE_HLINK, FTYPE_PIPE, FTYPE_ROOT, FTYPE_SLINK,\
    ZARFLG2SYM, ZARFLG_ENC, ZARFLG_ENCCONT, ZARFLG_ENCMETA, ZARFLG_ENCTOC, ZARFLG_OK
from . import plugins

__all__ = ['ZAR', 'ZARID', 'FTYPE_DEV', 'FTYPE_DIR', 'FTYPE_EMPTY', 'FTYPE_HLINK', 'FTYPE_PIPE', 'FTYPE_ROOT', 'FTYPE_SLINK',
           'ZARFLG2SYM', 'ZARFLG_ENC', 'ZARFLG_ENCCONT', 'ZARFLG_ENCMETA', 'ZARFLG_ENCTOC', 'ZARFLG_OK', 'plugins']

__version__ = "0.2.0"

__author__ = 'Martin Bammer'
__email__ = 'mrbm74@gmail.com'
__url__ = 'https://github.com/brmmm3/zstdarchiver'
__status__ = "alpha"
__license__ = 'MIT'

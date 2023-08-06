#! /usr/bin/env python3


"""
pyFuseFS: FUSE <-> pyFilesystem adapter
"""


import logging

import os
import sys
import errno
from time import asctime
from functools import wraps
from pwd import getpwuid
from grp import getgrgid
import time
import re
import stat
from getpass import getpass

from fs import open_fs
from fuse import FUSE, FuseOSError, Operations


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def log(func):
    f_name = func.__name__
    self = func.__self__

    @wraps(func)
    def wrapper(*args, **kwds):
        rss = self._root
        logger.debug(f'{asctime()} [{rss}]: Entering "{f_name}" with args={args} and kwds={kwds}')
        rv = func(*args, **kwds)
        logger.debug(f'{asctime()} [{rss}]: Exited "{f_name}" with retval={rv}')
        return rv
    return wrapper


class FuseFS(Operations):
    def __init__(self, root, create=False, write=False, debug=False):
        self._root = root
        fso = open_fs(root, writeable=write, create=create)
        self._fso = fso
        self._fds = {}
        self._objs = {}
        self._fdc = 0
        self._debug = debug
        return

    def __getattribute__(self, name):
        attr =  object.__getattribute__(self, name)
        if not name.startswith('_') and not name in ['getattr'] and self._debug:
            attr = log(attr)
        return attr

    # Helpers
    # =======

    def _full_path(self, partial):
        # NB: This actually isn't needed
        if True: return partial
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self._root, partial)
        return path

    def _flags_in_object(self, flags, obj, f_pat='^O_.*'):
        str_flags = []
        f_rx = re.compile(f_pat)

        for k, v in obj.__dict__.items():
            #v = obj.__dict__[k]
            if not (k.isupper() and f_rx.match(k) and isinstance(v, int)):
                continue
            if flags & v:
                str_flags.append(k)
        return str_flags

    def _mode_from_flags(self, str_flags):
        mode = []
        m_map = {
            'O_RDONLY': 'r',  # open for reading only
            'O_WRONLY': 'w',  # open for writing only
            'O_RDWR': 'r+',  # open for reading and writing
            'O_APPEND': 'a',  # append on write
            'O_NDELAY': '',
            'O_NONBLOCK': '',  # don't block on open
            'O_ACCMODE': '',
            'O_TRUNC': 'w+',  # truncate size to 0
            'O_NOFOLLOW': '',  # don't follow symlinks
            'O_EXCL': 'x',  # create file, fails if file exists
            'O_NOCTTY': '',
        }

        for sf in str_flags:
            if not sf in m_map:
                print(f'Missing flag: {sf}')
                continue
                raise KeyError(f'"{sf}" not found')
            m = m_map[sf]
            if not m: continue

            if isinstance(m, str):
                mode.append(m)

            elif callable(m):
                pass

            else:
                raise TypeError(f'Unable to process {type(m)} for mode')
        if 'a' in mode and 'w' in mode: mode.remove('w')
        return mode

    def _path_to_fd(self, path, obj=None):
        fd = self._fds.get(path)

        if not fd:
            self._fdc += 1
            fd = self._fdc
            self._fds[path] = fd
            if obj: self._objs[fd] = obj
        return fd

    def _fd_to_obj(self, fd):
        return self._objs.get(fd)

    # Filesystem methods
    # ==================

    def access(self, path: str, mode: int) -> None:
        """Test for access to a path."""
        full_path = self._full_path(path)
        if (os.path.exists(full_path) and not os.access(full_path, mode)):
            raise FuseOSError(errno.EACCES)
        return None

    def chmod(self, path: str, mode: int) -> None:
        """Update resource permissions."""
        full_path = self._full_path(path)
        #os.chmod(full_path, mode)
        str_flags = self._flags_in_object(mode, stat, r'^S_.*')
        mode_list = self._mode_from_flags(str_flags)
        print(f'Flags to chmod {full_path}: {str_flags}')
        info = {
            'access': {
                'permissions': [],
            },
        }
        self._fso.setinfo(full_path, info)
        return None

    def chown(self, path: str, uid: int, gid: int) -> None:
        """Update resource ownership."""
        full_path = self._full_path(path)
        #os.chown(full_path, uid, gid)
        info = {'access': {
            'owner': getpwuid(uid).pw_name,
            'group': getgrgid(gid).gr_name,
        }}
        self._fso.setinfo(full_name, info)
        return None

    def getattr(self, path: str, fh: int=None) -> dict:
        """Return resource metadata."""
        full_path = self._full_path(path)
        info = None

        try:
            r_info = self._fso.getinfo(full_path, ('details', 'access', 'lstat')).raw

        except:
            raise FuseOSError(errno.ENOENT)
        basic = r_info['basic']
        details = r_info.get('details') or {}
        access = r_info.get('access') or {}
        lstat = r_info.get('lstat') or {}
        st = {
            'st_atime': int(details.get('accessed') or time.time()),
            'st_ctime': int(details.get('created') or lstat.get('st_ctime') or details.get('modified') or time.time()),
            'st_gid': access.get('gid', 1000),
            'st_mode': lstat.get('st_mode') or (16893 if basic['is_dir'] else 33204),  # TODO: calculate the value
            'st_mtime': int(details.get('modified') or time.time()),
            'st_nlink': lstat.get('st_nlink', 1),
            'st_size': details.get('size') or (4096 if basic['is_dir'] else 0),
            'st_uid': access.get('uid', 1000),
        }
        return st

    def readdir(self, path, fh):
        """Create a generator to return dir entries."""
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if self._fso.isdir(full_path):
            dirents.extend(self._fso.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path) -> str:
        """Return the path to which a symbolic link points."""
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev) -> None:
        """Create a filesystem node."""
        #os.mknod(self._full_path(path), mode, dev)
        return

    def rmdir(self, path) -> None:
        """Delete the given directory."""
        self._fso.removedir(path)
        return

    def mkdir(self, path, mode) -> None:
        """Create the specified diectory."""
        # TODO: handle mode
        self._fso.makedir(self._full_path(path))
        return None

    def statfs(self, path) -> dict:
        """Return filesystem information."""
        full_path = self._full_path(path)
        try:
            stv = os.statvfs(full_path)

        except:
            stv = {
                'f_bavail': 0,
                'f_bfree': 0,
                'f_blocks': 0,
                'f_bsize': 0,
                'f_favail': 0,
                'f_ffree': 0,
                'f_files': 0,
                'f_flag': 0,
                'f_frsize': 0,
                'f_namemax': 0,
            }
        return stv

    def unlink(self, path) -> None:
        """Delete the given file."""
        self._fso.remove(self._full_path(path))
        return

    def symlink(self, name, target) -> None:
        """Create a symbolic link pointing to target."""
        os.symlink(target, self._full_path(name))
        return

    def rename(self, old, new) -> None:
        """Rename a file or folder."""
        fso = self._fso

        if fso.getinfo(old).is_dir:
            fso.movedir(old, new)

        else:
            fso.move(old, new)
        return

    def link(self, target, name) -> None:
        """Create a hard link pointing to target."""
        #os.link(self._full_path(name), self._full_path(target))
        return

    def utimens(self, path, times=None) -> None:
        if not times: times = (time.time()) * 2
        info = {'details': {
            'accessed': times[0],
            'modified': times[1],
        }}
        return self._fso.setinfo(self._full_path(path), info)

    # File methods
    # ============

    def open(self, path, flags) -> int:
        """Open a file and return a descriptor."""
        full_path = self._full_path(path)
        str_flags = self._flags_in_object(flags, os) or 'r'
        mode = ''.join(self._mode_from_flags(str_flags)) if not str_flags == 'r' else str_flags
        if not mode: mode = 'r'
        logger.info(f'Flags for opening {full_path}: {str_flags}; mode: "{mode}"')
        fo = self._fso.openbin(full_path, mode)
        return self._path_to_fd(full_path, fo)

    def create(self, path, mode, fi=None) -> int:
        full_path = self._full_path(path)
        str_flags = self._flags_in_object(mode, os) or 'w'
        mode_list = self._mode_from_flags(str_flags) if not str_flags == 'w' else str_flags
        logger.info(f'Flags for creating {full_path}: {str_flags}')
        self._fso.create(full_path)
        fo = self._fso.openbin(full_path, mode_list)
        return self._path_to_fd(full_path, fo)

    def read(self, path, length, offset, fh):
        fo = self._fd_to_obj(fh)
        fo.seek(offset)
        return fo.read(length)

    def write(self, path, buf, offset, fh) -> int:
        fo = self._fd_to_obj(fh)
        fo.seek(offset)
        return fo.write(buf)

    def truncate(self, path, length, fh=None) -> None:
        """Truncate file to specified number of bytes."""
        fso = self._fso
        fso.openbin(path, 'w+').write(fso.openbin(path).read()[length])
        return

    def flush(self, path, fh) -> None:
        """Write buffered data."""
        self._fd_to_obj(fh).flush()
        return

    def release(self, path, fh) -> None:
        """Close a file."""
        fo = self._fd_to_obj(fh)
        fo.close()
        del self._objs[fh]
        del self._fds[self._full_path(path)]
        return

    def fsync(self, path, fdatasync, fh) -> None:
        return self.flush(path, fh)


def get_input(text, pattern=r'.*(\[\[(\w|:)+\]\]).*', sep=':'):
    """Get input for placeholders."""
    # TODO: move to utils
    n_text = text
    pat_rx = re.compile(pattern)

    while True:
        rep = None
        match = pat_rx.match(n_text)
        if not match: break
        f_targ = match.group(1)
        targ = f_targ.replace('_', ' ')[2:-2]

        if targ.startswith(f'hide{sep}'):
            targ = targ.partition(f'{sep}')[-1]
            rep = getpass(f'Enter {targ}: ')

        elif targ.startswith(f'conf{sep}'):
            raise NotImplementedError('Reading from config file n/a')

        else:
            rep = input(f'Enter {targ}: ')
        n_text = n_text.replace(f_targ, rep)
    return n_text

def mount_fs(mp, root, create=False, write=False, debug=False):
    """Mount specified resource root on a mount point."""
    args = sys.argv[1:]

    if mp.startswith('~'):
        mp = mp.replace('~', os.environ.get('HOME') or '~')
    mp = os.path.abspath(mp)

    if not os.path.isdir(mp):
        raise OSError(f'{mp} is not a valid directory')

    if len(args) > 2:
        create = 'create' in args
        write =  'write' in args
    print(f'Mounting {root} at {mp}')
    root = get_input(root)

    try:
        FUSE(FuseFS(root, create, write, debug), mp, nothreads=True, foreground=True)

    except Exception as e:
        logger.exception(repr(e))
    return


if __name__ == '__main__':
    mount_fs(sys.argv[2], sys.argv[1])

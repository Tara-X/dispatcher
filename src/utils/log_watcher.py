#!/usr/bin/env python

"""
Real time log files watcher supporting log rotation.
Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
License: MIT
Link: http://code.activestate.com/recipes/577968-log-watcher-tail-f-log/
"""

"""
    New Features
    Author: SRK.Lyu <superalsrk@gmail.com>
    1. Support OSX (just for file.readlines()'s behavior is different between linux and osx)
    2. Support watching particular file
"""
import os
import time
import errno
import stat


class LogWatcher(object):
    """Looks for changes in all files of a directory.
    This is useful for watching log file changes in real-time.
    It also supports files rotation.
    Example:
    >>> def callback(filename, lines):
    ...     print filename, lines
    ...
    >>> l = LogWatcher("/var/log/", callback)
    >>> l.loop()
    """

    def __init__(self, location, callback, extensions=["log"], tail_lines=100):
        """Arguments:
        (str) @location:
            the location to watch
        (callable) @callback:
            a function which is called every time a new line in a 
            file being watched is found; 
            this is called with "filename" and "lines" arguments.
        (list) @extensions:
            only watch files with these extensions
        (int) @tail_lines:
            read last N lines from files being watched before starting
        """
        self.files_map = {}
        self.callback = callback
        self.location = os.path.realpath(location)
        self.extensions = extensions

        assert os.path.exists(self.location)
        assert callable(callback), repr(callback)
        self.update_files()
        # The first time we run the script we move all file markers at EOF.
        # In case of files created afterwards we don't do this.
        for id, file in self.files_map.iteritems():
            file.seek(os.path.getsize(file.name))  # EOF
            if tail_lines:
                lines = self.tail(file.name, tail_lines)
                if lines:
                    for line in lines:
                        self.callback(file.name, line)
            
    def __del__(self):
        self.close()

    def loop(self, interval=0.1, async=False):
        """Start the loop.
        If async is True make one loop then return.
        """
        while 1:
            self.update_files()
            for fid, file in list(self.files_map.iteritems()):
                self.readfile(file)

            if async:
                print 'async return'
                return

            time.sleep(interval)

    def log(self, line):
        """Log when a file is un/watched"""
        print line

    def listdir(self):
        """List directory and filter files by extension.
        You may want to override this to add extra logic or
        globbling support.
        """
        ls = os.listdir(self.location)
        if self.extensions:
            return [x for x in ls if os.path.splitext(x)[1][1:] \
                                           in self.extensions]
        else:
            return ls

    @staticmethod
    def tail(fname, window):
        """Read last N lines from file fname."""
        try:
            f = open(fname, 'r')
        except IOError, err:
            if err.errno == errno.ENOENT:
                print 'ENOENT error'
                return []
            else:
                print 'Raise error'
                raise
        else:
            BUFSIZ = 1024
            f.seek(0, os.SEEK_END)
            fsize = f.tell()
            block = -1
            data = ""
            exit = False
            while not exit:
                step = (block * BUFSIZ)
                if abs(step) >= fsize:
                    f.seek(0)
                    exit = True
                else:
                    f.seek(step, os.SEEK_END)
                data = f.read().strip()
                if data.count('\n') >= window:
                    break
                else:
                    block -= 1
            return data.splitlines()[-window:]

    def update_files(self):
        ls = []

        if os.path.isdir(self.location):
            for name in self.listdir():
                absname = os.path.realpath(os.path.join(self.location, name))
                try:
                    st = os.stat(absname)
                except EnvironmentError, err:
                    if err.errno != errno.ENOENT:
                        raise
                else:
                    if not stat.S_ISREG(st.st_mode):
                        continue
                    fid = self.get_file_id(st)
                    ls.append((fid, absname))
        else:
            try:
                st = os.stat(self.location)
            except  EnvironmentError, err:
                    if err.errno != errno.ENOENT:
                        raise
            else:
                if stat.S_ISREG(st.st_mode):
                    fid = self.get_file_id(st)
                    ls.append((fid, self.location))

        # check existent files
        for fid, file in list(self.files_map.iteritems()):
            try:
                st = os.stat(file.name)
            except EnvironmentError, err:
                if err.errno == errno.ENOENT:
                    self.unwatch(file, fid)
                else:
                    raise
            else:
                if fid != self.get_file_id(st):
                    # same name but different file (rotation); reload it.
                    self.unwatch(file, fid)
                    self.watch(file.name)

        # add new ones
        for fid, fname in ls:
            if fid not in self.files_map:
                self.watch(fname)

    def readfile(self, file):
        lines = file.readline()
        if lines:
            self.callback(file.name, lines)

    def watch(self, fname):
        try:
            file = open(fname, "r")
            fid = self.get_file_id(os.stat(fname))
        except EnvironmentError, err:
            if err.errno != errno.ENOENT:
                raise
        else:
            self.log("watching logfile %s" % fname)
            self.files_map[fid] = file

    def unwatch(self, file, fid):
        # file no longer exists; if it has been renamed
        # try to read it for the last time in case the
        # log rotator has written something in it.
        lines = self.readfile(file)
        self.log("un-watching logfile %s" % file.name)
        del self.files_map[fid]
        if lines:
            self.callback(file.name, lines)

    @staticmethod
    def get_file_id(st):
        return "%xg%x" % (st.st_dev, st.st_ino)

    def close(self):
        for id, file in self.files_map.iteritems():
            file.close()
        self.files_map.clear()


if __name__ == '__main__':

    def callback(filename, lines):
        print filename, lines

    #watcher = LogWatcher("/tmp/st/", callback, extensions=None)
    watcher = LogWatcher("/tmp/st/s.txt", callback, extensions=None)
    watcher.loop()
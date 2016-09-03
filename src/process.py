#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import signal
import plugins
import traceback

class Subprocess(object):
    def __init__(self, module = None, idx = 0):
        self.module = module
        self.idx = idx
        self.pid = 0
    
    def spawn(self):
        try:
            pid = os.fork()
        except OSError as why:
            if code == errno.EAGAIN:
                # process table full
                msg  = ('Too many processes in process table to spawn %r' %
                        self.config.name)
            else:
                msg = 'unknown error during fork for %r: %s' % (
                      self.config.name, errno.errorcode.get(code, code))
            return

        if pid != 0:
            return self._spawn_as_parent(pid)
        else:
            return self._spawn_as_child()
        

    def _spawn_as_parent(self, pid):
        self.pid = pid
        return pid
    
    def _spawn_as_child(self):

        self.pid = os.getpid()

        try:
            worker = plugins.module(self.module).ExpandWorker(idx = self.idx)
            worker.run()
            
        except:
            print 'exception occurs'
            traceback.print_exc()
        finally:
            os._exit(0) 
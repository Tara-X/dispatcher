# -*- coding: utf-8 -*-

from plugins import BaseWorker

import os
import sys
import time

import random



class ExpandWorker(BaseWorker):

    def run(self):
        print '=====> child process:', os.getpid()
        
        # while True:

        #     print 'start demo 01'
        #     time.sleep(3)

        while True:

            if self.is_valid() == False:
                os._exit(-1)

            time.sleep(3)

            #print 'child process parent pid', os.getppid()

            if random.randint(0, 100)  < 20:
                raise Exception('wrong')
                os._exit(-1)
                pass
        os._exit(-1)
            
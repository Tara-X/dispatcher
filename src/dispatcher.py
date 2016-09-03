# -*- coding: utf-8 -*-


from process import Subprocess

import os
import time
import signal

if __name__ == '__main__':



    print 'before main pid:', os.getpid(), os.getppid()


 
    #signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    process_list = [Subprocess(module='demo01_worker', idx=x) for x in range(0, 5)]

    for process in process_list:
        process.spawn()




    for process in process_list:
        print 'start waiting pid:', process.pid
        
    
    while True:
        pid, retval = os.wait()
        print '==============pid:', pid, 'retval:', retval

        for process in process_list:
            if process.pid == pid:
                process.spawn()



    print 'MAIN started', os.getpid()
    while True:
        pass
        time.sleep(2)










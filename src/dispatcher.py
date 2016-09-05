# -*- coding: utf-8 -*-


from process import Subprocess

import os
import time
import signal
import traceback

if __name__ == '__main__':



    print 'before main pid:', os.getpid(), os.getppid()


    def custom_hand(a, b):
        print 'xxxx:' , a, b
 
    signal.signal(signal.SIGCHLD, custom_hand)

    process_list = [Subprocess(module='demo01_worker', idx=x) for x in range(0, 5)]

    for process in process_list:
        process.spawn()




    for process in process_list:
        print 'start waiting pid:', process.pid
    

    try:
        while True:
            pid, retval = os.wait()
            print '-----------pid:', pid, 'retval:', retval
    except:
        traceback.print_exc()
    
    ''''
    while True:
        pid, retval = os.wait()
        print '==============pid:', pid, 'retval:', retval

        for process in process_list:
            if process.pid == pid:
                process.spawn()
                '''


    print 'MAIN started', os.getpid()
    while True:
        pass
        time.sleep(2)










#!/usr/bin/env python
import os
import time
#from collector import *
def main():

    # start Python Debugger
    debug = os.environ.get("DEBUG")
    print(debug)
    if debug=="1":
        print(debug=="1")
        import debugpy
        debugpy.listen(("0.0.0.0", 3001))
        print('Attached!')
    # end Python Debugger

    #startcollector()
while 1 != 2:
    time.sleep(2)

if __name__ == '__main__':
    main()

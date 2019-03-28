import demoTest
import termcolor
import pyserv
import sys

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print termcolor.colored("""
        +----------------------------------------+
        |           STARTING HTTP SRV            |
        +----------------------------------------+
        """, 'green')
        pyserv.startHttpSrv()
    elif sys.argv[1] == '-h' or sys.argv[1] == '--h' or sys.argv[1] == 'help':
        print termcolor.colored("""
        +----------------------------------------+
        |               NEED HELP?               |
        +----------------------------------------+
        """, 'green')
        print """
        NAME
                piheatincontroller.py
        SYNOPSIS
                python piheatincontroller.py [-h | -t | -c]
        DESCRIPTION
            -h  to show this help
            -t  to execute in test mode
            -c  to execute in configuration mode. Used to register sensors

        """
    elif sys.argv[1] == '-c':
        print termcolor.colored("""
        +----------------------------------------+
        |         CONFIGURATION MODE             |
        +----------------------------------------+
        """, 'green')
        pyserv.startHttpSrv(bool(True))
    elif sys.argv[1] == '-t':
        print termcolor.colored("""
        +----------------------------------------+
        |         STARTING IN DEMO MODE          |
        +----------------------------------------+
        """, 'green')
        demoTest.startDemo()
    else:
        print '\nERROR: invalid argument. -h option for help mode'

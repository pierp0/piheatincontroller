import demoTest
import termcolor
import sys

if __name__ == "__main__":
    if len(sys.argv) == 1:
        pass
    elif sys.argv[1] == '-h' or sys.argv[1] == '--h' or sys.argv[1] == 'help':
        print termcolor.colored("""
        +----------------------------------------+
        |               NEED HELP?               |
        +----------------------------------------+
        """, 'green')
        print """
        NAME
                Manager.py
        SYNOPSIS
                python Manager.py [-h|-d]
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
    elif sys.argv[1] == '-t':
        print termcolor.colored("""
        +----------------------------------------+
        |         STARTING IN DEMO MODE          |
        +----------------------------------------+
        """, 'green')
        demoTest.startDemo()
    else:
        print '\nERROR: invalid argument. -h option for help mode'

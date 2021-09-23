__docformat__ = "restructuredtext en"

# For run_cmd
import select
from popen2 import Popen3
import time
import sys, os
import fcntl


def make_non_blocking(fd):
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NDELAY)


def run_cmd(cmd, timeout=5):
    """ run_cmd(cmd, timeout) --> (out, err, retval)

    Run a given command (cmd) and return its out and err streams as python strings
    and the command's return value as an integer. If the process doesn't produce
    output for <timeout> number of seconds, then the process is killed and the
    output already gathered is returned.
    """
    process = Popen3(cmd, 1)

    retVal = -1
    outStr = ""
    errStr = ""
    lasttime = None

    process.tochild.close()
    outfile = process.fromchild
    errfile = process.childerr
    make_non_blocking(outfile.fileno())
    make_non_blocking(errfile.fileno())

    while 1:
        if process.poll() != -1:
            outStr += outfile.read()
            errStr += errfile.read()
            retVal = process.poll()
            break

        try:
            outTuple = select.select([outfile], [], [], .1)
            errTuple = select.select([errfile], [], [], .1)
        except select.error, e:
            outTuple = ([], [], [])
            errTuple = ([], [], [])
        # Is there output on stdout?
        if outTuple[0]:
            lasttime = time.time()
            outStr += outfile.read()
        # Is there output on stderr?
        if errTuple[0]:
            lasttime = time.time()
            errStr += errfile.read()
        # Was there output on either? If not, check for timeout
        if not (outTuple[0] or errTuple[0]):
            if not lasttime:
                lasttime = time.time()
            elif time.time() - lasttime > timeout:
                errStr += "Command '%s' timed out\n" % cmd
                outStr += "Command '%s' timed out\n" % cmd
                os.system('kill -9 %s' % process.pid)
                retVal = process.poll()
                break
    # Uncomment for debugging purposes
    #            else:
    #                print timeout-(time.time()-lasttime), 'seconds until timeout'

    return (outStr, errStr, retVal)

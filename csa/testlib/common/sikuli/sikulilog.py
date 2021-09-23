# $Id: //prod/main/sarf_centos/testlib/common/sikuli/sikulilog.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $
import os

logfile = 'c:\\tmp\\sikulidebug.log'


def get_length():
    try:
        file = open(logfile)
        file.seek(0, os.SEEK_END)
        ret = file.tell()
        print 'mark=', ret
        return ret
        file.close()
    except:
        print "log file '%s' can't be opened" % logfile
        return 0


def process(mark):
    try:
        file = open(logfile)
        file.seek(mark)
        found_errors = 0
        for item in file.readlines():
            print item,
            if item.startswith('[error]'):
                found_errors += 1

        if found_errors > 0:
            print '*** %s errors in the script' % found_errors
            raise AssertionError('run-time sikuli error')

        file.close()

    except:
        print "log file '%s' can't be opened" % logfile

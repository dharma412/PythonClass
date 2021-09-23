# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/failoverconfig_batch.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import time
import sys

from sal.exceptions import ConfigError
import clictorbase
from failoverconfig import failoverconfig
from clictorbase import IafCliError, REQUIRED, DEFAULT, EXACT, \
                        IafCliParamMap, IafCliConfiguratorBase
TIMEOUT=10

class failoverconfig_batch(clictorbase.IafCliConfiguratorBase):
    errors = failoverconfig.errors

    def __init__(self, sess):
        super(failoverconfig_batch, self).__init__(sess)
        self._set_local_err_dict(self.errors)

    def __call__(self):
        return self

    def execute(self, cmd):
        self.clearbuf()
        try:
            self._writeln(cmd)
            buffer_text = self._wait_for_prompt(timeout=TIMEOUT)
            self._end_command()

            if not buffer_text:
                buffer_text = self.getbuf()
            return buffer_text

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exc_type, exc_value, exc_traceback

    def test(self, groupid, elapse_seconds=2):
        """None means test all
        """
        self.clearbuf()
        cmd = 'failoverconfig TESTFAILOVERGROUP ' + str(groupid)
        try:
            self._writeln(cmd)
            time.sleep(int(elapse_seconds))
            self.interrupt()
            buffer_text = self._wait_for_prompt(timeout=elapse_seconds)
            self._end_command()

            if not buffer_text:
                buffer_text = self.getbuf()
            return buffer_text

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise exc_type, exc_value, exc_traceback

        finally:
            self.interrupt()
            self.interrupt()
            self._restart_nosave()

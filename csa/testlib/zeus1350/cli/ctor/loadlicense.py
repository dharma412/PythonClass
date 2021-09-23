# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/loadlicense.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

"""
Command Line Interface (CLI)
  command:
      cli -> loadlicense
"""

import re
import time

from clictorbase import IafCliConfiguratorBase
from common.util.sarftime import CountDownTimer
from sal.exceptions import TimeoutError

RESULT_SEARCH_PATTERN = \
    r'(Virtual.*(\n.*)+|License has expired.*(\n.*)+|Malformed license.*(\n.*)+)'


class ExpiredLicenseException(Exception):
    pass


class MalformedLicenseException(Exception):
    pass


class loadlicense(IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        # go to top-level command
        self._restart()
        self._writeln('loadlicense')

        while 1:
            try:
                buf = self._read_until('prior to installing the new license file',
                                       timeout=5)
                if buf.find('This command will remove all existing feature key') != -1:
                    self._query_response('Y')
                    break
            except TimeoutError:
                break

        return self

    def _load_license_from_file(self, filename):
        self.clearbuf()
        self._sess.writeln('2')
        self._query_response(filename)

        while 1:
            try:
                self._expect(['-Press Any Key For More-', 'agreement? []'],
                             timeout=10)
                buf = self.getbuf()
                if self._expectindex != 0:
                    if buf.find('Do you accept the above license') != -1:
                        self._writeln('Y')
                        license_info = self._wait_for_prompt()
                        match = re.search(RESULT_SEARCH_PATTERN, license_info, re.DOTALL)
                        if match.group(0):
                            return match.group(0)
                        break
                else:
                    self._writeln("\n")
                    continue
            except TimeoutError:
                break

        result = self._get_license_loading_result()
        self._analyse_license_result(result)

        return result

    def _load_license_from_cli(self, paste_conf):
        self.clearbuf()
        self._writeln('1')
        self._writeln(paste_conf)
        self._writeln('')
        self._writeln('\x04')

        while 1:
            try:
                self._expect(['-Press Any Key For More-', 'agreement? []'],
                             timeout=10)
                buf = self.getbuf()
                if self._expectindex != 0:
                    if buf.find('Do you accept the above license') != -1:
                        self._writeln('Y')
                        license_info = self._wait_for_prompt()
                        match = re.search(RESULT_SEARCH_PATTERN, license_info, re.DOTALL)
                        if match.group(0):
                            return match.group(0)
                        break
                else:
                    self._writeln("\n")
                    continue
            except TimeoutError:
                break

        result = self._get_license_loading_result()
        self._analyse_license_result(result)

        return result

    def _get_license_loading_result(self):
        # the function is needed because sometimes
        # the license output can appear with delay
        SLEEP_INTERVAL = 1
        TIMEOUT = 90
        tmr = CountDownTimer(TIMEOUT).start()
        while tmr.is_active():
            time.sleep(SLEEP_INTERVAL)
            buf = re.search(RESULT_SEARCH_PATTERN,
                            self._sess.getbuf(clear_buf=False), re.DOTALL)
            if buf:
                return buf.group(0)
            else:
                raise TimeoutError('License info did not appear in CLI ' \
                                   'within %d-seconds timeout' % (TIMEOUT))

    def _analyse_license_result(self, result):
        if result.find('License has expired') != -1:
            raise ExpiredLicenseException('License has expired')
        if result.find('Malformed license') != -1:
            raise MalformedLicenseException('Malformed license')

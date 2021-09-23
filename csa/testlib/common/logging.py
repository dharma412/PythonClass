#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/logging.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import time


class Logger:

    def _log(self, message, level='INFO'):
        if level != 'NONE':
            print '*%s* %s %s' \
                  % (level, time.asctime(time.localtime(time.time())), message)

    def _info(self, message):
        self._log(message)

    def _debug(self, message):
        self._log(message, 'DEBUG')

    def _warn(self, message):
        self._log(message, "WARN")

    def _html(self, message):
        self._log(message, 'HTML')

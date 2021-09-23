#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_check_error.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon


class ReportCheckError(guiexceptions.GuiError):
    """ Incorrect values were present on the page
    """

    # The special exception the product page validator
    def __init__(self, msg, page_errors=None):
        self.msg = msg
        if page_errors:
            self.page_errors = page_errors
        else:
            self.page_errors = list()

    def __str__(self):
        return str(self.msg) + ':\n\n' + '\n'.join(map(str, self.page_errors))

    # used by Robot Framework to print message to console and log
    def __unicode__(self):
        return unicode(self.__str__())

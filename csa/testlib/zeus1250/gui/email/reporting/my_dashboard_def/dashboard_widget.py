#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/email/reporting/my_dashboard_def/dashboard_widget.py#3 $
# $DateTime: 2019/06/07 02:45:52 $
# $Author: 

from common.gui.guicommon import Wait

DELETE_BUTTON = lambda locator: "%s//div[@title='Delete']" % (locator,)
CONFIRM_BUTTON = "//button[normalize-space()='Confirm']"
ACTION_RESULT_DIV = \
    "//div[@id='action-results' and not(contains(@style, 'display: none'))]"


class DashboardWidget(object):
    def __init__(self, gui_common, caption, locator):
        self.gui = gui_common
        self._caption = caption
        self._locator = locator

    @property
    def caption(self):
        return self._extract_short_caption(self._caption)

    @property
    def full_caption(self):
        return self._caption

    def _extract_short_caption(self, caption):
        return caption.split('>')[-1].strip()

    def delete(self):
        self.gui.click_button(DELETE_BUTTON(self._locator), 'don\'t wait')
        Wait(self.gui._is_element_present, timeout=5,
             msg='Failed to detect delete confirmation dialog within given timeout')\
                .wait(CONFIRM_BUTTON)
        self.gui.click_button(CONFIRM_BUTTON, 'don\'t wait')
        Wait(self.gui._is_element_present, timeout=10,
             msg='Failed to detect action result after report add action '\
                 'within given timeout').wait(ACTION_RESULT_DIV)
        self.gui._check_action_result()

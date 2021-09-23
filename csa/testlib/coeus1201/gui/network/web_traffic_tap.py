#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/web_traffic_tap.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
import re

SUBMIT = "xpath=//input[@class='submit']"
ENABLE_WTT = "xpath=//input[@id='enabled']"
POLICY_NAME = "xpath=//input[@id='policy_group_id']"
EDIT_SETTINGS = "xpath=//input[@value='Edit Settings']"


class WebTrafficTap(GuiCommon):

    def get_keyword_names(self):
        return [
            'enable_web_traffic_tap'
               ]

    def enable_web_traffic_tap(self):
        self._navigate_to('Network', 'Web Traffic Tap')
        self.click_button(EDIT_SETTINGS, 'dont wait')
        self._select_checkbox(ENABLE_WTT)
        self.click_button(SUBMIT, 'dont wait')


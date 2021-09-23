#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/management/administration/next_steps.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

ERROR_MESSAGE = ''

class NextSteps(GuiCommon):
    """Keywords for Management Appliance -> System Administration ->
    Next Steps
    """

    def get_keyword_names(self):
        return [
                'next_steps_check_links',
                'next_steps_follow_link',
                ]


    def _open_page(self):
        self._navigate_to('Management', 'System Administration',
            'Next Steps')


    def _follow_link(self, link_label):
        global ERROR_MESSAGE
        self._debug(link_label)

        _link_loc = "//a[normalize-space(text())='" + link_label + "']"
        if int(self.get_matching_xpath_count(_link_loc)) > 0:
            self._click("//a[normalize-space(text())='" + link_label + "']")
            return True
        else:
            ERROR_MESSAGE += "Link '%s' was not found.\r\n" % link_label
            return False


    def _check_links(self, expected_links_list):
        global ERROR_MESSAGE
        for _pair in expected_links_list:
            self._debug(_pair)
            _pos = _pair.find(':')
            if _pos <= 0:
                ERROR_MESSAGE += "Pair '%s' has incorrect format.\r\n" % _pair
                continue
            else:
                _label = _pair[0:_pos].strip()
                _title = _pair[_pos + 1:].strip()

            _followed = self._follow_link(_label)
            if _followed:
                _page_title = self.get_title()
                if _page_title.find(_title) < 0:
                    ERROR_MESSAGE += "'%s' page was open by '%s' link.\r\n" % (_page_title, _label)
                self.go_back()


    def next_steps_follow_link(self, link_label=None):
        """Follow a link on 'Next Steps' page.

        Parameters:
            - `link_label`: Label of a link to follow.

        Exceptions:
            - `GuiValueError`: appears if link was not found.

        Examples:
            | Next Steps Follow Link | Configure Security Appliances |
        """
        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        self._open_page()

        self._follow_link(link_label)

        if ERROR_MESSAGE != '':
            raise guiexceptions.GuiValueError(ERROR_MESSAGE)

        self._check_action_result()


    def next_steps_check_links(self, *expected_links):
        """Check that links open correct page on 'Next Steps' page.

        Parameters:
            Pairs of link labels and page titles (opened by these link).
            Label and title should be separated by colon.
            See example below.

        Exceptions:
            - `GuiValueError`: appears if link was not found,
                or incorrect page appears if follow a link.

        Examples:
            | Next Steps Check Links |
            | ... | Configure Security Appliances : Configure Security Appliances |
            | ... | Spam Quarantine : Spam Quarantine |
            | ... | Centralized Email Reporting : Centralized Email Reporting |
            | ... | Centralized Email Message Tracking : Centralized Email Message Tracking |
            | ... | Centralized Web Configuration Manager : Centralized Web Configuration Manager |
            | ... | Centralized Web Reporting : Centralized Web Reporting |
            | ... | Enter Feature Keys : Enter Feature Keys |
            | ... | Send Configuration File : Send Configuration File |
        """
        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        self._open_page()

        self._check_links(expected_links)

        if ERROR_MESSAGE != '':
            raise guiexceptions.GuiValueError(ERROR_MESSAGE)

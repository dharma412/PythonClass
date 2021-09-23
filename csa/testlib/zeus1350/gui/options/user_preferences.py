#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/options/user_preferences.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

from common.gui.guicommon import GuiCommon
from string import capwords
import common.gui.guiexceptions as guiexceptions

LIST_LABEL = lambda item: 'label=%s' % (item,)
EDIT_PREFERENCES_BUTTON = 'action:FormEdit'
LANGUAGE_LIST = 'language'
LANDING_PAGE_LIST = 'landing_page'
TIME_RANGE_LIST = 'date_range'
REPORT_ROWS_LIST = 'display_rows'
LIST_LABEL = lambda item: 'label=%s' % (item,)
OPTION_MENU = "//a[text()='Options' and contains(@class, 'menubar')]"
PREFERENCES_MENU = "xpath=//a[contains(@href,'/user_preferences')]"
SUBMIT_BUTTON = "xpath=//input[@class='submit']"


class UserPreferences(GuiCommon):
    """
        Keyword library for WebUI page Options -> Preferences
    """

    def get_keyword_names(self):
        return ['user_preferences_edit', ]

    def _open_page(self):
        self.mouse_over(OPTION_MENU)
        self.click_link(PREFERENCES_MENU)

    def _select_item_from_list(self, select_list, item, list_name):

        if item is None:
            return

        if not self._is_element_present(select_list):
            raise guiexceptions.GuiFeatureDisabledError( \
                '%s list is not available' % (list_name,))

        splitter_position = int(item.rfind(' > '))
        group_name = ''
        item_name = ''

        if (splitter_position > -1):
            group_name = item[0:splitter_position]
            item_name = item[(splitter_position + 3):]

        location_prefix = '//select[@name=\'' + select_list + '\']'
        optgroups = int(self.get_matching_xpath_count(location_prefix \
                                                      + '/optgroup[@label]'))

        if (optgroups > 0) and item != "":
            group_loc = location_prefix + '/optgroup[@label=\'' + group_name + '\']'

            if (int(self.get_matching_xpath_count(group_loc)) > 0):
                item_loc = group_loc + '/option[contains(text(),\'' + item_name + '\')]'

                if (int(self.get_matching_xpath_count(item_loc)) > 0):
                    self.click_element(item_loc)
                else:
                    raise ValueError('"%s" item of "%s" in "%s" list is not avaliable' % \
                                     (item_name, group_name, list_name))
            else:
                raise ValueError('"%s" group in %s list is not avaliable' % \
                                 (group_name, list_name))
        else:
            options = self.get_list_items(select_list)
            item = str(item)

            for option in options:
                if item in option:
                    self.select_from_list(select_list, LIST_LABEL(option))
                    break
            else:
                raise ValueError('%s option in %s list is not avaliable' % \
                                 (item, list_name))

    def user_preferences_edit(self, language=None, landing_page=None, \
                              time_range=None, rows_num=None):
        """Edit user preferences settings.

        *Parameters*
             All parameters must be provided in language which is currently
             configured on appliance. Be aware about encoding  for non english
             characters.
            - `language`: display language to use. String. This string will be
               compared with strings in list. Default value will left language
               settings unchanged.
               It is recommended to use official abbreviation of language.
            - `landing_page`: landing page title to use. String. Must be
               provided in form Menu1 > [Menu2 >] Item.  Default value
               will left landing page unchaged.
            - `time_range`: reporting time range displayed. String.
               Default value will lest  time range unchanged.
            - `rows_num`: the number of reporting rows displayed. String.
               Default value will left rows number unchanged.

        *Return*
            None.

        *Exceptions*
            - `ValueError`: in case of invalid value for any of the
                 input parameters.
            - `GuiFeatureDisabledError`: in case any of the provided
                 parameters is no applicable to the user.

        *Examples*
            | User Preferences Edit | language=ru |
            | ... | landing_page=Management Appliance > System Administartion > Alerts |
            | ... | time_range=Week | rows_num=100 |
            | User Preferences Edit | language=en |
        """
        self._open_page()

        self.click_button(EDIT_PREFERENCES_BUTTON)

        if language != None:
            language = language.lower()

        for options in ((LANGUAGE_LIST, language, 'Language Display'),
                        (LANDING_PAGE_LIST, landing_page, 'Landing Page'),
                        (TIME_RANGE_LIST, time_range, 'Reporting Time Range'),
                        (REPORT_ROWS_LIST, rows_num, 'Reporting Rows Displayed')
                        ):
            self._select_item_from_list(*options)

        self.click_button(SUBMIT_BUTTON)

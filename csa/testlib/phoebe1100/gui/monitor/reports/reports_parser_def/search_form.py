#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/monitor/reports/reports_parser_def/search_form.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, check_new_settings, \
    get_module_inputs_pairs

SEARCH_FOR_COMBO = ('search_option',
                    "//select[@id='search_dest']")
SEARCH_TEXT = ('search_text',
               "//input[@id='search_page']")
SEARCH_MATCH_COMBO = ('match_option',
                      "//select[@id='search_option']")
SEARCH_BUTTON = "//input[@value='Search']"


class SearchForm(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @check_new_settings
    def _set_combo_case_insensitive(self, settings, setting_name, combo_locator):
        if setting_name in settings:
            available_options = self.gui.get_list_items(combo_locator)
            value_to_set = settings[setting_name]
            for option in available_options:
                if option.lower().startswith(value_to_set.lower()):
                    self.gui.select_from_list(combo_locator, option)
                    return
            raise ValueError('There is no option named "%s" in ' \
                             'setting "%s"' % (value_to_set, setting_name))

    def _set_combos_case_insensitive(self, settings, *pairs):
        for caption, locator in pairs:
            self._set_combo_case_insensitive(settings, caption, locator)

    def get_contained_elements_names(self):
        return map(lambda x: x[0], self._get_registered_inputs())

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_combos_case_insensitive(new_value,
                                          SEARCH_FOR_COMBO,
                                          SEARCH_MATCH_COMBO)
        self._set_edits(new_value,
                        SEARCH_TEXT)

    def start_search(self):
        self.gui.click_button(SEARCH_BUTTON)

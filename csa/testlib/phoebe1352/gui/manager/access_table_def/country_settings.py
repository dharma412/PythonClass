#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/access_table_def/country_settings.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs
from common.gui.guiexceptions import ConfigError, GuiPageNotFoundError

SENDER_TYPE_COUNTRY = "//input[@id='sender_type_countries']"
COUNTRY = lambda index: \
        "//select[@id='country_selection[%s][country]']" % index
COMMENT = lambda index: \
        "//input[@id='country_selection[%s][comment]']" % index
ADD_ROW_BUTTON = "//input[@id='country_selection_domtable_AddRow']"
COUNTRY_EDIT = "//select[@id='country_edit']"
COUNTRY_EDIT_COMMENT = "//input[@id='country_edit_comment']"

class CountrySettings(InputsOwner):

    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, countries):
        if self._listener.lower() == 'outboundmail':
            raise GuiPageNotFoundError('Geo location feature is not available for Outbound mails')
        if self._method == 'add':
            self.gui._click_radio_button(SENDER_TYPE_COUNTRY)
            index = 0
            for country in countries.keys():
                if index > 0:
                    self.gui.click_button(ADD_ROW_BUTTON, "don't wait")
                country_names = self.gui.get_list_items(COUNTRY(index))
                if country in country_names:
                    self.gui.select_from_list(COUNTRY(index), country)
                    self.gui.input_text(COMMENT(index), countries[country])
                else:
                    raise ValueError('There is no country with name %s' % country)
                index += 1
        elif self._method == 'edit':
            self.gui.select_from_list(COUNTRY_EDIT, countries['new_country'])
            self.gui.input_text(COUNTRY_EDIT_COMMENT, countries['new_comment'])
        else:
            raise ConfigError('Unknow method [%s] pass for Geo location feature' % self._method)

    @set_speed(0, 'gui')
    def get(self):
        return NotImplementedError()

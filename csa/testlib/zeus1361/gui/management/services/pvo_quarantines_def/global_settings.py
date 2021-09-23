#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/management/services/pvo_quarantines_def/global_settings.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs, \
                                    check_new_settings

QUARANTINE_IP_INTERFACE = ( 'Quarantine IP Interface',
                            "//select[@id='interface']")
QUARANTINE_PORT = ( 'Quarantine Port', "//input[@id='port']")

ENABLE_CQ_FOR_PVO_CHECKBOX = ( 'Enable Centralized Quarantines service',
                               "//input[@type='checkbox' and @name='enabled']")

ENABLE_BUTTON = "//input[@type='button' and contains(@value, 'Enable')]"
EDIT_GLOBAL_SETTINGS__BUTTON = "//input[@type='button' "\
                            "and contains(@value, 'Edit Global Settings...')]"


class PVOGlobalSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value,
                        ENABLE_CQ_FOR_PVO_CHECKBOX,)
        self._set_combos(new_value,
                        QUARANTINE_IP_INTERFACE,)
        self._set_edits(new_value,
                        QUARANTINE_PORT,)


    @check_new_settings
    def _set_combo(self, settings, setting_name, combo_locator):
        if settings.has_key(setting_name):
            all_options = self.gui.get_list_items(combo_locator)
            value_to_set = settings[setting_name]
            dest_options = filter(lambda x: x.find(value_to_set) >= 0, all_options)
            if not dest_options:
                raise ValueError('There is no option that includes "%s" in '\
                                 'setting "%s"' % (value_to_set,
                                                   setting_name))
            self.gui.select_from_list(combo_locator, dest_options[0])


    def get(self):
        raise NotImplementedError()
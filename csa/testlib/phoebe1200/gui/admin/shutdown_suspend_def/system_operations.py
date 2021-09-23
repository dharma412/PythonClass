#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/admin/shutdown_suspend_def/system_operations.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

OPERATION_COMBO = ('Operation',
                   "//select[@id='halt_action']")
DELAY = ('Connections Close Timeout',
         "//input[@name='delay']")

COMMIT_BUTTON = "//input[@name='Submit']"


class SystemOperationsForm(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        assert (OPERATION_COMBO[0] in new_value)
        self._set_combos(new_value,
                         OPERATION_COMBO)
        self._set_edits(new_value,
                        DELAY)

    def commit(self):
        self.gui.click_button(COMMIT_BUTTON)
        self.gui._check_action_result()

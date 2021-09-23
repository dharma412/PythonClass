#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/services/scan_behaviour_def/import_form.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

FILE_NAME_COMBO = ('File Name',
                   "//select[@name='filename']")


class ImportForm(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_combos(new_value,
                         FILE_NAME_COMBO)

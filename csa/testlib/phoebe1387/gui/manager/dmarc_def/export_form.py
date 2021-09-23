#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/dmarc_def/export_form.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs


FILE_TO_EXPORT = ('File to Export',
                  "//input[@id='expfile']")


class ExportForm(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_edits(new_value,
                        FILE_TO_EXPORT)

    def perform_export(self):
        self.gui._click_submit_button()

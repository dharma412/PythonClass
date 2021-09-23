#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/network/certificates_def/import_settings.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.gui.decorators import go_to_page, set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

CERTIFICATE_PATH = "cert_file"
CERTIFICATE_PASSWORD = "//input[@id='cert_pass']"
CERTIFICATE_NAME = "//input[@id='cert_name']"
NEXT_BUTTON = "//input[starts-with(@value, 'Next') and @type='button']"


class ImportSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        browse_element = self.gui._selenium.find_element_by_name(
            CERTIFICATE_PATH)
        browse_element.send_keys(new_value['Path'])
        self.gui.input_text(CERTIFICATE_PASSWORD, new_value['Password'])
        self.gui.click_button(NEXT_BUTTON)
        self.gui._wait_until_element_is_present(CERTIFICATE_NAME)
        self.gui.input_text(CERTIFICATE_NAME, new_value['Name'])

#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/servicepassword.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from common.gui.guicommon import GuiCommon
import time
import re
from common.util.systools import SysTools

LOAD_BUTTON = 'xpath=//input[@value="Load"]'


class ServicePassword(GuiCommon):
    """
    """

    def get_keyword_names(self):
        return ['generate_password_for_service_user']

    def generate_password_for_service_user(self, service_password=None, serial=None, clear_previous=False):
        """Generates password for the service user.
           Used in combination with techsupport-> SSHACCESS cli command

        Parameters:
        - `service_password`: The user Supplied Service Password.
                              Required.

        - `serial`: The serial # of the DUT.
                By default is populated with the current DUT's serial number.

        - `clear_previous`: Either True of False.
                            Can be used to generate a fresh key.

        Returns:
        - The service password string that is generated.

        Example:

        | ${password}=   Generate password for service user | service_password=ironport  |

        """

        self._perform_login()
        self._select_service_password_from_drop_down()
        self._type_serial_number()
        self._type_service_password(service_password=service_password)
        if clear_previous:
            self._clear_previous()
        self._click_create()
        return self._parse_license_key()

    def _select_service_password_from_drop_down(self):
        option_select = "xpath=//select[@id='keyType']"
        self.select_from_list(option_select, 'Service Password')

    def _perform_login(self):
        self._open_login_page()
        self._set_login_name()
        self._set_login_password()
        self._click_login_button()

    def _open_login_page(self):
        self.open_browser('http://jester.mfg/key')

    def _set_login_name(self, value='testuser'):
        FIELD = "xpath=//input[@name='login']"
        self.input_text(FIELD, value)

    def _set_login_password(self, value='ironport'):
        FIELD = "xpath=//input[@name='password']"
        self.input_text(FIELD, value)

    def _click_login_button(self):
        button = "xpath=//input[@name='Login']"
        self.click(button)

    def _type_serial_number(self, serial=None):

        if not serial:
            serial = SysTools(self.dut, self.dut_version)._get_dut_serial()
        FIELD = "xpath=//input[@name='serialNumber']"
        self.input_text(FIELD, serial)

    def _type_service_password(self, service_password=None):
        if not service_password:
            raise ValueError, 'value cannot be None, Given- %s ' % service_password
        FIELD = "xpath=//input[@name='userSuppliedPass']"
        self.input_text(FIELD, service_password)

    def _click_create(self):
        create_button = "xpath=//input[@name='key']"
        self.click(create_button)
        self.wait_until_page_loaded(timeout=5000)

    def _clear_previous(self):
        clear_checkbox = "xpath=//input[@id='cb_clear']"
        self.click(clear_checkbox)

    def _parse_license_key(self):
        pattern = 'Key: *([\w]+)'
        text = self._get_text('//body')
        license_key = (re.search(pattern, text)).group(1)
        self._log('License that was generated is %s' % license_key)
        return license_key

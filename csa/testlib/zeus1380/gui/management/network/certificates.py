import common.gui.guiexceptions as guiexceptions

from common.gui.guicommon import GuiCommon

EDIT_SETTING_BUTTON = "//input[@value='Edit Settings...']"
CERT_CUSTOM_LIST_ENABLE_RADIO = "//input[@id='custom_ca_enable']"
CERT_CUSTOM_LIST_DISABLE_RADIO = "//input[@id='custom_ca_disable']"
CERT_CUSTOM_LIST_ENABLE_BROWSE_BUTTON = "//input[@id='custom_ca_file_upload']"
CERT_SYSTEM_LIST_ENABLE_RADIO = "//input[@id='system_ca_enable']"
CERT_SYSTEM_LIST_DISABLE_RADIO = "//input[@id='system_ca_disable']"
MANAGE_TRUSTED_ROOT_CERT_BUTTON = "//input[@value='Manage Trusted Root Certificates...']"
CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE = "//dl/dt[contains(text(),'Custom Trusted Root Certificates')]/../dd/table[@class='cols']/tbody"
CISCO_TRUSTED_ROOT_CERTIFICATE_TABLE = "//dl/dt[contains(text(),'Cisco Trusted Root Certificate List')]/../dd/table[@class='cols']/tbody"
DELETE_BUTTON = "//button[contains(text(),'Delete')]"
CUSTOM_TRUSTED_ROOT_CERTIFICATE_SUBMIT_BUTTON = "//input[@value='Submit'][1]"
CISCO_TRUSTED_ROOT_CERTIFICATE_SUBMIT_BUTTON = "//input[@value='Submit'][2]"
CERTIFICATE_AUTHORITIES_CUSTOM_LIST_STATUS = "//dl/dt[contains(text(),'Certificate Authorities')]/../dd/table[@class='pairs']/tbody/tr[1]/td"
CERTIFICATE_AUTHORITIES_SYSTEM_LIST_STATUS = "//dl/dt[contains(text(),'Certificate Authorities')]/../dd/table[@class='pairs']/tbody/tr[2]/td"
CISCO_TRUSTED_ROOT_CERTIFICATE_OVERRIDE_TRUST = "//*[@id='standard_row_{}']/td[3]/input"


class Certificates(GuiCommon):

    """Keywords for Management Appliance -> Network -> IP Interfaces"""

    def get_keyword_names(self):
        return ['click_edit_settings_cert_authorities',
                'cert_authorities_custom_list_enable_disable',
                'cert_authorities_system_list_enable_disable',
                'edit_certificate_authorities',
                'get_all_custom_trusted_root_cert',
                'delete_custom_trusted_root_cert',
                'get_certificate_authority_status',
                'get_custom_trusted_root_cert_detail',
                'override_trusted_root_certificate',
                ]

    def _open_page(self):
        self._navigate_to('Management', 'Network', 'Certificates')

    def _fill_local_file_path(self, filepath):
        self.choose_file(CERT_CUSTOM_LIST_ENABLE_BROWSE_BUTTON, filepath)
        self._info('Set local file path to "%s".' % (filepath,))

    def _click_enable_cert_custom_list(self):
        self.click_button(CERT_CUSTOM_LIST_ENABLE_RADIO, "don't wait")
        self._info('Clicked "Enable Certificate Authorities Custom List" radiobutton.')

    def _click_disable_cert_custom_list(self):
        self.click_button(CERT_CUSTOM_LIST_ENABLE_RADIO, "don't wait")
        self._info('Clicked "Disable Certificate Authorities Custom List" radiobutton.')

    def _click_enable_cert_system_list(self):
        self.click_button(CERT_CUSTOM_LIST_ENABLE_RADIO, "don't wait")
        self._info('Clicked "Enable Certificate Authorities System List" radiobutton.')

    def _click_disable_cert_system_list(self):
        self.click_button(CERT_CUSTOM_LIST_ENABLE_RADIO, "don't wait")
        self._info('Clicked "Disable Certificate Authorities System List" radiobutton.')

    def click_edit_settings_cert_authorities(self):
        self._open_page()
        self.click_button(EDIT_SETTING_BUTTON)
        self._info('Clicked "Certificate Authorities Edit Setting" button.')

    def click_manage_trusted_root_cert(self):
        self._open_page()
        self.click_button(MANAGE_TRUSTED_ROOT_CERT_BUTTON)
        self._info('Clicked "Manage Trusted root Certificates" button.')

    def click_submit_button(self):
        self._click_submit_button()
        self._info('Clicked "Edit Certificate Authorities Submit" button.')

    def _click_delete_button(self):
        try:
            self._wait_for_confirm_dialog()
        except:
            self._warn('Confirmation Dialog did not appear')

        try:
            self.click_button(DELETE_BUTTON)
            self._info('Clicked delete_button button')
        except:
            self._warn('Continue button did not appear')


        return self._check_action_result()

    def cert_authorities_custom_list_enable_disable(self, enable=False, cert_path=None):
        """Enable Disable the Certificate Authorities Custom list

                *Parameters*
                    - `enable`: If true it will enable the Custom list. Boolean.
                    Default value is ${False}.
                    - 'cert_path' : If enable is true and cert_path is provided it will choose the
                    cert file provided in path. String.
                    Default value is None.

                *Exeptions*
                    None.

                *Examples*
                | Cert Authorities Custom List Enable Disable | enable=${True} | cert_path=testdata/CA.pem |
                | Cert Authorities Custom List Enable Disable | enable=${True} |
                | Cert Authorities Custom List Enable Disable | enable=${False} |
        """
        if enable:
            self.click_button(CERT_CUSTOM_LIST_ENABLE_RADIO, "don't wait")
            if cert_path is not None:
                self._fill_local_file_path(cert_path)
        else:
            self.click_button(CERT_CUSTOM_LIST_DISABLE_RADIO, "don't wait")

    def cert_authorities_system_list_enable_disable(self, enable=False):
        """Enable Disable the Certificate Authorities System list

                *Parameters*
                    - `enable`: If true it will enable the System list. Boolean.
                    Default value is ${False}.

                *Exeptions*
                    None.

                *Examples*
                | Cert Authorities System List Enable Disable | enable=${True} |
                | Cert Authorities System List Enable Disable | enable=${False} |
        """

        if enable:
            self.click_button(CERT_SYSTEM_LIST_ENABLE_RADIO, "don't wait")
        else:
            self.click_button(CERT_SYSTEM_LIST_DISABLE_RADIO, "don't wait")

    def edit_certificate_authorities(self, custom_list_enable=False,
                                     system_list_enable=False,
                                     custom_list_cert_path=None):
        """Main Funtion to work on edit certificate authorities page.

                *Parameters*
                    - `custom_list_enable`: If true it will enable the Custom list. Boolean.
                    Default value is ${False}.
                    - 'custom_list_cert_path' : If enable is true and cert_path is provided it will choose the
                    cert file provided in path. String.
                    - `system_list_enable`: If true it will enable the System list. Boolean.
                    Default value is ${False}.

                *Exeptions*
                    None.

                *Examples*
                | Edit Certificate Authorities | custom_list_enable=${True} | custom_list_cert_path=testdata/CA.pem | system_list_enable=${True}|
                | Edit Certificate Authorities | custom_list_enable=${True} | system_list_enable=${True}|
                | Edit Certificate Authorities | custom_list_enable=${False} |system_list_enable=${False}|
        """
        self.click_edit_settings_cert_authorities()
        self.cert_authorities_custom_list_enable_disable(custom_list_enable, custom_list_cert_path)
        self.cert_authorities_system_list_enable_disable(system_list_enable)
        self._click_submit_button()

    def get_all_custom_trusted_root_cert(self):
        """Return the list of custom certificates"""

        self.click_manage_trusted_root_cert()
        cert_list = self._get_element_list(CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE)
        self._info("Custom Cert List : %s" % cert_list)
        return cert_list

    def delete_custom_trusted_root_cert(self, cert_name):
        """Delete a certificate with given name

                *Parameters*
                    - `cert_name`: Certificate Name to be deleted. String.
                    Default value is NONE.
        """
        cert_list = self.get_all_custom_trusted_root_cert()
        if cert_name in cert_list:
            cert_index = cert_list.index(cert_name) + 2
            delete_button_xpath = CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE + "/tr[%s]/td[4]/img" % cert_index
            self.click_element(delete_button_xpath, "don't wait")
            print delete_button_xpath
            self._click_delete_button()
            self.click_button(CUSTOM_TRUSTED_ROOT_CERTIFICATE_SUBMIT_BUTTON)
        else:
            raise ValueError('`%s` Certificate is not present on the page' % (cert_name,))

    def get_custom_trusted_root_cert_detail(self, cert_name):
        """Return the certificate details

                *Parameters*
                    - `cert_name`: Certificate Name to be deleted. String.
                    Default value is NONE.
        """
        cert_details = {}
        cert_list = self.get_all_custom_trusted_root_cert()
        if cert_name in cert_list:
            cert_index = cert_list.index(cert_name) + 2
            cert_link = CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE + "/tr[%s]/td[1]" % cert_index
            expiry_link = CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE + "/tr[%s]/td[2]" % cert_index
            on_cisco_list = CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE + "/tr[%s]/td[3]" % cert_index

            self.click_element(cert_link + '/a', "don't wait")

            cert_details['custom_name'] = self._get_text(cert_link + "/div/table/tbody/tr[1]/td[2]")
            cert_details['org'] = self._get_text(cert_link + "/div/table/tbody/tr[2]/td[2]")
            cert_details['org_unit'] = self._get_text(cert_link + "/div/table/tbody/tr[3]/td[2]")
            cert_details['country'] = self._get_text(cert_link + "/div/table/tbody/tr[4]/td[2]")
            cert_details['basic_constrain'] = self._get_text(cert_link + "/div/table/tbody/tr[5]/td[2]")
            cert_details['expiry_date'] = self._get_text(expiry_link)
            cert_details['basic_constrain'] = self._get_text(on_cisco_list)
            self._info('Cert Details %s' % cert_details)

            return cert_details
        else:
            raise ValueError('`%s` Certificate is not present on the page' % (cert_name,))

    def get_certificate_authority_status(self, cert_type='custom'):
        """Delete a certificate with given name

                *Parameters*
                    - `cert_type`: Certificate Type choose from 'custom' or 'system'. String.
                    Default value is 'custom'.
        """
        self._open_page()
        if cert_type.lower() == 'custom':
            return self._get_text(CERTIFICATE_AUTHORITIES_CUSTOM_LIST_STATUS)
        elif cert_type.lower() == 'system':
            return self._get_text(CERTIFICATE_AUTHORITIES_SYSTEM_LIST_STATUS)
        else:
            raise ValueError('`%s` Wrong certificate type' % (cert_type,))

    def override_trusted_root_certificate(self,certificate_position,enable=True):
        """Use the checkboxes to override entries

                *Examples*
                Override Trusted Root Certificate  1  ${True}
        """

        self.click_manage_trusted_root_cert()
        if enable:
            self._select_checkbox(CISCO_TRUSTED_ROOT_CERTIFICATE_OVERRIDE_TRUST.format(certificate_position))
        else:
            self._unselect_checkbox(CISCO_TRUSTED_ROOT_CERTIFICATE_OVERRIDE_TRUST.format(certificate_position))
        self._click_submit_button()
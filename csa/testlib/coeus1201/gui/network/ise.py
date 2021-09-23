#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/ise.py#2 $
# $DateTime: 2019/11/10 06:06:44 $
# $Author: biaramba $

import common.gui.guiexceptions as guiexceptions
from constants import https_cert_info
from common.gui.guicommon import GuiCommon
import time


RESULT_CONTAINER = 'id=ISE_container'
ISE_TEST_TIMEOUT = '5m'


class IdentityServiceEngine(GuiCommon):

    """
    Identity Service Engine (ISE) settings page interaction class.
    'Network -> Identity Services Engine' section.
    """
    ui_elements_ise = {
        "MENU_NETWORK": "Network",
        "SUBMENU_NETWORK_ISE": "Identity Services Engine",
        "BUTTON_ENABLE_AND_EDIT_SETTINGS": "xpath=//input[@value='Enable and Edit Settings...']",
        "BUTTON_EDIT_SETTINGS": "xpath=//input[@value='Edit Settings...']",
        "BUTTON_ENABLE": "//input[@id='enabled']",
        "ISE_SERVER_PRIMARY": "xpath=//input[@id='ise_server']",
        "ISE_SERVER_SECONDARY": "xpath=//input[@id='ise_server_secondary']",
        "BROWSE_PXGRID_CERT_PRIMARY": "xpath=//input[@id='uploadPxGridCertificate']",
        "UPLOAD_PXGRID_CERT_PRIMARY": "xpath=//input[@id='uploadFilesPxGrid']",
        "BROWSE_PXGRID_CERT_SECONDARY": "xpath=//input[@id='uploadSecondaryPxGridCertificate']",
        "UPLOAD_PXGRID_CERT_SECONDARY": "xpath=//input[@id='uploadFilesSecondaryPxGrid']",
        "BROWSE_PORTAL_CERT_PRIMARY": "xpath=//input[@id='uploadPortalCertificate']",
        "UPLOAD_PORTAL_CERT_PRIMARY": "xpath=//input[@id='uploadFilesPortal']",
        "BROWSE_PORTAL_CERT_SECONDARY": "xpath=//input[@id='uploadSecondaryPortalCertificate']",
        "UPLOAD_PORTAL_CERT_SECONDARY": "xpath=//input[@id='uploadFilesSecondaryPortal']",
        "RADIO_UPLOAD_WSA_CERT": "xpath=//input[@id='uploadedCertRadio']",
        "BROWSE_WSA_CERT": "xpath=//input[@id='uploadCertificate']",
        "BROWSE_WSA_KEY": "xpath=//input[@id='uploadKey']",
        "CHECK_WSA_KEY_ENCRYPTED": "xpath=//input[@id='encrypted_key']",
        "UPLOAD_WSA_CERT": "xpath=//input[@id='uploadFiles']",
        "TABLE_CELL_ISE_SERVERS_HEADER": "xpath=//th[contains(text(), 'Primary ISE pxGrid Node')]",
        "TABLE_CELL_ISE_SERVERS_VALUE": "xpath=//th[contains(text(), 'Primary ISE pxGrid Node')]/../td",
        "BUTTON_EDIT_CHECKBOX_SETTINGS": "//*[@id='enabled']",
        "BUTTON_ENABLE_ERS_CHECKBOX_SETTINGS": "//*[@id='ERSenabled']",
        "ERS_ADMIN_USERNAME": "//*[@id='ERSUsername']",
        "ERS_ADMIN_PASSWORD": "//*[@name='encrypted_ERSPassword']",
        "ERS_SERVER_CHECKBOX": "//*[@id='ISEServer']",
        "ERS_SERVER_PRIMARY": "//*[@id='ERSPrimary']",
        "ERS_SERVER_SECONDARY": "//*[@id='ERSSecondary']",
        "ERS_PORT": "//*[@id='ERSPort']",
    }

    cert_keys = [
        'name',
        'org',
        'org_unit',
        'country',
        'duration',
        'constraints'
    ]

    upload_cert_keys = [
        'cert',
        'key',
        'key_is_encrypted',
        'key_password',
    ]

    def get_keyword_names(self):
        return [
            'identity_service_engine_enable',
            'identity_service_engine_disable',
            'identity_service_engine_edit_settings',
            'identity_service_engine_ers_enable',
            'ise_start_test',
            'ers_enable',
            'ers_disable',
            'ers_edit_settings',
        ]

    def _ui_get(self, element):
        return self.ui_elements_ise.get(element)

    def _open_identity_service_engine_page(self):
        """Go to Identity Service Engine configuration page."""
        self._navigate_to(self._ui_get("MENU_NETWORK"), self._ui_get("SUBMENU_NETWORK_ISE"))

    def identity_service_engine_enable(
        self,
        ise_server=None,
        ise_server_backup=None,
        cert_name=None,
        cert_org=None,
        cert_org_unit=None,
        cert_country=None,
        cert_duration=None,
        cert_constraints=None,
        cert_location=None,
        cert_key=None,
        key_is_encrypted=None,
        key_password=None,
        portal_cert=None,
        pxgrid_cert=None,
        use_primary_certs=None,
        portal_cert2=None,
        pxgrid_cert2=None
    ):
        """Enables Identity Service Engine

        Parameters:
        - `ise_server`: primary ise server
        - `ise_server_backup`: backup ise server
        --- Root Certificate for Signing ---
        If none of the following 5 parameters is set then default values are
        set from variables/constants.py. Current values are:
        {
            'name': "ironport.com",
            'org': "QA Automation",
            'org_unit': "QA",
            'country': "US",
            'duration': 12,
            'constraints': False
        }

        - `cert_name`: certificate common name, in a string format. Leave empty
         if you are going to upload a new certificate.
        - `cert_org`: certificate organization.
        - `cert_org_unit`: certificate organizational unit.
        - `cert_country`: certificate country.
        - `cert_duration`: duration before certificate expiration in months.
        - `cert_constraints`: set X509v3 basic constraints extension
                           to critical. Either 'True' or 'False'.
        - `cert_location`: location of a certificate file to upload. Leave empty
                        if you are generating new certificate.
        - `cert_key`: location of key file to upload.
        - `key_is_encrypted`: Either 'True' or 'False'
        - `key_password`: password for encrypted key
        - `portal_cert`: location of ISE Portal Certificate to upload
        - `pxgrid_cert`: location of ISE PxGrid Certificate to upload
        - `use_primary_certs`: use primary certificates for secondary server
        - `portal_cert2`: location of admin certificate 2 to upload
        - `pxgrid_cert2`: location of pxgrid certificate 2 to upload

        Example:
        | Identity Service Engine Enable |

        | Identity Service Engine Enable |
        | ... | ise_server=1.2.3.4 |
        | ... | ise_server_backup=4.3.2.1 |
        | ... | cert_name=cert_name |
        | ... | cert_org=Cisco |
        | ... | cert_org_unit=QA Automation |
        | ... | cert_country=US |
        | ... | cert_duration=1 |
        | ... | portal_cert=%{SARF_HOME}/tests/testdata/admin1.crt |
        | ... | pxgrid_cert=%{SARF_HOME}/tests/testdata/pxgrid1.cert |
        | ... | use_primary_certs=Y |
        | ... | portal_cert2=%{SARF_HOME}/tests/testdata/admin2.crt |
        | ... | pxgrid_cert2=%{SARF_HOME}/tests/testdata/pxgrid2.cert |
        """
        cert_values = [
            cert_name,
            cert_org,
            cert_org_unit,
            cert_country,
            cert_duration
        ]

        upload_cert_values = [
            cert_location,
            cert_key,
            key_is_encrypted,
            key_password,
        ]

        if cert_location is not None:
            cert_info = dict(zip(self.upload_cert_keys, upload_cert_values))
        else:
            if all(cert_values):
                cert_values.append(cert_constraints)
                cert_info = dict(zip(self.cert_keys, cert_values))
            else:
                cert_info = https_cert_info.DEFAULT

        self._open_identity_service_engine_page()
        self._click_enable_and_edit_settings_button()
        self._set_ise_servers(ise_server, ise_server_backup)
        self._select_root_cert_for_signing(cert_info)
        self._upload_portal_cert(portal_cert)
        self._upload_pxgrid_cert(pxgrid_cert)
        # self._select_use_primary_certs(use_primary_certs)
        self._upload_portal_cert_secondary(portal_cert2)
        self._upload_pxgrid_cert_secondary(pxgrid_cert2)
        self._click_submit_button(wait=False)
        time.sleep(10)

    def _click_enable_and_edit_settings_button(self):
        edit_button = self._ui_get("BUTTON_ENABLE_AND_EDIT_SETTINGS")
        self.click_button(edit_button)

    def _click_edit_settings_button(self):
        edit_button = self._ui_get("BUTTON_EDIT_SETTINGS")
        self.click_button(edit_button)

    def _click_ers_enable_settings_button(self):
        edit_button = self._ui_get("BUTTON_ENABLE_ERS_CHECKBOX_SETTINGS")
        self.click_button(edit_button)

    def _click_ers_server_button(self):
        edit_button = self._ui_get("ERS_SERVER_CHECKBOX")
        self.click_button(edit_button)

    def _set_ise_ers_admin_credentials(
        self,
        ers_admin_username=None,
        ers_admin_password=None
    ):

        ers_admin_username_field = self._ui_get("ERS_ADMIN_USERNAME")
        ers_admin_password_field = self._ui_get("ERS_ADMIN_PASSWORD")
        self._input_text_if_not_none(ers_admin_username_field, ers_admin_username)
        self._input_text_if_not_none(ers_admin_password_field, ers_admin_password)

    def _set_ers_servers(
        self,
        ers_server_primary=None,
        ers_server_secondary=None,
        ers_port=None,
        use_same_ise_server=None,
    ):

        print('ers_server_primary', ers_server_primary)
        print('ers_server_secondary', ers_server_secondary)
        print('ers_port', ers_port)
        print('use_same_ise_server', use_same_ise_server)

        if use_same_ise_server == 'Yes':
            time.sleep(2)
            self._click_ers_server_button()
        else:
            ersserver_checkbox = self._ui_get("ERS_SERVER_CHECKBOX")
            self.unselect_checkbox(ersserver_checkbox)
            ers_server_primary_field = self._ui_get("ERS_SERVER_PRIMARY")
            self._input_text_if_not_none(ers_server_primary_field, ers_server_primary)
            ers_server_secondary_field = self._ui_get("ERS_SERVER_SECONDARY")
            self._input_text_if_not_none(ers_server_secondary_field, ers_server_secondary)
            print("check for thr port")
            ers_server_port_field = self._ui_get("ERS_PORT")
            self._input_text_if_not_none(ers_server_port_field, ers_port)

    def _set_ise_servers(self, ise_server=None, ise_server_backup=None):
        ise_server_field = self._ui_get("ISE_SERVER_PRIMARY")
        ise_server_backup_field = self._ui_get("ISE_SERVER_SECONDARY")
        self._input_text_if_not_none(ise_server_field, ise_server)
        self._input_text_if_not_none(ise_server_backup_field, ise_server_backup)

    def _select_root_cert_for_signing(self, cert_info=None):

        if cert_info:
            if 'name' in cert_info.keys():
                self._generate_certificate(generate_cert=cert_info)
            elif 'cert' in cert_info.keys():
                self._upload_certificate(upload_cert=cert_info)
            else:
                raise guiexceptions.ConfigError('Invalid Keys for \'Root Certificate for Signing\'')

    def _generate_certificate(self, generate_cert=None):

        cert_keys = {
            'name': 'dialogCertCommonName',
            'org': 'dialogCertOrganization',
            'org_unit': 'dialogCertOrganizationUnit',
            'country': 'dialogCertCountry',
            'duration': 'dialogCertExpiration',
            'constraints': 'dialogCertIsCritical'
        }

        generate_cert_radio_button = "id=generatedCertRadio"
        generate_new_cert_button = "generate_cert"

        self._click_radio_button(generate_cert_radio_button)
        self.click_button(generate_new_cert_button, "don't wait")

        if len(generate_cert) is not 6:
            raise ValueError('\'generate_cert\' should be of length 6')
        for cert_field, value in generate_cert.iteritems():
            if cert_field not in cert_keys.keys():
                raise ValueError(
                    'Invalid Key \'%s\' to Generate a new certificate. Here are the valid certificate fields %s' % (
                        cert_field,
                        cert_keys.keys()
                    )
                )
            if cert_field == 'constraints':
                if generate_cert['constraints']:
                    self.select_checkbox(cert_keys[cert_field])
            else:
                self._input_text_if_not_none(cert_keys[cert_field], generate_cert[cert_field])

        self._click_continue_button('Generate')
        self._wait_until_text_is_present('successfully generated')

    def _upload_portal_cert(self, cert):
        BROWSE = self._ui_get("BROWSE_PORTAL_CERT_PRIMARY")
        UPLOAD = self._ui_get("UPLOAD_PORTAL_CERT_PRIMARY")

        if cert:
            self.choose_file(BROWSE, cert)
            self.click_button(UPLOAD)
            self.check_for_warning()

    def _upload_portal_cert_secondary(self, cert):
        BROWSE = self._ui_get("BROWSE_PORTAL_CERT_SECONDARY")
        UPLOAD = self._ui_get("UPLOAD_PORTAL_CERT_SECONDARY")

        if cert:
            self.choose_file(BROWSE, cert)
            self.click_button(UPLOAD)
            self.check_for_warning()

    def _upload_pxgrid_cert(self, cert):
        BROWSE = self._ui_get("BROWSE_PXGRID_CERT_PRIMARY")
        UPLOAD = self._ui_get("UPLOAD_PXGRID_CERT_PRIMARY")

        if cert:
            self.choose_file(BROWSE, cert)
            self.click_button(UPLOAD)
            self.check_for_warning()

    def _upload_pxgrid_cert_secondary(self, cert):
        BROWSE = self._ui_get("BROWSE_PXGRID_CERT_SECONDARY")
        UPLOAD = self._ui_get("UPLOAD_PXGRID_CERT_SECONDARY")

        if cert:
            self.choose_file(BROWSE, cert)
            self.click_button(UPLOAD)
            self.check_for_warning()

    def choose_file_from_client(self, locator, file_path):
        """Inputs the `file_path` into file input field found by `locator`.

        This keyword is most often used to input files into upload forms.
        The file specified with `file_path` must be available on the same host
        where the Selenium Server is running.

        Example:
        | Choose File | my_upload_field | /home/user/files/trades.csv |
        """
        #if not os.path.isfile(file_path):
        #    raise AssertionError("File '%s' does not exist on the local file system"
        #                % file_path)
        self._element_find(locator, True, True).send_keys(file_path)


    def _upload_certificate(self, upload_cert=None):

        upload_fields = {
            'cert': "//input [@id='uploadCertificate']",
            'key': 'uploadKey',
            'key_is_encrypted': None,
            'key_password': None,
        }

        upload_cert_radio_button = self._ui_get("RADIO_UPLOAD_WSA_CERT")
        upload_files_button = self._ui_get("UPLOAD_WSA_CERT")

        if upload_cert:
            if len(upload_cert) is not 4:
                raise ValueError('\'upload_cert\' should be of length 4')

            for cert_key, value in upload_cert.iteritems():
                if cert_key not in upload_fields.keys():
                    raise guiexceptions.ConfigError(
                        'Invalid Key \'%s\' to upload a certificate. Here are the valid upload fields %s' % (
                            cert_key,
                            upload_fields.keys()
                        )
                    )

            self._click_radio_button(upload_cert_radio_button)
            self.choose_file(upload_fields['cert'], upload_cert['cert'])
            self.choose_file(upload_fields['key'], upload_cert['key'])
            self._set_key_is_encrypted(upload_cert['key_is_encrypted'])
            self._set_key_password(upload_cert['key_password'])
            self.click_button(upload_files_button)
            self.check_for_warning()

    def identity_service_engine_disable(self):
        """Disables Identity Service Engine

        Example:
        | Identity Service Engine Disable |
        """
        identity_service_checkbox = self._ui_get("BUTTON_EDIT_CHECKBOX_SETTINGS")
        self._open_identity_service_engine_page()

        if not self._check_feature_status(feature='ise'):
            return

        self._click_edit_settings_button()
        self.unselect_checkbox(identity_service_checkbox)
        self._click_submit_button(wait=False)

    def ers_disable(self):
        """Disables ERS """
        ers_checkbox = self._ui_get("BUTTON_ENABLE_ERS_CHECKBOX_SETTINGS")
        self._open_identity_service_engine_page()
        time.sleep(5)
        self._click_edit_settings_button()
        time.sleep(5)

        if self._check_feature_status(feature='ers'):
            self.unselect_checkbox(ers_checkbox)
            self._click_submit_button(wait=False)
        else:
            raise guiexceptions.GuiFeatureDisabledError('Cannot edit ERS is disabled')

    def identity_service_engine_edit_settings(
        self,
        ise_server=None,
        ise_server_backup=None,
        cert_name=None,
        cert_org=None,
        cert_org_unit=None,
        cert_country=None,
        cert_duration=None,
        cert_constraints=None,
        cert_location=None,
        cert_key=None,
        key_is_encrypted=None,
        key_password=None,
        portal_cert=None,
        pxgrid_cert=None,
        use_primary_certs=None,
        portal_cert2=None,
        pxgrid_cert2=None
    ):
        """Sets Identity Service settings.

        Parameters:
        - `ise_server`: primary ise server
        - `ise_server_backup`: backup ise server

        If none of the following 5 parameters is set then default values are
        set from variables/constants.py. Current values are:
        {'name': "ironport.com",
               'org': "QA Automation",
               'org_unit': "QA",
               'country': "US",
               'duration': 12,
               'constraints': False}

        - `cert_name`: certificate common name, in a string format.
              Leave empty if you are
                    going to upload a new certificate.

        - `cert_org`: certificate organization.

        - `cert_org_unit`: certificate organizational unit.

        - `cert_country`: certificate country.

        - `cert_duration`: duration before certificate expiration in months.

        - `cert_constraints`: set X509v3 basic constraints extension
                           to critical. Either 'True' or 'False'.

        - `cert_location`: location of a certificate file to upload.Leave empty
                        if you are generating new certificate.

        - `cert_key`: location of key file to upload.
        - `key_is_encrypted`: Either 'True' or 'False'
        - `key_password`: password for encrypted key
        - `portal_cert`: location of ISE Portal Certificate to upload
        - `pxgrid_cert`: location of ISE PxGrid Certificate to upload
        - `use_primary_certs`: use primary certificates for secondary server
        - `portal_cert2`: location of admin certificate 2 to upload
        - `pxgrid_cert2`: location of pxgrid certificate 2 to upload

        Example:

        | Identity Service Engine Edit Settings |
        | ... | ise_server=1.2.3.4 |
        | ... | ise_server_backup=4.3.2.1 |
        | ... | portal_cert=%{SARF_HOME}/tests/testdata/auth.cert |
        | ... | pxgrid_cert=%{SARF_HOME}/tests/testdata/ca.crt |
        | ... | use_primary_certs=Y |
        | ... | portal_cert2=%{SARF_HOME}/tests/testdata/admin2.crt |
        | ... | pxgrid_cert2=%{SARF_HOME}/tests/testdata/pxgrid2.cert |

        """
        cert_values = [
            cert_name,
            cert_org,
            cert_org_unit,
            cert_country,
            cert_duration
        ]

        upload_cert_values = [
            cert_location,
            cert_key,
            key_is_encrypted,
            key_password,
        ]

        if cert_location:
            cert_info = dict(zip(self.upload_cert_keys, upload_cert_values))
        else:
            if all(cert_values):
                cert_values.append(cert_constraints)
                cert_info = dict(zip(self.cert_keys, cert_values))
            else:
                cert_info = https_cert_info.DEFAULT

        self._open_identity_service_engine_page()
        if not self._check_feature_status(feature='ise'):
            raise guiexceptions.GuiFeatureDisabledError('Cannot edit Identity Service Engine as disabled')

        self._click_edit_settings_button()
        self._set_ise_servers(ise_server, ise_server_backup)
        self._select_root_cert_for_signing(cert_info)
        self._upload_portal_cert(portal_cert)
        self._upload_pxgrid_cert(pxgrid_cert)
        # self._select_use_primary_certs(use_primary_certs)
        self._upload_portal_cert_secondary(portal_cert2)
        self._upload_pxgrid_cert_secondary(pxgrid_cert2)
        self._click_submit_button(wait=False)
        time.sleep(10)

    def ers_edit_settings(
        self,
        ers_admin_username=None,
        ers_admin_password=None,
        ers_server_primary=None,
        ers_server_secondary=None,
        ers_port=None,
        use_same_ise_server=None
    ):

        print('use_same_ise_server', use_same_ise_server)
        self._open_identity_service_engine_page()
        time.sleep(5)
        self._click_edit_settings_button()
        if not self._check_feature_status(feature='ers'):
            raise guiexceptions.GuiFeatureDisabledError('Cannot edit ERS as disabled')

        else:
            self._set_ise_ers_admin_credentials(ers_admin_username, ers_admin_password)
            self._set_ers_servers(ers_server_primary, ers_server_secondary, ers_port, use_same_ise_server="No")
            self._click_submit_button(wait=False)
            time.sleep(10)

    def ers_enable(
        self,
        ise_server=None,
        ers_admin_username=None,
        ers_admin_password=None,
        ers_server_primary=None,
        ers_server_secondary=None,
        ers_port=None,
        use_same_ise_server=None
    ):

        print('ers_admin_username', ers_admin_username)
        print('ers_admin_password', ers_admin_password)
        print('ise_server', ise_server)
        print('ers_server_primary', ers_server_primary)
        print('ers_server_secondary', ers_server_secondary)
        print('ers_port', ers_port)
        print('use_same_ise_server', use_same_ise_server)

        """
        Enable ISE External Restful Service

        Parameters:
        - 'ers_admin_username' : Specific ERS User added present in ISE Server
        - 'ers_admin_password' : password for the ERS User
        If ERS server is same as the ISE Server then ERS SERVER PRIMARY 
        will be same as the ISE Server pxgrid node Ip address
        - 'ers_server_primary' : ISE Server ip where ERS user is present
        - 'ers_server_secondary' : doubt
        - 'ers_port' : default port for ers
        """
        self._open_identity_service_engine_page()
        time.sleep(5)
        self._click_edit_settings_button()
        self._click_ers_enable_settings_button()
        self._set_ise_ers_admin_credentials(ers_admin_username, ers_admin_password)
        self._set_ers_servers(ers_server_primary, ers_server_secondary, ers_port, use_same_ise_server)
        self._click_submit_button(wait=False)
        time.sleep(10)

    def identity_service_engine_ers_enable(self, name, password,):
        ersenabled = '//input [@id="ERSenabled"]'
        iseserver = '//input [@id="ISEServer"]'

        self._click_edit_settings_button()

        if not self._is_checked(ersenabled):
            self.select_checkbox(ersenabled)

        if name is not None:
            self._fill_ers_name(name)

        if password is not None:
            self._fill_ers_password(password)

        if not self._is_checked(iseserver):
            self.select_checkbox(iseserver)

        self._click_submit_button()

    def _fill_ers_name(self, name):
        name_id = 'id=ERSUsername'
        self.input_text(name_id, text=name)

    def _fill_ers_password(self, password):
        password_id = 'name=encrypted_ERSPassword'
        self.input_password(password_id, password)

    def _get_test_results(self):

        # self.wait_until_page_contains(text='Test completed',timeout=ISE_TEST_TIMEOUT)
        time.sleep(60)
        test_results = self.get_text(RESULT_CONTAINER)

        return test_results

    def ise_start_test(self):
        """Run test for the specified ASA host. Keyword returns
        test result as string in debug file.

        Example:
        | Acsm Start Test |
        """
        start_test_button = 'xpath=//*[@id="ISE_start_test"]'
        self._open_identity_service_engine_page()

        if not self._check_feature_status(feature='ise'):
            raise guiexceptions.GuiFeatureDisabledError('Cannot click start test button as ise is disabled')

        self._click_edit_settings_button()
        self.click_button(start_test_button)
        result = self._get_test_results()
        self._info(result)

        if result.find('Test completed success') != -1:
            pass

        else:
            self.click_button(start_test_button)
            result = self._get_test_results()

            if result.find('Test completed success') != -1:
                pass
            else:
                raise guiexceptions.IseTestError('Errors occurred. See debug file for more info.')

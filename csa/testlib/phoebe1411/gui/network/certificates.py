import time

from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
from common.gui.guiexceptions import GuiValueError

from certificates_def.import_settings import ImportSettings

ADD_CERTIFICATE_BUTTON = "//input[@value='Add Certificate...']"
IMPORT_TYPE_COMBO = "//select[@id='add_import_option']"
CERT_NAME = "//input[@id='cert_name']"
FIELD_COMMONNAME = "//input[@id='common_name']"
FIELD_ORGANIZATION = "//input[@id='organization']"
FIELD_ORGUNIT = "//input[@id='org_unit']"
FIELD_CITY = "//input[@id='city']"
FIELD_STATE = "//input[@id='state']"
FIELD_COUNTRY = "//input[@id='country']"
FIELD_DOMAINS = "xpath=(//input[@value=''])[11]"
FIELD_EMAIL = "xpath=(//input[@value=''])[12]"
FIELD_DURATION = "//input[@id='expiration']"
RADIO_2048 = "//input[@id='priv_key_size_2048']"
RADIO_1024 = "//input[@id='priv_key_size_1024']"
NEXT_BUTTON = "//form[@id='form']/input[3]"
FQDN_VALIDATION = "//input[@id='fqdn_validation']"                             
UPLOAD_SIGNED_CERT = "//input[@name='signed_cert']"
DOWNLOAD_CSR = "//a[contains(text(), 'Download Certificate Signing Request')]"
INTERMEDIATE_CERT_OPEN_ARROW = "//img[@id='interm_certs_arrow']"
UPLOAD_INTERMEDIATE_CERT = "//input[@name='interm_cert']"
SUBMIT_BUTTON = "//input[@value='Submit']"
CANCEL_BUTTON = "//input[@value='Cancel']"

CERTS_TABLE = "//table[@class='cols']"
CERT_EDIT_LINK = lambda name: "%s//a[contains(text(), '%s')]" % (CERTS_TABLE, name)
CERT_DELETE_LINK = lambda name: "%s//td[normalize-space()='%s']"\
                        "/following-sibling::td[8]/img" % \
                        (CERTS_TABLE, name)

CERT_TIME_REMAINING = lambda name: "%s//td[normalize-space()='%s']"\
                        "/following-sibling::td[5]/span" % \
                        (CERTS_TABLE, name)

CA_EDIT_SETTINGS_BUTTON = "//input[@value='Edit Settings...']"
CA_CUSTOM_LIST_ENABLE_BUTTON = "//input[@id='custom_ca_enable']"
CA_CUSTOM_LIST_DISABLE_BUTTON = "//input[@id='custom_ca_disable']"
CA_CUSTOM_LIST_UPLOAD_FILE_BUTTON = "//input[@id='custom_ca_file_upload']"
CA_CUSTOM_LIST_ENABLE_FQDN_CHECKBOX = "//input[@id='fqdn_validation']"
CA_VIEW_CUSTOM_CA_LINK = "//a[@id='preview_custom_ca']"
CA_SYSTEM_LIST_ENABLE_BUTTON = "//input[@id='system_ca_enable']"
CA_SYSTEM_LIST_DISABLE_BUTTON = "//input[@id='system_ca_disable']"
CA_EXPORT_LIST_BUTTON = "//input[@value='Export List...']"
CA_VIEW_SYSTEM_CA_LINK = "//a[@id='preview_system_ca']"
CA_EXPORT_LIST_SELECT_OPTION = "//select[@id='ca_list_option']"
CA_EXPORT_LIST_FILE_NAME = "//input[@id='file_name']"
CA_EXPORT_LIST_EXPORT_BUTTON = "//input[@value='Export']"
CA_EXPORT_LIST_CANCEL_BUTTON = "//input[@value='Cancel']"

MANAGE_TRUSTED_ROOT_CERT_BUTTON = "//input[@value='Manage Trusted Root " \
                                  "Certificates...']"
CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE = "//dt[contains(text(), 'Custom Trusted')]/following-sibling::dd//table[@class='cols']"
CISCO_TRUSTED_ROOT_CERTIFICATE_TABLE = "//dt[contains(text(), 'Cisco Trusted')]/following-sibling::dd//table[@class='cols']"
CUSTOM_TRUSTED_ROOT_CERTIFICATE_DELETE_BUTTON = lambda certificate: "%s/tbody/tr[%s]/td[4]/img" % \
                                        (CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE, certificate)
CUSTOM_TRUSTED_ROOT_CERTIFICATE_CONFIRM_DELETE_BUTTON = "//button[contains(text(), 'Delete')]"

EXPAND_CERTIFICATE = lambda certificate_table, certificate: "%s/tbody/tr[%s]/td//div[contains(@id, 'arrow_closed')]" % \
                                        (certificate_table, certificate)
COLLAPSE_CERTIFICATE = lambda certificate_table, certificate: "%s/tbody/tr[%s]/td//div[contains(@id, 'arrow_open')]" % \
                                        (certificate_table, certificate)
DOWNLOAD_CERTIFICATE = lambda certificate_table, certificate: "%s/tbody/tr[%s]/td/div[contains(@id, 'cert_section')]//a" % \
                                        (certificate_table, certificate)

CUSTOM_CERTIFICATE_LINK = CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE + "/tbody/tr[%s]/td[1]" 
CUSTOM_CERTIFICATE_EXPIRY_LINK = CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE + "/tbody/tr[%s]/td[2]"
CUSTOM_CERTIFICATE_ON_CISCO_LIST = CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE + "/tbody/tr[%s]/td[3]"

CUSTOM_CERTIFICATE_CUSTOM_NAME = "/div[contains(@id, 'cert_section')]//tr[1]//td[2]"
CUSTOM_CERTIFICATE_ORGANIZATION = "/div[contains(@id, 'cert_section')]//tr[2]//td[2]"
CUSTOM_CERTIFICATE_ORGANIZATION_UNIT = "/div[contains(@id, 'cert_section')]//tr[3]//td[2]"
CUSTOM_CERTIFICATE_COUNTRY = "/div[contains(@id, 'cert_section')]//tr[4]//td[2]"
CUSTOM_CERTIFICATE_BASIC_CONSTRAIN = "/div[contains(@id, 'cert_section')]//tr[5]//td[2]"

PAGE_PATH = ('Network', 'Certificates')


class Certificates(GuiCommon):
    """Keywords for GUI interaction with Network -> Certificates
    page"""

    def get_keyword_names(self):
        return ['certificates_create',
                'certificates_edit',
                'certificates_import',
                'certificates_delete',
                'certificates_get_certificates_info',
                'certificates_get_ca_info',
                'certificates_ca_edit_settings',
                'certificates_ca_export_list',
                'certificates_ca_view_custom_certificate_authorities',
                'certificates_ca_view_system_certificate_authorities',
                'certificates_get_remaining_days_for_expiry',
                'certificates_custom_trusted_root_certificates_get_names',
                'certificates_custom_trusted_root_certificates_download',
                'certificates_custom_trusted_root_certificates_delete',
                'certificates_custom_trusted_root_certificates_get_details',
                'certificates_cisco_trusted_root_certificates_get_names',
                'certificates_cisco_trusted_root_certificates_download']

    def _get_import_settings_controller(self):
        if not hasattr(self, '_import_settings_controller'):
            self._import_settings_controller = ImportSettings(self)
        return self._import_settings_controller

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_create(self,
                               certificate_type=None,
                               common_name=None,
                               organization=None,
                               organizational_unit=None,
                               city=None,
                               state=None,
                               country=None,
                               domains=None,
                               email=None,
                               duration=None,
                               size=None,
                               fqdn_validation=None,
                               signed_certificate=None,
                               intermediate_certificate=None,
                               download_csr=None):
        """Creates Certificate of either self signed or SMIME type

        *Parameters:*
        - `certificate_type`: Either self_signed or smime type
        - `common_name`: Common Name
        - `organization`: Organization
        - `organizational_unit`: Organizational Unit
        - `city`: City (Locality)
        - `state`: State (Province)
        - `country`: Country (2 letters only)
        - `domains`: Subject Alternative Name(Domains)
        - `email`: Subject Alternative Name(Email)
        - `duration`: Duration before expiration
        - `size`: Private Key Size
        - `fqdn_validation`: Pass Yes to enable FQDN validation
                             Pass No to disable FQDN validation
        - `signed_certificate`: Pass the signed certificate path to upload
        - `intermediate_certificate`: Pass the intermediate certificate path to upload
        - `download_csr`: Pass Yes to download the Certificate Signing Request

        *Examples:*
        | Certificates Create  |
        | ... | self_signed |
        | ... | cisco |
        | ... | cisco |
        | ... | sbg |
        | ... | bangalore |
        | ... | karnataka |
        | ... | IN |
        | ... | 3650 |
        | ... | 2048 |
        """
        self.click_button(ADD_CERTIFICATE_BUTTON)
        if certificate_type=="self_signed":
            self.select_from_list(IMPORT_TYPE_COMBO, 'Create Self-Signed Certificate')
        elif certificate_type=="smime":
            self.select_from_list(IMPORT_TYPE_COMBO, 'Create Self-Signed S/MIME Certificate')
        if common_name is not None:
            self.input_text(FIELD_COMMONNAME, common_name)
        if organization is not None:
            self.input_text(FIELD_ORGANIZATION, organization)
        if organizational_unit is not None:
            self.input_text(FIELD_ORGUNIT, organizational_unit)
        if city is not None:
            self.input_text(FIELD_CITY, city)
        if state is not None:
            self.input_text(FIELD_STATE, state)
        if country is not None:
            self.input_text(FIELD_COUNTRY, country)
        if certificate_type=="smime":
            if domains is not None:
                self.input_text(FIELD_DOMAINS, domains)
                self.press_key(FIELD_DOMAINS, "\\13")
            if email is not None:
                self.input_text(FIELD_EMAIL, email)
        if duration is not None:
            self.input_text(FIELD_DURATION, duration)
        if size == '2048':
            self._click_radio_button(RADIO_2048)
        elif size == '1024':
            self._click_radio_button(RADIO_1024)
        self.click_button(NEXT_BUTTON)
        self._wait_until_element_is_present(FQDN_VALIDATION)
        if fqdn_validation and fqdn_validation.lower() == 'yes':
            self._select_checkbox(FQDN_VALIDATION)
        if signed_certificate:
            self.input_text(UPLOAD_SIGNED_CERT, signed_certificate)
        if intermediate_certificate:
            self.click_element(INTERMEDIATE_CERT_OPEN_ARROW)
            self.input_text(UPLOAD_INTERMEDIATE_CERT, intermediate_certificate)
        if download_csr and download_csr.lower() == 'yes':
            self.click_element(DOWNLOAD_CSR)
        self._click_submit_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_edit(self,
                               cert_name=None,
                               cert_new_name=None,
                               fqdn_validation=None,
                               signed_certificate=None,
                               intermediate_certificate=None,
                               download_csr=None):
        """Edits Certificate settings. Following parameters can be modified.

        *Parameters:*
        - `cert_name`: Certificate's name which settings need to be modified.
        - `cert_new_name`: Certificate's new name.
        - `fqdn_validation`: Enable or disable FQDN validation. Yes or No
        - `signed_certificate`: Pass the singed certificate's path to upload.
        - `intermediate_certificate`: Pass the intermediate certificate's path to upload.
        - `download_csr`: Pass Yes to download the Certificate Signing Request (.csr file)

        *Examples:*
        | Certificates Edit                                                     |
        | ... | cert_name=my cert                                               |
        | ... | cert_new_name=New Cert                                          |    
        | ... | fqdn_validation=No                                              |
        | ... | signed_certificate=/home/aminath/work/csa/tests/testdata/ca.crt |
        | ... | download_csr=No                                                 |
        """
        self.click_element(CERT_EDIT_LINK(cert_name))
        if fqdn_validation and fqdn_validation.lower() == 'yes':
            self._select_checkbox(FQDN_VALIDATION)
        if cert_new_name:
            self.input_text(CERT_NAME, cert_new_name)
        if signed_certificate:
            self.input_text(UPLOAD_SIGNED_CERT, signed_certificate)
        if intermediate_certificate:
            self.click_element(INTERMEDIATE_CERT_OPEN_ARROW)
            self.input_text(UPLOAD_INTERMEDIATE_CERT, intermediate_certificate)
        if download_csr and download_csr.lower() == 'yes':
            self.click_element(DOWNLOAD_CSR)
        self._click_submit_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_import(self, settings):
        """Import certificate from PKCS#12 file

        *Parameters:*
        - `settings`: dictionary whose items are:
        | Name | name of the certificate profile, will be equal
        to CN property if omitted |
        | Path | path to a certificate in PKCS#12 format on
        the client machine, mandatory |
        | Password | password to the file, ironport by default |
        | FQDN Validation | Pass Yes to enable FQDN validation |
        | Signed Certificate | Pass the singed certificate's path to upload |
        | Intermediate Certificate | Pass the intermediate certificate's path to upload |
        | Download CSR | Pass Yes to download the Certificate Signing Request (.csr file) |

        *Examples:*
        Do not forget to include the
        generate_sign_server_certificate.txt resource into your suite
        | ${key_path} | ${cert_path}= | Generate Sign Server Certificate |
        | ${pk12_path}= | Generate PKCS12 File | ${key_path} | ${cert_path} |
        | ${import_settings}= | Create Dictionary |
        | ... | Name | new_my_cert |
        | ... | Path | ${pk12_path} |
        | ... | Password | ironport |
        | ... | FQDN Validation | Yes |
        | ... | Signed Certificate | %{SARF_HOME}/tests/testdata/esa/FQDN/p12 |
        | ... | Download CSR | Yes |
        | Certificates Import | ${import_settings} |
        """
        self.click_button(ADD_CERTIFICATE_BUTTON)
        self.select_from_list(IMPORT_TYPE_COMBO, 'Import Certificate')
        controller = self._get_import_settings_controller()
        if not settings.has_key('Password'):
            settings['Password'] = 'ironport'
        controller.set(settings)
        self._click_submit_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_delete(self, name):
        """Delete existing certificate

        *Parameters:*
        - `name`: existing certificate name

        *Exceptions:*
        - `ValueError`: if there is no certificate profile with given name

        *Examples:*
        | Certificates Delete | mycert |
        """
        if self._is_element_present(CERT_DELETE_LINK(name)):
            self.click_button(CERT_DELETE_LINK(name), 'don\'t wait')
        else:
            raise ValueError('Certificate profile "%s" does not exist' % \
                             (name,))
        self._click_continue_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_get_certificates_info(self):
        """
        Keyword to get all certificates information

        *Parameters:*
        None

        *Return:*
        A dictionary containing following items -
            key - Certificate Name
            value - A dictionary with following keys -
                - Common Name
                - Issued By
                - Domains
                - Status
                - Time Remaining
                - Expiration Date
                - FQDN compliance check

        *Examples:*
        | ${certificates}= | Certificates Get Certificates Info |
        | ${certificate_info}   | Get From Dictionary           |
        | ... | ${certificates} | Cisco ESA Certificate         |
        """
        cert_info = {}
        rows = self._selenium.find_elements_by_xpath("//table[@class='cols']/tbody/tr")
        for row in rows[1:]:
            data = row.find_elements_by_xpath('.//td')
            cert_info[data[0].text.strip()] = {
                'Common Name': data[1].text.strip(),
                'Issued By': data[2].text.strip(),
                'Domains': data[3].text.strip(),
                'Status': data[4].text.strip(),
                'Time Remaining': data[5].text.strip(),
                'Expiration Date': data[6].text.strip(),
                'FQDN compliance checked': data[7].text.strip(),
            }
        return cert_info
    
    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_get_ca_info(self):
        """
        Keyword to get status of custom ca and system ca

        *Parameters:*
        None

        *Return:*
        A dictionary containing following items -
            key - Certificate Name
            value - A dictionary with following keys -
                - Custom List
                - System List

        *Examples:*
        | ${ca_info}=                | Certificates Get CA Info |
        | ${custom_ca_status}        | Get From Dictionary      |
        | ... | ${ca_info}           | Custom List              |
        | Should Be Equal As Strings | ${custom_ca_status}      | Disabled | 
        """
        ca_info = {}
        rows = self._selenium.find_elements_by_xpath(
            "//dl[@class='box']//table[@class='pairs']/tbody/tr")
        for row in rows:
            key = row.find_element_by_xpath('.//th').text.strip().replace(':','')
            value = row.find_element_by_xpath('.//td').text.strip()
            ca_info[key] = value
        return ca_info

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_ca_edit_settings(self, settings={}):
        """Keyword to edit Certificate Authority settings.

        *Parameters:*
        - `settings`: A dictionary with following keys and values
            - `Custom List` - Pass "enable" (without quotes) to enable custom CA list
                              Pass "disable" (without quotes) to disable custom CA list
            - `Certificate To Upload` - Pass certificate full path to be uploaded.
                              Valid when "Custom List" is set to Enable.
            - `Use FQDN Validation` - Pass "Yes" or "No" if you want FQDN to be verified.
            - `System List` - Pass "enable" (without quotes) to enable system CA list
                              Pass "disable" (without quotes) to disable system CA list
        
        *Examples:*
        | ${settings}=                  | Create Dictionary                  |
        | ... | Custom List             | Enable                             |
        | ... | Certificate To Upload   | %{SARF_HOME}/tests/testdata/ca.crt |
        | ... | Use FQDN Validation     | No                                 |
        | ... | System List             | Disable                            |
        | Certificates CA Edit Settings | ${settings}                        |

        | ${settings}=                  | Create Dictionary                                     |
        | ... | Custom List             | Enable                                                |
        | ... | Certificate To Upload   | %{SARF_HOME}/tests/testdata/esa/certificates/cert.crt |
        | ... | System List             | Enable                                                |
        | Certificates CA Edit Settings | ${settings}                                           |
        
        | ${settings}=                  | Create Dictio|nary                                              |
        | ... | Custom List             | Enable                                                          |        
        | ... | Certificate To Upload   | %{SARF_HOME}/tests/testdata/esa/certificates/bug_55387_cert.crt |
        | Certificates CA Edit Settings | ${settings}                                                     |                                

        """
        self.click_button(CA_EDIT_SETTINGS_BUTTON)
        if 'Custom List' in settings:
            if settings['Custom List'].lower() == 'enable':
                self._click_radio_button(CA_CUSTOM_LIST_ENABLE_BUTTON)
                if 'Certificate To Upload' in settings:
                    self.input_text(CA_CUSTOM_LIST_UPLOAD_FILE_BUTTON,
                                    settings['Certificate To Upload'])
                if 'Use FQDN Validation' in settings:
                    if settings['Use FQDN Validation'].lower() == 'yes':
                        self._select_checkbox(CA_CUSTOM_LIST_ENABLE_FQDN_CHECKBOX)
                    else:
                        self._unselect_checkbox(
                            CA_CUSTOM_LIST_ENABLE_FQDN_CHECKBOX)
            if settings['Custom List'].lower() == 'disable':
                self._click_radio_button(CA_CUSTOM_LIST_DISABLE_BUTTON)
        if 'System List' in settings:
            if settings['System List'].lower() == 'enable':
                self._click_radio_button(CA_SYSTEM_LIST_ENABLE_BUTTON)
            if settings['System List'].lower() == 'disable':
                self._click_radio_button(CA_SYSTEM_LIST_DISABLE_BUTTON)
        self._click_submit_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_ca_export_list(self, list_type, file_name=None, cancel_export=False):
        """Keyword to export System or Custom Certificate Authoties.

        *Parameters:*
        - `list_type`: Certificate authority type. Allowed values are -
                       Custom Certificate Authority or System Certificate Authority
        - `file_name`: File name to save the export data. If not passed auto-generated
                       value will be used.
        - `cancel_export`: Pass a true value to Cancel export.

        *Examples:*
        | Certificates CA Export List | Custom Certificate Authority |
        | Certificates CA Export List | System Certificate Authority | system_ca.txt |
        """
        self.select_from_list(CA_EXPORT_LIST_SELECT_OPTION, list_type)
        if file_name:
            self.input_text(CA_EXPORT_LIST_FILE_NAME, file_name)

        if cancel_export:
            self.click_button(CA_EXPORT_LIST_CANCEL_BUTTON)
        else:
            self.click_button(CA_EXPORT_LIST_EXPORT_BUTTON, "don't wait")

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_ca_view_custom_certificate_authorities(self):
        """Keyword to get Custom Certificate Authoties data.

        *Parameters:*
        - None

        *Examples:*
        | ${custom_cas}= | Certificates CA View Custom Certificate Authorities |
        | Log Many       | ${custom_cas}                                       |
        """
        self.click_button(CA_EDIT_SETTINGS_BUTTON)
        self.click_element(CA_VIEW_CUSTOM_CA_LINK)
        return self._get_certificate_authorities()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_ca_view_system_certificate_authorities(self):
        """Keyword to get Seytem Certificate Authoties data.

        *Parameters:*
        - None

        *Examples:*
        | ${system_cas}= | Certificates CA View System Certificate Authorities |
        | Log Many       | ${system_cas}                                       |
        """
        self.click_button(CA_EDIT_SETTINGS_BUTTON)
        self.click_element(CA_VIEW_SYSTEM_CA_LINK)
        return self._get_certificate_authorities()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_get_remaining_days_for_expiry(self, name):
        """Get certificate remaining days for expiry

        *Parameters:*
        - `name`: existing certificate name

        *Exceptions:*
        - `ValueError`: if there is no certificate profile with given name

        *Examples:*
        | Certificates Get Remaining Days For Expiry | mycert |
        """
        if self._is_element_present(CERT_TIME_REMAINING(name)):
            days_remaining = self.get_text(CERT_TIME_REMAINING(name))
        else:
            raise ValueError('Certificate profile "%s" does not exist' % \
                             (name,))
        return days_remaining

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_custom_trusted_root_certificates_download(self, certificate_name='All'):
        """Method to Download Custom Trusted Root Certificate List.

          Note : Firefox profile has to be updated with below mentioned download properties.
            ${firefox_prefs_browser.download.dir}=  Certificates Download Directory path
            ${firefox_prefs_browser.helperApps.neverAsk.openFile}=  application/x-x509-ca-cert
            ${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}=  application/x-x509-ca-cert

        *Exceptions:*
        - `ValueError`: if manage trusted root certificate feature doesn't exist

        *Parameters:*
        - `certificate_name`: Provide the certificate name to be downloaded. If not passed all
                              custom trusted root certificates will be downloaded.

        *Examples:*
        | Certificates Custom Trusted Root Certificates Download |
        | Certificates Custom Trusted Root Certificates Download | SARF CA |
        """
        if self._is_element_present(MANAGE_TRUSTED_ROOT_CERT_BUTTON):
            self.click_button(MANAGE_TRUSTED_ROOT_CERT_BUTTON)
            rows = self._selenium.find_elements_by_xpath(
                '%s/tbody/tr' % CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE)
            self._info('Number of certificates : %s' % (len(rows) - 1))
            if certificate_name != 'All':
                for index in range(2, len(rows) + 1):
                    if rows[index - 1].find_element_by_xpath('.//td'):
                        if rows[index - 1].find_element_by_xpath('.//td').text == certificate_name:
                            try:
                                self.click_element(EXPAND_CERTIFICATE(
                                    CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE, index))
                                self.click_element(DOWNLOAD_CERTIFICATE(
                                    CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE, index))
                                self._info('Certificate %s was downloaded successfully' % certificate_name)
                                break
                            except Exception as error:
                                raise GuiValueError(
                                    'Unable to download custom trusted root certificate %s. Reason - %s' % (certificate_name, error))
                        else:
                            self._info('Row %s doesn\'t have intended certificate %s' % (index, certificate_name))
                            continue
                    else:
                        continue
            else:
                for index in range(2, len(rows) + 1):
                    try:
                        self.click_element(EXPAND_CERTIFICATE(
                            CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE, index))
                        self.click_element(DOWNLOAD_CERTIFICATE(
                            CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE, index))
                        self._info('Certificate %s was downloaded successfully' %
                                   rows[index - 1].find_element_by_xpath('.//td').text)
                    except Exception as error:
                        raise GuiValueError(
                            'Unable to download custom trusted root certificate %s . Reason - %s' % (rows[index].find_element_by_xpath('.//td').text, error))
        else:
            raise ValueError("Manage trusted root certificate \
                                 button doesn't exist")

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_custom_trusted_root_certificates_get_names(self):
        """Method to get all the Custom Trusted Root Certificate names.

        *Parameters:*
        None

        *Examples:*
        | ${custom_cas}=      | Certificates Custom Trusted Root Certificates Get Names |
        | Should Not Be Empty | ${custom_cas}                                           |
        """
        custom_trusted_root_certificates = []
        self.click_button(MANAGE_TRUSTED_ROOT_CERT_BUTTON)
        try:
            rows = self._selenium.find_elements_by_xpath(
                    '%s/tbody/tr' % CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE)
            for row in rows[1:]:
                custom_trusted_root_certificates.append(
                    row.find_element_by_xpath(
                    ".//td//div[contains(@id, 'arrow_closed')]").text.strip())
        except Exception as error:
            self._warn('Could not get custom trusted root certificates\nReason: %s' % error)
        return custom_trusted_root_certificates

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_custom_trusted_root_certificates_delete(self, certificate_name='All'):
        """Method to delete Custom Trusted Root Certificates.

        *Parameters:*
        - `certificate_name`: Provide the certificate name to be deleted. If not passed all
                              custom trusted root certificates will be deleted.

        *Examples:*
        | Certificates Custom Trusted Root Certificates Delete | SARF CA            |
        | ${custom_cas}=  | Certificates Custom Trusted Root Certificates Get Names |
        | List Should Not Contain Value  ${custom_cas}  SARF CA                     |

        | Certificates Cisco Trusted Root Certificates Delete                       |
        | ${custom_cas}=  Certificates Custom Trusted Root Certificates Get Names   |
        | Should Be Empty |  ${custom_cas}                                          |
        """
        if self._is_element_present(MANAGE_TRUSTED_ROOT_CERT_BUTTON):
            self.click_button(MANAGE_TRUSTED_ROOT_CERT_BUTTON)
            rows = self._selenium.find_elements_by_xpath(
                '%s/tbody/tr' % CUSTOM_TRUSTED_ROOT_CERTIFICATE_TABLE)
            self._info('Number of certificates : %s' % (len(rows) - 1))
            if certificate_name != 'All':
                for index in range(2, len(rows) + 1):
                    if rows[index - 1].find_element_by_xpath('.//td'):
                        if rows[index - 1].find_element_by_xpath('.//td').text == certificate_name:
                            try:
                                self.click_element(CUSTOM_TRUSTED_ROOT_CERTIFICATE_DELETE_BUTTON(index))
                                self.click_element(CUSTOM_TRUSTED_ROOT_CERTIFICATE_CONFIRM_DELETE_BUTTON)
                                break
                            except Exception as error:
                                raise GuiValueError(
                                    'Unable to delete custom trusted root certificate %s. Reason - %s' % (certificate_name, error))
                        else:
                            self._info('Row %s doesn\'t have intended certificate %s' % (index, certificate_name))
                            continue
                    else:
                        continue
            else:
                for index in range(2, len(rows) + 1):
                    try:
                        self.click_element(CUSTOM_TRUSTED_ROOT_CERTIFICATE_DELETE_BUTTON(2))
                        self.click_element(CUSTOM_TRUSTED_ROOT_CERTIFICATE_CONFIRM_DELETE_BUTTON)
                    except Exception as error:
                        raise GuiValueError(
                            'Unable to delete certificates %s due to %s' % (rows[index].find_element_by_xpath('.//td').text, error))
        else:
            raise ValueError("Manage trusted root certificate \
                                 button doesn't exist")

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_cisco_trusted_root_certificates_download(self, certificate_name='All'):
        """Method to Download Cisco Trusted Root Certificates.

          Note : Firefox profile has to be updated with below mentioned download properties.
            ${firefox_prefs_browser.download.dir}=  Certificates Download Directory path
            ${firefox_prefs_browser.helperApps.neverAsk.openFile}=  application/x-x509-ca-cert
            ${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}=  application/x-x509-ca-cert

        *Exceptions:*
        - `ValueError`: if manage trusted root certificate feature doesn't exist

        *Parameters:*
        - `certificate_name`: Provide the certificate name to be downloaded. If not passed all
                              cisco trusted root certificates will be downloaded.

        *Examples:*
        | Certificates Cisco Trusted Root Certificates Download |
        | Certificates Cisco Trusted Root Certificates Download | ACCVRAIZ1 |
        """
        if self._is_element_present(MANAGE_TRUSTED_ROOT_CERT_BUTTON):
            self.click_button(MANAGE_TRUSTED_ROOT_CERT_BUTTON)
            rows = self._selenium.find_elements_by_xpath(
                '%s/tbody/tr' % CISCO_TRUSTED_ROOT_CERTIFICATE_TABLE)
            self._info('Number of certificates : %s' % (len(rows) - 1))
            if certificate_name != 'All':
                for index in range(2, len(rows) + 1):
                    if rows[index - 1].find_element_by_xpath('.//td'):
                        if rows[index - 1].find_element_by_xpath('.//td').text == certificate_name:
                            try:
                                self.click_element(EXPAND_CERTIFICATE(
                                    CISCO_TRUSTED_ROOT_CERTIFICATE_TABLE, index))
                                self.click_element(DOWNLOAD_CERTIFICATE(
                                    CISCO_TRUSTED_ROOT_CERTIFICATE_TABLE, index))
                                self.click_element(COLLAPSE_CERTIFICATE(
                                    CISCO_TRUSTED_ROOT_CERTIFICATE_TABLE, index))
                                self._info('Certificate %s was downloaded successfully' % certificate_name)
                                break
                            except Exception as error:
                                raise GuiValueError(
                                    'Unable to download custom trusted root certificate %s. Reason - %s' % (certificate_name, error))
                        else:
                            self._info('Row %s doesn\'t have intended certificate %s' % (index, certificate_name))
                            continue
                    else:
                        continue
            else:
                for index in range(2, len(rows) + 1):
                    try:
                        self.click_element(EXPAND_CERTIFICATE(
                            CISCO_TRUSTED_ROOT_CERTIFICATE_TABLE, index))
                        self.click_element(DOWNLOAD_CERTIFICATE(
                            CISCO_TRUSTED_ROOT_CERTIFICATE_TABLE, index))
                        self.click_element(COLLAPSE_CERTIFICATE(
                            CISCO_TRUSTED_ROOT_CERTIFICATE_TABLE, index))
                        self._info('Certificate %s was downloaded successfully' %
                                   rows[index - 1].find_element_by_xpath('.//td').text)
                    except Exception as error:
                        raise GuiValueError(
                            'Unable to download custom trusted root certificate %s . Reason - %s' % (rows[index].find_element_by_xpath('.//td').text, error))
        else:
            raise ValueError("Manage trusted root certificate button doesn't exist")

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def certificates_cisco_trusted_root_certificates_get_names(self):
        """Method to get all the Cisco Trusted Root Certificate names.

        *Parameters:*
        None

        *Examples:*
        | ${system_cas}=      | Certificates Cisco Trusted Root Certificates Get Names |
        | Should Not Be Empty | ${system_cas}                                          |
        | Should Contain      | ${system_cas} | ACCVRAIZ1                              |
        """
        cisco_trusted_root_certificates = []
        self.click_button(MANAGE_TRUSTED_ROOT_CERT_BUTTON)
        try:
            rows = self._selenium.find_elements_by_xpath(
                '%s/tbody/tr' % CISCO_TRUSTED_ROOT_CERTIFICATE_TABLE)
            for row in rows[1:]:
                cisco_trusted_root_certificates.append(
                    row.find_element_by_xpath(
                        ".//td//div[contains(@id, 'arrow_closed')]").text.strip())
        except Exception as error:
            self._warn('Could not get cisco trusted root certificates\nReason: %s' % error)
        return cisco_trusted_root_certificates

    def certificates_custom_trusted_root_certificates_get_details(self, certificate_name):
        """Method to get all the Custom Trusted Root Certificate details.

        *Parameters:*
        None

        *Examples:*
        | ${custom_cas}=  | Certificates Custom Trusted Root Certificates Get Details |
        | Should Contain  | ${custom_cas} | cisco |
        """
        certificate_details = {}
        certificate_list = self.certificates_custom_trusted_root_certificates_get_names()
        if certificate_name in certificate_list:
            certificate_index = certificate_list.index(certificate_name) + 2
            certificate_link = CUSTOM_CERTIFICATE_LINK % certificate_index
            expiry_link = CUSTOM_CERTIFICATE_EXPIRY_LINK % certificate_index
            on_cisco_list = CUSTOM_CERTIFICATE_ON_CISCO_LIST % certificate_index

            self.click_element(certificate_link + '/a', "don't wait")

            certificate_details['custom_name'] = self._get_text(certificate_link + CUSTOM_CERTIFICATE_CUSTOM_NAME)
            certificate_details['org'] = self._get_text(certificate_link + CUSTOM_CERTIFICATE_ORGANIZATION)
            certificate_details['org_unit'] = self._get_text(certificate_link + CUSTOM_CERTIFICATE_ORGANIZATION_UNIT )
            certificate_details['country'] = self._get_text(certificate_link + CUSTOM_CERTIFICATE_COUNTRY)
            certificate_details['basic_constrain'] = self._get_text(certificate_link + CUSTOM_CERTIFICATE_BASIC_CONSTRAIN)
            certificate_details['expiry_date'] = self._get_text(expiry_link)
            certificate_details['basic_constrain'] = self._get_text(on_cisco_list)
            self._info('certificate Details %s' % certificate_details)

            return certificate_details
        else:
            raise ValueError('`%s` Certificate is not present on the page' % (certificate_name,))

    # Helper Methods
    def _get_certificate_authorities(self):
        certificate_authorities = ''

        window_before = self._selenium.window_handles[0]
        window_after = self._selenium.window_handles[1]
        self._selenium.switch_to.window(window_after)
        time.sleep(3)

        rows = self._selenium.find_elements_by_xpath(
            '//table[@class="layout"]/tbody/tr')
        for row in rows:
            if len(row.find_elements_by_xpath('.//td')) == 1:
                certificate_authorities += row.find_elements_by_xpath('.//td')[
                    0].text.strip() + "\n"
            elif len(row.find_elements_by_xpath('.//td')) == 2:
                certificate_authorities += row.find_elements_by_xpath('.//td')[
                    1].text.strip() + "\n\n"
            else:
                continue

        self._selenium.close()
        self._selenium.switch_to.window(window_before)
        self.click_button(CANCEL_BUTTON)

        return certificate_authorities

#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/network/certificates.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
from common.gui.guiexceptions import GuiValueError

from certificates_def.import_settings import ImportSettings

ADD_CERTIFICATE_BUTTON = "//input[@value='Add Certificate...']"
IMPORT_TYPE_COMBO = "//select[@id='add_import_option']"
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
SUBMIT_BUTTON = "//input[@value='Submit']"

CERTS_TABLE = "//table[@class='cols']"
CERT_DELETE_LINK = lambda name: "%s//td[normalize-space()='%s']"\
                        "/following-sibling::td[7]/img" % \
                        (CERTS_TABLE, name)

CERT_TIME_REMAINING = lambda name: "%s//td[normalize-space()='%s']"\
                        "/following-sibling::td[5]/span" % \
                        (CERTS_TABLE, name)

PAGE_PATH = ('Network', 'Certificates')
MANAGE_TRUSTED_ROOT_CERT_BUTTON = "//input[@value='Manage Trusted Root " \
                                  "Certificates...']"
EXPAND_CERTIFICATE = lambda certificate: "%s/tbody/tr[%s]" % \
                                         (CERTS_TABLE, certificate)
COLLAPSE_CERTIFICATE = lambda certificate: "%s/tbody/tr[%s]/td//a" % \
                                           (CERTS_TABLE, certificate)
DOWNLOAD_CERTIFICATE = lambda certificate: "%s/tbody/tr[%s]//table[@class='layout']" \
                                           "/tbody//a" % (CERTS_TABLE, certificate)


class Certificates(GuiCommon):
    """Keywords for GUI interaction with Network -> Certificates
    page"""

    def get_keyword_names(self):
        return ['certificates_create',
                'certificates_import',
                'certificates_delete',
                'certificates_get_remaining_days_for_expiry',
                'certificates_download_trusted_root_certificates']

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
                               size=None,):
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
        if domains is not None:
            self.input_text(FIELD_DOMAINS, domains)
            self.press_key(FIELD_DOMAINS, "\\13")
        if email is not None:
            self.input_text(FIELD_EMAIL, email)
            #self.send_keys(FIELD_EMAILS)
        if duration is not None:
            self.input_text(FIELD_DURATION, duration)
        if size == '2048':
            self._click_radio_button(RADIO_2048)
        elif size == '1024':
            self._click_radio_button(RADIO_1024)
        self.click_button(NEXT_BUTTON)
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

        *Examples:*
        Do not forget to include the
        generate_sign_server_certificate.txt resource into your suite
        | ${key_path} | ${cert_path}= | Generate Sign Server Certificate |
        | ${pk12_path}= | Generate PKCS12 File | ${key_path} | ${cert_path} |
        | ${import_settings}= | Create Dictionary |
        | ... | Name | new_my_cert |
        | ... | Path | ${pk12_path} |
        | ... | Password | ironport |
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
    def certificates_download_trusted_root_certificates(self):
        """Method to Download Cisco Trusted Root Certificate List.

        Note : Firefox profile has to be updated with below mentioned download properties.
            ${firefox_prefs_browser.download.dir}=  Certificates Download Directory path
            ${firefox_prefs_browser.helperApps.neverAsk.openFile}=  application/x-x509-ca-cert
            ${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}=  application/x-x509-ca-cert

        *Exceptions:*
        - `ValueError`: if manage trusted root certificate feature doesn't exist

        *Examples:*
        | Certificates Download Trusted Root Certificates |
        """
        if self._is_element_present(MANAGE_TRUSTED_ROOT_CERT_BUTTON):
            self.click_button(MANAGE_TRUSTED_ROOT_CERT_BUTTON)
            rows = self._selenium.find_elements_by_xpath('%s/tbody/tr' % CERTS_TABLE)
            self._info('Number of certificates : %s' % len(rows))
            for certificate in range(2,len(rows)):
                self._download_certificates(certificate)
        else:
            raise ValueError("Manage trusted root certificate \
                                 button doesn't exist")

    def _download_certificates(self,cert_name):
        try:
            self.click_element(EXPAND_CERTIFICATE(cert_name))
            self.click_element(DOWNLOAD_CERTIFICATE(cert_name))
            self.click_element(COLLAPSE_CERTIFICATE(cert_name))
        except Exception as error:
            raise GuiValueError('Unable to download certificates due to %s' % error)

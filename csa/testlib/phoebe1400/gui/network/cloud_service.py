
from common.gui.guicommon import GuiCommon
from common.gui.decorators import go_to_page, set_speed
from common.gui.guiexceptions import ConfigError

PAGE_PATH = ('Network', 'Cloud Service Settings')
CLOUD_SERVICE_SETTINGS_ENABLE = "//input[@title='Enable...' and @type='button']"
CISCO_CLOUD_SERVICES_ENABLE = "//input[@id='cloud_service' and @type='checkbox']"
CLOUD_SERVICE_DISABLED_STATUS = "//*[@class='text-info']"
CISCO_SECURE_SERVER_COMBO = "//select[@id='secure_x_server']"
SECUREX_CHECKBOX = "//input[@id='secure_x_status' and @type='checkbox']"
CISCO_SUCCESS_NETWORK_CHECKBOX = "//input[@id='csn_status' and @type='checkbox']"
EDIT_GLOBAL_SETTINGS = "//input[@title='Edit Global Settings...' and @type='button']"
CISCO_SERVICE_SETTINGS = "//*[@class='pairs']"
CISCO_SERVICE_SETTINGS_TH = "/tbody/tr[%s]/th"
CISCO_SERVICE_SETTINGS_TD = "/tbody/tr[%s]/td"
REGISTER_TOKEN = "//input[@id='token']"
REGISTER_BUTTON = "//input[@title='Register' and @type='button']"
DEREGISTER_BUTTON = "//input[@title='Deregister' and @type='button']"
DEREGISTER_CNF_BUTTON = "//*[@id='confirmation_dialog']/div[3]/span/span[1]/span/button"
REGISTER_FAIL_MSG = "//td[contains(text(), 'The registration failed because of an invalid or expired token')]"
SUBMIT_BUTTON = "//input[@title='Submit' and @type='button']"

class CloudService(GuiCommon):

    """Keywords for Network -> Cloud Service Settings"""

    def get_keyword_names(self):
        return [
            'enable_cloud_service',
            'disable_cloud_service',
            'edit_cloud_service',
            'get_cloud_service_status',
            'get_cloud_service_settings',
            'enable_secureX',
            'disable_secureX',
            'get_secureX_status',
            'enable_csn',
            'disable_csn',
            'get_csn_status',
            'register_cloud',
            'deregister_cloud',
            'is_appliance_registered_in_cloud'
            ]

    def _select_cisco_secure_server(self, secure_server):
        self.select_from_list_by_label(CISCO_SECURE_SERVER_COMBO, secure_server)

    def _change_state_securex(self, state):
        self._set_checkbox(state, SECUREX_CHECKBOX)

    def _change_state_cisco_success_network(self, state):
        self._set_checkbox(state, CISCO_SUCCESS_NETWORK_CHECKBOX)

    def _perform_edit_settings(self):
        if not self._is_element_present(EDIT_GLOBAL_SETTINGS):
            raise ConfigError("Could not find 'Edit Settings' button: Cloud Service is not enabled")
        else:
            self.click_button(EDIT_GLOBAL_SETTINGS)

    @go_to_page(PAGE_PATH)
    def enable_cloud_service(self, secure_server=None):
        """ Enables Cisco Cloud Services in Network -> Cloud Service Settings
           *Parameters:*
           server : Cisco Cloud Server. It is a optional parameter.
           *Examples:*
           | Enable Cloud Service |
           | Enable Cloud Service | EUROPE (api.eu.sse.itd.cisco.com) |
           | Enable Cloud Service | AMERICAS (stage-api-sse.cisco.com)|
       """

        if self._is_element_present(CLOUD_SERVICE_SETTINGS_ENABLE):
            self.click_button(CLOUD_SERVICE_SETTINGS_ENABLE)
            self._wait_until_element_is_present(CISCO_CLOUD_SERVICES_ENABLE, timeout=10)
            self._set_checkbox(True, CISCO_CLOUD_SERVICES_ENABLE)
            if secure_server:
                self._select_cisco_secure_server(secure_server)
            self.click_button(SUBMIT_BUTTON)
        else:
            self._info('Cloud services is already enabled')

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def get_cloud_service_status(self):
        """
        :return: will return the cloud service status. DISABLED|ENABLED
        """
        if self._is_element_present(CLOUD_SERVICE_DISABLED_STATUS):
            return 'Disabled'
        else:
            return 'Enabled'

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def get_cloud_service_settings(self):
        """
        To get the Cloud Service Settings
        :return: settings dictionary
        """
        settings = {}
        for index in range(1, 6):
            key = ''.join([CISCO_SERVICE_SETTINGS, CISCO_SERVICE_SETTINGS_TH % index])
            value = ''.join([CISCO_SERVICE_SETTINGS, CISCO_SERVICE_SETTINGS_TD % index])
            settings[self.get_text(key)] = self.get_text(value)
        return settings

    @go_to_page(PAGE_PATH)
    def edit_cloud_service(self, secure_server):
        """To edit the cloud services
        *Parameters:*
           server : Cisco Cloud Server. It is a optional parameter.
           *Examples:*
           | Edit Cloud Service | EUROPE (api.eu.sse.itd.cisco.com) |
        """
        if self._is_element_present(CLOUD_SERVICE_DISABLED_STATUS):
            self._debug('Cisco Secure Services already disabled..')
            raise ConfigError("Cisco Secure Services is disabled..")

        if secure_server:
            self._perform_edit_settings()
            self._select_cisco_secure_server(secure_server)
            self.click_button(SUBMIT_BUTTON)

    @go_to_page(PAGE_PATH)
    def disable_cloud_service(self):
        """ Disables Threat Response in Network -> Cloud Service Settings
            *Examples:*
            | Disable Cloud Service |
        """
        self._perform_edit_settings()
        self._set_checkbox(False, CISCO_CLOUD_SERVICES_ENABLE)
        self.click_button(SUBMIT_BUTTON)

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def enable_csn(self):
        """ Enable 'Cisco Success Network' in Network -> Cloud Service Settings

        *Parameters:*
        None

        *Examples:*
        | Enable CSN |
        """

        self._perform_edit_settings()
        self._change_state_cisco_success_network(True)
        self.click_button(SUBMIT_BUTTON)

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def disable_csn(self):
        """ Disable 'Cisco Success Network' in Network -> Cloud Service Settings
        *Examples:*
        | Disable CSN |
        """

        self._perform_edit_settings()
        self._change_state_cisco_success_network(False)
        self.click_button(SUBMIT_BUTTON)

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def get_csn_status(self):
        """ Get 'Cisco Success Networlk' Status from Network -> Cloud Service Settings
            Status will be returned as either Enabled or Disabled

        *Examples:*
        | ${status}=  Get CSN Status |
        | Log  ${status} |
        """
        settings = self.get_cloud_service_settings()
        if 'Cisco Success Network:' in settings:
            return settings['Cisco Success Network:']
        else:
            raise ConfigError("Failed to get Cisco Success Network status")

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def enable_secureX(self):
        """ Enables SecureX in Cisco Cloud Services
         *Examples:*
        | Enable SecureX |
        """

        self._perform_edit_settings()
        self._change_state_securex(True)
        self.click_button(SUBMIT_BUTTON)

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def disable_secureX(self):
        """ Disable SecureX in Cisco Cloud Services
        *Examples:*
        | Disable SecureX |
        """
        self._perform_edit_settings()
        self._change_state_securex(False)
        self.click_button(SUBMIT_BUTTON)

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def get_secureX_status(self):
        """ Get 'SecureX Status from Network -> Cloud Service Settings
            Status will be returned as either Enabled or Disabled

        *Parameters:*
        None

        *Examples:*
        | ${status}=  Get SecureX Status |
        | Log  ${status} |
        """
        settings = self.get_cloud_service_settings()
        if 'SecureX:' in settings:
            return settings['SecureX:']
        else:
            raise ConfigError("Failed to get SecureX status")

    @go_to_page(PAGE_PATH)
    def register_cloud(self, token_str):
        """ Register Cloud Service Settings

        *Parameters:*
        - `token_str`: Token string taken from stage portal site.

        *Examples:*
        | Register Cloud  |b92baf968e19418a33fc9023529e0d82 |

        """
        self._info(self._is_element_present(REGISTER_TOKEN))
        if self._is_element_present(REGISTER_TOKEN):
            self.input_text(REGISTER_TOKEN, token_str)
            self.click_element(REGISTER_BUTTON, "don't wait")
            if self._is_element_present(REGISTER_FAIL_MSG):
                raise ConfigError("Invalid Registration string given")
        else:
            raise ConfigError("Could not find 'Cloud Service Register' button")

    @go_to_page(PAGE_PATH)
    def deregister_cloud(self):
        """ Deregister Cloud Service Settings

        *Parameters:*
        None

        *Examples:*
        | Deregister Cloud |

        """
        self._wait_until_element_is_present(DEREGISTER_BUTTON, timeout=10)
        if not self._is_element_present(DEREGISTER_BUTTON):
            raise ConfigError("Could not find 'Cloud Service Deregister' button")
        self.click_element(DEREGISTER_BUTTON, "don't wait")
        self.click_element(DEREGISTER_CNF_BUTTON, "don't wait")

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def is_appliance_registered_in_cloud(self):
        """ Get 'Registered Appliance' Status from Network -> Cloud Service Settings
            Status will be returned as Boolean either True or False

        *Parameters:*
        None

       *Examples:*
        | ${status}=  Is Appliance Registered In Cloud |
        | Log  ${status} |

        """
        return self._is_element_present(DEREGISTER_BUTTON)

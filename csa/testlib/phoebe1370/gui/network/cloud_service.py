import common.gui.guiexceptions as guiexceptions
from common.gui.decorators import go_to_page
from cloud_service_def.cloud_service_settings import CloudServiceSettings
from common.gui.guicommon import GuiCommon
from cloud_service_def.cloud_service_settings import CiscoSuccessNetwork


PAGE_PATH = ('Network', 'Cloud Service Settings')

THREAT_RESPONSE_EDIT_SETTINGS = "//input[contains(@onclick, 'EditServiceSettings')]"
THREAT_RESPONSE_DISABLED = "//th[text()='Threat Response:']//following-sibling::td[contains(text(), 'Disabled')]"
THREAT_RESPONSE_ENABLED = "//th[text()='Threat Response:']//following-sibling::td[contains(text(), 'Enabled')]"

CSN_EDIT_SETTINGS = "//input[contains(@onclick, 'FormEditCSNStatus')]"
CSN_DISABLED = "//th[contains(text(),'Cisco Success Network:')]//following-sibling::td[contains(text(), 'Disabled')]"
CSN_ENABLED = "//th[contains(text(),'Cisco Success Network:')]//following-sibling::td[contains(text(), 'Enabled')]"

REGISTER_TOKEN = "//input[@id='token']"
REGISTER_BUTTON = "//input[@title='Register' and @type='button']"
DEREGISTER_BUTTON = "//input[@title='Deregister' and @type='button']"
DEREGISTER_CNF_BUTTON = "//button[@id='yui-gen28-button']"
REGISTER_FAIL_MSG = "//td[contains(text(), 'The registration failed because of an invalid or expired token')]"

class CloudService(GuiCommon):

    """Keywords for Network -> Cloud Service Settings"""

    def get_keyword_names(self):
        return [
            'enable_threat_response',
            'disable_threat_response',
            'get_threat_response_status',
            'enable_csn',
            'disable_csn',
            'get_csn_status',
            'register_cloud',
            'deregister_cloud']

    @go_to_page(PAGE_PATH)
    def enable_threat_response(self,  server=None):
        """ Enables Threat Response in Network -> Cloud Service Settings

        *Parameters:*
        server : Threat Response Server. It is a optional parameter.

        *Examples:*
        | Enable Threat Response |
        | Enable Threat Response | EUROPE (api.eu.sse.itd.cisco.com) |
        | Enable Threat Response | AMERICAS (stage-api-sse.cisco.com) |
        """

        if not self._is_element_present(THREAT_RESPONSE_EDIT_SETTINGS):
            raise guiexceptions.ConfigError("Could not find 'Edit Settings' button")
        else:
            self.click_button(THREAT_RESPONSE_EDIT_SETTINGS)
        settings = dict()
        settings['Threat Response'] = True
        if server:
            settings['Threat Response Server'] = server
        self.cloud_service_controller = CloudServiceSettings(self)
        self.cloud_service_controller.set(settings)
        self._click_submit_button(skip_wait_for_title=True)

    @go_to_page(PAGE_PATH)
    def disable_threat_response(self):
        """ Disables Threat Response in Network -> Cloud Service Settings

        *Parameters:*
        None

        *Examples:*
        | Disable Threat Response |
        """

        if not self._is_element_present(THREAT_RESPONSE_EDIT_SETTINGS):
            raise guiexceptions.ConfigError("Could not find 'Edit Settings' button")
        else:
            self.click_button(THREAT_RESPONSE_EDIT_SETTINGS)
        settings = dict()
        settings['Threat Response'] = False
        self.cloud_service_controller = CloudServiceSettings(self)
        self.cloud_service_controller.set(settings)
        self._click_submit_button(skip_wait_for_title=True)

    @go_to_page(PAGE_PATH)
    def get_threat_response_status(self):
        """ Get Threat Response Status from Network -> Cloud Service Settings
            Status will be returned as either Enabled or Disabled
        *Parameters:*
        None

        *Examples:*
        | ${status}=  Get Threat Response Status |
        | Log  ${status} |
        """

        if self._is_element_present(THREAT_RESPONSE_DISABLED):
            return  "Disabled"
        elif self._is_element_present(THREAT_RESPONSE_ENABLED):
            return  "Enabled"

    @go_to_page(PAGE_PATH)
    def enable_csn(self):
        """ Enable 'Cisco Success Network' in Network -> Cloud Service Settings

        *Parameters:*
        None

        *Examples:*
        | Enable CSN |
        """

        if not self._is_element_present(CSN_EDIT_SETTINGS):
            raise guiexceptions.ConfigError("Could not find 'Edit Settings' button")
        else:
            self.click_button(CSN_EDIT_SETTINGS)
        settings = dict()
        settings['Cisco Success Network Settings'] = True
        self.cloud_service_controller = CiscoSuccessNetwork(self)
        self.cloud_service_controller.set(settings)
        self._click_submit_button(skip_wait_for_title=True)

    @go_to_page(PAGE_PATH)
    def disable_csn(self):
        """ Disable 'Cisco Success Network' in Network -> Cloud Service Settings

        *Parameters:*
        None

        *Examples:*
        | Disable CSN |
        """

        if not self._is_element_present(CSN_EDIT_SETTINGS):
            raise guiexceptions.ConfigError("Could not find 'Edit Settings' button")
        else:
            self.click_button(CSN_EDIT_SETTINGS)
        settings = dict()
        settings['Cisco Success Network Settings'] = False
        self.cloud_service_controller = CiscoSuccessNetwork(self)
        self.cloud_service_controller.set(settings)
        self._click_submit_button(skip_wait_for_title=True)

    @go_to_page(PAGE_PATH)
    def get_csn_status(self):
        """ Get 'Cisco Success Networlk' Status from Network -> Cloud Service Settings
            Status will be returned as either Enabled or Disabled

        *Parameters:*
        None

        *Examples:*
        | ${status}=  Get CSN Status |
        | Log  ${status} |
        """

        if self._is_element_present(CSN_DISABLED):
            return  "Disabled"
        elif self._is_element_present(CSN_ENABLED):
            return  "Enabled"

    @go_to_page(PAGE_PATH)
    def register_cloud(self, token_str):
        """ Register Cloud Service Settings

        *Parameters:*
        - `token_str`: Token string taken from stage portal site.

        *Examples:*
        | Register Cloud   b92baf968e19418a33fc9023529e0d82 |

        """

        self._info(self._is_element_present(REGISTER_TOKEN))
        if self._is_element_present(REGISTER_TOKEN):
            self.input_text(REGISTER_TOKEN, token_str)
            self.click_element(REGISTER_BUTTON, "don't wait")
            if self._is_element_present(REGISTER_FAIL_MSG):
                raise guiexceptions.ConfigError("Invalid Registration string given")
        else:
            raise guiexceptions.ConfigError("Could not find 'Cloud Service Deregister' button")

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
            raise guiexceptions.ConfigError("Could not find 'Cloud Service Deregister' button")
        self.click_element(DEREGISTER_BUTTON, "don't wait")
        self.click_element(DEREGISTER_CNF_BUTTON, "don't wait")


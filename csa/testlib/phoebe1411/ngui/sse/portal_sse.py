# imports

from common.ngui.ngguicommon import NGGuiCommon
from portal_sse_def import PORTAL_SSE
from common.gui.guiexceptions import GuiLoginFailureError, GuiApplicationError

class PortalSSE(NGGuiCommon):

    def get_keyword_names(self):
        return ['get_registration_token_string',
                'delete_registred_device',]


    def portal_sse_login(self, username, password):
        self.click_button(PORTAL_SSE.LOGIN_BUTTON_1)
        self._wait_until_element_is_present(PORTAL_SSE.CISCO_SECURITY_ACCOUNT, timeout=10)
        self.click_element(PORTAL_SSE.CISCO_SECURITY_ACCOUNT)
        self._wait_until_element_is_present(PORTAL_SSE.USERNAME_FIELD, timeout=10)
        self.input_text(PORTAL_SSE.USERNAME_FIELD, username)
        self.click_button(PORTAL_SSE.LOGIN_BUTTON_2)
        self.input_password(PORTAL_SSE.PSW_FIELD, password)
        self.click_button(PORTAL_SSE.LOGIN_BUTTON_2)
        self._wait_until_element_is_present(PORTAL_SSE.SSE_LOGO, timeout=10)
        self.wait_for_angular()
        if not self._is_element_present(PORTAL_SSE.SSE_LOGO):
            raise GuiLoginFailureError("Security Services Exchange Login Failed")

    def get_token_string(self, token_timeout=None):
        self.click_element(PORTAL_SSE.ADD_DEVICE_BUTTON)
        if token_timeout:
            self._wait_until_element_is_present(PORTAL_SSE.TOKEN_EXP_TIME)
            self.select_ng_dropdown(PORTAL_SSE.TOKEN_EXP_TIME, token_timeout)
        self.click_button(PORTAL_SSE.ADD_DEVICE_OK_BUTTON)
        self._wait_until_element_is_present(PORTAL_SSE.CLOSE_BUTTON)
        self.click_button(PORTAL_SSE.CLOSE_BUTTON)
        self.click_element(PORTAL_SSE.REFRESH_BUTTON)
        self.click_element(PORTAL_SSE.SORT_BY_STATUS)
        self._wait_until_element_is_present(PORTAL_SSE.COPY_BUTTON)
        self.click_element(PORTAL_SSE.COPY_BUTTON)
        self._wait_until_element_is_present(PORTAL_SSE.TOKEN_STR)
        token_string = self.get_text(PORTAL_SSE.TOKEN_STR).strip()
        self.click_button(PORTAL_SSE.CLOSE_BUTTON)
        if len(token_string) == 32 and  token_string.isalnum():
            return token_string
        else:
            self._info("Invalid Token String: " + token_string)
            raise ValueError("Invalid Token String: " + token_string)

    def get_registration_token_string(self, username, password, token_timeout=None):
        """ Return registration token string from Security Services Exchange portal site.
        https://stage-portal.sse.itd.cisco.com/login

        *Parameters:*
        - `username`: Username to login Security Services Exchange portal site.
        - `password`: Password to login Security Services Exchange portal site.

        *Examples:*
        | Get Registration Token String  testuser@cisco.com  Cisco123$  ${PORTAL_SSE_URL} |

        """

        self.portal_sse_login(username, password)
        if token_timeout:
            token_string = self.get_token_string(token_timeout)
        else:
            token_string = self.get_token_string()
        return token_string

    def delete_registred_device(self, username, password):
        """ Delete registred devices from Security Services Exchange portal site.
        https://stage-portal.sse.itd.cisco.com/login

        *Parameters:*
        - `username`: Username to login Security Services Exchange portal site.
        - `password`: Password to login Security Services Exchange portal site.

        *Examples:*
        | Delete Registred Device  testuser@cisco.com  mypasswd |

        """

        self.portal_sse_login(username, password)
        num_of_entries = int(self.get_text(PORTAL_SSE.NUM_OF_ENTRIES))
        for i in range(num_of_entries):
            self.click_element(PORTAL_SSE.TRASH_ICON)
            self._wait_until_element_is_present(PORTAL_SSE.DELETE_CONFIRM)
            self.click_button(PORTAL_SSE.DELETE_CONFIRM)
            self.click_element(PORTAL_SSE.REFRESH_BUTTON)

        if self._is_element_present(PORTAL_SSE.TRASH_ICON):
            raise GuiApplicationError("Deleting all entries is not successful")

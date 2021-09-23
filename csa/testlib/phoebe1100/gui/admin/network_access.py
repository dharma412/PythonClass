#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/admin/network_access.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

EDIT_BUTTON = "//input[@value='Edit Settings...']"
CANCEL_BUTTON = "//input[@value='Cancel']"
CONFIRMATION_DIALOG = "//div[@id='confirmation_dialog']"

# Settings
ACTIVITY_TIMEOUT = ('Web UI Inactivity Timeout',
                    "//input[@name='session_timeout']")
ACCESS_COMBO = ('User Access',
                "//select[@id='access_type']")
ACCESS_LIST = ('Access List',
               "//textarea[@id='access_list']")
PROXY_LIST = ('Proxy List',
              "//textarea[@id='proxy_list']")
IP_HEADER = ('Origin IP Header',
             "//input[@id='ip_header']")


class NetworkAccessSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_combos(new_value,
                         ACCESS_COMBO)
        self._set_edits(new_value,
                        ACTIVITY_TIMEOUT,
                        ACCESS_LIST,
                        PROXY_LIST,
                        IP_HEADER)

    def get(self):
        details = self._get_values(ACCESS_COMBO,
                                   ACTIVITY_TIMEOUT,
                                   ACCESS_LIST,
                                   PROXY_LIST,
                                   IP_HEADER)
        return details


PAGE_PATH = ('System Administration', 'Network Access')


class NetworkAccess(GuiCommon):
    """Keywords for ESA GUI interaction with System Administration -> Network
    Access page
    """

    def get_keyword_names(self):
        return ['network_access_get_details',
                'network_access_edit']

    def _get_settings_controller(self):
        if not hasattr(self, '_settings_controller'):
            self._settings_controller = NetworkAccessSettings(self)
        return self._settings_controller

    @go_to_page(PAGE_PATH)
    def network_access_edit(self, settings={}):
        """Edit Network access settings

        *Parameters:*
        - `settings`: dictionary whose items are
        setting names and their values. This dictionary can
        contain the next items:
        | `Web UI Inactivity Timeout` | web ui inactivity timeout, minutes |
        | `User Access` | user access setting. Either "Allow Any Connection",
        "Only Allow Specific Connections",
        "Only Allow Specific Connections Through Proxy",
        "Allow Specific Connections Directly or Through Proxy" |
        | `Access List` | access list. Valid entries are an IP address,
        IP range, or CIDR range. Separate multiple entries with commas. Examples:
        10.0.0.1, 2001:420:80:1::5, 10.0.0.1-24, 2000::1-2000::10, 10.0.0.0/8,
        2001:db8::/32.). Mandatory if `User Access` is NOT set to
        "Allow Any Connection" |
        | `Proxy List` | IP Address of Proxy Server(s). Separate multiple entries
        with commas. Mandatory if `User Access` is set to
        "Only Allow Specific Connections Through Proxy" or
        "Allow Specific Connections Directly or Through Proxy" |
        | `Origin IP Header` | origin IP header. Available if `User Access` is set
        to "Only Allow Specific Connections Through Proxy" or
        "Allow Specific Connections Directly or Through Proxy" |

        *Exceptions:*
        - `ValueError`: if any of given values is not correct

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | Web UI Inactivity Timeout | 25 |
        | ... | User Access | Allow Specific Connections Directly or Through Proxy |
        | ... | Access List | 2000::1-2000::10, 10.0.0.0/8 |
        | ... | Proxy List | 1.1.1.1, 2.2.2.2 |
        | ... | Origin IP Header | x-bla-bla |
        | Network Access Edit | ${settings} |
        """
        self.click_button(EDIT_BUTTON)

        controller = self._get_settings_controller()
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def network_access_get_details(self):
        """Get Network access settings

        *Return:*
        Dictionary whose items are
        setting names and their values. This dictionary can
        contain the next items:
        | `Web UI Inactivity Timeout` | web ui inactivity timeout, minutes |
        | `User Access` | user access setting |
        | `Access List` | access list |
        | `Proxy List` | IP Address of Proxy Server(s) |
        | `Origin IP Header` | origin IP header |

        *Examples:*
        | ${settings}=  | Network Access Get Details |
        | ${timeout}= | Get From Dictionary | ${settings} | Web UI Inactivity Timeout |
        | Log | ${tiemout} |
        """
        self.click_button(EDIT_BUTTON)

        controller = self._get_settings_controller()
        details = controller.get()
        self.click_button(CANCEL_BUTTON)
        return details

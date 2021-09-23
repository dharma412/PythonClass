# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/options/slbl_admin.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

import functools
import sys

from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon

from slbl_admin_def.recipient_settings import RecipientSettings, \
                RECIPIENT_ADDRESS, SENDER_LIST

ADD_BUTTON = "//input[@value='Add']"

RECIPIENT_COL_MAPPING = {'Address': 1,
                         'Senders List': 2}
RECIPIENTS_TABLE = "//table[@summary]"
ALL_RECIPIENTS = "{0}/tbody[last()]/tr[td]".format(RECIPIENTS_TABLE)
RECIPIENT_BY_ADDRESS = lambda address: \
        "{0}/td[1][normalize-space()='{1}']".format(
                    ALL_RECIPIENTS, address)
RECIPIENT_EDIT_BY_ADDRESS = lambda address: \
        "{0}/following-sibling::td[2]//input".format(RECIPIENT_BY_ADDRESS(address),
                                                    address)
RECIPIENT_DELETE_BY_ADDRESS = lambda address: \
        "{0}/following-sibling::td[3]//img".format(RECIPIENT_BY_ADDRESS(address),
                                                  address)
RECIPIENT_DELETE_BY_ADDRESS_CONFIRM = "xpath=//input[@id='confirm_ok']"
CELL_BY_ROW_COL_IDX = lambda row_idx, col_idx: "{0}[{1}]/td[{2}]".\
        format(ALL_RECIPIENTS, row_idx, col_idx)

SEARCH_INPUT = "//input[@name='search_for']"
SEARCH_BUTTON = "//input[@value='Search']"
SEARCH_FOR_COMBO = "//select[@id='arranged_by']"

CANCEL_BUTTON = "//input[@value='Cancel']"


def go_to_page(func):
    @functools.wraps(func)
    def worker(self, list_type, *args, **kwargs):
        menu_item_name = list_type.lower().capitalize()
        available_types = ['Blocklist', 'Safelist']
        if menu_item_name not in available_types:
            raise ValueError('Unknown list type "{0}". Available list types are: {1}'.\
                             format(list_type, available_types))
        self.navigate_to('Options', menu_item_name)

        return func(self, list_type, *args, **kwargs)
    return worker


class SLBLAdmin(GuiCommon):
    """Keywords for interaction with SLBL in SMA quarantines"""

    def get_keyword_names(self):
        return ['slbl_admin_add_recipient',
                'slbl_admin_edit_recipient',
                'slbl_admin_delete_recipient',

                'slbl_admin_is_recipient_exist',
                'slbl_admin_get_recipient',
                'slbl_admin_search']

    def _get_cached_controller(self, cls):
        attr_name = '_{0}'.format(cls.__name__.lower())
        if not hasattr(self, attr_name):
            setattr(self, attr_name, cls(self))
        return getattr(self, attr_name)

    @go_to_page
    def slbl_admin_add_recipient(self, list_type, address, senders):
        """Add new recipient to SLBL

        *Parameters:*
        - `list_type`: Either 'Safelist' or 'Blocklist'
        - `address`: recipient's email
        - `senders`: comma separated or line break separated (\\n)
        list of email addresses

        *Examples:*
        | :FOR | ${list_type} | IN | blocklist | safelist |
        | \ | ${is_recipient_present}= | SLBL Admin Is Recipient Exist |
        | \ | ... | ${list_type} | ${RECIPIENT_ADDRESS} |
        | \ | Run Keyword If | not ${is_recipient_present} |
        | \ | ... | SLBL Admin Add Recipient | ${list_type} |
        | \ | ... | ${RECIPIENT_ADDRESS} |
        | \ | ... | ${list_type}_${SENDER1}, ${list_type}_${SENDER2} |
        """
        #Adding the utf encode to handle IDN characters
        reload(sys)
        sys.setdefaultencoding("utf8")
        address.encode('utf-8')

        self.click_button(ADD_BUTTON)
        controller = self._get_cached_controller(RecipientSettings)
        controller.set({RECIPIENT_ADDRESS[0]: address,
                        SENDER_LIST[0]: senders})
        self._click_submit_button()

    @set_speed(0)
    def _filter_items(self, items_type=None, filter_cond=''):
        if items_type is not None:
            self.select_from_list(SEARCH_FOR_COMBO, items_type)
        self.input_text(SEARCH_INPUT, filter_cond)
        self.click_button(SEARCH_BUTTON)

    @go_to_page
    def slbl_admin_edit_recipient(self, list_type, address, settings):
        """Edit existing recipient to SLBL

        *Parameters:*
        - `list_type`: Either 'Safelist' or 'Blocklist'
        - `address`: existing recipient's email
        - `settings`: dictionary containing the folowing items:
        | Address | new recipient's address |
        | Sender List | comma separated or line break separated (\\n)
        list of email addresses |

        *Exceptions:*
        - `ValueError`: if recipient having  given address does not
        exists

        *Examples:*
        | :FOR | ${list_type} | IN | blocklist | safelist |
        | \ | ${new_settings}= | Create Dictionary |
        | \ | ... | Address | ${RECIPIENT_ADDRESS} |
        | \ | ... | Sender List | ${list_type}_${SENDER1}, ${list_type}_${SENDER2} |
        | \ | SLBL Admin Edit Recipient | ${list_type} |
        | \ | ... | ${RECIPIENT_ADDRESS} | ${new_settings} |
        """
        self._filter_items(filter_cond=address)
        if not self._is_element_present(RECIPIENT_EDIT_BY_ADDRESS(address)):
            raise ValueError('Recipient "{0}" does not exist'.format(address))
        self.click_button(RECIPIENT_EDIT_BY_ADDRESS(address))
        controller = self._get_cached_controller(RecipientSettings)
        controller.set(settings)
        self._click_submit_button()

    @go_to_page
    def slbl_admin_delete_recipient(self, list_type, address):
        """Delete existing recipient from SLBL

        *Parameters:*
        - `list_type`: Either 'Safelist' or 'Blocklist'
        - `address`: existing recipient's email

        *Exceptions:*
        - `ValueError`: if recipient having given address does not
        exists

        *Examples:*
        | :FOR | ${list_type} | IN | blocklist | safelist |
        | \ | SLBL Admin Delete Recipient | ${list_type} | ${RECIPIENT_ADDRESS} |
        | \ | ${is_recipient_present}= | SLBL Admin Is Recipient Exist |
        | \ | ... | ${list_type} | ${RECIPIENT_ADDRESS} |
        | \ | Should Not Be True | ${is_recipient_present} |
        """
        self._filter_items(filter_cond=address)
        if not self._is_element_present(RECIPIENT_DELETE_BY_ADDRESS(address)):
            raise ValueError('Recipient "{0}" does not exist'.format(address))
        self.click_button(RECIPIENT_DELETE_BY_ADDRESS(address),"don't wait")
        self.click_button(RECIPIENT_DELETE_BY_ADDRESS_CONFIRM)

    @go_to_page
    def slbl_admin_is_recipient_exist(self, list_type, address):
        """Check whether given recipient exists in SLBL

        *Parameters:*
        - `list_type`: Either 'Safelist' or 'Blocklist'
        - `address`: recipient's email

        *Return:*
        - Either ${True} or ${False}

        *Examples:*
        | ${is_recipient_present}= | SLBL Admin Is Recipient Exist |
        | ... | ${list_type} | ${RECIPIENT_ADDRESS} |
        | Should Not Be True | ${is_recipient_present} |
        """
        self._filter_items(filter_cond=address)
        return self._is_element_present(RECIPIENT_BY_ADDRESS(address))

    @go_to_page
    def slbl_admin_get_recipient(self, list_type, address):
        """Get info about existing SLBL recipient

        *Parameters:*
        - `list_type`: Either 'Safelist' or 'Blocklist'
        - `address`: recipient's email

        *Exceptions:*
        - `ValueError`: if recipient having given address does not
        exists

        *Return:*
        - Dictionary. See the `settings` parameter description of
        `SLBL Admin Edit Recipient` keyword for more details

        *Examples:*
        | ${recipient_info}= | SLBL Admin Get Recipient |
        | ... | ${list_type} | ${RECIPIENT_ADDRESS} |
        | Log Dictionary | ${recipient_info} |
        """
        self._filter_items(filter_cond=address)
        if not self._is_element_present(RECIPIENT_EDIT_BY_ADDRESS(address)):
            raise ValueError('Recipient "{0}" does not exist'.format(address))
        self.click_button(RECIPIENT_EDIT_BY_ADDRESS(address))
        controller = self._get_cached_controller(RecipientSettings)
        result = controller.get()
        self.click_button(CANCEL_BUTTON)
        return result

    @go_to_page
    @set_speed(0)
    def slbl_admin_search(self, list_type, entry_type, search_criteria):
        """Search existing SLBL recipients

        *Parameters:*
        - `list_type`: Either 'Safelist' or 'Blocklist'
        - `entry_type`: Either 'Recipient' or 'Sender'
        - `search_criteria`: email address or a part of email address

        *Return:*
        - List of dictionaries. See the `settings` parameter description of
        `SLBL Admin Edit Recipient` keyword for more details about list elements.
        An empty list will be returned if no recipients found.

        *Examples:*
        | @{found_recipients}= | SLBL Admin Search | ${list_type} |
        | ... | Recipient | ${RECIPIENT_ADDRESS} |
        | Log List | ${found_recipients} |
        | ${is_address_found}= | Evaluate |
        | ... | bool(filter(lambda x: x['Address'] == '${rcpt_address}', ${found_recipients})) |
        | Should Be True | ${is_address_found} |
        """
        self._filter_items(entry_type, search_criteria)
        recipients_count = int(self.get_matching_xpath_count(ALL_RECIPIENTS))
        result = []
        for recipient_index in xrange(1, 1 + recipients_count):
            recipient_info = {}
            for col_name, col_index in RECIPIENT_COL_MAPPING.iteritems():
                cell_locator = CELL_BY_ROW_COL_IDX(recipient_index,
                                                   col_index).strip()
                cell_value = self.get_text(cell_locator)
                recipient_info[col_name] = cell_value
            result.append(recipient_info)
        return result

#!/usr/bin/env python -tt
#$Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/address_lists.py#1 $
#$DateTime: 2020/01/06 01:25:43 $
#$Author: saurgup5 $

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon

from address_lists_def.address_list_settings import AddressListSettings


ADD_ADDR_LIST_BUTTON = "//input[@value='Add Address List...']"
CONTAINER = "//table[@class='cols']"
EDIT_ADDR_LIST_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                    (CONTAINER, name)
DELETE_ALL_ADDR_LISTS_CHECKBOX = "//input[@id='checkbox_all']"
DELETE_ADDR_LIST_CHECKBOX = lambda name:"//*[@id='%s']" %(name)

DELETE_BUTTON = "//input[@value='Delete']"

PAGE_PATH = ('Mail Policies', 'Address Lists')

class AddressLists(GuiCommon):
    """Keywords for interaction with ESA GUI Mail Policies->
    Address Lists page
    """

    def get_keyword_names(self):
        return ['address_lists_add',
                'address_lists_edit',
                'address_lists_delete']

    def _get_settings_controller(self):
        if not hasattr(self, '_settings_controller'):
            self._settings_controller = AddressListSettings(self)
        return self._settings_controller

    @go_to_page(PAGE_PATH)
    def address_lists_add(self, name, settings):
        """Add new address list

        *Parameters:*
        - `name`: address list name, mandatory
        - `settings`: new address list settings. Dictionary
        which items can be
        | `Description` | description of newly added list |
        | `List Type` | choose either of the options to perform -
        Full Email Addresses only, Domains only, IP Addresses only,
        All of the above (by default) |
        | `Addresses` | list of items in this list, for example:
        user@example.com, user@, @example.com, @.example.com, @[1.2.3.4].
        Mandatory parameter |

        *Examples:*
        | ${list1_settings}= | Create Dictionary |
        | ... | Description | ${ADDRLIST1_NAME} description |
        | ... | List Type | Full Email Addresses only |
        | ... | Addresses | @zone1.${NETWORK}, @zone2.${NETWORK} |
        | Address Lists Add | ${ADDRLIST1_NAME} | ${list1_settings} |
        """
        self.click_button(ADD_ADDR_LIST_BUTTON)
        controller = self._get_settings_controller()
        settings.update({'Name': name})
        controller.set(settings)
        self._click_submit_button(skip_wait_for_title=True)

    @go_to_page(PAGE_PATH)
    def address_lists_edit(self, name, settings={}):
        """Edit address list settings

        *Parameters:*
        - `name`: existing address list name, mandatory
        - `settings`: new address list settings. Dictionary
        which items can be
        | `Name` | new name for the existing list |
        | `Description` | description of the existing list |
        | `Allow only full Email Addresses` | whether to allow
        only full email addresses in the `Addresses` field.
        Either ${True} or ${False}(by default) |
        | `Addresses` | list of items in this list, for example:
        user@example.com, user@, @example.com, @.example.com, @[1.2.3.4].
        Mandatory parameter |

        *Exceptions:*
        - `ValueError`: if address list with given name is not found

        *Examples:*
        | ${list2_settings}= | Create Dictionary |
        | ... | Description | ${ADDRLIST2_NAME} description |
        | ... | Allow only full Email Addresses | ${False} |
        | ... | Addresses | @zone3.${NETWORK} |
        | Address Lists Add | ${ADDRLIST2_NAME} | ${list2_settings} |
        | Set To Dictionary | ${list2_settings} | Addresses | @zone4.${NETWORK} |
        | Address Lists Edit | ${ADDRLIST2_NAME} | ${list2_settings} |
        """
        if not self._is_element_present(EDIT_ADDR_LIST_LINK(name)):
            raise ValueError('There is no Address List named %s' % \
                             (name,))
        self.click_button(EDIT_ADDR_LIST_LINK(name))
        controller = self._get_settings_controller()
        controller.set(settings)
        self._click_submit_button(skip_wait_for_title=True)

    @go_to_page(PAGE_PATH)
    def address_lists_delete(self, name):
        """Delete existing address list

        *Parameters:*
        - `name`: existing address list name or 'all' to delete all
        existing lists, mandatory

        *Exceptions:*
        - `ValueError`: if address list with given name is not found

        *Examples:*
        | Address Lists Delete | ${ADDRLIST1_NAME} |
        | Address Lists Delete | All |
        """
        if name.lower() == 'all':
            dest_locator = DELETE_ALL_ADDR_LISTS_CHECKBOX
        else:
            dest_locator = DELETE_ADDR_LIST_CHECKBOX(name)
        if not self._is_element_present(dest_locator):
            raise ValueError('There is no Address List that satisfies '\
                             '"%s" selector' % (name,))
        self._select_checkbox(dest_locator)
        self.click_button(DELETE_BUTTON, 'don\'t wait')
        self._click_continue_button()

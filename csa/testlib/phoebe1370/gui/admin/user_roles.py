#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/admin/user_roles.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon, Wait
import common.gui.guiexceptions as guiexceptions

from user_roles_def.role_settings import RoleSettings
from user_roles_def.assigning_settings import get_class_by_component_name


ADD_USER_ROLE_BUTTON = 'xpath=//input[@value="Add User Role..."]'
ROLES_TABLE = "//table[@class='cols']"
ROLE_EDIT_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                              (ROLES_TABLE, name)
ROLE_DELETE_LINK = lambda name: "%s//td[normalize-space()='%s']"\
                   "/following-sibling::td[11]/img" % \
                             (ROLES_TABLE, name)
CONFIRM_DIALOG = "//div[@id='confirmation_dialog']"
SUBMIT_BUTTON = "//input[@value='Submit']"


PAGE_PATH = ('System Administration', 'User Roles')


class UserRoles(GuiCommon):
    """Keywords for interaction with ESA GUI System Administration ->
    User Roles page
    """

    def get_keyword_names(self):
        return ['user_roles_add',
                'user_roles_edit',
                'user_roles_delete',

                'user_roles_edit_assigning']

    def _get_role_settings_controller(self):
        if not hasattr(self, '_role_settings_controller'):
            self._role_settings_controller = RoleSettings(self)
        return self._role_settings_controller

    def _confirm_settings(self):
        self.click_button(SUBMIT_BUTTON, 'don\'t wait')
        if self._is_element_present(CONFIRM_DIALOG):
            self._click_continue_button()
        else:
            try:
                self.wait_until_page_loaded(5)
            except Exception as e:
                # Sometimes submit is performed too fast
                # so we ignore this exception and continue normally
                self._debug(str(e))
            self._check_action_result()

    @go_to_page(PAGE_PATH)
    def user_roles_add(self, name, settings={}):
        """Add new user role

        *Parameters:*
        - `name`: name of the user role
        - `settings`: dictionary, whose items are:
        | `Description` | description of the user role |
        | `Mail Policies and Content Filters` | access privileges level for Mail
        Policies and Content Filters. Either "No access",
        "View assigned, edit assigned", "View all, edit assigned",
        "View all, edit all" |
        | `DLP Policies` | access privileges level for DLP Policies. Either
        "No access", "View assigned, edit assigned", "View all, edit assigned",
        "View all, edit all" |
        | `Email Reporting` | access privileges level for Email Reporting.
        Either "No access", "View relevant reports", "View all reports" |
        | `Message Tracking` | access privileges level for Message Tracking.
        Either "No access" or "Message Tracking access" |
        | `Trace` | access privileges level for Trace. Either "No access" or
        "Trace access" |
        | `Quarantines` | access privileges level for Spam quarantine.
        Either "No access" or "Manage assigned quarantines" |
        | `Log Subscription` | access privileges level for log.
        Either "No access" or "Log Subscription Access" |

        *Exceptions:*
        - `ValueError`: if any of passed values is not valid

        *Examples:*
        | ${role_settings}= | Create Dictionary |
        | ... | Description | my description |
        | ... | Mail Policies and Content Filters | View all, edit assigned |
        | ... | DLP Policies | View assigned, edit assigned |
        | ... | Email Reporting | View relevant reports |
        | ... | Message Tracking | Message Tracking access |
        | ... | Trace | Trace access |
        | ... | Quarantines | Manage assigned quarantines |
        | ... | Log Subscription | Log Subscription Access|
        | User Roles Add | my_new_role | ${role_settings} |
        """
        self.click_button(ADD_USER_ROLE_BUTTON)

        controller = self._get_role_settings_controller()
        settings.update({'Name': name})
        controller.set(settings)
        self._confirm_settings()

    @go_to_page(PAGE_PATH)
    def user_roles_edit(self, name, settings={}):
        """Edit edit user role.

        *Parameters:*
        - `name`: name of the existing user role
        - `settings`: dictionary, whose items are:
        | `Name` | new user role name |
        | `Description` | description of the user role |
        | `Mail Policies and Content Filters` | access privileges level for Mail
        Policies and Content Filters. Either "No access",
        "View assigned, edit assigned", "View all, edit assigned",
        "View all, edit all" |
        | `DLP Policies` | access privileges level for DLP Policies. Either
        "No access", "View assigned, edit assigned", "View all, edit assigned",
        "View all, edit all" |
        | `Email Reporting` | access privileges level for Email Reporting.
        Either "No access", "View relevant reports", "View all reports" |
        | `Message Tracking` | access privileges level for Message Tracking.
        Either "No access" or "Message Tracking access" |
        | `Trace` | access privileges level for Trace. Either "No access" or
        "Trace access" |
        | `Quarantines` | access privileges level for Spam quarantine.
        Either "No access" or "Manage assigned quarantines" |

        *Exceptions:*
        - `ValueError`: if any of passed values is not valid or
        if user role with given name does not exist

        *Examples:*
        | ${role_settings}= | Create Dictionary |
        | ... | Name | edited_name |
        | ... | Description | my description |
        | ... | Mail Policies and Content Filters | View all, edit assigned |
        | ... | DLP Policies | View assigned, edit assigned |
        | ... | Email Reporting | View relevant reports |
        | ... | Message Tracking | Message Tracking access |
        | ... | Trace | Trace access |
        | ... | Quarantines | Manage assigned quarantines |
        | User Roles Edit | my_role | ${role_settings} |
        """
        if self._is_element_present(ROLE_EDIT_LINK(name)):
            self.click_button(ROLE_EDIT_LINK(name))
        else:
            raise ValueError('There is no user role named "%s"' % \
                             (name,))

        controller = self._get_role_settings_controller()
        controller.set(settings)
        self._confirm_settings()

    @go_to_page(PAGE_PATH)
    def user_roles_delete(self, name):
        """Delete user role.

        *Parameters:*
        - `name`: name of existing user role to delete.

        *Exceptions:*
        - `ValueError`: in case user role with given name does not exist

        *Examples:*
        | User Roles Delete | my_role |
        """
        if self._is_element_present(ROLE_DELETE_LINK(name)):
            self.click_button(ROLE_DELETE_LINK(name), 'don\'t wait')
        else:
            raise ValueError('There is no user role named "%s"' % \
                             (name,))
        self._click_continue_button()

    @go_to_page(PAGE_PATH)
    def user_roles_edit_assigning(self, role_name, component_name, assigning_map):
        """Assign Content Filters, Mail Policies, DLP Policies, etc. to custom
        roles

        *Parameters:*
        - `role_name`: existing user role name to which components are getting
        to be assigned
        - `component_name`: one of available component names which items will be
        assigned. Can be one of (case insensitive):
        | Incoming Content Filters |
        | Outgoing Content Filters |
        | Incoming Mail Policies |
        | Outgoing Mail Policies |
        | Dlp Policies |
        | Quarantines |
        | Encryption Profiles |
        - `assigning_map`: dictionary containing assigning map for the selected
        component. Keys are item names within the selected component and values
        are either ${True} or ${False} to assign/unassign this item to the
        particular user role

        *Exceptions:*
        - `ValueError`: if there is no user role with given name
        - `ConfigError`: if there is no access to given component in
        given role

        *Examples:*
        | ${incoming_filter_name}= | Set Variable | my-incom-filter |
        | ${drop_action}= | Create Dictionary |
        | ... | Drop (Final Action)  Yeah, drop it |
        | ${actions}= | Content Filter Create Actions |
        | ... | Drop (Final Action) | ${drop_action} |
        | ${conditions}= | Create Dictionary |
        | Content Filter Add | Incoming | ${incoming_filter_name} |
        | ... | Super filter | ${actions} | ${conditions} |
        | ${assigning}= | Create Dictionary |
        | ... | ${incoming_filter_name} | ${True} |
        | User Roles Edit Assigning | ${EXISTING_USER_ROLE_NAME} |
        | ... | Incoming Content Filters | ${assigning} |
        """
        if not self._is_element_present(ROLE_EDIT_LINK(role_name)):
            raise ValueError('There is no user role named "%s"' % (role_name,))
        dest_setter_class = get_class_by_component_name(component_name)
        main_entry_locator = dest_setter_class.get_main_entry_locator(role_name)
        if self._is_element_present(main_entry_locator):
            self.click_button(main_entry_locator)
        else:
            raise guiexceptions.ConfigError('The role "%s" has no access to "%s"'\
                                            % (role_name, component_name))
        dest_setter_class(self).set(assigning_map)
        self._click_submit_button()

# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/management/administration/user_roles.py#1 $  $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

import common.gui.guiexceptions as guiexceptions

from common.gui.guicommon import GuiCommon
from sma.constants import sma_config_masters


config_masters = (
    sma_config_masters.CM91,
    sma_config_masters.CM105,
    sma_config_masters.CM110,
    sma_config_masters.CM115,
    sma_config_masters.CM117,
    sma_config_masters.CM118,
    sma_config_masters.CM120
)

ADD_USER_ROLE_BUTTON = lambda role_type:\
    "//input[@value='Add %s User Role...']" % (role_type.capitalize(),)
ROLE_NAME_TEXTBOX = 'name=name'
ROLE_DESCRIPTION_TEXTBOX = "//table[@class='pairs']//textarea[@name='description']"

# Locators for Web User Role page
VISIBILITY_ON_RADIOBUTTON = 'id=visibility_true'
VISIBILITY_OFF_RADIOBUTTON = 'id=visibility_false'
PUBLISH_ON_RADIOBUTTON = 'id=publishability_true'
PUBLISH_OFF_RADIOBUTTON = 'id=publishability_false'

# Locators for Email User Role page
DISABLE_REPORTING_ACCESS = 'id=reportsnone'
ENABLE_REPORTING_BY_GROUP = 'id=reportsreports_by_group'
ENABLE_REPORTING_BY_GROUP_LIST = 'name=reports_by_group_options'
ENABLE_REPORTING_FROM_APPL = 'id=reportsreports_from_all_appliances'
ENABLE_REPORTING_FROM_APPL_LIST = 'name=reports_from_all_appliances_options'
ENABLE_TRACKING_ACCESS = 'id=trackingunrestricted'
DISABLE_TRACKING_ACCESS = 'id=trackingnone'
ENABLE_QUARANTINE_ACCESS = 'id=quarantinerestricted'
DISABLE_QUARANTINE_ACCESS = 'id=quarantinenone'

EMAIL_ROLES_TABLE = "//div[@class='group']/s[text()='Email Roles']/following"\
    "::table[@class='cols']"
WEB_ROLES_TABLE = "//div[@class='group']/s[text()='Web Roles']/following"\
    "::table[@class='cols']"
USER_ROLE_TABLE_CELL = lambda table, row, column, extrapath='':\
    '%s//tr[%s]/td[%s]%s' % (table, row, column, extrapath)
EDIT_ROLE_LINK = lambda role: 'link=%s' % (role,)
DELETE_ROLE_LINK = lambda table, row: '%s//tr[%s]/td[last()]/img' %\
    (table, row)
DUPLICATE_ROLE_LINK = lambda table, row: '%s//tr[%s]/td[last()-1]/a/img' %\
    (table, row)
CONFIG_MASTERS_ROW = "%s//tr[2]/th[@class='center']" % (WEB_ROLES_TABLE,)
CONFIG_MASTER_NAME = lambda column: '%s//tr[2]/th[%s]' %\
    (WEB_ROLES_TABLE, column)
EDIT_ACCESS_POLICY_LINK = lambda row, column:\
    '%s//tr[%s]/td[%s]/a[1]' % (WEB_ROLES_TABLE, row, column)
EDIT_URL_CATEGORY_LINK = lambda row, column:\
    '%s//tr[%s]/td[%s]/a[2]' % (WEB_ROLES_TABLE, row, column)

# Table locators for 'Access Policies' and 'Custom URL Categories' tables.
TABLE_LOCATOR = "//table[@class='cols']"
TABLE_ENTRY_LOCATOR = "//input[@name='include[]']"
TABLE_ENTRY_NAME_CELL = lambda row: '%s//tr[%s]/td[3]' % (TABLE_LOCATOR, row)
TABLE_CHECKBOX_CELL = lambda row: '%s//tr[%s]/td[1]/input' %\
    (TABLE_LOCATOR, row)

EMAIL_ROLE = 'email'
WEB_ROLE   = 'web'


class UserRoles(GuiCommon):

    """Keywords for Management Appliance -> System Administration -> User
    Roles

    Additional Information:
    1. TODO: link to Configuration Masters constants
    """

    def get_keyword_names(self):
        return ['user_roles_web_role_add',
                'user_roles_email_role_add',
                'user_roles_web_role_edit',
                'user_roles_email_role_edit',
                'user_roles_web_role_delete',
                'user_roles_email_role_delete',
                'user_roles_web_role_duplicate',
                'user_roles_email_role_duplicate',
                'user_roles_access_policies_assign',
                'user_roles_custom_url_categories_assign',
            ]

    def _open_page(self, check_config_masters=False, check_web_table=False,
                   check_email_table=False):
        self._navigate_to('Management', 'System Administration',
                               'User Roles')
        if check_config_masters:
            err_msg = 'All Configuration Masters are currently disabled'
            if self._is_text_present(err_msg):
                raise guiexceptions.GuiFeatureDisabledError(err_msg)

        if check_web_table and not self._is_web_roles_table_present():
            raise guiexceptions.ConfigError('No Web roles have been defined')

        if check_email_table and not self._is_email_roles_table_present():
            raise guiexceptions.ConfigError('No Email roles have been defined')

    def _click_add_user_role_button(self, role_type=WEB_ROLE):
        self.click_button(ADD_USER_ROLE_BUTTON(role_type))

    def _fill_web_user_role_page(self, name, description, visible, publish):
        if name is not None:
            self._fill_role_name_textbox(name)

        if description is not None:
            self._fill_role_description_textbox(description)

        if visible is not None:
            self._click_visibility_radiobutton(visible)

        if publish is not None:
            self._click_publish_radiobutton(publish)

    def _fill_email_user_role_page(self, name, description, reporting_access,
        report_type, tracking_access, quarantine_access):
        if name is not None:
            self._fill_role_name_textbox(name)

        if description is not None:
            self._fill_role_description_textbox(description)

        if reporting_access is not None:
            self._select_reporting_access(reporting_access, report_type)

        if tracking_access is not None:
            self._select_tracking_access(tracking_access)

        if quarantine_access is not None:
            self._select_quarantine_access(quarantine_access)

    def _fill_role_name_textbox(self, name):
        self.input_text(ROLE_NAME_TEXTBOX, name)

    def _fill_role_description_textbox(self, description):
        self.input_text(ROLE_DESCRIPTION_TEXTBOX, description)

    def _click_visibility_radiobutton(self, visibility):
        if visibility:
            self._click_radio_button(VISIBILITY_ON_RADIOBUTTON)
        else:
            self._click_radio_button(VISIBILITY_OFF_RADIOBUTTON)

    def _click_publish_radiobutton(self, publish):
        if publish:
            self._click_radio_button(PUBLISH_ON_RADIOBUTTON)
        else:
            self._click_radio_button(PUBLISH_OFF_RADIOBUTTON)

    def _select_report_type(self, list_locator, report_type):
        if report_type is None:
            return

        available_options = self.get_list_items(list_locator)
        for option in available_options:
            if report_type in option:
                self.select_from_list(list_locator, option)
                break
        else:
            raise guiexceptions.GuiValueError(
                '%s report type was not found' % (report_type,))

    def _select_reporting_access(self, access_type, report_type):
        if not self._is_element_present(DISABLE_REPORTING_ACCESS):
            raise guiexceptions.GuiFeatureDisabledError(\
                'Centralized Email Reporting is disabled')

        if access_type == False or access_type.lower() == 'no access':
            self._click_radio_button(DISABLE_REPORTING_ACCESS)
        elif access_type.lower() == 'group':
            self._click_radio_button(ENABLE_REPORTING_BY_GROUP)
            self._select_report_type(ENABLE_REPORTING_BY_GROUP_LIST,
                report_type)
        elif access_type.lower() == 'appliances':
            self._click_radio_button(ENABLE_REPORTING_FROM_APPL)
            self._select_report_type(ENABLE_REPORTING_FROM_APPL_LIST,
                report_type)
        else:
            raise guiexceptions.GuiValueError(
                'Wrong value for reporting access restriction')

    def _select_tracking_access(self, access):
        if not self._is_element_present(ENABLE_TRACKING_ACCESS):
            raise guiexceptions.GuiFeatureDisabledError(\
                'Centralized Message Tracking is disabled')

        tracking_locators = {
            True: ENABLE_TRACKING_ACCESS,
            False: DISABLE_TRACKING_ACCESS}
        self._click_radio_button(tracking_locators[access])

    def _select_quarantine_access(self, access):
        if not self._is_element_present(ENABLE_QUARANTINE_ACCESS):
            raise guiexceptions.GuiFeatureDisabledError(\
                'Spam Quarantine is disabled')

        quarantine_locators = {
            True: ENABLE_QUARANTINE_ACCESS,
            False: DISABLE_QUARANTINE_ACCESS}
        self._click_radio_button(quarantine_locators[access])

    def _is_email_roles_table_present(self):
        num_of_tables = int(self.get_matching_xpath_count(EMAIL_ROLES_TABLE))
        if num_of_tables == 2:
            return True
        elif num_of_tables == 1 and not self._is_web_roles_table_present():
            return True
        else:
            return False

    def _is_web_roles_table_present(self):
        return self._is_element_present(WEB_ROLES_TABLE)

    def _get_all_roles(self, role_type):
        roles = []
        start_row = 3
        num_of_columns = 6
        table = WEB_ROLES_TABLE
        extraopt = ''

        if role_type == EMAIL_ROLE:
            num_of_columns = 7
            table = EMAIL_ROLES_TABLE
            extraopt = '/img'

        num_of_rows = int(self.get_matching_xpath_count(
            USER_ROLE_TABLE_CELL(table, '*', num_of_columns, extraopt)))
        for row in xrange(start_row, start_row + num_of_rows):
            role_name = self.get_text(USER_ROLE_TABLE_CELL(table, row, 1))
            roles.append(role_name)
        return roles

    def _click_edit_user_role_link(self, name, role_type=WEB_ROLE):
        user_roles = self._get_all_roles(role_type)

        if name not in user_roles:
            raise guiexceptions.GuiValueError('There is no %s %s user role' %\
                             (name, role_type.capitalize()))

        self.click_element(EDIT_ROLE_LINK(name))

    def _click_delete_user_role_link(self, name, role_type):
        user_roles = self._get_all_roles(role_type)
        if role_type == WEB_ROLE:
            table = WEB_ROLES_TABLE
        else:
            table = EMAIL_ROLES_TABLE

        if name not in user_roles:
            raise guiexceptions.GuiValueError('There are no %s %s user role' %\
                (name, role_type.capitalize()))
        self.click_element(DELETE_ROLE_LINK(table, user_roles.index(name) + 3),
            'dont wait')

    def _get_config_master_column_index(self, config_master):
        if config_master not in config_masters:
            raise guiexceptions.GuiValueError(
                'Invalid "%s" value for configuration master' %\
                (config_master,))

        starting_row = 1
        num_of_masters = int(self.get_matching_xpath_count(CONFIG_MASTERS_ROW))
        for index in xrange(starting_row, num_of_masters + 1):
            master_name = self.get_text(CONFIG_MASTER_NAME(index))
            if master_name == config_master:
                return index + 1
        else:
            raise guiexceptions.ConfigError(
                'Config master "%s" is not initialized' % (config_master,))

    def _clear_all_checkboxes(self, locators):
        map(self.unselect_checkbox, locators)

    def _get_location_in_table(self, name, config_master):
        web_roles = self._get_all_roles(WEB_ROLE)
        if name not in web_roles:
            raise guiexceptions.GuiValueError(
                '"%s" user role does not exist' % (name,))

        row = web_roles.index(name) + 3
        column = self._get_config_master_column_index(config_master)
        return (row, column)

    def _click_edit_access_policies_link(self, name, config_master):
        row, column = self._get_location_in_table(name, config_master)
        self.click_element(EDIT_ACCESS_POLICY_LINK(row, column))

    def _click_edit_url_categories_link(self, name, config_master):
        row, column = self._get_location_in_table(name, config_master)
        self.click_element(EDIT_URL_CATEGORY_LINK(row, column))

    def _get_access_policies_dict(self):
        starting_row = 2
        policies = {}
        entries_num = int(self.get_matching_xpath_count(TABLE_ENTRY_LOCATOR))
        for row in xrange(starting_row, entries_num + starting_row):
            name = self.get_text(TABLE_ENTRY_NAME_CELL(row)).split('\n')[0]
            policies[name] = TABLE_CHECKBOX_CELL(row)
        return policies

    def _select_access_policies(self, policies):
        policies_dict = self._get_access_policies_dict()
        policies = self._convert_to_tuple(policies)

        if not policies:
            return

        for policy in policies:
            pol_loc = policies_dict.get(policy)
            if pol_loc is None:
                raise guiexceptions.GuiValueError(
                    '"%s" access policy does not exist' % (policy,))
            self.select_checkbox(pol_loc)

    def _get_url_categories_dict(self):
        starting_row = 2
        categories = {}
        entries_num = int(self.get_matching_xpath_count(TABLE_ENTRY_LOCATOR))
        for row in xrange(starting_row, entries_num + starting_row):
            name = self.get_text(TABLE_ENTRY_NAME_CELL(row))
            categories[name] = TABLE_CHECKBOX_CELL(row)
        return categories

    def _select_url_categories(self, categories):
        err_msg = 'No Custom URL Categories are defined'
        if self._is_text_present(err_msg):
            raise guiexceptions.ConfigError(err_msg)

        categories_dict = self._get_url_categories_dict()
        self._clear_all_checkboxes(categories_dict.values())

        for category in self._convert_to_tuple(categories):
            cat_loc = categories_dict.get(category)
            if cat_loc is None:
                raise guiexceptions.GuiValueError(
                    '"%s" URL category does not exist' % (category,))
            self.select_checkbox(cat_loc)

    def _delete_role(self, name, role_type=WEB_ROLE):
        if role_type == WEB_ROLE:
            self._open_page(check_config_masters=True, check_web_table=True)
        elif role_type == EMAIL_ROLE:
            self._open_page(check_email_table=True)
        else:
            raise ValueError('Wrong "%s" value for role type' % (role_type,))

        self._click_delete_user_role_link(name, role_type)

        self._click_continue_button()

    def _click_duplicate_user_role(self, name, role_type='web'):
        if role_type == WEB_ROLE:
            self._open_page(check_config_masters=True, check_web_table=True)
        elif role_type == EMAIL_ROLE:
            self._open_page(check_email_table=True)
        else:
            raise ValueError('Wrong "%s" value for role type' % (role_type,))

        user_roles = self._get_all_roles(role_type)
        if role_type == WEB_ROLE:
            table = WEB_ROLES_TABLE
        else:
            table = EMAIL_ROLES_TABLE

        if name not in user_roles:
            raise guiexceptions.GuiValueError('There are no %s %s user role' %\
                (name, role_type.capitalize()))

        self.click_element(DUPLICATE_ROLE_LINK(table, user_roles.index(name) + 3),
            'dont wait')

    def user_roles_web_role_add(self, name, description=None, visible=None,
        publish=None):
        """Add new web user role.

        Parameters:
        - `name`: name for the user role.
        - `description`: description for user role.
        - `visible`: visibility of the policies and custom URL categories to
           the user role. Boolean.
        - `publish`: allow the user to publish any Configuration Master.
           Boolean.

        Examples:
        | User Roles Web Role Add | testwebrole |
        | User Roles Web Role Add | webrolename | test role | ${True} |
        | ... | ${False} |

        Exceptions:
        - `GuiFeatureDisabledError`: in case all configuration masters are
           disabled.
        """
        self._open_page(check_config_masters=True)

        self._click_add_user_role_button()

        self._fill_web_user_role_page(name, description, visible, publish)

        self._click_submit_button(accept_confirm_dialog=True)

    def user_roles_email_role_add(self, name, description=None,
        reporting_access=None, report_type=None, tracking_access=None,
        quarantine_access=None):
        """Add new email user role.

        Parameters:
        - `name`: name for the user role.
        - `description`: description for the user role.
        - `reporting_access`: enable access privileges for email reporting.
           Can be one of 'No Access' or ${False} to disable access privileges
           for email reporting. 'Group' or 'Appliances' to enable access by
           reporting group or email appliances correspondingly.
        - `report_type`: name of the report type to grant email reporting
           access privileges to. Applies only if `reporting_access` is positive
           value.
        - `tracking_access`: enable access privileges for message tracking.
           Boolean.
        - `quarantine_access`: enable access privileges for spam quarantine.
           Boolean.


        Examples:
        | User Roles Email Role Add | testrole | brand-new role | Group |
        | ... | All reports | ${True} | ${False} |
        | User Roles Email Role Add | emailrole | reporting_access=${False} |
        | ... | tracking_access=${False} |


        Exceptions:
        - `GuiValueError`: in case of invalid value for `reporting_access`
           or `report_type`.
        - `GuiFeatureDisabledError`: in case any of Email Reporting, Email
           Tracking or Spam Quarantine is disabled when trying to give access
           to it.
        """
        self._open_page()

        self._click_add_user_role_button(EMAIL_ROLE)

        self._fill_email_user_role_page(name, description, reporting_access,
            report_type, tracking_access, quarantine_access)

        self._click_submit_button()

    def user_roles_web_role_edit(self, name, new_name=None, description=None,
        visible=None, publish=None):
        """Edit web user role.

        Parameters:
        - `name`: name of the user role to edit.
        - `new_name`: new name for the user role.
        - `description`: description for the user role.
        - `visible`: visibility of the policies and custom URL categories to
           the user role. Boolean.
        - `publish`: allow the user to publish any Configuration Master.
           Boolean.

        Examples:
        | User Roles Web Role Edit | testwebrole | newrolename |
        | User Roles Web Role Edit | newrolename | visible=${False} |
        | ... | publish=${True} |


        Exceptions:
        - `GuiValueError`: in case user role does not exist.
        - `ConfigError`: in case no user roles were configured.
        - `GuiFeatureDisabledError`: in case all configuration masters are
           disabled.
        """
        self._open_page(check_config_masters=True, check_web_table=True)

        self._click_edit_user_role_link(name)

        self._fill_web_user_role_page(new_name, description, visible, publish)

        self._click_submit_button()

    def user_roles_email_role_edit(self, name, new_name=None, description=None,
        reporting_access=None, report_type=None, tracking_access=None,
        quarantine_access=None):
        """Edit email user role.

        Parameters:
        - `name`: name for the user role.
        - `new_name`: new name for the user role.
        - `description`: description for the user role.
        - `reporting_access`: enable access privileges for email reporting.
           Can be one of 'No Access' or ${False} to disable access privileges
           for email reporting. 'Group' or 'Appliances' to enable access by
           reporting group or email appliances correspondingly.
        - `report_type`: name of the report type to grant email reporting
           access privileges to. Applies only if `reporting_access` is positive
           value.
        - `tracking_access`: enable access privileges for message tracking.
           Boolean.
        - `quarantine_access`: enable access privileges for spam quarantine.
           Boolean.

        Examples:
        | User Roles Email Role Edit | emailrole | newname | Some test role |
        | ... | Appliances | DLP Reports | ${False} | ${True} |
        | User Roles Email Role Edit | emailrole | repoting_access=Group |
        | ... | quarantine_access=${False} |

        Exceptions:
        - `GuiValueError`: in case user role does not exist or in case of
           invalid value for `reporting_access` or `report_type`.
        - `ConfigError`: in case no user roles were configured.
        - `GuiFeatureDisabledError`: in case any of Email Reporting, Email
           Tracking or Spam Quarantine is disabled when trying to give access
           to it.
        """
        self._open_page(check_email_table=True)

        self._click_edit_user_role_link(name, EMAIL_ROLE)

        self._fill_email_user_role_page(new_name, description,
            reporting_access, report_type, tracking_access, quarantine_access)

        self._click_submit_button()

    def user_roles_web_role_duplicate(self, name, new_name=None, description=None,
        visible=None, publish=None):
        """Duplicate web user role.

        Parameters:
        - `name`: name of the user role to duplicate.
        - `new_name`: new name for the user role.
        - `description`: description for the user role.
        - `visible`: visibility of the policies and custom URL categories to
           the user role. Boolean.
        - `publish`: allow the user to publish any Configuration Master.
           Boolean.

        Examples:
        | User Roles Web Role Duplicate | testwebrole | newrolename |
        | ... | publish=${True} |


        Exceptions:
        - `GuiValueError`: in case user role does not exist.
        - `ConfigError`: in case no user roles were configured.
        - `GuiFeatureDisabledError`: in case all configuration masters are
           disabled.
        """
        print '\nuser_roles_web_role_duplicate: name(%s)' % (name)
        self._open_page(check_config_masters=True, check_web_table=True)
        self._click_duplicate_user_role(name)
        self._fill_web_user_role_page(new_name,
            description, visible, publish)
        self._click_submit_button()

    def user_roles_email_role_duplicate(self, name, new_name=None, description=None,
        reporting_access=None, report_type=None, tracking_access=None,
        quarantine_access=None):
        """Duplicate email user role.

        Parameters:
        - `name`: name for the user role.
        - `new_name`: new name for the user role.
        - `description`: description for the user role.
        - `reporting_access`: enable access privileges for email reporting.
           Can be one of 'No Access' or ${False} to disable access privileges
           for email reporting. 'Group' or 'Appliances' to enable access by
           reporting group or email appliances correspondingly.
        - `report_type`: name of the report type to grant email reporting
           access privileges to. Applies only if `reporting_access` is positive
           value.
        - `tracking_access`: enable access privileges for message tracking.
           Boolean.
        - `quarantine_access`: enable access privileges for spam quarantine.
           Boolean.

        Examples:
        | User Roles Email Role Duplicate | emailrole | newname | Some test role |
        | ... | Appliances | DLP Reports | ${False} | ${True} |

        Exceptions:
        - `GuiValueError`: in case user role does not exist or in case of
           invalid value for `reporting_access` or `report_type`.
        - `ConfigError`: in case no user roles were configured.
        - `GuiFeatureDisabledError`: in case any of Email Reporting, Email
           Tracking or Spam Quarantine is disabled when trying to give access
           to it.
        """
        print '\nuser_roles_email_role_duplicate: name(%s)' % (name)

        self._open_page(check_email_table=True)
        self._click_duplicate_user_role(name, role_type=EMAIL_ROLE)

        self._fill_email_user_role_page(new_name, description,
            reporting_access, report_type, tracking_access, quarantine_access)

        self._click_submit_button()

    def user_roles_web_role_delete(self, name):
        """Delete web user role.

        Parameters:
        - `name`: name of the web user role to delete.

        Examples:
        | User Roles Web Role Delete | testrole |

        Exceptions:
        - `GuiValueError`: in case user role does not exist.
        - `ConfigError`: in case no user roles were configured.
        - `GuiFeatureDisabledError`: in case all configuration masters are
           disabled.
        """
        self._delete_role(name)

    def user_roles_email_role_delete(self, name):
        """Delete email user role.

        Parameters:
        - `name`: name of the email user role to delete.

        Examples:
        | User Roles Email Role Delete | testrole |

        Exceptions:
        - `GuiValueError`: in case user role does not exist.
        - `ConfigError`: in case no user roles were configured.
        """
        self._delete_role(name, EMAIL_ROLE)

    def user_roles_access_policies_assign(self, name, config_master, policies):
        """Assign access policies to the web user role.

        Parameters:
        - `name`: name of the web user role to assign policies to.
        - `config_master`: configuration master to edit settings for.
        - `policies`: string of comma-separated values of access policies names
           to include into the role. ${EMPTY} to exclude all assigned policies.

        Examples:
        | User Roles Access Policies Assign | testwebrole |
        | ... | ${sma_config_masters.CM80} | Default Policy, Custom Policy |
        | User Roles Access Policies Assign | testwebrole |
        | ... | ${sma_config_masters.CM77} | ${EMPTY} |
        | User Roles Access Policies Assign | testwebrole |
        | ... | ${sma_config_masters.CM77} | MyAccessPolicy |


        Exceptions:
        - `GuiValueError`: in case of invalid input for the name of the role,
           configuration master name or name of the access policy.
        - `ConfigError`: in case no access policies, user roles were configured
           or configuration master is not available.
        - `GuiFeatureDisabledError`: in case all configuration masters are
           disabled.
        """
        self._open_page(check_config_masters=True, check_web_table=True)

        self._click_edit_access_policies_link(name, config_master)

        self._select_access_policies(policies)

        self._click_submit_button()

    def user_roles_custom_url_categories_assign(self, name, config_master,
        url_categories):
        """Assign custom URL categories to the web user role.

        Parameters:
        - `name`: name of the web user role to assign URL categories to.
        - `config_master`: configuration master name to edit settings for. One
        - `url_categories`: string of comma-separated values of custom URL
           categories names to include into the role. ${EMPTY} to exclude all
           assigned URL categories.

        Examples:
        | User Roles Custom URL Categories Assign | testwebrole |
        | ... | ${sma_config_masters.CM77} | CustomSearchCat |
        | User Roles Custom URL Categories Assign | testwebrole |
        | ... | ${sma_config_masters.CM80} | CustCat1, CustCat2 |
        | User Roles Custom URL Categories Assign | testwebrole |
        | ... | ${sma_config_masters.CM77 | ${EMPTY} |


        Exceptions:
        - `GuiValueError`: in case of invalid input for the name of the role,
           configuration master name or name of the custom URL category.
        - `ConfigError`: in case no custom URL categories, user roles were
           configured or configuration master is not available.
        - `GuiFeatureDisabledError`: in case all configuration masters are
           disabled.
        """
        self._open_page(check_config_masters=True, check_web_table=True)

        self._click_edit_url_categories_link(name, config_master)

        self._select_url_categories(url_categories)

        self._click_submit_button()



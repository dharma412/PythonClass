import re

from common.gui.decorators import go_to_page
from common.gui.guiexceptions import GuiValueError
from common.gui.guicommon import GuiCommon

OIDC_EDIT_SETTINGS_BUTTON = '//input[@value="Edit Settings"]'
OIDC_METADATA_URL = "//input[@id='metadata_url']"
OIDC_ISSUER_URL = "//input[@id='issuer']"
OIDC_AUDIENCE_ADD_ROW_BUTTON = '//input[@id="oidc_audience_domtable_AddRow"]'
OIDC_AUDIENCE = lambda index: "//input[@id='oidc_audience[%s][aud]']" % (index,)
OIDC_CLAIM_FOR_ROLE = "//input[@id='role_claim']"
OIDC_IDENTITY_PROVIDER_ROLE_ADD_ROW_BUTTON = "//input[@id='oidc_role_map_domtable_AddRow']"
OIDC_IDENTITY_PROVIDER_ROLE = lambda index: "//input[@id='oidc_role_map[%s][cust_role]']" % index
OIDC_APPLIANCE_ROLE = lambda index: "//select[@id='oidc_role_map[%s][esa_role]']" % index
OIDC_AUDIENCE_FIELD_REGEX = 'oidc_audience\[(\d+)\]\[aud\]'
OIDC_AUDIENCE_FIELD_XPATH = lambda index: 'oidc_audience[%d][aud]' % index
OIDC_AUDIENCE_DELETE_BUTTON = lambda index: '//tr[@id="oidc_audience_row%s"]/td[2]/img' % index
OIDC_ROLE_MAP_FIELD_REGEX = 'oidc_role_map\[(\d+)\]\[cust_role\]'
OIDC_ROLE_MAP_FIELD_XPATH = lambda index: 'oidc_role_map[%d][cust_role]' % index
OIDC_ROLE_DELETE_BUTTON = lambda index: '//tr[@id="oidc_role_map_row%s"]/td[3]/img' % index

PAGE_PATH = ('System Administration', 'OpenID Connect')


class OidcConfiguration(GuiCommon):
    """
    Keywords for GUI interaction with System Administration -> OIDC Configuration page.
    """

    def get_keyword_names(self):
        return [
            'oidc_configuration_edit_settings'
        ]

    @go_to_page(PAGE_PATH)
    def oidc_configuration_edit_settings(self, settings):
        """
        Keyword to edit OIDC setttings
        :Params
        A dictionary containing below keys -
            `Metadata URL` - string: OIDC Metadata URL 
            `Issuer` - string: OIDC Issuer URL
            `Audience` - list: OIDC Audience URL(s)
                Add prefix add:: if you want to add an audience URL
                Add prefix delete:: if you want to delete an audience URL
            `Claim for Role` - string: OIDC Claim for the role
            `Identity Provider Role to Appliance Role Mappings` -
                dictionary: Key - IDP Role, Value - Appliance Role
                    Add prefix add:: to key if you want to add a OIDC role mapping
                    Add prefix delete:: to key if you want to delete a OIDC role mapping
        
        :Return: None

        :Examples
        ${audience}=  Create List   add::https://u32c01p21-vrouter.cisco.com/
        ${idp_role_to_appliance_role_map}=  Create Dictionary
        ...  add::log_collector  Log Files Access
        ${settings}=  Create Dictionary
        ...  Metadata URL    https://win-qjhp14uq9vv.plugin.com/adfs/.well-known/openid-configuration
        ...  Issuer          http://win-qjhp14uq9vv.plugin.com/adfs/services/trust
        ...  Audience        ${audience}
        ...  Claim for Role  role
        ...  Identity Provider Role to Appliance Role Mappings  ${idp_role_to_appliance_role_map}
        Oidc Configuration Edit Settings  ${settings}

        ${audience}=  Create List
        ...  delete::https://u32c01p21-vrouter.cisco.com/
        ...  add::https://u32c01p21-vrouter.cisco.com/1/
        ...  add::https://u32c01p21-vrouter.cisco.com/2/
        ...  add::https://u32c01p21-vrouter.cisco.com/3/
        ${idp_role_to_appliance_role_map}=  Create Dictionary
        ...  delete::log_collector  Technician
        ...  add::log_collector1  Log Files Access
        ...  add::log_collector2  Administrator
        ...  add::log_collector3  Operator
        ${settings}=  Create Dictionary
        ...  Metadata URL    https://win-qjhp14uq9vv.plugin.com/adfs/.well-known/openid-configuration
        ...  Issuer          http://win-qjhp14uq9vv.plugin.com/adfs/services/trust
        ...  Audience        ${audience}
        ...  Claim for Role  role
        ...  Identity Provider Role to Appliance Role Mappings  ${idp_role_to_appliance_role_map}
        Oidc Configuration Edit Settings  ${settings}
        """
        self.click_button(OIDC_EDIT_SETTINGS_BUTTON)
        if 'Metadata URL' in settings:
            self.input_text(OIDC_METADATA_URL, settings['Metadata URL'])
        if 'Issuer' in settings:
            self.input_text(OIDC_ISSUER_URL, settings['Issuer'])
        if 'Audience' in settings:
            self._edit_audience_settings(settings['Audience'])
        if 'Claim for Role' in settings:
            self.input_text(OIDC_CLAIM_FOR_ROLE, settings['Claim for Role'])
        if 'Identity Provider Role to Appliance Role Mappings' in settings:
            self._edit_oidc_role_mapping(settings['Identity Provider Role to Appliance Role Mappings'])
        self._click_submit_button()

    # Helper methods

    # Method to add or delete audience URLs
    def _edit_audience_settings(self, audiences):
        row_values = self._get_table_row_values(
            OIDC_AUDIENCE_FIELD_REGEX, OIDC_AUDIENCE_FIELD_XPATH)
        self._debug('Existing Audience Settings - %s' % row_values)

        audiences_to_add = filter(lambda x: x, map(lambda url: re.search(
            r'add::(\S+)', url).group(1) if re.search(r'add::(\S+)', url) else None, audiences))
        self._debug('Audiences to add - %s' % audiences_to_add)
        if audiences_to_add:
            if row_values and row_values[0]:
                for index in range(len(audiences_to_add)):
                    self.click_button(
                        OIDC_AUDIENCE_ADD_ROW_BUTTON, "don't row")
                    self.input_text(OIDC_AUDIENCE(index + len(row_values)),
                                    audiences_to_add[index].replace('add::', ''))
            else:
                if len(audiences_to_add) > 1:
                    for index in range(len(audiences_to_add)):
                        self.input_text(OIDC_AUDIENCE(index),
                                        audiences_to_add[index].replace('add::', ''))
                        if index != len(audiences) - 1:
                            self.click_button(
                                OIDC_AUDIENCE_ADD_ROW_BUTTON, "don't row")
                else:
                    self.input_text(OIDC_AUDIENCE(
                        0), audiences_to_add[0].replace('add::', ''))

        audiences_to_delete = filter(lambda x: x, map(lambda url: re.search(
            r'delete::(\S+)', url).group(1) if re.search(r'delete::(\S+)', url) else None, audiences))
        self._debug('Audiences to delete - %s' % audiences_to_delete)
        if audiences_to_delete:
            for audience in audiences_to_delete:
                if audience not in row_values:
                    GuiValueError(
                        'OIDC audience with name %s not found ' % audience)
                for index, row_value in enumerate(row_values):
                    if audience == row_value:
                        self._info('Deleting "%s"' % audience)
                        self.click_button(
                            OIDC_AUDIENCE_DELETE_BUTTON(index), "don't wait")
                        self._info("Deleted '%s'" % audience)

    # Method to add or delete OIDC role mapping
    def _edit_oidc_role_mapping(self, idp_role_to_appliance_role_map):
        row_values = self._get_table_row_values(
            OIDC_ROLE_MAP_FIELD_REGEX, OIDC_ROLE_MAP_FIELD_XPATH)
        self._debug('Existing OIDC Role mappings - %s' % row_values)
        
        roles_to_add = filter(lambda x: x, map(lambda role: role if re.search(r'add::\S+', role) else None, idp_role_to_appliance_role_map.keys()))
        self._debug('Roles to add - %s' % roles_to_add)
        if roles_to_add:
            if row_values and row_values[0]:
                for index in range(len(roles_to_add)):
                    self.click_button(
                        OIDC_IDENTITY_PROVIDER_ROLE_ADD_ROW_BUTTON, "don't row")
                    idp_role = roles_to_add[index].replace('add::', '')
                    appliance_role = idp_role_to_appliance_role_map[roles_to_add[index]]

                    self.input_text(
                        OIDC_IDENTITY_PROVIDER_ROLE(index + len(row_values)), idp_role)
                    self.select_from_list(
                        OIDC_APPLIANCE_ROLE(index + len(row_values)), appliance_role)
            else:
                if len(idp_role_to_appliance_role_map.keys()) > 1:
                    for index in range(len(roles_to_add)):
                        idp_role = roles_to_add[index].replace('add::', '')
                        appliance_role = idp_role_to_appliance_role_map[roles_to_add[index]]
                        self.input_text(
                            OIDC_IDENTITY_PROVIDER_ROLE(index), idp_role)
                        self.select_from_list(
                            OIDC_APPLIANCE_ROLE(index), appliance_role)
                        if index != len(roles_to_add) - 1:
                            self.click_button(
                                OIDC_IDENTITY_PROVIDER_ROLE_ADD_ROW_BUTTON, "don't row")
                else:
                    self.input_text(OIDC_IDENTITY_PROVIDER_ROLE(
                        0), roles_to_add[0].replace('add::', ''))
                    self.select_from_list(OIDC_APPLIANCE_ROLE(
                        0), idp_role_to_appliance_role_map[roles_to_add[0]])

        roles_to_delete = filter(lambda x: x, map(lambda role: re.search(
            r'delete::(\S+)', role).group(1) if re.search(r'delete::(\S+)', role) else None, idp_role_to_appliance_role_map.keys()))
        self._debug('Roles to delete - %s' % roles_to_delete)
        if roles_to_delete:
            for role in roles_to_delete:
                if role not in row_values:
                    GuiValueError('OIDC role with name %s not found ' % role)
                for index, row_value in enumerate(row_values):
                    if role == row_value:
                        self._info('Deleting "%s"' % role)
                        self.click_button(
                            OIDC_ROLE_DELETE_BUTTON(index), "don't wait")
                        self._info("Deleted '%s'" % role)
    
    def _get_table_row_values(self, row_regex, table_regex):
        val_list = []
        row_pattern = re.compile(row_regex)
        text_fields = self._get_all_fields()
        for field in text_fields:
            result = row_pattern.search(field)
            if result:
                value = self.get_value(table_regex(int(result.group(1))))
                val_list.append(value)

        return val_list


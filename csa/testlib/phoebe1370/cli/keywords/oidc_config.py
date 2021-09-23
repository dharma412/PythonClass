from common.cli.clicommon import CliKeywordBase

class OidcConfig(CliKeywordBase):
    """
    CLI command: oidcconfig
    """

    def get_keyword_names(self):
        return [
            'oidc_config_setup_config',
            'oidc_config_edit_config',
            'oidc_config_delete_config',
            'oidc_config_setup_mapping_new',
            'oidc_config_setup_mapping_edit',
            'oidc_config_setup_mapping_delete',
            'oidc_config_setup_mapping_print'
        ]

    def oidc_config_setup_config(self, *args):
        """
        CLI keyword for configuring OIDC settings.

        *Params*:
        - `metadata_url`: <String> The metadata URL is used to fetch the OpenID Connect configuration
                                   metadata. The metadata is used to validate the access token.
        - `issuer`: <String> The value must match the issuer claim value of the access token when
                             validating the access token.
        - `role`: <String> The value is used to retrieve the role information from the access token.
        - `audience`: <String> Value for "audience". Use a comma to separate multiple values.
        - `create_group_mappings`: <String> Option to create external group mappings.
                                            Pass Yes to create and No to skip.
        - `role_mappings`: <Dictionary> Key value pair of 'Group Name' and 'Role'.
                                        Group names are case-sensitive.
        
        *Returns*:
        - None

        *Example*:
        | ${role_mapping}= | Create Dictionary                                  |
        | ... | logs_admin | Administrators                                     |
        | ... | logs_guest | Guests                                             |
        | Oidc Config Setup Config                                              |
        | ... | metadata_url=https://WIN-BL0P4116VDB.onpremesa.com/adfs         |
        | ... | issuer=http://WIN-BL0P4116VDB.onpremesa.com/adfs/services/trust |
        | ... | role=role                                                       |
        | ... | audience=https://u32c01p21-vrouter.cisco.com                    |
        | ... | create_group_mappings=Y                                         |
        | ... | role_mappings=${role_mapping}                                   |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.oidcconfig().setup(**kwargs)

    def oidc_config_edit_config(self, *args):
        """
        CLI keyword for editing OIDC settings.

        *Params*:
        - `metadata_url`: <String> The metadata URL is used to fetch the OpenID Connect configuration
                                   metadata. The metadata is used to validate the access token.
        - `issuer`: <String> The value must match the issuer claim value of the access token when
                             validating the access token.
        - `role`: <String> The value is used to retrieve the role information from the access token.
        - `audience`: <String> Value for "audience". Use a comma to separate multiple values.
        - `create_group_mappings`: <String> Option to create external group mappings.
                                            Pass Yes to create and No to skip.
        - `role_mappings`: <Dictionary> Key value pair of 'Group Name' and 'Role'.
                                        Group names are case-sensitive.
        
        *Returns*:
        - None

        *Example*:
        | ${role_mapping}=  | Create Dictionary                                 |
        | ... | logs_admin2 | Administrators                                    |
        | ... | logs_guest2 | Help Desk Users                                   |
        | Oidc Config Edit Config                                               |
        | ... | metadata_url=https://WIN-BL0P4116VDB.onpremesa.com/adfs/openid  |
        | ... | issuer=http://WIN-BL0P4116VDB.onpremesa.com/adfs/trust          |
        | ... | role=New Role                                                   |
        | ... | audience=https://u32c01p19-vrouter.cisco.com                    |
        | ... | create_group_mappings=Y                                         |
        | ... | role_mappings=${role_mapping}                                   |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.oidcconfig().edit(**kwargs)

    def oidc_config_delete_config(self, **args):
        """
        CLI keyword for deleting OIDC settings.

        *Params*:
        - None
        
        *Returns*:
        - None

        *Example*:
        | Oidc Config Delete Config |
        """
        return self._cli.oidcconfig().delete(**args)

    def oidc_config_setup_mapping_new(self, *args):
        """
        CLI keyword for adding new role map in OIDC settings.

        *Params*:
        - `role_mappings`: <Dictionary> Key value pair of 'Group Name' and 'Role'.
                                        Group names are case-sensitive.
        
        *Returns*:
        - None

        *Example*:
        | ${role_mapping}=              | Create Dictionary             |
        | ... | logs_admin3             | Guests                        |
        | ... | logs_guest3             | Technicians                   |
        | Oidc Config Setup Mapping New | role_mappings=${role_mapping} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.oidcconfig().mapping_new(**kwargs)

    def oidc_config_setup_mapping_edit(self, *args):
        """
        CLI keyword for editing role map in OIDC settings.

        *Params*:
        - `role_mappings`: <Dictionary> Key value pair of 'Group Name' and 'Role'.
                                        Group names are case-sensitive.
        
        *Returns*:
        - None

        *Example*:
        | ${role_mapping}=               | Create Dictionary             |
        | ... | logs_guest3              | Read-Only Operators           |
        | Oidc Config Setup Mapping Edit | role_mappings=${role_mapping} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.oidcconfig().mapping_edit(**kwargs)

    def oidc_config_setup_mapping_delete(self, *args):
        """
        CLI keyword for deleting role map in OIDC settings.

        *Params*:
        - `role_mappings`: <List> List of group names to be deleted.
        
        *Returns*:
        - None

        *Example*:
        | ${role_mapping}=                 | Create List                   |
        | ... | logs_admin2                | logs_guest3                   |
        | Oidc Config Setup Mapping Delete | role_mappings=${role_mapping} |
        """
        kwargs=self._convert_to_dict(args)
        self._cli.oidcconfig().mapping_delete(**kwargs)

    def oidc_config_setup_mapping_print(self):
        """
        CLI keyword for printing/getting role map in OIDC settings.

        *Params*:
        - None
        
        *Returns*:
            List of of role maps.
            ['1. logs_admin -> Administrators', '2. logs_guest -> Guests']

        *Example*:
        | ${role_mappings}= | Oidc Config Setup Mapping Delete |
        | Log Many          | ${role_mapping}                  |
        """
        return self._cli.oidcconfig().mapping_print()

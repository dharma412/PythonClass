#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/devops_external_auth_config.py#1 $
# $DateTime: 2020/05/25 00:19:30 $
# $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase
from sal.containers.yesnodefault import YES, NO, is_yes

class DevopsExternalAuthConfig(CliKeywordBase):
    """ SARF keywords class to configure SAML for devops user"""

    def get_keyword_names(self):
        return ['devops_external_auth_config_new',
                'devops_external_auth_config_edit_sp',
                'devops_external_auth_config_edit_idp',
                'devops_external_auth_config_delete',
                ]

    def devops_external_auth_config_new(self, *args):
        """Keyword to configure SAML SP (Service Provider) and
        IDP profiles (Identity Provider).

        devopsexternalauthconfig -> SAML -> NEW

        Parameters:
        - `sp_profile_name`: Provide the SP profile Name.
        - `sp_entity_id`: Provide the SP Entity Id.
        - `assertion_consumer_url`: Assertion consumer URL
        - `sp_certificate`: Provide the SP Certificate.
        - `sp_certificate_key`: Provide the key for SP Certificate.
        - `sp_certificate_passphrase`: Provide the password for SP Certificate.
        - `sp_sign_request`: Do you want to Sign Requests. Allowed values: 0 | 1
        - `sp_sign_assertion_request`: Do you want to Sign Assertion Requests.
            Allowed values: 0 | 1
        - `sp_technical_contact_id`: SP technical contact id.
        - `sp_organization_url`: URL of the Organization.
        - `sp_organization_name`: Name of the Organization.
        - `sp_organization_display_name`: Display name of the Organization.
        - `idp_profile_name`: Provide the IDP Profile Name.
        - `idp_metadata_action`: Provide the action to configure IDP metadata.
            Allowed values are: ENTER | PASTE.
        Following three parameters are valid only when *idp_metadata_action*
        is set to ENTER.
        - `idp_entity_id`: Provide the IDP Id.
        - `idp_sso_url`: Provide the IDP SSO URL.
        - `idp_certificate`: Provide the certificate for IDP.
        Below parameter is valid only when *idp_metadata_action* is set to PASTE.
        - `idp_metadata_xml`: Provide the XML content of IDP metadata.

        Examples:
        | Devops External Auth Config New                                   |
        | ... | sp_profile_name=${sp_profile_name}                          |
        | ... | sp_entity_id=${sp_entity_id}                                |
        | ... | assertion_consumer_url=${acs_url}                           |
        | ... | sp_certificate=${sp_certificate}                            |
        | ... | sp_certificate_key=${sp_certificate_key}                    |
        | ... | sp_certificate_passphrase=${sp_certificate_passphrase}      |
        | ... | sp_sign_request=1                                           |
        | ... | sp_sign_assertion_request=1                                 |
        | ... | sp_technical_contact_id=${technical_contact_id}             |
        | ... | sp_organization_url=${organization_url}                     |
        | ... | sp_organization_name=${organization_name}                   |
        | ... | sp_organization_display_name=${organization_display_name}   |
        | ... | idp_profile_name=${idp_profile_name}                        |
        | ... | idp_metadata_action=paste                                   |
        | ... | idp_metadata_xml=${idp_metadata_xml}                        |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.devopsexternalauthconfig().new(**kwargs)

    def devops_external_auth_config_edit_sp(self, *args):
        """Keyword to edit SP settings.

        devopsexternalauthconfig -> SAML -> EDIT -> SP

        Parameters:
        - `sp_profile_name`: Provide the SP profile Name.
        - `sp_entity_id`: Provide the SP Entity Id.
        - `sp_certificate_edit_option`: Edit action for SP certificate.
            Allowed values are: USE | REPLACE
        - `sp_certificate`: Provide the SP Certificate.
        - `sp_certificate_key`: Provide the key for SP Certificate.
        - `sp_certificate_passphrase`: Provide the password for SP Certificate.
        - `sp_sign_request`: Do you want to Sign Requests. Allowed values: 0 | 1
        - `sp_sign_assertion_request`: Do you want to Sign Assertion Requests.
            Allowed values: 0 | 1
        - `sp_technical_contact_id`: SP technical contact id.
        - `sp_organization_url`: URL of the Organization.
        - `sp_organization_name`: Name of the Organization.
        - `sp_organization_display_name`: Display name of the Organization.

        Examples:
        | Devops External Auth Config Edit Sp                                       |
        | ...  | sp_profile_name=${new_sp_profile_name}                             |
        | ...  | sp_entity_id=${new_sp_entity_id}                                   |
        | ...  | sp_certificate_edit_option=Replace                                 |
        | ...  | sp_certificate=${new_sp_certificate}                               |
        | ...  | sp_certificate_key=${new_sp_certificate_key}                       |
        | ...  | sp_certificate_passphrase=${new_sp_certificate_passphrase}         |
        | ...  | sign_request=0                                                     |
        | ...  | sign_assertion_request=0                                           |
        | ...  | sp_technical_contact_id=${new_sp_technical_contact_id}             |
        | ...  | sp_organization_url=${new_sp_organization_url}                     |
        | ...  | sp_organization_name=${new_sp_organization_name}                   |
        | ...  | sp_organization_display_name=${new_sp_organization_display_name}   |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.devopsexternalauthconfig().edit_sp(**kwargs)

    def devops_external_auth_config_edit_idp(self, *args):
        """Keyword to edit IDP settings.

        devopsexternalauthconfig -> SAML -> EDIT -> IDP

        Parameters:
        - `idp_metadata_edit_action`: Edit action for IDP metadata.
            Allowed values are: PASTE | ENTER.
        Below three parameters are valid only when *idp_metadata_edit_action*
        is set to ENTER.
        - `idp_entity_id`: Provide the IDP entity id.
        - `idp_sso_url`: Provide the IDP IDP SSO URL.
        - `idp_certificate`: Provide the IDP certificate.
        Below parameter is valid only when *idp_metadata_edit_action* is set to PASTE.
        - `idp_metadata_xml`: Provide the XML metadata of IDP.

        Examples:
        | Devops External Auth Config Edit Idp              |
        | ... | idp_metadata_edit_action=Enter              |
        | ... | idp_entity_id=${new_idp_entity_id}          |
        | ... | idp_sso_url=${new_idp_sso_url}              |
        | ... | idp_certificate=${new_idp_certificate}      |

        | Devops External Auth Config Edit Idp              |
        | ... | idp_metadata_edit_action=Pase               |
        | ... | idp_metadata_xml=${new_idp_metadata_xml}    |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.devopsexternalauthconfig().edit_idp(**kwargs)

    def devops_external_auth_config_delete(self):
        """Keyword to delete SP/IDP settings.

        devopsexternalauthconfig -> SAML -> DELETE

        Parameters: None

        Examples:
        | Devops External Auth Config Delete |
        """
        self._cli.devopsexternalauthconfig().delete()

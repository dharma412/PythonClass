#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/saml_config.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase
from sal.containers.yesnodefault import YES, NO, is_yes

class SamlConfig(CliKeywordBase):
    """ SARF keywords class to configure SAML """

    def get_keyword_names(self):
        return ['saml_config_new',
                'saml_config_edit_sp',
                'saml_config_edit_idp',
                'saml_config_delete',
                ]

    def saml_config_new(self, *args):
        """Keyword to configure SAML SP (Service Provider) and
        IDP profiles (Identity Provider).

        samlconfig -> UILOGIN -> NEW

        Parameters:
        - `sp_profile_name`: Provide the SP profile Name.
        - `sp_entity_id`: Provide the SP Entity Id.
        - `assertion_consumer_url` : Assertion consumer URL
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
        | Saml Config New                                                   |
        | ... | sp_profile_name=${sp_profile_name}                          |
        | ... | sp_entity_id=${sp_entity_id}                                |
        | ... | assertion_consumer_url=${New_consumer_url}                  |
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
        self._cli.samlconfig().new(**kwargs)

    def saml_config_edit_sp(self, *args):
        """Keyword to edit SP settings.

        samlconfig -> UILOGIN -> EDIT -> SP

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
        | Saml Config Edit Sp                                                       |
        | ...  | sp_profile_name=${new_sp_profile_name}                             |
        | ...  | sp_entity_id=${new_sp_entity_id}                                   |
        | ...  | sp_certificate_edit_action=Replace                                 |
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
        self._cli.samlconfig().edit_sp(**kwargs)

    def saml_config_edit_idp(self, *args):
        """Keyword to edit IDP settings.

        samlconfig -> UILOGIN -> EDIT -> IDP

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
        | Saml Config Edit Idp                              |
        | ... | idp_metadata_edit_action=Enter              |
        | ... | idp_entity_id=${new_idp_entity_id}          |
        | ... | idp_sso_url=${new_idp_sso_url}              |
        | ... | idp_certificate=${new_idp_certificate}      |

        | Saml Config Edit Idp                              |
        | ... | idp_metadata_edit_action=Pase               |
        | ... | idp_metadata_xml=${new_idp_metadata_xml}    |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.samlconfig().edit_idp(**kwargs)

    def saml_config_delete(self):
        """Keyword to delete SP/IDP settings.

        samlconfig -> UILOGIN -> DELETE

        Parameters: None

        Examples:
        | Saml Config Delete |
        """
        self._cli.samlconfig().delete()

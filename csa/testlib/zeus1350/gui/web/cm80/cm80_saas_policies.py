#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm80/cm80_saas_policies.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from coeus80.gui.manager.saas_policies import SaasPolicies


class Cm80SaasPolicies(SaasPolicies):
    """
    Keywords library for WebUI page Web -> Configuration Master 8.0 -> SaaS Policies
    """

    def _open_page(self):
        self._navigate_to('Web', 'Configuration Master 8.0', 'SaaS Policies')

    def get_keyword_names(self):
        return [
            'cm80_saas_policies_enable_saas_application',
            'cm80_saas_policies_disable_saas_application',
            'cm80_saas_policies_add_saas_application',
            'cm80_saas_policies_edit_saas_application',
            'cm80_saas_policies_delete_saas_application',
        ]

    def cm80_saas_policies_enable_saas_application(self, name):
        """
        Enable SaaS Application Authentication Policy from Configuration Master 8.0

        Use this method to enable previously disabled SaaS Application
        Authentication Policy.

        *Parameters*
        - `name`: The name of SaaS Application Authentication Policy to be
        enabled. String. Mandatory.

        *Exceptions*
        - GuiControlNotFoundError:xxx

        *Examples*
        | CM80 Saas Policies Enable Application | myAppName |
        """
        self.saas_policies_enable_saas_application(name)

    def cm80_saas_policies_disable_saas_application(self, name):
        """Disable SaaS Application Authentication Policy  from Configuration Master 8.0

        Use this method to disable SaaS Application Authentication Policy.

        *Parameters*
        - `name`: The name of SaaS Application Authentication Policy to be
        disabled. String. Mandatory.

        *Examples*
        | CM80 Saas Policies Disable Application | myAppName |
        """
        self.saas_policies_disable_saas_application(name)

    def cm80_saas_policies_add_saas_application(self,
                                                name,
                                                sp_metadata,
                                                description=None,
                                                auth_realm=None,
                                                saas_sso_authentication_prompt=None,
                                                saml_username_mapping=None,
                                                saml_attribute_mapping=None,
                                                authentication_context=None
                                                ):
        """Add SaaS Application policy from Configuration Master 8.0

        Use this method to create a SaaS Application Authentication Policy.

        *Parameters*
        - `name`: name to identify the SaaS application for this
        policy group. String. Mandatory.
        - `sp_metadata`: metadata that describes the service provider referenced
        in this policy group. List. Should contain 1 or 3 elements. 1 element if
        you want to upload a metadata file provided by the SaaS application. In
        This case list element represents path to metadata file. Otherwise 3
        elements of the list contain the following values:
        _Service Provider Entity ID_ - (typically string in URI format) the SaaS
        application uses to identify itself as a service provider.
        _Name ID Format_ - format the appliance should use to identify users in
        the SAML assertion it sends to service providers. Possible values:
        'X509SubjectName', 'Kerberos', 'Unspecified', 'Entity', 'Transient',
        'EmailAddress', 'WindowsDomainNameQualifiedName'.
        Default value: 'X509SubjectName'.
        _Assertion Consumer Service Location_ - string that contains URL to
        where the Web Security appliance should send the SAML assertion it
        creates.
        - `description`: description for this SaaS application. String. Optional.
        - `auth_realm`: contains authentication realm or authentication
        sequence the Web Proxy should use to authenticate users
        accessing this SaaS application. String. Optional. Default value:
        `All Realms`.
        - `saas_sso_authentication_prompt`: choose whether to allow users to
        transparently sign into the SaaS application using their local
        authentication credentials, or to always prompt users for their
        credentials when accessing the SaaS application. String.
        Either `Prompt` or 'Transparently' or 'Automatically'. First value used by default.
        - `saml_username_mapping`: Specify how the Web Proxy should represent user
        names to the service provider in the SAML assertion. List with 2
        elements. First element represents one of methods:  'No mapping',
        'LDAP query', 'Fixed Rule mapping'. Second element used when method is
        'LDAP query' or 'Fixed Rule mapping'. It represents expression used
        with selected method.
        - `saml_attribute_mapping`: information about the internal users from the
        LDAP authentication server if required by the SaaS application. List
        with strings that contain pairs of values separated by semicolon. (LDAP
        attribute mapped to a SAML attribute). Optional.
        - `authentication_context`: contains one of values:
        'SecureRemotePassword', 'InternetProtocolPassword',
        'AuthenticatedTelephony', 'Unspecified', 'PreviousSession',
        'MobileTwoFactorUnregistered', 'MobileTwoFactorContract', 'Kerberos',
        'Public Key - XMLDSig', 'MobileOneFactorContract', 'Public Key - X.509',
        'MobileOneFactorUnregistered', 'TLSClient', 'Automatic', 'SoftwarePKI',
        'PasswordProtectedTransport', 'Public Key - SPKI', 'Password',
        'Smartcard', 'PersonalTelephony', 'InternetProtocol', 'Telephony',
        'Public Key - PGP', 'SmartcardPKI', 'NomadTelephony', 'TimeSyncToken'.
        Default: 'Automatic'.

        *Exceptions*
        - ConfigError: In order to add or edit SaaS applications, you must create at least one authentication realm
        - ConfigError: SaaS SSO Authentication Prompt settings error
        - ConfigError: Service Provider Name ID Format Error
        - ConfigError: Service Provider Metadata Format Error
        - ConfigError: Expression Name is missing in SAML Username Mapping
        - ConfigError: Authentication Context option error'
        - ValueError: Invalid argument. Please use semicolon separated string

        *Examples*
        | @{METADATA} | test.com | Entity | https://host.com |
        | @{SAML_USERNAME_MAPPING} | Fixed Rule mapping | %s@example.com |
        | @{SAML_ATTR_MAPPING} | saml: ldap |
        | CM80 Saas Policies Add Saas Application | myAppPolicy |
        | ... | ${METADATA} |
        | ... | description=test saas app |
        | ... | auth_realm=test |
        | ... | saas_sso_authentication_prompt=Transparently sign in SaaS users |
        | ... | saml_username_mapping=${SAML_USERNAME_MAPPING} |
        | ... | saml_attribute_mapping=${SAML_ATTR_MAPPING} |
        | ... | authentication_context=TimeSyncToken |
        | CM80 Saas Policies Add Saas Application | zero | ${METADATA} |
        | ... | test policy |
        """
        self.saas_policies_add_saas_application(
            name,
            sp_metadata,
            description=description,
            auth_realm=auth_realm,
            saas_sso_authentication_prompt=saas_sso_authentication_prompt,
            saml_username_mapping=saml_username_mapping,
            saml_attribute_mapping=saml_attribute_mapping,
            authentication_context=authentication_context
        )

    def cm80_saas_policies_edit_saas_application(self,
                                                 name,
                                                 sp_metadata,
                                                 description=None,
                                                 auth_realm=None,
                                                 saas_sso_authentication_prompt=None,
                                                 saml_username_mapping=None,
                                                 saml_attribute_mapping=None,
                                                 authentication_context=None
                                                 ):
        """Edit SaaS Application from Configuration Master 8.0

        Use this method to edit a SaaS Application Authentication Policy.

        *Parameters*
        - `name`: name to identify the SaaS application. String. Mandatory.
        - `sp_metadata`: metadata that describes the service provider referenced
        in this policy group. List. Should contain 1 or 3 elements. 1 element if
        you want to upload a metadata file provided by the SaaS application. In
        This case list element represents path to metadata file. Otherwise 3
        elements of the list contain the following values:
        _Service Provider Entity ID_ - (typically string in URI format) the SaaS
        application uses to identify itself as a service provider.
        _Name ID Format_ - format the appliance should use to identify users in
        the SAML assertion it sends to service providers. Possible values:
        'X509SubjectName', 'Kerberos', 'Unspecified', 'Entity', 'Transient',
        'EmailAddress', 'WindowsDomainNameQualifiedName'.
        _Assertion Consumer Service Location_ - string that contains URL to
        where the Web Security appliance should send the SAML assertion it
        creates.
        - `description`: description for this SaaS application. String.
        - `auth_realm`: contains authentication realm or authentication
        sequence the Web Proxy should use to authenticate users
        accessing this SaaS application. String. Optional.
        - `saas_sso_authentication_prompt`: choose whether to allow users to
        transparently sign into the SaaS application using their local
        authentication credentials, or to always prompt users for their
        credentials when accessing the SaaS application. String.
        Either `Prompt` or 'Transparently' or 'Automatically'.
        - `saml_username_mapping`: Specify how the Web Proxy should represent user
        names to the service provider in the SAML assertion. List with 2
        elements. First element represents one of methods:  'No mapping',
        'LDAP query', 'Fixed Rule mapping'. Second element used when method is
        'LDAP query' or 'Fixed Rule mapping'. It represents expression used
        with selected method.
        - `saml_attribute_mapping`: information about the internal users from the
        LDAP authentication server if required by the SaaS application. List
        with strings that contain pairs of values separated by semicolon. (LDAP
        attribute mapped to a SAML attribute). Optional.
        - `authentication_context`: contains one of values:
        'SecureRemotePassword', 'InternetProtocolPassword',
        'AuthenticatedTelephony', 'Unspecified', 'PreviousSession',
        'MobileTwoFactorUnregistered', 'MobileTwoFactorContract', 'Kerberos',
        'Public Key - XMLDSig', 'MobileOneFactorContract', 'Public Key - X.509',
        'MobileOneFactorUnregistered', 'TLSClient', 'Automatic', 'SoftwarePKI',
        'PasswordProtectedTransport', 'Public Key - SPKI', 'Password',
        'Smartcard', 'PersonalTelephony', 'InternetProtocol', 'Telephony',
        'Public Key - PGP', 'SmartcardPKI', 'NomadTelephony', 'TimeSyncToken'.

        *Exceptions*
        - ConfigError: In order to add or edit SaaS applications, you must create at least one authentication realm
        - ConfigError: SaaS SSO Authentication Prompt settings error
        - ConfigError: Service Provider Name ID Format Error
        - ConfigError: Service Provider Metadata Format Error
        - ConfigError: Expression Name is missing in SAML Username Mapping
        - ConfigError: Authentication Context option error'
        - ValueError: Invalid argument. Please use semicolon separated string

        Example:
        | @{ALT_METADATA} | %{SARF_HOME}/variables/sp_metadata.xml |
        | @{ALT_SAML_USERNAME_MAPPING} | LDAP query | <user>@<domain>.com. |
        | @{ALT_SAML_ATTR_MAPPING} | aaa: bbb | ccc: ddd |


        | CM80 Saas Policies Edit Saas Application | myAppPolicy |
        | ... | ${ALT_METADATA} |
        | ... | description=test saas app |
        | ... | auth_realm=test |
        | ... | saas_sso_authentication_prompt=Transparently sign in SaaS users |
        | ... | saml_username_mapping=${ALT_SAML_USERNAME_MAPPING} |
        | ... | saml_attribute_mapping=${ALT_SAML_ATTR_MAPPING} |
        | ... | authentication_context=TimeSyncToken |
        """
        self.saas_policies_edit_saas_application(
            name,
            sp_metadata,
            description=description,
            auth_realm=auth_realm,
            saas_sso_authentication_prompt=saas_sso_authentication_prompt,
            saml_username_mapping=saml_username_mapping,
            saml_attribute_mapping=saml_attribute_mapping,
            authentication_context=authentication_context
        )

    def cm80_saas_policies_delete_saas_application(self, name):
        """Delete SaaS Application from Configuration Master 8.0

        Use this method to delete SaaS Application Authentication Policy.

        *Parameters*
        - `name`: The name of SaaS Application to be deleted. String.
        Mandatory.

        *Exceptions*
        - GuiControlNotFoundError:xxx

        *Example*
        | CM80 Saas Policies Delete Saas Application | myAppName |
        """
        self.saas_policies_delete_saas_application(name)

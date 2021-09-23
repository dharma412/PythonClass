#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/smartlicense.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class smartlicense(CliKeywordBase):
    """
    This CLI command is used to manage smartlicenses for the ESA

       CLI --> smartlicense

       The various options are
       - `enable` : Enable Smart License
       - `transport_setup` : Configure transport setup
       - `register`: Register the ESA with CSSM
       - `reregister` : Reregister the ESA with CSSM
       - `Deregister` : Deregister the ESA
       - `activate_entitlement` : To activate entitlement(s)
       - `deactivate_entitlement`: To deactivate entitlement(s)
       - `renewath` : To renew authorization
       - `renewcert` : To renew certification
       - `status` : To display the status
       - `show_entitlement_status` : To display entitlment status

    """

    def get_keyword_names(self):
        return ['smart_license_enable',
                'smart_license_register',
                'smart_license_deregister',
                'smart_license_reregister',
                'smart_license_renewcert',
                'smart_license_renewauth',
                'smart_license_transport_setup',
                'smart_license_status',
                'smart_license_activate_entitlement',
                'smart_license_deactivate_entitlement',
                'smart_license_show_entitlement_status']

    def smart_license_enable(self):
        """Enable Smartlicense

        CLI command: smartlicense > enable

        *Parameters:*
        None

        *Return:*
        None

        *Example:*
        | Smartlicense Enable |
        """

        self._cli.smartlicense().enable()

    def smart_license_register(self, token_id):
        """Registers the ESA with CSSM

        CLI command: smartlicense > register > token_id

        *Parameters:*
        - `token_id`: token Id to be used for ESA registration with CSSM

        *Return:*
        None

        *Examples:*
        | smartlicense register <token_id>|
        """
        self._cli.smartlicense().register(token_id)

    def smart_license_deregister(self):
        """Deregisters the ESA with CSSM

        CLI command: smartlicense > deregister

        *Parameters:*
        None

        *Return:*
        None

        *Examples:*
        | smartlicense deregister |
        """
        self._cli.smartlicense().deregister()

    def smart_license_renewcert(self):
        """Renews the certificate of
        registration of ESA with CSSM.

        CLI command: smartlicense > renewcert

        *Parameters:*
        None

        *Return:*
        None

        *Examples:*
        | smart license renewcert |
        """
        self._cli.smartlicense().renewcert()

    def smart_license_renewauth(self):
        """Renews licenses with CSSM.

        CLI command: smartlicense > renewauth

        *Parameters:*
        None

        *Return:*
        None

        *Examples:*
        | smart license renewauth |
        """
        self._cli.smartlicense().renewauth()

    def smart_license_reregister(self, token_id):
        """ReRegisters the ESA with CSSM
        CLI command: smartlicense > register > token_id

        *Parameters:*
        - `token_id`: token Id to be used for ESA to reregister with CSSM

        *Return:*
        None

        *Examples:*
        | smartlicense reregister <token_id>|
        """
        self._cli.smartlicense().reregister(token_id)

    def smart_license_transport_setup(self, transport_connection, gateway_url=None):
        """Enable Smartlicense

        CLI command: smartlicense > enable

        *Parameters:*
        - 'transport_connection': Provide gateway option as DIRECT or TRANSPORT_GATEWAY
        - 'gateway_url': provide the url for transport gateway.

        *Return:*
        None

        *Example1:*
         For Direct connection
        transport_connection = DIRECT
        | Smart License Transport Setup | transport_connection = DIRECT|

        *Example2:*
         For Gateway Url connection
        | Smart License Transport Setup |
        ...  | transport_connection = TRANSPORT_GATEWAY |
        ...  | gateway_url = "http://url"|

        """

        self._cli.smartlicense().transport_setup(transport_connection, gateway_url)

    def smart_license_status(self):
        """Gets smartlicense status output

        CLI command: smartlicense > STATUS

        status output displays info in below pattern:

        Smart Licensing Status
        =======================
        Smart Licensing is ENABLED

        Registration:
        Status: UNREGISTERED
        Export-Controlled Functionality: Not Allowed

        License Authorization:
        Status: EVAL MODE
        Evaluation Period Remaining: 87 days 1 hr 41 min 0 sec
        Last Communication Attempt: NONE

        Evaluation Period:
        Evaluation Mode: In Use
        Evaluation Period Remaining: 87 days 1 hr 41 min 0 sec

        License Usage
        =============
        License Authorization Status: EVALUATION MODE
        Evaluation Period Remaining: 87 days 1 hr 41 min 0 sec

        (VOF)
        Description: null
        Count: 1
        Version: 1.0
        Status: Eval

        Product Information
        ===================
        UDI: PID:CSR1000VSN:3C08F660A0A4-FCH1752V0MEHOSTID:null

        Agent Version
        =============
        Smart Agent for Licensing: 1.3.5

        Transport Configuration
        ========================
        Mode: Direct
        URL: https://pteodc-alphastg.cloudapps.cisco.com/its/service/oddce/services/DDCEService

        *Parameters:*
        None

        *Returns*:
        Nested dictionaries of complete status output.

        self.smart_license = {
            'Agent Version': {
                'Smart Agent for Licensing': '1.3.1'},
            'Transport Configuration' : {
                'Mode': 'Direct',
                'URL': ....},
            'License Usage': {
                'License Authorization Status': 'No Licenses in Use'},
            'Product Information': {
                'UDI': 'PID:......:'},
            'Smart Licensing Status': {
                'Enabled': True,
                'Evaluation Period': {   'Evaluation Mode': 'Not In Use',
                                          etc .....},
                'License Authorization': {  'Status': 'No Licenses in Use',
                                            etc ........,
                                         },
                'Registration': {   'Status': 'REGISTERED',
                                    etc ..........}}
        }

        Example:

        To get only the registration details from status output:

        |  ${status} | Smart License Status
        |  ${reg_details} | Get From Dictionary | ${status} | Registration

        output:
        In the above example output of status would be :

        ${status} =
        {   'Smart Licensing Status': { 'Registration': {
                                         'Export-Controlled Functionality': 'Allowed',
                                         'Status': 'UNREGISTERED'}}}
        """
        return self._cli.smartlicense().status()

    def smart_license_activate_entitlement(self, entitlement_list):
        """Activate Smartlicense entitlements

        CLI command: smartlicense > activate_entitlement
        >activate_entitlement
           Tag Name                   Status
        --------------------------------------------------------------------
        1. Outbreak Filters              NOT_AVAILABLE
        2. File Analysis                 NOT_AVAILABLE
        3. File Reputation               NOT_AVAILABLE
        4. IronPort Anti-Spam            NOT_AVAILABLE
        5. Cloudmark SP                  NOT_AVAILABLE
        6. dpp                           NOT_AVAILABLE
        7. IronPort Email Encryption     NOT_AVAILABLE
        8. Graymail Safe Unsubscription  NOT_AVAILABLE
        9. IronPort Image Analysis       NOT_AVAILABLE
        10.Incoming Mail Handling        NOT_AVAILABLE
        11.Intelligent Multi-Scan        NOT_AVAILABLE
        12.McAfee                        NOT_AVAILABLE
        13.Sophos                        NOT_AVAILABLE
        Enter the appropriate entitlement number(s) for activation (for example, 3,5,8)

        *Parameters:*
        - `entitlement_list` : Enter comma separated entitlements to be activated
         It can take one more values from following list
         Outbreak Filters
         File Analysis
         Sophos
         McAfee
         File Reputation
         Cloudmark SP
         dpp
         IronPort Email Encryption
         Graymail Safe Unsubscription
         IronPort Image Analysis
         Incoming Mail Handling
         Intelligent Multi-Scan
         Ironport Anti-Spam
        *Example:*
        | @{entl_list}=  | Create List |
        | ... | McAfee |
        | ... | Sophos |
        | Smart License Activate Entitlement  ${entl_list} |
        """
        self._cli.smartlicense().activate(entitlement_list)

    def smart_license_deactivate_entitlement(self, entitlement_list):
        """Deactivate Smartlicense entitlements

        CLI command: smartlicense > deactivate_entitlement
        []> deactivate_entitlement

           Tag Name                      Status
        -----------------------------------------------------------------
        1. File Analysis                 AVAILABLE
        2. dpp                           NA_OOC
        3. IronPort Email Encryption     AVAILABLE
        4. Graymail Safe Unsubscription  NA_OOC
        5. IronPort Image Analysis       NA_OOC
        6. Incoming Mail Handling        NA_OOC
        7. Intelligent Multi-Scan        AVAILABLE
        8. McAfee                        AVAILABLE
        9. Sophos                        NA_OOC
        Enter the appropriate entitlement number(s) for deactivation (for example, 3,5,8)

        *Parameters:*
        - `entitlement_list` : Enter comma separated entitlements to be activated
         It can take one more values from following list
         Outbreak Filters
         File Analysis
         Sophos
         McAfee
         File Reputation
         Cloudmark SP
         dpp
         IronPort Email Encryption
         Graymail Safe Unsubscription
         IronPort Image Analysis
         Incoming Mail Handling
         Intelligent Multi-Scan
         Ironport Anti-Spam

        *Example:*
        | @{entl_list}=  | Create List |
        | ... | McAfee |
        | ... | Sophos |

        | Smart License Deactivate Entitlement  ${entl_list} |
        """

        self._cli.smartlicense().deactivate(entitlement_list)

    def smart_license_show_entitlement_status(self):
        """  Gets the status of the activated entitlements.

        CLI command: smartlicense > SHOW_ENTITLEMENT_STATUS

        *Parameters:*
        None

        *Return:*
        Nested dictionaries of complete entitlement status which were activated,
        In the below format.

        ${status} = {
            feature_name : {
                license_count : '..',
                expiry_date: '..',
                status: '..'
            }
        }

        Output of show entitlement status is displayed as below.
        Here only Sophos and Mcafee were activated:

        FeatureName   LicenseAuthorisationStatus   AuthorisationExpiryDate   Count
        --------------------------------------------------------------------------
        Sophos            Eval                     2017-12-11 05:25:01       1
        McAfee            Eval                     2017-12-11 05:25:00       1

        Example:
        |  ${entitlement_status} | Smart License Show Entitlement Status

        output:
        ${entitlement_status} = { 'Sophos': { 'Count': '1',
                                              'ExpiryDate': '2017-12-11 05:25:01',
                                              'Status': 'Eval'},
                                  'McAfee': { 'Count': '1',
                                              'ExpiryDate': '2017-12-11 05:25:01',
                                              'Status': 'Eval'}}
        """
        return self._cli.smartlicense().show_entitlement_status()

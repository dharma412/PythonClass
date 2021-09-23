#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/licensesmart.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase

class licensesmart(CliKeywordBase):
    """
    This CLI command is used to manage smartlicenses for the WSA

       CLI --> smartlicense

       The various options are
       - `enable` : Enable Smart License
       - `transport_setup` : Configure transport setup
       - `register`: Register the WSA with CSSM
       - `Deregister` : Deregister the WSA
       - `requestsmart_entitlement` : To activate entitlement(s)
       - `releasesmart_entitlement`: To deactivate entitlement(s)
       - `renew_auth` : To renew authorization
       - `renew_id` : To renew certification
       - `status` : To display the status
       - `summary` : To display entitlment status

    """

    def get_keyword_names(self):
        return ['license_smart_enable',
                'license_smart_register',
                'license_smart_deregister',
                'license_smart_renewid',
                'license_smart_renewauth',
                'license_smart_url',
                'license_smart_status',
                'license_smart_request_smart_entitlement',
                'license_smart_release_smart_entitlement',
                'license_smart_menu_item_check',
                'license_smart_get_license_list_available_for_request',
                'license_smart_get_releasesmart_license_list',
                'license_smart_summary']

    def license_smart_enable(self):

        """Enable Smartlicense

        CLI command: license_smart > enable

        *Parameters:*
        None

        *Return:*
        None

        *Example:*
        | License Smart Enable |
        """

        self._cli.licensesmart().enable()

    def license_smart_register(self, *args):
        """
        Registers the WSA with CSSM. There is a force register option
        in "REGISTERED" Mode. The functionality of it is to remove and register
        the DUT to CSSM if it is already registered.

        CLI command: license_smart > register > token_id

        *Parameters:*
        - `token`: token Id to be used for WSA registration with CSSM
        - 'reregister': Reregister this product instance if it is already registered 'yes' or 'no'
        - 'remove_register': remove the existing product instance from Smart Software
           Manager and register this one in its place
        *Return:*
        None

        *Examples:*
        1. If the status in Unregistered state

        Choose the operation you want to perform:
        - REGISTER - Register the product for Smart Licensing.
        - URL - Set the Smart Transport URL.
        - STATUS - Show overall Smart Licensing status.
        - SUMMARY - Show Smart Licensing status summary.
        []> register

         Reregister this product instance if it is already registered [N]>

         Enter token to register the product:
         []>
         Example:
         | license smart register | token=${token} | reregister=yes


        2. If the Device is REGISTERED.

        Choose the operation you want to perform:
        - URL - Set the Smart Transport URL.
        - REQUESTSMART_LICENSE - Request licenses for the product.
        - RELEASESMART_LICENSE - Release licenses of the product.
        - DEREGISTER - Deregister the product from Smart Licensing.
        - REREGISTER - Reregister the product for Smart Licensing.
        - RENEW_AUTH - Renew authorization of Smart Licenses in use.
        - RENEW_ID - Renew registration with Smart Licensing.
        - STATUS - Show overall Smart Licensing status.
        - SUMMARY - Show Smart Licensing status summary.

        EX: IF product is in registered mode. When executed reregister command
        below is the output provided.

        []> reregister

        A product instance has already been registered to Smart Software Manager.
        Do you want to remove the existing product instance from Smart Software Manager and
        register this one in its place? Press Yes or No []> no

        Example for using this function in 3rd Menu when product is registered:
        | license smart register | token=${token} | remove_register =yes

        """

        kwargs = self._convert_to_dict(args)
        if 'remove_register' in kwargs:
            self._cli.licensesmart().reregister(**kwargs)
        else:
            self._cli.licensesmart().register(**kwargs)

    def license_smart_deregister(self):

        """Deregisters the WSA with CSSM

        CLI command: license_smart > deregister

        *Parameters:*
        None

        *Return:*
        None

        *Examples:*
        | license smart deregister |
        """
        self._cli.licensesmart().deregister()

    def license_smart_renewid(self):

        """Renews the certificate of
        registration of WSA with CSSM.

        CLI command: license_smart > renew_id

        *Parameters:*
        None

        *Return:*
        None

        *Examples:*
        | license smart renewid |
        """
        self._cli.licensesmart().renewid()

    def license_smart_renewauth(self):

        """Renews licenses with CSSM.

        CLI command: license_smart > renew_auth

        *Parameters:*
        None

        *Return:*
        None

        *Examples:*
        | license_smart_renewauth |
        """
        self._cli.licensesmart().renewauth()

    def license_smart_url(self, transport_connection, gateway_url=None):
        """Enable Smartlicense

        CLI command: license_smart > url

        *Parameters:*
        - 'transport_connection': Provide gateway option as DIRECT or TRANSPORT_GATEWAY
        - 'gateway_url': provide the url for transport gateway.

        *Return:*
        None

        *Example1:*
         For Direct connection
        transport_connection = DIRECT
        | License Smart URL | transport_connection = DIRECT|

        *Example2:*
         For Gateway Url connection
        | License Smart URL |
        ...  | transport_connection = TRANSPORT_GATEWAY |
        ...  | gateway_url = "http://url"|

        """

        self._cli.licensesmart().url(transport_connection, gateway_url)

    def license_smart_status(self):

        """Gets smartlicense status output

        CLI command: license_smart > STATUS

        status output displays info in below pattern:

        Smart Licensing Status
        =======================
        Smart Licensing is ENABLED

        Registration:
        Status: UNREGISTERED

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

        Product Instance:
        ===================
        Product Instance Name: pod1216-wsa112.ibauto

        Transport Configuration
        ========================
        Mode: Direct
        URL: https://pteodc-alphastg.cloudapps.cisco.com/its/service/oddce/services/DDCEService

        *Parameters:*
        None

        *Returns*:
        Nested dictionaries of complete status output.

        self.smart_license = {
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

        |  ${status} | License Smart Status
        |  ${reg_details} | Get From Dictionary | ${status} | Registration

        output:
        In the above example output of status would be :

        ${status} =
        {   'Smart Licensing Status': { 'Registration': {
                                         'Status': 'UNREGISTERED'}}}
        """
        return self._cli.licensesmart().status()

    def license_smart_request_smart_entitlement(self, entitlement_list):
        """Activate Smartlicense entitlements

        CLI command: license_smart > requestsmart_entitlement
        >requestsmart_entitlement
           Tag Name                                                                     Status
        ---------------------------------------------------------------------------------------
        1. Web Security Appliance Cisco IronPort Web Usage Controls                    Not requested
        2. Web Security Appliance Anti-Virus Webroot                                   Not requested
        3. Web Security Appliance IronPort L4 Traffic Monitor                          Not requested
        4. Web Security Appliance Cisco AnyConnect SM for AnyConnect                   Not requested
        5. Web Security Appliance Advanced Malware Protection Reputation               Not requested
        6. Web Security Appliance Anti-Virus Sophos                                    Not requested
        7. Web Security Appliance IronPort Web Reputation Filters                      Not requested
        8. Web Security Appliance Advanced Malware Protection                          Not requested
        9. Web Security Appliance Anti-Virus McAfee                                    Not requested
        10. Web Security Appliance IronPort Web Proxy                                  Not requested
        11. Web Security Appliance HTTPs Decryption                                    Not requested

        Enter the appropriate entitlement number(s) for activation (for example, 1,2)

        *Parameters:*
        - `entitlement_list` : Enter comma separated entitlements to be activated
        *Example:*
        | @{entl_list}=  | Create List |
        | ... | Web Security Appliance Cisco IronPort Web Usage Controls |
        | ... | Web Security Appliance Anti-Virus Webroot |
        | License Smart Request Smart Entitlement  ${entl_list} |
        """
        self._cli.licensesmart().requestsmart_entitlement(entitlement_list)

    def license_smart_release_smart_entitlement(self, entitlement_list):
        """Deactivate Smartlicense entitlements

        CLI command: license_smart > releasesmart_entitlement
        []> releasesmart_entitlement

           Tag Name                                                                            Status
        -----------------------------------------------------------------------------------------------

       1. Web Security Appliance Cisco IronPort Web Usage Controls                              Eval
       2. Web Security Appliance Anti-Virus Webroot                                             Eval
       3. Web Security Appliance IronPort L4 Traffic Monitor                                    Eval
       4. Web Security Appliance Cisco AnyConnect SM for AnyConnect                             Eval
       5. Web Security Appliance Advanced Malware Protection Reputation                         Eval
       6. Web Security Appliance Anti-Virus Sophos                                              Not requested
       7. Web Security Appliance IronPort Web Reputation Filters                                Not requested
       8. Web Security Appliance Advanced Malware Protection                                    Not requested
       9. Web Security Appliance Anti-Virus McAfee                                              Not requested
       10. Web Security Appliance IronPort Web Proxy                                            Not requested
       11. Web Security Appliance HTTPs Decryption                                              Not requested

        Enter the appropriate entitlement number(s) for deactivation (for example, 1,2)

        *Example:*
        | @{entl_list}=  | Create List |
        | ... | Web Security Appliance Cisco IronPort Web Usage Controls |
        | ... | Web Security Appliance Anti-Virus Webroot |

        | License Smart Release Smart Entitlement  ${entl_list} |
        """

        self._cli.licensesmart().releasesmart_entitlement(entitlement_list)

    def license_smart_summary(self):
        """  Gets the status of the activated entitlements.

        CLI command: license_smart > summary

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
        Feature Name                                                                          License Authorization Status
        -----------------------------------------------------------------------------------------------------------------
         Web Security Appliance Cisco IronPort Web Usage Controls                              Eval
         Web Security Appliance Anti-Virus Webroot                                             Eval

        Example:
        |  ${entitlement_status} | License Smart Summary

        output:
        ${entitlement_status} = { 'Web Security Appliance Cisco IronPort Web Usage Controls': { 'Count': '1',
                                              'Status': 'Eval'},
                                  'Web Security Appliance Anti-Virus Webroot': { 'Count': '1',
                                              'Status': 'Eval'}}
        """
        return self._cli.licensesmart().summary()

    def license_smart_menu_item_check(self, menu):
        """  Verifies the list of menu items under license smart command.
        Returns 'True' if found else retuens 'False'.

        *Parameters:*
        -'Menu' - Provide the Menu item that needs to be verified.

        *Return:*
        Boolean True or False

        Example:
        > license_smart(below are list of menu's diaplyed)
        Choose the operation you want to perform:
        - REQUESTSMART_ENTITLEMENT - Request entitlements for the product.
        - RELEASESMART_ENTITLEMENT - Release entitlements of the product.
        - REGISTER - Register the product for Smart Licensing.
        - URL - Set the Smart Transport URL.
        - STATUS - Show overall Smart Licensing status

        |  ${exists} | License Smart Menu Item Check |  URL

        output:
        ${exists} == True
        """
        return self._cli.licensesmart().smartlicense_verify_menu_items(menu)

    def license_smart_get_license_list_available_for_request(self):
        """It will return the list of entitlement present under
           REQUESTSMART_ENTITLEMENT command.

        CLI command: license_smart > requestsmart_entitlement
        >requestsmart_entitlement
           Tag Name                                                          Status
        ------------------------------------------------------------------------------
        1. Web Security Appliance Cisco IronPort Web Usage Controls                    Not requested
        2. Web Security Appliance Anti-Virus Webroot                                   Not requested
        3. Web Security Appliance IronPort L4 Traffic Monitor                          Not requested
        4. Web Security Appliance Cisco AnyConnect SM for AnyConnect                   Not requested
        5. Web Security Appliance Advanced Malware Protection Reputation               Not requested
        6. Web Security Appliance Anti-Virus Sophos                                    Not requested
        7. Web Security Appliance IronPort Web Reputation Filters                      Not requested
        8. Web Security Appliance Advanced Malware Protection                          Not requested
        9. Web Security Appliance Anti-Virus McAfee                                    Not requested
        10. Web Security Appliance IronPort Web Proxy                                  Not requested
        11. Web Security Appliance HTTPs Decryption                                    Not requested
         Enter the appropriate entitlement number(s) for activation (for example, 3,5,8)

        *Parameters:*
         None

        *Return:*
        Returns dictinary
        containing entitlement Tag and number corresponding to it available under.
        'REQUESTSMART_ENTITLEMENT' command.

        *Example:*

        | ${not_activated_list} | License Smart Get Entitlementlist Requested Not Activated

        output:

        Returns whichever entitlements present under requestsmart_entitlement command in below format.
        ${not_activated_list} = {'Web Security Appliance Cisco IronPort Web Usage Controls':'1' , 'Web Security Appliance Anti-Virus Webroot':'2'}

        """
        return self._cli.licensesmart().get_license_list_available_for_request()

    def license_smart_get_releasesmart_license_list(self):
        """It will return the list of entitlement present under
           RELEASESMART_LICENSE command.

        CLI command: license_smart > releasesmart_license
        []> releasesmart_license

         Feature Name                                                                License Authorization Status
         -----------------------------------------------------------------------------------------------------
         1. Web Security Appliance Cisco AnyConnect SM for AnyConnect                             Eval
         2. Web Security Appliance HTTPs Decryption                                               Eval

         *Parameters:*
         None

        *Return:*
        Returns dictinary
        containing entitlement Tag and state corresponding to it available under.
        'RELEASESMART_LICENSE' command.

        *Example:*

        | ${activated_list} | License Smart Get ReleaseSmart License List

        output:

        Returns whichever entitlements present under RELEASESMART_LICENSE command in below format.
        ${activated_list} = {'Web Security Appliance Cisco AnyConnect SM for AnyConnect': 'Eval', 'Web Security Appliance HTTPs Decryption': 'Eval'}

        """
        return self._cli.licensesmart().get_license_list_releasesmart_license()

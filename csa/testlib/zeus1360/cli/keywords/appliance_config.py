# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/appliance_config.py#1 $
# $DateTime: 2020/03/05 19:45:32 $
# $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class ApplianceConfig(CliKeywordBase):
    """
    cli -> applianceconfig

    The applianceconfig command is used to configure other appliances that the
    M-series appliance transfers data with, as well as which services are
    enabled for each appliance.
    """

    def get_keyword_names(self):
        return [
            'appliance_config_list',
            'appliance_config_add',
            'appliance_config_edit',
            'appliance_config_services',
            'appliance_config_delete',
            'appliance_config_test',
            'appliance_config_status',
            'appliance_config_port',
                ]

    def appliance_config_list(self):
        """
        This will list all configured appliances, with their IP, name, and
        whether or not they have been authenticated.

        Examples:
        | Appliance Config List |
        """
        output = self._cli.applianceconfig(batch_cmd="list")
        self._info(output)
        return output

    def appliance_config_add(self, IP, name, product_type, username=None,
            password=None, port=None):
        """
        This will add a new appliance with the given IP address for use by the
        M-series.  A name is also associated with the IP for ease of use.  The
        M-series can be authorized to connect to the appliance for file
        transfer by passing a username and password.  Providing a port will
        override the global ssh port setting.

        Parameters:
            - `IP` - The IP address or hostname of the appliance to add.
            - `name` - A name to associate with this appliance.
            - `product_type` - Either 'esa' or 'wsa'.
            - `username` - A valid username on the appliance.
            - `password` - The password for the given username.
            - `port` - The port to connect to.

        Note:
            If username and password for ssh transfer are not passed then it
            will not be enabled.

        Examples:
        | # Add ESA Appliance without file transfer access via SSH |
        | Appliance Config Add | 10.92.145.126 | my_esa | esa |
        | # Add WSA Appliance with file transfer access via SSH on port 10022 |
        | Appliance Config Add | 10.7.8.114 | wsa103 | wsa |
        | ... | username=admin | password=ironport | port=10022 |
        | # Add WSA Appliance add assign default configuration master to it |
        | Appliance Config Add | wsa103.wga | wsa103 | wsa |
        | ... | username=admin | password=ironport |
        | # Add WSA Appliance add assign configuration master 7.5 to it |
        | Appliance Config Add | wsa103.wga | wsa103 | wsa |
        | ... | username=admin | password=ironport |
        """
        kwargs = {
                'ip_addr': IP,
                'name': name,
                'type': product_type,
                }

        # if username and password for ssh transfer are not passed then it will
        # not be enabled
        ssh_transfer = 'no' if username is None \
                            and password is None else 'yes'
        kwargs['ssh_transfer']  = self._process_yes_no(ssh_transfer)
        if ssh_transfer == 'yes':
            kwargs['username'] = username or DEFAULT
            kwargs['password'] = password or DEFAULT

            # custom ssh port settings
            use_custom_ssh_port = 'no' if port is None else 'yes'
            if use_custom_ssh_port == 'yes':
                kwargs['cust_ssh_port'] = \
                        self._process_yes_no(use_custom_ssh_port)
                kwargs['ssh_port'] = port or DEFAULT

        self._cli.applianceconfig().add(**kwargs)

    def appliance_config_edit(self, name, IP=None, new_name=None,
            product_type=None, username=None, password=None, port=None):
        """
        This will edit an existing appliance with current-ip to be updated
        with new information.  Providing a username and password will
        also authenticate the M-series to connect to the appliance.
        Providing a port will override the global ssh port setting.

        Parameters:
            - `name` - The name, IP address or hostname of the appliance to edit.
            - `IP` - The new IP address or hostname of the appliance.
            - `new_name` - The new name to associate with this appliance.
            - `product_type` - Either 'esa' or 'wsa'.
            - `username` - A valid username on the appliance.
            - `password` - The password for the given username.
            - `port` - The SSH port to connect to.

        Note:
            If username and password for ssh transfer are not passed then it
            will not be enabled.

        Examples:
        | # Enable file transfer access to the ESA Appliance via SSH port 10022 |
        | Appliance Config Edit | my_esa | username=admin | password=ironport |
        | # Update name and IP address and disable file transfer to the WSA Appliance |
        | Appliance Config Edit | my_wsa | new_name=my_new_wsa | IP=10.10.10.10 |
        """
        kwargs = {
                'edit_name': name,
                }

        kwargs['name'] = new_name or DEFAULT
        kwargs['ip_addr'] = IP or DEFAULT
        kwargs['type'] = product_type or DEFAULT

        # if username and password for ssh transfer are not passed then it will
        # not be enabled
        ssh_transfer = 'no' if username is None \
                            and password is None else 'yes'
        kwargs['ssh_transfer']  = self._process_yes_no(ssh_transfer)
        if ssh_transfer == 'yes':
            kwargs['username'] = username or DEFAULT
            kwargs['password'] = password or DEFAULT

            # custom ssh port settings
            use_custom_ssh_port = 'no' if port is None else 'yes'
            if use_custom_ssh_port == 'yes':
                kwargs['cust_ssh_port'] = \
                        self._process_yes_no(use_custom_ssh_port)
                kwargs['ssh_port'] = port or DEFAULT

        self._cli.applianceconfig().edit(**kwargs)

    def appliance_config_delete(self, name):
        """
        This will delete the given appliance so that the M-series will
        no longer interact with the appliance.

        Parameters:
            - `name` - The name, IP address or hostname of the appliance
                       to delete.

        Examples:
        | # Delete Appliance using name assigned to it |
        | Appliance Config Delete | my_esa |
        | # Delete Appliance using its hostname |
        | Appliance Config Delete | wsa103.wga |
        """
        self._cli.applianceconfig().delete(name)

    def appliance_config_test(self, name):
        """
        This will test two things.  First it tests that the M-series can
        sucessfully connect to the appliance.  Secondly, it will check to make
        sure that the services which are enabled on the M-series for this
        appliance are also enabled on the appliance itself.  If the service is
        disabled on the appliance a warning will be printed.

        Parameters:
            - `name` - The name, IP address or hostname of the appliance
                       to test.

        Examples:
        | # Test Appliance using name assigned to it |
        | Appliance Config Test | my_wsa |
        | # Test Appliance using its hostname |
        | Appliance Config Test | wsa103.wga |
        """
        output = self._cli.applianceconfig().test(name)
        self._info(output)
        return output

    def appliance_config_services(self, name, email_slbl=None,
            email_reporting=None, email_tracking=None, web_reporting=None,
            web_config_mgr=None, assign_master=None, cm_version=None,
            email_quarantine=None):
        """
        This will turn on or off the given feature for the given appliance.

        Parameters:
            - `name` - The name, IP address or hostname of the appliance
                       to configure.

            ESA fetures:
            - `email_quarantine` - Turn on or off Centralized Policy Quarantine
            - `email_slbl` - Turn on or off Centralized Safelist/Blocklist
            - `email_tracking` - Turn on or off Centralized Tracking
            - `email_reporting` - Turn on or off Centralized Email Reporting

            WSA features:
            - `web_reporting` - Turn on or off Centralized Web Reporting.
            - `web_config_mgr` - Turn on or off Cisco IronPort Centralized
                                 Configuration Manager.
            - `assign_master` - Whether assign the appliance to a configuration
                                master.
            - `cm_version` - configuration master for this appliance
        Note:
            All parameters expect either 'yes' or 'no'
            values. If parameter is missed or ${EMPTY} string is passed then
            default value of thi parameter will be used.

        Examples:
        | # Enable all features for the ESA Appliance |
        | Appliance Config Services | my_esa | email_slbl=yes | email_reporting=yes |
        | ... | email_tracking=yes |
        | # Disable Reporting for the WSA Appliance and enable rest |
        | Appliance Config Services | my_wsa | web_reporting=no | web_config_mgr=yes |
        | ... | assign_master=yes |
        """
        kwargs = {
                'name_num': name,
                }

        is_esa = email_slbl is not None or \
                 email_reporting is not None or \
                 email_tracking is not None or \
                 email_quarantine is not None
        is_wsa = web_reporting is not None or \
                 web_config_mgr is not None or \
                 assign_master is not None

        if is_esa and is_wsa:
            raise ValueError, "Either services for ESA or WSA appliance" \
                    " should be configured in single keyword."
        if is_esa:
            self._info("Configuring services for ESA appliance")
            kwargs['email_slbl'] = self._process_yes_no(email_slbl or DEFAULT)
            kwargs['email_tracking'] = self._process_yes_no(email_tracking \
                or DEFAULT)
            kwargs['email_reporting'] = self._process_yes_no(email_reporting \
                or DEFAULT)
            kwargs['email_quarantine'] = self._process_yes_no(email_quarantine \
                or DEFAULT)
        elif is_wsa:
            self._info("Configuring services for WSA appliance")
            kwargs['web_reporting'] = self._process_yes_no(web_reporting or \
                                                           DEFAULT)
            if web_config_mgr is not None:
                kwargs['web_config_mgr'] = self._process_yes_no(web_config_mgr)

            if assign_master is not None:
                kwargs['assign_master'] = \
                    self._process_yes_no(assign_master)
                if cm_version:
                    kwargs['cm_version'] = cm_version
        else:
            self._info("No configuration parameters is passed.")
            return

        self._cli.applianceconfig().services(**kwargs)


    def appliance_config_status(self):
        """
        This will print out the global status of the services controlled by
        applianceconfig.

        Examples:
        | Appliance Config Status |
        """
        output = self._cli.applianceconfig().status()
        self._info(output)
        return output

    def appliance_config_port(self, port=None):
        """
        This will print out the port currently being used to communicate with
        remote appliances.  An optional port number can be provided to change
        that value.

        Parameters:
            - `port` - port do you want to use for appliance communication.

        Examples:
        | # Print port used for communication |
        | Appliance Config Port |
        | # Change port number to 10022 |
        | Appliance Config Port | 10022 |
        """
        if port is None:
            output = self._cli.applianceconfig(batch_cmd='port')
            self._info(output)
            return output
        else:
            self._cli.applianceconfig().port(port)

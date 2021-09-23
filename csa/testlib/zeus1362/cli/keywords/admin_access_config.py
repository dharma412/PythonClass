#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/admin_access_config.py#2 $ $DateTime: 2020/06/18 05:28:57 $ $Author: mrmohank $

from common.cli.clicommon import CliKeywordBase
import common.cli.cliexceptions as cliexceptions
import socket

class AdminAccessConfig(CliKeywordBase):
    """Configuration for admin interface access."""

    proxy_list = ['proxy', 'proxyonly']
    restricted_list = ['restrict'] + proxy_list
    all_list = ['all'] + restricted_list

    error_message_incorrect_mode = "Incorrect mode for this operation"

    def get_keyword_names(self):
        return ['admin_access_config_csrf',
                'admin_access_config_banner',
                'admin_access_config_welcome_message',
                'admin_access_clear_welcome_message',
                'admin_access_config_ipaccess_print',
                'admin_access_config_ipaccess_change_mode',
                'admin_access_config_ipaccess_allow_all',
                'admin_access_config_ipaccess_new',
                'admin_access_config_ipaccess_edit',
                'admin_access_config_ipaccess_delete',
                'admin_access_config_ipaccess_clear',
                'admin_access_config_ipaccess_proxylist_new',
                'admin_access_config_ipaccess_proxylist_edit',
                'admin_access_config_ipaccess_proxylist_delete',
                'admin_access_config_ipaccess_proxylist_clear',
                'admin_access_config_ipaccess_proxyheader',
                'admin_access_config_hostheader',
                ]

    def admin_access_config_banner(self, operation=None, banner_text=None, banner_file=None):
        """Configure login message(banner) for appliance administrator login.

        adminaccessconfig > banner

        *Parameters:*
        - `operation`: Operation to perform.  Either 'print', 'import', or 'clear'.
        - `banner_text`: banner text if 'operation' is set to 'import'.
        - `banner_file`: name of file in /data/pub/configuration directory of
                  appliance if 'operation' is set to 'import'.

        *Examples:*
        | Admin Access Config Banner | operation=import | banner_text=Hello QA Folks! |
        | Admin Access Config Banner | operation=import | banner_file=mybanner.txt | # mybanner.txt should existed on dut's /data/pub/configuration |
        | Admin Access Config Banner | operation=clear |
        | Admin Access Config Banner | operation=print |
        """
        if operation is not None:
            if operation.lower() == 'import':
                return self._cli.adminaccessconfig().banner().import_banner(banner_text, banner_file)
            elif operation.lower() == 'clear':
                return self._cli.adminaccessconfig().banner().clear()
            elif operation.lower() == 'print':
                return self._cli.adminaccessconfig().print_info('banner')
            else:
                raise cliexceptions.CliValueError(
                    "Valid operations are 'print', 'import', or 'clear'")


    def admin_access_config_welcome_message(self,message):
        """Configures welcome message cli and gui logins

        *Examples:*
        Admin Access Welcome New  message='Welcome'
         """
        self._cli.adminaccessconfig().welcome().new(message)

    def admin_access_clear_welcome_message(self):
        """Clears the welcome message

        *Examples:*
        Admin Access Welcome Clear
         """
        self._cli.adminaccessconfig().welcome().clear()

    def admin_access_config_ipaccess_print(self):
        """Output configuration for ipaccess

        *Examples:*
        | ${result} | Admin Access Config Ipaccess Print |
        """
        return self._cli.adminaccessconfig().print_info('ipaccess')

    def admin_access_config_ipaccess_allow_all(self):
        """Switching to mode when all have access

        adminaccessconfig > ipaccess > all

        *Examples:*
        | Admin Access Config Ipaccess Allow All |
        """
        self._cli.adminaccessconfig().ipaccess().allow_all()

    def admin_access_config_ipaccess_change_mode(self, mode=None):
        """Change mode of access
        All data should be inserted before changing mode

        adminaccessconfig > ipaccess > [all,restrict,proxy,proxyonly]

        *Parameters:*
        - `mode`: mode that will be used. Either 'all', 'proxy',
                  'proxyonly', 'restrict'

        *Example:*
        | Admin Access Config Ipaccess Change Mode | mode=Restrict |
        | Admin Access Config Ipaccess Change Mode | mode=Proxyonly |
        """
        if mode.lower() in self.all_list:
            self._cli.adminaccessconfig().ipaccess().change_mode(mode)
        else:
            raise cliexceptions.CliValueError(self.error_message_incorrect_mode)

    def admin_access_config_ipaccess_new(self, mode=None, ip=None):
        """Addition of a new ip address

        adminaccessconfig > ipaccess > [restrict,proxy,proxyonly] > new

        *Parameters:*
        - `mode`: mode that will be used after addition.
                  Either 'restrict', 'proxy' or 'proxyonly'.
        - `ip`: new ip address

        *Example:*
        | Admin Access Config Ipaccess New | mode=Restrict | ip=2.3.4.5 |
        | Admin Access Config Ipaccess New | mode=Proxy | ip=1.2.3.4 |
        """
        if mode.lower() in self.restricted_list:
            self._cli.adminaccessconfig().ipaccess(mode).new(ip)
        else:
            raise cliexceptions.CliValueError(self.error_message_incorrect_mode)

    def admin_access_config_ipaccess_delete(self, mode=None, ip=None):
        """Deletion of an existing ip address

        adminaccessconfig > ipaccess > [restrict,proxy,proxyonly] > delete

        *Parameters:*
        - `mode`: mode that will be used after deletion.
                   Either 'restrict', 'proxy' or 'proxyonly'.
        - `ip`: ip address of existing ip

        *Example:*
        | Admin Access Config Ipaccess Delete | mode=Restrict | ip=2.3.4.5 |
        | Admin Access Config Ipaccess Delete | mode=Proxy | ip=1.2.3.4 |
        """
        if mode.lower() in self.restricted_list:
            self._cli.adminaccessconfig().ipaccess(mode).delete(ip)
        else:
            raise cliexceptions.CliValueError(self.error_message_incorrect_mode)

    def admin_access_config_ipaccess_edit(self, mode=None, ip_set=None):
        """Modify existing ip address

        adminaccessconfig > ipaccess > [restrict,proxy,proxyonly] > edit

        *Parameters:*
        - `mode`: mode that will be used after modification.
                  Either 'restrict', 'proxy' or 'proxyonly'.
        - `ip_set`: ip addresses of existing ip and new one to replace the
            old address. Both in CIDR notation in specific
            format olp_ip:new_ip

        *Example:*
        | Admin Access Config Ipaccess Edit | mode=Restrict | ip_set=1.2.3.4:2.3.4.5 |
        | Admin Access Config Ipaccess Edit | mode=Proxy | ip_set=1.2.3.4:2.3.4.5 |
        """
        if ip_set is not None:
            if mode.lower() in self.restricted_list:
                self._cli.adminaccessconfig().ipaccess(mode).\
                    edit(old_ip=str(ip_set.split(':')[0]),
                    new_ip=str(ip_set.split(':')[1]))
            else:
                raise cliexceptions.CliValueError(
                    self.error_message_incorrect_mode)

    def admin_access_config_ipaccess_clear(self, mode=None):
        """Clearing ipaccess configuration for ip addresses

        adminaccessconfig > ipaccess > [restrict,proxy,proxyonly] > clear

        *Parameters:*
        - `mode`: mode that will be used after clearing.
                  Either 'restrict', 'proxy' or 'proxyonly'.

        *Example:*
        | Admin Access Config Ipaccess Clear | mode=Restrict |
        | Admin Access Config Ipaccess Clear | mode=Proxy |
        """
        if mode.lower() in self.restricted_list:
            self._cli.adminaccessconfig().ipaccess(mode).clear()
        else:
            raise cliexceptions.CliValueError(self.error_message_incorrect_mode)

    def admin_access_config_ipaccess_proxylist_new(self, mode=None, ip=None):
        """Addition of a new proxy address

        adminaccessconfig > ipaccess > [proxy,proxyonly] > proxy_list > new

        *Parameters:*
        - `mode`: mode that will be used after addition.
                  Either 'proxy' or 'proxyonly'.
        - `ip`: new proxy address

        *Example:*
        | Admin Access Config Ipaccess Proxylist New | mode=Proxyonly | ip=2.3.4.5 |
        | Admin Access Config Ipaccess Proxylist New | mode=Proxy | ip=1.2.3.4 |
        """
        if mode.lower() in self.proxy_list:
            self._cli.adminaccessconfig().ipaccess(mode).proxylist().new(ip)
        else:
            raise cliexceptions.CliValueError(self.error_message_incorrect_mode)

    def admin_access_config_ipaccess_proxylist_delete(self, mode=None, ip=None):
        """Deletion an existing proxy address

        adminaccessconfig > ipaccess > [proxy,proxyonly] > proxy_list > delete

        *Parameters:*
        - `mode`: mode that will be used after deletion.
                  Either 'proxy' or 'proxyonly'.
        - `ip`: ip address of existing proxy

        *Example:*
        | Admin Access Config Ipaccess Proxylist Delete | mode=Proxyonly | ip=2.3.4.5 |
        | Admin Access Config Ipaccess Proxylist Delete | mode=Proxy | ip=1.2.3.4 |
        """
        if mode.lower() in self.proxy_list:
            self._cli.adminaccessconfig().ipaccess(mode).proxylist().delete(ip)
        else:
            raise cliexceptions.CliValueError(self.error_message_incorrect_mode)

    def admin_access_config_ipaccess_proxylist_edit(self, mode=None, ip_set=None):
        """Modify of an existing proxy address

        adminaccessconfig > ipaccess > [proxy,proxyonly] > proxy_list > edit

        *Parameters:*
        - `mode`: mode that will be used after modification. Either 'proxy' or 'proxyonly'.
        - `ip_set`: ip addresses of existing proxies and new one to replace the
            old address. Both in CIDR notation in specific
            format olp_ip:new_ip

        Example:
        | Admin Access Config Ipaccess Proxylist Edit | mode=Proxyonly | ip_set=1.2.3.4:2.3.4.5 |
        | Admin Access Config Ipaccess Proxylist Edit | mode=Proxy | ip_set=1.2.3.4:2.3.4.5 |
        """
        if mode.lower() in self.proxy_list:
            self._cli.adminaccessconfig().ipaccess(mode).proxylist().\
                edit(old_ip=str(ip_set.split(':')[0]),
                new_ip=str(ip_set.split(':')[1]))
        else:
            raise cliexceptions.CliValueError(self.error_message_incorrect_mode)

    def admin_access_config_ipaccess_proxylist_clear(self, mode=None, ip=None):
        """Clearing ipaccess configuration for proxy addresses

        adminaccessconfig > ipaccess > [proxy,proxyonly] > proxy_list > clear

        *Parameters:*
        - `mode`: mode that will be used after clearing. Either 'proxy' or 'proxyonly'.

        *Example:*
        | Admin Access Config Ipaccess Proxylist Clear | mode=Proxyonly |
        | Admin Access Config Ipaccess Proxylist Clear | mode=Proxy |
        """
        if mode.lower() in self.proxy_list:
            self._cli.adminaccessconfig().ipaccess(mode).proxylist().clear(ip)
        else:
            raise cliexceptions.CliValueError(self.error_message_incorrect_mode)

    def admin_access_config_ipaccess_proxyheader(self, mode=None, header_name=None):
        """Modify a value of the proxy header

        adminaccessconfig > ipaccess > [proxy,proxyonly] > origin_ip_header

        *Parameters:*
        - `mode`: mode that will use after modification. Either 'proxy' or 'proxyonly'.
        - `header_name`: value that will be used as proxy header

        *Example:*
        | Admin Access Config Ipaccess Proxyheader | mode=Proxyonly | header_name=Hello QA! |
        | Admin Access Config Ipaccess Proxyheader | mode=Proxy | header_name=Hello testers! |
        """
        if header_name is not None:
            if mode.lower() in self.proxy_list:
                self._cli.adminaccessconfig().ipaccess(mode).proxyheader(header_name)
            else:
                raise cliexceptions.CliValueError(self.error_message_incorrect_mode)

    def admin_access_config_csrf(self, operation=None):
        """Configure web UI Cross-Site Request Forgeries protection

        adminaccessconfig > csrf

        *Parameters:*
        - `operation`: Operation to perform.  Either 'print', 'enable', or 'disable'

        *Examples:*
        | Admin Access Config CSRF | operation=enable |
        | Admin Access Config CSRF | operation=disable |
        | Admin Access Config CSRF | operation=print |
        """
        if operation is not None:
            if operation.lower() == 'enable':
                return self._cli.adminaccessconfig().csrf().enable()
            elif operation.lower() == 'disable':
                return self._cli.adminaccessconfig().csrf().disable()
            elif operation.lower() == 'print':
                return self._cli.adminaccessconfig().print_info('csrf')
            else:
                raise cliexceptions.CliValueError(
                    "Valid operations are 'print', 'enable', or 'disable'")

    def admin_access_config_hostheader(self, operation=None):
        """Configure option to use host header in HTTP requests

        adminaccessconfig > hostheader

        *Parameters:*
        - `operation`: Operation to perform.  Either 'print', 'enable', or 'disable'

        *Examples:*
        | Admin Access Config HostHeader | operation=enable |
        | Admin Access Config HostHeader | operation=disable |
        | Admin Access Config HostHeader | operation=print |
        """
        if operation is not None:
            if operation.lower() == 'enable':
                return self._cli.adminaccessconfig().hostheader().enable()
            elif operation.lower() == 'disable':
                return self._cli.adminaccessconfig().hostheader().disable()
            elif operation.lower() == 'print':
                return self._cli.adminaccessconfig().print_info('hostheader')
            else:
                raise cliexceptions.CliValueError(
                    "Valid operations are 'print', 'enable', or 'disable'")

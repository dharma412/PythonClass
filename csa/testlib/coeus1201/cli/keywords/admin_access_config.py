#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/admin_access_config.py#1 $

from common.cli.clicommon import CliKeywordBase
import common.cli.cliexceptions as cliexceptions

class AdminAccessConfig(CliKeywordBase):
    """Configuration for admin interface access."""

    def get_keyword_names(self):
        return ['admin_access_config_banner',
                'admin_access_config_ipaccess_allow_all',
                'admin_access_config_ipaccess_restricted_new',
                'admin_access_config_ipaccess_restricted_delete',
                'admin_access_config_ipaccess_restricted_edit',
                'admin_access_config_ipaccess_restricted_clear',
                'admin_access_config_timeout',
                'admin_access_config_how_tos',
                'admin_access_config_how_tos_is_enabled'
                ]

    def admin_access_config_banner(self, op=None, banner=None, file=None):
        """Configure access banner for appliance administrator login.

        adminaccessconfig > banner

        Parameters:
        - `op`: Operation to perform.  Either 'paste', 'load', or 'clear'.
        - `banner`: banner text if 'op' is set to 'paste'.
        - `file`: name of file in /data/pub/configuration directory of
                  appliance if 'op' is set to 'load'.

        Examples:
        | Admin Access Config Banner | op=paste | banner=Hello QA Folks! |
        | Admin Access Config Banner | op=load | file=mybanner.txt | # mybanner.txt should existed on dut's /data/pub/configuration |
        | Admin Access Config Banner | op=clear |
        """
        if op is not None:
            if op not in ('paste', 'load', 'clear'):
                raise cliexceptions.CliValueError(
                    "Valid operation are 'paste', 'load', or 'clear'")
            else:
                if op == 'paste':
                    load_method = 'pasting'
                    if banner is not None:
                        banner_str = str(banner)
                    else:
                        raise cliexceptions.CliValueError(
                            'Banner text is required for paste operation.')
                    file_name = None
                elif op == 'load':
                    load_method = 'file'
                    banner_str = None
                    if file is not None:
                        file_name = str(file)
                    else:
                        raise cliexceptions.CliValueError(
                            'Name of file is required for load operation.')
                else:
                    load_method = 'Clear'
                    banner_str = None
                    file_name = None

        self._cli.adminaccessconfig().banner(load_method, banner_str, file_name)

    def admin_access_config_ipaccess_allow_all(self):
        """Configure to allow all IP access.

        adminaccessconfig > ipaccess -> allowall

        Example:
        | Admin Access Config Ipaccess Allow All |
        """

        self._cli.adminaccessconfig().ipaccess().allowall()

    def admin_access_config_ipaccess_restricted_new(self, ip=None):
        """Configure to restrict the specified IP.

        adminaccessconfig > ipaccess > restricted > new

        Parameters:
        - `ip`: new ip address in CIDR notation.

        Example:
        | Admin Access Config Ipaccess Restricted New | ip=1.2.3.4 |
        """
        if ip is not None:
            self._cli.adminaccessconfig().ipaccess().restricted().\
            new(ip=str(ip))

    def admin_access_config_ipaccess_restricted_delete(self, ip=None):
        """Remove an existing IP address.

        adminaccessconfig > ipaccess > restricted > delete

        Parameters:
        - `ip`: ip address in CIDR notation to be deleted.

        Example:
        | Admin Access Config Ipaccess Restricted Delete | ip=1.2.3.4 |
        """
        if ip is not None:
            self._cli.adminaccessconfig().ipaccess().restricted().\
            delete(ip=str(ip))

    def admin_access_config_ipaccess_restricted_edit(self, ip_set=None):
        """Modify an existing ip address.

        adminaccessconfig > ipaccess > restricted > edit

        Parameters:
        - `ip_set`: ip addresses of existing ip and new one to replace the
            old address. Both in CIDR notation in specific
            format olp_ip:new_ip.

        Example:
        | Admin Access Config Ipaccess Restricted Edit | ip_set=1.2.3.4:2.3.4.5 |
        """
        if ip_set is not None:
            self._cli.adminaccessconfig().ipaccess().restricted().\
            edit(old_ip=str(ip_set.split(':')[0]),
                 new_ip=str(ip_set.split(':')[1]))

    def admin_access_config_ipaccess_restricted_clear(self):
        """Clear all existing ip addresses.

        adminaccessconfig > ipaccess > restricted > clear

        Example:
        | Admin Access Config Restricted Clear |
        """
        self._cli.adminaccessconfig().ipaccess().restricted().\
            clear()

    def admin_access_config_timeout(self, timeout=30):
        """Set timeout for idle sessions.

        adminaccessconfig > timeout

        Example:
        | Admin Access Config Timeout  5|
        """
        self._cli.adminaccessconfig().timeout(timeout)

    def admin_access_config_how_tos(self, operation=None):
        """Configure How-tos feature , to enable or disable HOW-TOS feature

        adminaccessconfig > HOW-TOS

        *Parameters:*
        - `operation`: Operation to perform.  Either 'enable', or 'disable'

         *Examples:*
        | Admin Access Config How Tos| operation=enable  |
        | Admin Access Config How Tos| operation=disable |
         *Exceptions*:
         If operation value is None it will raise CliValueError
         """
        if operation is not None:
            if operation.lower() == 'enable':
                return self._cli.adminaccessconfig().how_tos().enable()
            if operation.lower() == 'disable':
                return self._cli.adminaccessconfig().how_tos().disable()
        else:
            raise cliexceptions.CliValueError("Operation needs to be either enable/disable")

    def admin_access_config_how_tos_is_enabled(self):
        """To verify the How-Tos feature is enabled

        adminaccessconfig > HOW-TOS

        *Examples:*
        |${status}  | Admin Access Config How Tos Is Enabled |

        *Return:* return value is True or False. It will return true if its enabled else false .
        """
        enabled_string = 'How-Tos feature is currently enabled'
        return enabled_string in self._cli.adminaccessconfig().how_tos().status()

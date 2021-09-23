#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/fipsconfig.py#1 $ 
# $DateTime: 2019/08/14 09:58:47 $ 
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase

class FipsConfig(CliKeywordBase):
    """Change FIPS configuration.
    """

    def get_keyword_names(self):
        return [
            'fips_config',
            'fips_config_is_enabled',
            'fips_check_status',
            'fips_config_outboundacl_new',
            'fips_config_outboundacl_edit',
            'fips_config_outboundacl_delete',
            'fips_config_outboundacl_clear'
        ]

    def fips_config(self, action, always_encrypt='yes', timeout=900):
        """Change current FIPS mode.
        Will pass silently if already disabled/enabled.

        *Warning:*
        - This keyword will restart your appliance if
        current FIPS mode differs from passed 'action'
        value. Then this will wait automatically until
        the appliance reboots and restarts CLI session.
        Do not forget to take care about GUI session
        restart if necessary

        - Care should be taken while changing only the encryption option.
        If Fips is already enabled, should disable it first and then
        re-enable with the required encryption option.

        *Parameters:*
        - `action`: 'enable' to enable and 'disable' to disable FIPS
        - `always_encrypt`: Either 'yes' or 'no'. Default is 'yes'
        Whether to enable encryption to sensitive data in configuration file
        - `timeout`: maximum number of seconds to wait until appliance
        reboots

        *Exceptions:*
        - `ValueError`: if action parameter has incorrect value
        - `ConfigError`: if the system has failed to reboot after
        mode change
        - `TimeoutError`: if the system has failed to close all
        opened connection before reboot

        *Return:*
        Current FIPS status (before the status has been changed with current command).
        Boolean: True - if FIPS was enabled, False - if FIPS was disabled.

        *Examples:*
        | ${was_enabled}= | FIPS Config | Enable |
        | ${was_enabled}= | FIPS Config | Disable |
        | ${was_enabled}= | FIPS Config | Enable | timeout=600 |
        | ${was_enabled}= | FIPS Config | Enable | always_encrypt=no | timeout=600 |
        | ${was_enabled}= | FIPS Config | Enable | always_encrypt=yes | timeout=600 |
        """
        action = str(action.lower())
        if action in ('enable', 'disable'):
            dest_method = getattr(self._cli.fipsconfig(), action)
            res = dest_method(self.dut, self.dut_version, action, always_encrypt, int(timeout))
            self.start_cli_session_if_not_open()
            return res
        else:
            raise ValueError('action should be either "disable" or "enable". Given: %s' % (action,))

    def fips_config_is_enabled(self):
        """Get current FIPS feature status

        *Return:*
        ${True} or ${False} depending on current FIPS feature state

        *Examples:*
        | ${fips_state}= | FIPS Config Is Enabled |
        """
        return self._cli.fipsconfig().is_enabled()

    def fips_check_status(self):
        """Get whether services are fips complaint or not

        *Return:*
        ${True} or ${False} depending on current FIPS complaint or not state

        """
        return self._cli.fipsconfig()._get_fipschk_output()

    def fips_config_outboundacl_new(self, ip):
        """Add new IP in the outbound acl of management port in fipsconfig command
           We can add a new IP address/subnet/hostname.
        *Examples:*
        FIPS Config Outboundacl New  10.10.33.5
        FIPS Config Outboundacl New  10.10.33.5/27
        FIPS Config Outboundacl New  <hostname>
        """
        self._cli.fipsconfig().outboundacl().new(ip=str(ip))

    def fips_config_outboundacl_edit(self, ip_set = None):
        """
        Modify an existing ip address.

        fips_config > OUTBOUNDACL > edit

        Parameters:
        - `ip_set`: ip addresses of existing ip and new one to replace the
            old address. Both in CIDR notation in specific
            format olp_ip:new_ip.
        *Examples:*
        FIPS Config Outboundacl Edit  1.2.3.4:2.3.4.5
        """
        self._cli.fipsconfig().outboundacl().edit(old_ip=str(ip_set.split(':')[0]), new_ip=str(ip_set.split(':')[1]))

    def fips_config_outboundacl_delete(self, ip):
        """Edit IP in the outbound acl of management port in fipsconfig command
           We can add a new IP address/subnet/hostname.
        *Examples:*
        FIPS Config Outboundacl Delete
        """
        self._cli.fipsconfig().outboundacl().delete(ip=str(ip))

    def fips_config_outboundacl_clear(self):
        """Edit IP in the outbound acl of management port in fipsconfig command
           We can add a new IP address/subnet/hostname.
        *Examples:*
        FIPS Config Outboundacl Clear
        """
        self._cli.fipsconfig().outboundacl().clear()

#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/snmpconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class SnmpConfig(CliKeywordBase):
    """Configure Simple Network Management Protocol agent.

       *List of enterprise trap*

       The number, associated with each of the following traps, can be used as
       input to either `traps_to_disable` or `traps_to_enable` parameters below:

        1. CPUUtilizationExceeded
        2. FIPSModeDisableFailure
        3. FIPSModeEnableFailure
        4. RAIDStatusChange
        5. connectivityFailure
        6. fanFailure
        7. highTemperature
        8. keyExpiration
        9. linkUpDown
        10. memoryUtilizationExceeded
        11. powerSupplyStatusChange
        12. updateFailure
        13. upstreamProxyFailure

    """

    def get_keyword_names(self):
        return [
            'snmp_config_setup',
            'snmp_config_is_snmp_enabled',
        ]

    def snmp_config_setup(self, *args):
        """Configures Simple Network Managment Protocol agent.

        Parameters:
        - `enable_snmp`: specify wheter to enable or disable SNMP.  Either
                         'yes' or 'no'.
        - `ip_interface`: specify an interface for SNMP requests.  Either
                          'Management', 'P1', or 'P2'.  Note that 'P1' and
                          'P2' are only available if these interfaces are
                          configured on appliance.
        - `snmpv3_passphrase`: specify SNMPv3 passphrase which must be at least
                               8 characters.
        - `snmp_port`: specify port that SNMP daemon listen on.
        - `snmpv1v2_enabled`: specify whether to service SNMP V1/V2c requests.
                              Either 'yes' or 'no'.
        - `snmpv1v2_community`: specify SNMP V1/V2c community string.
        - `snmpv1v2_permit_via_ipv4`: shall SNMP V2c requests be serviced from
                                    IPv4 addresses or not. Default: yes.
        - `snmpv1v2_network`: specify IPv4 networks that SNMP V1/V2c requests
                              allowed.  Either a string of comma-separate or
                              a list of IP addresses.
        - `snmpv1v2_permit_via_ipv6`: shall SNMP V2c requests be serviced from
                                    IPv6 addresses or not.
        - `snmpv1v2_ipv6_network`: specify IPv6 networks that SNMP V1/V2c requests
                              allowed.  Either a string of comma-separate or
                              a list of IPv6 addresses.
        - `trap_target`: specify trap target.  Either a string of
                         comma-separate or a list of host name or IP addresses.
                         Specify 'None' to disable traps.
        - `trap_community`: specify trap community string.
        - `change_trap_status`: specify whether to change current settings for
                                enterprise trap status.  Either 'yes' or 'no'.
        - `disable_traps`: specify whether to disable any enterprise trap.
                           Either 'yes' or 'no'.
        - `traps_to_disable`: a string of comma-separated number representing
                              enterprise trap to disable if `disable_traps`
                              parameter is set to 'yes'.  Refer to list of
                              enterprise trap listed in `Introduction` for
                              specific number.
        - `enable_traps`: specify whether to enable any enterprise trap.  Either
                           'yes' or 'no'.
        - `traps_to_enable`: a string of comma-separated number representing
                             enterprise trap to enable if `enable_traps`
                             parameter is set to 'yes'.  Refer to list of
                             enterprise trap listed in `Introduction` for
                             specific number.
        - `cpu_util_threshold`: threshold to set when enabling
                                'CPUUtilizationExceeded' trap.
        - `conn_fail_url`: URL to check for when enabling 'connectivityFailure'
                           trap.
        - `mem_util_threshold`: threshold to set when enabling
                                'memoryUtilizationExceeded' trap.
        - `system_location_string`: specify System Location string.
        - `system_contact_string`: specify System Contact string.

        Examples:
        | Snmp Config Setup | enable_snmp=yes | ip_interface=P1 | snmpv3_passphrase=ironport |
        | Snmp Config Setup | enable_snmp=yes | ip_interface=Management | snmpv3_passphrase=ironport |
        | | snmp_port=162 | snmpv1v2_enabled=yes | snmpv1v2_community=snmptesting |
        | | snmpv1v2_network=10.7.2.0/24 | trap_target=127.0.0.1 | trap_community=ironport |
        | | change_trap_status=yes | disable_traps=yes | traps_to_disable=4, 8 |
        | | enable_traps=yes | traps_to_enable=1, 3, 9 | cpu_util_threshold=100 |
        | | conn_fail_url=http://foo.bar | mem_util_threshold=110 | system_location_string=San Bruno |
        | | system_contact_string=foo bar |
        | Snmp Config Setup | enable_snmp=no |
        """
        kwargs = self._convert_to_dict(args)
        if 'change_trap_status' in kwargs and \
            self._process_yes_no(kwargs['change_trap_status']) == 'Y':
            kwargs['change_trap_status'] = ['yes', 'no']
        if 'snmpv3_passphrase' in kwargs:
            kwargs['snmpv3_passphrase_again'] = kwargs['snmpv3_passphrase']
        if 'snmpv3_privacy_passphrase' in kwargs:
            kwargs['snmpv3_privacy_passphrase_again'] = kwargs['snmpv3_privacy_passphrase']
        if 'snmpv3_passphrase_diff_pass' in kwargs:
            kwargs['snmpv3_passphrase_again_diff_pass'] = kwargs['snmpv3_passphrase_diff_pass']
        if 'snmpv3_privacy_passphrase_diff_pass' in kwargs:
            kwargs['snmpv3_privacy_passphrase_again_diff_pass'] = kwargs['snmpv3_privacy_passphrase_diff_pass']
        self._cli.snmpconfig().setup(**kwargs)

    def snmp_config_is_snmp_enabled(self):
        """Checks to see if SNMP is currently enabled.

        Example:
        | ${status}= | Snmp Config Is Snmp Enabled |
        """

        return self._cli.snmpconfig().is_snmp_enabled()

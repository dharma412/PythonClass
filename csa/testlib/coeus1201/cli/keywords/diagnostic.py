#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/diagnostic.py#1 $

from common.cli.clicommon import CliKeywordBase

class Diagnostic(CliKeywordBase):
    """Configure Cisco IronPort system alerts.

    Class designed to provide keywords for Cisco IronPort diagnostic utility
    command.
    """

    def get_keyword_names(self):
        return ['diagnostic_net_start',
                'diagnostic_net_stop',
                'diagnostic_net_status',
                'diagnostic_net_filter',
                'diagnostic_net_interface',
                'diagnostic_net_clear',
                'diagnostic_proxy_snap',
                'diagnostic_proxy_offline',
                'diagnostic_proxy_resume',
                'diagnostic_proxy_cache',
                'diagnostic_reporting_delete_db',
                'diagnostic_reporting_disable',
                'diagnostic_reporting_enable',
                ]

    def diagnostic_net_start(self):
        """Start packet capture

        diagnostic > net > start

        Examples:
        | Diagnostic Net Start |
        """

        self._cli.diagnostic().net().start()

    def diagnostic_net_stop(self):
        """Stop packet capture

        diagnostic > net > stop

        Examples:
        | Diagnostic Net Stop |
        """

        self._cli.diagnostic().net().stop()

    def diagnostic_net_status(self):
        """Status capture

        diagnostic > net > status

        Examples:
        | Diagnostic Net Status |
        """

        self._cli.diagnostic().net().status()

    def diagnostic_net_filter(self, filter=''):
        """Set packet capture filter

        diagnostic > net > filter

        Parameters:
        - `filter`: filter to be used for the packet capture.

        Examples:
        | Diagnostic Net Filter | filter=tcp and port 80 |
        """

        self._cli.diagnostic().net().filter(filter)

    def diagnostic_net_interface(self, interface=''):
        """Set packet capture interface

        diagnostic > net > interface

        Parameters:
        - `interface`: interface to be used for the packet capture. Valid
        entries are: 'M2', 'Management', 'P1', 'P2', 'T1', 'T2'.

        Examples:
        | Diagnostic Net Interface | interface=P1 |
        """

        self._cli.diagnostic().net().interface(interface)

    def diagnostic_net_clear(self, confirm='yes'):
        """Remove previous packet captures

        diagnostic > net > clear

        Parameters:
        - `confirm`: answer for confirmation question. Either 'yes' or 'no'.
        Default 'yes'.

        Examples:
        | Diagnostic Net Clear |
        """

        self._cli.diagnostic().net().clear(self._process_yes_no(confirm))

    def diagnostic_proxy_snap(self):
        """Take a snapshot of the proxy

        diagnostic > proxy > snap

        Example:
        | Diagnostic Proxy Snap |
        """

        self._cli.diagnostic().proxy().snap()

    def diagnostic_proxy_offline(self):
        """Take the proxy offline (via WCCP)

        diagnostic > proxy > offline

        Example:
        | Diagnostic Proxy Offline |
        """

        self._cli.diagnostic().proxy().offline()

    def diagnostic_proxy_resume(self):
        """Resume proxy traffic via (via WCCP)

        diagnostic > proxy > resume

        Example:
        | Diagnostic Proxy Resume |
        """

        self._cli.diagnostic().proxy().resume()

    def diagnostic_proxy_cache(self):
        """Clear proxy cache

        diagnostic > proxy > cache

        Example:
        | Diagnostic Proxy Cache |
        """

        self._cli.diagnostic().proxy().cache()

    def diagnostic_reporting_delete_db(self, confirm='yes'):
        """Reinitialize the reporting database

        diagnostic > reporting > deletedb

        Parameters:
        - `confirm`: answer for confirmation question. Either 'yes' or 'no'.
        Default 'yes'.

        Example:
        | Diagnostic Reporting Delete DB | confirm='no' |
        """

        self._cli.diagnostic().reporting().deletedb(
            self._process_yes_no(confirm))

    def diagnostic_reporting_disable(self):
        """Disable the reporting system

        diagnostic > reporting > disable

        Example:
        | Diagnostic Reporting Disable |
        """

        self._cli.diagnostic().reporting().disable()

    def diagnostic_reporting_enable(self):
        """Enable the reporting system

        diagnostic > reporting > enable

        Example:
        | Diagnostic Reporting Enable |
        """

        self._cli.diagnostic().reporting().enable()

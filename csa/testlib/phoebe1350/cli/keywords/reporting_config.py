#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase

class ReportingConfig(CliKeywordBase):
    """Configuring the Reporting System from CLI

       Cli -> Reporingconfig

       Reportingconfig has a hidden command `mailsetup` which has the options
       - Senderbase
       - Multiplayer
       - Counters
       - Throttling
       - Tld
       - Storage
       - Legacy
    """

    def get_keyword_names(self):
#TODO: The option, Mailsetup->Storage is not finished in ctor.

        return ['reporting_config_setup',
                'reporting_config_mailsetup_senderbase',
                'reporting_config_mailsetup_multiplier',
                'reporting_config_mailsetup_counters',
                'reporting_config_mailsetup_throttling',
                'reporting_config_mailsetup_tld_add',
                'reporting_config_mailsetup_tld_replace',
                'reporting_config_mailsetup_tld_clear',
                'reporting_config_mailsetup_legacy',
               ]

    def reporting_config_setup(self,*args):
        """Used to enable centralized or local reporting for the appliance.

           reportingconfig -> setup

           *Parameter*
           - `enable`:Indicates whether centralized
           reporting should be enabled. By default Local Reporting is enabled
           and when Centralised Reporting is enabled, the other is turned off.
           It takes values Either 'yes' or 'no'.

           *Example*
           | Reporting Config Setup | enable=yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.reportingconfig().setup(**kwargs)

    def reporting_config_mailsetup_senderbase(self,*args):
        """Used to configure SenderBase timeout for the web interface

           reportingconfig -> mailsetup -> Senderbase

           *Parameters*
           - `timeout`:This is the Senderbase timeout used by the web interface
           Value should be an integer between 1 and 20.

           *Example*
           | Reporting Config Mailsetup Senderbase | timeout=15 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.reportingconfig().mailsetup().senderbase(**kwargs)

    def reporting_config_mailsetup_multiplier(self,*args):
        """Used to configure Sender Reputation Multiplier.

           reportingconfig -> mailsetup -> Multiplier

           *Parameter*
           - `multiplier`: This is Sender Reputation Multiplier.
           Value must be an integer from 1 to 10.

           *Example*
           | Reporting Config Mailsetup Multiplier | multipier=9 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.reportingconfig().mailsetup().multiplier(**kwargs)

    def reporting_config_mailsetup_counters(self,*args):
        """Used to choose the level of reporting system limitation.
           It can take the following values:
           | Level Number | Level Name |
           |  1  | Unlimited reporting data |
           |  2  | Minimally limited reporting data |
           |  3  | Moderately limited reporting data |
           |  4  | Severely limited reporting data |
           Default value 1.

           reportingconfig -> mailsetup -> counters

           *Parameter*
           - `level`: It is the level of reporting system limitation
           Choose a value between 1 and 4.

           *Example*
           | Reporting Config Mailsetup Counters | level=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.reportingconfig().mailsetup().counters(**kwargs)

    def reporting_config_mailsetup_throttling(self,*args):
        """Used to Limit unique hosts tracked for rejected connection reporting.
           To reduce the performance impact of reporting on rejected connections,
           the system supports limiting the number of hosts that will be reported
           on to the most active unique IP addresses in each one
           minute period. This command lets you set this maximum value.

           reportingconfig -> mailsetup -> throttling

           *Parameter*
           -`max_unique_hosts`: Maximum number of unique hosts reported on.
           Can be any integer value.

           *Example*
           | Reporting Config MailSetup Throttling | max_unique_hosts=10 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.reportingconfig().mailsetup().throttling(**kwargs)

    def reporting_config_mailsetup_tld_add(self,*args):
        """Used to Add customer specific domains for reporting rollup.
           The reporting system rolls up statistics for IP addresses and hostnames to
           entities called domains, which are determined by a list of top level domains
           (TLD) and second level domains (SLD) provided by IronPort.  For example,
           reporting for mx1.ironport.com and mx2.ironport.com will be reported under
           ironport.com because com is a TLD.
           Some domains get special handling such as co.uk and fed.us.  These SLDs
           contain large networks so in these cases the reporting will be done on
           the domain one level lower in the hostname.
           This command allows the customer to add additional second level domains for
           reporting.  If you add example.com as an SLD you will no longer see
           example.com in the reporting domains list, but instead subdomain.example.com
           will be considered a domain for reporting.
           Changes made using this command are not retroactive.  Data previously
           collected by the reporting system will continue to report domains as they
           were configured at event time.

           reportingconfig -> mailsetup -> tld -> add

           *Parameter*
           -`host_list` - the list of custom top level domains

           *Examples*
           | Reporting Config MailSetup Tld Add | host_list='com' |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.reportingconfig().mailsetup().tld().add(**kwargs)

    def reporting_config_mailsetup_tld_replace(self,*args):
        """Used to replace customer specific domains for reporting rollup.

           reportingconfig -> mailsetup -> tld -> replace

           *Parameter*
           -`host_list` - the list of custom top level domains to be replaced.

           *Example*
           | Reporting Config MailSetup Tld Replace |  host_list='qa'|
        """
        kwargs = self._convert_to_dict(args)
        self._cli.reportingconfig().mailsetup().tld().replace(**kwargs)

    def reporting_config_mailsetup_tld_clear(self,*args):
        """Used to delete customer specific domains for reporting rollup.

           reportingconfig -> mailsetup -> tld -> clear

           *Example*
           | Reporting Config MailSetup Tld Clear |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.reportingconfig().mailsetup().tld().clear(**kwargs)

    def reporting_config_mailsetup_legacy(self,*args):
        """Used to Configure legacy mailflow report
           This command enables additional reporting counters for tracking messages,
           recipients, and data to support a legacy mailflow report.  This mode is
           disabled by default for performance reasons as the majority of customers do not
           access this report.

           reportingconfig -> mailsetup -> legacy

           *Parameter*
           -`enable`: To enable or disable the legacy setup. Either 'yes' or 'no'.

          *Example*
          |  Reporting Config MailSetup Legacy | enable=yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.reportingconfig().mailsetup().legacy(**kwargs)






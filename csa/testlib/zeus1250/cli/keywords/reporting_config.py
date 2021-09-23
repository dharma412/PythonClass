#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/reporting_config.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class ReportingConfig(CliKeywordBase):

    """Keywords for reportingconfig CLI command."""

    def get_keyword_names(self):
        return ['reporting_config_setup',
                'reporting_config_filters',
                'reporting_config_domain_tld_add',
                'reporting_config_domain_tld_replace',
                'reporting_config_domain_tld_clear',
                'reporting_config_domain_hat_reject_info_enable',
                'reporting_config_domain_hat_reject_info_disable',
                'reporting_config_alert_timeout_enable',
                'reporting_config_alert_timeout_disable']

    def reporting_config_setup(self, enable_email=DEFAULT, enable_web=DEFAULT,
        anonymize=DEFAULT):
        """Enable Centralized Reporting services.

        Parameters:
        - `enable_email`: enable Centralized Email Reporting.
        - `enable_web`: enable Centralized Web Reporting.
        - `anonymize`: anonymize usernames in reports.

        Examples:
        | Reporting Config Setup | enable_email=yes | enable_web=no |
        | Reporting Config Setup | enable_web=yes | anonymize=yes |
        | Reporting Config Setup | enable_email=no | enable_web=no |
        """
        config_dict = {
            'enable_email': self._process_yes_no(enable_email),
            'enable_web': self._process_yes_no(enable_web),
            'anonymize': self._process_yes_no(anonymize),
        }

        self._cli.reportingconfig().setup(config_dict)

    def reporting_config_filters(self, groups):
        """Select reporting groups to not record data for.

        Parameters:
        - `groups`: the numbers of the groups.

        Examples:
        | Reporting Config Filters | 1 |
        | Reporting Config Filters | 1,4 |
        """
        self._cli.reportingconfig().filters(groups=groups)

    def reporting_config_domain_tld_add(self, domains):
        """Add entry to SLD list.

        Parameters:
        - `domains`: a string of comma-separated domains to add to SLD list.

        Examples:
        | Reporting Config Domain TLD Add | example.com |
        """
        self._cli.reportingconfig().domain().tld().add(domains)

    def reporting_config_domain_tld_replace(self, domains):
        """Replace SLD list.

        Parameters:
        - `domains`: a string of comma-separated domains to replace SLD list
           with.

        Examples:
        | Reporting Config Domain TLD Replace | example.com, test.com |
        """
        self._cli.reportingconfig().domain().tld().replace(domains)

    def reporting_config_domain_tld_clear(self):
        """Clear SLD list.

        Examples:
        | Reporting Config Domain TLD Clear |
        """
        self._cli.reportingconfig().domain().tld().clear()

    def reporting_config_domain_hat_reject_info_enable(self):
        """Enable inclusion of HAT reject info in domain reports.

        Examples:
        | Reporting Config Domain Hat Reject Info Enable |
        """
        self._cli.reportingconfig().domain().hat_reject_info(include='yes')

    def reporting_config_domain_hat_reject_info_disable(self):
        """Disable inclusion of HAT reject info in domain reports.

        Examples:
        | Reporting Config Domain Hat Reject Info Disable |
        """
        self._cli.reportingconfig().domain().hat_reject_info(include='no')

    def reporting_config_alert_timeout_enable(self, timeout):
        """Enable timeout alerts.

        Parameters:
        - `timeout`: the number of minutes an alert should be sent after.

        Examples:
        | Reporting Config Alert Timeout Enable |
        | Reporting Config Alert Timeout Enable | 180 |
        """
        self._cli.reportingconfig().alert_timeout(enable='yes',
            timeout=timeout)

    def reporting_config_alert_timeout_disable(self):
        """Disable timeout alerts.

        Examples:
        | Reporting Config Alert Timeout Disable |
        """
        self._cli.reportingconfig().alert_timeout(enable='no')


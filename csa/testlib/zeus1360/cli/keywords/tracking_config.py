#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/tracking_config.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class TrackingConfig(CliKeywordBase):

    """Keywords for trackingconfig CLI command."""

    def get_keyword_names(self):
        return ['tracking_config_enable',
                'tracking_config_disable',
                'tracking_config_alert_timeout_enable',
                'tracking_config_alert_timeout_disable']

    def tracking_config_enable(self):
        """Enable Centralized Message Tracking.

        Examples:
        | Tracking Config Enable |
        """
        self._cli.trackingconfig().setup(enable_tracking='yes')

    def tracking_config_disable(self):
        """Disable Centralized Message Tracking.

        Examples:
        | Tracking Config Disable |
        """
        self._cli.trackingconfig().setup(enable_tracking='no')

    def tracking_config_alert_timeout_enable(self, timeout=DEFAULT):
        """Enable timeout alerts.

        Parameters:
        - `timeout`: the number of minutes an alert should be sent after.

        Examples:
        | Tracking Config Alert Timeout Enable |
        | Tracking Config Alert Timeout Enable | 180 |
        """
        self._cli.trackingconfig().alert_timeout(enable='yes', timeout=timeout)

    def tracking_config_alert_timeout_disable(self):
        """Disable timeout alerts.

        Examples:
        | Tracking Config Alert Timeout Disable |
        """
        self._cli.trackingconfig().alert_timeout(enable='no')


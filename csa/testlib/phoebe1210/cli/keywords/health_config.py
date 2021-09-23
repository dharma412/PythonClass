#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/health_config.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase
from sal.containers.yesnodefault import YES, NO, is_yes


class HealthConfig(CliKeywordBase):
    """Configure healthconfig workqueue/cpu/swap settings"""

    def get_keyword_names(self):
        return ['healthconfig_workqueue',
                'healthconfig_cpu',
                'healthconfig_swap',
                ]

    def healthconfig_workqueue(self, *args):
        """Verify/edit workqueue settings

        healthconfig > workqueue

        Parameters:
        - `edit_settings`: Edit threshold and alert settings. YES or NO.
        - `threshold_value`: Threshold(max value) for the workqueue size.
        - `receive_alerts` : YES or NO. Whether to receive an alert if threshold value is crossed.

        | Healthconfig Workqueue | edit_settings=NO |
        | Healthconfig Workqueue | edit_settings=YES |
        | ... | threshold_value=440 |
        | ... | receive_alerts=YES |
        """

        kwargs = self._convert_to_dict(args)
        self._cli.healthconfig().workqueue(**kwargs)

    def healthconfig_cpu(self, *args):
        """Verify/edit cpu settings

        healthconfig > cpu

        Parameters:
        - `edit_settings`: Edit threshold and alert settings. YES or NO.
        - `threshold_value`: Threshold(max value) for the workqueue size.
        - `receive_alerts` : YES or NO. Whether to receive an alert if threshold value is crossed.

        | Healthconfig CPU | edit_settings=NO |
        | Healthconfig CPU | edit_settings=YES |
        | ... | threshold_value=4 |
        | ... | receive_alerts=YES |
        """

        kwargs = self._convert_to_dict(args)
        self._cli.healthconfig().cpu(**kwargs)

    def healthconfig_swap(self, *args):
        """Verify/edit swap settings

        healthconfig > swap

        Parameters:
        - `edit_settings`: Edit threshold and alert settings. YES or NO.
        - `threshold_value`: Threshold(max value) for the workqueue size. Only Positive Value.
        - `receive_alerts` : YES or NO. Whether to receive an alert if threshold value is crossed.

        | Healthconfig SWAP | edit_settings=NO |
        | Healthconfig SWAP | edit_settings=YES |
        | ... | threshold_value=4 |
        | ... | receive_alerts=YES |
        """

        kwargs = self._convert_to_dict(args)
        self._cli.healthconfig().swap(**kwargs)

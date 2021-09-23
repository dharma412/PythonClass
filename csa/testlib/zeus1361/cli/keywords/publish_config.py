#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/publish_config.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase, DEFAULT
from sma.constants import (sma_config_masters,)

masters_map = {
        sma_config_masters.CM77: '7.7',
        sma_config_masters.CM80: '8.0',
        sma_config_masters.CM85: '8.5',
    }

class PublishConfig(CliKeywordBase):
    """Publish Configuration to Configuration Masters"""

    def get_keyword_names(self):
        return ['publish_config',]

    def publish_config(self, config_master, job_name=None, host_list=None):
        """Publish master configuration to a list of hosts

        Parameters:
        - `config_master`: is required and can be one of sma_config_masters
          values.
        - `job_name`: name of the job that will be scheduled. If None, than
          job name will be generated automaticaly.
        - `host_list`: list of the host names or ip addresses for WSA
          appliances to be published. If None, than configuration will be
          published to all hosts assigned to the configuration master.

        Example:
        | Publish Config | ${sma_config_masters.CM77} | job_name=test_job_name | host_list=wsa103.wga |
        | Publish Config | ${sma_config_masters.CM77} |
        | Publish Config | ${sma_config_masters.CM77} | host_list=wsa103.wga |
        """

        if config_master not in masters_map:
            raise ValueError('Configuration master should be from the list {0}'.format(sorted(masters_map.values())))

        self._cli.publishconfig(masters_map[config_master], job_name, host_list)

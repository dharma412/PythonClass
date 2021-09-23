#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/cluster_mode.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class ClusterMode(CliKeywordBase):
    """
    Define the configuration mode for subsequent changes.
    CLI command: clustermode
    """

    def get_keyword_names(self):
        return ['cluster_mode', ]

    def cluster_mode(self, *args):
        """Define the configuration mode for subsequent changes.

        CLI command: clustermode

        *Parameters:*
        - `level`: The configuration mode for subsequent changes.
        One from:
        | 1 | Cluster |
        | 2 | Group |
        | 3 | Machine |
        - `machine_or_group_name`: The group or machine to configure.

        *Return:*
        None

        *Examples:*
        | Cluster Mode | level=group | machine_or_group_name=group1 |
        | Cluster Mode | level=machine | machine_or_group_name=machine.name.qa |
        | Cluster Mode | level=cluster |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.clustermode(**kwargs)

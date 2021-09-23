#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase


class CesClusterMode(CliKeywordBase):
    """
    Define the configuration mode for subsequent changes.
    CLI batch command: clustermode
    """

    def get_keyword_names(self):
        return ['ces_cluster_mode_cluster',
                'ces_cluster_mode_group',
                'ces_cluster_mode_machine',
               ]

    def ces_cluster_mode_cluster(self):
        """Shifts to cluster mode.

        CLI command: clustermode

        *Parameters:*
        None

        *Return:*
        None

        *Examples:*
        | Ces Cluster Mode cluster |
        """
        batch_cmd = 'clustermode cluster'
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]

    def ces_cluster_mode_group(self, group_name):
        """Shifts to given group mode.

        CLI command: clustermode group <group_name>

        *Parameters:*
        - `group_name` : The group to configure
        *Return:*
        None

        *Examples:*
        | Ces Cluster Mode Group | G3|
        """
        batch_cmd = 'clustermode group '+group_name
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]

    def ces_cluster_mode_machine(self, machine_name):
        """Shifts to given machine mode.
        
        CLI command: clustermode machine <machine_name>
        
        *Parameters:*
        - `machine_name` : The machine to configure
        
        *Return:*
        None
        
        *Examples:*
        | Ces Cluster Mode Group | vm30esa0010.ibqa |
        """
        batch_cmd = 'clustermode machine '+machine_name
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]

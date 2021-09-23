#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase


class CesClusterConfig(CliKeywordBase):
    """
    cli -> clusterconfig batch commands

    Provides keywords for clusterconfig batch command which is used to configure
    cluster-related settings.
    """
    def get_keyword_names(self):
        return ['ces_cluster_config_new',
                'ces_cluster_config_remove_machine',
                'ces_cluster_config_add_group',
                'ces_cluster_config_rename_group',
                'ces_cluster_config_set_group',
                'ces_cluster_config_list',
                'ces_cluster_config_disconnect',
                'ces_cluster_config_reconnect',
                'ces_cluster_config_connstatus',
                'ces_cluster_config_join',
               ]

    def ces_cluster_config_new(self, cluster_name):
        """
        Creates a new cluster.  The cluster starts off with no members

        >clusterconfig new <cluster_name> no

        *Parameters*:
        - `cluster_name`: Name of the cluster to be created

        *Examples*:
        | Ces Cluster Config New | cluster01 |
        """
        batch_cmd = 'clusterconfig new '+cluster_name+' no'
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]

    def ces_cluster_config_remove_machine(self, machine):
        """
        Remove a machine from the cluster

        >clusterconfig removemachine <machine>

        *Parameters*:
        - `machine`: Machine to remove from the cluster

        *Examples*:
        | Ces Cluster Config Remove Machine | machine=vm30esa0010.ibqa |
        """
        batch_cmd = 'clusterconfig removemachine '+machine
       
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]

    def ces_cluster_config_add_group(self, group_name):
        """
        Creates a new cluster group.  The group starts off with no members

        >clusterconfig addgroup <group_name>

        *Parameters*:
        - `group`: Name of the group to be created

        *Examples*:
        | Ces Cluster Config Add Group | rf_group |
        """
        batch_cmd = 'clusterconfig addgroup '+group_name
       
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]

    def ces_cluster_config_rename_group(self, old_group, new_group):
        """
        Changes the name of a cluster group

        >clusterconfig renamegroup <old_group> <new_group>

        *Parameters*:
        - `old_group`: Specify the group to rename
        - `new_group`: Specify the new name of the group

        *Examples*:
        | Ces Cluster Config Rename Group | rf_group1 | new_rf_group1 |
        """
        batch_cmd = 'clusterconfig renamegroup '+old_group+' '+new_group
       
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]

    def ces_cluster_config_set_group(self, machine, group_name):
        """
        Sets (or changes) which group a machine is a member of

        >clusterconfig setgroup <machine> <group_name>

        *Parameters*:
        - `machine`: Specify the machine to be moved to a different group
        - `group`: Specify the group that the machine should be a member of

        *Examples*:
        | Ces Cluster Config Set Group | vm30esa0010.ibqa | rf_group |
        """
        batch_cmd = 'clusterconfig setgroup '+machine+' '+group_name
       
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]

    def ces_cluster_config_list(self):
        """
        Display all the machines currently in the cluster and whether they are
        currently administratively disconnected

        > clusterconfig list

        *Examples*:
        | ${Result}= | Ces Cluster Config List |
        """
        batch_cmd = 'clusterconfig list' 
       
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]

    def ces_cluster_config_disconnect(self, machine):
        """
        Temporarily detach a machine from the cluster

        > clusterconfig disconnect <machine>

        *Parameters*:
        - `machine`: Name of the machine to disconnect

        *Examples*:
        | Ces Cluster Config Disconnect | vm30esa0015.ibqa |
        """
        batch_cmd = 'clusterconfig disconnect '+machine
       
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.read_until('[Disconnected]>')
        return [line for line in self._cli._sess.getbuf().split("\n")]

    def ces_cluster_config_reconnect(self, machine):
        """
        This will restore connections with machines that were detached with the
        "disconnect" command

        > clusterconfig reconnect <machine>

        *Parameters*:
        - `machine`: Name of the machine to be reconnected

        *Examples*:
        | Ces Cluster Config Reconnect | vm30esa0015.ibqa |
        """
        batch_cmd = 'clusterconfig reconnect '+machine
       
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]

    def ces_cluster_config_connstatus(self):
        """
        Display the status of connections between all the machines currently in
        the cluster

        > clusterconfig connstatus

        *Examples*:
        | ${Result}= | Ces Cluster Config Connstatus |
        """
        batch_cmd = 'clusterconfig connstatus' 
       
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]

    def ces_cluster_config_join(self, remote_cluster_ip, ssh_admin_name, ssh_admin_password, add_to_group):
        """
        Joins the machine to alreadt existing cluster 

        >clusterconfig join <remote_cluster_ip> <ssh_admin_name> <ssh_admin_password> <add_to_group>

        *Parameters*:
        - `remote_cluster_ip`: Specify the the IP address of another machine
          in the cluster
        - `ssh_admin_name`: Name of an administrator present on the remote
          machine
        - `ssh_admin_password`: The password of the user.  This should not be
          specified
        - `add_to_group`: Specify the group in the cluster name provided to
          which the machine has to be placed in     `
        - `group`: Name of the group to be created

        *Examples*:
        | Ces Cluster Config Join | 10.10.21.32 | admin | Cisco12$ | G3
        """
        batch_cmd = 'clusterconfig join '+remote_cluster_ip+' '+ssh_admin_name+' '+ssh_admin_password+' '+add_to_group
       
        self._cli._sess.writeln(batch_cmd)
        self._cli._sess.expect('Is this a valid key for this host')
        self._cli._sess.writeln('Y')
        self._cli._sess.wait_for_prompt()
        return [line for line in self._cli._sess.getbuf().split("\n")]


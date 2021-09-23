#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/cluster_config.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase, DEFAULT
from sal.containers.yesnodefault import YES, NO
import traceback

NO_DEFAULT = None

class ClusterConfig(CliKeywordBase):
    """
    cli -> clusterconfig

    Provides keywords for clusterconfig command which is used to configure
    cluster-related settings.
    """
    default_group_name = 'Main_Group'

    def get_keyword_names(self):
        return ['cluster_config_setup',
                'cluster_config_add_group',
                'cluster_config_set_group',
                'cluster_config_rename_group',
                'cluster_config_delete_group',
                'cluster_config_remove_machine',
                'cluster_config_set_name',
                'cluster_config_list',
                'cluster_config_disconnect',
                'cluster_config_reconnect',
                'cluster_config_connstatus',
               ]

    def cluster_config_setup(self, *args):
        """
        Setup the machine in cluster mode. If the machine is not part of a
        cluster, this will give you the option of joining a cluster or creating
        a new cluster or remain as a standalone one.

        cli -> clusterconfig

        *Parameters*:
        - `changes_pending_continue_ynd`: Pending changes in standalone mode
          will be lost while joining a cluster. Either 'yes' or 'no'
        - `cluster_action`: Specify the action to be done.
          Either 'standalone' or 'create' or 'ssh_join' or 'ccs_join'
        - `cluster_name`: Name of the new cluster. This machine will be a
          member of this cluster and a member of a default cluster group called
          called "Main Group"
        - `ccs_interface`: Specify the interface on which to enable the Cluster
          Communication Service
        - `ccs_port`: Specify the port on which to enable the Cluster
          Communication Service
        - `remote_cluster_ip`: Specify the the IP address of another machine
          in the cluster
        - `remote_cluster_port`: Specify the remote port to connect to.
          This must be the normal admin ssh port, not the CCS port
        - `ssh_admin_name`: Name of an administrator present on the remote
          machine
        - `ssh_admin_password`: The password of the user.  This should not be
          specified if joining over CCS
        - `is_valid_host_key_ynd`: Valid public key for this host.
          Either 'yes' or 'no'
        - `add_to_group`: Specify the group in the cluster name provided to
          which the machine has to be placed in
        - `continue_on_join_error_ynd`: Continue on join. Either 'yes' or 'no'
        - `communication_method`: Specify how all machines in the cluster
          should communicate with each other. Either 'hostname' or 'IP address'
        - `communication_ip`: Specify the IP address other machines should use
          to communicate with this machine
        - `communication_ip_manual`: Specify an IP address manually
        - `communication_port_manual`: Specify the port for the IP address
          provided manually
        - `switch_mode_ynd`: Restricted command to machine or cluster mode.
          Switch to cluster or machine mode respectively. Either 'yes' or 'no'
        - `machine_or_group_name`: Machine or group name to be selected if
          multiple machine or group names respectively are present when
          switching between machine or group levels
        - `reconnect_ynd`: Machine is disconnected from cluster.
          Reconnect to the cluster. Either 'yes' or 'no'

        *Examples*:
        | Cluster Config Setup | cluster_action=create | cluster_name=cluster1 |
        | Cluster Config Setup | cluster_action=ssh_join |
        | ... | remote_cluster_ip=10.76.68.113 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.clusterconfig(**kwargs)

    def cluster_config_add_group(self, group):
        """
        Creates a new cluster group.  The group starts off with no members

        clusterconfig -> addgroup

        *Parameters*:
        - `group`: Name of the group to be created

        *Examples*:
        | Cluster Config Add Group | rf_group |
        """
        self._cli.clusterconfig().addgroup(group)

    def cluster_config_set_group(self, machine, group=default_group_name):
        """
        Sets (or changes) which group a machine is a member of

        clusterconfig -> setgroup

        *Parameters*:
        - `machine`: Specify the machine to be moved to a different group
        - `group`: Specify the group that the machine should be a member of

        *Examples*:
        | Cluster Config Set Group | vm30esa0010.ibqa | rf_group |
        """
        self._cli.clusterconfig().setgroup(machine, group_name=group)

    def cluster_config_rename_group(self, old_group, new_group):
        """
        Changes the name of a cluster group

        clusterconfig -> renamegroup

        *Parameters*:
        - `old_group`: Specify the group to rename
        - `new_group`: Specify the new name of the group

        *Examples*:
        | Cluster Config Rename Group | rf_group1 | new_rf_group1 |
        """
        self._cli.clusterconfig().renamegroup(old_group, new_group)

    def cluster_config_delete_group(self, group, dest_group=None):
        """
        Removes a cluster group

        clusterconfig -> deletegroup

        *Parameters*:
        - `group`: Name of the cluster group to remove
        - `dest_group`: The cluster group to put machines of the old group into.
          This is not necessary if there are no machines in the group

        *Examples*:
        | Cluster Config Delete Group | rf_group | dest_group=Main_Group |
        """
        self._cli.clusterconfig().\
              deletegroup(group, dest_group_name=dest_group)

    def cluster_config_remove_machine(self, machine=DEFAULT, confirm=YES):
        """
        Remove a machine from the cluster

        clusterconfig -> removemachine

        *Parameters*:
        - `machine`: Machine to remove from the cluster
        - `confirm`: Confirm to remove. Either 'yes' or 'no'. Default 'yes'

        *Examples*:
        | Cluster Config Remove Machine | machine=vm30esa0010.ibqa |
        """
        self._cli.clusterconfig().\
              removemachine(machine_name=machine, confirm_continue=confirm)

    def cluster_config_set_name(self, cluster_name):
        """
        Changes the name of the cluster to the given name

        clusterconfig -> setname

        *Parameters*:
        - `cluster_name`: New name for this cluster

        *Examples*:
        | Cluster Config Set Name | newcluster |
        """
        self._cli.clusterconfig().setname(cluster_name)

    def cluster_config_list(self):
        """
        Display all the machines currently in the cluster and whether they are
        currently administratively disconnected

        clusterconfig -> list

        *Examples*:
        | ${Result}= | Cluster Config List |
        """
        return self._cli.clusterconfig().list()

    def cluster_config_disconnect(self, machine, confirm=YES):
        """
        Temporarily detach a machine from the cluster

        clusterconfig -> disconnect

        *Parameters*:
        - `machine`: Name of the machine to disconnect
        - `confirm`: Confirm to disconnect. Either 'yes' or 'no'. Default 'yes'

        *Examples*:
        | Cluster Config Disconnect | vm30esa0015.ibqa |
        """
        self._cli.clusterconfig().\
              disconnect(machine, confirm_disconnect=confirm)

    def cluster_config_reconnect(self, machine, confirm=YES):
        """
        This will restore connections with machines that were detached with the
        "disconnect" command

        clusterconfig -> reconnect

        *Parameters*:
        - `machine`: Name of the machine to be reconnected
        - `confirm`: Confirm to reconnect. Either 'yes' or 'no'. Default 'yes'

        *Examples*:
        | Cluster Config Reconnect | vm30esa0015.ibqa |
        """
        self._cli.clusterconfig().\
              reconnect(machine, confirm_reconnect=confirm)

    def cluster_config_connstatus(self):
        """
        Display the status of connections between all the machines currently in
        the cluster

        clusterconfig -> connstatus

        *Examples*:
        | ${Result}= | Cluster Config Connstatus |
        """
        return self._cli.clusterconfig().connstatus()

    def cluster_config_route(self):
        # TBD
        raise NotImplementedError()

    def cluster_config_prejoin(self):
        # TBD
        raise NotImplementedError()





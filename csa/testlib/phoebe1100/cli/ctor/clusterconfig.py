#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/clusterconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import re
import socket

import clictorbase
from sal.containers.yesnodefault import YES, NO
from sal.exceptions import ConfigError, TimeoutError

DEFAULT = clictorbase.DEFAULT
NO_DEFAULT = clictorbase.NO_DEFAULT
REQUIRED = clictorbase.REQUIRED


class clusterconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1
    # clusterconfig on join creats a default group called Main_Group
    default_group_name = 'Main_Group'

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

        # errors that can appear in __call__()
        __call__clusterconfig_error_strings = (
            'clusterconfig command requires a feature key',
            'ailed to open clustercomm key',
            'ailed to commit new cluster',
            'nly the "admin" user can join a cluster',
            'port is already in use',
            'ailed to join the cluster',
            'ould not connect to cluster: Unexpected EOF',
            # 'Could not connect to cluster:'
            'possible that there was an error in the',
            # does not match the cluster version
            'annot join the cluster as the machine version ',
            'model of the remote server is '  # not compatible with cluster
            'uthentication failure',
            'WARNING:  The host key',  # for %s appears to have changed.'
            'has not yet resynchronized with the cluster after',  # upgrading
            'machine has not been clustered'  # Commit any clustering changes

            # DELETEGROUP: Since there is only 1 group defined, you cannot
            # delete it because there must be at least 1 group in the cluster
            'there must be at least 1 group in the cluster',
        )
        err_dict = {}
        for err_str in __call__clusterconfig_error_strings:
            err_dict[(err_str, clictorbase.EXACT)] = clictorbase.IafCliError

        self._set_local_err_dict(err_dict)

    def __call__(self,
                 # standalone questions:
                 changes_pending_continue_ynd=YES,
                 cluster_action=DEFAULT,  # create,ssh_join,ccs_join,standalone
                 # create cluster questions
                 cluster_name=NO_DEFAULT,
                 # join cluster (over ssh or ccs) questions
                 ccs_interface=DEFAULT,
                 ccs_port=DEFAULT,
                 remote_cluster_ip=NO_DEFAULT,
                 remote_cluster_port=DEFAULT,
                 ssh_admin_name='admin',
                 ssh_admin_password='ironport',  # non-ccs
                 is_valid_host_key_ynd=YES,
                 add_to_group=NO_DEFAULT,  # group name. Input List
                 continue_on_join_error_ynd=YES,
                 communication_method=DEFAULT,
                 communication_ip=NO_DEFAULT,
                 communication_ip_manual=NO_DEFAULT,
                 communication_port_manual=DEFAULT,
                 pre_shared_keys=NO,

                 # level restriction questions
                 switch_mode_ynd=YES,
                 machine_or_group_name=NO_DEFAULT,
                 # disconnected
                 reconnect_ynd=YES,
                 ):
        # params:
        #   - cluster_action: 'create', 'ssh_join' or 'ccs_join'

        self._writeln('clusterconfig')

        sentinel = 'Choose the operation'
        search = ('pending changes that may be lost', 'create a cluster?',
                  sentinel, self._sub_prompt, 'Would you like to switch')
        idx = self._query(*search, timeout=60)
        while idx == len(search) - 1:
            # Switching cluster mode and continue
            self._writeln('Y')
            idx = self._query(*search, timeout=60)
        text = self._get_last_matched_text().lower()

        # If you see the 'pending...' or 'create...' string it means the MGA
        # is in standalone mode.
        if idx in (0, 1):  # standalone questions (ie. no clustering enabled)
            if idx == 0:
                changes_pending_continue_ynd = YES
                self._query_response(changes_pending_continue_ynd)

            # cluster_action can be: create, ssh, ccs, standalone
            if cluster_action.lower().find('standalone') >= 0 \
                    or str(cluster_action) == '1':
                self._query_select_list_item(cluster_action)
                self._wait_for_prompt()

                return None  # back to main prompt

            elif cluster_action.lower().find('create') >= 0 \
                    or str(cluster_action) == '2':
                self._query_select_list_item(cluster_action)
                self._query_response(cluster_name)
                self._query_select_list_item(communication_method)

                if self._query(self._sub_prompt, 'What IP address should', \
                               timeout=60) == 1:
                    self._query_select_list_item(communication_ip)

                    if self._query(self._sub_prompt, 'Enter the IP address',
                                   timeout=60) == 1:
                        self._query_response(communication_ip_manual)
                        self._query_response(communication_port_manual)

                self._writeln()
                self._wait_for_prompt()
                self._restart()

                # RETURN NONE ON CREATE!!
                return None
            else:  # must be join-ssh or join-ccs
                if cluster_action.lower().find('ssh_join') >= 0 \
                        or str(cluster_action) == '3':
                    ccs_enable_bool = False
                    cluster_action = 'SSH'
                elif cluster_action.lower().find('ccs_join') >= 0 \
                        or str(cluster_action) == '4':
                    ccs_enable_bool = True
                    cluster_action = 'CCS'
                else:
                    raise ConfigError, 'Must specify standalone, create, ' \
                                       'ssh_join or ccs_join instead of: %s' % cluster_action

                self._query_select_list_item(cluster_action)

                # join cluster (over ssh or ccs) questions
                if ccs_enable_bool:
                    self._query_select_list_item(ccs_interface)
                    self._query_response(ccs_port)
                else:
                    self._query_response(NO)  # enable ccs? answer NO

                # convert to IP if it's a hostname
                remote_cluster_ip = socket.gethostbyname(remote_cluster_ip)
                self._query_response(remote_cluster_ip)
                self._query_response(remote_cluster_port)
                self._query_response(pre_shared_keys)

                if not ccs_enable_bool:  # remote ssh password
                    self._query_response(ssh_admin_name)
                    self._query('Enter passphrase', timeout=60)
                    self._writeln(ssh_admin_password)

                # 'sentinel' marks the end of this question/answer sequence.
                # And that cluster-join  was successful.
                sentinel = 'cluster takes effect immediately'
                self._query(sentinel, self._sub_prompt, timeout=60)
                text = self._get_last_matched_text()

                if text.lower().find('Is this a valid key'.lower()) >= 0:
                    self._writeln(is_valid_host_key_ynd)
                    self._query(sentinel, self._sub_prompt, timeout=60)
                    text = self._get_last_matched_text()

                if text.lower().find('Choose the group'.lower()) >= 0:
                    self._select_list_item(add_to_group, text)
                    self._query(sentinel, self._sub_prompt, timeout=60)
                    text = self._get_last_matched_text()

                if text.lower().find('Do you wish to continue'.lower()) >= 0:
                    self._writeln(continue_on_join_error_ynd)
                    self._query(sentinel, self._sub_prompt, timeout=60)
                    text = self._get_last_matched_text()

                # if cluster join is ok we see message in 'sentinel'
                assert text.lower().find(sentinel) >= 0, \
                    'no sentinel(%s) found' % sentinel

                sentinel = 'Choose the operation'
                self._query(sentinel, self._sub_prompt, timeout=60)
                text = self._get_last_matched_text().lower()

                self._to_the_top(self.newlines)

                return None  # RETURN NONE ON JOIN!!

        else:  # idx == 2 or 3
            # not in standalone mode
            if cluster_action != DEFAULT:
                raise ConfigError, 'MGA not in standalone mode. ' \
                                   'cluster_action can only be used in standalone mode.'

        # level restriction questions
        if text.find('command is restricted'.lower()) >= 0:
            self._writeln(switch_mode_ynd)
            if not switch_mode_ynd:
                self._wait_for_prompt()
                return None  # back to main prompt
            self._query(sentinel, self._sub_prompt)
            text = self._get_last_matched_text().lower()

            # If multiple machines in new machine level
            # must select a machine. Similarly, must select
            # group when switching to a group level with
            # multiple groups. If only one 1 machine or
            # 1 group then no question is asked (automatically
            # defaults to that machine or group).
            if text.find('Choose the group'.lower()) >= 0 \
                    or text.find('Choose a machine'.lower()) >= 0:
                machine_or_group_name = '1'  # #TODO
                self._writeln(machine_or_group_name)
                self._query(sentinel, self._sub_prompt)
                text = self._get_last_matched_text().lower()

        # disconnected
        if text.find('is currently disconnected') >= 0:
            self._writeln(reconnect_ynd)
            self._query(sentinel, self._sub_prompt)
            text = self._get_last_matched_text().lower()
        assert text.lower().find(sentinel.lower()) >= 0
        return self

    def addgroup(self, group_name):
        self._query_response('ADDGROUP')
        self._query_response(group_name)
        self._to_the_top(self.newlines)

    def setgroup(self, machine_name, group_name=default_group_name):
        self._query_response('SETGROUP')
        self._query_select_list_item(machine_name)
        self._query_select_list_item(group_name)
        self._to_the_top(self.newlines)

    def renamegroup(self, old_group_name, new_group_name):
        self._query_response('RENAMEGROUP')
        self._query_select_list_item(old_group_name)
        self._query_response(new_group_name)
        self._to_the_top(self.newlines)

    def deletegroup(self, group_name, dest_group_name=None):
        self._query_response('DELETEGROUP')
        self._query_select_list_item(group_name)
        if dest_group_name:
            # Choose the group that machines in %s should be moved to
            self._query_select_list_item(dest_group_name)
        self._to_the_top(self.newlines)
        # ('Choose which group you wish to remove.') ##TODO:
        # ('Choose the group that machines in %s should be moved to.')
        # _print(_('Group %s removed.') % groupname)

    def removemachine(self, machine_name=DEFAULT, confirm_continue=YES):
        self._query_response('REMOVEMACHINE')
        self._query_select_list_item(machine_name)
        self._query_response(confirm_continue)
        self._restart(90)

    def setname(self, cluster_name):
        self._query_response('SETNAME')
        self._query_response(cluster_name)
        self._to_the_top(self.newlines)

    def list(self):  # #TODO:HANDLE PAGINATION
        self._query_response('LIST')
        raw = None
        try:
            raw = self._read_until('Choose the operation')
        finally:
            # return to the CLI prompt
            self._to_the_top(self.newlines)
        return raw

    def route(self):
        return clusterconfigRoute(self._sess)

    def disconnect(self, machine_name, confirm_disconnect=YES):
        self._query_response('DISCONNECT')
        self._query_select_list_item(machine_name)
        self._query_response(confirm_disconnect)
        self._to_the_top(self.newlines)

    def reconnect(self, machine_name, confirm_reconnect=YES):
        self._query_response('RECONNECT')
        self._query_select_list_item(machine_name)
        self._query_response(confirm_reconnect)
        self._to_the_top(self.newlines)

    def prepjoin(self):
        return clusterconfigPrepJoin(self._sess)

    def connstatus(self):
        self._query_response('CONNSTATUS')
        raw = None
        try:
            raw = self._read_until('Choose the operation')
        finally:
            # return to the CLI prompt
            self._to_the_top(self.newlines)
        return raw


class clusterconfigPrepJoin(clictorbase.IafCliConfiguratorBase):  # #TODO
    def new(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class clusterconfigRoute(clictorbase.IafCliConfiguratorBase):  # #TODO
    def list(self):
        raise NotImplementedError

    def status(self):
        raise NotImplementedError

    def test(self):
        raise NotImplementedError

    def new(self):
        raise NotImplementedError

    def edit(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


if __name__ == '__main__':
    import sys

    # standalone:
    # 1. standalone
    # 2. create cluster
    # 3. join cluster ssh
    # 4. join cluster ccs

    # clustered (and standalone)
    # restricted mode: switch
    # restricted mode: no switch
    # disconnected: reconnect ok

    sess = clictorbase.get_sess()
    cc = clusterconfig(sess)

    print '-------------------------------------------------------------'
    print 'CLUSTER MGA IN STANDALONE MODE'
    kwargs = {
        'cluster_action': 'standalone',
    }
    cc(**kwargs)

    print '-------------------------------------------------------------'
    print 'CREATE CLUSTER NAMED CLUSTER1'
    kwargs = {
        'cluster_action': 'create',
        'cluster_name': 'cluster1',
    }
    cc(**kwargs)
    cc().removemachine()

    # Get 2nd mga from stdin
    print 'Enter hostname of a second MGA that already has clustering enabled.'
    print 'Press Enter to Quit'
    print '> ',
    hostname = raw_input().strip()
    if hostname == '':
        print 'Exiting...'
        sys.exit(0)

    remote_cluster_ip = socket.gethostbyname(hostname)

    print '-------------------------------------------------------------'
    print 'CONNECT TO REMOTE CLUSTER USING SSH'
    kwargs = {
        'cluster_action': 'ssh_join',
        'remote_cluster_ip': remote_cluster_ip,
        'remote_cluster_port': '22',  # optional arg
        'ssh_admin_password': 'ironport',
    }
    cc(**kwargs)
    cc().removemachine()

    print '-------------------------------------------------------------'
    print 'CONNECT TO REMOTE CLUSTER USING CCS'
    kwargs = {
        'cluster_action': 'ccs_join',
        'ccs_interface': 'Management',  # optional arg
        'ccs_port': '2222',  # optional arg
        'remote_cluster_ip': remote_cluster_ip,
        'remote_cluster_port': '22',  # optional arg
        'ssh_admin_password': 'ironport',
    }
    cc(**kwargs)
    cc().removemachine()

    print '-------------------------------------------------------------'
    print 'CREATE CLUSTER GROUP; SET GROUPNAME; RENAME GROUPNAME'
    kwargs = {
        'cluster_action': 'create',
        'cluster_name': 'cluster1',
    }
    group_name = 'group_name'
    cc(**kwargs).addgroup(group_name)
    machine_name = 'emily.qa'
    cluster_name = 'new_cluster_name'
    cc().setname(cluster_name)
    cc().setgroup(machine_name, group_name=clusterconfig.default_group_name)
    old_group_name = group_name
    new_group_name = 'new_group_name'
    cc().renamegroup(old_group_name, new_group_name)

    print '-------------------------------------------------------------'
    print 'DISCONNECT AND RECONNECT'
    cc().disconnect(machine_name)
    cc().reconnect(machine_name)

    print '-------------------------------------------------------------'
    print 'LIST AND CONNSTATUS'
    cc().list()
    cc().connstatus()

    # cc().route()
    # cc().prepjoin()

    print '-------------------------------------------------------------'
    print 'DELETE GROUP'
    dest_group_name = ''
    cc().deletegroup(new_group_name, dest_group_name)
    cc().removemachine(machine_name)

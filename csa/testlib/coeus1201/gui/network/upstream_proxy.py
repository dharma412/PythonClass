#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/upstream_proxy.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

load_balancing_dict = {
    'failover': "label=None (Failover)",
    'fewest': "label=Fewest Connections",
    'hash': "label=Hash Based",
    'least': "label=Least Recently Used",
    'round': "label=Round Robin"
}

failure_handling_dict = {
    'connect': "direct_connect",
    'drop': "drop_requests"
}

NAME_LINK = lambda row: "xpath=//table[@class=\'cols\']//tr[%s]//td[1]/a" % row
SEVER_ADDRESS_FIELD = lambda index: "proxies[%s][host]" % index
PORT_FIELD = lambda index: "proxies[%s][port]" % index
RECONNECTION_ATTEMPTS_FIELD = lambda index: "proxies[%s][reconnect_count]" \
                                            % index
GROUP_DELETE_ICON = lambda row: "xpath=//table[@class=\'cols\']//tr[%s]" \
                                "//td[4]/img" % row
SERVER_DELETE_ICON = lambda index: "xpath=//tr[@id='proxies_row%d']/td[4]" \
                                   "/img" % index

class UpstreamProxy(GuiCommon):

    """GUI configurator for 'Network -> Upstream Proxy' page.
    """

    def get_keyword_names(self):
        return ['upstream_proxy_add_group',
                'upstream_proxy_get_list',
                'upstream_proxy_edit_servers',
                'upstream_proxy_delete_group',
                'upstream_proxy_edit_group_settings',
                ]

    def _open_page(self):
        """Go to ' Network -> Upstream Proxy'"""
        self._navigate_to('Network', 'Upstream Proxy')

    def _click_add_group_button(self):

        add_group_button = "AddGroup"
        self.click_button(add_group_button)

    def _delete_group(self, name):

        confirm_delete_button = "//button[@type=\'button\']"
        name = self._convert_to_tuple(name)
        for grp in name:
            group_row = self._get_group_row_index(grp)
            if group_row is None:
                raise guiexceptions.GuiValueError, ('"%s" proxy group does '
                                                    'not exist' % grp)
            self.click_element(GROUP_DELETE_ICON(group_row), "don't wait")
            self.click_button(confirm_delete_button)

    def _click_edit_group_link(self, name):
        group_row = self._get_group_row_index(name)
        if group_row is None:
            raise guiexceptions.GuiValueError, ('"%s" proxy group does not '
                                                'exist' % name)
        self.click_link(NAME_LINK(group_row))

    def _get_group_row_index(self, name):

        group_table = "//table[@class=\'cols\']"
        number_of_rows = int(self.get_matching_xpath_count('%s//tr' %
                             group_table))
        for i in xrange(2, number_of_rows + 1):
            group_name = self.get_text('%s//tr[%s]//td[1]' %\
                          (group_table, i)).split(' \n')[0]
            if group_name == name:
                return i
        return None

    def _get_number_of_configured_server(self):
        proxy_server_table = '//table[@id="proxies"]//tbody[2]//tr'

        num_server =  int(self.get_matching_xpath_count(proxy_server_table))
        if num_server == 1 and not self.get_value(SEVER_ADDRESS_FIELD(0)):
        # There is alway one entry in the 'Proxy Servers:' table.  Need
        # to check to see if it is an empty entry or a defined entry.  If
        # 'Server Address' field of this first entry is empty, number of
        # configured server is 0.
                num_server = 0
        return num_server

    def _fill_in_name(self, name):

        group_name_field = "group_name"
        if name is not None:
            self.input_text(group_name_field, name)

    def _fill_in_server_info(self, servers, starting_entry=0):

        # For adding new group, "starting_entry" will default to 0 to indicate
        # the very first entry for server.  For editing server of existing
        # group, all current configured proxy server will be deleted first.
        # And "starting_entry" will be the entry of the last sever get deleted.
        add_row_button = "proxies_domtable_AddRow"
        servers = self._convert_to_tuple(servers)
        for i, _server in enumerate(servers):
            if _server.find('#') > -1:
                server = _server.split('#')
            else:
                server = _server.split(':')
            if len(server) != 3:
                raise ValueError('Invalid value for Server ' + _server)
            if starting_entry:
                entry = i + (starting_entry - 1)
            else:
                entry = i + starting_entry
            self.input_text(SEVER_ADDRESS_FIELD(entry),
                            server[0])
            self.input_text(PORT_FIELD(entry), server[1])
            self.input_text(RECONNECTION_ATTEMPTS_FIELD(entry),
                            server[2])
            if (i + 1) < len(servers):
                self.click_button(add_row_button, "don't wait")

    def _delete_all_server(self):

        num_server = self._get_number_of_configured_server()
        for i in range(num_server):
            self.click_element(SERVER_DELETE_ICON(i), "don't wait")
        # return number of server deleted in case this is part of
        # edit_group_server() call.  This will give the initial starting entry
        # for adding new server..
        return num_server

    def _select_load_balancing(self, load_balancing):

        load_balancing_option_button = "load_balancing"
        if self._get_number_of_configured_server() < 2 and \
            load_balancing is not None:
            raise guiexceptions.GuiValueError('Load balancing required at '
                'least 2 configured upstream proxies')
        if load_balancing is not None:
            self.select_from_list(load_balancing_option_button,
                                  load_balancing_dict[load_balancing.lower()])

    def _configure_failure_handling(self, failure_handling):

        if failure_handling is not None:
            self._click_radio_button(failure_handling_dict[failure_handling])

    def upstream_proxy_add_group(self,
                                 name,
                                 servers,
                                 load_balancing=None,
                                 failure_handling=None):

        """ Adds new upstream proxy group.

        Parameters:
           - `name`: name of proxy group.
           - `servers`: a string of comma separated or a list of the
                        following:
                        <proxy address>#<port>#<reconnection attempts>
                Note: format with separating ':" is deprecated,
                but works for ipv4 for backward compatibility
                        <proxy address>:<port>:<reconnection attempts>
           - `load_balancing`: type of load balancing if group has multiple
                               proxy servers.  Either 'none', 'fewest',
                               'hash', 'least' or 'round'.
           - `failure_handling`: how to handle requests if all proxies in
                                 this group fail.  Either 'connect' or 'drop'.

        Examples:
        | Upstream Proxy Add Group | myGrp1 | 1.2.3.4#3129#4 | failure_handling=drop |
        | Upstream Proxy Add Group | myGrp2 | 5.6.7.8#3129#4, 9.10.11.12#3130#6 | load_balancing=round | failure_handling=drop |
        """

        self._open_page()
        self._click_add_group_button()
        self._fill_in_name(name)
        self._fill_in_server_info(servers)
        self._select_load_balancing(load_balancing)
        self._configure_failure_handling(failure_handling)
        self._click_submit_button()

    def upstream_proxy_get_list(self):

        """ Gets the list of upsteam proxies

        Parameters:
        None

        Exceptions:
        None

        Examples:
        | ${result} | Upstream Proxy Get List |
        """
        ENTRY_ENTITIES = lambda row, col:\
                    '//table[@class=\'cols\']/tbody/tr[%s]/td[%d]' % (str(row), col)

        self._open_page()
        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(ENTRY_ENTITIES('*', 1))) + 2
        for row in xrange(2, num_of_entries):
            name = self.get_text(ENTRY_ENTITIES(row, 1))
            proxies = self.get_text(ENTRY_ENTITIES(row, 2))
            load_balancing = self.get_text(ENTRY_ENTITIES(row, 3))
            entries[name] = [proxies, load_balancing]
        return entries

    def upstream_proxy_edit_servers(self,
                                    name,
                                    servers):

        """ Edits current configured upstream proxy servers for the specified
            proxy group.

        Parameters:
           - `name`: name of proxy group to be edited.
           - `servers`: a string of comma separated or a list of the
                        following:
                        <proxy address>#<port>#<reconnection attempts>.
                Note: format with separating ':" is deprecated,
                but works for ipv4 for backward compatibility
                        <proxy address>:<port>:<reconnection attempts>
                        Note that all currently configured upstream proxy
                        servers will be replaced by the newly specified servers.

        Examples:
        | Upstream Proxy Edit Servers | myGrp2 | 10.20.30.40#3135#12 |
        | Upstream Proxy Edit Servers | myGrp4 | 5.6.7.8#3129#4, 9.10.11.12#3130#6 |
        """

        self._open_page()
        self._click_edit_group_link(name)
        num_of_deleted_server = self._delete_all_server()
        self._fill_in_server_info(servers, num_of_deleted_server)
        self._click_submit_button()

    def upstream_proxy_delete_group(self, name):
        """ Deletes specified list of upstream proxy group.

        Parameters:
           - `name`: a string of comma separate or a list of group to
                     be deleted.

        Examples:
        | Upstream Proxy Delete Group | myGrp2 |
        | Upstream Proxy Delete Group | myGrp1, myGrp2, myGrp3 |
        """

        self._open_page()
        self._delete_group(name)

    def upstream_proxy_edit_group_settings(self,
                                           name,
                                           load_balancing=None,
                                           failure_handling=None):

        """ Edits existing settings for the specified upstream proxy group.

        :Parameters:
            - `name`: name of proxy group to be edited.
            - `load_balancing`: type of load balancing if group has multiple
                                proxy servers.  Either 'failover', 'fewest',
                                'hash', 'least' or 'round'.
            - `failure_handling`: how to handle requests if all proxies in
                                  this group fail.  Either 'connect' or 'drop'.
                                  Defaulted to 'connect'.

        Examples:
        | Upstream Edit Group Settings | myGrp1 | load_balancing=round | failure_handling=connect |
        | Upstream Edit Group Settings | myGrp2 | load_balancing=hash | failure_handling=drop |
        """

        self._open_page()
        self._click_edit_group_link(name)
        self._select_load_balancing(load_balancing)
        self._configure_failure_handling(failure_handling)
        self._click_submit_button()

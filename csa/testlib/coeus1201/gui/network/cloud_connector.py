#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/cloud_connector.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $
import time

from common.gui.guicommon import GuiCommon
from common.gui import guiexceptions

class CloudConnector(GuiCommon):

    """GUI configurator for 'Network -> Cloud Connector' page.
    """

    def get_keyword_names(self):
        return [
                'cloud_connector_edit_settings',
                'cloud_connector_edit_groups',
                ]

    def _open_page(self):
        """Go to ' Network -> Cloud Connector'"""
        self._navigate_to('Network', 'Cloud Connector')

    def cloud_connector_edit_groups(self,
        realm=None,
        groups_add=None,
        groups_remove=None,
        ):
        """
        Edit Cloud Policy Directory Groups

        Parameters:
        - `realm`: Selection of drop-list "Realm:"
        - `groups_add` - list of groups to be added
        (partial or full names separated by comma)
        - `groups_remove` - list of groups to be removed
         (partial or full names separated by comma)

        Examples:
        Cloud Connector Edit Groups Groups
        ...    realm=All Realms
        ...    groups_add=AD3\\Account Operators, AD1\\Allowed RODC Password Replication Group
        ...    groups_remove=Account Operators

        """
        self._open_page()
        self._click_edit_groups_link()
        self._select_groups(groups_add, groups_remove)

    def _click_edit_groups_link(self):
        LINK = "//input[@value ='Edit Groups...']"
        self.click_element(LINK, "don't wait")

    def _select_groups(self, groups_add, groups_remove):
        self._wait_until_text_is_present('Directory search completed',
            timeout=200)
        self._handle_groups('add', groups_add)
        self._handle_groups('remove', groups_remove)
        self._click_done_button()

    def _handle_groups(self, action, groups):
        TIMEOUT = 60
        _map = {
            "add": ("//select [@id='auth_group_list']",
                    "//input [@id='add_member_button']"),
            "remove": ("//select [@id='members_auth_group']",
                       "//input [@id='remove_member_button']"),
        }
        if groups:
            start_time = time.time()
            selections = [mem.strip() for mem in groups.split(',')]
            found = False
            while (not found and (time.time() - start_time < TIMEOUT)):
                available_selections = self.get_list_items(_map[action][0])
                for available_selection in available_selections:
                    if available_selection.find(selections[0]) > -1:
                        found = True
                        break

            select_list = []
            for selection in selections:
                for available_selection in available_selections:
                    if available_selection.find(selection) > -1:
                        if not available_selection in select_list:
                            select_list.append(available_selection)
                        break
                else:
                    raise guiexceptions.ConfigError(action + \
                        'selection "%s" not found' % selection)

            self.select_from_list(_map[action][0], *select_list)
            self.click_element(_map[action][1], "don't wait")

    def cloud_connector_edit_settings(self,
        server1=None,
        server2=None,
        server3=None,
        failure_handling=None,
        auth_scheme=None,
        auth_key=None,
        ):

        """ Edits Cloud Connector settings

        :Parameters:
           - `server1` - Cloud Web Security Proxy Server
           - `server2` - Cloud Web Security Proxy Server
           - `server3` - Cloud Web Security Proxy Server
           - `failure_handling` - Specify how to handle requests if all
            specified Cloud Web Security Proxy servers fail.
            'connect' - connect directly
            'drop' - drop requests
           - `auth_scheme` - Cloud Web Security Authorization Scheme
           'ip' - Authorize transaction based on IP address
           'key' - Send authorization key information with transaction
           - `auth_key` - Authorization Key

        Exceptions:
        - ValueError failure_handling 'XXX' should be in ['connect', 'drop']
        - ValueError auth_scheme 'XXX' should be in ['ip', 'key']

        Examples:
        | Cloud Connector Edit Settings |
        | ... | server1=1.1.1.1 |
        | ... | server2=2.2.2.2 |
        | ... | server3=3.3.3.3 |
        | ... | failure_handling=connect |
        | ... | auth_scheme=ip |
        | Cloud Connector Edit Settings |
        | ... | server1=server.com |
        | ... | failure_handling=drop |
        | ... | auth_scheme=key |
        | ... | auth_key=12345678901234567890123456789012 |
        """

        self._open_page()
        self._click_edit_settings_link()
        self._set_servers(server1, server2, server3)
        self._set_failure_handling(failure_handling)
        self._set_auth_scheme(auth_scheme, auth_key)
        self._click_submit_button()

    def _click_edit_settings_link(self):
        LINK = "//input[@value ='Edit Settings...']"
        self.click_element(LINK, "don't wait")

    def _set_servers(self, server1, server2, server3):
        """ Set Cloud Web Security Proxy Servers"""
        TEXT1 = "//input[@id='scansafe_servers[0][host]']"
        TEXT2 = "//input[@id='scansafe_servers[1][host]']"
        TEXT3 = "//input[@id='scansafe_servers[2][host]']"
        if server1 != None:
            self.input_text(TEXT1, server1)
        if server2 != None:
            self.input_text(TEXT2, server2)
        if server3 != None:
            self.input_text(TEXT3, server3)

    def _set_failure_handling(self, failure_handling):
        """ Specify how to handle requests if all specified Cloud Web Security
         Proxy servers fail """
        OPTIONS = {"connect":"//input[@value='connect']",
                 "drop":"//input[@value='drop']"}
        if failure_handling != None:
            if failure_handling in OPTIONS.keys():
                self._click_radio_button(OPTIONS[failure_handling])
            else:
                raise ValueError("failure_handling '" + \
                    failure_handling + \
                    "' should be in " + str(OPTIONS.keys()))

    def _set_auth_scheme(self, auth_scheme, auth_key):
        """ Specify Cloud Web Security Authorization Scheme """
        OPTIONS = {"ip":"//input[@value='ip']",
                 "key":"//input[@value='key']"}
        TEXT = "//input[@id='scansafe_license']"
        if auth_scheme != None:
            if auth_scheme in OPTIONS.keys():
                self._click_radio_button(OPTIONS[auth_scheme])
            else:
                raise ValueError("auth_scheme '" + \
                    auth_scheme + \
                    "' should be in " + str(OPTIONS.keys()))
        if auth_key != None:
            self.input_text(TEXT, auth_key)

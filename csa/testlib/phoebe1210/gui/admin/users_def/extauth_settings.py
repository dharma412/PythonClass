#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/admin/users_def/extauth_settings.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

AUTH_TYPE_COMBO = ('Authentication Type',
                   "//select[@id='ext_auth']")
CACHE_TIMEOUT = ('External Authentication Cache Timeout',
                 "//input[@id='extauth_cache_timeout']")
GROUP_MAPPING = ('Group Mapping', {})
GROUP_MAPPING_ADD_BUTTON = "//input[@id='ldap_groups_mapping_domtable_AddRow']"
GROUP_MAPPING_CONTAINER = "//tbody[@id='ldap_groups_mapping_rowContainer']"
# indexes starts from 1
GROUP_MAPPING_EXT_GROUP_NAME = lambda index: \
    "%s/tr[%d]//input[contains(@id, '[group_name]')]" % (GROUP_MAPPING_CONTAINER,
                                                         index)
GROUP_MAPPING_LOCAL_GROUP_NAME_COMBO = lambda index: \
    "%s/tr[%d]//select[contains(@id, '[role]')]" % (GROUP_MAPPING_CONTAINER,
                                                    index)
GROUP_MAPPING_DELETE_BUTTON = lambda index: \
    "%s/tr[%d]//img[@title='Delete...']" % (GROUP_MAPPING_CONTAINER, index)

# LDAP
LDAP_AUTH_QUERY_COMBO = ('LDAP External Authentication Query',
                         "//select[@id='query']")
LDAP_SERVER_TIMEOUT = ('Timeout To Wait For Valid Response From Server',
                       "//input[@id='timeout']")

# RADIUS
RADIUS_SERVER_INFO = ('RADIUS Server Information', {})
RADIUS_MAPPING_OPTIONS_RADIO_GROUP = ('Group Mapping to Local',
                                      {'Map externally authenticated users to multiple local roles': \
                                           "//input[@id='groups_enabled_true']",
                                       'Map all externally authenticated users to the Administrator role': \
                                           "//input[@id='groups_enabled_false']"})

RADIUS_HOSTS_CONTAINER = "//tbody[@id='service_hosts_rowContainer']"
# indexes starts from 1
RADIUS_SERVER_HOSTNAME = lambda index: "%s/tr[%d]//input[contains(@id, '[host]')]" % \
                                       (RADIUS_HOSTS_CONTAINER, index)
RADIUS_SERVER_PORT = lambda index: "%s/tr[%d]//input[contains(@id, '[port]')]" % \
                                   (RADIUS_HOSTS_CONTAINER, index)
RADIUS_SERVER_SHARED_SECRET = lambda index: \
    "%s/tr[%d]//input[contains(@id, '[shared_secret]')]" % (RADIUS_HOSTS_CONTAINER, index)
RADIUS_SERVER_TIMEOUT = lambda index: "%s/tr[%d]//input[contains(@id, '[timeout]')]" % \
                                      (RADIUS_HOSTS_CONTAINER, index)
RADIUS_SERVER_AUTH_TYPE = lambda index: "%s/tr[%d]//select[contains(@id, '[auth_type]')]" % \
                                        (RADIUS_HOSTS_CONTAINER, index)
RADIUS_SERVER_DELETE_BUTTON = lambda index: "%s/tr[%d]//img[@title='Delete...']" % \
                                            (RADIUS_HOSTS_CONTAINER, index)
RADIUS_SERVER_ADD_BUTTON = "//input[@id='service_hosts_domtable_AddRow']"


class ExtAuthSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, settings):
        self._set_combos(settings,
                         AUTH_TYPE_COMBO,
                         LDAP_AUTH_QUERY_COMBO)
        self._set_edits(settings,
                        CACHE_TIMEOUT,
                        LDAP_SERVER_TIMEOUT)
        self._set_radio_groups(settings,
                               RADIUS_MAPPING_OPTIONS_RADIO_GROUP)
        self._set_raduis_servers(settings)
        self._set_group_mapping(settings)

    def _set_group_mapping(self, settings):
        if settings.has_key(GROUP_MAPPING[0]):
            # clear list
            while self.gui._is_element_present(GROUP_MAPPING_DELETE_BUTTON(2)):
                self.gui.click_button(GROUP_MAPPING_DELETE_BUTTON(2), 'don\'t wait')
            pairs_to_set = settings[GROUP_MAPPING[0]]
            for index, pair in zip(range(1, len(pairs_to_set) + 1), pairs_to_set.items()):
                if index > 1:
                    self.gui.click_button(GROUP_MAPPING_ADD_BUTTON, 'don\'t wait')
                ext_group, local_group = pair
                self.gui.input_text(GROUP_MAPPING_EXT_GROUP_NAME(index), ext_group)
                self.gui.select_from_list(GROUP_MAPPING_LOCAL_GROUP_NAME_COMBO(index),
                                          local_group)

    def _set_raduis_servers(self, settings):
        if settings.has_key(RADIUS_SERVER_INFO[0]):
            # clear list
            while self.gui._is_element_present(RADIUS_SERVER_DELETE_BUTTON(2)):
                self.gui.click_button(RADIUS_SERVER_DELETE_BUTTON(2), 'don\'t wait')
            servers_to_set = settings[RADIUS_SERVER_INFO[0]]
            for index, server_options in zip(range(1, len(servers_to_set) + 1), servers_to_set):
                if index > 1:
                    self.gui.click_button(RADIUS_SERVER_ADD_BUTTON, 'don\'t wait')
                host_name, port, shared_secret, timeout, auth_type = \
                    tuple(map(lambda x: x.strip(), server_options.split(',')))
                self.gui.input_text(RADIUS_SERVER_HOSTNAME(index), host_name)
                if port:
                    self.gui.input_text(RADIUS_SERVER_PORT(index), port)
                self.gui.input_text(RADIUS_SERVER_SHARED_SECRET(index), shared_secret)
                if timeout:
                    self.gui.input_text(RADIUS_SERVER_TIMEOUT(index), timeout)
                if auth_type:
                    self.gui.select_from_list(RADIUS_SERVER_AUTH_TYPE(index), auth_type)

    def get(self):
        raise NotImplementedError()

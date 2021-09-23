#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/admin/users_def/sfauth_settings.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs


AUTH_TYPE_COMBO = ('Authentication Type',
                   "//select[@id='sf_auth']")

# RADIUS
RADIUS_HOSTS_CONTAINER = "//tbody[@id='service_hosts_rowContainer']"
# indexes starts from 1

RADIUS_SERVER_INFO = ('RADIUS Server Information', {})

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


class SfAuthSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, settings):
        self._set_radius_servers(settings)

    def _set_radius_servers(self, settings):
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

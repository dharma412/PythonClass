#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/network/smtp_authentication_def/forward_profile_settings.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.gui.decorators import set_speed

from base_profile_settings import BaseProfileAddSettings


class ForwardProfileAddSettings(BaseProfileAddSettings):
    HOSTNAME = ('Hostname',
                "//input[@name='hostname']")
    PORT = ('Port',
            "//input[@name='port']")
    INTERFACE_COMBO = ('Interface',
                       "//select[@name='ip_interface']")
    MAX_CONNECTIONS = ('Maximum Simultaneous Connections',
                       "//input[@name='connections']")
    REQUIRE_TLS_CHECKBOX = ('Require TLS',
                            "//input[@id='tls']")
    USE_SASL_LOGIN_CHECKBOX = ('Use SASL LOGIN mechanism',
                               "//input[@id='sasl_login']")
    USE_SASL_PLAIN_CHECKBOX = ('Use SASL PLAIN mechanism',
                               "//input[@id='sasl_plain']")

    def _set_interface_combo(self, interface_name):
        interface_name = interface_name.lower()
        all_options = self.gui.get_list_items(self.INTERFACE_COMBO[1])
        interfaces_mapping = dict(map(lambda x: (x.split(' ')[0].lower(), x),
                                      all_options))
        if interface_name in interfaces_mapping:
            self.gui.select_from_list(self.INTERFACE_COMBO[1],
                                      interfaces_mapping[interface_name])
        else:
            raise ValueError('Unknown interface name "%s". Available interface ' \
                             'names are: %s' % (interface_name,
                                                interfaces_mapping.keys()))

    def set(self, new_value):
        super(ForwardProfileAddSettings, self).set(new_value)

        self._set_edits(new_value,
                        self.HOSTNAME,
                        self.PORT,
                        self.MAX_CONNECTIONS)
        self._set_checkboxes(new_value,
                             self.REQUIRE_TLS_CHECKBOX,
                             self.USE_SASL_LOGIN_CHECKBOX,
                             self.USE_SASL_PLAIN_CHECKBOX)
        if self.INTERFACE_COMBO[0] in new_value:
            self._set_interface_combo(new_value[self.INTERFACE_COMBO[0]])

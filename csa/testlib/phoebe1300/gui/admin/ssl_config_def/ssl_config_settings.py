#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/ssl_config_def/ssl_config_settings.py#3 $ $DateTime: 2019/09/16 22:49:03 $ $Author: amanikaj $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner

CATEGORIES_MAPPING = {'GUI HTTPS': 'gui',
                      'Inbound SMTP': 'inbound',
                      'Outbound SMTP': 'outbound'}
METHODS_MAPPING = {'TLS v1': 'tlsv1_0',
                   'TLS v1.1': 'tlsv1_1',
                   'SSL v3': 'sslv3',
                   'SSL v2': 'sslv2',
                   'TLS v1.2': 'tlsv1_2'}
ALL_CHECKBOXES = []
ALL_EDITS = []
for category_name_prefix, category_locator_prefix in CATEGORIES_MAPPING.iteritems():
    for method_name_suffix, method_locator_suffix in METHODS_MAPPING.iteritems():
        checkbox_name = '{0} Method {1}'.format(category_name_prefix,
                                                method_name_suffix)
        checkbox_locator = "//input[@id='ssl_{0}_method_{1}']".format(
            category_locator_prefix, method_locator_suffix)
        ALL_CHECKBOXES.append((checkbox_name, checkbox_locator))
    edit_name = '{0} SSL Cipher(s) to use'.format(category_name_prefix)
    edit_locator = "//input[@name='ssl_{0}_ciphers']".format(category_locator_prefix)
    ALL_EDITS.append((edit_name, edit_locator))
    if (category_locator_prefix == 'gui' or category_locator_prefix == 'inbound'):
        tls_reg_name = '{0} TLS Renegotiation {1}'.format(category_name_prefix, "Enable")
        tls_reg_locator = "//input[@id='{0}_tls_renegotiation']".format(category_locator_prefix)
        ALL_CHECKBOXES.append((tls_reg_name, tls_reg_locator))


class SSLConfigSettings(InputsOwner):
    def _get_registered_inputs(self):
        return ALL_CHECKBOXES + ALL_EDITS

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value,
                             *ALL_CHECKBOXES)
        self._set_edits(new_value,
                        *ALL_EDITS)

    @set_speed(0, 'gui')
    def get(self):
        result = self._get_checkboxes(*ALL_CHECKBOXES)
        result.update(self._get_values(*ALL_EDITS))
        return result

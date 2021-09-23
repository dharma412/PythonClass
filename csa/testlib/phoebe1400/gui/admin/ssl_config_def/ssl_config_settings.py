#!/usr/bin/env python -tt

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner


CATEGORIES_MAPPING = {'GUI HTTPS': 'gui',
                      'Inbound SMTP': 'inbound',
                      'Outbound SMTP': 'outbound'}
METHODS_MAPPING = {'TLS v1.0': 'tlsv1_0',
                   'TLS v1.1': 'tlsv1_1',
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
    if (category_locator_prefix=='gui' or category_locator_prefix=='inbound'):
      tls_reg_name = '{0} TLS Renegotiation {1}' .format(category_name_prefix,"Enable")
      tls_reg_locator= "//input[@id='{0}_tls_renegotiation']".format(category_locator_prefix)
      ALL_CHECKBOXES.append((tls_reg_name,tls_reg_locator))

other_clients_tls_checbox_name = 'Other TLS Client Services'
other_clients_tls_checbox_locator = "//input[@id='tls_client_method']"
ALL_CHECKBOXES.append((other_clients_tls_checbox_name, other_clients_tls_checbox_locator))

fqdn_validation_checkbox_name = 'Peer Certificate FQDN Validation'
fqdn_validation_checkbox_locator = "//input[@id='peer_cert_fqdn']"
ALL_CHECKBOXES.append((fqdn_validation_checkbox_name,
                       fqdn_validation_checkbox_locator))

x509_validation_checkbox_name = 'Peer Certificate X509 Validation'
x509_validation_checkbox_locator = "//input[@id='peer_cert_x509']"
ALL_CHECKBOXES.append((x509_validation_checkbox_name,
                       x509_validation_checkbox_locator))

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

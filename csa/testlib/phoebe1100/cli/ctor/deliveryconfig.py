#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/deliveryconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
SARF CLI ctor - deliveryconfig
"""
import clictorbase as ccb
import re
from sal.containers.yesnodefault import is_yes

DEFAULT = ccb.DEFAULT


class deliveryconfig(ccb.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['ifname'] = \
            ['default interface to deliver', DEFAULT, True]
        param_map['enable_poss_delivery'] = \
            ['Enable "Possible Delivery"', DEFAULT]
        param_map['max_outbound_concur'] = \
            ['wide maximum outbound ', DEFAULT]
        param_map['max_tls_outbound_concur'] = \
            ['wide TLS maximum outbound', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')
        return self._process_input(param_map)

    def get_settings(self, as_dictionary='y'):
        raw = self._read_until('Choose the operation ')
        self._to_the_top(1)
        if is_yes(as_dictionary):
            ifname = \
                re.search(".*interface.*:(?P<ifname>.*)",
                          raw, re.MULTILINE | re.IGNORECASE). \
                    groupdict()['ifname'].strip()
            poss_delivery = \
                re.search(".*Possible.*:(?P<poss_delivery>.*)",
                          raw, re.MULTILINE | re.IGNORECASE). \
                    groupdict()['poss_delivery'].strip()
            max_outbound_concur = \
                re.search(".*wide maximum outbound.*:(?P<max_outbound_concur>.*)",
                          raw, re.MULTILINE | re.IGNORECASE). \
                    groupdict()['max_outbound_concur'].strip()
            max_tls_outbound_concur = \
                re.search(".*wide TLS maximum.*:(?P<max_tls_outbound_concur>.*)",
                          raw, re.MULTILINE | re.IGNORECASE). \
                    groupdict()['max_tls_outbound_concur'].strip()
            d = {'ifname': ifname,
                 'poss_delivery': poss_delivery,
                 'max_outbound_concur': max_outbound_concur,
                 'max_tls_outbound_concur': max_tls_outbound_concur, }
            return d
        return raw

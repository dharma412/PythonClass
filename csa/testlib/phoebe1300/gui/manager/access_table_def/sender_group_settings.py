#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/manager/access_table_def/sender_group_settings.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

NAME = ('name',
        'xpath=//input[@name=\'id\']')
COMMENT = ('comment',
           "//input[@name='comment']")
POLICY_COMBO = ('policy',
                '//select[@name=\'policy\']')
SBRS_MIN = ('sbrs_min',
            'xpath=//input[@name=\'sbrs_from\']')
SBRS_MAX = ('sbrs_max',
            'xpath=//input[@name=\'sbrs_to\']')
INCLUDE_SBRS_NONE_CHECKBOX = ('include_sbrs_none',
                              'xpath=//input[@id=\'sbrs_none\']')
DNS_LIST = ('dns_list',
            'xpath=//input[@name=\'dnslists\']')
NX_DOMAIN_CHECKBOX = ('nx_domain',
                      'xpath=//input[@id=\'nx_domain\']')
SERV_FAIL_CHECKBOX = ('serv_fail',
                      'xpath=//input[@id=\'serv_fail\']')
NOT_DOUBLE_DOT_VERIFIED_CHECKBOX = ('not_double_dot_verified',
                                    'xpath=//input[@id=\'not_double_dot_verified\']')
ORDER_COMBO = ('order',
               '//select[@name=\'order\']')

EXTERNAL_THREAT_FEEDS = ('external_threat_feeds', 'xpath=//*[@id="etf_selection[0][etf_source]"]')


class SenderGroupSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_edits(new_value,
                        NAME,
                        COMMENT,
                        SBRS_MIN,
                        SBRS_MAX,
                        DNS_LIST)
        self._set_combos(new_value,
                         ORDER_COMBO,
                         POLICY_COMBO)
        self._set_checkboxes(new_value,
                             INCLUDE_SBRS_NONE_CHECKBOX,
                             NX_DOMAIN_CHECKBOX,
                             SERV_FAIL_CHECKBOX,
                             NOT_DOUBLE_DOT_VERIFIED_CHECKBOX)

    @set_speed(0, 'gui')
    def get(self):
        return self._get_values(NAME,
                                COMMENT,
                                POLICY_COMBO,
                                SBRS_MIN,
                                SBRS_MAX,
                                INCLUDE_SBRS_NONE_CHECKBOX,
                                DNS_LIST,
                                EXTERNAL_THREAT_FEEDS,
                                NX_DOMAIN_CHECKBOX,
                                SERV_FAIL_CHECKBOX,
                                NOT_DOUBLE_DOT_VERIFIED_CHECKBOX)

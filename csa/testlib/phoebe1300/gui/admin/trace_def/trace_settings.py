#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/trace_def/trace_settings.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs, \
    CUSTOM_RADIO_FLAG


class TraceSettings(InputsOwner):
    SOURCE_IP = ('Source IP Address',
                 "//input[@id='source_ip']")
    FQDN = ('Fully Qualified Domain Name',
            "//input[@name='fqdn']")
    INJECTOR_NAME_COMBO = ('Trace Behavior on',
                           "//select[@id='injector_name']")
    HELO_DOMAIN = ('Domain Name to be Passed to HELO/EHLO',
                   "//input[@name='helo_domain']")
    SMTP_AUTH = ('SMTP Authentication Username',
                 "//input[@id='smtp_auth_id']")
    SBO_CHOICE_RADIO_GROUP = ('SenderBase Network Owner ID',
                              {'Lookup network owner ID associated with source IP': \
                                   "//input[@id='sbo_choice_lookup']",
                               CUSTOM_RADIO_FLAG: ('input_text', 'get_value',
                                                   "//input[@name='sbo']",
                                                   "//input[@id='sbo_choice_enter']")})
    SBRS_CHOICE_RADIO_GROUP = ('SenderBase Reputation Score',
                               {'Lookup SBRS associated with source IP': \
                                    "//input[@id='sbrs_choice_lookup']",
                                CUSTOM_RADIO_FLAG: ('input_text', 'get_value',
                                                    "//input[@name='sbrs']",
                                                    "//input[@id='sbrs_choice_ent']")})
    MAIL_FROM = ('Envelope Sender',
                 "//input[@name='mail_from']")
    RCPT_LIST = ('Envelope Recipients',
                 "//textarea[@id='rcpt_list']")
    MSG_BODY = ('Message Body',
                "//textarea[@id='msg_body']")

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    def set(self, new_value):
        self._set_combos(new_value,
                         self.INJECTOR_NAME_COMBO)
        self._set_radio_groups(new_value,
                               self.SBO_CHOICE_RADIO_GROUP,
                               self.SBRS_CHOICE_RADIO_GROUP)
        self._set_edits(new_value,
                        self.SOURCE_IP,
                        self.FQDN,
                        self.HELO_DOMAIN,
                        self.SMTP_AUTH,
                        self.MAIL_FROM,
                        self.RCPT_LIST,
                        self.MSG_BODY)

    def get(self):
        raise NotImplementedError()

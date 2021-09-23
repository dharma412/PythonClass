#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/network/smtp_authentication_def/ldap_profile_settings.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.decorators import set_speed

from base_profile_settings import BaseProfileAddSettings


class LDAPProfileAddSettings(BaseProfileAddSettings):
    LDAP_QAUERY_COMBO = ('LDAP Query',
                         "//select[@name='profile_query']")
    ENCRYPTION_TYPE_COMBO = ('Default Encryption Method',
                             "//select[@name='enc_type']")
    SMTP_AUTH_VERIFY_CHECKBOX = \
            ('Check with LDAP if user is allowed to use SMTP AUTH',
                                 "//input[@id='smtp_auth_verify']")
    NOT_ALLOWED_RADIOGROUP = ('If user is found to be not allowed to use SMTP AUTH',
                              {'Monitor': "//input[@id='ldap_verify_monitor']",
                               'Reject': "//input[@id='ldap_verify_reject']"})
    SMTP_AUTH_CUSTOM_RESPONSE_CHECKBOX = ('Custom SMTP response',
                                          "//input[@id='smtp_auth_custom_response']")
    SMTP_AUTH_CUSTOM_RESPONSE_CODE = ('SMTP Code',
                                      "//input[@id='smtp_auth_custom_response_code']")
    SMTP_AUTH_CUSTOM_RESPONSE_TEXT = ('Custom SMTP Response Text',
                                      "//textarea[@id='smtp_auth_custom_response_text']")

    def set(self, new_value):
        super(LDAPProfileAddSettings, self).set(new_value)

        self._set_combos(new_value,
                         self.LDAP_QAUERY_COMBO,
                         self.ENCRYPTION_TYPE_COMBO)
        self._set_checkboxes(new_value,
                             self.SMTP_AUTH_VERIFY_CHECKBOX)
        self._set_radio_groups(new_value,
                               self.NOT_ALLOWED_RADIOGROUP)
        self._set_checkboxes(new_value,
                             self.SMTP_AUTH_CUSTOM_RESPONSE_CHECKBOX)
        self._set_edits(new_value,
                        self.SMTP_AUTH_CUSTOM_RESPONSE_CODE,
                        self.SMTP_AUTH_CUSTOM_RESPONSE_TEXT)

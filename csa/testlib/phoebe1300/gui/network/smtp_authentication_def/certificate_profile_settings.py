#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/network/smtp_authentication_def/certificate_profile_settings.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.gui.decorators import set_speed

from base_profile_settings import BaseProfileAddSettings


class CertificateProfileAddSettings(BaseProfileAddSettings):
    CERTAUTH_LDAP_PROFILE_COMBO = ('LDAP Query to Use',
                                   "//select[@name='certauth_ldap_profile']")
    ALLOW_SMTP_AUTH_NO_CERT_CHECKBOX = ('Allow SMTP AUTH Command if no Certificate',
                                        "//input[@id='allow_smtp_auth_no_cert']")
    LDAP_FORWARD_PROFILE_COMBO = ('LDAP or Forward Type SMTP Auth Profile',
                                  "//select[@id='ldap_forward_profile']")

    def set(self, new_value):
        super(CertificateProfileAddSettings, self).set(new_value)

        self._set_combos(new_value,
                         self.CERTAUTH_LDAP_PROFILE_COMBO)
        self._set_checkboxes(new_value,
                             self.ALLOW_SMTP_AUTH_NO_CERT_CHECKBOX)
        self._set_combos(new_value,
                         self.LDAP_FORWARD_PROFILE_COMBO)

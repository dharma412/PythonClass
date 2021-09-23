#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/network/smtp_authentication_def/outgoing_profile_settings.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.gui.decorators import set_speed

from base_profile_settings import BaseProfileAddSettings


class OutgoingProfileAddSettings(BaseProfileAddSettings):
    AUTH_USERNAME = ('Authentication Username',
                     "//input[@name='auth_username']")
    AUTH_PASSWORD = ('Authentication Password',
                     "//input[@name='auth_password']")

    def set(self, new_value):
        super(OutgoingProfileAddSettings, self).set(new_value)

        self._set_edits(new_value,
                        self.AUTH_USERNAME,
                        self.AUTH_PASSWORD)

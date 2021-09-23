#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/network/crl_sources_def/crl_sources_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

CRL_INBOUND_CHECK_CHECKBOX = ('CRL check for inbound SMTP TLS',
                              "//input[@id='crl_inbound_check']")
CRL_OUTBOUND_CHECK_CHECKBOX = ('CRL check for outbound SMTP TLS',
                               "//input[@id='crl_outbound_check']")


class CRLSourcesSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value,
                             CRL_INBOUND_CHECK_CHECKBOX,
                             CRL_OUTBOUND_CHECK_CHECKBOX)

#!/usr/bin/env python -tt
#$Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/smart_license_def/smart_license_settings.py#1 $
#$DateTime: 2019/08/14 09:58:47 $
#$Author: uvelayut $

from common.gui.decorators import go_to_page, set_speed
from common.util.ordered_dict import OrderedDict
from common.gui.inputs_owner import InputsOwner

ROW_MAPPING = OrderedDict(
   [('Web Security Appliance Cisco Web Usage Controls', 'firestone'),
   ('Web Security Appliance Anti-Virus Webroot', 'merlin'),
   ('Web Security Appliance L4 Traffic Monitor', 'trmon'),
   ('Web Security Appliance Cisco AnyConnect SM for AnyConnect', 'mus'),
   ('Web Security Appliance Advanced Malware Protection Reputatio', 'amp_file_rep'),
   ('Web Security Appliance Anti-Virus Sophos', 'sophos'),
   ('Web Security Appliance Web Reputation Filters', 'wbrs'),
   ('Web Security Appliance Advanced Malware Protection', 'amp_file_analysis'),
   ('Web Security Appliance Anti-Virus McAfee', 'mcafee'),
   ('Web Security Appliance Web Proxy and DVS Engine', 'proxy'),
   ('Web Security Appliance HTTPs Decryption', 'https')])

CHECKBOX_MAPPING = OrderedDict()
for row_name_expanded, row_name_short in ROW_MAPPING.iteritems():
        CHECKBOX_MAPPING[row_name_expanded] = "//input[@id='%s']" % (row_name_short)

class SmartLicenseSettings(InputsOwner):
    def _get_registered_inputs(self):
        return CHECKBOX_MAPPING.items()

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value, *CHECKBOX_MAPPING.items())

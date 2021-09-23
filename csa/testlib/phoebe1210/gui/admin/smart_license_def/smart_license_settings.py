#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/admin/smart_license_def/smart_license_settings.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

from common.gui.decorators import go_to_page, set_speed
from common.util.ordered_dict import OrderedDict
from common.gui.inputs_owner import InputsOwner

ROW_MAPPING = OrderedDict(
    [('Mail Handling', 'imh'),
     ('Email Security Appliance Bounce Verification', 'bounce_verification'),
     ('Email Security Appliance Anti-Spam License', 'case'),
     ('Email Security Appliance Outbreak Filters', 'VOF'),
     ('Email Security Appliance Data Loss Prevention', 'rsadlp'),
     ('Email Security Appliance Cloudmark Anti-Spam', 'cloudmark'),
     ('Email Security Appliance Advanced Malware Protection Reputation', 'amp_file_rep'),
     ('Email Security Appliance Sophos Anti-Malware', 'sophos'),
     ('Email Security Appliance PXE Encryption', 'envelope_encryption'),
     ('Email Security Appliance Advanced Malware Protection', 'amp_file_analysis'),
     ('Email Security Appliance McAfee Anti-Malware', 'mcafee'),
     ('Email Security Appliance Intelligent Multi-Scan', 'ims'),
     ('Email Security Appliance Image Analyzer', 'iia'),
     ('Email Security Appliance External Threat Feeds', 'ETF'),
     ('Email Security Appliance Graymail Safe-unsubscribe', 'gm_unsubscription')])

CHECKBOX_MAPPING = OrderedDict()
for row_name_expanded, row_name_short in ROW_MAPPING.iteritems():
    CHECKBOX_MAPPING[row_name_expanded] = "//input[@id='%s']" % (row_name_short)


class SmartLicenseSettings(InputsOwner):
    def _get_registered_inputs(self):
        return CHECKBOX_MAPPING.items()

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value, *CHECKBOX_MAPPING.items())

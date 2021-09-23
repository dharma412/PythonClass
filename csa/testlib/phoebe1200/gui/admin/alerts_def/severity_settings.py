#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/admin/alerts_def/severity_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner
from common.util.ordered_dict import OrderedDict

RECIPIENT = ('Recipient Address',
             "//input[@name='recipient']")
RSN = ('Release and Support Notifications',
       "//input[@id='rnt-all']")
ROW_MAPPING = OrderedDict(
    [('All', 'all'),
     ('System', 'system'),
     ('Hardware', 'hardware'),
     ('Updater', 'updater'),
     ('Outbreak Filters', 'vof'),
     ('Anti-Virus', 'antivirus'),
     ('Anti-Spam', 'antispam'),
     ('Directory Harvest Attack Prevention', 'dhap')])

COLUMN_MAPPING = OrderedDict([(k, k.lower()) for k in \
                              ['All', 'Critical', 'Warning', 'Info']])

CHECKBOX_MAPPING = OrderedDict()
for row_name_human, row_name in ROW_MAPPING.iteritems():
    for column_name_human, column_name in COLUMN_MAPPING.iteritems():
        if row_name_human == column_name_human:
            key = '%s' % (row_name_human,)
        else:
            key = '%s %s' % (row_name_human, column_name_human)
        CHECKBOX_MAPPING[key] = "//input[@id='%s-%s']" % (row_name, column_name)


class SeveritySettings(InputsOwner):
    def _get_registered_inputs(self):
        return CHECKBOX_MAPPING.items() + [RECIPIENT] + [RSN]

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_edits(new_value,
                        RECIPIENT)
        self._set_checkboxes(new_value,
                             *CHECKBOX_MAPPING.items())
        self._set_checkboxes(new_value,
                             RSN)

    def get(self):
        raise NotImplementedError()

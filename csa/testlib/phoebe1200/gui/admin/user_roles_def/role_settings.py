#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/admin/user_roles_def/role_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

NAME = ('Name',
        "//input[@name='name']")
DESCRIPTION = ('Description',
               "//textarea[@name='description']")
MAIL_POLICIES_AND_CONTENT_FILTERS_RADIO_GROUP = ('Mail Policies and Content Filters',
                                                 {'No access': "//input[@id='mailpolicynone']",
                                                  'View assigned, edit assigned': "//input[@id='mailpolicyrestricted']",
                                                  'View all, edit assigned': "//input[@id='mailpolicysemirestricted']",
                                                  'View all, edit all': "//input[@id='mailpolicyunrestricted']"})
DLP_POLICIES_RADIO_GROUP = ('DLP Policies',
                            {'No access': "//input[@id='dlppolicynone']",
                             'View assigned, edit assigned': "//input[@id='dlppolicyrestricted']",
                             'View all, edit assigned': "//input[@id='dlppolicysemirestricted']",
                             'View all, edit all': "//input[@id='dlppolicyunrestricted']"})
EMAIL_REPORTING_RADIO_GROUP = ('Email Reporting',
                               {'No access': "//input[@id='reportsnone']",
                                'View relevant reports': "//input[@id='reportssemirestricted']",
                                'View all reports': "//input[@id='reportsunrestricted']"})
MESSAGE_TRACKING_RADIO_GROUP = ('Message Tracking',
                                {'No access': "//input[@id='trackingnone']",
                                 'Message Tracking access': "//input[@id='trackingunrestricted']"})
TRACE_RADIO_GROUP = ('Trace',
                     {'No access': "//input[@id='tracenone']",
                      'Trace access': "//input[@id='traceunrestricted']"})
QUARANTINES_RADIO_GROUP = ('Quarantines',
                           {'No access': "//input[@id='quarantinenone']",
                            'Manage assigned quarantines': "//input[@id='quarantinerestricted']"})


class RoleSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_edits(new_value,
                        NAME,
                        DESCRIPTION)
        self._set_radio_groups(new_value,
                               MAIL_POLICIES_AND_CONTENT_FILTERS_RADIO_GROUP,
                               DLP_POLICIES_RADIO_GROUP,
                               EMAIL_REPORTING_RADIO_GROUP,
                               MESSAGE_TRACKING_RADIO_GROUP,
                               TRACE_RADIO_GROUP,
                               QUARANTINES_RADIO_GROUP)

    def get(self):
        raise NotImplementedError()

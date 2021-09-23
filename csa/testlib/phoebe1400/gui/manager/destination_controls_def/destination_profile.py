#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/destination_controls_def/destination_profile.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs


class BaseDestinationProfileSettings(InputsOwner):
    IP_ADDRESS_PREF_COMBO = ('IP Address Preference',
                             "//select[@name='ip_sort_pref']")
    MAX_HOST_CONCURRENCY = ('Concurrent Connections',
                            "//input[@id='max_host_concurrency']")
    MAX_MSGS_PER_CONNECTION = ('Maximum Messages Per Connection',
                               "//input[@name='max_messages_per_connection']")
    RECIPIENTS = ('Recipients',
                  "//input[@id='recipient_limit']")
    RECIPIENT_MINUTES = ('Recipient Minutes',
                         "//input[@id='recipient_minutes']")
    LIMITS_PER_DEST_RADIOGROUP = ('Apply Limits Per Destination',
                        {'Entire Domain': "//input[@id='limit_type_domain']",
                         'Each Mail Exchanger (MX Record) IP address': \
                                        "//input[@id='limit_type_mx']"})
    LIMITS_PER_HOSTNAME_RADIOGROUP = ('Apply Limits Per ESA Hostname',
                        {'System Wide': "//input[@id='limit_apply_wide']",
                         'Each Virtual Gateway': "//input[@id='limit_apply_gw']"})
    TLS_SUPPORT_COMBO = ('TLS Support',
                         "//select[@id='table_tls']")
    DANE_COMBO = ('Dane Support',"//select[@name='dane_option']")
    BOUNCE_PROFILE_COMBO = ('Bounce Profile',
                            "//select[@name='bounce_profile']")

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    def set(self, new_value):
        self._set_combos(new_value,
                         self.IP_ADDRESS_PREF_COMBO,
                         self.BOUNCE_PROFILE_COMBO,
                         self.TLS_SUPPORT_COMBO,
                         self.DANE_COMBO)
        self._set_radio_groups(new_value,
                               self.LIMITS_PER_DEST_RADIOGROUP,
                               self.LIMITS_PER_HOSTNAME_RADIOGROUP)
        self._set_edits(new_value,
                        self.MAX_HOST_CONCURRENCY,
                        self.MAX_MSGS_PER_CONNECTION,
                        self.RECIPIENTS,
                        self.RECIPIENT_MINUTES)

    def get(self):
        raise NotImplementedError()


class DestinationProfileSettings(BaseDestinationProfileSettings):
    DESTINATION = ('Destination',
                   "//input[@name='new_name']")
    CONCURRENT_CONNECTIONS_RADIOGROUP = ('Concurrent Connections Limit',
                         {'Use Default': "//input[@id='host_concurrency_default']",
                          'Custom': "//input[@id='host_concurrency_custom']"})
    MAX_MSGS_PER_CONNECTION_RADIOGROUP = ('Maximum Messages Per Connection Limit',
                {'Use Default':  "//input[@id='messages_per_connection_default']",
                 'Custom': "//input[@id='messages_per_connection_custom']"})
    RECIPIENTS_RADOIGROUP = ('Recipients Limit',
                             {'Use Default': "//input[@id='recipient_no_limit']",
                              'Custom': "//input[@id='recipient_max_of']"})
    BOUNCE_VERIFICATION_RADIOGROUP = ('Bounce Verification',
                   {'Use Default': "//input[@id='bounce_validation_default_id']",
                    'Yes': "//input[@id='bounce_validation_yes_id']",
                    'No': "//input[@id='bounce_validation_no_id']"})

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_edits(new_value,
                        self.DESTINATION)
        self._set_radio_groups(new_value,
                               self.CONCURRENT_CONNECTIONS_RADIOGROUP,
                               self.MAX_MSGS_PER_CONNECTION_RADIOGROUP,
                               self.RECIPIENTS_RADOIGROUP,
                               self.BOUNCE_VERIFICATION_RADIOGROUP)
        super(DestinationProfileSettings, self).set(new_value)

    @set_speed(0, 'gui')
    def get(self):
        raise NotImplementedError()


class DefaultDestinationProfileSettings(BaseDestinationProfileSettings):
    RECIPIENTS_RADOIGROUP = ('Recipients Limit',
                             {'No Limit': "//input[@id='recipient_no_limit']",
                              'Custom': "//input[@id='recipient_max_of']"})
    BOUNCE_VERIFICATION_RADIOGROUP = ('Bounce Verification',
                           {'Yes': "//input[@id='bounce_validation_yes_id']",
                            'No': "//input[@id='bounce_validation_no_id']"})

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_radio_groups(new_value,
                               self.RECIPIENTS_RADOIGROUP,
                               self.BOUNCE_VERIFICATION_RADIOGROUP)
        super(DefaultDestinationProfileSettings, self).set(new_value)

    @set_speed(0, 'gui')
    def get(self):
        raise NotImplementedError()

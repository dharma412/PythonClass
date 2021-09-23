#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/network/bounce_profiles_def/bounce_profile.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs

NOTIFICATION_LANGUAGE = lambda notif_type, index: '//select[@id="%s_tmpl[%s][lang]"]' % (notif_type, index,)
NOTIFICATION_TEMPLATE = lambda notif_type, index: '//select[@id="%s_tmpl[%s][tmpl]_id"]' % (notif_type, index,)
TEMPLATE_ADD_BUTTON = lambda notif_type: '%s_tmpl_domtable_AddRow' % (notif_type,)


class BaseBounceProfileSettings(InputsOwner):
    RETR_NUMBER = ('Maximum Number of Retries',
                   "//input[@name='max_retries']")
    TIME_IN_QUEUE = ('Maximum Time in Queue',
                     "//input[@name='max_queue_lifetime']")
    INIT_TIME_TO_WAIT_PER_MSG = ('Initial Time to Wait per Message',
                                 "//input[@name='initial_retry']")
    MAX_TIME_TO_WAIT_PER_MSG = ('Maximum Time to Wait per Message',
                                "//input[@name='max_retry_timeout']")
    HARD_BOUNCE_MSG_SUBJECT = ('Hard Bounce Message Subject',
                               "//input[@name='bounce_subject']")
    HARD_BOUNCE_NOTIF_TEMPLATE_COMBO = ('Hard Bounce Notification Template',
                                        "//select[@id='bounce_tmpl_id']")
    SEND_DELAY_MSG_SUBJECT = ('Send Delay Message Subject',
                              "//input[@name='delay_subject']")
    SEND_DELAY_NOTIF_TEMPLATE_COMBO = ('Send Delay Notification Template',
                                       "//select[@id='delay_tmpl_id']")
    SEND_DELAY_MIN_INTERVAL_BETWEEN_MSGS = ('Minimum Interval Between Messages',
                                            "//input[@name='send_warnings_interval']")
    SEND_DELAY_MAX_MSG_TO_SEND = ('Maximum Number of Messages to Send',
                                  "//input[@name='send_warnings_count']")
    ALTERNATE_ADDRESS = ('Alternate Address',
                         "//input[@id='alt_address']")
    RECIPIENT_FOR_MSGS_RADOIGROUP = ('Recipient for Bounce and Warning Messages',
                                     {'Message sender': "//input[@id='message_sender']",
                                      'Alternate': "//input[@id='alternate']"})
    LANGUAGE_MAP = {
        'default': 'others', 'deutsch': 'de',
        'english': 'en', 'espanol': 'es',
        'french': 'fr', 'italian': 'it',
        'japanese': 'ja', 'korean': 'ko',
        'portuguese': 'pt', 'russian': 'ru',
        'chinese': 'zh-cn', 'taiwanese': 'zh-tw',
    }

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    def _add_notification_template(self, notification_type, template_dict={}):
        if template_dict.has_key('Default'):
            self.gui.select_from_list(NOTIFICATION_TEMPLATE(notification_type, 0), \
                                      template_dict['Default'])
            del template_dict['Default']
        languages = template_dict.keys()
        languages.sort()
        if (len(languages) >= 1):
            for index in range(1, len(languages) + 1):
                self.gui.click_button(TEMPLATE_ADD_BUTTON(notification_type), "don't wait")
                self.gui.select_from_list(NOTIFICATION_LANGUAGE(notification_type, index), \
                                          self.LANGUAGE_MAP[languages[index - 1].lower()])
                self.gui.select_from_list(NOTIFICATION_TEMPLATE(notification_type, index), \
                                          template_dict[languages[index - 1]])

    def set(self, new_value):
        self._set_radio_groups(new_value,
                               self.RECIPIENT_FOR_MSGS_RADOIGROUP)
        self._set_edits(new_value,
                        self.RETR_NUMBER,
                        self.TIME_IN_QUEUE,
                        self.INIT_TIME_TO_WAIT_PER_MSG,
                        self.MAX_TIME_TO_WAIT_PER_MSG,
                        self.HARD_BOUNCE_MSG_SUBJECT,
                        self.SEND_DELAY_MSG_SUBJECT,
                        self.SEND_DELAY_MIN_INTERVAL_BETWEEN_MSGS,
                        self.SEND_DELAY_MAX_MSG_TO_SEND,
                        self.ALTERNATE_ADDRESS)
        if new_value.has_key('Hard Bounce Notification Template'):
            self._add_notification_template('bounce', \
                                            new_value['Hard Bounce Notification Template'])
        if new_value.has_key('Send Delay Notification Template'):
            self._add_notification_template('delay', \
                                            new_value['Send Delay Notification Template'])

    def get(self):
        raise NotImplementedError()


class BounceProfileSettings(BaseBounceProfileSettings):
    PROFILE_NAME = ('Profile Name',
                    "//input[@name='newName']")
    SEND_HARD_BOUNCE_MSGS_RADIOGROUP = ('Send Hard Bounce Messages',
                                        {'Use Default': "//input[@id='default_bounces']",
                                         'Yes': "//input[@id='yes_bounces']",
                                         'No': "//input[@id='no_bounces']"})
    HARD_BOUNCE_USE_DSN_FORMAT_RADIOGROUP = ('Use DSN format for bounce messages',
                                             {'Use Default': "//input[@id='default_dsn']",
                                              'Yes': "//input[@id='yes_dsn']",
                                              'No': "//input[@id='no_dsn']"})
    HARD_BOUNCE_USE_BOUNCE_RESPONSE_CODE_RADIOGROUP = \
        ('Parse DSN "Status" field from bounce responses',
         {'Use Default': "//input[@id='default_dsn_parse']",
          'Yes': "//input[@id='yes_dsn_parse']",
          'No': "//input[@id='no_dsn_parse']"})
    SEND_DELAY_WARN_MSGS_RADIOGROUP = ('Send Delay Warning Messages',
                                       {'Use Default': "//input[@id='default_warnings']",
                                        'Yes': "//input[@id='yes_warnings']",
                                        'No': "//input[@id='no_warnings']"})
    USE_DKEY_RADIOGROUP = ('Use Domain Key Signing for Bounce and Delay Messages',
                           {'Use Default': "//input[@id='sign_bounce_messages2']",
                            'Yes': "//input[@id='sign_bounce_messages1']",
                            'No': "//input[@id='sign_bounce_messages0']"})

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_radio_groups(new_value,
                               self.SEND_HARD_BOUNCE_MSGS_RADIOGROUP,
                               self.HARD_BOUNCE_USE_DSN_FORMAT_RADIOGROUP,
                               self.HARD_BOUNCE_USE_BOUNCE_RESPONSE_CODE_RADIOGROUP,
                               self.SEND_DELAY_WARN_MSGS_RADIOGROUP,
                               self.USE_DKEY_RADIOGROUP)
        self._set_edits(new_value, self.PROFILE_NAME)
        super(BounceProfileSettings, self).set(new_value)

    @set_speed(0, 'gui')
    def get(self):
        raise NotImplementedError()


class DefaultBounceProfileSettings(BaseBounceProfileSettings):
    PROFILE_NAME = ('Profile Name',
                    "//td[input[@name='newName']]")
    SEND_HARD_BOUNCE_MSGS_RADIOGROUP = ('Send Hard Bounce Messages',
                                        {'Yes': "//input[@id='yes_bounces']",
                                         'No': "//input[@id='no_bounces']"})
    HARD_BOUNCE_USE_DSN_FORMAT_RADIOGROUP = ('Use DSN format for bounce messages',
                                             {'Yes': "//input[@id='yes_dsn']",
                                              'No': "//input[@id='no_dsn']"})
    HARD_BOUNCE_USE_BOUNCE_RESPONSE_CODE_RADIOGROUP = \
        ('Parse DSN "Status" field from bounce responses',
         {'Yes': "//input[@id='yes_dsn_parse']",
          'No': "//input[@id='no_dsn_parse']"})
    SEND_DELAY_WARN_MSGS_RADIOGROUP = ('Send Delay Warning Messages',
                                       {'Yes': "//input[@id='yes_warnings']",
                                        'No': "//input[@id='no_warnings']"})
    USE_DKEY_RADIOGROUP = ('Use Domain Key Signing for Bounce and Delay Messages',
                           {'Yes': "//input[@id='sign_bounce_messages1']",
                            'No': "//input[@id='sign_bounce_messages0']"})

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_radio_groups(new_value,
                               self.SEND_HARD_BOUNCE_MSGS_RADIOGROUP,
                               self.HARD_BOUNCE_USE_DSN_FORMAT_RADIOGROUP,
                               self.HARD_BOUNCE_USE_BOUNCE_RESPONSE_CODE_RADIOGROUP,
                               self.SEND_DELAY_WARN_MSGS_RADIOGROUP,
                               self.USE_DKEY_RADIOGROUP)
        super(DefaultBounceProfileSettings, self).set(new_value)

    @set_speed(0, 'gui')
    def get(self):
        raise NotImplementedError()

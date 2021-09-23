#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/admin/log_subscriptions_def/subscription_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.inputs_owner import InputsOwner, CUSTOM_RADIO_FLAG, \
    get_module_inputs_pairs

LOG_TYPE_COMBO = ('Log Type',
                  "//select[@name='type']")
LOG_NAME = ('Log Name',
            "//input[@name='new_id']")
FILE_NAME = ('File Name',
             "//input[@name='filename']")
ROLLOVER_BY_FILESIZE = ('Rollover by File Size',
                        "//input[@name='filesize']")
ROLLOVER_BY_TIME_COMBO = ('Rollover by Time',
                          "//select[@id='rollover_by_time']")
ROLLOVER_CUSTOM_TIME = ('Custom Rollover Interval',
                        "//input[@name='rollover_custom_time']")
LOG_LEVEL_RADIO = lambda index: "//input[@id='level_radio%d']" % (index,)
LOG_LEVEL_RADIOGROUP = ('Log Level',
                        {'Critical': LOG_LEVEL_RADIO(1),
                         'Warning': LOG_LEVEL_RADIO(2),
                         'Information': LOG_LEVEL_RADIO(3),
                         'Debug': LOG_LEVEL_RADIO(4),
                         'Trace': LOG_LEVEL_RADIO(5)})
RETRIEVAL_METHOD_RADIO = lambda index: "//input[@id='method_radio%d']" % \
                                       (index,)
RETRIEVAL_METHOD_RADIOGROUP = ('Retrieval Method',
                               {'Manually Download Logs': RETRIEVAL_METHOD_RADIO(1),
                                'FTP Push to Remote Server': RETRIEVAL_METHOD_RADIO(2),
                                'SCP Push to Remote Server': RETRIEVAL_METHOD_RADIO(3),
                                'Syslog Push': RETRIEVAL_METHOD_RADIO(4)})
# Manually download logs
MAXIMUM_FILES = ('Maximum Files',
                 "//input[@id='max_num_files']")
# FTP Push to Remote Server
FTP_HOST = ('FTP Host',
            "//input[@id='ftp_host']")
FTP_DIRECTORY = ('FTP Directory',
                 "//input[@id='ftp_directory']")
FTP_USERNAME = ('FTP Username',
                "//input[@id='ftp_username']")
FTP_PASSWORD = ('FTP Password',
                "//input[@id='ftp_password']")
# SCP Push to Remote Server
PROTOCOL_RADIO = lambda index: "//input[@id='scp_protocol%s']" % (index,)
PROTOCOL_RADIO_GROUP = ('SCP Protocol',
                        {'SSH1': PROTOCOL_RADIO(1),
                         'SSH2': PROTOCOL_RADIO(2)})
SCP_HOST = ('SCP Host',
            "//input[@id='scp_host']")
SCP_PORT = ('SCP Port',
            "//input[@id='scp_port']")
SCP_DIRECTORY = ('SCP Directory',
                 "//input[@id='scp_directory']")
SCP_USERNAME = ('SCP Username',
                "//input[@id='scp_username']")
ENABLE_HOST_KEY_CHECKING_CHECKBOX = ('Enable Host Key Checking',
                                     "//input[@id='scp_key']")
HOST_KEY_CHECKING_RADIOGROUP = ('Host Key Checking',
                                {'Automatically Scan': "//input[@id='key_method_radio1']",
                                 CUSTOM_RADIO_FLAG: ('input_text',
                                                     'get_value',
                                                     "//textarea[@id='key_value']",
                                                     "//input[@id='key_method_radio2']")})
# Syslog Push
PUSH_HOSTNAME = ('Hostname',
                 "//input[@id='syslog_hostname']")
PUSH_PROTOCOL_RADIO = lambda index: "//input[@id='syslog_protocol%d']" % \
                                    (index,)
PUSH_PROTOCOL_RADIOGROUP = ('Syslog Push Protocol',
                            {'UDP': PUSH_PROTOCOL_RADIO(1),
                             'TCP': PUSH_PROTOCOL_RADIO(2)})
FACILITY_COMBO = ('Facility',
                  "//select[@name='syslog_facility']")


class SubscriptionSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_combos(new_value,
                         LOG_TYPE_COMBO)
        # page reload will happen here
        self.gui.wait_until_page_loaded()

        self._set_radio_groups(new_value,
                               LOG_LEVEL_RADIOGROUP,
                               RETRIEVAL_METHOD_RADIOGROUP)
        self._set_checkboxes(new_value,
                             ENABLE_HOST_KEY_CHECKING_CHECKBOX)
        self._set_radio_groups(new_value,
                               PROTOCOL_RADIO_GROUP,
                               HOST_KEY_CHECKING_RADIOGROUP,
                               PUSH_PROTOCOL_RADIOGROUP)
        self._set_edits(new_value,
                        LOG_NAME, FILE_NAME, ROLLOVER_BY_FILESIZE,
                        MAXIMUM_FILES,
                        FTP_HOST, FTP_DIRECTORY, FTP_USERNAME, FTP_PASSWORD,
                        SCP_HOST, SCP_PORT, SCP_DIRECTORY, SCP_USERNAME,
                        PUSH_HOSTNAME)
        self._set_combos(new_value,
                         ROLLOVER_BY_TIME_COMBO,
                         FACILITY_COMBO)
        self._set_edits(new_value, ROLLOVER_CUSTOM_TIME)

    def get(self):
        raise NotImplementedError()

#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/services/acsm.py#1 $

import re
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

ASA_TBODY_ROW = '//tbody[@id=\"asa_hosts_rowContainer\"]/tr'
ASA_TABLE_FIELD = lambda index, field: 'asa_hosts[%d][%s]' % (index, field,)
GET_FIELD_REGEX = 'asa_hosts\[(\d+)\]\[host\]'
ASA_DEL = lambda index: 'xpath=//*[@id="delete_icon_%s"]' % (index,)
RESULT_CONTAINER = 'id=ASA_container'
ASA_HOST_ROW = lambda index, info_type: "//input[@id=\'asa_hosts[%s][%s]\']"\
            % (index, info_type)
ASA_TEST_TIMEOUT = '5m'

class Acsm(GuiCommon):
    """AnyConnect Secure Mobility page interaction class.
    'Security Services -> AnyConnect Secure Mobility' section.
    """

    def get_keyword_names(self):
        return ['acsm_delete_asa_host',
                'acsm_enable',
                'acsm_edit_settings',
                'acsm_get_settings',
                'acsm_disable',
                'acsm_start_test',]

    def _open_page(self):
        """Open AnyConnect Secure Mobility."""

        self._navigate_to('Security Services', 'AnyConnect Secure Mobility')
        if self._is_text_present('Feature Key Unavailable'):
            raise guiexceptions.GuiFeaturekeyMissingError\
            ("Feature key is missing on page \'AnyConnect Secure Mobility\'")

    def _click_edit_global_settings_button(self):

        edit_global_settings =\
                    "xpath=//input[@value='Edit Global Settings...']"
        self.click_button(edit_global_settings)

    def _enable_or_edit(self):
        """Enable or click edit button."""

        enable_acsm_button = "xpath=//input[@value='Enable...']"
        accept_license_button = "xpath=//input[@value='Accept']"
        if self._check_feature_status(feature='acsm'):
            self._click_edit_global_settings_button()
        else:
            self.click_button(enable_acsm_button)
            if self._is_text_present\
              ('AnyConnect Secure Mobility License Agreement'):
                self.click_button(accept_license_button)

    def _add_asa_info(self, user_info=None):

        asa_passwd_field = 'password'
        self._set_table(len(user_info))
        row_ids = self._get_table_row_data('ids')
        for host, index in zip(user_info, row_ids):
                self._fill_asa_host_row(host, index)
        if user_info[0][2] is not None:
            self.input_text(asa_passwd_field, user_info[0][2])
        else:
            raise guiexceptions.GuiValueError('Remote User info. '\
                                              'Must have a password')

    def _add_ip_range(self, user_info=None):

        ip_range_field = 'ip_range'
        user_info = ','.join(user_info)
        self.input_text(ip_range_field, user_info)

    def _fill_user_info(self, user_info=None, user=None):

        if user_info is not None:
            if user.lower() == 'ip':
                self._add_ip_range(user_info=user_info)
            elif user.lower() == 'asa':
                self._add_asa_info(user_info=tuple([tuple(item.split(':'))\
                                                    for item in user_info]))

    def acsm_delete_asa_host(self, host=None):
        """Delete ASA Host Name from Cisco ASA Integration.

        Parameters:
        - `host`: string with comma separated values of ASA host names/IP
                to be deleted.

        Example:
        | ACSM Delete ASA Host | host=1.1.1.1 |
        | ACSM Delete ASA Host | host=1.1.1.1, 2.2.2.2 |
        """
        if host is not None:
            self._open_page()
            # check if Mobile User Security is disabled or not
            if not self._check_feature_status(feature='acsm'):
                raise guiexceptions.GuiFeatureDisabledError\
                ('Cannot perform delete operation as '\
                            'AnyConnect Secure Mobility is disabled')
            self._click_edit_global_settings_button()
            self._perform_delete_operation(names=host)
            self._click_submit_button()

    def _get_table_row_data(self, data):
        val_list = []
        row_pattern = re.compile(GET_FIELD_REGEX)
        text_fields = self._get_all_fields()
        for field in text_fields:
            result = row_pattern.search(field)
            if result:
                if data == 'values':
                    value = self.get_value\
                        (ASA_TABLE_FIELD(int(result.group(1)), 'host'))
                elif data == 'ids':
                    value = result.group(1)
                val_list.append(value)
        return val_list

    def _perform_delete_operation(self,
                                  names=None):

        names = self._convert_to_tuple(names)
        asa_names = self._get_table_row_data('values')
        for name in names:
            if name not in asa_names:
                raise guiexceptions.GuiControlNotFoundError\
                      ('\'%s\'' % (name,), 'AnyConnect Secure Mobility')
            for i, asa_name in enumerate(asa_names):
                if name == asa_name:
                    self.click_element(ASA_DEL(i), "don't wait")

    def _select_remote_user(self, user=None):

        user_radio_button = {'ip': 'ip_range_radio',
                             'asa': 'asa_integration_radio'}
        if user is not None:
            if user.lower() == 'ip':
                self._click_radio_button(user_radio_button['ip'])
            elif user.lower() == 'asa':
                self._click_radio_button(user_radio_button['asa'])
            else:
                raise ValueError('Invalid input value  \'%s\' for \'users\' ' \
                             'it should either be \'ip\' or \'asa\'' % (user,))

    def acsm_enable(self,
                    user=None,
                    user_info=None):
        """Enable AnyConnect Secure Mobility

        Parameters:
        - `user`: string with Remote Users value, either 'IP' for 'IP Range'
                or 'ASA' for 'Cisco ASA Integration'.
        - `user_info`: define Remote Users information:
            to define IP Range, provide string with comma separated IP range;
            to define ASA, provide string with comma separated
            ASAHost:port:password values.

        Example:
        | ACSM Enable | user=asa | user_info=2.2.2.2:22:ironport, 1.1.1.1:22:ironport |
        | ACSM Enable | user=ip | user_info=1.1.1.1, 1.1.1.2, 1.1.1.3 |
        """
        self._open_page()
        self._enable_or_edit()
        self._select_remote_user(user)
        self._fill_user_info(self._convert_to_tuple(user_info), user)
        self._click_submit_button()

    def acsm_edit_settings(self,
                             user=None,
                             user_info=None):
        """Edit AnyConnect Secure Mobility

        Parameters:
        - `user`: string with Remote Users value, either 'IP' for 'IP Range'
                or 'ASA' for 'Cisco ASA Integration'.
        - `user_info`: define Remote Users information:
            to define IP Range, provide string with comma separated IP range;
            to define ASA, provide string with comma separated
            ASAHost:port:password values.

        Example:
        | ACSM Enable | user=asa | user_info=2.2.2.2:22:ironport, 1.1.1.1:22:ironport |
        | ACSM Enable | user=ip | user_info=1.1.1.1, 1.1.1.2 |
        """
        self._open_page()
        # Check if Mobile User Security Settings already disabled
        if not self._check_feature_status(feature='acsm'):
            raise guiexceptions.GuiFeatureDisabledError\
            ('Cannot edit AnyConnect Secure Mobility as disabled')
        self._click_edit_global_settings_button()
        self._select_remote_user(user)
        self._fill_user_info(self._convert_to_tuple(user_info), user)
        self._click_submit_button()

    def acsm_get_settings(self,):
        """Gets settings of Edit AnyConnect Secure Mobility

        Parameters:
        None

        Example:
        | ${result} | ACSM Get Settings |
        """
        ENTRY_ENTITIES = lambda row,col:\
            '//table[@class=\'pairs\']/tbody/tr[%s]%s' % (str(row),col)
        entries = {}

        self._open_page()
        num_of_entries = int(self.get_matching_xpath_count(ENTRY_ENTITIES('*',''))) + 1
        if num_of_entries > 1:
            for row in xrange(1, num_of_entries):
                name = self.get_text(ENTRY_ENTITIES(row, '/th[1]'))
                value = self.get_text(ENTRY_ENTITIES(row, '/td[1]'))
                entries[name] = value
        return entries

    def acsm_disable(self):
        """Disable AnyConnect Secure Mobility

        Example:
        | Acsm Disable |
        """
        acsm_checkbox = 'enabled'
        self._open_page()
        if not self._check_feature_status(feature='acsm'):
            return
        self._click_edit_global_settings_button()
        self.unselect_checkbox(acsm_checkbox)
        self._click_submit_button()

    def _get_test_results(self):

        self.wait_until_page_contains(text='Test completed',
                                      timeout=ASA_TEST_TIMEOUT)
        test_results = self.get_text(RESULT_CONTAINER)
        return test_results

    def acsm_start_test(self):
        """Run test for the specified ASA host. Keyword returns
        test result as string in debug file.

        Example:
        | Acsm Start Test |
        """
        start_test_button = 'xpath=//*[@id="ASA_start_test"]'
        self._open_page()
        if not self._check_feature_status(feature='acsm'):
            raise guiexceptions.GuiFeatureDisabledError\
             ('Cannot click start test button as AnyConnect Secure Mobility '\
                                                          'is disabled')
        self._click_edit_global_settings_button()
        self.click_button(start_test_button)
        result = self._get_test_results()
        self._info(result)
        if result.find('Errors occurred')  != -1:
            raise guiexceptions.AsaTestError('Errors occurred. See debug '\
                                             'file for more info.')

    def _set_table(self, num_of_rows):

        add_row_field = 'asa_hosts_domtable_AddRow'
        num_of_entries = int(self.get_matching_xpath_count(ASA_TBODY_ROW))
        rows_diff = num_of_rows - num_of_entries
        if rows_diff < 0:
            for i in xrange(abs(rows_diff)):
                self.click_element(ASA_DEL(i), "don't wait")
        elif rows_diff > 0:
            for i in xrange(rows_diff):
                self.click_button(add_row_field, "don't wait")

    def _fill_asa_host_row(self, host, index):

        for entry, link in zip((host[0], host[1]), ('host', 'port')):
            self.input_text(ASA_HOST_ROW(index, link), entry)

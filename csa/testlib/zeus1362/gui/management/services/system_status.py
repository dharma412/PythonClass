#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/gui/management/services/system_status.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.gui.guicommon import GuiCommon
from common.gui import guiexceptions
import re
import time
import urllib2

ERROR_MESSAGE = ""

class SystemStatusCheckError(guiexceptions.GuiError):
    """ Incorrect values were present on the page
    """
    # The special exception the product page validator
    def __init__(self, msg, page_errors=None):
        self.msg = msg
        if page_errors:
            self.page_errors = page_errors
        else:
            self.page_errors = list()

    def __str__(self):
        return str(self.msg) + ':\n\n' + '\n'.join(map(str, self.page_errors))

    # used by Robot Framework to print message to console and log
    def __unicode__(self):
        return unicode(self.__str__())

class SystemStatus(GuiCommon):
    """Keywords for GUI page: Management Appliance -> Centralized Services -> System Status
    """

    def get_keyword_names(self):
        return [
                'system_status_email_spam_quarantine',
                'system_status_email_spam_quarantine_get',
                'system_status_email_spam_quarantine_check',
                'system_status_email_policy_virus_outbreak_quarantines',
                'system_status_email_policy_virus_outbreak_quarantines_get',
                'system_status_email_policy_virus_outbreak_quarantines_check',
                'system_status_email_centralized_reporting',
                'system_status_email_centralized_reporting_get',
                'system_status_email_centralized_reporting_check',
                'system_status_email_centralized_message_tracking',
                'system_status_email_centralized_message_tracking_get',
                'system_status_email_centralized_message_tracking_check',
                'system_status_web_centralized_configuration_manager',
                'system_status_web_centralized_configuration_manager_get',
                'system_status_web_centralized_configuration_manager_check',
                'system_status_web_centralized_reporting',
                'system_status_web_centralized_reporting_get',
                'system_status_web_centralized_reporting_check',
                'system_status_centralized_services',
                'system_status_centralized_services_get',
                'system_status_centralized_services_check',
                'system_status_system_information_uptime',
                'system_status_system_information_uptime_get',
                'system_status_system_information_uptime_check',
                'system_status_system_information_cpu_utilization',
                'system_status_system_information_cpu_utilization_get',
                'system_status_system_information_cpu_utilization_check',
                'system_status_system_information_version_information',
                'system_status_system_information_version_information_get',
                'system_status_system_information_version_information_check',
                'system_status_system_information_hardware',
                'system_status_system_information_hardware_get',
                'system_status_system_information_hardware_check',
                'system_status_system_information',
                'system_status_system_information_get',
                'system_status_system_information_check',
                'system_status_security_appliance_data_transfer_status',
                'system_status_security_appliance_data_transfer_status_get',
                'system_status_security_appliance_data_transfer_status_check',
                'system_status',
                'system_status_get',
                'system_status_check',
                ]

    def _open_page(self):
        """Open 'System Status' page """
        self._navigate_to('Management Appliance', 'Centralized Services', 'System Status')

    def _convert_list_to_dictionary(self, user_input):
        """
        Convert list of pairs ('key:value') to dictionary.
        Pair without column or without key is converted to 'Report:value'
        """
        _result = {}
        for _pair in user_input:
            self._debug(_pair)
            _pos = _pair.find(':')
            if _pos < 0:
                _result['Report'] = _pair.strip()
            elif _pos == 0:
                _result['Report'] = _pair[1:].strip()
            else:
                _result[_pair[0:_pos].strip()] = _pair[_pos + 1:].strip()
        return _result

    def _convert_string_to_dictionary(self, user_input):
        """ Convert string of comma-separated pairs ('key:value') to dictionary.
        Pair without column or without key is converted to 'Report:value'
        """
        _array = str(user_input).split(',')
        return self._convert_list_to_dictionary(_array)

    def _convert_tuple_to_table(self, user_input):
        """ Convert tuple with strings of comma-separated pairs ('key:value') to
        multidimentional list. """
        _first_column_name = None
        _headers = []
        _table = []
        _row = []
        for _user_string in user_input:
            _array = _user_string.split(',')
            for _pair in _array:
                _pos = _pair.find(':')
                if _pos < 0:
                    _name  = 'Report'
                    _value = _pair.strip()
                    if _value == '':
                        continue
                elif _pos == 0:
                    _name  = 'Report'
                    _value = _pair[1:].strip()
                else:
                    _name  = _pair[0:_pos].strip()
                    _value = _pair[_pos + 1:].strip()
                if _first_column_name is None:
                    _first_column_name = _name
                elif _name == _first_column_name:
                    _table.append(list(_row))
                    _row = map(lambda x:'', range(len(_headers)))
                if _name not in _headers:
                    _headers.append(_name)
                    _row.append(_value)
                else:
                    _row[_headers.index(_name)] = _value
        _table.append(list(_row))
        _table.insert(0, _headers)
        self._debug(_table)
        return _table

    def _compare_dicts(self, exp_dict, found_dict, section_name=None):
        """
            Compares two dictionaries and
            returns message for reporting errors.
        """
        message = ''
        if section_name != None:
            section_name = " in '%s' section" % section_name
        else:
            section_name = ''
        for k1 in exp_dict.keys():
            if k1 in found_dict:
                exp_value = exp_dict[k1]
                fnd_value = found_dict[k1]
                if (exp_value == '*'):
                    self._info("'%s' contained value '%s'%s." % (k1, fnd_value, section_name))
                elif (exp_value != fnd_value):
                    message += "\r\n'%s' was '%s' instead of expected '%s'%s." % (k1, fnd_value, exp_value, section_name)
            else:
                message += "\r\n'%s' was not found%s." % (k1, section_name)
        for k2 in found_dict:
            if k2 not in exp_dict:
                message += "\r\n'%s' was not expected%s." % (k2, section_name)
        return message

    def _compare_tables(self, exp_table, fnd_table, section_name=None):
        """
            Compares two-dimentional arrays and
            returns message for reporting errors.
        """
        message = ''
        if section_name != None:
            section_name = " in '%s' section" % section_name
        else:
            section_name = ''

        # Checking column headers from first rows.
        # 'new_exp_head' and 'new_fnd_head' contain matched headers.
        new_exp_head = []
        new_fnd_head = {}
        for exp_head in exp_table[0]:
            if (fnd_table[0].count(exp_head)) == 0:
                message += "\r\n'%s' column was not found%s." % (exp_head, section_name)
            else:
                new_exp_head.append([exp_head, exp_table[0].index(exp_head)])
                new_fnd_head[exp_head] = fnd_table[0].index(exp_head)

        for fnd_head in fnd_table[0]:
            if (exp_table[0].count(fnd_head)) == 0:
                message += "\r\n'%s' column was not expected%s." % (fnd_head, section_name)

        # Creating list of row identifiers by taking values from first column.
        exp_items = []
        for i in range(1, len(exp_table)):
            exp_items.append(exp_table[i][0])

        fnd_items = []
        for i in range(1, len(fnd_table)):
            fnd_items.append(fnd_table[i][0])

        # Checking rows by values in first column.
        # 'new_exp_row' and 'new_fnd_row' contain matched rows.
        new_exp_row = []
        new_fnd_row = {}
        for exp_item in exp_items:
            if (fnd_items.count(exp_item)) == 0:
                message += "\r\n'%s' item was not found%s." % (exp_item, section_name)
            else:
                new_exp_row.append([exp_item, exp_items.index(exp_item)+1])
                new_fnd_row[exp_item] = fnd_items.index(exp_item)+1

        for fnd_item in fnd_items:
            if (exp_items.count(fnd_item)) == 0:
                message += "\r\n'%s' item was not expected%s." % (fnd_item, section_name)

        # Checking values in mached rows and columns
        for row_name, row_num in new_exp_row:
            for col_name, col_num in new_exp_head:
                exp_value = exp_table[row_num][col_num]
                fnd_value = fnd_table[new_fnd_row[row_name]][new_fnd_head[col_name]]
                if (exp_value == '*'):
                    self._info("'%s' column of '%s' row contains value '%s'%s." % (col_name, row_name, fnd_value, section_name))
                elif (exp_value != fnd_value):
                    message += "\r\n'%s' was present instead of expected '%s'%s." % (fnd_value, exp_value, section_name)

        return message

    def _find_section(self, section_path):
        """ Find section by indicating section name and parent headers as path. """
        sections = section_path.split(" > ")
        section_loc = ""
        if(len(sections)>1):
            section_loc += "//dl[contains(@class, 'header')]/dt//*[contains(text(), '" + sections[0] + "')]"
            section_loc += "/ancestor::dt/following-sibling::dd"
        if(len(sections)>2):
            section_loc += "//table[@class='dashboard']//*[contains(text(), '" + sections[1] + "')]"
            section_loc += "/ancestor::table[@class='dashboard']/following-sibling::table"
        section_loc = "(" + section_loc + "//*[contains(text(), '"+sections[len(sections)-1]+"')]" + ")[1]"
        section_loc = "(" + section_loc + "/ancestor-or-self::*[contains(@class, 'header')]" + ")[last()]"
        section_loc = "(" + section_loc + "/ancestor::tr" + ")[last()]"
        section_loc += "/following-sibling::tr"
        section_count = int(self.get_matching_xpath_count(section_loc))
        if section_count < 1:
            raise guiexceptions.GuiControlNotFoundError("'%s' section was not found." % section_path, "System Status")
        return section_loc

    def _find_table(self, section_path):
        """ Find table by indicating section name and parent headers as path. """
        sections = section_path.split(" > ")
        table_loc = ""
        table_loc += "//dl[contains(@class, 'header')]/dt//*[contains(text(), '"+sections[0]+"')]"
        table_loc += "/ancestor::dt/following-sibling::dd"
        if(len(sections)>1):
            table_loc += "//table[@class='dashboard']//*[contains(text(), '"+sections[1]+"')]"
            table_loc += "/ancestor::table[@class='dashboard']/following-sibling::table"
        table_loc += "//thead/parent::table"
        tables_count = int(self.get_matching_xpath_count(table_loc))
        if tables_count < 1:
            raise guiexceptions.GuiControlNotFoundError("Table was not found in '%s' section." % section_path, "System Status")
        return table_loc

    def _get_section_values(self, rows_loc):
        """ Return list of values in a section, specified by section locator. """
        item_list = []
        rows_count = int(self.get_matching_xpath_count(rows_loc))
        for row_num in range(1, rows_count+1):
            inner_tables_count = int(self.get_matching_xpath_count("(" + rows_loc + ")["+str(row_num)+"]//table"))
            if inner_tables_count > 0:
                row_list = []
                items_loc = "(" + rows_loc + ")["+str(row_num)+"]/*"
                items_count = self.get_matching_xpath_count(items_loc)
                for i in range(1, int(items_count)+1):
                    item_text = self.get_text("xpath=("+items_loc+")["+str(i)+"]")
                    item_text = item_text.strip()
                    self._debug("xpath=("+items_loc+")["+str(i)+"]")
                    self._debug(item_text)
                    row_list.append(item_text)
                item_list.append(row_list)
            else:
                item_text = self.get_text("xpath=("+rows_loc+")["+str(row_num)+"]")
                item_text = item_text.strip()
                item_list.append(item_text)
            last_row = self.get_matching_xpath_count("("+rows_loc+")["+str(row_num)+"]/self::*[contains(@class, 'last_row')]")
            if int(last_row) > 0: break
        if len(item_list) == 1 and isinstance(item_list[0], list):
            return item_list[0]
        else:
            return item_list

    def _get_table_values(self, tables_loc):
        """ Return list of values in a table or tables, specified by table locator. """
        tables_list = []
        tables_count = int(self.get_matching_xpath_count(tables_loc))
        for table_num in range(1, 1 + tables_count ):
            table_list = []
            table_loc = "("+tables_loc+")["+str(table_num)+"]"
            table_head = table_loc+"/thead"
            table_head_lastrow = table_head + "/tr[last()]"

            head_list = []
            for th_num in range(1, 1+int(self.get_matching_xpath_count(table_head_lastrow+"/th"))):
                th_value = self.get_text("xpath="+table_head_lastrow+"/th["+str(th_num)+"]")
                head_list.append(th_value)
            table_list.append(head_list)
            table_body = table_loc+"/tbody[@style='']"
            for tr_num in range(1, 1+int(self.get_matching_xpath_count(table_body+"/tr"))):
                row_list = []
                for td_num in range(1, 1+int(self.get_matching_xpath_count(table_body+"/tr["+str(tr_num)+"]/td"))):
                    td_value = self.get_text("xpath="+table_body+"/tr["+str(tr_num)+"]/td["+str(td_num)+"]")
                    row_list.append(td_value)
                table_list.append(row_list)
            tables_list.append(table_list)

        if len(tables_list)==1:
            return tables_list[0]
        else:
            return tables_list

    def _process_section(self, section_name, expected_values=None):
        """ Process getting or checking a section, specified by section full name (with names of parent headers). """
        rows_loc = self._find_section(section_name)
        actual_list = self._get_section_values(rows_loc)

        self._debug("Expected table:")
        self._debug(expected_values)
        self._debug("Actual_table:")
        self._debug(actual_list)

        if expected_values and expected_values is not None:
            actual_dict = self._convert_list_to_dictionary(actual_list)
            expected_dict = self._convert_string_to_dictionary(expected_values)
            global ERROR_MESSAGE
            ERROR_MESSAGE += self._compare_dicts(expected_dict, actual_dict, section_name)

        return actual_list

    def _process_table(self, section_name, expected_values=None):
        """ Process getting or checking a table, specified by section full name (with names of parent headers). """
        _tbl_loc = self._find_table(section_name)
        _actual_table = self._get_table_values(_tbl_loc)

        self._debug("Expected table:")
        self._debug(expected_values)
        self._debug("Actual_table:")
        self._debug(_actual_table)

        if expected_values is None:
            return _actual_table

        if isinstance(expected_values, (str, unicode)):
            expected_values = tuple([expected_values])

        if len(expected_values) > 0:
            _expected_table = self._convert_tuple_to_table(expected_values)
            self._debug("Expected table:")
            self._debug(_expected_table)
            self._debug("Actual_table:")
            self._debug(_actual_table)
            global ERROR_MESSAGE
            ERROR_MESSAGE += self._compare_tables(_expected_table, _actual_table, section_name)

        return _actual_table

    def system_status_email_spam_quarantine(self, expected_values=None):
        """Get or check 'Centralized Services > Email Security > Spam Quarantine'
        data from 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.
                If this parameter was skipped, the keyword returns
                list of values in the section

        Return:
            - List of values in the section, if expectations were not indicated.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${spam_quar}= | System Status Email Spam Quarantine |
        | Log Many | ${spam_quar} |
        | System Status Email Spam Quarantine | Disk Quota Used:0.0%, Messages:0, Not enabled |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        _section_name = "Centralized Services > Email Security > Spam Quarantine"
        _return_list = self._process_section(_section_name, expected_values)

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_email_spam_quarantine_get(self):
        """Get 'Centralized Services > Email Security > Spam Quarantine'
        data from 'System Status' page.

        Return:
            - List of values in the section.

        Examples:
        | ${spam_quar}= | System Status Email Spam Quarantine Get |
        | Log Many | ${spam_quar} |
        """

        return self.system_status_email_spam_quarantine()

    def system_status_email_spam_quarantine_check(self, expected_values):
        """Check 'Centralized Services > Email Security > Spam Quarantine'
        data on 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status Email Spam Quarantine Check | Disk Quota Used:0.0%, Messages:0, Not enabled  |
        """

        return self.system_status_email_spam_quarantine(expected_values)

    def system_status_email_policy_virus_outbreak_quarantines(self, expected_values=None):
        """Get or check 'Centralized Services > Email Security > Policy, Virus and Outbreak Quarantines'
        data from 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.
                If this parameter was skipped, the keyword returns
                list of values in the section

        Return:
            - List of values in the section, if expectations were not indicated.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${pvo_quar}= | System Status Email Policy Virus Outbreak Quarantines |
        | Log Many | ${pvo_quar} |
        | System Status Email Policy Virus Outbreak Quarantines | Disk Quota Used:0.0%, Messages:0, Not enabled |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        _section_name = "Centralized Services > Email Security > Policy, Virus and Outbreak Quarantines"
        _return_list = self._process_section(_section_name, expected_values)

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list


    def system_status_email_policy_virus_outbreak_quarantines_get(self):
        """Get 'Centralized Services > Email Security > Policy, Virus and Outbreak Quarantines'
        data from 'System Status' page.

        Return:
            - List of values in the section.

        Examples:
        | ${pvo_quar}= | System Status Email Policy Virus Outbreak Quarantines Get |
        | Log Many | ${pvo_quar} |
        """

        return self.system_status_email_policy_virus_outbreak_quarantines()

    def system_status_email_policy_virus_outbreak_quarantines_check(self, expected_values):
        """Check 'Centralized Services > Email Security > Policy, Virus and Outbreak Quarantines'
        data on 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status Email Policy Virus Outbreak Quarantines Check | Disk Quota Used:0.0%, Messages:0, Not enabled  |
        """

        return self.system_status_email_policy_virus_outbreak_quarantines(expected_values)


    def system_status_email_centralized_reporting(self, expected_values=None):
        """Get or check 'Centralized Services > Email Security > Centralized Reporting'
        data from 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.
                If this parameter was skipped, the keyword returns
                list of values in the section

        Return:
            - List of values in the section, if expectations were not indicated.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${email_report}= | System Status Email Centralized Reporting |
        | Log Many | ${email_report} |
        | System Status Email Centralized Reporting | Processing Queue:0.0%, Status:0, Email Overview Report |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        _section_name = "Centralized Services > Email Security > Centralized Reporting"
        _return_list = self._process_section(_section_name, expected_values)

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_email_centralized_reporting_get(self):
        """Get 'Centralized Services > Email Security > Centralized Reporting'
        data from 'System Status' page.

        Return:
            - List of values in the section.

        Examples:
        | ${email_report}= | System Status Email Centralized Reporting Get |
        | Log Many | ${email_report} |
        """

        return self.system_status_email_centralized_reporting()

    def system_status_email_centralized_reporting_check(self, expected_values):
        """Check 'Centralized Services > Email Security > Centralized Reporting'
        data on 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status Email Centralized Reporting Check | Processing Queue:0.0%, Status:0, Email Overview Report |
        """

        return self.system_status_email_centralized_reporting(expected_values)

    def system_status_email_centralized_message_tracking(self, expected_values=None):
        """Get or check 'Centralized Services > Email Security > Centralized Message Tracking '
        data from 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.
                If this parameter was skipped, the keyword returns
                list of values in the section

        Return:
            - List of values in the section, if expectations were not indicated.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${email_track}= | System Status Email Centralized Message Tracking  |
        | Log Many | ${email_track} |
        | System Status Email Centralized Message Tracking  | Processing Queue:0.0%, Status:0, Track Messages |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        _section_name = "Centralized Services > Email Security > Centralized Message Tracking"
        _return_list = self._process_section(_section_name, expected_values)

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_email_centralized_message_tracking_get(self):
        """Get 'Centralized Services > Email Security > Centralized Message Tracking '
        data from 'System Status' page.

        Return:
            - List of values in the section.

        Examples:
        | ${email_track}= | System Status Email Centralized Message Tracking Get |
        | Log Many | ${email_track} |
        """

        return self.system_status_email_centralized_message_tracking()

    def system_status_email_centralized_message_tracking_check(self, expected_values):
        """Check 'Centralized Services > Email Security > Centralized Message Tracking '
        data on 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status Email Centralized Message Tracking Check | Processing Queue:0.0%, Status:0, Track Messages |
        """

        return self.system_status_email_centralized_message_tracking(expected_values)

    def system_status_web_centralized_configuration_manager(self, expected_values=None):
        """Get or check 'Centralized Services > Web Security > Centralized Configuration Manager'
        data from 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.
                If this parameter was skipped, the keyword returns
                list of values in the section

        Return:
            - List of values in the section, if expectations were not indicated.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${web_manager}= | System Status Web Centralized Configuration Manager |
        | Log Many | ${web_manager} |
        | System Status Web Centralized Configuration Manager | Processing Queue:0.0%, Status:0, Web Overview Report |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        _section_name = "Centralized Services > Web Security > Centralized Configuration Manager"
        _return_list = self._process_section(_section_name, expected_values)

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_web_centralized_configuration_manager_get(self):
        """Get 'Centralized Services > Web Security > Centralized Configuration Manager'
        data from 'System Status' page.

        Return:
            - List of values in the section.

        Examples:
        | ${web_manager}= | System Status Web Centralized Configuration Manager Get |
        | Log Many | ${web_manager} |
        """

        return self.system_status_web_centralized_configuration_manager()

    def system_status_web_centralized_configuration_manager_check(self, expected_values):
        """Check 'Centralized Services > Web Security > Centralized Configuration Manager'
        data on 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status Web Centralized Configuration Manager Check | Processing Queue:0.0%, Status:0, Web Overview Report |
        """

        return self.system_status_web_centralized_configuration_manager(expected_values)

    def system_status_web_centralized_reporting(self, expected_values=None):
        """Get or check 'Centralized Services > Web Security > Centralized Reporting'
        data from 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.
                If this parameter was skipped, the keyword returns
                list of values in the section

        Return:
            - List of values in the section, if expectations were not indicated.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${web_report}= | System Status Web Centralized Reporting |
        | Log Many | ${web_report} |
        | System Status Web Centralized Reporting | Processing Queue:0.0%, Status:0, Web Overview Report |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        _section_name = "Centralized Services > Web Security > Centralized Reporting"
        _return_list = self._process_section(_section_name, expected_values)

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_web_centralized_reporting_get(self):
        """Get 'Centralized Services > Web Security > Centralized Reporting'
        data from 'System Status' page.

        Return:
            - List of values in the section.

        Examples:
        | ${web_report}= | System Status Web Centralized Reporting Get |
        | Log Many | ${web_report} |
        """

        return self.system_status_web_centralized_reporting()

    def system_status_web_centralized_reporting_check(self, expected_values):
        """Check 'Centralized Services > Web Security > Centralized Reporting'
        data on 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status Web Centralized Reporting Check | Processing Queue:0.0%, Status:0, Web Overview Report |
        """

        return self.system_status_web_centralized_reporting(expected_values)


    def system_status_centralized_services(self, expected_email_spam_quar=None,
            expected_email_centr_report=None, expected_email_centr_track=None,
            expected_web_centr_manag=None, expected_web_centr_report=None):
        """Get or check Centralized Services part of System Status.

        Parameters:
            Every parameter should be indicated as a string of comma-separated pairs with expectations.
            Pair contains label and expected value, separated by colon (like 'label:value').
            If value = *, related item is not checked on the page.
            - `expected_email_spam_quar`: Expectations for
                    'Email Security > Spam Quarantine'
            - `expected_email_centr_report`: Expectations for
                    'Email Security > Centralized Reporting'
            - `expected_email_centr_track`: Expectations for
                    'Email Security > Centralized Message Tracking'
            - `expected_web_centr_manag`: Expectations for
                    'Web Security > Centralized Configuration Manager'
            - `expected_web_centr_report`: Expectations for
                    'Web Security > Centralized Reporting'

        Return:
            - List of values in tables.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${system_status}= | System Status Centralized Services |
        | Log Many | ${system_status} |
        | System Status Centralized Services |
        | ... | expected_email_spam_quar=Disk Quota Used:0.0%, Messages:0, Not enabled |
        | ... | expected_email_centr_report=Processing Queue:0.0%, Status:Not enabled, Email Overview Report |
        | ... | expected_email_centr_track=Processing Queue:0.0%, Status:Not enabled, Track Messages |
        | ... | expected_web_centr_manag=Processing Queue:0.0%, Status:Not enabled, View Appliance Status List |
        | ... | expected_web_centr_report=Processing Queue:0.0%, Status:Not enabled, Web Overview Report |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''
        _return_list=[]

        _section_name = "Centralized Services > Email Security > Spam Quarantine"
        _return_list.append(self._process_section(_section_name, expected_email_spam_quar))

        _section_name = "Centralized Services > Email Security > Centralized Reporting"
        _return_list.append(self._process_section(_section_name, expected_email_centr_report))

        _section_name = "Centralized Services > Email Security > Centralized Message Tracking"
        _return_list.append(self._process_section(_section_name, expected_email_centr_track))

        _section_name = "Centralized Services > Web Security > Centralized Configuration Manager"
        _return_list.append(self._process_section(_section_name, expected_web_centr_manag))

        _section_name = "Centralized Services > Web Security > Centralized Reporting"
        _return_list.append(self._process_section(_section_name, expected_web_centr_report))

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_centralized_services_get(self):
        """Get Centralized Services part of System Status.

        Return:
            - List of values in tables.

        Examples:
        | ${system_status}= | System Status Centralized Services |
        | Log Many | ${system_status} |
        """
        return self.system_status_centralized_services()

    def system_status_centralized_services_check(self, expected_email_spam_quar=None,
            expected_email_centr_report=None, expected_email_centr_track=None,
            expected_web_centr_manag=None, expected_web_centr_report=None):
        """Check Centralized Services part of System Status.

        Parameters:
            Every parameter should be indicated as a string of comma-separated pairs with expectations.
            Pair contains label and expected value, separated by colon (like 'label:value').
            If value = *, related item is not checked on the page.
            - `expected_email_spam_quar`: Expectations for
                    'Email Security > Spam Quarantine'
            - `expected_email_centr_report`: Expectations for
                    'Email Security > Centralized Reporting'
            - `expected_email_centr_track`: Expectations for
                    'Email Security > Centralized Message Tracking'
            - `expected_web_centr_manag`: Expectations for
                    'Web Security > Centralized Configuration Manager'
            - `expected_web_centr_report`: Expectations for
                    'Web Security > Centralized Reporting'

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status Centralized Services |
        | ... | expected_email_spam_quar=Disk Quota Used:0.0%, Messages:0, Not enabled |
        | ... | expected_email_centr_report=Processing Queue:0.0%, Status:Not enabled, Email Overview Report |
        | ... | expected_email_centr_track=Processing Queue:0.0%, Status:Not enabled, Track Messages |
        | ... | expected_web_centr_manag=Processing Queue:0.0%, Status:Not enabled, View Appliance Status List |
        | ... | expected_web_centr_report=Processing Queue:0.0%, Status:Not enabled, Web Overview Report |
        """

        return self.system_status_centralized_services(expected_email_spam_quar,
            expected_email_centr_report, expected_email_centr_track,
            expected_web_centr_manag, expected_web_centr_report)


    def system_status_system_information_uptime(self, expected_values=None):
        """Get or check 'System Information > Uptime'
        data from 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.
                If this parameter was skipped, the keyword returns
                list of values in the section

        Return:
            - List of values in the section, if expectations were not indicated.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${uptime}= | System Status System Information Uptime |
        | Log Many | ${uptime} |
        | System Status System Information Uptime | Appliance Up Since:* |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        _section_name = "System Information > Uptime"
        _return_list = self._process_section(_section_name, expected_values)

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_system_information_uptime_get(self):
        """Get 'System Information > Uptime'
        data from 'System Status' page.

        Return:
            - List of values in the section.

        Examples:
        | ${uptime}= | System Status System Information Uptime Get |
        | Log Many | ${uptime} |
        """

        return self.system_status_system_information_uptime()

    def system_status_system_information_uptime_check(self, expected_values):
        """Check 'System Information > Uptime'
        data on 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status System Information Uptime Check | Appliance Up Since:* |
        """

        return self.system_status_system_information_uptime(expected_values)

    def system_status_system_information_cpu_utilization(self, expected_values=None):
        """Get or check 'System Information > CPU Utilization'
        data from 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.
                If this parameter was skipped, the keyword returns
                list of values in the section

        Return:
            - List of values in the section, if expectations were not indicated.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${cpu_utilization}= | System Status System Information CPU Utilization |
        | Log Many | ${cpu_utilization} |
        | System Status System Information CPU Utilization | Security Management Appliance:0.0%,
            Quarantine Service:0.0%, Reporting Service:0.0%, Tracking Service:0.0%, Total CPU Utilization:0.0% |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        _section_name = "System Information > CPU Utilization"
        _return_list = self._process_section(_section_name, expected_values)

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_system_information_cpu_utilization_get(self):
        """Get 'System Information > CPU Utilization'
        data from 'System Status' page.

        Return:
            - List of values in the section.

        Examples:
        | ${cpu_utilization}= | System Status System Information CPU Utilization Get |
        | Log Many | ${cpu_utilization} |
        """

        return self.system_status_system_information_cpu_utilization()

    def system_status_system_information_cpu_utilization_check(self, expected_values):
        """Check 'System Information > CPU Utilization'
        data on 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status System Information CPU Utilization Check | Security Management Appliance:0.0%,
            Quarantine Service:0.0%, Reporting Service:0.0%, Tracking Service:0.0%, Total CPU Utilization:0.0% |
        """

        return self.system_status_system_information_cpu_utilization(expected_values)

    def system_status_system_information_version_information(self, expected_values=None):
        """Get or check 'System Information > Version Information'
        data from 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.
                If this parameter was skipped, the keyword returns
                list of values in the section

        Return:
            - List of values in the section, if expectations were not indicated.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${version_information}= | System Status System Information Version Information |
        | Log Many | ${version_information} |
        | System Status System Information Version Information | Model:M650,
            Operating System:7.8.0-555, Build Date:27 Jan 2012 00:00 (GMT),
            Install Date:30 Jan 2012 14:42 (GMT), Serial Number:00188B3D2A21-CDLB0C1 |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        _section_name = "System Information > Version Information"
        _return_list = self._process_section(_section_name, expected_values)

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_system_information_version_information_get(self):
        """Get 'System Information > Version Information'
        data from 'System Status' page.

        Return:
            - List of values in the section.

        Examples:
        | ${version_information}= | System Status System Information Version Information Get |
        | Log Many | ${version_information} |
        """

        return self.system_status_system_information_version_information()

    def system_status_system_information_version_information_check(self, expected_values):
        """Check 'System Information > Version Information'
        data on 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status System Information Version Information Check | Model:M650,
            Operating System:7.8.0-555, Build Date:27 Jan 2012 00:00 (GMT),
            Install Date:30 Jan 2012 14:42 (GMT), Serial Number:00188B3D2A21-CDLB0C1 |
        """

        return self.system_status_system_information_version_information(expected_values)

    def system_status_system_information_hardware(self, expected_values=None):
        """Get or check 'System Information > Hardware'
        data from 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.
                If this parameter was skipped, the keyword returns
                list of values in the section

        Return:
            - List of values in the section, if expectations were not indicated.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${hardware}= | System Status System Information Hardware |
        | Log Many | ${hardware} |
        | System Status System Information Hardware | RAID Status:Degraded |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        _section_name = "System Information > Hardware"
        _return_list = self._process_section(_section_name, expected_values)

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_system_information_hardware_get(self):
        """Get 'System Information > Hardware'
        data from 'System Status' page.

        Return:
            - List of values in the section.

        Examples:
        | ${hardware}= | System Status System Information Hardware Get |
        | Log Many | ${hardware} |
        """

        return self.system_status_system_information_hardware()

    def system_status_system_information_hardware_check(self, expected_values):
        """Check 'System Information > Hardware'
        data on 'System Status' page.

        Parameters:
            - `expected_values`: String of comma-separated pairs with expectations for the section.
                (Items in a pair are separated by colon like 'key:value').
                If expected value equal *, key value is not checked.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status System Information Hardware Check | RAID Status:Degraded |
        """

        return self.system_status_system_information_hardware(expected_values)

    def system_status_system_information(self,
            expected_sys_uptime=None, expected_sys_cpu=None,
            expected_sys_version=None, expected_sys_hardware=None):
        """Get or check System Information part of System Status.

        Parameters:
            Every parameter should be indicated as a string of comma-separated pairs with expectations.
            Pair contains label and expected value, separated by colon (like 'label:value').
            If value = *, related item is not checked on the page.
            - `expected_sys_uptime`: Expectations for
                    'System Information > Uptime'
            - `expected_sys_cpu`: Expectations for
                    'System Information > CPU Utilization'
            - `expected_sys_version`: Expectations for
                    'System Information > Version Information'
            - `expected_sys_hardware`: Expectations for
                    'System Information > Hardware'

        Return:
            - List of values in the section.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${system_status}= | System Status System Information |
        | Log Many | ${system_status} |
        | System Status System Information |
        | ... | expected_sys_uptime=Appliance Up Since:* |
        | ... | expected_sys_cpu=Security Management Appliance:0.0%, Quarantine Service:0.0%, Reporting Service:0.0%, Tracking Service:0.0%, Total CPU Utilization:0.0% |
        | ... | expected_sys_version=Model:M650, Operating System:7.8.0-555, Build Date:27 Jan 2012 00:00 (GMT), Install Date:30 Jan 2012 14:42 (GMT), Serial Number:00188B3D2A21-CDLB0C1 |
        | ... | expected_sys_hardware=RAID Status:Degraded |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''
        _return_list=[]

        _section_name = "System Information > Uptime"
        _return_list.append(self._process_section(_section_name, expected_sys_uptime))

        _section_name = "System Information > CPU Utilization"
        _return_list.append(self._process_section(_section_name, expected_sys_cpu))

        _section_name = "System Information > Version Information"
        _return_list.append(self._process_section(_section_name, expected_sys_version))

        _section_name = "System Information > Hardware"
        _return_list.append(self._process_section(_section_name, expected_sys_hardware))

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_system_information_get(self):
        """Get System Information part of System Status.

        Return:
            - List of values in the section.

        Examples:
        | ${system_status}= | System Status System Information |
        | Log Many | ${system_status} |
        """
        return self.system_status_system_information()

    def system_status_system_information_check(self, expected_email_spam_quar=None,
            expected_email_centr_report=None, expected_email_centr_track=None,
            expected_web_centr_manag=None, expected_web_centr_report=None,
            expected_sys_uptime=None, expected_sys_cpu=None,
            expected_sys_version=None, expected_sys_hardware=None,
            expected_appliance_status=None):
        """Check System Information part of System Status.

        Parameters:
            Every parameter should be indicated as a string of comma-separated pairs with expectations.
            Pair contains label and expected value, separated by colon (like 'label:value').
            If value = *, related item is not checked on the page.
            - `expected_sys_uptime`: Expectations for
                    'System Information > Uptime'
            - `expected_sys_cpu`: Expectations for
                    'System Information > CPU Utilization'
            - `expected_sys_version`: Expectations for
                    'System Information > Version Information'
            - `expected_sys_hardware`: Expectations for
                    'System Information > Hardware'

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status System Information |
        | ... | expected_sys_uptime=Appliance Up Since:* |
        | ... | expected_sys_cpu=Security Management Appliance:0.0%, Quarantine Service:0.0%, Reporting Service:0.0%, Tracking Service:0.0%, Total CPU Utilization:0.0% |
        | ... | expected_sys_version=Model:M650, Operating System:7.8.0-555, Build Date:27 Jan 2012 00:00 (GMT), Install Date:30 Jan 2012 14:42 (GMT), Serial Number:00188B3D2A21-CDLB0C1 |
        | ... | expected_sys_hardware=RAID Status:Degraded |
        """

        return self.system_status_system_information(expected_sys_uptime, expected_sys_cpu,
            expected_sys_version, expected_sys_hardware)

    def system_status_security_appliance_data_transfer_status(self, *expected_values):
        """Get or check 'Security Appliance Data Transfer Status'
        data from 'System Status' page.

        Parameters:
            Every expectation for a row of the table should be indicated as
            a string of comma-separated pairs with expectations.
            Pair contains label and expected value, separated by colon (like 'label:value').
            If value = *, related item is not checked on the page.
            Indicating of an expectation for 'Name' column is required.

        Return:
            - List of values in the table, if expectations were not indicated.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${appliances}= | System Status Security Appliance Data Transfer Status |
        | Log Many | ${appliances} |
        | System Status Security Appliance Data Transfer Status |
        | ... | Name:c670s01.sma, IP Address or Hostname:10.92.154.113, Type:Email, Status:*, Services:* |
        | ... | Name:wsa102.wga, IP Address or Hostname:10.7.8.98, Type:Web, Status:*, Services:* |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''

        _section_name = "Security Appliance Data Transfer Status"
        _return_list = self._process_table(_section_name, expected_values)

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_security_appliance_data_transfer_status_get(self):
        """Get 'Security Appliance Data Transfer Status'
        data from 'System Status' page.

        Return:
            - List of values in the table.

        Examples:
        | ${appliances}= | System Status Security Appliance Data Transfer Status |
        | Log Many | ${appliances} |
        """

        return self.system_status_security_appliance_data_transfer_status()

    def system_status_security_appliance_data_transfer_status_check(self, *expected_values):
        """Check 'Security Appliance Data Transfer Status'
        data from 'System Status' page.

        Parameters:
            Every expectation for a row of the table should be indicated as
            a string of comma-separated pairs with expectations.
            Pair contains label and expected value, separated by colon (like 'label:value').
            If value = *, related item is not checked on the page.
            Indicating of an expectation for 'Name' column is required.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status Security Appliance Data Transfer Status |
        | ... | Name:c670s01.sma, IP Address or Hostname:10.92.154.113, Type:Email, Status:*, Services:* |
        | ... | Name:wsa102.wga, IP Address or Hostname:10.7.8.98, Type:Web, Status:*, Services:* |
        """

        return self.system_status_security_appliance_data_transfer_status(*expected_values)

    def system_status(self, expected_email_spam_quar=None,
            expected_email_centr_report=None, expected_email_centr_track=None,
            expected_web_centr_manag=None, expected_web_centr_report=None,
            expected_sys_uptime=None, expected_sys_cpu=None,
            expected_sys_version=None, expected_sys_hardware=None,
            expected_appliance_status=None):
        """Get or check System Status.

        Parameters:
            Every parameter should be indicated as a string of comma-separated pairs with expectations.
            Pair contains label and expected value, separated by colon (like 'label:value').
            If value = *, related item is not checked on the page.
            - `expected_email_spam_quar`: Expectations for
                    'Email Security > Spam Quarantine'
            - `expected_email_centr_report`: Expectations for
                    'Email Security > Centralized Reporting'
            - `expected_email_centr_track`: Expectations for
                    'Email Security > Centralized Message Tracking'
            - `expected_web_centr_manag`: Expectations for
                    'Web Security > Centralized Configuration Manager'
            - `expected_web_centr_report`: Expectations for
                    'Web Security > Centralized Reporting'
            - `expected_sys_uptime`: Expectations for
                    'System Information > Uptime'
            - `expected_sys_cpu`: Expectations for
                    'System Information > CPU Utilization'
            - `expected_sys_version`: Expectations for
                    'System Information > Version Information'
            - `expected_sys_hardware`: Expectations for
                    'System Information > Hardware'
            - `expected_appliance_status`: Expectations for
                    'Security Appliance Data Transfer Status' table

        Return:
            - List of values in tables.

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | ${system_status}= | System Status |
        | Log Many | ${system_status} |
        | System Status |
        | ... | expected_email_spam_quar=Disk Quota Used:0.0%, Messages:0, Not enabled |
        | ... | expected_email_centr_report=Processing Queue:0.0%, Status:Not enabled, Email Overview Report |
        | ... | expected_email_centr_track=Processing Queue:0.0%, Status:Not enabled, Track Messages |
        | ... | expected_web_centr_manag=Processing Queue:0.0%, Status:Not enabled, View Appliance Status List |
        | ... | expected_web_centr_report=Processing Queue:0.0%, Status:Not enabled, Web Overview Report |
        | ... | expected_sys_uptime=Appliance Up Since:* |
        | ... | expected_sys_cpu=Security Management Appliance:0.0%, Quarantine Service:0.0%, Reporting Service:0.0%, Tracking Service:0.0%, Total CPU Utilization:0.0% |
        | ... | expected_sys_version=Model:M650, Operating System:7.8.0-555, Build Date:27 Jan 2012 00:00 (GMT), Install Date:30 Jan 2012 14:42 (GMT), Serial Number:00188B3D2A21-CDLB0C1 |
        | ... | expected_sys_hardware=RAID Status:Degraded |
        | ... | expected_appliance_status=Name:c670s01.sma, IP Address or Hostname:10.92.154.113, Type:Email, Status:*, Services:*, Name:wsa102.wga, IP Address or Hostname:10.7.8.98, Type:Web, Status:*, Services:* |
        """
        self._open_page()

        global ERROR_MESSAGE
        ERROR_MESSAGE = ''
        _return_list=[]

        _section_name = "Centralized Services > Email Security > Spam Quarantine"
        _return_list.append(self._process_section(_section_name, expected_email_spam_quar))

        _section_name = "Centralized Services > Email Security > Centralized Reporting"
        _return_list.append(self._process_section(_section_name, expected_email_centr_report))

        _section_name = "Centralized Services > Email Security > Centralized Message Tracking"
        _return_list.append(self._process_section(_section_name, expected_email_centr_track))

        _section_name = "Centralized Services > Web Security > Centralized Configuration Manager"
        _return_list.append(self._process_section(_section_name, expected_web_centr_manag))

        _section_name = "Centralized Services > Web Security > Centralized Reporting"
        _return_list.append(self._process_section(_section_name, expected_web_centr_report))

        _section_name = "System Information > Uptime"
        _return_list.append(self._process_section(_section_name, expected_sys_uptime))

        _section_name = "System Information > CPU Utilization"
        _return_list.append(self._process_section(_section_name, expected_sys_cpu))

        _section_name = "System Information > Version Information"
        _return_list.append(self._process_section(_section_name, expected_sys_version))

        _section_name = "System Information > Hardware"
        _return_list.append(self._process_section(_section_name, expected_sys_hardware))

        _section_name = "Security Appliance Data Transfer Status"
        _return_list.append(self._process_table(_section_name, expected_appliance_status))

        if ERROR_MESSAGE != '':
            raise SystemStatusCheckError(ERROR_MESSAGE)

        return _return_list

    def system_status_get(self):
        """Get System Status.

        Return:
            - List of values in tables.

        Examples:
        | ${system_status}= | System Status |
        | Log Many | ${system_status} |
        """
        return self.system_status()

    def system_status_check(self, expected_email_spam_quar=None,
            expected_email_centr_report=None, expected_email_centr_track=None,
            expected_web_centr_manag=None, expected_web_centr_report=None,
            expected_sys_uptime=None, expected_sys_cpu=None,
            expected_sys_version=None, expected_sys_hardware=None,
            expected_appliance_status=None):
        """Check System Status.

        Parameters:
            Every parameter should be indicated as a string of comma-separated pairs with expectations.
            Pair contains label and expected value, separated by colon (like 'label:value').
            If value = *, related item is not checked on the page.
            - `expected_email_spam_quar`: Expectations for
                    'Email Security > Spam Quarantine'
            - `expected_email_centr_report`: Expectations for
                    'Email Security > Centralized Reporting'
            - `expected_email_centr_track`: Expectations for
                    'Email Security > Centralized Message Tracking'
            - `expected_web_centr_manag`: Expectations for
                    'Web Security > Centralized Configuration Manager'
            - `expected_web_centr_report`: Expectations for
                    'Web Security > Centralized Reporting'
            - `expected_sys_uptime`: Expectations for
                    'System Information > Uptime'
            - `expected_sys_cpu`: Expectations for
                    'System Information > CPU Utilization'
            - `expected_sys_version`: Expectations for
                    'System Information > Version Information'
            - `expected_sys_hardware`: Expectations for
                    'System Information > Hardware'
            - `expected_appliance_status`: Expectations for
                    'Security Appliance Data Transfer Status' table

        Exceptions:
            - `SystemStatusCheckError`: the exception appears if values on the page are not equal to expected.

        Examples:
        | System Status |
        | ... | expected_email_spam_quar=Disk Quota Used:0.0%, Messages:0, Not enabled |
        | ... | expected_email_centr_report=Processing Queue:0.0%, Status:Not enabled, Email Overview Report |
        | ... | expected_email_centr_track=Processing Queue:0.0%, Status:Not enabled, Track Messages |
        | ... | expected_web_centr_manag=Processing Queue:0.0%, Status:Not enabled, View Appliance Status List |
        | ... | expected_web_centr_report=Processing Queue:0.0%, Status:Not enabled, Web Overview Report |
        | ... | expected_sys_uptime=Appliance Up Since:* |
        | ... | expected_sys_cpu=Security Management Appliance:0.0%, Quarantine Service:0.0%, Reporting Service:0.0%, Tracking Service:0.0%, Total CPU Utilization:0.0% |
        | ... | expected_sys_version=Model:M650, Operating System:7.8.0-555, Build Date:27 Jan 2012 00:00 (GMT), Install Date:30 Jan 2012 14:42 (GMT), Serial Number:00188B3D2A21-CDLB0C1 |
        | ... | expected_sys_hardware=RAID Status:Degraded |
        | ... | expected_appliance_status=Name:c670s01.sma, IP Address or Hostname:10.92.154.113, Type:Email, Status:*, Services:*, Name:wsa102.wga, IP Address or Hostname:10.7.8.98, Type:Web, Status:*, Services:* |
        """

        return self.system_status(expected_email_spam_quar,
            expected_email_centr_report, expected_email_centr_track,
            expected_web_centr_manag, expected_web_centr_report,
            expected_sys_uptime, expected_sys_cpu,
            expected_sys_version, expected_sys_hardware,
            expected_appliance_status)

#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_setup.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $
import sys
from sma.constants import sma_email_reports
from sma.constants import sma_web_reports
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
import time


class ReportSetup(GuiCommon):
    """Base class for report setup.
    To be able to use constants user should add 'constants.py' file to the test
    case. This can be done via adding following line at the top of the test
    case under \*** Settings \*** section:
            Variables      sma/constants.py
    Example of constant's usage:
    | Web Scheduled Reports Add Report | ${sma_web_reports.OVERVIEW} |
    | Web Archived Reports Add Report | ${sma_web_reports.URL_CAT} |
    | Email Scheduled Reports Add Report | ${sma_email_reports.DELIVERY} |
    | Email Archived Reports Add Report | ${sma_email_reports.VIRUS_TYPES} |
    Every web report type has it's specifics chart data values and sort column
    values.
    Every email report type has it's specifics sort column values.
    To specify report chart data use values represented above.
    Example:
    | Web Scheduled Reports Add Report | ${sma_web_reports.URL_CAT} |
    | ... | title=Report2 |
    | ... | report_format=pdf |
    | ... | time_range=num days:50 |
    | ... | schedule=monthly:03:30 |
    | ... | email_to=test_mail@ironport.com |
    | ... | num_of_rows=20 |
    | ... | chart_data=webcat warned:webcat blocked |
    | ... | sort_col=time spent |
    In this example we specified chart data for `url categories` report type.
    First chart will contain `webcat warned` values, and second one
    `webcat blocked` values.
    To specify only one chart data and leave another default or with it's
    previous value just pass ${None} or None as it's value (See second example):
    Example:
    | Web Scheduled Reports Add Report | ${sma_web_reports.URL_CAT} |
    | ... | title=Report2 |
    | ... | report_format=pdf |
    | ... | time_range=num days:50 |
    | ... | schedule=monthly:03:30 |
    | ... | email_to=test_mail@ironport.com |
    | ... | num_of_rows=20 |
    | ... | chart_data=${None}:webcat blocked |
    | ... | sort_col=time spent |
    Next example shows how to specify sorting column for report:
    Example:
    | ${type} | Set Variable | ${sma_web_reports.L4TM} |
    | Web Scheduled Reports Add Report | ${type} |
    | ... | title=Report7 |
    | ... | report_format=pdf |
    | ... | time_range=last week |
    | ... | schedule=monthly:03:30 |
    | ... | email_to=test_mail@ironport.com |
    | ... | num_of_rows=50 |
    | ... | chart_data=total monitored:total detected |
    | ... | sort_col=total monitored:total blocked:total detected |
    In this example we specify three sorting columns for l4 traffic monitor
    report. To leave previous value or default value see chart data examples.
    """
    _report_type_to_chart_data = None
    _report_types = None
    _available_reports = None

    def _register_standard_reports(self, listin):
        for filein in listin:
            self._debug('Processing "%s"' % (filein,))
            try:
                name = 'common.gui.reports.report_types.%s' % (filein,)
                __import__(name)
                report_classes = sys.modules[name].get_reports()
                for report_class in report_classes:
                    report = report_class()
                    self._register_report(report)
            except Exception as e:
                self._warn('Exception while report import: %s' % (e,))
                continue

    def _register_additional_reports(self):
        pass

    def _register_report(self, report):
        try:
            report_name = report.get_name()
        except Exception as e:
            self._warn('Exception while report registration: %s' % (e,))
            return
        if report_name in self.available_reports:
            self._warn('Duplicate report name found "%s"' % (report_name,))
        self._debug('Registered report "%s"' % (report_name,))
        self._available_reports[report_name] = report

    def get_available_reports(self):
        # lazy load
        if self._available_reports is not None:
            return self._available_reports
        self._available_reports = {}
        self._register_standard_reports(self.standard_reports_names)
        self._register_additional_reports()
        return self._available_reports

    def set_available_reports(self, reports):
        self._available_reports = reports

    standard_reports_names = [
        'wsa_antimalware',
        'wsa_app_visibility',
        'wsa_l4tm',
        'wsa_malware_risk',
        'wsa_overview',
        'wsa_system_cap',
        'wsa_system_cap_overview',
        'wsa_top_app_types',
        'wsa_url_cat',
        'wsa_url_cat_extended',
        'wsa_user_location',
        'wsa_users',
        'wsa_wbrs_filters',
        'wsa_web_sites',
        'esa_delivery',
        'esa_dlp_incident',
        'esa_domain_based',
        'esa_executive',
        'esa_filters',
        'esa_in_mail',
        'esa_int_users',
        'esa_out_destinations',
        'esa_out_domain_senders',
        'esa_out_mail',
        'esa_sender_groups',
        'esa_system_cap',
        'esa_tls_conn',
        'esa_virus_types',
        'esa_vof',
    ]
    available_reports = property(get_available_reports, set_available_reports)

    def _convert_to_tuple_from_colon_separated_string(self, user_input):
        if isinstance(user_input, (str, unicode)):
            user_input = tuple([item.strip() for item in user_input.split(':')])
        else:
            raise ValueError('Argument \'%s\' should be string type.' % \
                             (user_input,))
        return user_input

    def _click_add_scheduled_report_button(self):
        self.click_button("xpath=//input[@title='Add Scheduled Report...']")

    def _click_add_archived_report_button(self):
        self.click_button("xpath=//input[@title='Generate Report Now...']")

    def _select_report_type(self, report_type):
        report_class = self.available_reports.get(report_type)
        if report_class is None:
            raise guiexceptions.ConfigError("Invalid report type '%s'." % \
                                            (report_type))
        selector = report_class.get_selector()
        self._debug('Selector for report type "%s" is "%s"' % \
                    (report_type, selector))
        self.select_from_list('report_type', selector)
        # wait for a page load to happen or timeout expires.
        self.wait_until_page_loaded(5000)

    def _fill_report_title(self, title):
        self.input_text("xpath=//input[@id='report_title']", title)

    def _select_time_range(self, timerange):
        if timerange is None:
            return False
        time_range_types = {'last day': 'calendar_day',
                            'last week': 'calendar_week',
                            'last month': 'calendar_month',
                            'last year': 'calendar_year',
                            'num days': 'custom_day',
                            'num months': 'custom_month',
                            'timestamp': 'timestamp_day',
                            'day': 'current_day',
                            'week': 'current_week',
                            'month': 'current_month',
                            '30 days': 'current_month',
                            'quarter': 'current_quarter',
                            '90 days': 'current_quarter',
                            'yesterday': 'calendar_day',
                            'previous month': 'calendar_month',
                            'previous calendar month': 'calendar_month',
                            'custom': 'timestamp_day',
                            'custom range': 'timestamp_day'
                            }
        num_days = None
        num_months = None
        timerange = self._convert_to_tuple_from_colon_separated_string(timerange)
        if len(timerange) == 2:
            time_range = timerange[0]
            if (timerange[0] == 'num days'):
                num_days = timerange[1]
            if (timerange[0] == 'num months'):
                num_months = timerange[1]
        elif len(timerange) == 3:
            time_range = timerange[0]
            date1 = timerange[1]
            date2 = timerange[2]
        else:
            time_range = timerange[0]
            num_days = None
            num_months = None

        if time_range.lower() not in time_range_types.keys():
            raise guiexceptions.ConfigError("Invalid time range '%s'." % \
                                            (time_range))
        _time_locator1 = 'days_include'
        _time_locator2 = 'date_range'
        if int(self.get_matching_xpath_count("id('" + _time_locator1 + "')")) > 0:
            self.select_from_list(_time_locator1, '%s' % \
                                  (time_range_types[time_range.lower()],))
        elif int(self.get_matching_xpath_count("id('" + _time_locator2 + "')")) > 0:
            self.select_from_list(_time_locator2, '%s' % \
                                  (time_range_types[time_range.lower()],))
        else:
            raise guiexceptions.GuiValueError('Time Range control was not founds')
        if time_range.lower() == 'timestamp' or time_range.lower() == 'custom' or (time_range.lower())[:6] == 'custom':
            self._select_timestamp(date1, date2)
        else:
            if num_days is not None:
                if not num_days.isdigit():
                    raise guiexceptions.ConfigError(
                        "Invalid value '%s'. Should be positive int." % \
                        (num_days))
                self.input_text("xpath=//input[@id='custom_day']", num_days)
            if num_months is not None:
                if not num_months.isdigit():
                    raise guiexceptions.ConfigError(
                        "Invalid value '%s'. Should be positive int." % \
                        (num_months))
                self.input_text("xpath=//input[@id='custom_month']", num_months)

    def _select_report_format(self, reportformat):
        format_types = {'pdf': 'id=format_pdf',
                        'csv': 'id=format_csv'
                        }
        if reportformat not in format_types.keys():
            raise guiexceptions.ConfigError("Invalid format '%s'." % (reportformat))
        self._click_radio_button(format_types[reportformat])

    def _select_filtering(self, filtertype):
        filter_types = {'global': 'id=global',
                        'local': 'id=local'
                        }
        if filtertype not in filter_types.keys():
            raise guiexceptions.ConfigError("Invalid filter '%s'." % (filtertype))
        self._click_radio_button(filter_types[filtertype])

    def _select_outgoing_domain(self, domain):
        domain_types = {'server': 'id=data_source_cg_server',
                        'email_address': 'id=data_source_cg_address'
                        }
        if domain not in domain_types.keys():
            raise guiexceptions.ConfigError(
                "Invalid outgoing domain '%s'." % (domain))
        self._click_radio_button(domain_types[domain])

    def _select_report_schedule(self, schedule):
        schedule_types = {'daily': 'id=schedule_type_daily',
                          'weekly': 'id=schedule_type_weekly',
                          'monthly': 'id=schedule_type_monthly'}
        schedule = \
            self._convert_to_tuple_from_colon_separated_string(schedule)
        if len(schedule) == 4:
            schedule_type, time_h, time_m, day = schedule
        else:
            schedule_type, time_h, time_m = schedule
            day = None
        time_h_types = [('%02d' % (x)) for x in range(24)]
        time_h_types.append(None)
        time_m_types = ['00', '15', '30', '45', None]
        day_types = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                     'Thursday', 'Friday', 'Saturday', None]
        if schedule_type not in schedule_types.keys():
            raise guiexceptions.ConfigError(
                'Invalid report schedule type value \'%s\'.' % (schedule_type,))
        if time_h not in time_h_types:
            raise guiexceptions.ConfigError(
                'Invalid report schedule hour value \'%s\'.' % (time_h,))
        if time_m not in time_m_types:
            raise guiexceptions.ConfigError(
                'Invalid report schedule minutes value \'%s\'.' % (time_m,))
        if day not in day_types:
            raise guiexceptions.ConfigError(
                'Invalid report schedule day value \'%s\'. ' % (day,))
        if schedule_type is not None:
            self._click_radio_button(schedule_types[schedule_type])
        if time_h is not None:
            self.select_from_list('id=hour', '%s' % (time_h))
        if time_m is not None:
            self.select_from_list('id=minute', '%s' % (time_m))
        if day is not None:
            self.select_from_list('id=wday', '%s' % (day))

    def _fill_email_to(self, emails):
        if emails.lower() == 'off':
            self.input_text("xpath=//input[@id='recipients']", '')
        else:
            self.input_text("xpath=//input[@id='recipients']", emails)

    def _select_language(self, language):
        language = language.lower()
        language_types = {'deutsch': 'de-de',
                          'english': 'en-us',
                          'espanol': 'es',
                          'france': 'fr-fr',
                          'italian': 'it',
                          'japanese': 'ja',
                          'korean': 'ko',
                          'portuguese': 'pt-br',
                          'russian': 'ru',
                          'chinese': 'zh-cn',
                          'taiwan': 'zh-tw'
                          }
        if language not in language_types.keys():
            raise guiexceptions.ConfigError(
                'Invalid language %s requested' % language)
        self.select_from_list('id=lang', language_types[language])

    def _select_number_of_rows(self, number_of_rows):
        select = "xpath=//select[@id='max_items' or @id='max_rows']"
        if not self._is_element_present(select):
            return
        valid_values = self.get_list_items(select)
        if number_of_rows not in valid_values:
            raise guiexceptions.ConfigError(
                "Invalid number of rows/items '%s'." % (number_of_rows))
        self.select_from_list(select, '%s' % (number_of_rows))

    def _select_chart_data(self, charttype, row, type_dict):
        link = "xpath=//table[@class='layout']//tr[%d]//td[2]/a" % (row,)
        if charttype.lower() == 'none':
            return
        if charttype not in type_dict.keys():
            raise guiexceptions.ConfigError(
                "Invalid chart data type '%s'." % (charttype))
        radio_button_link = "xpath=//input[@id='chart_option_dlg_%s']" % \
                            (type_dict[charttype])
        self.click_element(link, "don't wait")
        self._click_radio_button(radio_button_link)
        self.click_element("xpath=//span[@class='button-group']/button[2]",
                           "don't wait")

    def _get_type_dicts(self, report_type):
        self._debug('report_type is %s' % (report_type,))
        report_class = self.available_reports[report_type]
        return report_class.get_chart_data()

    def _select_chart_display_data(self, report_type, data):
        if isinstance(data, dict):
            self._select_chart_display_data_by_dict(data)
        else:
            if report_type is None:
                raise guiexceptions.ConfigError(
                    "This report does not have fixed set of charts so " + \
                    "chart data should be defined by dictionary")
            self._select_chart_display_data_by_string(report_type, data)

    def _select_chart_display_data_by_string(self, report_type, data):

        l_type_dict, r_type_dict = self._get_type_dicts(report_type)
        data = self._convert_to_tuple_from_colon_separated_string(data)
        if len(data) == 2:
            chart_left, chart_right = data
        else:
            raise guiexceptions.ConfigError('')
        if chart_left is not None:
            self._select_chart_data(chart_left, 2, l_type_dict)
        if chart_right is not None:
            self._select_chart_data(chart_right, 3, r_type_dict)

    def _select_chart_display_data_by_dict(self, data):

        charts_table_selector = \
            "//table[@class='pairs']//tr[th[contains(text(),'Charts')]]" + \
            "//table[@class='layout']"
        rows = int(self.get_matching_xpath_count(charts_table_selector + '//tr'))
        name_to_row = {}
        for i in xrange(2, rows):
            name = self.get_value(charts_table_selector + '//tr[%s]/td[1]' % (i,))
            name = name.strip()
            name_to_row[name] = i
        for chart_name, label_text in data:
            row = name_to_row.get(chart_name)
            if row is None:
                raise guiexceptions.ConfigError(
                    'Chart name "%s" was not found in charts list: %s' % \
                    (chart_name, name_to_row.keys()))
            link = charts_table_selector + '//tr[%s]/td[2]/a' % (row,)
            self.click_element(link, "don't wait")
            radio_button_link = "//div[@id='chart_option_dlg']" + \
                                "//div[label[text()='%s']]/input" % (label_text,)
            self._click_radio_button(radio_button_link)
            self.click_element("xpath=//span[@class='button-group']/button[2]",
                               "don't wait")

    def _select_sort_column(self, report_type, columns):
        if isinstance(columns, dict):
            self._select_sort_column_by_dict(columns)
        else:
            if report_type is None:
                raise guiexceptions.ConfigError(
                    "This report does not have fixed set of sort columns so " + \
                    "sort columns data should be defined by dictionary")
            self._select_sort_column_by_string(report_type, columns)

    def _select_sort_column_by_string(self, report_type, columns):
        report_class = self.available_reports[report_type]
        columns_data = report_class.get_table_columns_data()
        columns = \
            self._convert_to_tuple_from_colon_separated_string(columns)
        if columns_data is None:
            return
        for table, col in zip(columns_data, columns):
            select_name, columns_dict = table
            self.select_from_list(
                "xpath=//select[@name='%s']" % (select_name,),
                columns_dict[col])

    def _select_sort_column_by_dict(self, columns):
        sort_col_table_selector = \
            "//table[@class='pairs']//tr[th[contains(text(),'Sort Column')]]" + \
            "//table[@class='layout']"
        rows = int(self.get_matching_xpath_count(sort_col_table_selector + '//tr'))
        name_to_row = {}
        for i in xrange(2, rows):
            name = self.get_value(sort_col_table_selector + '//tr[%s]/td[1]' % (i,))
            name = name.strip()
            name_to_row[name] = i
        for col_name, value in columns:
            row = name_to_row.get(col_name)
            if row is None:
                raise guiexceptions.ConfigError(
                    'Sort column "%s" was not found in columns list: %s' % \
                    (col_name, name_to_row.keys()))
            selector = sort_col_table_selector + '//tr[%s]/td[2]/input' % (row,)
            self.select_from_list(selector, value)

    def _get_report_row_index(self, name, col):
        report_table = '//table[@class="cols"]'
        table_rows = self.get_matching_xpath_count(
            '%s/tbody/tr' % (report_table,))
        for i in xrange(2, int(table_rows) + 1):
            report_name = self.get_text('xpath=%s/tbody/tr[%s]/td[%s]' %
                                        (report_table, i, col)).split(' \n')[0]
            if name == report_name:
                return i
        return None

    def _click_deliver_button(self):
        self.click_button("xpath=//input[@value='Deliver This Report']")

    def _click_edit_report_link(self, name):
        cell_id = 'xpath=//table[@class="cols"]//tr[%s]//td[2]/a'
        row = self._get_report_row_index(name, 2)
        if row is None:
            raise guiexceptions.GuiValueError('Report "%s"' % (name,))
        self.click_link(cell_id % (row))

    def _click_delete_button(self):
        self.click_button("xpath=//input[@value='Delete']", "don't wait")
        self.click_button("xpath=//button[text()='Delete']")

    def _check_for_deletion(self, name, name_col, check_col):
        cell_id = 'xpath=//table[@class="cols"]//tr[%s]//td[%s]/input'
        row = self._get_report_row_index(name, name_col)
        if row is None:
            raise guiexceptions.GuiValueError('Report "%s"' % (name,))
        self.click_element(cell_id % (row, check_col), "don't wait")

    def _set_archive_setting(self, setting):
        archive_checkbox = "xpath=//input[@name='archive']"
        if setting not in ['yes', 'no']:
            raise guiexceptions.ConfigError(
                'Invalid archive setting \'%s\'.Should be \'yes\' or \'no\'.' \
                % (setting,))
        if setting.lower() == 'yes':
            self.select_checkbox(archive_checkbox)
        else:
            self.unselect_checkbox(archive_checkbox)

    def _select_timestamp(self, start_date, end_date):
        start_date_input = "xpath=//input[@id='from_date']"
        end_date_input = "xpath=//input[@id='end_date']"
        start_time = "xpath=//select[@id='from_time']"
        end_time = "xpath=//select[@id='end_time']"
        date = "xpath=//a[text()='15']"
        try:
            start_date = time.strptime(start_date, '%d %b %Y %H')
            end_date = time.strptime(end_date, '%d %b %Y %H')
        except ValueError:
            raise ('Incorrect time range value: %s, %s.' % \
                   (start_date, end_date))
        if start_date > end_date:
            raise \
                guiexceptions.GuiValueError('Incorrect time range %s, %s.' + \
                                            'first date should be less than second date.' % \
                                            (start_date, end_date))
        # used trick: start and end date passed into hidden values instead
        # using calendar stuff.
        self.click(start_date_input)
        self.click(date)
        # if you see errors related to invisible elements -
        # this should be changed to
        #
        # start_date_input_id = 'from_date'
        # self._set_input_value_with_javascript(start_date_input_id,
        #               time.strftime('%d %b %Y', start_date))
        self.input_text(start_date_input,
                        time.strftime('%d %b %Y', start_date))
        self.click(end_date_input)
        self.click(date)
        # if you see errors related to invisible elements -
        # same as above
        self.input_text(end_date_input, time.strftime('%d %b %Y', end_date))
        self.select_from_list(start_time, time.strftime('%H', start_date))
        self.select_from_list(end_time, time.strftime('%H', end_date))
        self.click_button("xpath=//button[text()='Save']")

    def _get_report_type(self):

        reportType = self.get_text("xpath=//table[@class='pairs']//tr[1]//td[1]")

        return reportType

        # TODO: report 'My Reports' have select value that depends on
        #       logged-in user. Improve this function to properly detect
        #       such kind of reports

    def _show_all(self):
        if self._is_element_present('id=pageSize'):
            self.select_from_list('id=pageSize', 'All')

    def _select_all_reports(self):
        self.click_element("xpath=//input[@name='del_0']", "don't wait")

    def _fill_report_data(self, report_type, title, report_format, time_range,
                          schedule, email_to, num_of_rows, chart_data,
                          sort_col, filterreport, language=None):
        if report_type is not None:
            self._select_report_type(report_type)
        else:
            report_type = self._get_report_type()

        time.sleep(2)
        if title is not None:
            self._fill_report_title(title)
        if chart_data is not None:
            self._select_chart_display_data(report_type, chart_data)
        if sort_col is not None:
            self._select_sort_column(report_type, sort_col)
        if time_range is not None:
            self._select_time_range(time_range)
        if report_format is not None:
            self._select_report_format(report_format)
        if num_of_rows is not None:
            self._select_number_of_rows(num_of_rows)
        if schedule is not None:
            self._select_report_schedule(schedule)
        if email_to is not None:
            self._fill_email_to(email_to)
        if filterreport is not None:
            self._select_filtering(filterreport)
        if language is not None:
            self._select_language(language)

    def _fill_archived_report_data(self, report_type, title, report_format,
                                   time_range, email_to, archive, num_of_rows,
                                   chart_data, sort_col, filterreport, language=None):
        self._fill_report_data(report_type, title, report_format, time_range,
                               None, None, num_of_rows, chart_data, sort_col,
                               filterreport, language)
        if archive is not None:
            self._set_archive_setting(archive)
        if archive is not None and archive.lower() == 'no' and \
                email_to is None:
            guiexceptions.ConfigError(
                'You have to specify at least one option: ' + \
                'either \'archive\' or \'email to\'.')
        if email_to is not None:
            self.select_checkbox("xpath=//input[@id='deliver']")
            self._fill_email_to(email_to)

    def _select_report_generation(self, report_generation, file_to_upload,
                                  domains, emails):
        if report_generation is None:
            return
        if report_generation == 'configfile':
            self._click_radio_button(
                "xpath=//input[@id='gen_opt_upload_file']")
            available_files = self.get_list_items(
                "xpath=//select[@id='file_server']")
            if file_to_upload is not None:
                if file_to_upload in available_files:
                    self._click_radio_button(
                        "xpath=//input[@id='load_type_server']")
                    self.select_from_list('file_server', '%s' % \
                                          (file_to_upload))
                else:
                    self._click_radio_button(
                        "xpath=//input[@id='load_type_local']")
                    self.input_text(
                        "xpath=//input[@id='local_file']", file_to_upload)
        elif report_generation == 'individual':
            self._click_radio_button("xpath=//input[@id='gen_opt_enter_data']")
            if domains is not None:
                if domains.lower() == 'off':
                    self.input_text("xpath=//input[@id='domains']", '')
                else:
                    self.input_text("xpath=//input[@id='domains']", domains)
            if emails is not None:
                if emails.lower() == 'off':
                    self.input_text(
                        "xpath=//input[@id='gen_opt_recipients']", '')
                else:
                    self.input_text(
                        "xpath=//input[@id='gen_opt_recipients']", emails)
        else:
            raise guiexceptions.GuiValueError(
                'Unknown "%s" report generation option.' % \
                (report_generation,))

    def _select_logo(self, logo):
        if logo is None:
            return
        elif logo.lower() == 'cisco':
            self._click_radio_button("xpath=//input[@id='default_logo_id']")
        else:
            self._click_radio_button("xpath=//input[@id='custom_logo_id']")
            self.input_text("xpath=//input[@id='custom_logo']", logo)

    def _check_reports_availability(self):
        no_scheduled_msg = 'There are no Scheduled Reports defined.'
        no_archived_msg = 'There are no reports to display.'
        report_exist = False
        if self._is_text_present(no_scheduled_msg):
            self._info(no_scheduled_msg)
        elif self._is_text_present(no_archived_msg):
            self._info(no_archived_msg)
        else:
            report_exist = True
        return report_exist

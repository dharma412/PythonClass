#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/common/util/csv_report_reader.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import csv
import StringIO
from common.gui.guicommon import GuiCommon


class CsvReader(GuiCommon):
    """CSV Reader interaction class.
    Keyword for reading report data from csv file.
    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['csv_reader_get_csv_report_data']

    def _get_msg_content(self, msg):
        msg_body, msg_attach = None, None

        for msg_part in msg.walk():
            if msg_part.get_content_type() == 'text/plain':
                msg_body = msg_part.get_payload(decode=True)
            elif msg_part.get_content_type() == 'application/csv':
                msg_attach = msg_part.get_payload(decode=True)

        return msg_body, msg_attach

    def _verify_body(self, body, report_name, report_sub_type):
        patt = 'report titled "%s" is attached, in CSV format.\n%s_%s' \
               % (report_name, report_name, report_sub_type,)

        exist = False
        if patt not in body:
            self._info('No "%s" was found in message body\r\n%s' % \
                       (patt, body))
        else:
            self._info('"%s" was found in message body' % (patt,))
            exist = True

        return exist

    def _get_csv_report_data(self, csv_string):
        reader = csv.DictReader(StringIO.StringIO(csv_string))
        results = []

        for row in reader:
            results.append(row)

        return results

    def csv_reader_get_csv_report_data(self,
                                       msg,
                                       report_name,
                                       report_subtype):
        """Get CSV Report Data.

        Use this method to get report data from CSV file.

        Parameters:
        - `msg`: full text of message from mbox from null_smtpd daemon,
        which are returned by `Null Smtpd Next Message` keyword.
        - `report_name`: name of generated report.
        - `report_subtype`: subtype report name.
        e.g. After generation Web Overview Report, we receive 9 emails
        with attached subtype reports: _Total Web Proxy Activity_,
        _Suspect Transactions_, _Top URL Categories: Total Transactions_,
        _Top Malware Categories: Monitored or Blocked_, _Web Proxy Summary_,
        _L4 Traffic Monitor Summary_, _Suspect Transactions Summary_,
        _Top Application Types: Total Transactions_,
        _Top Users: Blocked or Warned Transactions_. To get data for
        _Web Proxy Summary_ report need to specify
        `report_subtype` == Web Proxy Summary.

        Returns: None, empty list or list of dictionaries.
        None - if there is no email, or no email with specified report name
        found or no specified attachment found.
        empty list - if there is no data for specified report.
        list of dictionaries - if data for specified report is found

        Examples:
        | ${msg} = | Null Smtpd Next Message |
        | ${REPORT_TITLE} = | Set Variable | Web_Archived_Report |
        | ${REPORT_SUBTYPE} = | Set Variable | Web Proxy Summary |
        | ${results} = | Csv Reader Get Csv Report Data |
        | ... | ${msg} |
        | ... | ${REPORT_TITLE} |
        | ... | ${REPORT_SUBTYPE} |
        """
        data = None
        if msg is not None:
            msg_body, msg_attach = self._get_msg_content(msg)
            if msg_body is not None:
                if self._verify_body(msg_body, report_name, report_subtype):
                    if msg_attach is not None:
                        data = self._get_csv_report_data(msg_attach)
                    else:
                        self._info('No CSV report was attached to msg')
            else:
                self._info('Message body was not found')
        else:
            self._info('Message was not found')

        return data

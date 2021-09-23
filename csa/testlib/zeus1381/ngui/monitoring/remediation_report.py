import re

from common.gui.decorators import visit_page
from common.ngui.exceptions import DataNotFoundError
from common.ngui.ngguicommon import NGGuiCommon

from monitoring_def import MONITORING

class RemediationReport(NGGuiCommon):

    def get_keyword_names(self):
        return ['remediation_report_summary', 'mailbox_auto_remediation_summary',
                'mailbox_search_and_remediate_summary', 'remediation_batch_count', 'remediation_batches_detail',
                'remediation_batch_report_details']

    def get_message_remediated_summary(self):
        summary = {}
        total_match = re.search('(\d+)\s+(.*)', self.get_text(Remediation.total_summary_messages_remediated))
        if total_match:
           summary['total'] =  total_match.group(1)
        for legend_index in range(1, 3):
           legend_xpath = '%s/%s' % (
               Remediation.message_remediated_legend, Remediation.summary_legend_span % legend_index)
           if self._is_element_present(legend_xpath):
               lengend_match = re.search('(\d+)\s+(.*)', self.get_text(legend_xpath))
               if lengend_match:
                 summary[lengend_match.group(2)] = lengend_match.group(1)
        return summary

    def get_mar_message_summary(self):
        summary = {}
        total_auto_match = re.search('(\d+)\s+(.*)', self.get_text(Remediation.total_summary_messages_auto_remediated))
        if total_auto_match:
           summary['total'] = total_auto_match.group(1)
        for legend_index in range(1, 6):
           legend_xpath = '%s/%s' % (
               Remediation.message_auto_remeediated_legend, Remediation.summary_legend_span % legend_index)
           if self._is_element_present(legend_xpath):
               lengend_match = re.search('(\d+)\s+(.*)', self.get_text(legend_xpath))
               if lengend_match:
                 summary[lengend_match.group(2)] = lengend_match.group(1)
        return summary

    def get_sar_message_summary(self):
        summary = {}
        total_sar_match = re.search('(\d+)\s+(.*)',
                                    self.get_text(Remediation.total_summary_messages_search_and_remediated))
        if total_sar_match:
           summary['total'] =  total_sar_match.group(1)
        for legend_index in range(1, 6):
           legend_xpath = '%s/%s' % (
               Remediation.message_search_and_remediated_legend, Remediation.summary_legend_span % legend_index)
           if self._is_element_present(legend_xpath):
               lengend_match = re.search('(\d+)\s+(.*)', self.get_text(legend_xpath))
               if lengend_match:
                  summary[lengend_match.group(2)] = lengend_match.group(1)
        return summary

    def remediation_report_summary(self):
        report_summary = {}
        self.click_element(Remediation.summary_tab)
        self.set_selenium_speed('0s')
        report_summary['Messages Remediated'] = self.get_message_remediated_summary()
        report_summary['Messages Auto Remediated'] = self.get_mar_message_summary()
        report_summary['Messages Searched and Remediated'] = self.get_sar_message_summary()
        self.set_selenium_speed('0.5s')
        return report_summary

    def mailbox_auto_remediation_summary(self):
        report_summary = {}
        self.click_element(Remediation.mailbox_auto_remediation_tab)
        self.set_selenium_speed('0s')
        report_summary = self.get_mar_message_summary()
        self.set_selenium_speed('0.5s')
        return report_summary

    def mailbox_search_and_remediate_summary(self):
        report_summary = {}
        self.click_element(Remediation.mailbox_search_and_remediate_tab)
        self.set_selenium_speed('0s')
        report_summary = self.get_sar_message_summary()
        self.set_selenium_speed('0.5s')
        return report_summary

    def remediation_batches_detail(self):
        batch_detail =  {}
        self.click_element(Remediation.mailbox_search_and_remediate_tab)
        count = self.remediation_batch_count()
        for eachrow in range(1, count+1):
            col_dict = {}
            col_dict['Batch ID'] = self.get_text('%s%s' %(Remediation.remediation_batch_table,
                                                                    Remediation.remediation_batch_row%(eachrow, 1)))
            batch_detail[col_dict['Batch ID']] = {}
            col_dict['Batch Name'] = self.get_text('%s%s' % (Remediation.remediation_batch_table,
                                                                       Remediation.remediation_batch_row % (eachrow, 2)))
            col_dict['Status'] = self.get_text('%s%s' % (Remediation.remediation_batch_table,
                                                             Remediation.remediation_batch_row % (eachrow, 3)))

            status_match = re.search('(\d+)\s+(.*)', self.get_text('%s%s' %(Remediation.remediation_batch_table,
                                                                    Remediation.remediation_batch_row%(eachrow, 4))))
            if status_match:
                col_dict['Message Status'] = {status_match.group(2): status_match.group(1)}
            batch_detail[col_dict['Batch ID']] = col_dict
        return batch_detail

    def remediation_batch_count(self):
        """
        To get the remediation batch count
        :return: remediation batch count
        """
        self.click_element(Remediation.mailbox_search_and_remediate_tab)
        if self._is_element_present(Remediation.batch_no_data):
            raise DataNotFoundError(self.get_text(Remediation.batch_no_data))
        count_match = re.search('(\d+)\s+(.*)', self.get_text(Remediation.remediation_batch_count))
        if count_match:
            return int(count_match.group(1))

    def remediation_batch_report_details(self, batch_id):
        report_detail = {}
        self.click_element(Remediation.mailbox_search_and_remediate_tab)
        search_batch_name = Remediation.batch_name%batch_id
        if self._is_element_present(search_batch_name):
            self.click_element(search_batch_name)
            self.set_selenium_speed('0s')
            report_detail['Initiated On'] = self.get_text(Remediation.batch_detail_name%Remediation.intiated_on)
            report_detail['Initiated Source'] = self.get_text(Remediation.batch_detail_name % Remediation.intiated_source)
            report_detail['Initiated By'] = self.get_text(Remediation.batch_detail_name % Remediation.intiated_by)
            report_detail['Action Taken'] = self.get_text(Remediation.batch_detail_name % Remediation.action_taken)
            report_detail['Batch Name'] = self.get_text(Remediation.report_batch_name)
            report_detail['Batch Description'] = self.get_text(Remediation.batch_description)
            row_count = self.get_element_count(Remediation.remediation_batch_detail_table_rows)
            detail_column=['Message ID', 'Message Read', 'Status', 'From', 'To', 'Message Sent At']
            for eachrow in range(1, row_count+1):
                row_detail = {}
                for column in range(1, 7):
                    row_detail[detail_column[column-1]] = self.get_text(Remediation.remediation_batch_detail_table_row_elements%(eachrow,column))
                report_detail[row_detail['Message ID']] = row_detail
            self.set_selenium_speed('0.5s')
            self.click_element(Remediation.go_back_batch_tab)
            return report_detail
        else:
            raise DataNotFoundError('Invalid batch id:%s' %batch_id)

class Remediation:
    summary_tab = "//*[@class='ngsma-tabs']/div//*[@translate='monitoring.reporting.summary']"
    mailbox_auto_remediation_tab = "//*[@translate='monitoring.reporting.mailboxAutoRemReport']"
    mailbox_search_and_remediate_tab = "//*[@translate='monitoring.reporting.mailboxOnDemandRemediation']"
    summary_messages_remediated = "//*[@progress-bar-data='$ctrl.summaryRemData']"
    summary_messages_auto_remediated = "//*[@progress-bar-data='$ctrl.summaryAutoRemData']"
    summary_messages_search_and_remediated = "//*[@progress-bar-data='$ctrl.summaryOnDemandRemData']"
    total_summary_messages_remediated = '%s/div/div[1]/div[2]' %summary_messages_remediated
    total_summary_messages_auto_remediated = '%s/div/div[1]/div[2]' %summary_messages_auto_remediated
    total_summary_messages_search_and_remediated = '%s/div/div[1]/div[2]' %summary_messages_search_and_remediated
    message_remediated_legend = '%s/div/div[2]/div[2]'%summary_messages_remediated
    message_auto_remeediated_legend = '%s/div/div[2]/div[2]' %summary_messages_auto_remediated
    message_search_and_remediated_legend = '%s/div/div[2]/div[2]' %summary_messages_search_and_remediated
    summary_legend_span = '/span[%s]/span[2]'
    batch_no_data = "//*[@translate='monitoring.reporting.noDataMessage']"
    remediation_batch_table = "//*[@class='ui-grid-canvas']"
    remediation_batch_count = "//*[@ng-if='$ctrl.config.customTitle']"
    remediation_batch_row ='/div[%s]/div/div[%s]'
    batch_name = "//*[contains(text(),'%s')]/../../../div[2]/div/div/a"
    go_back_batch_tab = "//*[@ng-click='$ctrl.goToRemediationMorBatchTab()']"
    batch_detail_name = "//*[@translate='monitoring.remediation_reports.remediation_report_batch_details.batchDetailNames.%s']/../div"
    intiated_on = "initiatedOn"
    intiated_source = "initiatedSource"
    intiated_by = "initiatedBy"
    action_taken = 'actionTaken'
    remediation_batch_detail_table_rows= "//*[@class='ui-grid-canvas']/div"
    remediation_batch_detail_table_row_elements  = "//*[@class='ui-grid-canvas']/div[%s]/div/div[%s]"
    report_batch_name = "//*[@ng-if='$ctrl.dataLoaded']/div/div[1]/div[2]"
    batch_description = "//*[@ng-if='$ctrl.dataLoaded']/div/div[2]/div[1]"

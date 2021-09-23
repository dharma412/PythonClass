from common.ngui.exceptions import DataNotFoundError
from common.ngui.ngguicommon import NGGuiCommon
from monitoring_def import MONITORING

class MailFlowDetails(NGGuiCommon):

    def get_keyword_names(self):
        return ['select_mail_flow_details', 'search_results', 'search_result_for_detailed_reporting']

    def _get_table_details(self, title, counter):
        res = {}
        col_names = [self.get_text('%s[%s]' % (title, eachcol)).strip().split('\n') for eachcol in
                     range(1, self.get_element_count(title) + 1) if eachcol]
        tab_counter = [self.get_text('%s[%s]' % (counter, eachtab)).strip().split('\n') for eachtab in
                     range(1, self.get_element_count(counter) + 1) if eachtab]
        key,value = col_names[0],tab_counter[0]
        res= dict(zip(key,value))
        return res

    def select_mail_flow_details(self, report, tab):
        if not MailFlowReport.reports.has_key(report):
            raise DataNotFoundError('Invalid report:%s' %report)
        if not MailFlowReport.tabs.has_key(tab):
            raise DataNotFoundError('Invalid tab:%s' %tab)
        self.click_element(MailFlowReport.reports[report])
        self.wait_for_angular()
        self.click_element(MailFlowReport.tabs[tab])
        self.wait_for_angular()

    def search_result_for_detailed_reporting(self):
        return self._get_table_details(MailFlowReport.Reporting_table_title, MailFlowReport.Reporting_table_counters)

    def search_results(self, match, input=None):
        """
        To do the reporting search
        :param match: Domains,Network Owners, IP Address
        :param input: Input value
        :return:
        """
        self.select_custom_dropdown(MONITORING.SEARCH_REPORT, match)
        self._info('Selecting reporting search:%s' % (match))
        if input:
            self._info('Selecting reporting search:%s: Input:%s' % (match, input))
            self.input_text(MONITORING.SEARCH_QUERY, input)
        self.click_element(MONITORING.SEARCH)
        self.wait_for_angular()


class MailFlowReport:
    reports = {'Incoming Mails': "//*[@translate='monitoring.reporting.incomingMail']",
               'Outgoing Senders': "//*[@translate='monitoring.reporting.outgoingSenders']"}
    tabs = {'IP Addresses': "//*[@translate='reporting.tabs.ip_addresses']",
            'Domains': "//*[@translate='reporting.tabs.domains']",
            'Network Owners':"//*[@translate='reporting.tabs.network_owners']"
            }
    Reporting_table_title = "//*[@class='ui-grid-header ng-scope']"
    Reporting_table_counters = "//*[@class='ui-grid-row ng-scope']"

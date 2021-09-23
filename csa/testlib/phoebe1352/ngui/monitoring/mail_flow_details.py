from common.ngui.exceptions import DataNotFoundError
from common.ngui.ngguicommon import NGGuiCommon

class MailFlowDetails(NGGuiCommon):

    def get_keyword_names(self):
        return ['select_mail_flow_details']

    def select_mail_flow_details(self, report, tab):
        if not MailFlowReport.reports.has_key(report):
            raise DataNotFoundError('Invalid report:%s' %report)
        if not MailFlowReport.tabs.has_key(tab):
            raise DataNotFoundError('Invalid tab:%s' %tab)
        self.click_element(MailFlowReport.reports[report])
        self.wait_for_angular()
        self.click_element(MailFlowReport.tabs[tab])
        self.wait_for_angular()

class MailFlowReport:
    reports = {'Incoming Mails': "//*[@translate='monitoring.reporting.incomingMail']",
               'Outgoing Senders': "//*[@translate='monitoring.reporting.outgoingSenders']"}
    tabs = {'IP Addresses': "//*[@translate='reporting.tabs.ip_addresses']",
            'Domains': "//*[@translate='reporting.tabs.domains']",
            'Network Owners':"//*[@translate='reporting.tabs.network_owners']"
            }


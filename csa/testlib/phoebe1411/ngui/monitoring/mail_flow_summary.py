from common.ngui.ngguicommon import NGGuiCommon
from common.gui.decorators import set_speed
from common.ngui.exceptions import DataNotFoundError

class MailFlowSummary(NGGuiCommon):

    def get_keyword_names(self):
        return ['get_threat_detection_summary',
                'get_reputation_filtering_details',
                'get_threat_messages'
                ]

    @set_speed('0s')
    def _get_tab_details(self, title, counter):
        tab_names = [self.get_text('%s[%s]' % (title, eachtab)) for eachtab in
                     range(1, self.get_element_count(title) + 1) if eachtab ]
        tab_counter = ['NA']
        tab_counter.extend([self.get_text('%s[%s]' % (counter, eachtab)) for eachtab in
                     range(1, self.get_element_count(counter) + 1) if eachtab])
        return {tab_names[count]: tab_counter[count] for count in range(len(tab_names))}

    @set_speed('0s')
    def get_reputation_filtering_details(self):
        headers = ['Reputation Filtering', 'Messages']
        return self.get_grid_canvas_details(MailFlowSummaryReport.Repuation_Filtering_Messages, headers)

    def get_threat_detection_summary(self):
        return self._get_tab_details(MailFlowSummaryReport.Threat_Detection_Summary % MailFlowSummaryReport.Title,
                                       MailFlowSummaryReport.Threat_Detection_Summary% MailFlowSummaryReport.Counter)

    def get_threat_messages(self):
        headers = ['Threats', 'Threat_Percentage', 'Count']
        return self.get_grid_canvas_details(MailFlowSummaryReport.Threat_Messages, 
        headers, counter=True)


class MailFlowSummaryReport:

    Threat_Detection_Summary = "(//*[@class='trend-widget__container trend-widget__incomingThreatDetection']%s)"
    Counter = "//*[@class='ribbon-data__counter-value ng-binding']"
    Title = "//*[@class='ribbon-card__title']"
    Repuation_Filtering_Messages = "//*[@class='ui-grid-canvas']/div"
    Threat_Messages = "//*[@class='overview__msg-status']//*[@class='pie-chart-block__legend-body-item ng-scope']"

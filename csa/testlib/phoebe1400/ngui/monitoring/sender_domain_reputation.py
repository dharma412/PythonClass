from common.ngui.ngguicommon import NGGuiCommon
from common.gui.decorators import set_speed

class SenderDomainReputation(NGGuiCommon):

    def get_keyword_names(self):
        return ['get_incoming_messages_sdr_verdict']

    @set_speed('0s')
    def get_incoming_messages_sdr_verdict(self):
        headers = ['SDR Verdict', 'percent', 'Messages']
        return self.get_grid_canvas_details(SenderDomainReputationReport.Incoming_Message_Verdict, headers, flag=True)


class SenderDomainReputationReport:
    Incoming_Message_Verdict = "//*[@class='ui-grid-canvas']/div"

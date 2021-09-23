import re

from common.ngui.exceptions import DataNotFoundError
from common.ngui.ngguicommon import NGGuiCommon

class AdvancePhisingProtection(NGGuiCommon):

    def get_keyword_names(self):
        return ['advanced_phishing_protection_forward_details']

    def advanced_phishing_protection_forward_details(self):
        forward_detail = {}
        if self._is_element_present(AdvancePhising.forwaded_to_phising_protection_cloud_service):
            total_msg_match = re.search('(\d+)\s+(.*)', self.get_text(AdvancePhising.total_messages_forwaded))
            if total_msg_match:
                forward_detail['Total Messages'] = total_msg_match.group(1)
            for legend_index in range(1, 3):
                status_match = re.search('(\d+)\s+(.*)',\
                                         self.get_text('%s/span[%s]'\
                                                       %(AdvancePhising.message_status, legend_index)).strip())
                if status_match:
                    forward_detail[status_match.group(2)] = status_match.group(1)
            return forward_detail
        else:
            raise DataNotFoundError('Phising Forward details not found')

class AdvancePhising:
    forwaded_to_phising_protection_cloud_service = "//*[@progress-bar-data='$ctrl.appProgressData']"
    total_messages_forwaded = '%s/div/div/div' % forwaded_to_phising_protection_cloud_service
    message_status = '%s/div/div[2]/div[2]' % forwaded_to_phising_protection_cloud_service

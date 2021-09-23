
from common.ngui.ngguicommon import NGGuiCommon

class OtherQuarantine(NGGuiCommon):

    def get_keyword_names(self):
        return ['pvo_quarantines_search' , 'pvo_quarantines_view_message']

    def pvo_quarantines_search(self):
        """
        This keyword to do the PVO Quarantine Search
        :return:
        """
        self.click_element(OtherQuarantineSearch.search_tab)
        self.wait_for_angular()
        self.click_element(OtherQuarantineSearch.search_button)
        self.wait_for_angular()

    def pvo_quarantines_view_message(self, sender, recipient, subject):
        """
        This keyword to view message based on the input matches on the PVO Quarantine Search
        :return:
        """
        for message in range(1, self.get_element_count(OtherQuarantineSearch.message_row)+1):
            sender_text = self.get_text('%s%s'%(OtherQuarantineSearch.message_row, OtherQuarantineSearch.sender %message))
            recipient_text = self.get_text('%s%s' % (OtherQuarantineSearch.message_row, OtherQuarantineSearch.recipient %message))
            subject_text = self.get_text('%s%s' % (OtherQuarantineSearch.message_row, OtherQuarantineSearch.subject %message))
            if str(sender) == sender_text and recipient_text == str(recipient) and subject in subject_text:
                self.click_element('%s%s/div/a' % (OtherQuarantineSearch.message_row, OtherQuarantineSearch.subject %message))
                self.wait_for_angular()
                break

class OtherQuarantineSearch:

    search_tab = "//span[@translate='tabs.search']"
    search_button = "//*[@id='controlBtn_search0']"
    message_row = "//*[@class='ui-grid-row ng-scope']"
    sender = '[%s]/div[1]/div[2]'
    recipient = '[%s]/div[1]/div[3]'
    subject =  '[%s]/div[1]/div[4]'
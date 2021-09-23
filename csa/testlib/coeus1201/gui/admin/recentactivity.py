import time
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

class Recentactivity(GuiCommon):

    #GUI Recent Activity Table.
    def get_keyword_names(self):
        return ['recent_activity_info',
                'recent_activity_table_info']

    def _open_page(self):
    #Go to ' Reporting -> My dashboard' page
        self._navigate_to("Reporting", "My Dashboard")

    def recent_activity_table_info(self):
        activity_id = "//*[@id='recent-activity-icon']"
        self._open_page()
        self.click_element(activity_id, "don't wait")
        ssh_id = "//*[@id='win']/div[2]/div/table/tbody/tr[5]/td[1]"
        success_id="//*[@id='win']/div[2]/div/table/tbody/tr[5]/td[2]"
        fail_id="//*[@id='win']/div[2]/div/table/tbody/tr[5]/td[3]"
        txt = self.get_text(ssh_id)
        if txt == "SSH":
          success_count=self.get_text(success_id)
          fail_count=self.get_text(fail_id)
        return (success_count,fail_count)

    def recent_activity_info(self):
        activity_id = "//*[@id='recent-activity-icon']"
        self._open_page()
        self.click_element(activity_id, "don't wait")
        ssh_id = "//*[@id='win']/div[2]/div/table/tbody/tr[5]/td[1]"
        success_id="//*[@id='win']/div[2]/div/table/tbody/tr[5]/td[2]"
        fail_id="//*[@id='win']/div[2]/div/table/tbody/tr[5]/td[3]"
        success_msg_id="//*[@id='win']/div[2]/div/p[2]"
        fail_msg_id="//*[@id='win']/div[2]/div/p[1]"
        txt = self.get_text(ssh_id)
        if txt == "SSH":
          success_count=self.get_text(success_id)
          fail_count=self.get_text(fail_id)
          success_msg=self.get_text(success_msg_id)
          fail_msg=self.get_text(fail_msg_id)
        return (success_count,fail_count,success_msg,fail_msg)

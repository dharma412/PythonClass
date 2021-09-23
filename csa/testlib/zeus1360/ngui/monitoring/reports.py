
from common.ngui.ngguicommon import NGGuiCommon
from common.ngui.exceptions import UserInputError

from monitoring_def import MONITORING, Reports

class MonitoringReports(NGGuiCommon):

    def get_keyword_names(self):
        return ['select_reports']

    def select_reports(self, name):
        self.click_element(MONITORING.REPORT_MENU)
        if Reports.has_key(name):
            self._visit_to(Reports[name]['xpath'], Reports[name]['href'])
            self._info('Selected Reports:%s' %name)
        else:
            raise UserInputError('Select Report Menu:%s is invalid'%name )
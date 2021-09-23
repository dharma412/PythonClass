from common.gui.decorators import visit_page
from common.ngui.ngguicommon import NGGuiCommon

from monitoring_def import MONITORING

class Monitoring(NGGuiCommon):

    def get_keyword_names(self):
        return ['go_to_monitoring_page', 'view_data_for_appliance', 'select_time_range', 'go_to_monitoring_page_nowait']        

    @visit_page(MONITORING.MONITORING_HEADER_XPATH, MONITORING.MONITORING_URL_PATH)
    def view_data_for_appliance(self, appliance):
        self.select_custom_dropdown(MONITORING.VIEW_DATA_FOR, appliance)
        self._info("Viewing data for appliance:%s"%appliance)

    @visit_page(MONITORING.MONITORING_HEADER_XPATH, MONITORING.MONITORING_URL_PATH)
    def go_to_monitoring_page(self):
        self._info('visiting to monitoring page.')

    @visit_page(MONITORING.MONITORING_HEADER_XPATH, MONITORING.MONITORING_URL_PATH , wait=False)
    def go_to_monitoring_page_nowait(self):
        self._info('Visiting to monitoring page without wait')

    def select_time_range(self, value):
        self.select_custom_dropdown(MONITORING.TIME_RANGE, value)
        self._info('selecting time range:%s'%value)

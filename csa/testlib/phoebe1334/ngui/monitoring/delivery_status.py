from common.gui.decorators import visit_page
from common.ngui.exceptions import DataNotFoundError, BackEndProcessingError
from common.ngui.ngguicommon import NGGuiCommon

class DeliveryStatus(NGGuiCommon):

    def get_keyword_names(self):
        return ['outgoing_destinations_status', 'retry_all_delivery']

    def retry_all_delivery(self):
        if self._is_element_present(OutgoingDestination.retry_all_button):
            self.click_element(OutgoingDestination.retry_all_button)
            if self.check_for_backend_error():
                raise BackEndProcessingError
            if not self._is_element_present(OutgoingDestination.destination_status_table):
                raise DataNotFoundError('outgoing destinations status not visible after retry')
        else:
            raise DataNotFoundError('Retry all delivery is not found')

    def _get_row_detail(self, rowindex, status_headers, header_count=0):
        row_details = {}
        fields_data = {}
        for columnindex in range(1, header_count + 1):
            fields_data[status_headers[columnindex-1]] = self.get_text('%s' % ( \
                    OutgoingDestination.details_row_fields % (OutgoingDestination.detail_row,
                                                              rowindex, columnindex)))
        row_details[fields_data[status_headers[0]]] = fields_data
        return row_details

    def outgoing_destinations_status(self ):
        status_headers = []
        status_summary = {}
        if self._is_element_present(OutgoingDestination.destination_status_header):
            self.set_selenium_speed('0s')
            header_count  = self.get_element_count(OutgoingDestination.destination_status_header)
            for header in range(1, header_count+1):
                status_headers.append(self.get_text('%s/div[%s]' %(OutgoingDestination.destination_status_header_row, \
                                                                   header)))
            details_row_count = self.get_element_count(OutgoingDestination.detail_row)
            for eachrow in range(1, details_row_count+1):
                status_summary.update(self._get_row_detail(eachrow, status_headers, header_count))
            self.set_selenium_speed('0.5s')
            return status_summary
        else:
            raise DataNotFoundError('Failed to find the Outgoing destinations status data')

class OutgoingDestination:
    destination_status_table = "//*[@class='ui-grid-contents-wrapper']"
    destination_status_header_row = "%s/div/div[1]/div/div/div/div/div" %(destination_status_table)
    destination_status_header = "%s/div/div[1]/div/div/div/div/div/div" %(destination_status_table)
    detail_row = '%s/div/div[2]/div/div' %(destination_status_table)
    details_row_fields = '%s[%s]/div/div[%s]'
    retry_all_button = "//label[@translate='buttons.retryAllDelivery']"
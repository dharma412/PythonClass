from common.gui.decorators import visit_page
from common.ngui.exceptions import DataNotFoundError, BackEndProcessingError
from common.ngui.ngguicommon import NGGuiCommon

class DeliveryStatus(NGGuiCommon):

    def get_keyword_names(self):
        return ['outgoing_destinations_status', 'retry_all_delivery', 'favourite_outgoing_destinations_status',
                'export_outgoing_destinations_status', 'delivery_status_host_status_details',
                'delivery_status_delivery_information_details', 'delivery_status_counters_details',
                'delivery_status_gauges_details', 'delivery_status_ordered_ip_addresses_details',
                'delivery_status_mx_records_details', 'delivery_status_smtp_routes_for_this_host',
                'export_outgoing_destinations_status_details','outgoing_destinations_tracking_redirect']

    def retry_all_delivery(self):
        if self._is_element_present(OutgoingDestination.retry_all_button):
            self.click_element(OutgoingDestination.retry_all_button)
            if self.check_for_backend_error():
                raise BackEndProcessingError
            if not self._is_element_present(OutgoingDestination.destination_status_table):
                raise DataNotFoundError('outgoing destinations status not visible after retry')
        else:
            raise DataNotFoundError('Retry all delivery is not found')

    def _get_row_detail(self, rowindex, status_headers, value_row, row_fields, header_count=0):
        row_details = {}
        fields_data = {}
        for columnindex in range(1, header_count + 1):
            fields_data[status_headers[columnindex-1]] = self.get_text('%s' % ( \
                    row_fields % (value_row, rowindex, columnindex)))
        row_details[fields_data[status_headers[0]]] = fields_data
        return row_details

    def _get_table_data(self, table, header_row, value_row, row_fields):
        status_summary = {}
        status_headers = []
        self.set_selenium_speed('0s')
        header_count = self.get_element_count(table)
        for header in range(1, header_count + 1):
            status_headers.append(self.get_text('%s/div[%s]' % (header_row, header)))
        details_row_count = self.get_element_count(value_row)
        for eachrow in range(1, details_row_count + 1):
            status_summary.update(self._get_row_detail(eachrow, status_headers, value_row, row_fields, header_count))
        self.set_selenium_speed('0.5s')
        return status_summary

    def outgoing_destinations_status(self ):
        """
        This keyword will return the Outgoing Destinations Status table data
        :return: outgoing_destinations_status summary
        """
        status_headers = []
        status_summary = {}
        if self._is_element_present(OutgoingDestination.destination_status_header):
            status_summary = self._get_table_data(OutgoingDestination.destination_status_header,
                                                  OutgoingDestination.destination_status_header_row,
                                                  OutgoingDestination.detail_row,
                                                  OutgoingDestination.details_row_fields)
            return status_summary
        else:
            raise DataNotFoundError('Failed to find the Outgoing destinations status data')

    def outgoing_destinations_tracking_redirect(self, destination_domain, track):
        """
        To redirect outgoing_destinations_tracking_redirect
        :param destination_domain: name of the destination domain :cisco.com, the.encryption.queue
        :param track: Active Recipients,Delivery Recipients
        :return:
        # After using this window use tracking related keywords for verification use keyword
        select_window   MAIN
        to back to main window..
        """
        tracking_headers = {'Active Recipients':3, 'Connection Out':4, 'Delivery Recipients':5,
                            'Soft Bounced': 6, 'Hard Bounced':7}
        if not tracking_headers.has_key(track):
            raise DataNotFoundError('Tracking header name is incorrect..')
        if self._is_element_present(OutgoingDestination.destination_domain_name %destination_domain):
            if track == 'Hard Bounced':
                redirect_cell = '%s%s' % (OutgoingDestination.destination_domain_name % destination_domain,
                                          OutgoingDestination.tracking_header_bounce % tracking_headers[track])
            else:
                redirect_cell = '%s%s'%(OutgoingDestination.destination_domain_name %destination_domain,
                                    OutgoingDestination.tracking_header%tracking_headers[track])
            if self._is_element_present(redirect_cell):
                self.click_element(redirect_cell)
                self.select_window('NEW')
            else:
                raise DataNotFoundError('Tracking redirection is not enabled')
        else:
            raise DataNotFoundError('Failed to find the Outgoing destination domain')

    def favourite_outgoing_destinations_status(self):
        """
        This keyword is add outgoing destinations status data to the favourite
        :return:
        """
        if not self._is_element_present(OutgoingDestination.favourite):
            raise DataNotFoundError('outgoing destinations favourite is not visible')
        else:
            self.click_element(OutgoingDestination.favourite)

    def export_outgoing_destinations_status(self):
        """
        This keyword to export the outgoing destinations status data
        :return:
        """
        if not self._is_element_present(OutgoingDestination.export):
            raise DataNotFoundError('outgoing destinations export is not visible')
        else:
            self.click_element(OutgoingDestination.export)
            self._wait_until_element_is_present(OutgoingDestination.download_dialog, timeout=10)
            self.click_element(OutgoingDestination.download)

    def _get_gauge_data(self, gauge):
        result_dict = {}
        value_dict = {}
        self.set_selenium_speed('0s')
        gauage_count = self.get_element_count(gauge)
        gaugekey = self.get_text('%s[1]'%gauge)
        for eachgauge in range(2, gauage_count+1):
            gauge_value = '%s[%s]/div[2]' % (gauge, eachgauge)
            if self._is_visible(gauge_value):
                value_dict[self.get_text('%s[%s]/div[1]' %(gauge, eachgauge))] = self.get_text(gauge_value)
        self.set_selenium_speed('0.5s')
        result_dict[gaugekey] = value_dict
        return result_dict

    def _navigate_to_destination_domain(self, destination_domain):
        if not self._is_element_present(OutgoingDestination.menu_slider_name):
            destination_name = OutgoingDestination.destination_domain % destination_domain
            if not self._is_element_present(destination_name):
                raise DataNotFoundError('Destination domain:%s does not exists'%destination_domain)
            else:
                self.click_element(destination_name)
        else:
            self._debug('Already in the destination domain page')

    def delivery_status_host_status_details(self, destination_domain):
        """
        To get the details for destination domain Host Status
        :param destination_domain:
        :return: table details in dict
        """
        self._navigate_to_destination_domain(destination_domain)
        return self._get_gauge_data(OutgoingDestination.host_status)

    def delivery_status_delivery_information_details(self, destination_domain):
        """
        To get the details for destination domain Host Status
        :param destination_domain:
        :return: table details in dict
        """
        self._navigate_to_destination_domain(destination_domain)
        return self._get_gauge_data(OutgoingDestination.delivery_information)


    def delivery_status_counters_details(self, destination_domain):
        """
        To get the details for destination domain counters details
        :param destination_domain:
        :return: table details in dict
        """
        self._navigate_to_destination_domain(destination_domain)
        return self._get_gauge_data(OutgoingDestination.counters)

    def delivery_status_gauges_details(self, destination_domain):
        """
        To get the details for destination domain gauges details
        :param destination_domain:
        :return: table details in dict
        """
        self._navigate_to_destination_domain(destination_domain)
        return self._get_gauge_data(OutgoingDestination.gauges)


    def delivery_status_ordered_ip_addresses_details(self, destination_domain):
        """
        To get the details for destination status ordered IP details
        :param destination_domain:
        :return: table details in dict
        """
        self._navigate_to_destination_domain(destination_domain)
        return self._get_table_data(OutgoingDestination.ordered_ip_address_header,
                                    OutgoingDestination.ordered_ip_address_header_row,
                                    OutgoingDestination.ordered_ip_address_detail_row,
                                    OutgoingDestination.ordered_ip_address_details_row_fields)


    def delivery_status_mx_records_details(self, destination_domain):
        """
        To get the details for destination MX records details
        :param destination_domain:
        :return: table details in dict
        """
        self._navigate_to_destination_domain(destination_domain)
        return self._get_table_data(OutgoingDestination.mx_records_header,
                                    OutgoingDestination.mx_records_header_row, \
                                    OutgoingDestination.mx_records_detail_row,
                                    OutgoingDestination.mx_records_details_row_fields)


    def delivery_status_smtp_routes_for_this_host(self, destination_domain):
        """
        To get the details for destination MX records details
        :param destination_domain:
        :return:table details in dict
        """
        self._navigate_to_destination_domain(destination_domain)
        return self._get_table_data(OutgoingDestination.smtp_routes_host_header,
                                    OutgoingDestination.smtp_routes_host_header_row, \
                                    OutgoingDestination.smtp_routes_host_detail_row,
                                    OutgoingDestination.smtp_routes_host_details_row_fields)

    def export_outgoing_destinations_status_details(self, destination_domain):
        """
        To export Outgoing Destination status details
        :param destination_domain:
        :return:
        """
        if not self._is_element_present(OutgoingDestination.details_export):
            raise DataNotFoundError('outgoing destinations details export is not visible')
        else:
            self.click_element(OutgoingDestination.details_export)
            self._wait_until_element_is_present(OutgoingDestination.download_dialog, timeout=10)
            self.click_element(OutgoingDestination.download)

class OutgoingDestination:
    destination_status_table = "//*[@class='ui-grid-contents-wrapper']"
    destination_status_header = "%s/div/div[1]/div/div/div/div/div/div" % (destination_status_table)
    destination_status_header_row = "%s/div/div[1]/div/div/div/div/div" %(destination_status_table)
    detail_row = '%s/div/div[2]/div/div' %(destination_status_table)
    details_row_fields = '%s[%s]/div/div[%s]'
    retry_all_button = "//label[@translate='buttons.retryAllDelivery']"
    favourite = "//*[@ng-click='$ctrl.toggleBlock()']"
    export  = "//*[@translate='buttons.export']"
    download_dialog = "//*[@translate='downloadPrintReports']"
    download = "//*[@translate='buttons.download']"
    host_status = "//*[@translate='monitoring.delivery_status_details.hostStatus']/../div"
    delivery_information = "//*[@translate='monitoring.delivery_status_details.deliveryInformation']/../div"
    counters = "//*[@translate='monitoring.delivery_status_details.softBouncedEvents']/../../div"
    gauges  = "//*[@translate='monitoring.delivery_status_details.unattemptedRecipients']/../../div"
    destination_domain = "//*[@ng-bind='row.entity[col.field]' and  contains(text(), '%s')]"
    menu_slider_name = "//*[@translate='menu_slider.reporting.deliveryStatusDetail']"
    ordered_ip_address_table = "//*[@table-data='$ctrl.tableData[1]']/div/div[2]/ngsma-custom-table/div/div"
    ordered_ip_address_header = "%s/div/div[1]/div/div/div/div/div/div" % (ordered_ip_address_table)
    ordered_ip_address_header_row = "%s/div/div[1]/div/div/div/div/div" %(ordered_ip_address_table)
    ordered_ip_address_detail_row = '%s/div/div[2]/div/div' %(ordered_ip_address_table)
    ordered_ip_address_details_row_fields = '%s[%s]/div/div[%s]'
    mx_records_table = "//*[@table-data='$ctrl.tableData[0]']/div/div[2]/ngsma-custom-table/div/div"
    mx_records_header = "%s/div/div[1]/div/div/div/div/div/div" % (mx_records_table)
    mx_records_header_row = "%s/div/div[1]/div/div/div/div/div" % (mx_records_table)
    mx_records_detail_row = '%s/div/div[2]/div/div' % (mx_records_table)
    mx_records_details_row_fields = '%s[%s]/div/div[%s]'
    smtp_routes_host_table = "//*[@table-data='$ctrl.tableData[2]']/div/div[2]/ngsma-custom-table/div/div"
    smtp_routes_host_header = "%s/div/div[1]/div/div/div/div/div/div" % (smtp_routes_host_table)
    smtp_routes_host_header_row = "%s/div/div[1]/div/div/div/div/div" % (smtp_routes_host_table)
    smtp_routes_host_detail_row = '%s/div/div[2]/div/div' % (smtp_routes_host_table)
    smtp_routes_host_details_row_fields = '%s[%s]/div/div[%s]'
    details_export = "//*[@id='export']"
    destination_domain_name = "//*[@class='ngsma-custom-table-cell ng-scope']//*[text()= '%s']"
    tracking_header = "/../../../../div[%s]/div[2]/a"
    tracking_header_bounce = "/../../../../div[%s]/div[1]/a"
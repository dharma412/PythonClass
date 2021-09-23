
from common.gui.decorators import visit_page
from common.ngui.exceptions import DataNotFoundError, BackEndProcessingError
from common.ngui.ngguicommon import NGGuiCommon

class SystemStatus(NGGuiCommon):

    def get_keyword_names(self):
        return ['get_mail_system_status', 'get_version_information', 'get_rates_events_per_hour_detail',
                'get_counters_detail', 'reset_counters','get_last_counter_reset', 'get_mail_processing_queue',
                'get_cpu_utilization','get_active_recipients_in_queue', 'get_general_resource_utilization',
                'get_queue_space', 'get_log_disk_utilization', 'get_hardware' ]

    def reset_counters(self):
        """
        This keyword will reset the counters
        :return: None
        """
        self.click_ng_button(System.reset_counter, '')
        self.wait_for_angular()

    def get_last_counter_reset(self):
        """
        This keyoword will get the last counter reset time
        :return: last counter reset time
        """
        return self.get_text(System.last_counter_reset)

    def _get_gauge_data(self, gauge):
        result_dict = {}
        value_dict = {}
        self.set_selenium_speed('0s')
        gauage_count = self.get_element_count(gauge)
        gaugekey = self.get_text('%s[1]'%gauge)
        for eachgauge in range(2, gauage_count+1):
            value_dict[self.get_text('%s[%s]/div[1]' %(gauge, eachgauge))] = self.get_text('%s[%s]/div[2]'%(gauge, \
                                                                                                            eachgauge))
        self.set_selenium_speed('0.5s')
        result_dict[gaugekey] = value_dict
        return result_dict

    def _get_table_content(self, table):
        self.set_selenium_speed('0s')
        counter_count = self.get_element_count(table)
        headers = []
        group_dict = {}
        group_name = ''
        group_dict['Total'] = {}
        for eachcolumn in range(1, 6):
            current_column = '%s[%s]/div[%s]' % (table, 1, eachcolumn)
            if self._is_visible(current_column):
                headers.append(self.get_text(current_column))
        for eachcounter in range(2, counter_count + 1):
            if self._is_visible('%s[%s]/div[%s]' % (table, eachcounter, 2)):
                current_event_name = self.get_text('%s[%s]/div[%s]' % (table, eachcounter, 1))
                if current_event_name:
                    group_name = current_event_name
                    group_dict[group_name] = {}
            row_tmp_dict = {}
            for eachcolumn in range(3, 6):
                current_column = '%s[%s]/div[%s]' % (table, eachcounter, eachcolumn)
                if self._is_visible(current_column):
                    row_tmp_dict[headers[eachcolumn -1]] = self.get_text(current_column)
            event_field = '%s[%s]/div[%s]' % (table, eachcounter, 2)
            if self._is_visible(event_field):
                event_text = self.get_text(event_field)
                if 'Total' in event_text:
                    group_name = 'Total'
                if group_dict[group_name].has_key(event_text):
                    group_dict[group_name][event_text].update(row_tmp_dict)
                else:
                    group_dict[group_name][event_text] = row_tmp_dict
        self.set_selenium_speed('0.5s')
        return group_dict

    def get_mail_system_status(self):
        """
        This keyword to get details under mail system status
        :return:
        """
        return {'System Status': self.get_text(System.system_status),
                 'Status as of': self.get_text(System.status_as_of),
                  'Up since' : self.get_text(System.up_since),
                 'Oldest message': self.get_text(System.oldest_message)}

    def get_version_information(self):
        """
        This keyword to get details under version Information
        :return:
        """
        return {'Model': self.get_text(System.model_info),
                        'Operating System' : self.get_text(System.operating_system),
                        'Build Date' : self.get_text(System.build_date),
                        'Install Date': self.get_text(System.install_date),
                        'Serial Number': self.get_text(System.serial_number)}

    def get_mail_processing_queue(self):
        """
        This keyword to get details under mail processing queue gauge
        :return:
        """
        return self._get_gauge_data(System.mailprocess_queue)

    def get_cpu_utilization(self):
        """
        This keyword to get details under cpu utilization gauge
        :return:
        """
        return self._get_gauge_data(System.cpu_utilization)

    def get_active_recipients_in_queue(self):
        """
        This keyword to get details under get active recipients in queue gauge
        :return:
        """
        return self._get_gauge_data(System.active_recp_queue)

    def get_general_resource_utilization(self):
        """
        This keyword to get details under get general resource utilization gauge
        :return:
        """
        return self._get_gauge_data(System.general_resource_utilization)

    def get_queue_space(self):
        """
        This keyword to get details under get queue space gauge
        :return:
        """
        return self._get_gauge_data(System.queue_space)

    def get_log_disk_utilization(self):
        """
        This keyword to get details under get log disk utilization gauge
        :return:
        """
        return self._get_gauge_data(System.log_disk_utilization)

    def get_hardware(self):
        """
        This keyword to get details under get hardware gauge
        :return:
        """
        return self._get_gauge_data(System.hardware)

    def get_rates_events_per_hour_detail(self):
        """
        This keyword to get details under get rates events per hour event data
        :return:
        """
        rates_details = self._get_table_content(System.rates)
        return rates_details

    def get_counters_detail(self):
        """
        This keyword to get details under get counters data
        :return:
        """
        counter_details = self._get_table_content(System.counters)
        return counter_details

class System:
    system_status = "//*[@translate='monitoring.system_status.systemStatus']/../div[2]"
    status_as_of = "//*[@translate='monitoring.system_status.statusAsOf']/../div[4]"
    up_since = "//*[@translate='monitoring.system_status.statusAsOf']/../div[5]"
    oldest_message = "//*[@translate='monitoring.system_status.statusAsOf']/../div[6]"
    model_info = "//*[@translate='monitoring.system_status.model']/../div[3]"
    operating_system  = "//*[@translate='monitoring.system_status.model']/../div[4]"
    build_date = "//*[@translate='monitoring.system_status.buildDate']/../div[4]"
    install_date = "//*[@translate='monitoring.system_status.buildDate']/../div[5]"
    serial_number = "//*[@translate='monitoring.system_status.buildDate']/../div[6]"
    rates = "//*[@translate='monitoring.system_status.mailHandlingRates']/../../div"
    counters = "//*[@translate='monitoring.system_status.mailHandlingEvents']/../../div"
    mailprocess_queue = "//*[@translate='monitoring.system_status.mailProcessingQueue']/../../div"
    cpu_utilization = "//*[@translate='monitoring.system_status.cpuUtilization']/../../div"
    active_recp_queue = "//*[@translate='monitoring.system_status.activeRecepientsInQueue']/../../div"
    general_resource_utilization = "//*[@translate='monitoring.system_status.generalResourceUtilization']/../../div"
    queue_space = "//*[@translate='monitoring.system_status.queueSpace']/../../div"
    log_disk_utilization = "//*[@translate='monitoring.system_status.loggingDiskUtilization']/../../div"
    hardware = "//*[@translate='monitoring.system_status.hardware']/../../div"
    reset_counter = '$ctrl.resetCounters()'
    last_counter_reset = "//*[@translate='monitoring.system_status.lastReset']/../span[2]"
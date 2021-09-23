#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/email/reporting/charts.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

import hashlib
import time
import tempfile
from urllib import urlencode
import uuid

from common.gui.guicommon import GuiCommon
from credentials import DUT_ADMIN, DUT_ADMIN_PASSWORD
from sal.clients.crawler import DownloadLinkBuilder
from sal.clients.crawler import download as download_file_from_dut


UNIQ_QUERY_TEMPLATE = lambda name, guid: '%s-%s' % (name, guid)

class ChartLinkBuilder(DownloadLinkBuilder):
    CHART_LINK_BASE = 'chart'

    COMMON_CHART_LINK_QUERY_PARAMS = {'width': '',
                                      'height': '',
                                      'ts': '',
                                      'widget': 'chart_stacked_bar',
                                      'type': 'hor_stacked_bar',
                                      'report_type': 'phoebe',
                                      'XLabel': 'Messages', }

    CHART_NAMES = {'Incoming Mail Graph': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': 'sma_overview_incoming_mail_over_time',
                                           'report_def_id': 'sma_overview',
                                           'YLabel': 'Messages',
                                           'XLabel': ''},
                   'Outgoing Mail Graph': {'section_id': 'ss_0_1_0',
                                           'uniq_query_id': 'sma_overview_outgoing_mail_over_time',
                                           'report_def_id': 'sma_overview',
                                           'YLabel': 'Messages',
                                           'XLabel': ''},

                   'Top Senders by Total Threat Messages': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': 'sma_incoming_mail_top_domain_threat_messages',
                                           'report_def_id': 'sma_incoming_mail'},
                   'Top Senders by Clean Messages': {'section_id': 'ss_0_0_1',
                                           'uniq_query_id': 'sma_incoming_mail_top_domain_clean_messages',
                                           'report_def_id': 'sma_incoming_mail',
                                           'profile_type': 'domain'},

                   'Top Destinations by Total Threat Messages': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': 'mga_destination_domains_top_threat',
                                           'report_def_id': 'mga_destination_domains'},
                   'Top Destinations by Clean Messages': {'section_id': 'ss_0_0_1',
                                           'uniq_query_id': 'mga_destination_domains_top_clean',
                                           'report_def_id': 'mga_destination_domains'},

                   'Top Outgoing Senders by Total Threat Messages': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': 'mga_internal_senders_top_threat',
                                           'report_def_id': 'mga_internal_senders',
                                           'XLabel': 'Messages',
                                           'profile_type': 'sender_domain'},
                   'Top Outgoing Senders by Clean Messages': {'section_id': 'ss_0_0_1',
                                           'uniq_query_id': 'mga_internal_senders_top_clean',
                                           'report_def_id': 'mga_internal_senders',
                                           'profile_type': 'sender_domain'},

                   'Top Users by Clean Incoming Messages': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': 'sma_internal_users_top_incoming_messages',
                                           'report_def_id': 'sma_internal_users'},
                   'Top Users by Clean Outgoing Messages': {'section_id': 'ss_0_0_1',
                                           'uniq_query_id': 'sma_internal_users_top_outgoing_messages',
                                           'report_def_id': 'sma_internal_users'},

                   'Top Incoming Content Filter Matches': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': 'mga_content_filters_top_incoming_cf_matches',
                                           'report_def_id': 'mga_content_filters'},
                   'Top Outgoing Content Filter Matches': {'section_id': 'ss_0_0_1',
                                           'uniq_query_id': 'mga_content_filters_top_outgoing_cf_matches',
                                           'report_def_id': 'mga_content_filters'},

                   'Top Incoming Virus Types Detected': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': 'mga_virus_types_top_incoming_virus_types',
                                           'report_def_id': 'mga_virus_types'},
                   'Top Outgoing Virus Types Detected': {'section_id': 'ss_0_0_1',
                                           'uniq_query_id': 'mga_virus_types_top_outgoing_virus_types',
                                           'report_def_id': 'mga_virus_types'},

                   'Incoming TLS Connections Graph': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': 'mga_tls_connections_received_tls_graph',
                                           'report_def_id': 'mga_tls_connections',
                                           'YLabel': 'Connections',
                                           'XLabel': ''},
                   'Outgoing TLS Connections Graph': {'section_id': 'ss_0_3_0',
                                           'uniq_query_id': 'mga_tls_connections_sent_tls_graph',
                                           'report_def_id': 'mga_tls_connections',
                                           'YLabel': 'Connections',
                                           'XLabel': ''},

                   'Top Offenders by Incident': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': 'mga_rate_limit_sender_top_senders_by_incidents',
                                           'report_def_id': 'mga_rate_limit_sender',
                                           'XLabel': ''},
                   'Top Offenders by Rejected Recipients': {'section_id': 'ss_0_0_1',
                                           'uniq_query_id': 'mga_rate_limit_sender_top_senders_by_rejected_recipients',
                                           'report_def_id': 'mga_rate_limit_sender',
                                           'XLabel': ''},

                   'Overall Reporting Data Availability': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': 'sma_data_status_data_status_total',
                                           'report_def_id': 'sma_data_status',
                                           'XLabel': '',
                                           'type': '',
                                           'YLabel': '% Data Available'},

                   'Average Time Spent in Work Queue': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': 'sma_system_capacity_average_time_workqueue',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': 'time',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'Average Messages in Work Queue': {'section_id': 'ss_0_1_0',
                                           'uniq_query_id': 'sma_system_capacity_average_messages_workqueue',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': 'Messages',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'Maximum Messages in Work Queue': {'section_id': 'ss_0_2_0',
                                           'uniq_query_id': 'sma_system_capacity_max_messages_workqueue',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': 'Messages',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'Total Incoming Connections': {'section_id': 'ss_0_3_0',
                                           'uniq_query_id': 'sma_system_capacity_total_incoming_connections',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': 'Connections',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'Total Incoming Messages': {'section_id': 'ss_0_4_0',
                                           'uniq_query_id': 'sma_system_capacity_total_incoming_messages',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': 'Messages',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'Average Incoming Message Size (Bytes)': {'section_id': 'ss_0_5_0',
                                           'uniq_query_id': 'sma_system_capacity_average_incoming_message_size',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': 'Message Size',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'Total Incoming Message Size (Bytes)': {'section_id': 'ss_0_6_0',
                                           'uniq_query_id': 'sma_system_capacity_total_incoming_message_size',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': 'Message Size',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'Total Outgoing Connections': {'section_id': 'ss_0_7_0',
                                           'uniq_query_id': 'sma_system_capacity_total_outgoing_connections',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': 'Connections',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'Total Outgoing Messages': {'section_id': 'ss_0_8_0',
                                           'uniq_query_id': 'sma_system_capacity_total_outgoing_messages',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': 'Messages',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'Average Outgoing Message Size (Bytes)': {'section_id': 'ss_0_9_0',
                                           'uniq_query_id': 'sma_system_capacity_average_outgoing_message_size',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': 'Message Size',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'Total Outgoing Message Size (Bytes)': {'section_id': 'ss_0_10_0',
                                           'uniq_query_id': 'sma_system_capacity_total_outgoing_message_size',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': 'Message Size',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'Overall CPU Usage': {'section_id': 'ss_0_11_0',
                                           'uniq_query_id': 'sma_system_capacity_overall_cpu_usage',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': '% CPU',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'CPU by Function': {'section_id': 'ss_0_12_0',
                                           'uniq_query_id': 'sma_system_capacity_cpu_by_function',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': '% CPU',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},
                   'Memory Page Swapping': {'section_id': 'ss_0_13_0',
                                           'uniq_query_id': 'sma_system_capacity_swap_page_out',
                                           'report_def_id': 'sma_system_capacity',
                                           'XLabel': '',
                                           'YLabel': 'Pages',
                                           'type': 'line',
                                           'profile_type': 'all',
                                           'widget': 'chart_line'},

                   'Threats by Type': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': \
                                                'mga_virus_outbreaks_threats_by_type',
                                           'report_def_id': 'mga_virus_outbreaks',
                                           'type': 'hor_stacked_bar'},

                   'Top Incidents by Severity': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id': \
                                             'mga_dlp_incident_summary_top_incidents_by_severity',
                                           'report_def_id': 'mga_dlp_incident_summary',
                                           'XLabel': '',
                                           'type': 'line'},
                   'Top DLP Policy Matches': {'section_id': 'ss_0_1_0',
                                           'uniq_query_id':  \
                                             'mga_dlp_incident_summary_top_dlp_policy_matches',
                                           'report_def_id': 'mga_dlp_incident_summary',
                                           'XLabel': '',
                                           'type': 'line'},
                   'Top External Threat Feed Sources': {'section_id': 'ss_0_0_0',
                                           'uniq_query_id':  \
                                             'mga_threatfeed_tf_graph_top_sources',
                                           'report_def_id': 'mga_threatfeed',
                                           'XLabel': '',
                                           'type': 'hor_stacked_bar',
                                           'widget': 'chart_hor_stacked_bar',
                                           'width': '250',
                                           'height': '280'},
                    'Top Indicator of Compromise (IOC) Matches': {'section_id': 'ss_0_1_0',
                                           'uniq_query_id':  \
                                             'mga_threatfeed_tf_graph_top_iocs',
                                           'report_def_id': 'mga_threatfeed',
                                           'XLabel': '',
                                           'type': 'hor_stacked_bar',
                                           'widget': 'chart_hor_stacked_bar',
                                           'width': '250',
                                           'height': '130'},
                    'Top External Threat Feed Sources by incoming mail connections': {'section_id': 'ss_0_2_0',
                                           'uniq_query_id':  \
                                             'mga_threatfeed_tf_graph_connection',
                                           'report_def_id': 'mga_threatfeed',
                                           'XLabel': '',
                                           'type': 'hor_stacked_bar',
                                           'widget': 'chart_hor_stacked_bar'}}

    def __init__(self, name, time_range=None, width=255, height=255):
        if name not in self.CHART_NAMES.keys():
            raise ValueError('Chart name "{0}" value is not valid. Available '\
                             'chart names: {1}'.format(name,
                                                       self.CHART_NAMES.keys()))
        self._time_range = time_range
        self._name = name
        self._width = width
        self._height = height

    def _get_query(self):
        querydict = self.COMMON_CHART_LINK_QUERY_PARAMS.copy()

        self._add_formatted_range_parameter(self._time_range, querydict)
        querydict['width'] = str(self._width)
        querydict['height'] = str(self._height)
        querydict.update(self.CHART_NAMES[self._name])
        querydict['uniq_query_id'] = \
                    UNIQ_QUERY_TEMPLATE(querydict['uniq_query_id'],
                                        str(uuid.uuid1()))
        querydict['ts'] = str(time.time())
        return urlencode(querydict)

    def _get_path(self):
        return self.CHART_LINK_BASE


DEFAULT_CHART_WIDTH = 255
DEFAULT_CHART_HEIGHT = 255

class EmailReportingCharts(GuiCommon):
    """Keywords are used to handle email reporting charts as image files.
    """

    def get_keyword_names(self):
        return ['email_reporting_charts_download',
                'email_reporting_charts_get_md5_hash']

    def email_reporting_charts_download(self, name, time_range=None, dest_path=None,
                                        width=DEFAULT_CHART_WIDTH,
                                        height=DEFAULT_CHART_HEIGHT,
                                        username=DUT_ADMIN,
                                        password=DUT_ADMIN_PASSWORD):
        """Download Email Reporting chart from appliance to local
        file system

        *Parameters:*
        - `name`: chart name. Available chart names are:
        | Incoming Mail Graph |
        | Outgoing Mail Graph |
        | Top Senders by Total Threat Messages |
        | Top Senders by Clean Messages |
        | Top Destinations by Total Threat Messages |
        | Top Destinations by Clean Messages |
        | Top Outgoing Senders by Total Threat Messages |
        | Top Outgoing Senders by Clean Messages |
        | Top Users by Clean Incoming Messages |
        | Top Users by Clean Outgoing Messages |
        | Top Incoming Content Filter Matches |
        | Top Outgoing Content Filter Matches |
        | Top Incoming Virus Types Detected |
        | Top Outgoing Virus Types Detected |
        | Incoming TLS Connections Graph |
        | Outgoing TLS Connections Graph |
        | Top Offenders by Incident |
        | Top Offenders by Rejected Recipients |
        | Overall Reporting Data Availability |
        | Average Time Spent in Work Queue |
        | Average Messages in Work Queue |
        | Maximum Messages in Work Queue |
        | Total Incoming Connections' |
        | Total Incoming Messages |
        | Average Incoming Message Size (Bytes) |
        | Total Incoming Message Size (Bytes) |
        | Total Outgoing Connections |
        | Total Outgoing Messages |
        | Average Outgoing Message Size (Bytes) |
        | Total Outgoing Message Size (Bytes) |
        | Overall CPU Usage |
        | CPU by Function |
        | Memory Page Swapping |
        | Threats by Type |
        | Top Incidents by Severity|
        | Top DLP Policy Matches |

        - `time_range`: time range for which statistical data
        should be shown. There can be predefined values:
        | Day |
        | Week |
        | Month |
        | Quarter |
        | Year |
        | Previous Day |
        | Previous Month |

        or custom ones in format `%m/%d/%Y %H, %m/%d/%Y %H`,
        where the first timestamp is period start datetime and the second
        timestamp is period end datetime
        - `dest_path`: destination path to where an image should be saved.
        If this parameter is ignored then temporary path
        (mkstemp(suffix='.png')) will be used
        - `width`: the width of downloaded image
        - `height`: the height of downloaded image
        - `username`: valid appliance username (DUT_ADMIN by default)
        - `password`: valid appliance username's password
        (DUT_ADMIN_PASSWORD by default)

        *Return:*
        - path to downloaded image

        *Examples:*
        | ${width}= | Set Variable | 300 |
        | ${height}= | Set Variable | 300 |
        | ${path}= | Email Reporting Charts Download |
        | ... | Incoming Mail Graph | 8/1/2013 0, 8/5/2013 10 |
        | ... | width=${width} | height=${height} |
        | ${output}= | OperatingSystem.Run | file "${path}" |
        | Should Contain | ${output} |
        | ... | PNG image data, ${width} x ${height} |
        | OperatingSystem.Remove File | ${path} |
        """
        relative_url = ChartLinkBuilder(name,
                                        time_range,
                                        int(width),
                                        int(height)).get_link()
        image_in_memory = download_file_from_dut(self.dut, relative_url,
                                                 username, password)
        if dest_path is None:
            dest_path = tempfile.mkstemp(suffix='.png')[1]
        with open(dest_path, 'wb') as f:
            f.write(image_in_memory.read())
        return dest_path

    def email_reporting_charts_get_md5_hash(self, name, time_range=None,
                                            width=DEFAULT_CHART_WIDTH,
                                            height=DEFAULT_CHART_HEIGHT,
                                            username=DUT_ADMIN,
                                            password=DUT_ADMIN_PASSWORD):
        """Download Email Reporting chart from appliance to local
        file system and return its md5 hash

        *Parameters:*
        - `name`: chart name. See `Email Reporting Charts Download`
        keyword parameters description for possible values list
        - `time_range`: time range for which statistical data
        should be shown. See `Email Reporting Charts Download`
        keyword parameters description for possible values list
        - `width`: the width of downloaded image
        - `height`: the height of downloaded image
        - `username`: valid appliance username (DUT_ADMIN by default)
        - `password`: valid appliance username's password
        (DUT_ADMIN_PASSWORD by default)

        *Return:*
        - md5 hash of downloaded image as hexdigest string

        *Examples:*
        | @{common_chart_params}= | Create List |
        | ... | Top Senders by Total Threat Messages | Month |
        | @{hashes}= | Create List |
        | :FOR | ${idx} | IN RANGE | 2 |
        | \ | ${hash}= | Email Reporting Charts Get MD5 Hash |
        | \ | ... | @{common_chart_params} |
        | \ | Append to List | ${hashes} | ${hash} |
        | Should Be Equal As Strings | @{hashes}[0] | @{hashes}[1] |
        """
        relative_url = ChartLinkBuilder(name,
                                        time_range,
                                        int(width),
                                        int(height)).get_link()
        image_in_memory = download_file_from_dut(self.dut, relative_url,
                                                 username, password)
        return hashlib.md5(image_in_memory.read()).hexdigest()

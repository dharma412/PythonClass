#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/esa_out_destinations.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_email_reports
from report_interface import ReportInfoHolder


class EsaOutDestinationsReport(ReportInfoHolder):
    """
    | OUT_DESTINATIONS | 'Outgoing Destinations' |

    Sorting column values for this email reports:

    Outgoing Destinations:
    | 'spam'            |
    | 'virus'           |
    | 'stopped'         |
    | 'threat'          |
    | 'clean'           |
    | 'total processed' |
    | 'hard'            |
    | 'delivered'       |
    | 'total delivered' |

    """

    outgoing_dest_detail_col_types = \
        {'spam': 'Spam Detected',
         'virus': 'Virus Detected',
         'stopped': 'Stopped by Content Filter',
         'threat': 'Total Threat',
         'clean': 'Clean',
         'total processed': 'Total Processed',
         'hard': 'Hard Bounced',
         'delivered': 'Delivered',
         'total delivered': 'Total Messages Delivered'
         }

    def get_name(self):
        return sma_email_reports.OUT_DESTINATIONS

    def get_selector(self):
        return 'value=mga_destination_domains'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        select_name = 'sort_columns[mga_destination_domains_virus_types_detail]'
        values_map = {}
        for key, val in self.outgoing_dest_detail_col_types.iteritems():
            values_map[key] = 'label=%s' % (val,)
        table = (select_name, values_map)
        return [table]


# module functions
def get_reports():
    return [EsaOutDestinationsReport]

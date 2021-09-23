#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/esa_delivery.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_email_reports
from report_interface import ReportInfoHolder


class EsaDeliveryReport(ReportInfoHolder):
    """
    | DELIVERY | 'Delivery Status' |

    Sorting column values for this email reports:

    Delivery Status:
    | 'host status'     |
    | 'active'          |
    | 'connections out' |
    | 'delivered'       |
    | 'soft'            |
    | 'hard'            |

    """

    outgoing_dest_status_col_types = \
        {'host status': 'Latest Host Status',
         'active': 'Active Recipients',
         'connections out': 'Connections Out',
         'delivered': 'Delivered Recipients',
         'soft': 'Soft Bounced',
         'hard': 'Hard Bounced'
         }

    def get_name(self):
        return sma_email_reports.DELIVERY

    def get_selector(self):
        return 'value=mga_outgoing_delivery_status'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        select_name = 'sort_columns[mga_outgoing_delivery_status_status_table]'
        values_map = {}
        for key, val in self.outgoing_dest_status_col_types.iteritems():
            values_map[key] = 'label=%s' % (val,)
        table = (select_name, values_map)
        return [table]


# module functions
def get_reports():
    return [EsaDeliveryReport]

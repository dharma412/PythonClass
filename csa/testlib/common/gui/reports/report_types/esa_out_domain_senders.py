#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/esa_out_domain_senders.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_email_reports
from report_interface import ReportInfoHolder


class EsaOutDomainSendersReport(ReportInfoHolder):
    """
    | OUT_DOMAIN_SENDERS | 'Outgoing Senders: Domains' |

    Sorting column values for this email reports:

    Outgoing Senders: Domains:
    | 'spam'    |
    | 'virus'   |
    | 'stopped' |
    | 'threat'  |
    | 'clean'   |
    | 'total'   |

    """

    senders_detail_col_types = \
        {'spam': 'Spam Detected',
         'virus': 'Virus Detected',
         'stopped': 'Stopped by Content Filter',
         'threat': 'Total Threat',
         'clean': 'Clean',
         'total': 'Total Messages'
         }

    def get_name(self):
        return sma_email_reports.OUT_DOMAIN_SENDERS

    def get_selector(self):
        return 'value=mga_internal_senders'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        select_name = 'sort_columns[mga_internal_senders_sender_detail]'
        values_map = {}
        for key, val in self.senders_detail_col_types.iteritems():
            values_map[key] = 'label=%s' % (val,)
        table = (select_name, values_map)
        return [table]


# module functions
def get_reports():
    return [EsaOutDomainSendersReport]

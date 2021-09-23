#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/status.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

import re
from common.cli.clicommon import CliKeywordBase

class Status(CliKeywordBase):
    """Get system status"""

    def get_keyword_names(self):
        return ['status',
                'status_get_value'
               ]

    def status(self):
        """Get system status

        Parameters:
        None

        Examples:
        | ${result}= | Status |
        """
        status = self._cli.status()
        return status.clean_output

    def status_get_value(self, group_name, parameter_name, parameter_index=0):
        """Get a system status value

        Parameters:
        - `group_name`: group name
        - `parameter_name`: parameter name in the group
        - `parameter_index`: parameter index

        The list of available groups and appropriate parameters are following:
        | group name | parameter name |
        | system | up_since |
        | | system_status |
        | | status_as_of |
        | | last_counter_reset |
        | | oldest_message |
        | counter | recipients_received |
        | | icid |
        | | delivered_recipients |
        | | get_bounce_recipients |
        | | fivexx_hard_bounces |
        | | rejected_recipients |
        | | messages_received |
        | | dcid |
        | | mid |
        | | completed_recipients |
        | | filter_hard_bounces |
        | | dropped_messages |
        | | hard_bounced_recipients |
        | | deleted_recipients |
        | | other_hard_bounces |
        | | global_unsub_hits |
        | | soft_bounced_events |
        | | domainkeys_signed_msgs |
        | | expired_hard_bounces |
        | | dns_hard_bounces |
        | rate | recipients_received |
        | | messages_received |
        | | hard_bounced_receivents |
        | | completed_recipients |
        | | soft_bounced_events |
        | | delivered_recipients |
        | gauge | cpu_utilization_antivirus |
        | | messages_in_quarantine |
        | | disk_io_utilization |
        | | cpu_utilization_case |
        | | kilobytes_in_quarantine |
        | | attempted_recipients |
        | | cpu_utilization_total |
        | | ram_utilization |
        | | logging_disk_available |
        | | resource_conversation |
        | | destinations_in_memory |
        | | active_recipients |
        | | messages_in_work_queue |
        | | current_inbound_conn |
        | | kilobytes_used |
        | | logging_disk_usage |
        | | cpu_utilization_mga |
        | | kilobytes_free |
        | | current_outbound_conn |
        | | unattempted_recipients |
        | feature | ciscoironportspamquarantine |
        | | ciscoironportcentralizedemailmessagetracking |
        | | ciscoironportcentralizedwebreporting |
        | | incomingmailhandling |
        | | ciscoironportcentralizedemailreporting |
        | | ciscoironportcentralizedwebconfigurationmanager |

        The list of available groups and appropriate parameter indexes are following:
        | group name | parameter index |
        | system | 0, 1 - for parameter `up_since` |
        | | 0 - for all other parameters |
        | counter | 0, 1, 2, reset, uptime, lifetime |
        | rate | 0, 1, 2, 1min, 5min, 15min |

        Examples:
        | ${result}= | Status Get Value | system | up_since | 1 |
        | ${result}= | Status Get Value | counter | icid | uptime |
        | ${result}= | Status Get Value | rate | messages_received | 5min |
        | ${result}= | Status Get Value | gauge | kilobytes_used |
        | ${result}= | Status Get Value | feature | incomingmailhandling |
        """
        status =  self._cli.status()

        if parameter_index != 0:
            if re.match('[0-2]', parameter_index):
                parameter_index = int(parameter_index)
        result = None
        if group_name.lower() == 'system':
            result = status.get_system(parameter_name, idx=parameter_index)
        elif group_name.lower() == 'counter':
            result = status.get_counter(parameter_name, idx=parameter_index)
        elif group_name.lower() == 'rate':
            result = status.get_rate(parameter_name, idx=parameter_index)
        elif group_name.lower() == 'gauge':
            result = status.get_gauge(parameter_name)
        elif group_name.lower() == 'feature':
            result = status.get_feature(parameter_name)
        else:
            raise ValueError('Only names of'\
                ' existing groups should be used.')
        return result
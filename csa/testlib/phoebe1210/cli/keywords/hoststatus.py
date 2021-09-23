#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/hoststatus.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class Hoststatus(CliKeywordBase):
    """Get the status of the given hostname"""

    def get_keyword_names(self):
        return ['hoststatus',
                'hoststatus_get_value',
                ]

    def hoststatus(self, host_name):
        """Get the status of the given hostname

        *Parameters:*
        - `host_name`: host name

        *Examples:*
        | ${status_out}= | Hoststatus | example.com |
        """
        host_status = self._cli.hoststatus(host_name)
        return host_status.raw

    def hoststatus_get_value(self, host_name, group_name, parameter_name):
        """Get a value of a parameter from status of the given hostname

        *Parameters:*
        - `host_name`: host name
        - `group_name`: group name
        - `par_name`: parameter name in the group

        The list of available groups and appropriate parameters are following:
        | *group name* | *parameter name* |
        | system | status_for |
        |            | status_as_of |
        |            | up_down |
        | counter | soft_bounced_events |
        |         | completed_recipients |
        |         | hard_bounced_recipients |
        |         | dns_hard_bounces |
        |         | fivexx_hard_bounces |
        |         | filter_hard_bounces |
        |         | expired_hard_bounces |
        |         | other_hard_bounces |
        |         | delivered_recipients |
        |         | deleted_recipients |
        | gauge | active_recipients |
        |       | unattempted_recipients |
        |       | attempted_recipients |
        |       | current_outbound_connections |
        |       | pending_outbound_connections |
        |       | oldest_message |
        |       | last_activity |

        *Exceptions:*
            - `ValueError`: in case of not existing
                 group or parameter

        *Examples:*
        | ${par}= | Hoststatus Get Value | example.com | system | status_for |
        | ${par}= | Hoststatus Get Value | example.com | counter | completed_recipients |
        | ${par}= | Hoststatus Get Value | example.com | gauge | last_activity |
        """
        host_status = self._cli.hoststatus(host_name)

        result = None
        if group_name.lower() == 'system':
            result = host_status.get_system(parameter_name)
        elif group_name.lower() == 'counter':
            result = host_status.get_counter(parameter_name)
        elif group_name.lower() == 'gauge':
            result = host_status.get_gauge(parameter_name)
        else:
            raise ValueError('Only names of' \
                             ' existing groups should be used.')

        return result

#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/status.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class status(CliKeywordBase):
    """The status command is an administrative tool to provide specific
       functionality on your system
    """

    def get_keyword_names(self):
        return [
                'status_get_system',
                'status_get_counter',
                'status_get_rate',
                'status_get_gauge',
                'status_get_feature'
               ]


    def status_get_system(self, name, idx=0):

        """Displays the system status.


        *Parameters*:
        - `name` : Valid values are status_as_of, up_since,
                   last_counter_reset, system_status, oldest_message
        - `idx` :  Requires Integer value. idx can be 0 or 1 when *name* parameter is *up_since*.
                   For every other *name* idx must be 0

        *Returns*:
          A string

        *Examples*:

        | ${status} | Status get system | status_as_of | 0 |
        | ${status} | Status get system | status_as_of |   |
        | ${status} | Status get system | up_since | 1 |

        """

        return str(self._cli.status().get_system(name,int(idx)))

    def status_get_counter(self, name, idx=0):

        """Gets the counter values for the specified counter.


        *Parameters*:
        - `name` : Valid values are messages_received, recipients_received, gen_bounce_recipients,
                   rejected_recipients, dropped_messages, soft_bounced_events, completed_recipients,
                   hard_bounced_recipients, dns_hard_bounces, fivexx_hard_bounces, expired_hard_bounces,
                   filter_hard_bounces, other_hard_bounces, delivered_recipients, deleted_recipients,
                   global_unsub_hits, domainkeys_signed_msgs, mid, icid, dcid
        - `idx` :  Requires Integer value. idx can be 0,1,2, reset, uptime, lifetime.
                   The integers are mapped as follows:
                   0:reset,1:uptime,2:lifetime

        *Returns*:
          A string

        *Examples*:

        | ${imsgs_rec} | Status get counter | messages_received | 0 |
        | ${msgs_rec} | Status get counter | messages_received |  |

        """

        return str(self._cli.status().get_counter(name, int(idx)))

    def status_get_rate(self, name, idx=0):

        """Displays the status at the defined rate.


        *Parameters*:
        - `name` : Valid values are messages_received, recipients_received, soft_bounced_events,
                   completed_recipients, hard_boucned_recipients, delivered_recipients
        - `idx` : Requires Integer value. idx can be 0, 1, 2, 1min, 5min, 15Min.
                  The integers are mapped as follows:
                  0:1min, 1:5min, 2:15min

        *Returns*:
          A string

        *Examples*:

        | ${imsgs_rec} | Status get rate | messages_received | 0 |
        | ${imsgs_rec} | Status get rate | messages_received |   |

        """

        return str(self._cli.status().get_rate(name, int(idx)))

    def status_get_gauge(self, name):

        """Displays the gauge.


        *Parameters*:
        - `name` : Valid values are ram_utilization, cpu_utilization_total, cpu_utilization_mga,
                   cpu_utilization_case, cpu_utilization_bm_antispam, cpu_utilization_antivirus,
                   disk_io_utilization, resource_conservation, logging_disk_usage, logging_disk_available,
                   current_inbound_conn, current_outbound_conn, active_recipients, unattempted_recipients,
                   attempted_recipients, messages_in_work_queue, messages_in_quarantine, destinations_in_memory,
                   kilobytes_used, kilobytes_in_quarantine, kilobytes_free

        *Returns*:
          A string

        *Examples*:

        | ${ram_util} | Status get gauge | ram_utilization |
        | ${cpu_util} | Status get gauge | cpu_utilization_bm_antispam  |

        """

        return str(self._cli.status().get_gauge(name))

    def status_get_feature(self, name):

       """Displays the feature key status.


        *Parameters*:
        - `name` : Valid values are virusoutbreakfilters, ironportantispam, receiving, brightmail,
                   sophos, centralmgmt
                   Other fkey names are valid and accepted they are just not listed here.

        *Returns*:
          An integer. Seconds remaining.

        *Examples*:

        | ${temp} | Status get feature | incomingmailhandling |

       """

       return self._cli.status().get_feature(name)

#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/tophosts.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class Tophosts(CliKeywordBase):
    """Keywords for tophost CLI command."""

    def get_keyword_names(self):
        return ['tophosts',
                ]

    def tophosts(self, option=1):
        """
         Display the top hosts by queue size.

        *Parameters:*
        - `option`: what information you want to get. String. Posible values
          are: '1' - Active Recipients
          '2' - Connections Out
          '3' - Delivered Recipients
          '4' - Hard Bounced Recipients
          '5' - Soft Bounced Events
          Default is '1'.

        *Return:*
        Dictionary. Keys of this dictionary is numbers of ranks(ex. 1, 2, 3 )
        and 'date'. Key 'data' contain value wich represent date of status
        information. Rank's number keys value contain dictionary with statistic information and Recipient Host.
        Example of retrurn value:\n
        {'date': 'Mon Mar 26 12:56:14 2012 GMT', '1': {'active_recipients': 0.0,
        'host': 'the.encryption.queue', 'soft_bounced': 0.0, 'connection_out':
        0.0, 'hard_bounced': 0.0, 'delivered_recipients': 0.0}, '3':
        {'active_recipients': 0.0, 'host': 'the.euq.release.queue',
        'soft_bounced': 0.0, 'connection_out': 0.0, 'hard_bounced': 0.0,
        'delivered_recipients': 0.0}, '2': {'active_recipients': 0.0, 'host':
        'the.euq.queue', 'soft_bounced': 0.0, 'connection_out': 0.0,
        'hard_bounced': 0.0, 'delivered_recipients': 0.0}}

        *Exceptons:*
        None.

        *Examples:*
        | ${out} | Tophosts | 2 |
        | ${out} | Tophosts | 1 |
        """
        return self._cli.tophosts(option)

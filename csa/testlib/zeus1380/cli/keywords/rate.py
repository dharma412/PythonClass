#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/rate.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)

class Rate(CliKeywordBase):

    """Keywords for nslookup CLI command."""

    def get_keyword_names(self):
        return ['rate'
                ]

    def rate(self, *args):
        """ Display statistics over time.

        *Parameters*
        - `records`: how many lines of output you want to get. Default 2.
        - `sec`: Number of seconds to wait between displays. Default 10.
        - `batch`: run this command in batch mode? Boolean. Defaul ${False}

        *Return*
        Dictionary. Keys is time and values are list. Example:\n
        {'07:51:13': [0, 0, 230, 0, 263, 0, 8],
        '07:51:11': [0, 0, 230, 0, 263, 0, 8]}

        *Examples*
        | Rate |
        | Rate | records=3 | sec=4 |
        | Rate | sec=5 |
        | Rate | records=10 | sec=5 | batch_mode=${True} |
        """
        kwargs = self._parse_args(args)

        if kwargs.get('sec', None):
            kwargs['sec'] = int(kwargs.get('sec'))

        if kwargs.get('records', None):
            kwargs['records'] = int(kwargs.get('records'))

        return self._cli.rate( **kwargs)


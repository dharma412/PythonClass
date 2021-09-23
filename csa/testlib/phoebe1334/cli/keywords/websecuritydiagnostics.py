#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/websecuritydiagnostics.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class websecuritydiagnostics(CliKeywordBase):
    def get_keyword_names(self):
        return [
                'websecuritydiagnostics_get_general',
                'websecuritydiagnostics_get_responseTime',
                'websecuritydiagnostics_get_dnsLookupTime'
               ]

    def websecuritydiagnostics_get_general(self, name):

        """Displays the websecuritydiagnostics general info`.

        *Parameters*:
        - `cache_size` : Display the Cache size
        - `cache_hits` : Display the Cache hits

        *Returns*:
          A string

        *Examples*:
        | ${webstatus1} | Websecuritydiagnostics get general | cache_size |
        | ${webstatus2} | Websecuritydiagnostics get general | cache_hits |
        | Log | ${webstatus1} |
        | Log | ${webstatus2} |
        """

        return str(self._cli.websecuritydiagnostics().get_general(name))

    def websecuritydiagnostics_get_responseTime(self, name):

        """Gets the Response Time values.

        *Parameters*:
        - `minimum` : Display the minimum Response Time
        - `average` : Display the Average Response Time
        - `maximum` : Display the Maximum Response Time

        *Returns*:
          A string

        *Examples*:
        | ${webstatus3} | Websecuritydiagnostics get responseTime | minimum |
        | ${webstatus4} | Websecuritydiagnostics get responseTime | average |
        | ${webstatus5} | Websecuritydiagnostics get responseTime | maximum |
        | Log | ${webstatus3} |
        | Log | ${webstatus4} |
        | Log | ${webstatus5} |
        """

        return str(self._cli.websecuritydiagnostics().get_responseTime(name))

    def websecuritydiagnostics_get_dnsLookupTime(self, name):

        """Gets the Response Time values.

        *Parameters*:
        - `minimum` : Display the minimum DnsLookup Time
        - `average` : Display the Average DnsLookup Time
        - `maximum` : Display the Maximum DnsLookup Time

        *Returns*:
          A string

        *Examples*:
        | ${webstatus6} | Websecuritydiagnostics get dnsLookupTime | minimum |
        | ${webstatus7} | Websecuritydiagnostics get dnsLookupTime | average |
        | ${webstatus8} | Websecuritydiagnostics get dnsLookupTime | maximum |
        | Log | ${webstatus6} |
        | Log | ${webstatus7} |
        | Log | ${webstatus8} |
        """

        return str(self._cli.websecuritydiagnostics().get_dnsLookupTime(name))
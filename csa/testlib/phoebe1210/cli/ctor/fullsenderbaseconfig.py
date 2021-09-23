#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/fullsenderbaseconfig.py#1 $

"""
IAF 2 CLI command: fullsenderbaseconfig
"""

import clictorbase


class fullsenderbaseconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self, sb_hostname='phonehome.senderbase.org',
                 sb_port=443, update_freq=300, no_per_ip_stats='N',
                 max_ips=100000, verbose_logs='Y', custom_lookup='N',
                 custom_hostname='foo.bar.com'):
        self._sess.writeln('fullsenderbaseconfig')
        m = self._query('sharing not enabled', 'SenderBase upload hostname')
        if (m == 1):  # only asked if SBRS sharing enabled
            self._query_response(sb_hostname)
            self._query_response(sb_port)
            self._query_response(update_freq)
            self._query_response(no_per_ip_stats)
            if no_per_ip_stats.upper() == 'N':
                self._query_response(max_ips)
            self._query_response(verbose_logs)

        self._query_response(custom_lookup)
        if custom_lookup.upper() == 'Y':
            self._query_response(custom_hostname)
        self._wait_for_prompt()


if __name__ == '__main__':
    sess = clictorbase.get_sess()
    fsbc = fullsenderbaseconfig(sess)
    fsbc()

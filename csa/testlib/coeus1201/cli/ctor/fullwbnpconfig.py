#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/fullwbnpconfig.py#1 $

"""
IAF 2 CLI command: fullwbnpconfig
   - this is a hidden command.
"""

import clictorbase

DEFAULT = clictorbase.DEFAULT

class fullwbnpconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self,
                 extra_sampling=DEFAULT,
                 feedback_sampling=DEFAULT,
                 max_stats_size=DEFAULT,
                 stats_server_host=DEFAULT,
                 stats_server_port=DEFAULT,
                 upload_interval=DEFAULT,
                 user_sampling=DEFAULT,
                 verbose_logging=DEFAULT):

        self._sess.writeln('fullwbnpconfig')
        self._query_response(extra_sampling)
        self._query_response(feedback_sampling)
        self._query_response(max_stats_size)
        self._query_response(stats_server_host)
        self._query_response(stats_server_port)
        self._query_response(upload_interval)
        self._query_response(user_sampling)
        self._query_response(verbose_logging)
        self._wait_for_prompt()

if __name__ == '__main__':
    sess = clictorbase.get_sess()
    fwbnpc = fullwbnpconfig(sess)
    fwbnpc()
    fwbnpc(extra_sampling=30,
           feedback_sampling=80,
           manifest_server_host='manifest.wga',
           manifest_server_port=8080,
           max_stats_size=200000,
           stats_server_host='stats.wga',
           stats_server_port=8081,
           upload_interval=320,
           user_sampling=90,
           verbose_logging=1)


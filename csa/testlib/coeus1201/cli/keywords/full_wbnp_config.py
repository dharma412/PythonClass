#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/full_wbnp_config.py#1 $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class FullWbnpConfig(CliKeywordBase):

    """Hidden command for WBNP servers configuration."""

    def get_keyword_names(self):
        return [
            'full_wbnp_config',
        ]

    def full_wbnp_config(self,
              extra_sampling=DEFAULT,
              feedback_sampling=DEFAULT,
              max_stats_size=DEFAULT,
              stats_server_host=DEFAULT,
              stats_server_port=DEFAULT,
              upload_interval=DEFAULT,
              user_sampling=DEFAULT,
              verbose_logging=DEFAULT):

        """Full WBNP Config.
        Keyword for WBNP servers configuring.

        Parameters:
        - `extra_sampling`: extra sampling value. Must be an integer
                        from 1 to 100.
        - `feedback_sampling`: feedback sampling value. Must be an integer
                        from 1 to 100.
        - `max_stats_size`: max statistic file size. Must be an integer
                        from 1,000 to 1,000,000,000.
        - `stats_server_host`: statistic server host. The address must be
                        a hostname or an IP.
        - `stats_server_port`: statistic server port. Must be a number
                        from 1 to 65535.
        - `upload_interval`: interval before every data upload. Must be
                        an integer from 20 to 3,600.
        - `user_sampling`: user sampling value. Must be an integer
                        from 1 to 100.
        - `verbose_logging`: logging verbose level. Must be one of these:
                        'yes', 'no', 'true' or 'false'.

        Examples:
        | Full Wbnp Config | #nothing will be changed |
        | Full Wbnp Config |
        | ... | extra_sampling=30 |
        | ... | feedback_sampling=80 |
        | ... | max_stats_size=200000 |
        | ... | stats_server_host=stats.wga |
        | ... | stats_server_port=8081 |
        | ... | upload_interval=320 |
        | ... | user_sampling=90 |
        | ... | verbose_logging=1 |
        """

        if extra_sampling != '' or extra_sampling is None:
            extra_sampling = int(extra_sampling)

        if feedback_sampling != '' or feedback_sampling is None:
            feedback_sampling = int(feedback_sampling)

        if max_stats_size != '' or max_stats_size is None:
            max_stats_size = int(max_stats_size)

        if stats_server_port != '' or stats_server_port is None:
            stats_server_port = int(stats_server_port)

        if upload_interval != '' or upload_interval is None:
            upload_interval = int(upload_interval)

        if user_sampling != '' or user_sampling is None:
            user_sampling = int(user_sampling)

        if verbose_logging != '' or verbose_logging is None:
            verbose_logging = int(verbose_logging)

        self._cli.fullwbnpconfig(
            extra_sampling,
            feedback_sampling,
            max_stats_size,
            stats_server_host,
            stats_server_port,
            upload_interval,
            user_sampling,
            verbose_logging
        )


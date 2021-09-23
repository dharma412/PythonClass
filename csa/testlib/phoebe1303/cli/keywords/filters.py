#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/filters.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class Filters(CliKeywordBase):
    """
    Manage message filters..
    CLI command: filters
    """

    def get_keyword_names(self):
        return ['filters_new',
                'filters_delete',
                'filters_import',
                'filters_export',
                'filters_move',
                'filters_set',
                'filters_list',
                'filters_detail',
                'filters_rollovernow',
                'filters_logconfig_edit',]

    def filters_new(self, *args):
        """Create a new filter.

        CLI command: filters > new

        *Parameters:*
        - `script`: Filter script. Required.

        *Return:*
        None

        *Examples:*
        | Filters New | script=${f1}: if (true) { log('${f1}'); } |

        | Filters New | script=f2: if (true) { log('${f2}'); } |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.filters().new(**kwargs)

    def filters_delete(self, *args):
        """Remove a filter.

        CLI command: filters > delete

        *Parameters:*
        - `filter`: Filter to delete. Required.

        *Return:*
        None

        *Examples:*
        | Filters Delete | filter=f1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.filters().delete(**kwargs)

    def filters_import(self, *args):
        """Import filters from file.

        CLI command: filters > import

        *Parameters:*
        - `filename`: The filename to import filter(s) from.
        - `encoding`: The encoding to use for the imported file.

        *Return:*
        None

        *Examples:*
        | Filters Import | filename=${exported_active} | encoding=Unicode (UTF-8) |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.filters().import_filter(**kwargs)

    def filters_export(self, *args):
        """Export filter to file.

        CLI command: filters > export

        *Parameters:*
        - `filename`: The name of the file to export to.
        - `encoding`: The encoding to use for the exported file.

        *Return:*
        None

        *Examples:*
        | Filters Export | filename=${exported_inactive} | encoding=Unicode (UTF-8) |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.filters().export_filter(**kwargs)

    def filters_move(self, *args):
        """Move a filter to a different position.

        CLI command: filters > move

        *Parameters:*
        - `filter_to_move`: The filter to move.
        - `target_filter`: The target filter.

        *Return:*
        None

        *Examples:*
        | Filters Move | filter_to_move=${f1} | target_filter=${f3} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.filters().move(**kwargs)

    def filters_set(self, *args):
        """Set a filter attribute.

        CLI command: filters > set

        *Parameters:*
        - `filter`: The filter name, number, or range. Use _all_ to alter all filters.
        - `attribute`: The attribute to set. Either _'Active'_ or _'Inactive'_.

        *Return:*
        None

        *Examples:*
        | Filters Set | filter=all | attribute=Inactive |
        | Filters Set | filter=f1 | attribute=Active |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.filters().filter_set(**kwargs)

    def filters_list(self, *args):
        """List the filters.

        CLI command: filters > list

        *Parameters:*
        - `parse`: Parse list output. YES or NO. NO by default.

        *Return:*
        None

        *Examples:*
        | ${filters}= | Filters List | parse=yes |
        | Log List | ${filters} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.filters().filter_list(**kwargs)

    def filters_detail(self, *args):
        """Get detailed information on the filters.

        CLI command: filters > detail

        *Parameters:*
        - `filter`: The filter name, number, or range. Use _all_ to get all filters.

        *Return:*
        Raw output

        *Examples:*
        | ${detail}= | Filters Detail | filter=f1 |
        | Log | ${detail} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.filters().detail(**kwargs)

    def filters_rollovernow(self, *args):
        """Roll over a filter log file.

        CLI command: filters > rollovernow

        *Parameters:*
        - `log_to_roll`: The to to roll over. _All Logs_ for all.

        *Return:*
        None

        *Examples:*
        | Filters Rollovernow | log_to_roll=all |
        | Filters Rollovernow | log_to_roll=f1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.filters().rollovernow(**kwargs)

    def filters_logconfig_edit(self, *args):
        """Configure log subscriptions used by filters.

        CLI command: filters > logconfig > edit

        *Parameters:*
        - `log_to_edit`: The number of the log to edit.
        - `method`: Use index or name:
        | 1 | Download Manually |
        | 2 | FTP Push |
        | 2 | SCP Push |
        - `filename_to_log`: Filename to use for log files.
        - `file_size`: The maximum file size.
        Specify suffixes as: *m* for megabytes, *k* for kilobytes.
        Suffixes are case-insensitive.
        - `file_numbers`: The maximum number of files.
        - `allow_alerts`: Send alert when files are removed due to the maximum number of files allowed. YES or NO.
        - `allow_time_based_rollover`: Configure time-based log files rollover. YES or NO.
        - `rollover_interval`: Configure log rollover settings. Either _Custom time interval_ or _Weekly rollover_.
        - `time_interval`: An interval if `rollover_settings` is _Custom time interval_ is used.
        - `day_of_week`: Choose the day of week to roll over the log files. Used if `rollover_settings` is _Weekly rollover_.
        Use index or name:
        | 1 | Monday |
        | 2 | Tuesday |
        | 3 | Wednesday |
        | 4 | Thursday |
        | 5 | Friday |
        | 6 | Saturday |
        | 7 | Sunday |
        - `time_of_day`: The time of day to rollover log files in 24-hour format (HH:MM).
        Time values is a comma separated list of HH:MM-formatted times.
        Values cannot be duplicated. Hour is in a range 00 to 23, or the wild card "\*".
        Minute is in a range 00 to 59, or the wild card "*".
        - `hostname`: Hostname to deliver the logs.
        - `port`: Port to connect to on the remote host.
        - `user_name`: Username on the remote host.
        - `password`: Password for user.
        - `directory`: Directory on remote host to place logs.
        - `ssh_ver_protocol`: Protocol when `method` is _SCP Push_. Either _SSH1_ or _SSH2_.
        - `enable_key_checking`: Enable host key checking. YES or NO.

        *Return:*
        None

        *Examples:*
        | Filters Logconfig Edit |
        | ... | log_to_edit=${f1} |
        | ... | method=manually |
        | ... | filename_to_log=manual${f1}.mbox |
        | ... | file_size=1000k |
        | ... | file_numbers=15 |
        | ... | allow_alerts=yes |
        | ... | allow_time_based_rollover=yes |
        | ... | rollover_interval=Custom |
        | ... | time_interval=3000 |

        | Filters Logconfig Edit |
        | ... | log_to_edit=${f2} |
        | ... | method=ftp push |
        | ... | hostname=ftp.qa |
        | ... | user_name=user |
        | ... | password=password |
        | ... | directory=/ |
        | ... | filename_to_log=ftp${f2}.mbox |
        | ... | file_size=1m |
        | ... | allow_time_based_rollover=y |
        | ... | rollover_interval=weekly |
        | ... | day_of_week=sunday |
        | ... | time_of_day=12:00 |

        | Filters Logconfig Edit |
        | ... | log_to_edit=${f3} |
        | ... | method=scp push |
        | ... | hostname=scp.qa |
        | ... | port=2222 |
        | ... | user_name=user |
        | ... | directory=/mydir |
        | ... | filename_to_log=scp${f3}.mbox |
        | ... | file_size=200k |
        | ... | allow_time_based_rollover=n |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.filters().logconfig().edit(**kwargs)
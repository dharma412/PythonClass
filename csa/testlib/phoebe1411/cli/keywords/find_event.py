#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/find_event.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class FindEvent(CliKeywordBase):
    """
    CLI command: findevent
    """

    def get_keyword_names(self):
        return ['find_event',]

    def find_event(self, *args):
        """Find event.

        CLI command: findevent

        *Parameters:*
        - `search_type`: Type of search to perform. One from:
        | 1 | Search by envelope FROM |
        | 2 | Search by Message ID |
        | 3 | Search by Subject |
        | 4 | Search by envelope TO |
        - `regex`: The regular expression to search for.
        - `mid`: Select MID from matching message IDs that were found.
        - `log`: The number of the log to use for message tracking.
        - `log_set`: Set of logs to search. One from:
        | 1 | All available log files |
        | 2 | Select log files by date list |
        | 3 | Current log file |
        - `log_files`: Available mail log files, listed by log file start time.
        Specify multiple log files by separating with commas or specify a range with a dash.
        This option appears when `log_set` is _2_.
        - `result_item`: An item to show detailed info if there are multiple results mathed.
        - `as_list`: Return result as list. YES or NO. YES by default.

        *Return:*
        Raw output if `as_list` is NO, otherwise - List.

        *Examples:*
        | ${res}= | Find Event |
        | ... | search_type=4 |
        | ... | regex=${NETWORK} |
        | ... | log=mail_logs |
        | ... | log_set=select |
        | ... | log_files=1 |
        | ... | log=mail_logs |
        | ... | result_item=1 |
        | Log List | ${res} |

        | ${res}= | Find Event | search_type=2 | mid=1 | log=mail_logs | log_set=1 | as_list=no |
        | Log | ${res} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.findevent(**kwargs)
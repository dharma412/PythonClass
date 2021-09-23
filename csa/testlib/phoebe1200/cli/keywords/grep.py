#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/grep.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)
from sal.containers.yesnodefault import NO


class Grep(CliKeywordBase):
    """Keywords for grep CLI command."""

    def get_keyword_names(self):
        return ['grep_logs',
                'grep_logs_batch', ]

    def grep_logs(self, log_name, regex=DEFAULT, insensitive=DEFAULT, file_pattern='*'):
        """ Get information from log files on device.

        *Parameters*
        - `log_name`: name of the log file in 'grep' command promt.
        - `regex`: an extended grep expression. String.
        - `insensitive`: ingnore or not case sensitivities. Yes or No. Default Yes
        - `file_pattern`: Define file selection pattern. Optional. '*' - by default.
        *Return*
        All strings from log file with satisfied provided regular expression.

        *Examples*
        | Grep Logs | authentication | regex=failed | authentication |
        | Grep Logs | gui_logs | regex=agent | insensitive=No |
        | Grep Logs | antispam |
        """
        return self._cli.grep(log_name, regex, insensitive, file_pattern)

    def grep_logs_batch(self,
                        regexp=None,
                        log_name=None,
                        count=NO,
                        count_around=None,
                        file_pattern=None,
                        ignore_case=NO,
                        paginate=NO,
                        tail=NO):
        """ Runs grep in batch mode.
            grep -e <regexp> [options] <log_name>

        *Parameters*
        - `log_name`: name of the log file in 'grep' command prompt.
        - `regexp`: an extended grep expression. String.
        - `count`: The number of lines to count. Not used by default.
        - `count_around`: Provide 'count' lines of context around the grep pattern found. Not used by default.
        - `file_pattern`: Define file selection pattern. Optional. Not used by default.
        - `ignore_case`: Ignore case sensitivities. YES or NO. NO - by default.
        - `paginate`: Paginate the output. YES or NO. NO - by default.
        - `tail`:Run the grep over a tail of the log file.. YES or NO. NO - by default.

        *Return*
        All strings from log file with satisfied provided regular expression.

        *Examples*
        | Grep Logs Batch | failed | authentication |
        | ${out}= | Grep Logs Batch |
        | ... | regexp=User admin entered |
        | ... | log_name=cli_logs |
        | ... | ignore_case=yes |
        | ... | count=yes |
        | Log | ${out} |

        | ${out}= | Grep Logs Batch |
        | ... | regexp=Time offset |
        | ... | log_name=antivirus |
        | ... | count_around=5 |
        | ... | Log | ${out} |
        """
        return self._cli.grep.grep_batch(regexp=regexp,
                                         log_name=log_name,
                                         count=count,
                                         count_around=count_around,
                                         file_pattern=file_pattern,
                                         ignore_case=ignore_case,
                                         paginate=paginate,
                                         tail=tail)

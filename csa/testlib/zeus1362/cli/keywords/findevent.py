#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/findevent.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class Findevent(CliKeywordBase):
    """Find events for appropriate conditions"""

    def get_keyword_names(self):
        return ['findevent',
               ]

    def findevent(self, *args):
        """Find an event from logs

        Parameters:
        - `search_type` : type of search you want to perform
        - `mid` : message ID
        - `regex` : regular expression to search for
        - `log` : number of the log you wish to use
        - `log_set` : set of logs to search
        - `log_files` : available mail log files
        - `result_item` : following matching message IDs were found

        The list of available types of search is following:
        | FROM |
        | TO |
        | ID |
        | Subject |

        The list of available sets of logs is following:
        | All |
        | Select |
        | Current |

        Examples:
        | ${result}= | Findevent | search_type=FROM | regex=auto | log=mail_logs | log_set=All | result_item=1 |
        | ${result}= | Findevent | search_type=ID   | mid=1      | log=mail_logs | log_set=Select | log_files=1 |
        | ${result}= | Findevent | search_type=TO   | regex=auto | log=mail_logs | log_set=All | result_item=1 |
        | ${result}= | Findevent | search_type=Subject | regex=Spam | log=mail_logs | log_set=All | result_item=1 |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.findevent(**kwargs)
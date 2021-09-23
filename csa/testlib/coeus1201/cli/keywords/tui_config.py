
#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/tui_config.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase
from sal.exceptions import ConfigError

class TUIconfig(CliKeywordBase):
    """
        cli -> tuiconfig
    """
    def get_keyword_names(self):
        return [
            'tui_config',
        ]

    def  tui_config(self,
                           mapping_timeout_ad=None,
                           mapping_timeout_edir=None,
                           query_wait_time_ad=None,
                           query_wait_time_edir=None
                           ):
        """
        cli -> tuiconfig

        Parameters:
        - `mapping_timeout_ad`:Configure Mapping Timeout for AD Agent
                               Range 1-300
        - `mapping_timeout_edir`:Configure Mapping Timeout for Novell
                                 eDirectory
                                 Range 1-300
        - `query_wait_time_ad`:Configure Query Wait time for AD Agent
                                Range 1-300
        - `query_wait_time_edir`:Configure Query Wait time for Novell
                                 eDirector
                                 Range 1-300

        Examples:

         |  TUI Config                   |
         |...|  mapping_timeout_ad=200   |
         |...|  mapping_timeout_edir=200 |
         |...|  query_wait_time_ad=200   |
         |...|  query_wait_time_edir=200 |

        """
        if not any([mapping_timeout_ad,mapping_timeout_edir,\
                    query_wait_time_ad,query_wait_time_edir]):
            return
        parameter_string = 'tuiconfig'
        if mapping_timeout_ad:
            mapping_timeout_ad = int(mapping_timeout_ad)
            if not ((mapping_timeout_ad > 0) & (mapping_timeout_ad < 301)):
                raise ValueError, 'mapping_timeout_ad should range between \
                1-300 Given- %d' % mapping_timeout_ad
            parameter_string = parameter_string + ' --mapping_timeout_ad ' + \
            str(mapping_timeout_ad)
        if mapping_timeout_edir:
            mapping_timeout_edir = int(mapping_timeout_edir)
            if not ((mapping_timeout_edir > 0) & (mapping_timeout_edir < 301)):
                raise ValueError, 'mapping_timeout_edir  should range between \
                1-300 Given- %d' % mapping_timeout_edir
            parameter_string = parameter_string + ' --mapping_timeout_edir ' + \
            str(mapping_timeout_edir)
        if query_wait_time_ad:
            query_wait_time_ad = int(query_wait_time_ad)
            if not ((query_wait_time_ad > 0) & (query_wait_time_ad < 301)):
                raise ValueError, 'query_wait_time_ad  should range between \
                1-300 Given- %d' % query_wait_time_ad
            parameter_string = parameter_string + ' --query_wait_time_ad ' + \
            str(query_wait_time_ad)
        if query_wait_time_edir:
            query_wait_time_edir = int(query_wait_time_edir)
            if not ((query_wait_time_edir > 0) & (query_wait_time_edir < 301)):
                raise ValueError, 'query_wait_time_edir  should range between \
                1-300 Given - %d' % query_wait_time_edir
            parameter_string = parameter_string + ' --query_wait_time_edir ' + \
            str(query_wait_time_edir)

        self._cli.tuiconfig()._tui_config(options=parameter_string)

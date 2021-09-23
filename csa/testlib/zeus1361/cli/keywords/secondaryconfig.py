#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/secondaryconfig.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase
from sal.containers.yesnodefault import YES, NO

class Secondaryconfig(CliKeywordBase):
    """Set Enable or Disable secondary aggregation"""

    def get_keyword_names(self):
            return ['secondary_config']

    def secondary_config(self, enable, source_name=None):
        """Set Enable or Disable secondary aggregation

        *Parameters:*
        - `enable`: values YES or NO
        - `source_name`: the data source name to aggregate from

        *Example:*
        | Secondary Config | NO |
        | Secondary Config | YES | resfil |

        """
        kwargs = {
            'enable': enable,
            'source_name': source_name
        }
        self._cli.secondaryconfig().enable(**kwargs)

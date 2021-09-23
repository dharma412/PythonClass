#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/rollback_config.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class rollback_config(CliKeywordBase):
    """
    Keywords for 'rollbackconfig' cli command.
    """

    def get_keyword_names(self):
        return ['rollback_config',
                'rollback_setup', ]

    def rollback_config(self, commmit_item, *args):
        """
        CLI command: rollbackconfig -> rollback
        Rolls back to one of previously committed configurations.

        *Parameters:*
        - `commmit_item`: The number of the config to revert to.
        The 'Commits' table has columns: 'Committed On', 'User', and 'Description'.
        So, you can use any of those columns as a lookup parameter of certain Commit entry.
        The values in the columns are not guaranteed to be unique, so the first match wins.
        Please refer to Examples below.
        - `confirm`: Confirm roll back of the configuration. Either YES or NO. YES by default.
        - `commit`: Commit reverted configuration. Either YES or NO. YES by default.

        *Examples:*
        Roll back by descrption of the Commit.
        | Commit Changes | babar |
        | Rollback Config | babar |

        Roll back by number of the Commit.
        | Commit Changes | babar |
        | Rollback Config | 1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.rollbackconfig().rollback(commmit_item, **kwargs)

    def rollback_setup(self, *args):
        """
        CLI command: rollbackconfig -> setup

        *Parameters:*
        - `enable`: whether to enable Rollback Config or not.
           Either 'yes' or 'no'. Default is 'no'.
        - `disable`: whether to disable Rollback Config or not.
           Either 'yes' or 'no'. Default is 'no'.

        *Examples:*
        | Rollback Setup | disable=no |
        | Rollback Setup | disable=yes |
        | Rollback Setup | enable=no |
        | Rollback Setup | enable=yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.rollbackconfig().setup(**kwargs)

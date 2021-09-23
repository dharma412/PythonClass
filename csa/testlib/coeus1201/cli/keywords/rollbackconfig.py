#!/usr/bin/env python
# Id: $

from common.cli.clicommon import CliKeywordBase
from common.util.misc import Misc

class RollBackConfig(CliKeywordBase):

    def get_keyword_names(self):
        return [
            'get_rollback_status',
            'set_rollback_status',
            'roll_back_to_config',
        ]

    def get_rollback_status(self):
        return self._cli.rollbackconfig.get_rollback_status()


    def set_rollback_status(self, status, desc):
        return self._cli.rollbackconfig.set_rollback_status(status, desc)


    def roll_back_to_config(self, desc, commit_desc):
        self._cli.rollbackconfig(desc, commit_desc)

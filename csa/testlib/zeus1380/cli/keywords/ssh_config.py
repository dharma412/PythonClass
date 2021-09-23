#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/ssh_config.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)

class SshConfig(CliKeywordBase):

    """Keywords for sshconfig CLI command."""

    def get_keyword_names(self):
        return ['sshconfig_new',
                'sshconfig_delete',
                'sshconfig_user',
                'sshconfig_get_key'
                ]

    def sshconfig_new(self, ssh_key):
        """ Add new ssh key for current user's ssh file.

        *Parameters*
        - `ssh_key`: string wich represented ssh key.

        *Example*
        | Sshconfig New |
        | ... | ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAIEAoPWj3H7paui4u6jda9/qPY7O8RviJV2RS3KOY/kEDuecaz5b79ceVUGUao/pMw9ZKM6IM4dU8CPNJOrzch7Gx8I/jY1tsS65zdDJMr89q= esafronov@pan.iron |
        """
        self._cli.sshconfig().new(ssh_key)

    def sshconfig_delete(self, keynumber):
        """ Delete ssh key from current user's ssh file.

        *Parameters*
        - `keynumber`: number wich represented ssh key.

        *Examples*
        | Sshconfig Delete | 1 |
        | Sshconfig Delete | 2 |
        """
        self._cli.sshconfig().delete(keynumber)

    def sshconfig_get_key(self, keynumber):
        """ Return ssh key.

        *Parameters*
        - `keynumber`: number which represent ssh key.

        *Examples*
        | Sshconfig Get Key | 1 |
        | Sshconfig Get Key | 2 |
        """
        return self._cli.sshconfig().print_key(keynumber)

    def sshconfig_user(self, username):
        """ Switch to `username` ssh config file.

        *Parameters*
        - `username`: user to which ssh config file switch.

        *Examples*
        | Sshconfig User | admin |
        | Sshconfig User | some_other_user |
        """
        self._cli.sshconfig().user(username)

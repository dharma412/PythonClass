#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/ssh_config.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)

class SshConfig(CliKeywordBase):

    """Keywords for sshconfig CLI command."""

    def get_keyword_names(self):
        return ['sshconfig_new',
                'sshconfig_delete',
                'sshconfig_user',
                'sshconfig_get_key',
                'sshconfig_edit_settings',
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

    def sshconfig_edit_settings(self, incomplete_ssh_session_timeout,
                         min_server_key_size,
                         pubkey_algorithms,
                         kex_algorithms,
                         cipher_algorithms,
                         unsuccessfull_ssh_session_timeout,
                         mac_methods):
        """ Edit SSH server settings.

        *Parameters*:
        - `incomplete_ssh_session_timeout`: Incomplete SSH session timeout (in secs).
                                 [60]
        - `min_server_key_size`: Minimum Server Key Size. By Default the value is 1024
        - `pubkey_algorithms`: Public Key Authentication Algorithms.
                               [rsa1,ssh-dss,ssh-rsa]
        - `kex_lgorithms`: KEX Algorithms
                               [diffie-hellman-group-exchange-sha256,
                               diffie-hellman-group-exchange-sha1,
                               diffie-hellman-group14-sha1,diffie-hellman-group1-sha1]
        - `cipher_algorithms`: Cipher Algorithms.
                               [aes128-ctr,aes192-ctr,aes256-ctr,
                               arcfour256,arcfour128,aes128-cbc,
                               3des-cbc,blowfish-cbc,cast128-cbc,
                               aes192-cbc,aes256-cbc,arcfour,
                               rijndael-cbc@lysator.liu.se]
        - `unsuccessfull_ssh_session_timeout`: Unsuccessful SSH login attempts allowed.
                                 [3]
        - `mac_methods`: MAC Methods.
                               [hmac-md5,hmac-sha1,umac-64@openssh.com,hmac-ripemd160,hmac-ripemd160@openssh.com,hmac-sha1-96,hmac-md5-96]


        *Examples*:
        |   Sshconfig Edit Settings |
        |    ... | 60 | 1024 | ssh-dss | diffie-hellman-group14-sha1 | aes256-cbc |
        |    ... | 3 | hmac-sha1 |

        """
        return self._cli.sshconfig().sshd_edit_settings(incomplete_ssh_session_timeout=incomplete_ssh_session_timeout,
                                               min_server_key_size=min_server_key_size,
                                               pubkey_algorithms=pubkey_algorithms,
                                               kex_algorithms=kex_algorithms,
                                               cipher_algorithms=cipher_algorithms,
                                               unsuccessfull_ssh_session_timeout=unsuccessfull_ssh_session_timeout,
                                               mac_methods=mac_methods)

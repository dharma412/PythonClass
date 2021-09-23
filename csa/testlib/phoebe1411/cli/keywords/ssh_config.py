#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/ssh_config.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)

class SshConfig(CliKeywordBase):

    """Keywords for sshconfig CLI command."""

    def get_keyword_names(self):
        return ['sshconfig_new',
                'sshconfig_delete',
                'sshconfig_print',
                'sshconfig_user_new',
                'sshconfig_user_delete',
                'sshconfig_user_print',
                'sshconfig_edit_ssh_settings',]

    def sshconfig_new(self, ssh_key):
        """ Add new ssh key for current user's ssh file.

        *Parameters*:
        - `ssh_key`: string which represented ssh key.

        *Example*:
        | Sshconfig New |
        | ... | ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAIEAoPWj3H7paui4u6jda9/qPY7O8RviJV2RS3KOY/kEDuecaz5b79ceVUGUao/pMw9ZKM6IM4dU8CPNJOrzch7Gx8I/jY1tsS65zdDJMr89q= esafronov@pan.iron |
        """
        self._cli.sshconfig().new(ssh_key)

    def sshconfig_delete(self, keynumber):
        """ Delete ssh key from current user's ssh file.

        *Parameters*:
        - `keynumber`: number which represented ssh key.

        *Examples*:
        | Sshconfig Delete | 1 |
        | Sshconfig Delete | 2 |
        """
        self._cli.sshconfig().delete(keynumber)

    def sshconfig_print(self, keynumber):
        """ Return ssh key.

        *Parameters*:
        - `keynumber`: number which represent ssh key.

        *Examples*:
        | Sshconfig Print | 1 |
        | Sshconfig Print | 2 |

        *Return*:
        Raw ssh key. String.
        """
        return self._cli.sshconfig().print_key(keynumber)

    def sshconfig_user_new(self, username, ssh_key):
        """ Add new key to `username` ssh config file.

        *Parameters*:
        - `username`: user to which ssh config file key should be added.
        - `ssh_key`: key to be added.

        *Examples*:
        | ${output}= | OperatingSystem.Run | cd ${SUITE_TMP_DIR}; ssh-keygen -t rsa -f ${key_name} -C ${comment} -N "" -q |
        | ${rsa_pub}= | OperatingSystem.Get File | ${SUITE_TMP_DIR}/${key_name}.pub |
        | Sshconfig User New | admin | ${rsa_pub} |
        | Sshconfig User New | some_other_user | ${rsa_pub} |
        """
        self._cli.sshconfig().user_new(username, ssh_key=ssh_key)

    def sshconfig_user_delete(self, username, ssh_key):
        """ Delete key from `username` ssh config file.

        *Parameters*:
        - `username`: user from which ssh config file ssh_key should be deleted.
        - `ssh_key`: number which represents the key.

        *Examples*:
        | Sshconfig User Delete | admin | 1 |
        | Sshconfig User Delete | some_other_user | 2 |
        """
        self._cli.sshconfig().user_delete(username, ssh_key=ssh_key)

    def sshconfig_user_print(self, username, key_number):
        """ Print keys from `username` ssh config file.

        *Parameters*:
        - `username`: user from which ssh config file print keys.

        *Examples*:
        | Sshconfig User Print | admin | 1 |
        | Sshconfig User Print | some_other_user | 2 |

        *Return*:
        Raw ssh key. String.
        """
        return self._cli.sshconfig().user_print(username, key_number)

    def sshconfig_edit_ssh_settings(self, pubkey_algorithms, cipher_algorithms, mac_methods, min_server_key_size, kex_algorithms, fips_mode=False):
        """ Edit SSH server settings.

        *Parameters*:
        - `pubkey_algorithms`: Public Key Authentication Algorithms.
                               [rsa1,ssh-dss,ssh-rsa]
        - `cipher_algorithms`: Cipher Algorithms.
                               [aes128-ctr,aes192-ctr,aes256-ctr,
                               arcfour256,arcfour128,aes128-cbc,
                               3des-cbc,blowfish-cbc,cast128-cbc,
                               aes192-cbc,aes256-cbc,arcfour,
                               rijndael-cbc@lysator.liu.se]
        - `mac_methods`: MAC Methods.
                               [hmac-md5,hmac-sha1,umac-64@openssh.com,hmac-ripemd160,hmac-ripemd160@openssh.com,hmac-sha1-96,hmac-md5-96]
        - `min_server_key_size`: Minimum Server Key Size. By Default the value is 1024
        - `kex_lgorithms`: KEX Algorithms
                               [diffie-hellman-group-exchange-sha256,
                               diffie-hellman-group-exchange-sha1,
                               diffie-hellman-group14-sha1,diffie-hellman-group1-sha1]
        - `fips_mode`: False if FIPS mode is disabled ( default value ), True if FIPS mode is enabled.

        *Examples*:
        |   Sshconfig Edit Ssh Settings |
        |    ... | ssh-dss | aes256-cbc |
        |    ... | aes256-cbc | 2048 |
        |    ... | diffie-hellman-group14-sha1 | ${True} |

        """
        self._cli.sshconfig().sshd_edit_settings(pubkey_algorithms=pubkey_algorithms,
                                               cipher_algorithms=cipher_algorithms,
                                               mac_methods=mac_methods,
                                               min_server_key_size=min_server_key_size,
                                               kex_algorithms=kex_algorithms,
                                               fips_mode=fips_mode)

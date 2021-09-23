#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/ssh_config.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase
from common.cli import cliexceptions
DEFAULT = ''

class SshConfig(CliKeywordBase):
    """Configure user SSH keys for passwordless access."""

    def get_keyword_names(self):
        return [
            'ssh_config_new',
            'ssh_config_delete',
            'ssh_config_user',
            'ssh_config_print_key',
            'ssh_config_print_keys',
            'ssh_config_print_users',
            'ssh_config_user_new',
            'ssh_config_edit_ssh_settings',
        ]

    def ssh_config_new(self, key):
        """Add a new key.

        sshconfig > new

        Parameters:
        - `key`: public SSH key for authorization.

        Example:
        | ${key}= | ssh-rsa AAAAB3Nz...5zdDJMr89q=test@test.qa |
        | Ssh Config New | ${key} |
        """

        self._cli.sshconfig().new(key)

    def ssh_config_delete(self, key_num):
        """Remove a key.

        sshconfig > delete

        Parameters:
        - `key_num`: number of the key you wish to delete. (Numeration starts
        from 1. Valid key numbers can be obtained via keyword Ssh Config Print
        Keys).

        Example:
        | Ssh Config Delete | 1 |
        """

        self._cli.sshconfig().delete(key_num)

    def ssh_config_print_key(self, key_num):
        """Display a key.

        sshconfig > print

        Parameters:
        - `key_num`: number of the key you wish to display. (Numeration starts
        from 1. Valid key numbers can be obtained via keyword Ssh Config
        Print Keys).

        Example:
        | ${result}= | Ssh Config Print Key | 1 |
        | Log | ${result} |
        """

        output = self._cli.sshconfig().print_key(key_num)
        return output

    def ssh_config_print_keys(self):
        """Display keys.

        Example:
        | ${result}= | Ssh Config Print Keys |
        | Log | ${result} |
        """

        output = self._cli.sshconfig().print_keys()
        return output

    def ssh_config_print_users(self):
        """Display registered users.

        Example:
        | ${result}= | Ssh Config Print Users |
        | Log | ${result} |
        """

        output = self._cli.sshconfig().print_users()
        return output

    def ssh_config_user(self, user=''):
        """Switch to a different user to edit.

        sshconfig > user

        Parameters:
        - `user`: number or username of the user whose SSH keys you want to
        edit. Default: 1 (admin). (Numbers start from 1. Valid usernames and
        numbers can be obtained via keyword Ssh Config Print Users).

        Example:
        | Ssh Config User | 1 |
        """

        self._cli.sshconfig().user(user)

    def ssh_config_user_new(self, username, ssh_key):
        """ Add new key to `username` ssh config file.

        *Parameters*:
        - `username`: user to which ssh config file key should be added.
        - `ssh_key`: key to be added.

        *Examples*:
        | ${output}= | OperatingSystem.Run | cd ${SUITE_TMP_DIR}; ssh-keygen -t rsa -f ${key_name} -C ${comment} -N "" -q |
        | ${rsa_pub}= | OperatingSystem.Get File | ${SUITE_TMP_DIR}/${key_name}.pub |
        | Ssh Config User New | admin | ${rsa_pub} |
        | Ssh Config User New | some_other_user | ${rsa_pub} |
        """
        self._cli.sshconfig().user_new(username, ssh_key=ssh_key)

    def ssh_config_edit_ssh_settings(self, pubkey_algorithms=DEFAULT, cipher_algorithms=DEFAULT, mac_methods=DEFAULT, min_server_key_size=2048, kex_algorithms=DEFAULT, fips_mode=False, incomplete_ssh_session_timeout=DEFAULT, unsuccessfull_ssh_session_timeout=DEFAULT):
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
                        [hmac-md5,hmac-sha1,umac-64@openssh.com,hmac-ripemd160,
            hmac-ripemd160@openssh.com,hmac-sha1-96,hmac-md5-96]
        - `min_server_key_size`: Minimum Server Key Size. By Default the value is 1024
        - `kex_lgorithms`: KEX Algorithms
                               [diffie-hellman-group-exchange-sha256,
                               diffie-hellman-group-exchange-sha1,
                               diffie-hellman-group14-sha1,diffie-hellman-group1-sha1]
        - `fips_mode`: False if FIPS mode is disabled ( default value ), True if FIPS mode is enabled.
        - `incomplete_ssh_session_timeout`: Incomplete ssh session timeout value.
        - `unsuccessfull_ssh_session_timeout`: Unsuccessfull ssh session timeout value.

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
                                               fips_mode=fips_mode,
                                               incomplete_ssh_session_timeout=incomplete_ssh_session_timeout,
                                               unsuccessfull_ssh_session_timeout=unsuccessfull_ssh_session_timeout,)

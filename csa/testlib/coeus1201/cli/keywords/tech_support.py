#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/tech_support.py#1 $

from common.cli.clicommon import CliKeywordBase
from common.cli import cliexceptions

class TechSupport(CliKeywordBase):
    """Enable or disable remote service access to your system by a
    Cisco IronPort customer service representative, either using ssh access
    or setting up a secure tunnel.
    """

    def get_keyword_names(self):
        return ['tech_support_ssh_access',
                'tech_support_disable',
                'tech_support_status',
                'tech_support_tunnel',
                ]

    def tech_support_ssh_access(self, tmp_password, confirm='yes'):
        """Allow an Cisco IronPort customer service representative to remotely
        access your system, without establishing a tunnel.

        techsupport > sshaccess

        Parameters:
        - `tmp_password`: temporary password for customer support to use. This
        password will not be able to be used to directly access your system.
        - `confirm`: confirmation question answer. Either 'yes' or 'no'. Default
        value 'yes'.

        NOTE:
        * the password must be between 6 and 128 characters long;
        * it cannot be blank or consist only of spaces;
        * it must be different from the administrator's password.

        Examples:
        | Tech Support SSH Access | qwerty |

        | Tech Support SSH Access | qwerty | confirm=yes |
        """

        self._cli.techsupport().sshaccess(tmp_password,
                                          self._process_yes_no(confirm))

    def tech_support_status(self):
        """Display the current techsupport status.

        techsupport > status

        Example:
        | ${res}= | Tech Support Status |
        | Log | ${res} |
        """

        output = self._cli.techsupport().status()
        return output

    def tech_support_disable(self, confirm='yes'):
        """Prevent Cisco IronPort customer service representatives from remotely
        accessing your system.

        techsupport > disable

        Parameters:
        - `confirm`: confirmation question answer. Either 'yes' or 'no'. Default
        value 'yes'.

        Examples:
        | Tech Support Disable |

        | Tech Support Disable | confirm=yes |
        """

        self._cli.techsupport().disable(self._process_yes_no(confirm))

    def tech_support_tunnel(self, tmp_password, port_num='443', delay='5'):
        """Allow an Cisco IronPort customer service representative to remotely
        access your system, and establish a secure tunnel for communication.

        techsupport > tunnel

        Parameters:
        - `tmp_password`: temporary password for customer support to use. This
        password will not be able to be used to directly access your system.
        - `port_num`: port number for tunnel connection. Number from 1 to 65535.
        Default value '443'.
        - `delay`: time in seconds to wait for ssh tunnel to connect. Default
        value '5'.

        NOTE:
        * the password must be between 6 and 128 characters long;
        * it cannot be blank or consist only of spaces;
        * it must be different from the administrator's password.

        Examples:
        | Tech Support Tunnel | qwerty |

        | Tech Support Tunnel | qwerty | port_num=555 | delay=15 |
        """

        if not port_num.isdigit():
            raise cliexceptions.ConfigError(
                    'port_num must be a number from 1 to 65535')
        if not delay.isdigit():
            raise cliexceptions.ConfigError('delay must be a number.')

        self._cli.techsupport().tunnel(tmp_password, port_num, int(delay))


#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/address_config.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase
from sal.containers.yesnodefault import YES, NO, DEFAULT, is_yes

class AddressConfig(CliKeywordBase):
    """Allow the configuration of system generated email messages."""

    def get_keyword_names(self):
        return ['address_config_bouncefrom',
                'address_config_reportsfrom',
                'address_config_otherfrom']

    def address_config_bouncefrom(self,
                                  display_name=DEFAULT,
                                  user_name=DEFAULT,
                                  use_hostname='yes',
                                  domain_name=DEFAULT):

        """Edit the bounce from address.

        addressconfig > bouncefrom

        Parameters:
        - `display_name`: display name portion of the "bounce from" address.
        - `user_name`: user name portion of the "bounce from" address.
        - `use_hostname`: Either Yes or No value to use the system hostname for
          the domain portion.
        - `domain_name`: domain name portion of the "bounce from" address.

        Examples:
        | Address Config Bouncefrom | user_name=new_name |

        | Address Config Bouncefrom | display_name=admin |
        | ... | user_name=user |
        | ... | use_hostname='no' |
        | ... | domain_name=somedomain |
        """

        use_hostname = self._process_yes_no(use_hostname)

        input_dict = {
            'display_name': display_name,
            'user_name': user_name,
            'use_hostname': use_hostname,
        }

        if is_yes(use_hostname):
            input_dict.update({'domain_name': domain_name})

        self._cli.addressconfig().bouncefrom(input_dict)

    def address_config_reportsfrom(self,
                                   display_name=DEFAULT,
                                   user_name=DEFAULT,
                                   use_hostname='yes',
                                   domain_name=DEFAULT):

        """Edit the reports from address.

        addressconfig > reportsfrom

        Parameters:
        - `display_name`: display name portion of the "reports from" address.
        - `user_name`: user name portion of the "reports from" address.
        - `use_hostname`: Either Yes or No value to use the system hostname for
          the domain portion.
        - `domain_name`: domain name portion of the "reports from" address.

        Examples:
        | Address Config Reportsfrom | user_name=new_name |

        | Address Config Reportsfrom | display_name=admin |
        | ... | user_name=user |
        | ... | use_hostname='no' |
        | ... | domain_name=somedomain |
        """

        use_hostname = self._process_yes_no(use_hostname)

        input_dict = {
            'display_name': display_name,
            'user_name': user_name,
            'use_hostname': use_hostname,
        }

        if is_yes(use_hostname):
            input_dict.update({'domain_name': domain_name})

        self._cli.addressconfig().reportsfrom(input_dict)


    def address_config_otherfrom(self,
                                  display_name=DEFAULT,
                                  user_name=DEFAULT,
                                  use_hostname='yes',
                                  domain_name=DEFAULT):

        """Edit the all other messages from address.

        addressconfig > otherfrom

        Parameters:
        - `display_name`: display name portion of the "other from" address.
        - `user_name`: user name portion of the "other from" address.
        - `use_hostname`: Either Yes or No value to use the system hostname for
          the domain portion.
        - `domain_name`: domain name portion of the "other from" address.

        Examples:
        | Address Config Otherfrom | user_name=new_name |

        | Address Config Otherfrom | display_name=admin |
        | ... | user_name=user |
        | ... | use_hostname='no' |
        | ... | domain_name=somedomain |
        """

        use_hostname = self._process_yes_no(use_hostname)

        input_dict = {
            'display_name': display_name,
            'user_name': user_name,
            'use_hostname': use_hostname,
        }

        if is_yes(use_hostname):
            input_dict.update({'domain_name': domain_name})

        self._cli.addressconfig().otherfrom(input_dict)


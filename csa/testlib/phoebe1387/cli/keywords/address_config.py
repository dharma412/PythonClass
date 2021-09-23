#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/address_config.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class AddressConfig(CliKeywordBase):
    """
    addressconfig

    Allow the configuration of system generated email messages.
    """

    def get_keyword_names(self):
        return ['address_config_avfrom',
                'address_config_bouncefrom',
                'address_config_notifyfrom',
                'address_config_quarantinefrom',
                'address_config_dmarcfrom',
                'address_config_otherfrom'
                ]

    def _edit_addressconfig(self, operation, *args):
        kwargs = self._convert_to_dict(args)
        self._cli.addressconfig().addressconfig_edit(oper=operation, **kwargs)

    def address_config_avfrom(self, *args):
        """
        Edit the anti-virus from address

        addressconfig -> avfrom

        *Parameters*:
        - `display_name` : display name portion of the "anti-virus from" address
        - `user_name` : user name portion of the "anti-virus from" address
        - `use_hostname` : use the system hostname for the domain portion?
                           Either 'yes' or 'no'
        - `domain_name` : enter the domain name portion of the "anti-virus from"
                           address

        *Examples*:

        | Address Config avfrom | display_name=testname |
        | Address Config avfrom | use_hostname=no | domain_name=testdomain.com |

        """
        self._edit_addressconfig('AVFROM', *args)

    def address_config_bouncefrom(self, *args):
        """
        Edit the bounce from address

        addressconfig -> bouncefrom

        *Parameters*:
        - `display_name` : display name portion of the "bounce from" address
        - `user_name` : user name portion of the "bounce from" address
        - `use_hostname` : use the system hostname for the domain portion?
                           Either 'yes' or 'no'
        - `domain_name` : enter the domain name portion of the "bounce from"
                           address

        *Examples*:

        | Address Config bouncefrom | display_name=testname |
        | Address Config bouncefrom | use_hostname=no | domain_name=testdomain.com |

        """
        self._edit_addressconfig('BOUNCEFROM', *args)

    def address_config_notifyfrom(self, *args):
        """
        Edit the notify from address

        addressconfig -> notifyfrom

        *Parameters*:
        - `display_name` : display name portion of the "notify from" address
        - `user_name` : user name portion of the "notify from" address
        - `use_hostname` : use the system hostname for the domain portion?
                           Either 'yes' or 'no'
        - `domain_name` : enter the domain name portion of the "notify from"
                           address

        *Examples*:

        | Address Config notifyfrom | display_name=testname |
        | Address Config notifyfrom | use_hostname=no | domain_name=testdomain.com |

        """
        self._edit_addressconfig('NOTIFYFROM', *args)


    def address_config_quarantinefrom(self, *args):
        """
        Edit the quarantine bcc from address

        addressconfig -> quarantinefrom

        *Parameters*:
        - `display_name` : display name portion of the "quarantine from" address
        - `user_name` : user name portion of the "quarantine from" address
        - `use_hostname` : use the system hostname for the domain portion?
                           Either 'yes' or 'no'
        - `domain_name` : enter the domain name portion of the "quarantine from"
                           address

        *Examples*:

        | Address Config quarantinefrom | display_name=testname |
        | Address Config quarantinefrom | use_hostname=no | domain_name=testdomain.com |

        """
        self._edit_addressconfig('QUARANTINEFROM', *args)

    def address_config_dmarcfrom(self, *args):
        """
        Edit the DMARC reports from address

        addressconfig -> dmarcfrom

        *Parameters*:
        - `display_name` : display name portion of the "DMARC reports from" address
        - `user_name` : user name portion of the "DMARC reports from" address
        - `use_hostname` : use the system hostname for the domain portion?
                           Either 'yes' or 'no'
        - `domain_name` : enter the domain name portion of the "DMARC reports from"
                           address

        *Examples*:

        | Address Config dmarcfrom | display_name=testname |
        | Address Config dmarcfrom | use_hostname=no | domain_name=testdomain.com |

        """
        self._edit_addressconfig('DMARCFROM', *args)


    def address_config_otherfrom(self, *args):
        """
        Edit the all other messages from address

        addressconfig -> otherfrom

        *Parameters*:
        - `display_name` : display name portion of all other messages from address
        - `user_name` : user name portion of all other messages from address
        - `use_hostname` : use the system hostname for the domain portion?
                           Either 'yes' or 'no'
        - `domain_name` : enter the domain name portion of all other messages from
                           address

        *Examples*:

        | Address Config otherfrom | display_name=testname |
        | Address Config otherfrom | use_hostname=no | domain_name=testdomain.com |

        """
        self._edit_addressconfig('OTHERFROM', *args)

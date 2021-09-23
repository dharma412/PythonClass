#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/addresslist_config.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class AddressListConfig(CliKeywordBase):
    """
    addresslistconfig

    addresslistconfig new <name> --descr=<description> --addresses=<address1,address2,...>
    addresslistconfig edit <name> --name=<new-name> --descr=<description> --addresses=<address1,address2,...>
    addresslistconfig delete <name>
    addresslistconfig print <name>
    addresslistconfig conflicts <name>

    Configure address lists.

    new - Create a new address list.
    edit - Edit an existing address list.
    delete - Delete an address list.
    print - Print the details of an address list.
    conflicts - Find conflicting addresses within an address list.

    name - An indentifier for the list.
    new-name - A identifier to rename the list, can be same as existing
               identifier.
    description - A description of the list.
    address - A partial or complete email address.


    """

    def get_keyword_names(self):
        return ['addresslist_config_new',
                'addresslist_config_edit',
                'addresslist_config_delete',
                'addresslist_config_print',
                'addresslist_config_conflicts'
                ]

    def addresslist_config_new(self, *args):
        """
        Create a new address list

        addresslistconfig -> new

        *Parameters*:
        - `list_name` : Enter a name for the address list, REQUIRED FIELD
        - `list_desc` : Enter a description for the address list
        - `addr_list` : Enter a comma separated list of addresses

        *Examples*:

        | AddressList Config new | list_name=testlist |
        | AddressList Config new | list_name=testlist | addr_list=user@,@test.com |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.addresslistconfig().new(**kwargs)

    def addresslist_config_edit(self, *args):
        """
        Edit the address list

        addresslistconfig -> edit

        *Parameters*:
        - `list_name` : Enter a name for the address list, REQUIRED FIELD
        - `new_list_name` : new name for the address list
        - `list_desc` : Enter a description for the address list
        - `addr_list` : Enter a comma separated list of addresses

        *Examples*:

        | AddressList Config edit | list_name=testlist | new_list_name=testlist1 |
        | AddressList Config edit | list_name=testlist | addr_list=user@,@test.com |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.addresslistconfig().edit(**kwargs)

    def addresslist_config_print(self, *args):
        """
        Print the address list

        addresslistconfig -> Print

        *Parameters*:
        - `list_name` : Enter a name for the address list

        *Return*:
        Details of the addresslist like name,description,addresslists

        *Examples*:

        | details= | AddressList Config Print | list_name=testlist |

        """
        kwargs = self._convert_to_dict(args)
        return self._cli.addresslistconfig().Print(**kwargs)

    def addresslist_config_delete(self, *args):
        """
        Delete the address list

        addresslistconfig -> Delete

        *Parameters*:
        - `list_name` : Enter a name for the address list. Required


        *Examples*:

        | AddressList Config Delete | list_name=testlist |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.addresslistconfig().delete(**kwargs)

    def addresslist_config_conflicts(self, *args):
        """
        Returns conflicts of  the address list

        addresslistconfig -> conflicts

        *Parameters*:
        - `list_name` : Enter a name for the address list. Required

        *Return*:
        Details of the conflicts


        *Examples*:

        | AddressList Config conflicts | list_name=testlist |

        """
        kwargs = self._convert_to_dict(args)
        return self._cli.addresslistconfig().conflicts(**kwargs)

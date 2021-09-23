#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/altsrchost.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class Altsrchost(CliKeywordBase):
    """
    altsrchost new <source_address> <interface>
    altsrchost edit <source_address> <new_source_address> <new_interface>
    altsrchost delete <source_address>
    altsrchost print
    altsrchost export <filename>
    altsrchost import <filename>
    altsrchost clear

    The altsrchost command sets up Virtual Gateways(tm).  Each Virtual
    Gateway(tm) sends email over a different IP interface.  The routing
    is done based on either the envelope sender address, or the IP address
    of the sending host.

    source_address - The envelope sender address, or the IP address of the
                     sending host.
    interface - The interface name (or IP address) or IP group, to use for
                outgoing mail.
    filename - The filename for import/export.

    """

    def get_keyword_names(self):
        return ['altsrchost_new',
                'altsrchost_edit',
                'altsrchost_delete',
                'altsrchost_print',
                'altsrchost_clear',
                'altsrchost_import',
                'altsrchost_export'
                ]

    def altsrchost_new(self, *args):
        """
        Create a new altsrchost

        altsrchost -> new

        *Parameters*:
        - `address` : Enter address(es) for. REQUIRED
        - `interface` : name of the interface.

        *Examples*:

        | Altsrchost new | address=address@ua.com | interface=Management |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.altsrchost().new(**kwargs)

    def altsrchost_edit(self, *args):
        """
        Edit the altsrchost

        altsrchost -> edit

        *Parameters*:
        - `address_to_edit``: Enter the address to edit
        - `address` : Enter address(es) for. REQUIRED
        - `interface` : name of the interface.

        *Examples*:

        | Altsrchost edit | address_to_edit=address@ua.com | address=addressnew@uq.com | interface=Management |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.altsrchost().edit(**kwargs)

    def altsrchost_print(self):
        """
        Print the altsrchosts

        altsrchost -> Print

        *Parameters*:
        None

        *Return*:
        Details of the altsrchosts

        *Examples*:

        | ${details}= | Altsrchost Print |

        """
        return self._cli.altsrchost().print_mappings()

    def altsrchost_delete(self, *args):
        """
        Delete the altsrchost

        altsrchost -> Delete

        *Parameters*:
        - `address` : Enter address(es) for. REQUIRED
        - `confirmation` : Either yes or no


        *Examples*:

        | Altsrchost Delete | address=addressnew@ |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.altsrchost().delete(**kwargs)

    def altsrchost_clear(self):
        """
        Clear the altsrchosts

        altsrchost -> clear

        *Parameters*:
        None

        *Examples*:

        | Altsrchost clear |

        """
        self._cli.altsrchost().clear()

    def altsrchost_import(self, *args):
        """
        Import the altsrchosts

        altsrchost -> import

        *Parameters*:
        - `import_file` : Name of the file to import into.REQUIRED

        *Examples*:

        | Altsrchost import | import_file=testimport |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.altsrchost().import_mappings(**kwargs)

    def altsrchost_export(self, *args):
        """
        Export the altsrchosts

        altsrchost -> export

        *Parameters*:
        - `export_file` : Name of the file to export into.REQUIRED

        *Examples*:

        | Altsrchost export | export_file=testexport |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.altsrchost().export_mappings(**kwargs)

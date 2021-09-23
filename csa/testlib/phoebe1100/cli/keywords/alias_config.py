#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/alias_config.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class Aliasconfig(CliKeywordBase):
    """
    aliasconfig
    aliasconfig new <domain> <alias> <email_address> [email_address] [...]
    aliasconfig edit <domain> <alias> <email_address> [email_address] [...]
    aliasconfig delete <domain> <alias>
    aliasconfig print
    aliasconfig import <filename>
    aliasconfig export <filename>
    aliasconfig clear

    Configure the alias table.

    <domain> - The domain context in which an alias is applied.
               "global" specifies the Global Domain Context.

    <alias> - The name of the alias to configure.

        Allowed aliases at the Global Domain Context:
            - "user@domain" - This email address.
            - "user" - This user for any domain.
            - "@domain" - All users in this domain.
            - "@.partialdomain" - All users in this domain, or any of its
                                  sub domains.

        Allowed aliases for specific domain contexts:
            - "user" - This user in this domain context.
            - "user@domain" - This email address.

    <email_address> - The email address that aliases map to.  A single
                      alias can map to multiple email addresses.

    <filename> - The filename to use with importing and exporting the
                 alias table.

    Note: using "aliasconfig new <domain>" with a non-existant domain
    will cause that domain to be created.


    """

    def get_keyword_names(self):
        return ['alias_config_new',
                'alias_config_edit',
                'alias_config_delete',
                'alias_config_print',
                'alias_config_clear',
                'alias_config_import',
                'alias_config_export'
                ]

    def alias_config_new(self, *args):
        """
        Create a new alias config

        aliasconfig -> new

        *Parameters*:
        - `aliases_apply` : How do you want your aliases to apply.Choose from table:
        | 1 | Globally |
        | 2 | Add a new domain context |
        Default is 1
        - `aliases` : Enter the alias(es) to match on. REQUIRED
        - `address` : Enter address(es) for. REQUIRED
        - `another_alias` : Do you want to add another alias. Either yes or no
        - `domain_context`: Enter new domain context. REQUIRED

        *Examples*:

        | AliasConfig new | aliases_apply=2 | domain_context=somedomain.context | address=address@ua.com | aliases=somealiases |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.aliasconfig().new(**kwargs)

    def alias_config_edit(self, *args):
        """
        Edit the alias config

        aliasconfig -> edit

        *Parameters*:
        - `domain_context`: Enter new domain context.
        - `aliases` : Enter the alias(es) to match on.
        - `address` : Enter address(es) for. REQUIRED

        *Examples*:

        | AliasConfig edit |  alias=somealiases | address=address1@uq.com |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.aliasconfig().edit(**kwargs)

    def alias_config_print(self):
        """
        Print the aliases

        aliasconfig -> Print

        *Parameters*:
        None

        *Return*:
        Details of the aliases

        *Examples*:

        | ${details}= | AliasConfig Print |

        """
        return self._cli.aliasconfig().print_aliases()

    def alias_config_delete(self, *args):
        """
        Delete the address list

        aliasconfig -> Delete

        *Parameters*:
        - `domain` : Enter a name of the domain
        - `alias` : Enter the name of the alias . REQUIRED


        *Examples*:

        | AliasConfig Delete | alias=testalias |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.aliasconfig().delete(**kwargs)

    def alias_config_clear(self, *args):
        """
        Clear the aliases

        aliasconfig -> clear

        *Parameters*:
        None

        *Examples*:

        | AliasConfig clear |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.aliasconfig().clear(**kwargs)

    def alias_config_import(self, *args):
        """
        Import the aliases

        aliasconfig -> import

        *Parameters*:
        - `import_file` : Name of the file to import into.REQUIRED

        *Examples*:

        | AliasConfig import | import_file=testimport |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.aliasconfig().import_aliases(**kwargs)

    def alias_config_export(self, *args):
        """
        Export the aliases

        aliasconfig -> export

        *Parameters*:
        - `export_file` : Name of the file to export into.REQUIRED

        *Examples*:

        | AliasConfig export | export_file=testexport |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.aliasconfig().export_aliases(**kwargs)

#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/exception_config.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class ExceptionConfig(CliKeywordBase):
    """Configure domain exception table."""

    def get_keyword_names(self):
        return ['exception_config_new',
                'exception_config_edit',
                'exception_config_delete',
                'exception_config_move',
                'exception_config_print',
                'exception_config_search',
                'exception_config_clear', ]

    def exception_config_new(self, *args):
        """Create a new domain exception table entry.

        CLI command: exceptionconfig > new

        *Parameters*:
        - `address`: The address for which you wish to provide an exception.
        Can be:
        | user@domain | Matches entire email address |
        | user@ | Matches any email address beginning with user@ |
        | @[IP address] | Matches any email address with this IP address |
        | @domain | Matches any email address with this domain |
        | @.partial.domain | Matches any email address domain ending in this domain |
        - `policy`: A policy for this domain exception. Can be:
        | 1 | Allow |
        | 2 | Reject |
        - `use_smtp_custom_code`: Specify a custom SMTP reject response. YES or NO.
        - `smtp_code`: The SMTP code to use in the response. 553 is the standard code.
        - `smtp_rsp`: Custom SMTP response.

        *Return*:
        None

        *Examples*:
        | Exception Config New |
        | ... | address=${u1} |
        | ... | policy=allow |

        | Exception Config New |
        | ... | address=${u2} |
        | ... | policy=reject |
        | ... | use_smtp_custom_code=yes |
        | ... | smtp_code=501 |
        | ... | smtp_rsp=No luck |

        | Exception Config New |
        | ... | address=${u3} |
        | ... | policy=reject |
        | ... | use_smtp_custom_code=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.exceptionconfig().new(**kwargs)

    def exception_config_edit(self, *args):
        """Edit a domain exception table entry.

        CLI command: exceptionconfig > edit

        *Parameters*:
        - `address`: The address to edit.
        Can be:
        | user@domain | Matches entire email address |
        | user@ | Matches any email address beginning with user@ |
        | @[IP address] | Matches any email address with this IP address |
        | @domain | Matches any email address with this domain |
        | @.partial.domain | Matches any email address domain ending in this domain |
        - `new_address`: The address for which you wish to provide an exception.
        - `policy`: A policy for this domain exception. Can be:
        | 1 | Allow |
        | 2 | Reject |
        - `use_smtp_custom_code`: Specify a custom SMTP reject response. YES or NO.
        - `smtp_code`: The SMTP code to use in the response. 553 is the standard code.
        - `smtp_rsp`: Custom SMTP response.

        *Return*:
        None

        *Examples*:
        | Exception Config Edit |
        | ... | address=${u3} |
        | ... | new_address=${u4} |
        | ... | policy=allow |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.exceptionconfig().edit(**kwargs)

    def exception_config_delete(self, *args):
        """Delete a domain exception table entry.

        CLI command: exceptionconfig > delete

        *Parameters*:
        - `address`: The address to delete.

        *Return*:
        None

        *Examples*:
        | Exception Config Delete | address=${u1} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.exceptionconfig().delete(**kwargs)

    def exception_config_print(self):
        """Print all domain exception table entries.

        CLI command: exceptionconfig > print

        *Parameters*:
        None

        *Return*:
        Raw output.

        *Examples*:
        | ${tb}= | Exception Config Print |
        | Log | ${tb} |
        | Should Contain | ${tb} | ${u1} |
        """
        return self._cli.exceptionconfig().print_exception_table()

    def exception_config_search(self, *args):
        """Search domain exception table.

        CLI command: exceptionconfig > search

        *Parameters*:
        - `address`: The address to search for.

        *Return*:
        Boolean. Returns TRUE(1) if address was found otherwise returns FALSE(0).

        *Examples*:
        | ${res}= | Exception Config Search  address=${u1} |
        | Should Be True | ${res} |

        | ${res}= | Exception Config Search  address=some_unknown@mail.qa |
        | Should Not Be True | ${res} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.exceptionconfig().search(**kwargs)

    def exception_config_move(self, *args):
        """Move entries in the domain exception table.

        CLI command: exceptionconfig > move

        *Parameters*:
        - `entry_to_move`: The number of the entry to move.
        - `dst_entry`: The number of the destination for this entry.

        *Return*:
        None

        *Examples*:
        | Exception Config Move  entry_to_move=${u1} | dst_entry=3 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.exceptionconfig().move(**kwargs)

    def exception_config_clear(self, *args):
        """Clear entries in the domain exception table.

        CLI command: exceptionconfig > clear

        *Parameters*:
        - `confirm`: Confirm clearing all domain exceptions. YES or NO.

        *Return*:
        None

        *Examples*:
        | Exception Config Clear | confirm=yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.exceptionconfig().clear(**kwargs)

#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/dict_config.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class DictConfig(CliKeywordBase):
    """
    Create and manage content dictionaries.
    CLI command: dictconfig
    """

    def get_keyword_names(self):
        return ['dict_config_new',
                'dict_config_delete',
                'dict_config_rename',
                'dict_config_edit_new_entry',
                'dict_config_edit_delete_entry',
                'dict_config_edit_settings',
                'dict_config_edit_print',
                'dict_config_edit_export',
                'dict_config_edit_import', ]

    def dict_config_new(self, *args):
        """Create new content dictionary.

        CLI command: dictconfig > new

        *Parameters:*
        - `name`: The name of content dictionary. String. REQUIRED.
        - `file_import`: Specify a file for import. YES or NO. NO by default.
        - `file_name`: The filename to import dictionary from. String.
        - `encoding`:The default encoding to be used for exporting this dictionary.
        - `regular_expr`:The new words or regular expressions.
        Separate multiple entries with line breaks.
        Optionally define weights by separating the word or expression with a comma and number.
        Enter a blank line to finish.

        *Return:*
        None

        *Examples:*
        | Dict Config New | name=${dict1} | regular_expr=.*Andriy.*,10\n^Petro,5\nIvan.*,2 |

        | Dict Config New | name=boo | regular_expr=^babar$ |

        | Dict Config New |
        | ... | name=${dict_imported} |
        | ... | file_import=yes |
        | ... | file_name=${dict_exported} |
        | ... | encoding=Unicode (UTF-16) |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.dictconfig().new(**kwargs)

    def dict_config_delete(self, *args):
        """Delete content dictionary.

        CLI command: dictconfig > delete

        *Parameters:*
        - `name`: The name of the dictionary to delete. REQUIRED.
        - `confirm`: Confirm deleting if dictionary is used by filters. YES or NO.

        *Return:*
        None

        *Examples:*
        | Dict Config Delete | name=some_dictionary |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.dictconfig().delete(**kwargs)

    def dict_config_rename(self, *args):
        """Rename content dictionary.

        CLI command: dictconfig > rename

        *Parameters:*
        - `name`: The name of the dictionary to rename. String. Required.
        - `confirm`: Confirm renaming if dictionary is used by filters. YES or NO.
        - `new_name`: Define new name of the dictionary. String. Required.

        *Return:*
        None

        *Examples:*
        | Dict Config Rename | name=${dict1} | new_name=${dict_renamed} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.dictconfig().rename(**kwargs)

    def dict_config_edit_new_entry(self, *args):
        """Edit content dictionary. Add new entries.

        CLI command: dictconfig > edit > new

        *Parameters:*
        - `name`: The name of the dictionary to edit. String. Required.
        - `regular_expr`: The new words or regular expressions.
        Separate multiple entries with line breaks.
        Optionally define weights by separating the word or expression with a comma and number.
        Enter a blank line to finish.

        *Return:*
        None

        *Examples:*
        | Dict Config Edit New Entry | name=some_name_dict | regular_expr=^reg$ |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.dictconfig(). \
            edit(name=kwargs.pop('name', None)).new(**kwargs)

    def dict_config_edit_delete_entry(self, *args):
        """Edit content dictionary. Delete entry.

        CLI command: dictconfig > edit > delete

        *Parameters:*
        - `name`: The name of the dictionary to edit. String. Required.
        - `dict_entry`: The entry in dictionary to delete. The entry itself or the number of an entry.

        *Return:*
        None

        *Examples:*
        | Dict Config Edit Delete Entry | name=some_name | dict_entry=babar |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.dictconfig(). \
            edit(name=kwargs.pop('name', None)).delete(**kwargs)

    def dict_config_edit_settings(self, *args):
        """Edit content dictionary. Delete entry.

        CLI command: dictconfig > edit > delete

        *Parameters:*
        - `name`: The name of the dictionary to edit. String. Required.
        - `ignore_case`: Ignore case when matching using this dictionary. YES or NO. YES by default.
        - `match_words`: Strings in this dictionary should match complete words. YES or NO. YES by default.
        - `encoding`: The default encoding to be used for exporting this dictionary.

        *Return:*
        None

        *Examples:*
        | Dict Config Edit Settings |
        | ... | name=some_name |
        | ... | ignore_case=No |
        | ... | match_words=No |
        | ... | encoding=Unicode (UTF-8) |

        | Dict Config Edit Settings |
        | ... | name=some_name |
        | ... | ignore_case=yes |
        | ... | encoding=Unicode (UTF-16) |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.dictconfig(). \
            edit(name=kwargs.pop('name', None)).settings(**kwargs)

    def dict_config_edit_print(self, *args):
        """Print content dictionary.

        CLI command: dictconfig > edit > print

        *Parameters:*
        - `name`: The name of the dictionary to print. String. Required.

        *Return:*
        Raw output.

        *Examples:*
        | ${entries}= | Dict Config Edit Print | name=${dict1} |
        | Log | ${entries} |
        | Should Contain | ${entries} | Andriy |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.dictconfig().edit(**kwargs).print_dict()

    def dict_config_edit_import(self, *args):
        """Import content dictionary entries from file.

        CLI command: dictconfig > edit > import

        *Parameters:*
        - `name`: The name of the dictionary to edit. String. Required.
        - `file_name`: The name of the file on machine to import. String. Required.
        - `encoding`: The encoding to use. String. Optional.

        *Return:*
        None

        *Examples:*
        | Dict Config Edit Import |
        | ... | name=some_name |
        | ... | file_name=file.txt |
        | ... | encoding=Unicode (UTF-18) |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.dictconfig(). \
            edit(name=kwargs.pop('name', None)).import_dict(**kwargs)

    def dict_config_edit_export(self, *args):
        """Export content dictionary to a file.

        CLI command: dictconfig > edit > export

        *Parameters:*
        - `name`: The name of the dictionary to edit. String. Required.
        - `file_name`: The name for the exported file. String. Required.
        - `encoding`: The encoding to use. String. Optional.

        *Return:*
        None

        *Examples:*
        | Dict Config Edit Export |
        | ... | name=some_name |
        | ... | file_name=boo.txt |
        | ... | encoding=Unicode (UTF-16) |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.dictconfig(). \
            edit(name=kwargs.pop('name', None)).export_dict(**kwargs)

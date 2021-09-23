#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/show_config.py#1 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class ShowConfig(CliKeywordBase):

    """Shows the current system configuration."""

    def get_keyword_names(self):
        return [
            'show_config',
        ]

    def show_config(self, include_pwd=DEFAULT):
        """Shows the current system configuration.
        This does not include uncommitted changes.

        showconfig

        Parameters:
        - `with_passwords`: string with answer to confirmation question if
                    you need to view current system configuration with
                    passwords. Either 'Yes' or 'No'. 'Yes' is used by default.

        Examples:
        | ${command_output}= | Show Config |
        | ${command_output}= | Show Config | include_pwd=No |
        """
        output = self._cli.showconfig(self._process_yes_no(include_pwd))
        self._info(output)
        return output


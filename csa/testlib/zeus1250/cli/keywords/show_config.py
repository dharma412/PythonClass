#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/show_config.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class ShowConfig(CliKeywordBase):
    """Shows the current system configuration."""

    def get_keyword_names(self):
        return ['show_config']

    def show_config(self, mask_pwd=DEFAULT):
        """Shows the current system configuration.
        This does not include uncommitted changes.

        showconfig

        Parameters:
        - `mask_pw`: string with answer to confirmation question if
                    you need to view current system configuration with
                    passwords. Either 'Yes' or 'No'. 'Yes' is used by default.

        Examples:
        | ${command_output}= | Show Config |
        | ${command_output}= | Show Config | mask_pwd=No |
        """
        output = self._cli.showconfig(self._process_yes_no(mask_pwd))
        self._info(output)
        return output

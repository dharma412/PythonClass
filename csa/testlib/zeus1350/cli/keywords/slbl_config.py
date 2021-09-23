#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/slbl_config.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class SLBLConfig(CliKeywordBase):
    """Keywords for slblconfig CLI command."""

    def get_keyword_names(self):
        return ['slbl_config_import',
                'slbl_config_export']

    def slbl_config_import(self, filename=DEFAULT, ignore_invalid=DEFAULT):
        """Replace all entries in SLBL with entries from file.

        Parameters:
        - `filename`: name or number of the file to import.
        - `ignore_invalid`: ignore invalid entries.

        Examples:
        | SLBL Config Import | some_file.csv | yes |
        | SLBL Config Import | filename=1 |
        """
        self._cli.slblconfig().Import(filename,
                                      self._process_yes_no(ignore_invalid))

    def slbl_config_export(self):
        """Export SLBL entries to a file.

        Return:
        Name of the file where entries were exported to.

        Examples:
        | ${filename} = | SLBL Config Export |
        """
        return self._cli.slblconfig().export()

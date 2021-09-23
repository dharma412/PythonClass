#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/slbl_config.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class SLBLConfig(CliKeywordBase):
    """Keywords for slblconfig CLI command."""

    def get_keyword_names(self):
        return ['slbl_config_import',
                'slbl_config_export']

    def slbl_config_import(self, filename=DEFAULT, ignore_invalid=DEFAULT, timeout=40):
        """Replace all entries in SLBL with entries from file.

        Parameters:
        - `filename`: name or number of the file to import.
        - `ignore_invalid`: ignore invalid entries.
        - `timeout`: timeout. Default value is 40 seconds.

        Examples:
        | SLBL Config Import | some_file.csv | yes | 20 |
        | SLBL Config Import | some_file.csv | no |
        | SLBL Config Import | filename=1 |
        """
        self._cli.slblconfig().Import(filename,
                                      self._process_yes_no(ignore_invalid), float(timeout))

    def slbl_config_export(self, timeout=20):
        """Export SLBL entries to a file.

        Parameters:
        - `timeout`: timeout. Default value is 20 seconds.

        Return:
        Name of the file where entries were exported to.

        Examples:
        | ${filename} = | SLBL Config Export | 25 |
        | ${filename} = | SLBL Config Export |
        """
        return self._cli.slblconfig().export(float(timeout))

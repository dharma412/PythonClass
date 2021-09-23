#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase


class Resume(CliKeywordBase):
    """Keywords for resume CLI command."""

    def get_keyword_names(self):
        return ['resume', ]

    def resume(self):
        """Resume receiving and delivery.

        Exceptions:
        - `ConfigError`: in case receiving and delivery can not be resumed.

        Examples:
        | Resume |
        """
        self._cli.resume()

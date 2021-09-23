#!/usr/bin/env python
# $Id: //prod/main/sarf/testlib/zeus79/cli/keywords/setiafmode.py#2

from common.cli.clicommon import CliKeywordBase

class Setiafmode(CliKeywordBase):
    """Set the iaf mode."""

    def get_keyword_names(self):
        return ['setiafmode',]

    def _string_to_bool(self, val):
        if val:
            if val.lower()  == "on":
                return True
            elif val.lower() == "off":
                return False
            else:
                raise ValueError('Invalid value - should be ON or OFF')
        return False

    def setiafmode(self, on_off):
        """Set the iaf mode off/on.
            Set the CLI into a mode that adds conveniences for automated testing.
            E.g. with enabled iafmode it disables EULA when enabling any services

        setiafmode

        Parameters:
        -  on_off:  string to turn IAF mode on or off

        Example:
        | Setiafmode    on |

        """

        request = self._string_to_bool(on_off)
        self._cli.setiafmode(request)

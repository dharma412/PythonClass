#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/path_mtu_discovery.py#1 $

from common.cli.clicommon import CliKeywordBase

class PathMtuDiscovery(CliKeywordBase):
    """ Enable or disable path MTU discovery."""

    def get_keyword_names(self):
        return [
            'path_mtu_discovery',
        ]

    def path_mtu_discovery(self, answer='yes'):
        """This command toggles path MTU discovery option.

        Parameters:
        - `answer`: answer to confirmation question. Either 'yes' or 'no'.
        Default 'yes'.

        Examples:
        | Path Mtu Discovery | answer=no |

        | Path Mtu Discovery |
        """

        self._cli.pathmtudiscovery(answer)

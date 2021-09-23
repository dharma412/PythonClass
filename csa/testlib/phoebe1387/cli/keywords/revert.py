#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/revert.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase
from sal.containers.yesnodefault import DEFAULT, YES


class Revert(CliKeywordBase):

    """Keywords for revert CLI command."""

    def get_keyword_names(self):
        return ['revert']

    def revert(self, version=DEFAULT, continue_revert='', confirm_revert='',
               confirm_switch=''):
        """Reverting to an Earlier Version of AsyncOS.

        revert

        *Parameters:*
        - `version`: a previous version to use in format X.X.X-XXX. Mandatory.
        - `continue_revert`: should reverting be continued. Either 'Yes' or 'No'.
        'No' by default
        - `confirm_revert`: confirm reverting. Either 'Yes' or 'No'. 'No' by default
        - `confirm_switch`: whether to force switch from cluster to machine mode.
        Either 'Yes' or 'No'. 'Yes' by default.

        *Examples:*
        | Revert | version=7.6.0-444 |
        | ... | continue_revert=Yes |
        | ... | confirm_revert=Yes |
        """
        kwargs = {'version': version,
                  'continue': self._process_yes_no(continue_revert),
                  'confirm_switch': self._process_yes_no(confirm_switch),
                  'confirm': self._process_yes_no(confirm_revert)}
        self._cli.revert(**kwargs)

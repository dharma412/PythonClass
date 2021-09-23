# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/sdr_diagnostics.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class SdrDiagnostics(CliKeywordBase):
    """Run diagnostics on Sender Domain Repuataion engine via CLI."""

    def get_keyword_names(self):
        return ['sdr_diagnostics',
                'sdr_diagnostics_batch']

    def sdr_diagnostics(self):
        """
        CLI > sdrdiagnostics
        1. Show status of the Sender Domain Reputation service
        [1]>

        Connection Status: Connected

        Use this keyword to diagnose Sender Domain Repuataion engine via CLI.

        *Parameters:*
        - none

        *Return:*
        - Return the status of Sender Domain Repuataion engine.

        *Example:*
        | ${sdr_diagnostics}= | Sdr Diagnostics    |
        | Log                 | ${sdr_diagnostics} |
        """

        return self._cli.sdrdiagnostics()

    def sdr_diagnostics_batch(self):
        """
        Keyword to run sdrdiagnostics command in batch mode.

        :params:
            None
        :return:
            None
        :examples:
            | ${sdr_diagnostics_batch_output} | Sdr Diagnostics Batch|
            | Log                             | ${sdr_diagnostics_batch_output} |
        """
        return self._cli.sdrdiagnostics.batch()

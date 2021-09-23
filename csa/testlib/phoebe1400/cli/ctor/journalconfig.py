"""
Command Line Interface (CLI)
command: - journalconfig
"""

import time

from clictorbase import IafCliConfiguratorBase

class journalconfig(IafCliConfiguratorBase):

    def enable(self, routing_mode, mailbox, journal_mailto, non_journal_action,
               allow_traffic):
        cmd = 'journalconfig enable --routing-mode=%s --mailbox=%s --journal-mail-to=%s' \
              ' --non-journal-action=%s --allow-traffic=%s' \
                  % (routing_mode, mailbox, journal_mailto, non_journal_action, allow_traffic)
        self._writeln(cmd)
        self.clearbuf()
        self._wait_for_prompt(timeout=60)
        output = self.getbuf()

        return output

    def disable(self):
        cmd = 'journalconfig disable'
        self._writeln(cmd)
        self._wait_for_prompt(timeout=60)

    def _status(self, journal_output=False):
        cmd = 'journalconfig'
        self._writeln(cmd)
        self.clearbuf()
        self._wait_for_prompt(timeout=60)

        output = self.getbuf()
        if journal_output:
            return output
        if output.lower().find('easypov mode is enabled') != -1:
            return 'Enabled'
        elif output.lower().find('easypov mode disabled') != -1:
            return 'Disabled'
        elif output.find("Argument") >= 0 or output.find("invalid") >= 0:
            raise clictorbase.IafCliError

    def is_enabled(self):
        stat = self._status()
        if stat == 'Enabled':
            return True
        elif stat == 'Disabled':
            return False

    def journaloutput(self):
        output = self._status(True)
        return output

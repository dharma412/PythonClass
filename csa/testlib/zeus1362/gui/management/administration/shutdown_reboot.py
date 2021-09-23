#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/gui/management/administration/shutdown_reboot.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

import time

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

class ShutdownReboot(GuiCommon):
    """Shutdown/Reboot page interaction class.
    'System Administration -> Shutdown/Reboot' section.
    """

    def get_keyword_names(self):

        return ['shutdown',
                'reboot'
               ]

    def _open_page(self):
        self._navigate_to('Management', 'System Administration',
            'Shutdown/Reboot')

    def _select_operation(self, operation):
        operation_types = {'shutdown':'shutdown',
                           'reboot':'reboot'
                           }
        if operation not in operation_types.keys():
            raise guiexceptions.ConfigError("Invalid operation type '%s'." % \
                                            (operation))
        self.select_from_list('halt_action', 'value=%s' % \
                                (operation_types[operation],))

    def _fill_seconds_to_wait(self, delay):
        if delay is not None:
             if not delay.isdigit():
                 raise guiexceptions.ValueError(
                     'Value must be an integer from 0 to 3,600.')
             self.input_text("xpath=//input[@name='delay']", delay)

    def _click_commit_button(self):
        self.click_button("xpath=//input[@name='Submit']", "don't wait")

    def reboot(self, delay=None):
        """Reboot.

        Parameters:
        - `delay` - maximum number of seconds to wait for connections
            to close before doing a forceful disconnect. Does not need
            confirmation. Value must be an integer from 0 to 3,600.
            Default - 30.

        Examples:
        | reboot |
        | reboot | delay=60 |
        """

        self._open_page()
        self._select_operation('reboot')
        self._fill_seconds_to_wait(delay)
        self._click_commit_button()

    def shutdown(self, delay=None):
        """Shutdown.

        Parameters:
        - `delay` - maximum number of seconds to wait for connections
            to close before doing a forceful disconnect. Does not need
            confirmation. Value must be an integer from 0 to 3,600.
            Default - 30.

        Examples:
        | shutdown |
        | shutdown | delay=15 |
        """
        self._open_page()
        self._select_operation('shutdown')
        self._fill_seconds_to_wait(delay)
        self._click_commit_button()

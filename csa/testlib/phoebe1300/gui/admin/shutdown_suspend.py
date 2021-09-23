#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/shutdown_suspend.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

import functools

from common.gui.decorators import go_to_page
from common.gui.guiexceptions import ConfigError
from common.gui.guicommon import GuiCommon

from shutdown_suspend_def.mail_operations import MailOperationsForm
from shutdown_suspend_def.system_operations import SystemOperationsForm
from shutdown_suspend_def.work_queue import WorkQueueForm

PENDING_CHANGES_MARK = 'You have uncommitted changes pending'


def check_for_pending_changes(func):
    """Decorator used in GuiCommon descendants.
    Checks whether there are pending changes on
    appliance and raises ConfigError if true.
    """

    @functools.wraps(func)
    def decorator(self, *args, **kwargs):
        if self._is_text_present(PENDING_CHANGES_MARK):
            raise ConfigError('You have uncommited changes.' \
                              'Please commit or abandon all your changes in order '
                              'to start upgrade')

        return func(self, *args, **kwargs)

    return decorator


PAGE_PATH = ('System Administration', 'Shutdown/Suspend')


class ShutdownSuspend(GuiCommon):
    """Keywords for interaction with ESA GUI page System Administration ->
    Shutdown/Suspend"""

    def get_keyword_names(self):
        return ['shutdown_suspend_work_queue_status_get',

                'shutdown_suspend_mail_operations_set',
                'shutdown_suspend_mail_operations_get',

                'shutdown_suspend_system_operations_set']

    def _get_cached_controller(self, cls):
        attr_name = '_{0}'.format(cls.__name__.lower())
        if not hasattr(self, attr_name):
            setattr(self, attr_name, cls(self))
        return getattr(self, attr_name)

    @go_to_page(PAGE_PATH)
    def shutdown_suspend_work_queue_status_get(self):
        """Get current work queue status

        *Return:*
        - Dictionary, whose items are:
        | Work Queue Processing Status | Either 'Operational' or
        'Suspended' |
        | Messages in Work Queue | Count of messages in work queue |
        | Generated | Datetime when current report has been generated |

        *Examples:*
        | ${status}= | Shutdown Suspend Work Queue Status Get |
        | Log Dictionary | ${status} |
        | Should Be Equal As Strings |
        | ... | ${status['Work Queue Processing Status']} | Operational |
        """
        controller = self._get_cached_controller(WorkQueueForm)
        return controller.get()

    @go_to_page(PAGE_PATH)
    @check_for_pending_changes
    def shutdown_suspend_mail_operations_set(self, settings):
        """Set mail operations settings

        *Parameters:*
        - `settings`: dictionary, whose items can be the following
        | Listeners | dictionary containing settings for each listener.
        Each dictionary key is existing listener name and value is
        either 'suspend' or 'resume'. In case the listener is already
        resumed/suspended and you want to perform same action again, then
        it will be silently ignored by the keyword. Also, can be
        a simple 'suspend'/'resume' string to perform this operation for
        all existing listeners |
        | Suspend Delivery for | list or comma separated string. Domains
        for which delivery is going to be suspended/resumed.
        You may set 'ALL' to suspend/resume delivery for all
        domains |
        | Connections Close Timeout | number of seconds to wait
        before forcibly closing connections. 30 by default |

        *Exceptions:*
        - `ValueError`: If any of given listeners doesn't exist
        - `TimeoutError`: If keyword fails to set domains list
        - `ConfigError`: if there are uncommited changes on appliance

        *Examples:*
        | ${timeout}= | Set Variable | 20 |
        | ${listeners_settings}= | Create Dictionary |
        | ... | ${PUBLIC_LISTENER.name} | suspend |
        | ... | ${PRIVATE_LISTENER.name} | suspend |
        | ${domains}= | Create List | a.com | b.com |
        | ${settings}= | Create Dictionary |
        | ... | Listeners | ${listeners_settings} |
        | ... | Suspend Delivery for | ${domains} |
        | ... | Connections Close Timeout | ${timeout} |
        | Commit Changes |
        | Shutdown Suspend Mail Operations Set | ${settings} |
        """
        controller = self._get_cached_controller(MailOperationsForm)
        controller.set(settings)
        controller.commit()

    @go_to_page(PAGE_PATH)
    def shutdown_suspend_mail_operations_get(self):
        """Get current mail operations settings

        *Return:*
        - Dictionary. See parameters description of
        `Shutdown Suspend Mail Operations Set` keyword for more details.
        This keyword will set 'Suspended' value for suspended listener
        and 'Online' value for online ones.

        *Examples:*
        | ${status}= | Shutdown Suspend Mail Operations Get |
        | Log Dictionary | ${status} |
        | ${listeners_dict}= | Get From Dictionary | ${status} | Listeners |
        | Log Dictionary | ${listeners_dict} |
        | Should Be Equal As Strings |
        | ... | ${listeners_dict['${PUBLIC_LISTENER.name}']} | Suspended |
        | Should Be Equal As Strings |
        | ... | ${listeners_dict['${PRIVATE_LISTENER.name}']} | Suspended |
        | Lists Should Be Equal |
        | ... | ${status['Suspend Delivery for']} | ${domains} |
        """
        controller = self._get_cached_controller(MailOperationsForm)
        return controller.get()

    @go_to_page(PAGE_PATH)
    @check_for_pending_changes
    def shutdown_suspend_system_operations_set(self, settings):
        """Set system operations settings

        *Parameters:*
        - `settings`: dictionary, whose items can be the following
        | Operation | Either 'Reboot' or 'Shutdown' |
        | Connections Close Timeout | number of seconds to wait
        before forcibly closing connections. 30 by default |

        *Exceptions:*
        - `ValueError`: if any of given values is not correct
        - `ConfigError`: if there are uncommited changes on appliance

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | Operation | Reboot |
        | ... | Connections Close Timeout | 20 |
        | Commit Changes |
        | Shutdown Suspend System Operations Set | ${settings} |
        """
        controller = self._get_cached_controller(SystemOperationsForm)
        controller.set(settings)
        controller.commit()

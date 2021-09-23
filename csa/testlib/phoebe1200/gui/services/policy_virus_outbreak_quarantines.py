#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/services/policy_virus_outbreak_quarantines.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import functools

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

from pvo_quarantines_def.global_settings import PVOSettings
from pvo_quarantines_def.global_settings import ENABLE_BUTTON, \
    ENABLE_CQ_CHECKBOX, EDIT_SETTINGS_BUTTON

PAGE_PATH = ('Security Services', 'Policy, Virus and Outbreak Quarantines')


def check_pvo_feature(need_to_raise_exc):
    """This decorator is used to navigate and check Security Services
       -> Policy, Virus and Outbreak Quarantines option.

    *Parameters:*
    - `need_to_raise_exc`: whether to raise GuiFeatureDisabledError if
    PVO Quarantines is disabled. Either True or False

    *Exceptions:*
    - `GuiFeatureDisabledError`: if PVO Quarantines is disabled
    and need_to_raise_exc is set to True
    """

    def decorator(func):
        @functools.wraps(func)
        def worker(self, *args, **kwargs):
            if not self.pvo_quarantines_is_enabled():
                if need_to_raise_exc:
                    raise guiexceptions.GuiFeatureDisabledError(
                        'PVO Quarantines is not enabled')
            return func(self, *args, **kwargs)

        return worker

    return decorator


class PVOQuarantine(GuiCommon):
    """ Keywords for "Email Security Appliance-> Security Services -> Policy,
    Virus and Outbreak Quarantines. """

    def get_keyword_names(self):
        return [
            'pvo_quarantines_is_enabled',
            'pvo_quarantines_enable',
            'pvo_quarantines_disable',
            'pvo_quarantines_edit',
        ]

    def _get_pvo_settings_controller(self):
        if not hasattr(self, '_pvo_settings_controller'):
            self._pvo_settings_controller = PVOSettings(self)
        return self._pvo_settings_controller

    @go_to_page(PAGE_PATH)
    def pvo_quarantines_is_enabled(self):
        """ Check if Policy, Virus and Outbreak Quarantines settings
            are enabled.

        *Examples:*
        | ${status}=  | PVO Quarantines Is Enabled |
        | Log | ${status} |
        """
        return not self._is_element_present(ENABLE_BUTTON)

    @check_pvo_feature(False)
    def pvo_quarantines_enable(self, settings={}):
        """ Enable Policy, Virus and Outbreak Quarantines settings.

        *Parameters:*
        Dictionary with keys (optional) :
           | `Quarantine IP Interface` | Quarantine IP Interface. E.x. Management |
           | `Quarantine Port` |  Quarantine Port. It is required parameter and must be > 0. |
           | `Send Notification When Migration Is Completed` |
              string of emails divided by comma to send notification when migration is complete (Optional) |
        If no key is specified, the default values are set.

        *Examples:*

            | ${pvo_enable_settings}= | Create Dictionary |
            | ... | Quarantine IP Interface | Management |
            | ... | Quarantine Port |  7055 |
            | ... | Send Notification When Migration Is Completed | test@test.com |

            | PVO Quarantines Enable |
            | ... | ${pvo_enable_settings} |
        """
        if not self._is_element_present(ENABLE_BUTTON):
            # if already enabled, then return silently
            return

        self.click_button(ENABLE_BUTTON)
        controller = self._get_pvo_settings_controller()
        controller.set(settings)
        self._click_submit_button()

    @check_pvo_feature(False)
    def pvo_quarantines_disable(self):
        """ Disable Policy, Virus and Outbreak Quarantines settings.

        *Examples:*
        | PVO Quarantines Disable |
        """
        if not self._is_element_present(EDIT_SETTINGS_BUTTON):
            # if already disabled, then return silently
            return

        self.click_button(EDIT_SETTINGS_BUTTON)
        controller = self._get_pvo_settings_controller()
        controller.set({ENABLE_CQ_CHECKBOX[0]: False})
        self._click_submit_button()

    @check_pvo_feature(True)
    def pvo_quarantines_edit(self, settings):
        """Edit Policy, Virus and Outbreak Quarantines settings.

        *Parameters:*
        Dictionary with keys :
           | `Quarantine IP Interface` | Quarantine IP Interface. E.x. Management |
           | `Quarantine Port` |  Quarantine Port. It is required parameter and must be > 0. |

        *Examples:*
        | ${pvo_global_settings}= | Create Dictionary |
        | ... | Quarantine IP Interface | Management |
        | ... | Quarantine Port |  7055 |

        | PVO Quarantines Edit |
        | ... | ${pvo_global_settings} |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        controller = self._get_pvo_settings_controller()
        controller.set(settings)
        self._click_submit_button()

#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/management/services/policy_virus_outbreak_quarantines.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

import functools
import re
import time

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

from pvo_quarantines_def.global_settings import PVOGlobalSettings
from pvo_quarantines_def.global_settings import ENABLE_BUTTON, \
       ENABLE_CQ_FOR_PVO_CHECKBOX, EDIT_GLOBAL_SETTINGS__BUTTON
from pvo_quarantines_def.migration_wizard import PVOMigrationWizard, \
                                                LAUNCH_WIZARD_BUTTON

PAGE_PATH = ('Management Appliance', 'Centralized Services',
             'Policy, Virus and Outbreak Quarantines')

def check_pvo_feature(need_to_raise_exc):
    """This decorator is used to navigate and check Management Appliance->
    Centralized Services -> Policy, Virus and Outbreak Quarantines option.

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
                        'PVO Quarantines is not enabled' )
            return func(self, *args, **kwargs)
        return worker
    return decorator


class PVOQuarantine(GuiCommon):
    """ Keywords for "Management Appliance-> Centralized Services -> Policy,
    Virus and Outbreak Quarantines. """

    def get_keyword_names(self):
        return [
                'pvo_quarantines_is_enabled',
                'pvo_quarantines_enable',
                'pvo_quarantines_disable',
                'pvo_quarantines_edit',
                'pvo_migration_wizard_run',
                ]

    def _get_pvo_global_settings_controller(self):
        if not hasattr(self, '_pvo_global_settings_controller'):
            self._pvo_global_settings_controller = PVOGlobalSettings(self)
        return self._pvo_global_settings_controller

    def _get_pvo_migration_wizard_controller(self):
        if not hasattr(self, '_pvo_migration_wizard_controller'):
            self._migration_wizard_controller = PVOMigrationWizard(self)
        return self._migration_wizard_controller

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
    def pvo_quarantines_enable(self):
        """ Enable Policy, Virus and Outbreak Quarantines settings.

        *Examples:*
        | PVO Quarantines Enable |
        """
        if not self._is_element_present(ENABLE_BUTTON):
            # if already enabled, then return silently
            return

        self.click_button(ENABLE_BUTTON)
        self._accept_license()
        self._click_submit_button()

    @check_pvo_feature(False)
    def pvo_quarantines_disable(self):
        """ Disable Policy, Virus and Outbreak Quarantines settings.

        *Examples:*
        | PVO Quarantines Disable |
        """
        if not self._is_element_present(EDIT_GLOBAL_SETTINGS__BUTTON):
            # if already disabled, then return silently
            return

        self.click_button(EDIT_GLOBAL_SETTINGS__BUTTON)
        controller = self._get_pvo_global_settings_controller()
        controller.set({ENABLE_CQ_FOR_PVO_CHECKBOX[0]:False})
        self._click_submit_button()

    @check_pvo_feature(True)
    def pvo_quarantines_edit(self, settings):
        """Edit Policy, Virus and Outbreak Quarantines settings.

        *Parameters:*
        Dictionary with keys :
           | `Quarantine IP Interface` | Quarantine IP Interface. |
           | `Quarantine Port` |  Quarantine Port. It is required parameter and must be > 0. |

        *Examples:*
        | ${pvo_global_settings}= | Create Dictionary |
        | ...  Quarantine IP Interface | Management |
        | ...  Quarantine Port |  7055 |

        | PVO Quarantines Edit |
        | ... | ${pvo_global_settings} |
        """
        self.click_button(EDIT_GLOBAL_SETTINGS__BUTTON)
        controller = self._get_pvo_global_settings_controller()
        controller.set(settings)
        self._click_submit_button()

    @check_pvo_feature(True)
    def pvo_migration_wizard_run(self, settings):
        """ Migration Wizard for Policy, Virus and Outbreak Quarantines.

        *Parameters:*
        Dictionary, containing the following keys/values :
        - `PQ Migration Mode`: can be `Automatic` or `Custom`. If the key is
           absent, the `Automatic` mode is chosen by default.
        - `Policy Quarantines Mapping`: dictionary containing mappings of settings.
           The key is mandatory if `Custom` value of the `PQ Migration Mode` is chosen.
           This dictionary can contain next keys/values:
           | key | Name of SMA Quarantine Policy |
           | value | Can contain the following values: |

                | 'All' | add all ESA PVO Quarantines |
                | ESA1_HOSTNAME\tESA2_HOSTNAME | add all ESA PVO Quarantines from
                mentioned ESA hosts. Separator is tab character TAB  - '\\t' |
                | POLICY_NAME\nESA1_HOSTNAME\tPOLICY_NAME\nESA2_HOSTNAME  | custom policy from particular esa. Separators are: |
                    |    | '\\t'  | tab character (TAB) - separator between policy-hostname conjunction |
                    |    |  '\\n' | line feed (LF)  -  separator between policy and hosts |

        *Examples:*
        | ${quarantines_migration_mappings}= |  Create Dictionary |
        |  ...  | Policy  | vm10esa0022\\nvm10esa0022.qa |
        |  ...  | New_Test_Quarantine  | Policy\\nvm10esa0022.qa |
        |  ...  | TestCentralizedQuarantine  | vm10esa0018.qa\\tvm10esa0022.qa |

        | ${pvo_migration_settings}= |  Create Dictionary |
        |  ... | PQ Migration Mode | Custom |
        | ...  | Policy Quarantines Mapping | ${quarantines_migration_mappings} |

        | Pvo Migration Wizard Run |
        | ...  | ${pvo_migration_settings} |

        """
        self.click_button(LAUNCH_WIZARD_BUTTON)
        controller = self._get_pvo_migration_wizard_controller()
        controller.set(settings)

#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/services/antispam.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import functools

from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

from antispam_def.case_engine_page import CASEEnginePage
from antispam_def.ims_engine_page import IMSEnginePage
from antispam_def.cloudmark_engine_page import CloudmarkEnginePage

AVAILABLE_ENGINES = (CASEEnginePage, IMSEnginePage, CloudmarkEnginePage)

ENABLE_BUTTON = "//input[@value='Enable...']"
ENABLE_CHECKBOX = "//input[contains(@id, 'enabled') and @type='checkbox']"
ACCEPT_LICENCE_BUTTON = "//input[@name='action:AcceptLicense']"
EDIT_SETTINGS_BUTTON = "//input[@value='Edit Global Settings...']"
UPDATENOW_BUTTON = "//input[@name='action:UpdateNow']"
ACTION_RESULTS = "//td[@id='action-results-message']"
CANCEL_BUTTON = "//input[@name='action:EditCancel' or @name='CancelSettings']"

NO_FKEY_MARK = 'The feature key for this feature has expired or is unavailable'


def check_antispam_feature(need_to_raise_exc):
    """This decorator is used to navigate and check Antispam features.
     Decorator can be applied only to
    Antispam class methods whose first parameter is provider name
    (either "ironport", "ims" or "cloudmark")

    *Parameters:*
    - `need_to_raise_exc`: whether to raise GuiFeatureDisabledError if
    antispam feature is disabled. Either True or False

    *Exceptions:*
    - `GuiFeatureDisabledError`: if corresponding feature is disabled
    and need_to_raise_exc is set to True
    """

    def decorator(func):
        @functools.wraps(func)
        def worker(self, provider, *args, **kwargs):
            if not self.antispam_is_enabled(provider):
                if need_to_raise_exc:
                    raise guiexceptions.GuiFeatureDisabledError(
                        '%s antispam feature is not enabled' % \
                        (provider,))
            return func(self, provider, *args, **kwargs)

        return worker

    return decorator


class Antispam(GuiCommon):
    """Keywords for ESA GUI interaction with Security Services ->
    IronPort Anti-Spam, Security Services -> Cloudmark SP
    and Security Services -> IronPort Intelligent Multi-Scan pages
    """

    def get_keyword_names(self):
        return ['antispam_is_enabled',
                'antispam_enable',
                'antispam_disable',
                'antispam_edit_settings',
                'antispam_update_now',
                'antispam_get_details']

    def _get_controller(self, provider_marker):
        provider_marker = provider_marker.lower()
        for engine_class in AVAILABLE_ENGINES:
            if provider_marker in engine_class.get_markers():
                return engine_class(self)
        raise ValueError('Unknown provider name is passed: "%s"' % \
                         (provider_marker,))

    def antispam_is_enabled(self, provider):
        """Return antispam feature state

        *Parameters:*
        - `provider`: name of antispam provider. Either "IronPort"
        or "IMS" or "Cloudmark"

        *Return:*
        True if antispam feature is enabled or False otherwise

        *Exceptions:*
        - `ValueError`: if unknown provider name is passed
        - `GuiFeaturekeyMissingError`: if feature key for the
        particular provider is not installed

        *Examples:*
        | ${ims_state}= | AntiSpam Is Enabled | Ironport |
        """
        controller = self._get_controller(provider)
        PAGE_PATH = ('Security Services', controller.get_menu_entry_name())

        self._debug('Opening "%s" page' % (' -> '.join(PAGE_PATH),))
        is_navigation_successfull = True
        try:
            self._navigate_to(*PAGE_PATH)
        except Exception as e:
            print e
            is_navigation_successfull = False
        if self._is_text_present(NO_FKEY_MARK) or not is_navigation_successfull:
            raise guiexceptions.GuiFeaturekeyMissingError('"%s" feature ' \
                                                          'can not be reached because the corresponding feature key is ' \
                                                          'not installed' % (PAGE_PATH[1],))

        DISABLED_MARK = 'is currently disabled globally.'
        return not self._is_text_present(DISABLED_MARK)

    @check_antispam_feature(False)
    def antispam_enable(self, provider):
        """Enable antispam feature.
        Ignore state if feature is already enabled.

        *Parameters:*
        - `provider`: name of antispam provider to be enabled.
        Either "IronPort" or "IMS" or "Cloudmark"

        *Exceptions:*
        - `ValueError`: if unknown provider name is passed
        - `GuiFeaturekeyMissingError`: if feature key for the
        particular provider is not installed

        *Examples:*
        | AntiSpam Enable | IronPort |
        """
        LICENSE_AGREEMENT_MARK = 'License Agreement'

        if self._is_element_present(ENABLE_BUTTON):
            self.click_button(ENABLE_BUTTON)
            if self._is_text_present(LICENSE_AGREEMENT_MARK):
                self.click_button(ACCEPT_LICENCE_BUTTON)
            self._check_action_result()

    @check_antispam_feature(False)
    def antispam_disable(self, provider):
        """Disable antispam feature.
        Ignore state if feature is already enabled.

        *Parameters:*
        - `provider`: name of antispam provider to be disabled.
        Either "IronPort" or "IMS" or "Cloudmark"

        *Exceptions:*
        - `ValueError`: if unknown provider name is passed
        - `GuiFeaturekeyMissingError`: if feature key for the
        particular provider is not installed

        *Examples:*
        | AntiSpam Disable | IMS |
        """
        if self._is_element_present(EDIT_SETTINGS_BUTTON):
            self.click_button(EDIT_SETTINGS_BUTTON)
            self._unselect_checkbox(ENABLE_CHECKBOX)
            self._click_submit_button()

    @check_antispam_feature(True)
    def antispam_update_now(self, provider):
        """Force particular Antispam provider update

        *Parameters:*
        - `provider`: name of antispam provider to be updated.
        Either "IronPort" or "IMS" or "Cloudmark"

        *Exceptions:*
        - `ValueError`: if unknown provider name is passed
        - `GuiFeaturekeyMissingError`: if feature key for the
        particular provider is not installed
        - `GuiControlNotFoundError`: if given feature can not be
        updated manually

        *Examples:*
        | ${result}= | AntiSpam Update Now | IMS |
        """
        controller = self._get_controller(provider)
        controller.update_now()

    @check_antispam_feature(True)
    def antispam_edit_settings(self, provider, *args):
        """Edit Antispam settings

        *Parameters:*
        - `provider`: name of antivirus provider to be edited.
        Either "IronPort" or "IMS" or "Cloudmark"

        Arguments depend on particular provider. For different
        providers acceptable arguments are:

        *IronPort* and *IMS*:
        - `always_scan_max_size`: always scan messages smaller than
        this number of bytes. You can add a trailing K or M to indicate
        units. Recommended setting is 512K or less.
        - `never_scan_min_size`: never scan messages larger than this
        number of bytes. You can add a trailing K or M to indicate
        units. Recommended setting is 1024K(1MB) or less.
        - `timeout`: timeout for Scanning Single Message (in seconds)

        *Cloudmark*:
        - `never_scan_min_size`: never scan messages larger than this
        number of bytes. You can add a trailing K or M to indicate
        units. Recommended setting is 1024K(1MB) or less.
        - `timeout`: timeout for Scanning Single Message (in seconds)

        *Exceptions:*
        - `GuiFeatureDisabledError`: if corresponding feature is disabled
        - `ValueError`: if provider name or setting parameter is not correct

        *Examples:*
        | AntiSpam Edit Settings | IronPort |
        | ... | always_scan_max_size=1000 |
        | ... | never_scan_min_size=120000 |
        | ... | timeout=120 |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        controller = self._get_controller(provider)
        kwargs = self._parse_args(args)
        controller.set(kwargs)
        self._click_submit_button()

    @check_antispam_feature(True)
    def antispam_get_details(self, provider):
        """Get Antispam provider details

        *Parameters:*
        - `provider`: name of antispam provider.
        Either "IronPort" or "IMS" or "Cloudmark"

        *Exceptions:*
        - `GuiFeatureDisabledError`: if corresponding feature is disabled
        - `ValueError`: if provider name is not correct

        *Return:*
        Result depends on particular provider. For different
        providers results are:

        *IronPort* and *IMS*:
        Dictionary whose items are:
        | `always_scan_max_size` | always scan messages smaller than
        this number of bytes. |
        | `never_scan_min_size` | never scan messages larger than this
        number of bytes |
        | `timeout` | timeout for Scanning Single Message (in seconds) |
        | `Rule Updates` | <list of rule updates items> |
        each list item is dictionary whose items are:
        | `Rule Type` | type of particular rule  |
        | `Last Update` | timestamp of last update |
        | `Current Version` | version of particular rule |

        *Cloudmark*:
        Dictionary whose items are:
        | `never_scan_min_size` | never scan messages larger than this
        number of bytes |
        | `timeout` | timeout for Scanning Single Message (in seconds) |
        | `Rule Updates` | <list of rule updates items> |

        each list item is dictionary whose items are:

        | `Rule Type` | type of particular rule  |
        | `Last Update` | timestamp of last update |
        | `Current Version` | version of particular rule |

        *Examples:*
        | ${details}= | AntiSpam Get Details | Ironport |
        | Log ${details} |
        | ${timeout}= | Get From Dictionary | ${details} | timeout |
        | Log | ${timeout} |
        | @{rule_upd}= | Get From Dictionary | ${details} | Rule Updates |
        | Log Many | @{rule_upd} |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        controller = self._get_controller(provider)
        return controller.get()

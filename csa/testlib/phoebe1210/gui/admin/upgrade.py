#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/admin/upgrade.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

import functools

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
from common.gui.guiexceptions import ConfigError

from upgrade_def.upgrade_notification import NotificationSettings, \
    NotificationBalloon
from upgrade_def.upgrade_wizard import SystemUpgradeWizard
from upgrade_def.wizard_pages import OPERATIONS_KEY, UPGRADE_FILE_KEY, \
    INSTALL_OPERATION, DOWNLOAD_AND_INSTALL_OPERATION, \
    DOWNLOAD_ONLY_OPERATION

UPGRADE_OPTIONS_BUTTON = "//input[@value='Upgrade Options...']"

EDIT_NOTIF_SETTINGS_BUTTON = "//input[@value='Edit Settings...']"
CANCEL_BUTTON = "//input[@value='Cancel']"

PENDING_CHANGES_MARK = 'You have uncommitted changes pending'

PAGE_PATH = ('System Administration', 'System Upgrade')


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


class SystemUpgrade(GuiCommon):
    """Keywords for interaction with ESA GUI page System Administration ->
    System Upgrade"""

    def get_keyword_names(self):
        return ['system_upgrade',
                'system_upgrade_download_and_install',
                'system_upgrade_download',
                'system_upgrade_install',
                'system_upgrade_delete_downloaded',
                'system_upgrade_get_available',

                'system_upgrade_edit_notification_settings',
                'system_upgrade_get_notification_settings',
                'system_upgrade_is_notification_exist',
                'system_upgrade_get_notification_text',
                'system_upgrade_clear_notification']

    def _get_cached_controller(self, cls):
        attr_name = '_{0}'.format(cls.__name__.lower())
        if not hasattr(self, attr_name):
            setattr(self, attr_name, cls(self))
        return getattr(self, attr_name)

    def _continue_or_cancel_upgrade(self, params):
        if not params.has_key('only_versions'):
            self._only_versions = False
        else:
            self._only_versions = params['only_versions']

        if not params.has_key('continue_upgrade'):
            self._continue_upgrade = True
        else:
            self._continue_upgrade = params['continue_upgrade']

        if self._continue_upgrade:
            self._wait_until_element_is_present('//button[contains(text(),"Upgrade")]',
                                                timeout=10)
            self.click_button('//button[contains(text(),"Upgrade")]')
        else:
            self.click_button('//button[contains(text(),"Cancel")]', \
                              'don\'t wait')

    @go_to_page(PAGE_PATH)
    @check_for_pending_changes
    def system_upgrade_get_available(self, *args):
        """Get list of files available for upgrade

        *Parameters:*
        - `only_versions`: whether to return full upgrade names
        or only version numbers. Either ${False} or ${True}.
        ${False} by default
        - `continue_upgrade`: Whether to continue with upgrade process or not.
        Optional parameter. Default value: ${True}

        *Exceptions:*
        - `ConfigError`: if there are pending changes on appliance

        *Return:*
        List of strings containing version numbers in format X.X.X-XXX
        or full upgrade names depending on `only_versions` parameter
        value

        *Examples:*
        | ${versions_list}= | System Upgrade Get Available | ${True} |
        | ${dest_version}= | Get From List | ${versions_list} | 0 |
        | System Upgrade | ${dest_version} |
        """
        upgrades_list = []
        params = self._parse_args(args)
        self.click_button(UPGRADE_OPTIONS_BUTTON)
        self._continue_or_cancel_upgrade(params)
        if self._continue_upgrade:
            controller = self._get_cached_controller(SystemUpgradeWizard)
            upgrades_list = controller.get_available_upgrades(self._only_versions)
        return upgrades_list

    @go_to_page(PAGE_PATH)
    @check_for_pending_changes
    def system_upgrade(self, dest_version, settings={}):
        """Perform system upgrade and wait until it finishes.
        An appliance goes for reboot after upgrade finishes,
        so you have to handle this behavior in test

        *Parameters:*
        - `dest_version`: AsyncOS version-build ID in format X.X.X-XXX
        or full name of upgrade. Mandatory
        - `settings`: dictionary whose items are
        | `Save the Current Configuration` | whether to save current
        config before upgrade. Either ${True} or ${False} |
        | `Email the Current Configuration to` | email address(es) to
        where current config will be sent |
        | `Save Password Option` | How to save passwords in configuration
        file. Values are: 'Plain passwords in the configuration file',
        'Mask passwords in the configuration file' or 'Encrypt passwords
        in the configuration file'|
        | `Cancel System Upgrade From Upgrade Check Window`.Either
        ${True} or ${False}. Default: ${False} |

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct
        - `ConfigError`: if there are pending changes on appliance

        *Examples:*
        | ${upgrade_settings}= | Create Dictionary |
        | ... | Save the Current Configuration | ${True} |
        | ... | Email the Current Configuration to | mm@example.com |
        | ... | Save Password Option | Mask Passwords in the Configuration File |
        | System Upgrade | 8.0.0-621 | ${upgrade_settings} |
        | Selenium Close |
        | Wait Until DUT Reboots | timeout=1200 | wait_for_ports=22,80 |
        | Start CLI Session If Not Open |
        | Selenium Login |

        or

        | ${upgrade_settings}= | Create Dictionary |
        | ... | Save the Current Configuration | ${True} |
        | ... | Email the Current Configuration to | mm@example.com |
        | ... | Save Password Option | Plain passwords in the configuration file |
        | System Upgrade Download And Install | 8.0.0-621 | ${upgrade_settings} |
        | Selenium Close |
        | Wait Until DUT Reboots | timeout=1200 | wait_for_ports=22,80 |
        | Start CLI Session If Not Open |
        | Selenium Login |

        or

        | ${upgrade_settings}= | Create Dictionary |
        | ... | Save the Current Configuration | ${True} |
        | ... | Email the Current Configuration to | mm@example.com |
        | ... | Save Password Option | Encrypt passwords in the configuration file |
        | ... | Cancel System Upgrade From Upgrade Check Window | ${True} |
        | System Upgrade Download And Install | 8.0.0-621 | ${upgrade_settings} |
        """
        params = {}
        if settings.has_key( \
                'Cancel System Upgrade From Upgrade Check Window'):
            params['continue_upgrade'] = False

        self.click_button(UPGRADE_OPTIONS_BUTTON, 'don\'t wait')
        self._continue_or_cancel_upgrade(params)
        if self._continue_upgrade:
            controller = self._get_cached_controller(SystemUpgradeWizard)
            settings.update({UPGRADE_FILE_KEY: dest_version,
                             OPERATIONS_KEY: DOWNLOAD_AND_INSTALL_OPERATION})
            controller.set(settings)

    # symlink
    system_upgrade_download_and_install = system_upgrade

    @go_to_page(PAGE_PATH)
    @check_for_pending_changes
    def system_upgrade_download(self, *args):
        """Download system upgrade without applying it. In case there
        already exists some previously downloaded upgrade it will be
        overridden with this one.

        *Parameters:*
        - `dest_version`: AsyncOS version-build ID in format X.X.X-XXX
        or full name of upgrade. Mandatory
        - `continue_upgrade`: Whether to continue with upgrade process or not.
        Optional parameter. Default value: ${True}

        *Exceptions:*
        - `ValueError`: if the `dest_version` parameter contains incorrect
        value
        - `ConfigError`: if there are pending changes on appliance

        *Examples:*
        | ${build_to_version_code}= | Catenate |
        | ... | re.sub(r'\\w+\\-([0-9]+)\\-([0-9]+)\\-([0-9]+)\\-([0-9]+)', |
        | ... | r'\\1.\\2.\\3-\\4', '${ESA_BUILD}') |
        | ${ESA_VERSION}= | Evaluate | ${build_to_version_code} | re |
        | @{versions_list}= | System Upgrade Get Available | ${True} |
        | List Should Contain Value | ${versions_list} | ${ESA_VERSION} |
        | System Upgrade Download | dest_version=${ESA_VERSION} |
        | System Upgrade Download | dest_version=${ESA_VERSION} | continue_upgrade=${False} |
        """
        params = self._parse_args(args)
        self.click_button(UPGRADE_OPTIONS_BUTTON)
        self._continue_or_cancel_upgrade(params)
        if self._continue_upgrade:
            controller = self._get_cached_controller(SystemUpgradeWizard)
            settings = {UPGRADE_FILE_KEY: params['dest_version'],
                        OPERATIONS_KEY: DOWNLOAD_ONLY_OPERATION}
            controller.set(settings)

    @go_to_page(PAGE_PATH)
    @check_for_pending_changes
    def system_upgrade_install(self, dest_version, settings={}):
        """Install previously downloaded system upgrade

        *Parameters:*
        - `dest_version`: AsyncOS version-build ID in format X.X.X-XXX
        or full name of upgrade. Mandatory
        - `settings`: dictionary whose items are
        | `Save the Current Configuration` | whether to save current
        config before upgrade. Either ${True} or ${False} |
        | `Email the Current Configuration to` | comma separated email
        address(es) to where current config will be sent |
        | `Save Password Option` | How to save passwords in configuration
        file. Values are: 'Plain passwords in the configuration file',
        'Mask passwords in the configuration file' or 'Encrypt passwords
        in the configuration file'|
        | `Cancel System Upgrade From Upgrade Check Window`.Either
        ${True} or ${False}. Default: ${False} |

        *Exceptions:*
        - `ValueError`: if the `dest_version` parameter contains incorrect
        value
        - `ConfigError`: if there are pending changes on appliance or there is
        no upgrade downloaded yet

        *Examples:*
        | System Upgrade Download | dest_version=${ESA_VERSION} |
        | ${upgrade_settings}= | Create Dictionary |
        | ... | Save the Current Configuration | ${True} |
        | ... | Email the Current Configuration to | mm@example.com |
        | ... | Save Password Option | Encrypt passwords in the configuration file |
        | ... | Cancel System Upgrade From Upgrade Check Window | ${True} |
        | System Upgrade Install | 8.0.0-621 | ${upgrade_settings} |
        """
        params = {}
        if settings.has_key( \
                'Cancel System Upgrade From Upgrade Check Window'):
            params['continue_upgrade'] = False

        self.click_button(UPGRADE_OPTIONS_BUTTON, 'don\'t wait')
        self._continue_or_cancel_upgrade(params)
        if self._continue_upgrade:
            controller = self._get_cached_controller(SystemUpgradeWizard)
            settings.update({UPGRADE_FILE_KEY: dest_version,
                             OPERATIONS_KEY: INSTALL_OPERATION})
            controller.set(settings)

    @go_to_page(PAGE_PATH)
    @check_for_pending_changes
    def system_upgrade_delete_downloaded(self, *args):
        """Delete previously downloaded upgrade

        *Exceptions:*
        - `ConfigError`: if there are pending changes on appliance or
        there are no previously downloaded upgrades

        *Examples:*
        | System Upgrade Download | ${ESA_VERSION} |
        | System Upgrade Delete Downloaded |
        | System Upgrade Delete Downloaded | continue_upgrade=${False} |
        """
        params = self._parse_args(args)
        self.click_button(UPGRADE_OPTIONS_BUTTON, 'don\'t wait')
        self._continue_or_cancel_upgrade(params)
        if self._continue_upgrade:
            controller = self._get_cached_controller(SystemUpgradeWizard)
            controller.delete_current_upgrade()

    @go_to_page(PAGE_PATH)
    def system_upgrade_edit_notification_settings(self, settings):
        """Edit upgrade notification settings

        *Parameters:*
        - `settings`: dictionary. Available items are:
        | AsyncOS Upgrade Notification | Whether to enable (${True})
        or disable (${False}) upgrade notification |

        *Examples:*
        | ${settings}= | Create Dictionary |
        | ... | AsyncOS Upgrade Notification | ${False} |
        | System Upgrade Edit Notification Settings | ${settings} |
        | ${result_info}= | System Upgrade Get Notification Settings |
        | ${current_state}= | Get From Dictionary |
        | ... | ${result_info} | AsyncOS Upgrade Notification |
        | Should Not Be True | ${current_state} |
        """
        self.click_button(EDIT_NOTIF_SETTINGS_BUTTON)
        controller = self._get_cached_controller(NotificationSettings)
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def system_upgrade_get_notification_settings(self):
        """Get current upgrade notification settings

        *Return:*
        - dictionary. Available items are:
        | AsyncOS Upgrade Notification | Whether upgrade notification
        is enabled (${True}) or disabled (${False}) |

        *Examples:*
        - See `System Upgrade Edit Notification Settings` keyword
        example
        """
        self.click_button(EDIT_NOTIF_SETTINGS_BUTTON)
        controller = self._get_cached_controller(NotificationSettings)
        result = controller.get()
        self.click_button(CANCEL_BUTTON)
        return result

    def system_upgrade_is_notification_exist(self):
        """Check whether upgrade notification currently
        exists on web interface

        *Return:*
        - ${True} or ${False}

        *Example:*
        | ${is_exist}= | System Upgrade Is Notification Exist |
        | Should Be True | ${is_exist} |
        """
        self.go_to('https://{0}'.format(self.dut))
        controller = self._get_cached_controller(NotificationBalloon)
        return controller.is_exist()

    def system_upgrade_get_notification_text(self):
        """Get upgrade notification text

        *Return:*
        - Full text of upgrade notification balloon

        *Example:*
        | ${text}= | System Upgrade Get Notification Text |
        | Log | ${text} |
        """
        if not self.system_upgrade_is_notification_exist():
            raise ConfigError('System upgrade notification is not present on GUI')
        controller = self._get_cached_controller(NotificationBalloon)
        return controller.get_text()

    def system_upgrade_clear_notification(self):
        """
        """
        if not self.system_upgrade_is_notification_exist():
            raise ConfigError('System upgrade notification is not present on GUI')
        controller = self._get_cached_controller(NotificationBalloon)
        controller.clear()

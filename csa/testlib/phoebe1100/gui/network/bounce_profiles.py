#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/network/bounce_profiles.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import copy

from common.gui.decorators import go_to_page
from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon

from bounce_profiles_def.bounce_profile import BounceProfileSettings, \
    DefaultBounceProfileSettings
from bounce_profiles_def.bounce_profiles_settings import BounceProfilesSettings

EDIT_SETTINGS_BUTTON = "//input[@name='EditGlobalForm']"

ADD_PROFILE_BUTTON = "//input[@value='Add Bounce Profile...']"
PROFILES_TABLE = "//table[@class='cols']"
PROFILE_NAME_CELLS = "%s/tbody/tr[td]" % (PROFILES_TABLE,)
# idx starts from 1
PROFILE_NAME_CELL_BY_IDX = lambda idx: "%s/tbody/tr[td][%d]/td[1]" % \
                                       (PROFILES_TABLE, idx)
PROFILE_EDIT_LINK = lambda name: "%s//td/a[normalize-space()='%s']" % \
                                 (PROFILES_TABLE, name)
PROFILE_DELETE_CHECKBOX = lambda name: "%s//td[normalize-space()='%s']" \
                                       "/following-sibling::td[1]/input" % \
                                       (PROFILES_TABLE, name)
PROFILES_DELETE_BUTTON = "//input[@id='delete']"
PROFILE_DELETE_ALL_CHECKBOX = "//input[@id='delete_all']"

PAGE_PATH = ('Network', 'Bounce Profiles')


class BounceProfiles(GuiCommon):
    """Keywords for GUI interaction with Network ->
    Bounce Profiles page.
    """

    def get_keyword_names(self):
        return ['bounce_profiles_edit_settings',

                'bounce_profiles_add',
                'bounce_profiles_edit',
                'bounce_profiles_delete',
                'bounce_profiles_get_all']

    def _get_bounce_profiles_settings_controller(self):
        if not hasattr(self, '_bounce_profiles_settings_controller'):
            self._bounce_profiles_settings_controller = \
                BounceProfilesSettings(self)
        return self._bounce_profiles_settings_controller

    def _get_bounce_profile_controller(self, is_default):
        if is_default:
            if not hasattr(self, '_default_bounce_profile_controller'):
                self._default_bounce_profile_controller = \
                    DefaultBounceProfileSettings(self)
            return self._default_bounce_profile_controller
        else:
            if not hasattr(self, '_bounce_profile_controller'):
                self._bounce_profile_controller = BounceProfileSettings(self)
            return self._bounce_profile_controller

    @go_to_page(PAGE_PATH)
    def bounce_profiles_edit_settings(self, settings):
        """Edit Bounce Profiles global settings

        *Parameters:*
        - `settings`: dictionary, whose items can be:
        | Initial Period to Wait Before Retrying an Unreachable Host | number
        of seconds between 60 and 86400 |
        | Maximum Interval Allowed Between Retries to an Unreachable Host | number
        of seconds between 60 and 86400 |

        *Examples:*
        | ${new_settings}= | Create Dictionary |
        | ... | Initial Period to Wait Before Retrying an Unreachable Host | 61 |
        | ... | Maximum Interval Allowed Between Retries to an Unreachable Host |3602 |
        | Bounce Profiles Edit Settings | ${new_settings} |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        self._get_bounce_profiles_settings_controller().set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def bounce_profiles_add(self, name, settings={}):
        """Add new bounce profile

        *Parameters:*
        - `name`: name of the profile to be added
        - `settings`: dictionary containing new profile settings.
        All skipped settings will be taken from the Default profile.
        Possible items are:
        | Maximum Number of Retries | number of retries between 0 and 10000 |
        | Maximum Time in Queue | number of seconds between 0 and 3000000 |
        | Initial Time to Wait per Message | number of seconds between 60
        and 86400 |
        | Maximum Time to Wait per Message | number of seconds between 60
        and 86400 |
        | Hard Bounce Message Subject | string, message subject. Available only
        if `Use DSN format for bounce messages` is set to 'Yes' |
        | Send Delay Message Subject | string, message subject |
        | Minimum Interval Between Messages | number of seconds. Available only
        if `Send Delay Warning Messages` is set to 'Yes' |
        | Maximum Number of Messages to Send | count of messages. Available only
        if `Send Delay Warning Messages` is set to 'Yes' |
        | Alternate Address | email address string. Mandatory if
        `Recipient for Bounce and Warning Messages` is set to 'Alternate' |
        | Recipient for Bounce and Warning Messages | either 'Alternate' or
        'Message sender' |
        | Send Hard Bounce Messages | Either 'Use Default' or 'Yes' or 'No' |
        | Use DSN format for bounce messages | Either 'Use Default' or 'Yes'
        or 'No'. Available only if `Send Hard Bounce Messages` is set to 'Yes' |
        | Parse DSN "Status" field from bounce responses | Either 'Use Default'
        or 'Yes' or 'No' |
        | Send Delay Warning Messages | Either 'Use Default' or 'Yes' or 'No'.
        Available only if `Send Delay Warning Messages` is set to 'Yes' |
        | Use Domain Key Signing for Bounce and Delay Messages | Either
        'Use Default' or 'Yes' or 'No' |
        | Hard Bounce Notification Template | Dictionary containing templates for
        different languages. Key is `language` & value is `template name`.
        Available only if `Use DSN format for bounce messages` is set to 'Yes'.
        Allowed languages are: `Deutsch`, `English`, `Espanol`, `French`,
        `Italian`, `Japanese`, `Korean`, `Portuguese`, `Russian`, `Chinese`,
        `Taiwanese` |
        | Send Delay Notification Template | Dictionary containing templates for
        different languages. Key is `language` & value is `template name`.
        Available only if `Send Delay Warning Messages` is set to 'Yes'.
        Allowed languages are: `Deutsch`, `English`, `Espanol`, `French`,
        `Italian`, `Japanese`, `Korean`, `Portuguese`, `Russian`, `Chinese`,
        `Taiwanese` |

        *Examples:*
        | ${notification_templates}=  Create Dictionary |
        | ... | Deutsch   | System Generated |
		| ... | French    | System Generated |
		| ... | Taiwanese | System Generated |
        | ${my_profile_settings}= | Create Dictionary |
        | ... | Maximum Number of Retries | 100 |
        | ... | Maximum Time in Queue | 25920 |
        | ... | Initial Time to Wait per Message | 60 |
        | ... | Maximum Time to Wait per Message | 25920 |
        | ... | Hard Bounce Message Subject | Delivery Status Notification (Failure) |
        | ... | Send Delay Message Subject | Delivery Status Notification (Delay) |
        | ... | Minimum Interval Between Messages | 14400 |
        | ... | Maximum Number of Messages to Send | 1 |
        | ... | Alternate Address | me@example.com |
        | ... | Recipient for Bounce and Warning Messages | Alternate |
        | ... | Send Hard Bounce Messages | Yes |
        | ... | Use DSN format for bounce messages | Yes |
        | ... | Hard Bounce Notification Template  | ${notification_templates} |
        | ... | Parse DSN "Status" field from bounce responses | Yes |
        | ... | Send Delay Warning Messages | Yes |
        | ... | Use Domain Key Signing for Bounce and Delay Messages | Yes |
        | Bounce Profiles Add | ${my_profile} | ${my_profile_settings} |
        """
        self.click_button(ADD_PROFILE_BUTTON)
        local_settings = copy.copy(settings)
        local_settings.update({'Profile Name': name})
        self._get_bounce_profile_controller(False).set(local_settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def bounce_profiles_edit(self, name, new_settings={}):
        """Edit existing bounce profile settings

        *Parameters:*
        - `name`: name of the existing profile to be edited.
        Also can be equal to 'default'. But in this case all
        radiogrops will not contain the 'Default' setting
        and profile name will be read-only.
        - `settings`: dictionary containing new profile settings.
        All skipped settings will be taken from the Default profile.
        Possible items are:
        | Profile Name | new profile name |
        | Maximum Number of Retries | number of retries between 0 and 10000 |
        | Maximum Time in Queue | number of seconds between 0 and 3000000 |
        | Initial Time to Wait per Message | number of seconds between 60
        and 86400 |
        | Maximum Time to Wait per Message | number of seconds between 60
        and 86400 |
        | Hard Bounce Message Subject | string, message subject. Available only
        if `Use DSN format for bounce messages` is set to 'Yes' |
        | Send Delay Message Subject | string, message subject |
        | Minimum Interval Between Messages | number of seconds. Available only
        if `Send Delay Warning Messages` is set to 'Yes' |
        | Maximum Number of Messages to Send | count of messages. Available only
        if `Send Delay Warning Messages` is set to 'Yes' |
        | Alternate Address | email address string. Mandatory if
        `Recipient for Bounce and Warning Messages` is set to 'Alternate' |
        | Recipient for Bounce and Warning Messages | either 'Alternate' or
        'Message sender' |
        | Send Hard Bounce Messages | Either 'Use Default' or 'Yes' or 'No' |
        | Use DSN format for bounce messages | Either 'Use Default' or 'Yes'
        or 'No'. Available only if `Send Hard Bounce Messages` is set to 'Yes' |
        | Parse DSN "Status" field from bounce responses | Either 'Use Default'
        or 'Yes' or 'No' |
        | Send Delay Warning Messages | Either 'Use Default' or 'Yes' or 'No'.
        Available only if `Send Delay Warning Messages` is set to 'Yes' |
        | Use Domain Key Signing for Bounce and Delay Messages | Either
        'Use Default' or 'Yes' or 'No' |
        | Hard Bounce Notification Template | name of an existing notification
        template. Available only if `Use DSN format for bounce messages` is
        set to 'Yes' |
        | Send Delay Notification Template | name of an existing notification
        template. Available only if `Send Delay Warning Messages` is
        set to 'Yes' |

        *Examples:*
        | Bounce Profiles Edit | default | ${my_profile_settings} |
        """
        if name.lower() == 'default':
            name = 'Default'
        if self._is_element_present(PROFILE_EDIT_LINK(name)):
            self.click_button(PROFILE_EDIT_LINK(name))
        else:
            raise ValueError('There is no bounce profile "%s" ' \
                             'configured on the appliance' % (name,))
        self._get_bounce_profile_controller(name.lower() == 'default').set(
            new_settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def bounce_profiles_delete(self, name):
        """Delete existing bounce profile or all profiles except the default
        one

        *Parameters:*
        - `name`: name of the profile to be removed or 'all' to delete
        all existing profiles except the default one

        *Exceptions:*
        - `ValueError`: if bounce profile with given name doesn't exist

        *Examples:*
        | Bounce Profiles Delete | ${my_profile} |
        """
        if name.lower() == 'all':
            self._select_checkbox(PROFILE_DELETE_ALL_CHECKBOX)
        else:
            if self._is_element_present(PROFILE_DELETE_CHECKBOX(name)):
                self._select_checkbox(PROFILE_DELETE_CHECKBOX(name))
            else:
                raise ValueError('There is no bounce profile "%s" ' \
                                 'configured on the appliance' % (name,))
        self.click_button(PROFILES_DELETE_BUTTON, 'don\'t wait')
        self._click_continue_button()

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def bounce_profiles_get_all(self):
        """Get names of all configured bounce profiles (including default)

        *Return:*
        List of configured bounce profile names

        *Examples:*
        | @{all_profiles}= | Bounce Profiles Get All |
        | List Should Contain Value | ${all_profiles} | ${my_profile} |
        """
        profiles_count = int(self.get_matching_xpath_count(PROFILE_NAME_CELLS))
        result = []
        for idx in xrange(1, 1 + profiles_count):
            result.append(self.get_text(PROFILE_NAME_CELL_BY_IDX(idx)).strip())
        return result

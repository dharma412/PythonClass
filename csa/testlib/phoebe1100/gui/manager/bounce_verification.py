#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/manager/bounce_verification.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import go_to_page
from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

from bounce_verification_def.bounce_verification_settings import BVSettings
from bounce_verification_def.tagging_keys import TaggingKeyAddForm, TaggingKeyPurgeForm

EDIT_SETTINGS_BUTTON = "//input[@value='Edit Settings']"

KEYS_TABLE = "//table[@class='cols']"
ALL_KEYS = "%s/tbody/tr/td[1]" % (KEYS_TABLE,)
# idx starts from 1
KEY_BY_IDX = lambda idx: "%s/tbody/tr[td][%d]/td[1]" % (KEYS_TABLE, idx)
NEW_KEY_BUTTON = "//input[@value='New Key...']"
CLEAR_KEYS_BUTTON = "//input[@id='clearall']"
PURGE_KEYS_BUTTON = "//input[@id='purge_button_id']"
PURGE_KEYS_BUTTON_DISABLED = "//input[@id='purge_button_id' and @disabled]"
CANCEL_BUTTON = "//input[@value='Cancel']"

PAGE_PATH = ('Mail Policies', 'Bounce Verification')


class BounceVerification(GuiCommon):
    """Keywords for GUI interaction with Mail Policies ->
    Bounce Verification page. The corresponding Bounce Verification
    feature key has to be installed on an appliance in order to work
    with the Bounce Verification functionality.
    """

    def get_keyword_names(self):
        return ['bounce_verification_edit_settings',
                'bounce_verification_get_settings',

                'bounce_verification_add_key',
                'bounce_verification_purge_keys',
                'bounce_verification_clear_all_keys',
                'bounce_verification_get_all_keys']

    def _get_bv_settings_controller(self):
        if not hasattr(self, '_bv_settings_controller'):
            self._bv_settings_controller = BVSettings(self)
        return self._bv_settings_controller

    def _get_add_key_form_controller(self):
        if not hasattr(self, '_add_key_form_controller'):
            self._add_key_form_controller = TaggingKeyAddForm(self)
        return self._add_key_form_controller

    def _get_purge_key_form_controller(self):
        if not hasattr(self, '_purge_key_form_controller'):
            self._purge_key_form_controller = TaggingKeyPurgeForm(self)
        return self._purge_key_form_controller

    @go_to_page(PAGE_PATH)
    def bounce_verification_edit_settings(self, settings={}):
        """Edit Bounce Verification settings

        *Parameters:*
        - `settings`: non mandatory dictionary. Items can be:
        | Action when invalid bounce message received | either 'Reject' or
        'Add custom header and deliver' |
        | Header Name | custom header name. Mandatory only if
        'Action when invalid bounce message received' is set to
        'Add custom header and deliver' |
        | Header Content | custom header content. Mandatory only if
        'Action when invalid bounce message received' is set to
        'Add custom header and deliver' |
        | Smart Exceptions to tagging | whether to apply the "Smart Exceptions"
        feature to tagging. Either ${True} or ${False} |

        *Examples:*
        | ${new_settings}= | Create Dictionary |
        | ... | Action when invalid bounce message received |
        | ... | Add custom header and deliver |
        | ... | Header Name | ${custom_header_name} |
        | ... | Header Content | some content |
        | ... | Smart Exceptions to tagging | ${False} |
        | Bounce Verification Edit Settings | ${new_settings |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)

        self._get_bv_settings_controller().set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def bounce_verification_get_settings(self):
        """Get current Bounce Verification settings

        *Return:*
        - dictionary whose items are:
        | Action when invalid bounce message received | either 'Reject' or
        'Add custom header and deliver' |
        | Header Name | custom header name. This item is present only if
        'Action when invalid bounce message received' is set to
        'Add custom header and deliver' |
        | Header Content | custom header content. This item is present only if
        'Action when invalid bounce message received' is set to
        'Add custom header and deliver' |
        | Smart Exceptions to tagging | whether the "Smart Exceptions" feature
        is applied to tagging. Either ${True} or ${False} |

        *Examples:*
        | ${result}= | Bounce Verification Get Settings |
        | Log Dictionary | ${result} |
        | ${hname}= | Get From Dictionary | ${result} | Header Name |
        | Should be Equal | ${hname} | ${custom_header_name} |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)

        result = self._get_bv_settings_controller().get()
        self.click_button(CANCEL_BUTTON)
        return result

    @go_to_page(PAGE_PATH)
    def bounce_verification_add_key(self, new_key):
        """Add address tagging key to BV

        *Parameters:*
        - `new_key`: an arbitrary string for a new tag

        *Examples:*
        | ${my_key}= | Set Variable | blabla |
        | Bounce Verification Add Key | ${my_key} |
        """
        self.click_button(NEW_KEY_BUTTON)

        self._get_add_key_form_controller().set(
            {'Address Tagging Key': new_key})
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def bounce_verification_purge_keys(self, option=None):
        """Purge tag keys from Bounce Verification

        *Parameters:*
        - `option`: non mandatory string, purge option. Can be one of
        | Not used in one month |
        | Not used in one year |
        | All except current key |
        Default value is the 'Not used in one month'.

        *Exceptions:*
        - `ConfigError`: if there are no Tagging Keys available for
        purge operation

        *Examples:*
        | Bounce Verification Purge Keys | All except current key |
        """
        if not self._is_element_present(PURGE_KEYS_BUTTON) or \
                self._is_element_present(PURGE_KEYS_BUTTON_DISABLED):
            raise guiexceptions.ConfigError('There are no Tagging Keys ' \
                                            'available for purge operation')
        if option is not None:
            settings = {'Option': option}
        else:
            settings = {}
        self._get_purge_key_form_controller().set(settings)
        self.click_button(PURGE_KEYS_BUTTON, 'don\'t wait')
        self._click_continue_button()

    @go_to_page(PAGE_PATH)
    def bounce_verification_clear_all_keys(self):
        """Clear all tag keys from Bounce Verification

        *Exceptions:*
        - `ConfigError`: if there are no Tagging Keys
        configured for Bounce Verification

        *Examples:*
        | Bounce Verification Clear All Keys |
        """
        if self._is_element_present(CLEAR_KEYS_BUTTON):
            self.click_button(CLEAR_KEYS_BUTTON)
        else:
            raise guiexceptions.ConfigError('There are no Tagging Keys ' \
                                            'configured for Bounce Verification')

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def bounce_verification_get_all_keys(self):
        """Get all tag keys configured in BV

        *Return:*
        List of strings. Will return an empty list if
        there are no keys configured in BV

        *Examples:*
        | @{all_keys}= | Bounce Verification Get All Keys |
        | List Should Contain Value | ${all_keys} | ${my_key} |
        """
        result = []
        keys_count = int(self.get_matching_xpath_count(ALL_KEYS))
        for key_idx in xrange(1, 1 + keys_count):
            result.append(self.get_text(KEY_BY_IDX(key_idx)).strip())
        return result

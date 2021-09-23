#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/network/incoming_relays.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import functools

from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

from incoming_relays_def.incoming_relay_settings import IncomingRelaySettings

ENABLE_BUTTON = "//input[@type='button' and @value='Enable']"
DISABLE_BUTTON = "//input[@type='button' and @value='Disable']"

ADD_RELAY_BUTTON = "//input[@value='Add Relay...']"
PARENT_TABLE = "//table[@class='cols']"
EDIT_RELAY_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                               (PARENT_TABLE, name)
DELETE_RELAY_LINK = lambda name: \
    "%s//td[.//a[normalize-space()='%s']]/following-sibling::td[5]/img" % \
    (PARENT_TABLE, name)

PAGE_PATH = ('Network', 'Incoming Relays')


def verify_feature_is_enabled(func):
    @functools.wraps(func)
    def decorator(self, *args, **kwargs):
        if not self.incoming_relays_is_enabled():
            raise guiexceptions.ConfigError('Incoming Relays feature should ' \
                                            'be enabled in order to use this keyword')
        return func(self, *args, **kwargs)

    return decorator


class IncomingRelays(GuiCommon):
    """Keywords for interaction with ESA GUI Network->
    Incoming Relays page
    """

    def get_keyword_names(self):
        return ['incoming_relays_is_enabled',
                'incoming_relays_enable',
                'incoming_relays_disable',

                'incoming_relays_add',
                'incoming_relays_edit',
                'incoming_relays_delete']

    def _get_settings_controller(self):
        if not hasattr(self, '_settings_controller'):
            self._settings_controller = IncomingRelaySettings(self)
        return self._settings_controller

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def incoming_relays_is_enabled(self):
        """Return current Incoming Relays feature state

        *Return:*
        ${True} if Incoming Relays feature is enabled or
        ${False} otherwise

        *Examples:*
        | ${state}= | Incoming Relays Is Enabled |
        """
        return self._is_element_present(DISABLE_BUTTON)

    @set_speed(0)
    def incoming_relays_enable(self):
        """Enable Incoming Relays feature. Keyword will
        be silently ignored if Incoming Relays feature
        is already enabled.

        *Examples:*
        | ${state}= | Incoming Relays Is Enabled |
        | Run Keyword If | not ${state} |
        | ... | Incoming Relays Enable |
        """
        if self.incoming_relays_is_enabled():
            return
        self.click_button(ENABLE_BUTTON)
        self._check_action_result()

    @set_speed(0)
    def incoming_relays_disable(self):
        """Disable Incoming Relays feature. Keyword will
        be silently ignored if Incoming Relays feature
        is already disabled.

        *Examples:*
        | ${state}= | Incoming Relays Is Enabled |
        | Run Keyword If | ${state} |
        | ... | Incoming Relays Disable |
        """
        if not self.incoming_relays_is_enabled():
            return
        self.click_button(DISABLE_BUTTON)
        self._check_action_result()

    @set_speed(0)
    @verify_feature_is_enabled
    def incoming_relays_add(self, name, settings):
        """Add new incoming relay

        *Parameters:*
        - `name`: name of new incoming relay to be added
        - `settings`: dictionary containing new relay settings.
        Possible items are:
        | `IP Address` | incoming relay IP address, mandatory |
        | `Header` | can be 'Custom header' or 'Parse the "Received" header' |
        | `Custom Header` | custom message header. Available if `Header` is set
        to 'Custom header' |
        | `Begin parsing after` | the special character or string after which
        to begin parsing for the originating IP address. Available if
        'Header` is set to 'Parse the "Received" header' |
        | `Hop` | the position of the "Received:" header that contains the
        originating IP address. Number from 1 to 50 |

        *Exceptions:*
        - `ConfigError`: if Incoming Relays feature is disabled

        *Examples:*
        | ${relay2_settings}= | Create Dictionary |
        | ... | IP Address | 2.2.2.2 |
        | ... | Header | Parse the "Received" header |
        | ... | Begin parsing after | from |
        | ... | Hop | 2 |
        | Incoming Relays Add | ${relay2_name} | ${relay2_settings} |
        """
        self.click_button(ADD_RELAY_BUTTON)
        controller = self._get_settings_controller()
        settings.update({'Name': name})
        controller.set(settings)
        self._click_submit_button()

    @set_speed(0)
    @verify_feature_is_enabled
    def incoming_relays_edit(self, name, settings={}):
        """Edit existing incoming relay

        *Parameters:*
        - `name`: name of existing incoming relay to be edited
        - `settings`: dictionary containing new relay settings.
        Possible items are:
        | `Name` | new relay name |
        | `IP Address` | incoming relay IP address, mandatory |
        | `Header` | can be 'Custom header' or 'Parse the "Received" header' |
        | `Custom Header` | custom message header. Available if `Header` is set
        to 'Custom header' |
        | `Begin parsing after` | the special character or string after which
        to begin parsing for the originating IP address. Available if
        'Header` is set to 'Parse the "Received" header' |
        | `Hop` | the position of the "Received:" header that contains the
        originating IP address. Number from 1 to 50 |

        *Exceptions:*
        - `ConfigError`: if Incoming Relays feature is disabled
        - `ValueError`: if Incoming Relay with given name does not exist

        *Examples:*
        | ${relay1_settings}= | Create Dictionary |
        | ... | Name | bla |
        | ... | IP Address | 1.1.1.1 |
        | ... | Header | Custom header |
        | ... | Custom Header | X-my-header |
        | Incoming Relays Edit | existing_relay | ${relay2_settings} |
        """
        if not self._is_element_present(EDIT_RELAY_LINK(name)):
            raise ValueError('There is no incoming relay named "%s"' % \
                             (name,))
        self.click_button(EDIT_RELAY_LINK(name))
        controller = self._get_settings_controller()
        controller.set(settings)
        self._click_submit_button()

    def _get_existing_relay_names(self):
        result = []
        all_names = "%s/tbody/tr[.//a]" % (PARENT_TABLE,)
        all_names_count = int(self.get_matching_xpath_count(all_names))
        # row_idx starts from 1
        relay_name_cell = lambda row_idx: "%s[%d]/td/a" % \
                                          (all_names, row_idx)
        for row_idx in xrange(1, all_names_count + 1):
            result.append(self.get_text(relay_name_cell(row_idx)).strip())
        return result

    @set_speed(0)
    @verify_feature_is_enabled
    def incoming_relays_delete(self, name):
        """Delete existing incoming relay(s)

        *Parameters:*
        - `name`: name of existing incoming relay to be deleted or 'all'
        to delete all existing relays

        *Exceptions:*
        - `ConfigError`: if Incoming Relays feature is disabled
        - `ValueError`: if Incoming Relay with given name does not exist

        *Examples:*
        | Incoming Relays Delete | all |
        """
        if name.lower() == 'all':
            relay_names = self._get_existing_relay_names()
        else:
            relay_names = (name,)
        for relay_name in relay_names:
            if not self._is_element_present(DELETE_RELAY_LINK(relay_name)):
                raise ValueError('There is no incoming relay named "%s"' % \
                                 (name,))
            self.click_button(DELETE_RELAY_LINK(relay_name), 'don\'t wait')
            self._click_continue_button()

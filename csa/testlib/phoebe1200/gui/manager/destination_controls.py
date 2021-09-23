#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/manager/destination_controls.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import copy

from common.gui.decorators import go_to_page
from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon

from destination_controls_def.destination_controls_settings import \
    DestinationControlsSettings
from destination_controls_def.destination_profile import \
    DestinationProfileSettings, DefaultDestinationProfileSettings

EDIT_SETTINGS_BUTTON = "//input[@name='EditGlobalForm']"

ADD_PROFILE_BUTTON = "//input[@value='Add Destination...']"
PROFILES_TABLE = "//table[@class='cols']"
PROFILE_NAME_CELLS = "%s/tbody/tr[td]" % (PROFILES_TABLE,)
# idx starts from 1
PROFILE_NAME_CELL_BY_IDX = lambda idx: "%s/tbody/tr[td][%d]/td[1]" % \
                                       (PROFILES_TABLE, idx)
PROFILE_EDIT_LINK = lambda name: "%s//td/a[normalize-space()='%s']" % \
                                 (PROFILES_TABLE, name)
PROFILE_DELETE_CHECKBOX = lambda name: "%s//td[normalize-space()='%s']" \
                                       "/following-sibling::td[6]/input" % \
                                       (PROFILES_TABLE, name)
PROFILE_DELETE_BUTTON = "//input[@name='delete']"
PROFILE_DELETE_ALL_CHECKBOX = "//input[@name='delete_all']"

PAGE_PATH = ('Mail Policies', 'Destination Controls')


class DestinationControls(GuiCommon):
    """Keywords for GUI interaction with Mail Policies ->
    Destination Controls page.
    """

    def get_keyword_names(self):
        return ['destination_controls_edit_settings',

                'destination_controls_add',
                'destination_controls_edit',
                'destination_controls_delete',
                'destination_controls_get_all']

    def _get_destination_controls_settings_controller(self):
        if not hasattr(self, '_destination_controls_settings_controller'):
            self._destination_controls_settings_controller = \
                DestinationControlsSettings(self)
        return self._destination_controls_settings_controller

    def _get_destination_profile_controller(self, is_default):
        if is_default:
            if not hasattr(self, '_default_destination_profile_controller'):
                self._default_destination_profile_controller = \
                    DefaultDestinationProfileSettings(self)
            return self._default_destination_profile_controller
        else:
            if not hasattr(self, '_destination_profile_controller'):
                self._destination_profile_controller = \
                    DestinationProfileSettings(self)
            return self._destination_profile_controller

    @go_to_page(PAGE_PATH)
    def destination_controls_edit_settings(self, settings):
        """Edit Destination Controls global settings

        *Parameters:*
        - `settings`: dictionary whose items can be:
        | Certificate | existing system certificate name |
        | Send an alert when a required TLS connection fails | boolean,
        either ${True} or ${False} |

        *Examples:*
        | ${new_settings}= | Create Dictionary |
        | ... | Certificate | System Default |
        | ... | Send an alert when a required TLS connection fails | ${False} |
        | Destination Controls Edit Settings | ${new_settings} |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)
        self._get_destination_controls_settings_controller().set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def destination_controls_add(self, destination, settings={}):
        """Add a new profile to Destination Controls

        *Parameters:*
        - `destination:` valid domain name (suffix) or IP address
        - `settings`: dictionary whose items can be:
        | IP Address Preference  | Either 'IPv6 Preferred' or
        'IPv6 Required' or 'IPv4 Preferred' or 'IPv4 Required' |
        | Concurrent Connections Limit | Either 'Use Default' or
        'Custom' |
        | Concurrent Connections | number of concurrent connection
        between 1 and 1,000. Available only of 'Concurrent Connections Limit'
        is set to 'Custom' |
        | Maximum Messages Per Connection Limit | Either 'Use Default' or
        'Custom' |
        | Maximum Messages Per Connection | number of messages per connection.
        (between 1 and 1,000). Available if 'Maximum Messages Per Connection
        Limit' is set to 'Custom' |
        | Recipients Limit | Either 'Use Default' or 'Custom' |
        | Recipients | max number of recipient per time period,
        (between 0 and 1,000,000,000). Available only if 'Recipients Limit'
        is set to 'Custom' |
        | Recipient Minutes | period duration in minutes (between 1 and 60) |
        | Apply Limits Per Destination | Either 'Entire Domain' or
        'Each Mail Exchanger (MX Record) IP address' |
        | Apply Limits Per ESA Hostname | Either 'System Wide' or
        'Each Virtual Gateway' |
        | TLS Support | Either 'Preferred' or 'Required' or 'Preferred - Verify'
        or 'Required - Verify' |
        | Dane Support | Either 'Opportunistic' or 'Mandatory' |
        | Bounce Verification | Either 'Use Default' or 'Yes' or 'No' |
        | Bounce Profile | name of an existing bounce profile |

        *Examples:*
        | ${my_profile}= | Set Variable | 1.1.1.1 |
        | ${my_profile_settings}= | Create Dictionary |
        | ... | IP Address Preference | IPv4 Preferred |
        | ... | Concurrent Connections Limit | Custom |
        | ... | Concurrent Connections | 501 |
        | ... | Maximum Messages Per Connection Limit | Custom |
        | ... | Maximum Messages Per Connection | 51 |
        | ... | Recipients Limit | Custom |
        | ... | Recipients | 1000 |
        | ... | Recipient Minutes | 59 |
        | ... | Apply Limits Per Destination | Entire Domain |
        | ... | Apply Limits Per ESA Hostname | System Wide |
        | ... | TLS Support | Preferred |
        | ... | Dane Support | Mandatory |
        | ... | Bounce Verification | No |
        | Destination Controls Add | ${my_profile} | ${my_profile_settings} |
        """
        self.click_button(ADD_PROFILE_BUTTON)
        local_settings = copy.copy(settings)
        local_settings.update({'Destination': destination})
        self._get_destination_profile_controller(False).set(local_settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def destination_controls_edit(self, destination, new_settings={}):
        """Edit existing profile settings in Destination Controls

        *Parameters:*
        - `destination:` valid existing destination profile or 'default'
        to edit the Default profile. If destination is an IP address
        then it will be automatically converted into the appropriate
        form (surrounded with '[]')
        - `settings`: dictionary whose items can be:
        | Destination | valid domain name (suffix) or IP address |
        | IP Address Preference  | Either 'IPv6 Preferred' or
        'IPv6 Required' or 'IPv4 Preferred' or 'IPv4 Required' |
        | Concurrent Connections Limit | Either 'Use Default' or
        'Custom' |
        | Concurrent Connections | number of concurrent connection
        between 1 and 1,000. Available only of 'Concurrent Connections Limit'
        is set to 'Custom' |
        | Maximum Messages Per Connection Limit | Either 'Use Default' or
        'Custom' |
        | Maximum Messages Per Connection | number of messages per connection.
        (between 1 and 1,000). Available if 'Maximum Messages Per Connection
        Limit' is set to 'Custom' |
        | Recipients Limit | Either 'Use Default' or 'Custom' |
        | Recipients | max number of recipient per time period,
        (between 0 and 1,000,000,000). Available only if 'Recipients Limit'
        is set to 'Custom' |
        | Recipient Minutes | period duration in minutes (between 1 and 60) |
        | Apply Limits Per Destination | Either 'Entire Domain' or
        'Each Mail Exchanger (MX Record) IP address' |
        | Apply Limits Per ESA Hostname | Either 'System Wide' or
        'Each Virtual Gateway' |
        | TLS Support | Either 'Preferred' or 'Required' or 'Preferred - Verify'
        or 'Required - Verify' |
        | Dane Support | Either 'Opportunistic' or 'Mandatory' |
        | Bounce Verification | Either 'Use Default' or 'Yes' or 'No' |
        | Bounce Profile | name of an existing bounce profile |
        For the Default profile there are no 'Use Default' value and also
        the 'Destination' item is unavailable

        *Exceptions:*
        - `ValueError`: if there is no profile with given name

        *Examples:*
        | ${def_settings}= | Create Dictionary |
        | ... | Recipients Limit | No Limit |
        | ... | Bounce Verification | Yes |
        | Destination Controls Edit | default | ${def_settings} |
        """
        if destination.lower() == 'default':
            destination = 'Default'
        if self._is_element_present(PROFILE_EDIT_LINK(destination)):
            self.click_button(PROFILE_EDIT_LINK(destination))
        elif self._is_element_present(PROFILE_EDIT_LINK("[%s]" % (destination,))):
            # IP address can be escaped
            self.click_button(PROFILE_EDIT_LINK("[%s]" % (destination,)))
        else:
            raise ValueError('There is no destination "%s" ' \
                             'configured on the appliance' % (destination,))
        self._get_destination_profile_controller(destination.lower() == \
                                                 'default').set(new_settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def destination_controls_delete(self, destination):
        """Delete existing Destination Controls profile or all profiles except
        the default one

        *Parameters:*
        - `destination`: valid existing destination profile. If destination
        is an IP address then it will be automatically converted into the
        appropriate form (surrounded with '[]'). Also, can be 'all' in order
        to delete all custom profiles

        *Exceptions:*
        - `ValueError`: if there is no profile with given name

        *Examples:*
        | Destination Controls Delete | ${my_profile} |
        """
        if destination.lower() == 'all':
            self._select_checkbox(PROFILE_DELETE_ALL_CHECKBOX)
        elif self._is_element_present(PROFILE_DELETE_CHECKBOX(destination)):
            self._select_checkbox(PROFILE_DELETE_CHECKBOX(destination))
        elif self._is_element_present(PROFILE_DELETE_CHECKBOX("[%s]" % \
                                                              (destination,))):
            # IP address can be escaped
            self._select_checkbox(PROFILE_DELETE_CHECKBOX("[%s]" % \
                                                          (destination,)))
        else:
            raise ValueError('There is no destination "%s" ' \
                             'configured on the appliance' % (destination,))
        self.click_button(PROFILE_DELETE_BUTTON, 'don\'t wait')
        self._click_continue_button()

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def destination_controls_get_all(self):
        """Get names of all profiles configured in Destination Controls
        (including default)

        *Return:*
        List of all existing destination profiles. In case there are no
        custom profiles configured then 1-element list containing the Default
        profile will be returned. Special surrounding symbols for IP addresses
        ('[]') ill be stripped from names

        *Examples:*
        | @{all_profiles}= | Destination Controls Get All |
        | List Should Contain Value | ${all_profiles} | ${my_profile} |
        """
        profiles_count = int(self.get_matching_xpath_count(PROFILE_NAME_CELLS))
        return map(lambda idx: \
                       self.get_text(PROFILE_NAME_CELL_BY_IDX(idx)).strip().strip('[').strip(']'),
                   xrange(1, 1 + profiles_count))

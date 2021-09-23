#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/manager/dmarc.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
from common.util.ordered_dict import OrderedDict

from dmarc_def.dmarc_profile import DMARCProfile, PROFILE_NAME
from dmarc_def.dmarc_settings import DMARCSettings
from dmarc_def.export_form import ExportForm, FILE_TO_EXPORT
from dmarc_def.import_form import ImportForm, FILE_TO_IMPORT_LIST

ADD_PROFILE_BUTTON = "//input[@value='Add Profile...']"
EDIT_SETTINGS_BUTTON = "//input[@value='Edit Global Settings...']"
CANCEL_BUTTON = "//input[@value='Cancel']"
IMPORT_BUTTON = "//input[@value='Import Profiles...']"
EXPORT_BUTTON = "//input[@value='Export Profiles...']"

PROFILES_TABLE = "//table[@class='cols']"
ALL_ROWS = "{0}//tr[td]".format(PROFILES_TABLE)
PROFILE_EDIT_LINK = lambda name: "{0}/td[1]//a[normalize-space()='{1}']". \
    format(ALL_ROWS, name)
DELETE_ALL_CHECKBOX = "//input[@name='del_0']"
PROFILE_DELETE_CHECKBOX = lambda name: "{0}/td[.//a[normalize-space()='{1}']]" \
                                       "/following-sibling::td[5]/input". \
    format(ALL_ROWS, name)
CELL_BY_ROW_COL = lambda row_idx, col_idx: "{0}[{1}]/td[{2}]". \
    format(ALL_ROWS, row_idx, col_idx)
DELETE_BUTTON = "//input[@id='delete']"

PROFILE_INFO_MAPPING = [('Profile Name', 1),
                        ('Reject Message Action', 2),
                        ('Quarantine Message Action', 3),
                        ('SMTP Action For Temporary Failure', 4),
                        ('SMTP Action For Permanent Failure', 5)]

SHOW_ITEMS_COMBO = "//select[@id='pageSize']"
SELECTED_ITEMS_COUNT = "{0}/option[@selected]".format(SHOW_ITEMS_COMBO)

PAGE_PATH = ('Mail Policies', 'DMARC')


class DMARC(GuiCommon):
    """Keywords for GUI interaction with Mail Policies -> DMARC page"""

    def get_keyword_names(self):
        return ['dmarc_edit_settings',
                'dmarc_get_settings',

                'dmarc_add_profile',
                'dmarc_is_profile_exist',
                'dmarc_edit_profile',
                'dmarc_delete_profile',
                'dmarc_get_profiles',

                'dmarc_import_profiles',
                'dmarc_export_profiles']

    def _get_cached_controller(self, cls, *args, **kwargs):
        attr_name = '_{0}'.format(cls.__name__.lower())
        if not hasattr(self, attr_name):
            setattr(self, attr_name, cls(self, *args, **kwargs))
        return getattr(self, attr_name)

    def _set_max_visible_profiles_count(self, count_per_page):
        if unicode(count_per_page).lower() == 'all':
            count_per_page = 'All'
        else:
            count_per_page = unicode(count_per_page)
        if self._is_element_present(SELECTED_ITEMS_COUNT) and \
                self.get_text(SELECTED_ITEMS_COUNT).strip() != count_per_page:
            self.select_from_list(SHOW_ITEMS_COMBO, count_per_page)
            self.wait_until_page_loaded()

    @go_to_page(PAGE_PATH)
    def dmarc_edit_settings(self, settings):
        """Edit global DMARC settings

        *Parameters:*
        - `settings`: dictionary containing global DMARC settings
        to be applied. Available settings are:
        | Specific senders bypass address list | Name of existing address list.
        'None' by default |
        | Bypass verification for messages with headers | Comma separated
        list of message headers |
        | Schedule for report generation | Time string in format HH:MM AM/PM |
        | Entity generating reports | String |
        | Additional contact information | String |
        | Send copy of all aggregate reports to | comma separated list of email
        addresses |
        | Send delivery error reports | Whether to send delivery error reports.
        Either ${True} or ${False} |

        *Examples:*
        | ${scheduled_time}= | Set Variable | 11:30 PM |
        | ${new_settings}= | Create Dictionary |
        | ... | Specific senders bypass address list | None |
        | ... | Bypass verification for messages with headers | X-Bypass-DMARC, X-Some-Header |
        | ... | Schedule for report generation | ${scheduled_time} |
        | ... | Entity generating reports | blabla |
        | ... | Additional contact information | blabla |
        | ... | Send copy of all aggregate reports to | blabla@example.com |
        | ... | Send delivery error reports | ${True} |
        | DMARC Edit Settings | ${new_settings} |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)

        controller = self._get_cached_controller(DMARCSettings)
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def dmarc_get_settings(self):
        """Get current global DMARC settings

        *Return:*
        - Dictionary. See the list of available parameters for `DMARC Edit Settings`
        keyword for more details

        *Examples:*
        | ${scheduled_time}= | Set Variable | 11:30 PM |
        | ${result}= | DMARC Get Settings |
        | Log Dictionary | ${result} |
        | Should Be Equal As Strings | ${scheduled_time} |
        | ... | ${result['Schedule for report generation']} |
        """
        self.click_button(EDIT_SETTINGS_BUTTON)

        controller = self._get_cached_controller(DMARCSettings)
        result = controller.get()
        self.click_button(CANCEL_BUTTON)
        return result

    @go_to_page(PAGE_PATH)
    def dmarc_add_profile(self, name, settings):
        """Add new DMARC verification profile

        *Parameters:*
        - `name`: the name of a profile to be added
        - `settings`: dictionary. Available items are:
        | Message action when DMARC policy is reject | Either 'No Action' (default),
        'Quarantine' or 'Reject' |
        | Reject Policy Quarantine Name | The name of existing system quarantine.
        Available if `Message action when DMARC policy is reject` is set to
        'Quarantine' |
        | Reject SMTP Code | Code number. Available if
        `Message action when DMARC policy is reject` is set to 'Reject' |
        | Reject SMTP Response | Response string. Available if
        `Message action when DMARC policy is reject` is set to 'Reject' |
        | Message action when DMARC policy is quarantine | Either 'No Action' (default),
        'Quarantine' or 'Reject' |
        | Quarantine Policy Quarantine Name | The name of existing system quarantine.
        Available if `Message action when DMARC policy is quarantine` is set to
        'Quarantine' |
        | Message action in case of temporary failure | Either 'Accept' (default)
        or 'Reject' |
        | Temporary Failure SMTP Code | Code number. Available if
        `Message action in case of temporary failure` is set to 'Reject' |
        | Temporary Failure SMTP Response | Response string. Available if
        `Message action in case of temporary failure` is set to 'Reject' |
        | Message action in case of permanent failure | Either 'Accept' (default)
        or 'Reject' |
        | Permanent Failure SMTP Code | Code number. Available if
        `Message action in case of permanent failure` is set to 'Reject' |
        | Permanent Failure SMTP Response | Response string. Available if
        `Message action in case of permanent failure` is set to 'Reject' |

        *Examples:*
        | ${profile_settings}= | Create Dictionary |
        | ... | Message action when DMARC policy is reject | Quarantine |
        | ... | Reject Policy Quarantine Name | Policy |
        | ... | Message action when DMARC policy is quarantine | Quarantine |
        | ... | Quarantine Policy Quarantine Name | Policy |
        | ... | Message action in case of temporary failure | Reject |
        | ... | Temporary Failure SMTP Code | 451 |
        | ... | Temporary Failure SMTP Response | \\#4.7.1 Unable to perform DMARC verification. |
        | ... | Permanent Failure SMTP Code | 550 |
        | ... | Permanent Failure SMTP Response | \\#5.7.1 DMARC verification failed. |
        | DMARC Add Profile | ${PROFILE_NAME} | ${profile_settings} |
        """
        self.click_button(ADD_PROFILE_BUTTON)

        controller = self._get_cached_controller(DMARCProfile)
        settings[PROFILE_NAME[0]] = name
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def dmarc_is_profile_exist(self, name, count_per_page='All'):
        """Check whether DMARC verification profile exists on appliance

        *Parameters:*
        - `name`: the name of a profile
        - `count_per_page`: maximum count of visible items per current page.
        Available values are:
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        | All |
        'All' by default.

        *Return:*
        - ${True} or ${False}

        *Examples:*
        | DMARC Add Profile | ${PROFILE_NAME} | ${profile_settings} |
        | ${is_exist}= | DMARC Is Profile Exist | ${PROFILE_NAME} | 20 |
        | Should Be True | ${is_exist} |
        """
        self._set_max_visible_profiles_count(count_per_page)
        return self._is_element_present(PROFILE_EDIT_LINK(name))

    @go_to_page(PAGE_PATH)
    def dmarc_edit_profile(self, name, settings, count_per_page='All'):
        """Edit existing DMARC verification profile

        *Parameters:*
        - `name`: the name of an existing profile to be edited
        - `settings`: dictionary. Available items are:
        | Profile Name | new profile name |
        | Message action when DMARC policy is reject | Either 'No Action' (default),
        'Quarantine' or 'Reject' |
        | Reject Policy Quarantine Name | The name of existing system quarantine.
        Available if `Message action when DMARC policy is reject` is set to
        'Quarantine' |
        | Reject SMTP Code | Code number. Available if
        `Message action when DMARC policy is reject` is set to 'Reject' |
        | Reject SMTP Response | Response string. Available if
        `Message action when DMARC policy is reject` is set to 'Reject' |
        | Message action when DMARC policy is quarantine | Either 'No Action' (default),
        'Quarantine' or 'Reject' |
        | Quarantine Policy Quarantine Name | The name of existing system quarantine.
        Available if `Message action when DMARC policy is quarantine` is set to
        'Quarantine' |
        | Message action in case of temporary failure | Either 'Accept' (default)
        or 'Reject' |
        | Temporary Failure SMTP Code | Code number. Available if
        `Message action in case of temporary failure` is set to 'Reject' |
        | Temporary Failure SMTP Response | Response string. Available if
        `Message action in case of temporary failure` is set to 'Reject' |
        | Message action in case of permanent failure | Either 'Accept' (default)
        or 'Reject' |
        | Permanent Failure SMTP Code | Code number. Available if
        `Message action in case of permanent failure` is set to 'Reject' |
        | Permanent Failure SMTP Response | Response string. Available if
        `Message action in case of permanent failure` is set to 'Reject' |
        - `count_per_page`: maximum count of visible items per current page.
        Available values are:
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        | All |
        'All' by default.

        *Exceptions:*
        - `ValueError`: if profile having given name does not exist

        *Examples:*
        | ${changed_settings}= | Create Dictionary |
        | ... | Message action in case of temporary failure | Accept |
        | DMARC Edit Profile | ${PROFILE_NAME} | ${changed_settings} |
        """
        self._set_max_visible_profiles_count(count_per_page)
        if not self._is_element_present(PROFILE_EDIT_LINK(name)):
            raise ValueError('DMARC verification profile "{0}" does not exist'. \
                             format(name))
        self.click_button(PROFILE_EDIT_LINK(name))
        controller = self._get_cached_controller(DMARCProfile)
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def dmarc_delete_profile(self, name, count_per_page='All'):
        """Delete existing DMARC verification profile

        *Parameters:*
        - `name`: the name of an existing profile to be edited or
        'all' to delete all existing profiles
        - `count_per_page`: maximum count of visible items per current page.
        Available values are:
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        | All |
        'All' by default.

        *Exceptions:*
        - `ValueError`: if profile having given name does not exist

        *Examples:*
        | DMARC Delete Profile | All |
        | ${info}= | DMARC Get Profiles |
        | Should Be Empty | ${info} |
        """
        self._set_max_visible_profiles_count(count_per_page)
        if name.lower() == 'all':
            self._select_checkbox(DELETE_ALL_CHECKBOX)
        else:
            if not self._is_element_present(PROFILE_DELETE_CHECKBOX(name)):
                raise ValueError('DMARC verification profile "{0}" does not exist'. \
                                 format(name))
            self._select_checkbox(PROFILE_DELETE_CHECKBOX(name))
        self.click_button(DELETE_BUTTON, 'don\'t wait')
        self._click_continue_button()

    @go_to_page(PAGE_PATH)
    def dmarc_get_profiles(self, count_per_page='All'):
        """Get info about all existing DMARC verification profiles

        *Parameters:*
        - `count_per_page`: maximum count of visible items per current page.
        Available values are:
        | 20 |
        | 50 |
        | 100 |
        | 250 |
        | All |
        'All' by default.

        *Return:*
        - Ordered dictionary. Available keys are:
        | Profile Name |
        | Reject Message Action |
        | Quarantine Message Action  |
        | SMTP Action For Temporary Failure |
        | SMTP Action For Permanent Failure |

        Values are lists of cell values in corresponding columns

        *Examples:*
        | ${info}= | DMARC Get Profiles | All |
        | Log Dictionary | ${info} |
        | List Should Contain Value | ${info['Profile Name']} | ${PROFILE_NAME} |
        """
        self._set_max_visible_profiles_count(count_per_page)
        result = OrderedDict()
        profiles_count = int(self.get_matching_xpath_count(ALL_ROWS))
        for row_idx in xrange(1, 1 + profiles_count):
            for key, col_idx in PROFILE_INFO_MAPPING:
                value = self.get_text(CELL_BY_ROW_COL(row_idx, col_idx)).strip()
                if key in result:
                    result[key].append(value)
                else:
                    result[key] = [value]
        return result

    @go_to_page(PAGE_PATH)
    def dmarc_import_profiles(self, file_name):
        """Import DMARC verification profiles from existing file in
        /data/pub/configuration directory

        *Parameters:*
        - `file_name`: the name of existing file in /data/pub/configuration
        directory

        *Examples:*
        | DMARC Export Profiles | ${EXPORT_FILE_NAME} |
        | DMARC Import Profiles | ${EXPORT_FILE_NAME} |
        """
        self.click_button(IMPORT_BUTTON)

        controller = self._get_cached_controller(ImportForm)
        controller.set({FILE_TO_IMPORT_LIST[0]: file_name})
        controller.perform_import()

    @go_to_page(PAGE_PATH)
    def dmarc_export_profiles(self, file_name):
        """Export DMARC verification profiles to a file in
        /data/pub/configuration directory

        *Parameters:*
        - `file_name`: the name of a file to be created
        in /data/pub/configuration directory

        *Examples:*
        | DMARC Export Profiles | ${EXPORT_FILE_NAME} |
        | DMARC Import Profiles | ${EXPORT_FILE_NAME} |
        """
        self.click_button(EXPORT_BUTTON)

        controller = self._get_cached_controller(ExportForm)
        controller.set({FILE_TO_EXPORT[0]: file_name})
        controller.perform_export()

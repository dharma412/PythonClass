#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/services/services_overview.py#2 $
# $DateTime: 2019/07/08 08:12:20 $
# $Author: saurgup5 $

from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions
import re

PAGE_PATH = ('Security Services', 'Services Overview')

SERVICES_OVERVIEW_TABLE = "//table[@class='serviceupdatestbl']"
SERVICES_OVERVIEW_TABLE_COLS = "%s/tbody/tr/th" % SERVICES_OVERVIEW_TABLE
SERVICES_OVERVIEW_TABLE_ROWS = "%s/tbody/tr[@class='serviceupdatesrow']" % SERVICES_OVERVIEW_TABLE
SERVICES_OVERVIEW_TABLE_CELL = lambda row_num, col_num: \
    "%s/tbody/tr[%d]/td[%d]" % \
    (SERVICES_OVERVIEW_TABLE, row_num, col_num)
SERVICES_OVERVIEW_UPDATE_BUTTON = lambda row_num: \
    "%s/tbody/tr[%d]/td[4]//input[@value='Update']" % \
    (SERVICES_OVERVIEW_TABLE, row_num)
SERVICES_OVERVIEW_CHANGE_BUTTON = lambda row_num: \
    "%s/tbody/tr[%d]/td[5]/input[@value='Change']" % \
    (SERVICES_OVERVIEW_TABLE, row_num)
MODIFY_VERSION_RADIO_BUTTON = lambda row_num: \
    "%s/tbody/tr[%s]/td[1]/input[@type='radio']" % \
    (SERVICES_OVERVIEW_TABLE, row_num)
APPLY_UPDATE_BUTTON = "//input[@value='Apply' and @type='button']"
CANCEL_UPDATE_BUTTON = "//input[@value='Cancel' and @type='button']"

SERVICES_OVERVIEW_TABLE_CELL_MAP = {
    2: 'Current Service Version',
    3: 'Current Rule Version',
    4: 'Available Updates',
    5: 'Modify Versions',
    6: 'Auto Update',
}

SERVICES_OVERVIEW_TABLE_ROW_MAP = {
    'graymail': 2,
    'mcafee': 3,
    'sophos': 4
}

SERVICE_ROLLBACK_TABLE_CELL_MAP = {
    2: 'Service Version',
    3: 'Rule Version',
    4: 'Updated Time'
}


class ServicesOverview(GuiCommon):
    """Keywords for ESA GUI interaction with
       Security Services -> Services Overview page
    """

    def get_keyword_names(self):
        return [
            'services_overview_get_details',
            'services_overview_update',
            'services_overview_get_available_versions',
            'services_overview_modify_version']

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def services_overview_get_details(self):
        """
        Get Services Overview page details.

        *Parameters:*
        None

        *Return:*
        Returns a dictionary of dictionary in below format:
            {
                'engine1' : {
                    'Current Service Version' : '',
                    'Current Rule Version'    : '',
                    'Available Updates'       : '',
                    'Modify Versions'         : '',
                    'Auto Update'             : '',
                },
                'engine2' : {
                    'Current Service Version' : '',
                    'Current Rule Version'    : '',
                    'Available Updates'       : '',
                    'Modify Versions'         : '',
                    'Auto Update'             : '',
                }
            }

        *Examples:*
        | ${service_details} | Services Overview Get Details |
        | Log Dictionary     | ${service_details}            |
        """
        services_overview = {}
        rows = cols = 0

        if self._is_element_present(SERVICES_OVERVIEW_TABLE_ROWS):
            rows = int(self.get_matching_xpath_count(SERVICES_OVERVIEW_TABLE_ROWS))
        if self._is_element_present(SERVICES_OVERVIEW_TABLE_COLS):
            cols = int(self.get_matching_xpath_count(SERVICES_OVERVIEW_TABLE_COLS))

        if rows and cols:
            for row in range(2, rows + 2):
                engine_name = self.get_text( \
                    SERVICES_OVERVIEW_TABLE_CELL(row, 1)).strip()
                if not services_overview.has_key(engine_name):
                    services_overview[engine_name] = {}
                for col in range(2, cols + 1):
                    if self._is_element_present(SERVICES_OVERVIEW_TABLE_CELL(row, col)):
                        value = self.get_text(SERVICES_OVERVIEW_TABLE_CELL(row, col))
                        if value.lower() == 'this feature is not available or enabled':
                            services_overview[engine_name] = {
                                'Current Service Version': None,
                                'Current Rule Version': None,
                                'Available Updates': None,
                                'Modify Versions': None,
                                'Auto Update': None,
                            }
                            break
                        else:
                            services_overview[engine_name] \
                                [SERVICES_OVERVIEW_TABLE_CELL_MAP[col]] = value

        return services_overview

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def services_overview_update(self, **kwargs):
        """
        Clicks the update button for a given engine name from the
        Servies Overview page

        *Parameters:*
        - `engine_name`: Name of the engine which needs to be updated.
                         Allowed values are Sophos, McAfee

        *Return:*
        None

        *Examples:*
        | Services Overview Update | Sophos |
        | Services Overview Update | McAfee |
        """
        if not kwargs.has_key('engine_name'):
            raise ValueError('Mandatory parameter "engine_name" missing')

        update_button = SERVICES_OVERVIEW_UPDATE_BUTTON(
            SERVICES_OVERVIEW_TABLE_ROW_MAP[kwargs['engine_name'].lower()]
        )
        self._debug('[%s] Update button [%s]' % (kwargs['engine_name'], update_button))
        if self._is_element_present(update_button):
            self.click_button(update_button)
        else:
            raise guiexceptions.GuiFeatureDisabledError('Could not click ' \
                                                        + 'Update button for engine - %s. Update button NOT found' \
                                                        % kwargs['engine_name'])

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def services_overview_get_available_versions(self, **kwargs):
        """
        Get the versions available for rollback for a given engine name.

        *Parameters:*
        - `engine_name`: Name of the engine. Allowed values are Sophos, McAfee

        *Return:*
        - A dictionary containing versions info available for rollback
            {
                'version1' : {
                    'Service Version' : 'version 5700',
                    'Rule Version' : 'version 7437',
                    'Updated Time' : 'Available since Tue 21 Feb 2017 06:56:05',
                },
                'version2' : {
                    'Service Version' : 'version 5800',
                    'Rule Version' : 'version 8445',
                    'Updated Time' : 'Available since Tue 21 Feb 2017 22:08:09',
                },
            }

        *Examples:*
        | ${available_versions}= | Services Overview Get Available Versions | Sophos |
        | ${available_versions}= | Services Overview Get Available Versions | McAfee |
        """
        if not kwargs.has_key('engine_name'):
            raise ValueError('Mandatory parameter "engine_name" missing')

        rollback_versions = {}
        change_button = SERVICES_OVERVIEW_CHANGE_BUTTON(
            SERVICES_OVERVIEW_TABLE_ROW_MAP[kwargs['engine_name'].lower()]
        )
        self._debug('[%s] locator button XPATH [%s]' % (kwargs['engine_name'], change_button))
        if self._is_element_present(change_button):
            self.click_button(change_button)
            if self._is_element_present(SERVICES_OVERVIEW_TABLE_ROWS):
                rows = int(self.get_matching_xpath_count(SERVICES_OVERVIEW_TABLE_ROWS))
            if self._is_element_present(SERVICES_OVERVIEW_TABLE_COLS):
                cols = int(self.get_matching_xpath_count(SERVICES_OVERVIEW_TABLE_COLS))
            if rows > 2 and cols:
                index = 1
                for row in range(2, rows + 2):
                    for col in range(2, cols + 1):
                        if not rollback_versions.has_key('version' + str(index)):
                            rollback_versions['version' + str(index)] = {}
                        if self._is_element_present(SERVICES_OVERVIEW_TABLE_CELL(row, col)):
                            value = self.get_text(SERVICES_OVERVIEW_TABLE_CELL(row, col))
                            if value and re.search(r'(version.*)', value):
                                rollback_versions['version' + str(index)] \
                                    [SERVICE_ROLLBACK_TABLE_CELL_MAP[col]] = \
                                    re.search(r'(version.*)', value).group(1)
                            else:
                                rollback_versions['version' + str(index)] \
                                    [SERVICE_ROLLBACK_TABLE_CELL_MAP[col]] = value
                    index += 1
            self.click_button(CANCEL_UPDATE_BUTTON)
        else:
            self._error('Change button XPATH %s not present' % change_button)
        return rollback_versions

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def services_overview_modify_version(self, **kwargs):
        """
        Rolls back to a previous version for a given engine

        *Parameters:*
        - `engine_name`: Name of the engine. Allowed values are Sophos, McAfee.
        - `service_version`: Engine's service version.
        - `rule_version`: Engine's rule version.

        *Return:*
        None

        *Examples:*
        | Services Overview Modify Version        |
        | ... | engine_name=Sophos                |
        | ... | service_version=3.2.07.366.3_5.35 |
        | ... | rule_version=2017022101           |
        | Services Overview Modify Version        |
        | ... | engine_name=McAfee                |
        | ... | service_version=version 5700      |
        | ... | rule_version=version 8445         |
        """
        if not kwargs.has_key('engine_name') or \
                not kwargs.has_key('service_version') or \
                not kwargs.has_key('rule_version'):
            raise ValueError('One of the following parameters was not passed' \
                             + "\n\tengine_name\n\tservice_version\n\trule_version")
        change_button = SERVICES_OVERVIEW_CHANGE_BUTTON(
            SERVICES_OVERVIEW_TABLE_ROW_MAP[kwargs['engine_name'].lower()]
        )
        self._debug('[%s] Change button XPATH [%s]' % (kwargs['engine_name'], change_button))
        if self._is_element_present(change_button):
            self.click_button(change_button)
            radio_button = self._get_rollback_radio_button_xpath(
                kwargs['service_version'], kwargs['rule_version'])
            if radio_button:
                self._click_radio_button(radio_button)
                self.click_button(APPLY_UPDATE_BUTTON)
            else:
                self.click_button(CANCEL_UPDATE_BUTTON)
        else:
            raise guiexceptions.GuiFeatureDisabledError('Could not click ' \
                                                        + 'Change button for engine - %s. Change button NOT found' \
                                                        % kwargs['engine_name'])

    # --------------------------------------------------------------------------
    # Helper methods
    # --------------------------------------------------------------------------
    def _get_rollback_radio_button_xpath(self, service_version, rule_version):
        if self._is_element_present(SERVICES_OVERVIEW_TABLE_ROWS):
            rows = int(self.get_matching_xpath_count(SERVICES_OVERVIEW_TABLE_ROWS))
        if rows:
            for row in range(2, rows + 2):
                service = self.get_text(SERVICES_OVERVIEW_TABLE_CELL(row, 2))
                rule = self.get_text(SERVICES_OVERVIEW_TABLE_CELL(row, 3))
                self._debug('Row [%s] Service Version: %s' % (row, service))
                self._debug('Row [%s] Rule Version: %s' % (row, rule))
                if service_version.lower() in service.lower() \
                        and rule_version.lower() in rule.lower():
                    self._debug('Radio button row index found - [%s]' % row)
                    return MODIFY_VERSION_RADIO_BUTTON(row)
                else:
                    self._warn('Radio button row not found. Looking into next row')
        return None

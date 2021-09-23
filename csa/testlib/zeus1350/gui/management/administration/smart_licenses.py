#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/management/administration/smart_licenses.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
from smart_license_def.smart_license_settings import SmartLicenseSettings

EDIT_SETTINGS_BUTTON = "//input[@id='edit_settings']"
LICENSE_TABLE = "//table[@class='cols']"
HEADER_NAMES = "%s/tbody/tr[th]/th" % (LICENSE_TABLE,)
# idx starts from 1
LICENSE_ROWS = "%s/tbody/tr[td]" % (LICENSE_TABLE,)
CELL_BY_IDX = lambda row_idx, col_idx: "%s/tbody/tr[%d]/td[%d]" % \
                                       (LICENSE_TABLE, row_idx, col_idx)
SUBMIT_BUTTON = "//input[@class='submit']"
CONFIRM_OK_BUTTON = "//button[@id='yui-gen21-button']"

PAGE_PATH = ('System Administration', 'Licenses')


class SmartLicenses(GuiCommon):
    """Keywords for ESA GUI interaction with System Administration -> Licenses
    """

    def get_keyword_names(self):
        return ['smart_license_get_license_details',
                'smart_license_request_licenses',
                'smart_license_release_licenses']

    def _get_smart_license_settings_controller(self):
        if not hasattr(self, '_smart_license_settings_controller'):
            self._smart_license_settings_controller = SmartLicenseSettings(self)
        return self._smart_license_settings_controller

    def _edit_licenses(self, license_list, request_license):
        settings = {}
        self._info("Licenses are: %s" % (license_list))
        for license_idx in range(len(license_list)):
            settings[license_list[license_idx]] = request_license

        if self._is_element_present(EDIT_SETTINGS_BUTTON):
            self.click_button(EDIT_SETTINGS_BUTTON)
            controller = self._get_smart_license_settings_controller()
            controller.set(settings)
        else:
            raise GuiError('Edit Settings button is not displayed')
        if self._is_element_present(SUBMIT_BUTTON):
            self.click_button(SUBMIT_BUTTON, 'don\'t wait')
            if self._is_element_present(CONFIRM_OK_BUTTON):
                self.click_button(CONFIRM_OK_BUTTON)
            else:
                raise GuiError('Confirmation message is not displayed')
        else:
            raise GuiError('Submit Button is not displayed')

    @go_to_page(PAGE_PATH)
    def smart_license_request_licenses(self, request_license_list):
        """ Request smart licenses

        *Examples:*
        |@{request_license_list}= | Create List|
        |... | Content Security Management Config Manager |
        |... | Content Security Management Web Reporting |
        | Smart License Request Licenses| ${request_license_list} |

        """
        self._edit_licenses(request_license_list, request_license=True)

    @go_to_page(PAGE_PATH)
    def smart_license_release_licenses(self, release_license_list):
        """ Release smart licenses

        *Examples:*
        |@{release_license_list}= | Create List|
        |... | Content Security Management Config Manager |
        |... | Content Security Management Web Reporting |
        | Smart License Release Licenses| @{release_license_list} |

        """
        self._edit_licenses(release_license_list, request_license=False)

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def smart_license_get_license_details(self):
        """Get information about smart licenses

        *Return:*
        Dictionary of licenses and authorization status

        for example:
        Content Security Management Config Manager: Not requested
        Content Security Management Web Reporting: Not requested
        Content Security Management Master ISQ: Not requested
        Content Security Management Centralized Tracking: Not requested
        Content Security Management Centralized Reporting: Not requested
        Mail Handling: In Compliance

        *Examples:*
        | ${details}= | Smart License Get License Details |
        | Log Dictionary | ${details} |
        | ${keys}= | Get Dictionary Keys | ${details} |
        | Log List | ${keys} |
        """
        result = {}
        headers_count = int(self.get_matching_xpath_count(HEADER_NAMES))
        keys_count = int(self.get_matching_xpath_count(LICENSE_ROWS))
        for row_idx in xrange(2, keys_count + 2):
            for col_idx in xrange(1, headers_count):
                feature_name = self.get_text(CELL_BY_IDX(row_idx, col_idx)).strip()
                auth_status = self.get_text(CELL_BY_IDX(row_idx, col_idx + 1)).strip()
                result[feature_name] = auth_status
        return result

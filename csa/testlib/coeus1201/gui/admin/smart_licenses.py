#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/smart_licenses.py#1 $
#$DateTime: 2019/08/14 09:58:47 $
#$Author: uvelayut $

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
CONFIRM_OK_BUTTON = "//button[@id='yui-gen6-button']"

PAGE_PATH = ('System Administration', 'Licenses')

class SmartLicenses(GuiCommon):
    """Keywords for WSA GUI interaction with System Administration -> Licenses
    """

    def get_keyword_names(self):
        return ['smart_license_get_license_details',
                'smart_license_request_licenses',
                'smart_license_release_licenses']

    def _get_smart_license_settings_controller(self):
        if not hasattr(self, '_smart_license_settings_controller'):
            self._smart_license_settings_controller = SmartLicenseSettings(self)
        return self._smart_license_settings_controller

    def _edit_licenses(self,license_list,request_license):
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
    def smart_license_request_licenses(self,request_license_list):
        """ Request smart licenses

        *Examples:*
        |@{request_license_list}= | Create List|
        |... | Web Security Appliance Cisco Web Usage Controls |
        |... | Web Security Appliance Anti-Virus Webroot |
        | Smart License Request Licenses| ${request_license_list} |

        """
        self._edit_licenses(request_license_list,request_license=True)

    @go_to_page(PAGE_PATH)
    def smart_license_release_licenses(self,release_license_list):
        """ Release smart licenses

        *Examples:*
        |@{release_license_list}= | Create List|
        |... | Web Security Appliance Cisco Web Usage Controls |
        |... | Web Security Appliance Anti-Virus Webroot |
        | Smart License Release Licenses| @{release_license_list} |

        """
        self._edit_licenses(release_license_list,request_license=False)

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def smart_license_get_license_details(self):
        """Get information about smart licenses

        *Return:*
        Dictionary of licenses and authorization status

        for example:
        Web Security Appliance Cisco Web Usage Controls : Not requested
	Web Security Appliance Anti-Virus Webroot : Not requested
	Web Security Appliance L4 Traffic Monitor : Not requested
	Web Security Appliance Cisco AnyConnect SM for AnyConnect : Not requested
	Web Security Appliance Advanced Malware Protection Reputatio : Not requested
	Web Security Appliance Anti-Virus Sophos : Not requested
	Web Security Appliance Web Reputation Filters : Not requested
	Web Security Appliance Advanced Malware Protection : Not requested
	Web Security Appliance Anti-Virus McAfee : Not requested
	Web Security Appliance Web Proxy and DVS Engine : Not requested
	Web Security Appliance HTTPs Decryption : Not requested

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

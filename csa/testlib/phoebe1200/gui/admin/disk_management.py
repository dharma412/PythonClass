#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/admin/disk_management.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.guicommon import GuiCommon, Wait
from common.gui.guiexceptions import TimeoutError, GuiValueError
import re

EDIT_QUOTAS_BUTTON = "//input[@value='Edit Disk Quotas...']"
EUQ_QUOTA_TEXTBOX = "//input[@id='euq_quota']"
PVO_QUOTA_TEXTBOX = "//input[@id='pvo_quota']"
REPORTING_QUOTA_TEXTBOX = "//input[@id='reporting_quota']"
TRACKING_QUOTA_TEXTBOX = "//input[@id='tracking_quota']"
MISC_QUOTA_TEXTBOX = "//input[@id='misc_quota']"
DISK_TABLE = "//table[@class='cols']"
SERVICE_CELL_TEXT = lambda row: '%s//tr[%s]/td[1]' % (DISK_TABLE, row)
USAGE_CELL_TEXT = lambda row: '%s//tr[%s]/td[2]' % (DISK_TABLE, row)
QUOTA_CELL_TEXT = lambda row: '%s//tr[%s]/td[3]' % (DISK_TABLE, row)
SUBMIT_BUTTON = "//input[@value='Submit']"
SET_NEW_QUOTAS_BUTTON = 'xpath=//button[text()="Set New Quotas"]'


class DiskManagement(GuiCommon):
    """Keywords for Cisco Email Security Appliance ->
       System Administration -> Disk Management
    """

    def get_keyword_names(self):
        return ['disk_management_get_quotas',
                'disk_management_get_service_quota',
                'disk_management_get_usage',
                'disk_management_get_service_usage',
                'disk_management_get_total_quotas',
                'disk_management_get_total_usage',
                'disk_management_edit_quotas',
                ]

    def _open_page(self):
        self._navigate_to('System Administration', 'Disk Management')

    def _click_edit_quotas_button(self):
        self.click_button(EDIT_QUOTAS_BUTTON)

    def _fill_quotas_table(self, spam_quarantine, pvo_quarantine,
                           reporting, tracking, misc):
        values = (spam_quarantine, pvo_quarantine, reporting,
                  tracking, misc)
        locators = (EUQ_QUOTA_TEXTBOX, PVO_QUOTA_TEXTBOX,
                    REPORTING_QUOTA_TEXTBOX, TRACKING_QUOTA_TEXTBOX,
                    MISC_QUOTA_TEXTBOX)

        for locator, quota in zip(locators, values):
            if quota is not None:
                self.input_text(locator, quota)

    def _get_info_dict(self, row_locator):
        info_dict = {}
        starting_row = 2
        num_of_rows = int(
            self.get_matching_xpath_count(SERVICE_CELL_TEXT('*')))

        # Pattern to match a ',', '&', '(.*)' and ':'
        pattern1 = re.compile(',|&|\(.*\)|:')
        # Pattern to match a single space
        pattern2 = re.compile(' ')
        # Pattern to match two consicutive underscores '__'
        pattern3 = re.compile('__')
        for row in xrange(starting_row, num_of_rows):
            name = self.get_text(SERVICE_CELL_TEXT(row)).strip()
            # Remove any ',' or '&' or '(.*)' or ':'
            name = pattern1.sub('', name).strip().lower()
            # Replace single spaces ' ' with underscore '_'
            name = pattern2.sub('_', name)
            # Replace two consicutive underscores with a single underscore
            name = pattern3.sub('_', name)
            service_names = name.split()

            value = self.get_text(row_locator(row)).rstrip(' G')
            quota_or_usage_values = value.split()
            while 'G' in quota_or_usage_values:
                quota_or_usage_values.remove('G')

            # If a service contains sub-sections (ex: Miscallenius Files)
            # Then populate the info_dict dictionary in following format:
            # info_dict = {
            #    service_name1 : {
            #       total_usage  : total_usage,
            #       sub_service1 : value1,
            #       sub_service2 : value2,
            #    }
            #    service_name2 : value2,
            #    service_name3 : value3,
            # }

            if len(service_names) > 1 and len(quota_or_usage_values) > 1:
                service_name = service_names.pop(0).rstrip('_')
                total_usage = quota_or_usage_values.pop(0)
                info_dict[service_name] = {}
                info_dict[service_name]['total_usage'] = int(total_usage)
                for i in range(len(service_names)):
                    info_dict[service_name][service_names[i].rstrip('_')] = \
                        int(quota_or_usage_values[i])
            else:
                info_dict[name] = int(value)

        self._info(info_dict)

        return info_dict

    def _get_service_value(self, service_name, info_dict):
        pattern = re.compile(' ')
        service_name = pattern.sub('_', service_name).lower()
        for key, value in info_dict.iteritems():
            if service_name in key:
                return value
        else:
            raise GuiValueError('Unknown %s service name' % \
                                (service_name,))

    def _submit_new_quotas(self):
        self.click_button(SUBMIT_BUTTON, 'dont wait')
        try:
            # sometimes there is 1-2 seconds delay before dialog shows
            # up. Have to wait for it.
            Wait(self._is_element_present, timeout=5).wait(
                SET_NEW_QUOTAS_BUTTON)
            self.click_button(SET_NEW_QUOTAS_BUTTON)
        except TimeoutError:
            # no 'Set New Quotas' dialog was shown
            pass
        finally:
            self._check_action_result()

    def disk_management_get_quotas(self):
        """Get current disk quotas.

        Return:
        A dictionary where keys are the names of the services and values are
        the numbers of gigabytes of current disk quotas.

        Examples:
        | ${quotas} = | Disk Management Get Quotas |
        """
        self._open_page()

        return self._get_info_dict(QUOTA_CELL_TEXT)

    def disk_management_get_service_quota(self, service_name):
        """Get current disk quota for particular service.

        Parameters:
        - `service_name`: name of the service to get quota value for.
        Options are:
        | Spam Quarantine |
        | Policy Virus Outbreak Quarantines |
        | Reporting |
        | Tracking |
        | Miscellaneous Files |

        Return:
        A string of disk quota value.

        Examples:
        | ${tracking_quota} = | Disk Management Get Service Quota |
        | ... | Tracking |
        | ${isq_quota} = | Disk Management Get Service Quota |
        | ... | Spam Quarantine |

        Exceptions:
        - `GuiValueError`: in case of invalid `service_name`.
        """
        quotas = self.disk_management_get_quotas()

        return self._get_service_value(service_name, quotas)

    def disk_management_get_usage(self):
        """Get current disk usage.

        Return:
        A dictionary where keys are the names of the services and values are
        the numbers of gigabytes of current disk usage.

        Examples:
        | ${usage} = | Disk Management Get Usage |
        """
        self._open_page()

        return self._get_info_dict(USAGE_CELL_TEXT)

    def disk_management_get_service_usage(self, service_name):
        """Get current disk usage for particular service.

        Parameters:
        - `service_name`: name of the service to get disk usage for.
        Options are:
        | Spam Quarantine |
        | Policy Virus Outbreak Quarantines |
        | Reporting |
        | Tracking |
        | Miscellaneous Files |

        Return:
        A string of disk usage value.

        Examples:
        | ${tracking_usage} = | Disk Management Get Service Usage |
        | ... | Tracking |
        | ${isq_usage} = | Disk Management Get Service Usage |
        | ... | Spam Quarantine |

        Exceptions:
        - `GuiValueError`: in case of invalid `service_name`.
        """
        usage = self.disk_management_get_usage()

        return self._get_service_value(service_name, usage)

    def disk_management_edit_quotas(self, spam_quarantine=None,
                                    pvo_quarantine=None, reporting=None, tracking=None, misc=None):
        """Edit disk quotas.

        Parameters:
        - `spam_quarantine`: the number of gigabytes to use as disk quota for
           Spam Quarantine.
        - `pvo_quarantine`: the number of gigabytes to use as disk quota for
           Policy, Virus and Outbreak Quarantines.
        - `reporting`: the number of gigabytes to use as disk quota for
           Centralized Web Reporting.
        - `tracking`: the number of gigabytes to use as disk quota for
           Tracking.
        - `misc`: the number of gigabytes to use as disk quota for
           Miscelenious Services.


        Examples:
        | Disk Management Edit Quotas |
        | ... | spam_quarantine=10 |
        | ... | pvo_quarantine=50 |
        | ... | reporting=20 |
        | ... | tracking=30 |
        | ... | misc=50 |
        | Disk Management Edit Quotas | reporting=30 | tracking=20 |
        """
        self._open_page()

        self._click_edit_quotas_button()

        self._fill_quotas_table(spam_quarantine, pvo_quarantine,
                                reporting, tracking, misc)

        self._submit_new_quotas()

    def disk_management_get_total_quotas(self):
        """Get total allocated quota.

        Return:
        The integet value of the 'Total Space Allocated' field in UI

        Examples:
        | ${usage} = | Disk Management Get Total Quotas |
        """
        total_quota = 0

        self._open_page()
        quota_dict = self._get_info_dict(QUOTA_CELL_TEXT)

        for quota_size in quota_dict.values():
            total_quota += int(quota_size)

        return total_quota

    def disk_management_get_total_usage(self):
        """Get the total space used.

        Return:
        The integet value of the 'Total Space Used' field in UI

        Examples:
        | ${usage} = | Disk Management Get Total Usage |
        """
        total_usage = 0

        self._open_page()
        usage_dict = self._get_info_dict(USAGE_CELL_TEXT)

        for usage_size in usage_dict.values():
            if type(usage_size) is dict and usage_size.has_key('total_usage'):
                total_usage += int(usage_size['total_usage'])
            else:
                total_usage += int(usage_size)

        return total_usage

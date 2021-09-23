#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/management/administration/disk_management.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $


import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon, Wait


EDIT_QUOTAS_BUTTON = 'xpath=//input[@value=\'Edit Disk Quotas...\']'
EUQ_QUOTA_TEXTBOX = 'id=euq_quota'
REPORTING_QUOTA_TEXTBOX = 'id=reporting_quota'
WEB_TRACKING_QUOTA_TEXTBOX = 'id=web_tracking_quota'
EMAIL_TRACKING_QUOTA_TEXTBOX = 'id=tracking_quota'
CPQ_QUOTA_TEXTBOX = 'id=cpq_quota'
DISK_TABLE = "//table[@class='cols']"
SERVICE_CELL_TEXT = lambda row: '%s//tr[%s]/td[1]' % (DISK_TABLE, row)
USAGE_CELL_TEXT = lambda row: '%s//tr[%s]/td[2]' % (DISK_TABLE, row)
QUOTA_CELL_TEXT = lambda row: '%s//tr[%s]/td[3]' % (DISK_TABLE, row)
SUBMIT_BUTTON = "//input[@value='Submit']"
SET_NEW_QUOTAS_BUTTON = 'xpath=//button[text()="Set New Quotas"]'


class DiskManagement(GuiCommon):

    """Keywords for Management Appliance -> System Administration -> Disk
    Management
    """

    def get_keyword_names(self):
        return ['disk_management_get_quotas',
                'disk_management_get_service_quota',
                'disk_management_get_usage',
                'disk_management_get_service_usage',
                'disk_management_edit_quotas',
                ]

    def _open_page(self):
        self._navigate_to('Management', 'System Administration',
            'Disk Management')

    def _click_edit_quotas_button(self):
        self.click_button(EDIT_QUOTAS_BUTTON)

    def _fill_quotas_table(self, spam_quarantine, web_reporting, web_tracking,
                           email_tracking, pvo_quarantine):
        values = (spam_quarantine, web_reporting, web_tracking,
                    email_tracking, pvo_quarantine)
        locators = (EUQ_QUOTA_TEXTBOX, REPORTING_QUOTA_TEXTBOX,
                    WEB_TRACKING_QUOTA_TEXTBOX, EMAIL_TRACKING_QUOTA_TEXTBOX,
                    CPQ_QUOTA_TEXTBOX)

        for locator, quota in zip(locators, values):
            if quota is not None:
                self.input_text(locator, quota)

    def _get_info_dict(self, row_locator):
        info_dict = {}
        starting_row = 2
        num_of_rows = int(
            self.get_matching_xpath_count(SERVICE_CELL_TEXT('*')))

        for row in xrange(starting_row, num_of_rows):
            name = self.get_text(SERVICE_CELL_TEXT(row))
            value = self.get_text(row_locator(row))
            value = value.rstrip(' G')
            name_new = name.split('\n')
            value2 = self.get_text(row_locator(row)).split('\n')
            if len(name_new) > 1 and len(value2) > 1 :
                info_dict[name_new[0]] = {}
                total_usage = value2[0].rstrip(' G')
                total_usage = float(total_usage) if '.' in total_usage else int(total_usage)
                info_dict[name_new[0]]['total_usage'] = total_usage
                for i in range(1,len(value2)):
                    val = value2[i].rstrip(' G')
                    val = float(val) if '.' in val else int(val)
                    info_dict[name_new[0]][name_new[i]] = val
            else:
                info_dict[name] = float(value) if '.' in value else int(value)
        return info_dict

    def _get_service_value(self, service_name, info_dict):
        for key, value in info_dict.iteritems():
            if service_name in key:
                return value
        else:
            raise guiexception.GuiValueError('Unknown %s service name' %\
                (service_name,))

    def _submit_new_quotas(self):
        self.click_button(SUBMIT_BUTTON, 'dont wait')

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

        Return:
        A string of disk quota value.

        Examples:
        | ${email_tracking_quota} = | Disk Management Get Service Quota |
        | ... | Centralized Email Tracking |
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

        Return:
        A string of disk usage value.

        Examples:
        | ${email_tracking_usage} = | Disk Management Get Service Usage |
        | ... | Centralized Email Tracking |
        | ${isq_usage} = | Disk Management Get Service Usage |
        | ... | Spam Quarantine |

        Exceptions:
        - `GuiValueError`: in case of invalid `service_name`.
        """
        usage = self.disk_management_get_usage()

        return self._get_service_value(service_name, usage)

    def disk_management_edit_quotas(self, spam_quarantine=None,
        reporting=None, web_tracking=None, email_tracking=None,
        pvo_quarantine=None):
        """Edit disk quotas.

        Parameters:
        - `spam_quarantine`: the number of gigabytes to use as disk quota for
           Spam Quarantine.
        - `reporting`: the number of gigabytes to use as disk quota for
           Centralized Web Reporting.
        - `web_tracking`: the number of gigabytes to use as disk quota for
           Centralized Web Tracking.
        - `email_tracking`: the number of gigabytes to use as disk quota for
           Centralized Email Tracking.
        - `pvo_quarantine`: the number of gigabytes to use as disk quota for
           Policy, Virus and Outbreak Quarantines.


        Examples:
        | Disk Management Edit Quotas |
        | ... | spam_quarantine=10 |
        | ... | reporting=20 |
        | ... | web_tracking=30 |
        | ... | email_tracking=40 |
        | ... | pvo_quarantine=50 |
        | Disk Management Edit Quotas | reporting=30 | email_tracking=20 |
        """
        self._open_page()

        self._click_edit_quotas_button()

        self._fill_quotas_table(spam_quarantine, reporting, web_tracking,
            email_tracking, pvo_quarantine)

        self._submit_new_quotas()


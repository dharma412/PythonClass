#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/utilities/publish_history.py#1 $

import re

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

PUBLISH_HISTORY_TABLE = '//tbody[@class=\'yui-dt-data\']'
PUBLISH_HISTORY_TABLE_ROW = '%s/tr' % (PUBLISH_HISTORY_TABLE,)
TABLE_CELL_DATA = lambda row, column: '%s[%s]/td[%s]' % (PUBLISH_HISTORY_TABLE_ROW, row, column)
JOB_LINK = lambda name: 'link=%s' % (name,)


class PublishHistory(GuiCommon):
    """ Keywords for Web -> Utilities -> Publish History
    """

    def get_keyword_names(self):
        return [
            'publish_history_get_jobs',
            'publish_history_is_job_present',
            'publish_history_get_job_status',
            'publish_history_get_job_details',
            'publish_history_get_job_appliances',
            'publish_history_get_appliance_data',
            'publish_history_get_appliance_details',
        ]

    def _open_page(self):
        try:
            self._navigate_to('Web', 'Utilities', 'Publish History')
        except Exception as error:
            if re.search('Publish History.*not found', error.message):
                raise guiexceptions.GuiFeatureDisabledError(
                    'Configuration Masters are not initialized')
            raise

    def _get_all_jobs(self):
        jobs = []

        if self._is_text_present('No finished jobs'):
            return jobs

        num_of_rows = int(self.get_matching_xpath_count(PUBLISH_HISTORY_TABLE_ROW))
        num_of_columns = 6
        for row in xrange(1, num_of_rows + 1):
            data = []
            for column in xrange(1, num_of_columns):
                data.append(self.get_text(TABLE_CELL_DATA(row, column)))
            jobs.append(PublishHistoryJob(*data))

        return jobs

    def _get_job_status(self, job_name):
        if self._is_text_present('No finished jobs'):
            raise guiexceptions.GuiValueError("Job '%s' was not found.")

        job_row_loc = PUBLISH_HISTORY_TABLE + \
                      "//a[normalize-space(text())='%s']/ancestor::tr[1]" % (job_name,)

        if int(self.get_matching_xpath_count(job_row_loc)) == 0:
            raise guiexceptions.GuiValueError("Job '%s' was not found." % (job_name,))

        job_status = self.get_text("xpath=" + job_row_loc + "/td[5]")
        return job_status

    def _open_job_details(self, job_name):
        if self._is_text_present('No finished jobs'):
            raise guiexceptions.GuiValueError("Job '%s' was not found.")

        job_link_loc = PUBLISH_HISTORY_TABLE + "//a[normalize-space(text())='%s']" % (job_name,)

        if int(self.get_matching_xpath_count(job_link_loc)) == 0:
            raise guiexceptions.GuiValueError("Job '%s' was not found." % (job_name,))

        self.click_link("xpath=" + job_link_loc)

    def _get_job_details(self, job_name):
        self._open_job_details(job_name)

        job_details_loc = "//dt[normalize-space(text())='%s']/following-sibling::dd[1]" % ('Job Details',)
        job_detail_loc_pref = job_details_loc + "//th[normalize-space(text())='%s']/following-sibling::td[1]"

        job_general_details = {}
        name = self.get_text(job_detail_loc_pref % 'Job Name:')
        job_general_details['Job Name'] = name
        cm = self.get_text(job_detail_loc_pref % 'Configuration Master:')
        job_general_details['Configuration Master'] = cm
        time = self.get_text(job_detail_loc_pref % 'Completion Time:')
        job_general_details['Completion Time'] = time

        return job_general_details

    def _get_job_appliances(self, job_name):
        self._open_job_details(job_name)

        appliance_details_loc = "//*[normalize-space(text())='%s']/ancestor-or-self::*[parent::dd]/following-sibling::table[1]//tr" % (
        'Appliance Details for Job',)

        appliances = []
        appliances_num = int(self.get_matching_xpath_count(appliance_details_loc)) - 1
        for row_index in range(appliances_num):
            appl_name_loc = appliance_details_loc + "[" + str(2 + row_index) + "]/td[1]"
            appliance = self.get_text(appl_name_loc)
            appliances.append(appliance)

        return appliances

    def _get_job_appliance_data(self, job_name, appliance_name):
        self._open_job_details(job_name)

        appliance_row = "//*[normalize-space(text())='%s']/ancestor-or-self::*[parent::dd]/following-sibling::table[1]//a[normalize-space(text())='%s']/ancestor::tr[1]" % (
        'Appliance Details for Job', appliance_name)

        if int(self.get_matching_xpath_count(appliance_row)) == 0:
            raise guiexceptions.GuiValueError("Appliance '%s' was not found." % (appliance_name,))

        appl_name = self.get_text(appliance_row + "/td[1]")
        appl_ip_host = self.get_text(appliance_row + "/td[2]")
        appl_status = self.get_text(appliance_row + "/td[3]")
        appl_details = self.get_text(appliance_row + "/td[4]")

        return {
            'IP Address or Hostname': appl_ip_host,
            'Status': appl_status,
            'Status Details': appl_details,
        }

    def _get_job_appliance_details(self, job_name, appliance_name):
        self._open_job_details(job_name)

        appliance_row = "//*[normalize-space(text())='%s']/ancestor-or-self::*[parent::dd]/following-sibling::table[1]//a[normalize-space(text())='%s']/ancestor::tr[1]" % (
        'Appliance Details for Job', appliance_name)

        if int(self.get_matching_xpath_count(appliance_row)) == 0:
            raise guiexceptions.GuiValueError("Appliance '%s' was not found." % (appliance_name,))

        appliance_details_link = appliance_row + "/td[4]/a"

        if int(self.get_matching_xpath_count(appliance_details_link)) == 0:
            raise guiexceptions.GuiValueError("Appliance '%s' did not have 'Details' link." % (appliance_name,))

        self.click_link("xpath=" + appliance_details_link)

        info_loc = "//dd//div[@class='text-info']"
        rows_loc = "//dd//table//tr"

        issues = []

        info_count = int(self.get_matching_xpath_count(info_loc))
        if info_count > 0:
            text_info = self.get_text(info_loc)
            issues.append(text_info)

        rows_count = int(self.get_matching_xpath_count(rows_loc))
        for row_index in range(1, 1 + rows_count):
            data_loc = rows_loc + "[" + str(row_index) + "]/*"
            issue = self.get_text(data_loc + "[1]")
            if int(self.get_matching_xpath_count(data_loc + "[2]")) > 0:
                issue_change = self.get_text(data_loc + "[2]")
                issues.append([issue, issue_change])
            else:
                issues.append(issue)

        return issues

    def publish_history_get_jobs(self):
        """Get information about all published jobs.

        Return:
            A list of objects containing information about published jobs.
            Each object has the following attributes:
                - `name`: name of the job.
                - `time`: job completion time.
                - `cm`: configuration master that was published.
                - `app_num`: the number of appliances the configuration was
                   published to.
                - `status`: status of the publish.

        Example:
             | @{jobs} | Publish History Get Jobs |

        Exception:
            - `GuiFeatureDisabledError`: in case if configuration masters are
              not initialized.
        """
        self._open_page()

        jobs = self._get_all_jobs()

        return jobs

    def publish_history_is_job_present(self, job_name):
        """Check whether job name is on the publish history list.

        Parameters:
            - `job_name`: name of job to check.

        Return:
            A boolean value. True in case if job with 'job_name' is present on
            the page.

        Examples:
            | Publish History Is Job Present | job_name |

        Exception:
            - `GuiFeatureDisabledError`: in case if configuration masters are
               not initialized.
        """
        self._open_page()

        result = self._is_element_present(JOB_LINK(str(job_name)))

        if result:
            self._info('Job %s is present' % (job_name,))
        else:
            self._info('Job %s is not present' % (job_name,))

        return result

    def publish_history_get_job_status(self, job_name):
        """Get status of indicated job.

        Parameters:
            - `job_name`: name of a job.

        Return:
            String with status of the job.

        Example:
             | ${job_status} | Publish History Get Job Status | job1 |
             | Log | ${job_status} |

        Exception:
            - `GuiFeatureDisabledError`: in case if configuration masters are
              not initialized.
            - `GuiValueError`: in case if job was not found.
        """
        self._open_page()

        job_status = self._get_job_status(job_name)

        return job_status

    def publish_history_get_job_details(self, job_name):
        """Get details of specified job from "Publish History: Job Details" page.

        Parameters:
            - `job_name`: name of a job.

        Return:
            A dictionary with details for the job.
            Keys are: "Job Name", "Configuration Master", "Completion Time".

        Example:
             | ${job_details} | Publish History Get Job Details | job1 |
             | Log | ${job_details['Job Name']} |
             | Log | ${job_details['Configuration Master']} |
             | Log | ${job_details['Completion Time']} |

        Exception:
            - `GuiFeatureDisabledError`: in case if configuration masters are
              not initialized.
            - `GuiValueError`: in case if the job was not found.
        """
        self._open_page()

        job_details = self._get_job_details(job_name)

        return job_details

    def publish_history_get_job_appliances(self, job_name):
        """Get list of appliances in specified job from
        "Publish History: Job Details" page.

        Parameters:
            - `job_name`: name of a job.

        Return:
            A list of appliances in the job.

        Example:
             | @{job_appliances} | Publish History Get Job Appliances | job1 |
             | Log Many | @{job_appliances} |

        Exception:
            - `GuiFeatureDisabledError`: in case if configuration masters are
              not initialized.
            - `GuiValueError`: in case if the job was not found.
        """
        self._open_page()

        job_appliances = self._get_job_appliances(job_name)

        return job_appliances

    def publish_history_get_appliance_data(self, job_name, appliance_name):
        """Get data of specified appliance in specified job from
        "Publish History: Job Details" page.

        Parameters:
            - `job_name`: name of a job.
            - `appliance_name`: name of an appliance in the job.

        Return:
            A dictionary with data of the appliance in the job.
            Keys are: "IP Address or Hostname", "Status", "Status Details" (last cell in the row).

        Example:
             | ${appliance_data} | Publish History Get Appliance Data | job1 | WSA1 |
             | Log | ${appliance_data} |
             | Log | ${appliance_data['IP Address or Hostname'] |
             | Log | ${appliance_data['Status'] |
             | Log | ${appliance_data['Status Details'] |

        Exception:
            - `GuiFeatureDisabledError`: in case if configuration masters are
              not initialized.
            - `GuiValueError`: in case if the job was not found.
        """
        self._open_page()

        job_appliance_data = self._get_job_appliance_data(job_name, appliance_name)

        return job_appliance_data

    def publish_history_get_appliance_details(self, job_name, appliance_name):
        """Get details of specified appliance in specified job from
        "Web Appliance Publish Details" page.

        Parameters:
            - `job_name`: name of a job.
            - `appliance_name`: name of an appliance in the job.

        Return:
            A list of issues with publishing the job for the appliance.
            First item is info text from "Web Appliance Publish Details" page.
            Next items are rows from the table.

        Example:
             | ${appliance_details} | Publish History Get Appliance Details | job1 | WSA1 |
             | Log | ${appliance_data[0]} |
             | Log Many | ${appliance_data[1:] |

        Exception:
            - `GuiFeatureDisabledError`: in case if configuration masters are
              not initialized.
            - `GuiValueError`: in case if the job was not found.
        """
        self._open_page()

        job_appliance_data = self._get_job_appliance_details(job_name, appliance_name)

        return job_appliance_data


class PublishHistoryJob(object):
    """Container for detailed information about published jobs

    Attributes:
        - `name`: name of the job.
        - `time`: job completion time.
        - `cm`: configuration master that was published.
        - `app_num`: the number of appliances the configuration was
                     published to.
        - `status`: status of the publish.
    """

    def __init__(self, name, time, cm, app_num, status):
        self.name = name
        self.time = time
        self.cm = cm
        self.app_num = app_num
        self.status = status

    def __str__(self):
        text = ['Name: %s' % (self.name,),
                'Time: %s' % (self.time,),
                'Configuration Master: %s' % (self.cm,),
                'Number of Appliances: %s' % (self.app_num,),
                'Status: %s' % (self.status,)]

        return '\n'.join(text)

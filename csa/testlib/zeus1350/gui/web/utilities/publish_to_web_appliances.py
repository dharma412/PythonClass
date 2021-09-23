#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/utilities/publish_to_web_appliances.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

import re
import time
import common.gui.guiexceptions as guiexceptions

from common.gui.guicommon import (GuiCommon, Wait)
from sma.constants import sma_config_masters

PUBLISH_NOW_BUTTON = "//input[@value='Publish Configuration Now...']"
SCHEDULE_PUBLISH_BUTTON = "//input[@value='Schedule a Job...']"
CUSTOM_JOB_NAME_RADIOBUTTON = "//input[@id='sys_job_name_no']"
CUSTOM_JOB_NAME_FIELD = "//input[@id='job_name']"
SYSTEM_JOB_NAME_RADIOBUTTON = "//input[@id='sys_job_name_yes']"
DATE_FIELD = "//input[@id='start_at_date']"
TIME_FIELD = "//input[@id='start_at_time']"
CONFIGURATION_MASTERS_LIST = "//select[@id='config_master']"
FILEPATH_FIELD = "//input[@name='config_file']"
APPLIANCES_LIST = "//select[@id='appliances_option']"
APPLIANCES_TABLE_CELL = lambda row, column: \
    "//div[@id='add_edit_job_appliances_list_div']//table//tr[%s]/td[%s]" % \
    (row, column)
APPLIANCES_NAME_CELL = lambda row: APPLIANCES_TABLE_CELL(row, 2)
APPLIANCES_CHECKBOX_CELL = \
    lambda \
        row: "//div[@id='add_edit_job_appliances_list_div']//table//tr[%s]/td[1]/div/input[@name='appliances_list[]']" % \
             (row)
PUBLISH_BUTTON = "//input[@class='submit']"
CONTINUE_PUBLISH_BUTTON = "//button[@type='button' and contains(text(), 'Continue Publish')]"
RESULT_TEXT = "//*[@id='action-results-title']"
STATUS_TABLE = "//table[@id='status-table']"

SCHEDULED_JOBS_LINK = '//tbody[@class=\'yui-dt-data\']/tr[contains(@id, \'yui-rec\')]'
SCHEDULED_JOB_NAME_LINK = lambda row: \
    '//tbody[@class=\'yui-dt-data\']/tr[%d]/td[1]/div/a/text()' % (row + 1,)
SCHEDULED_JOB_FIELD_LINK = lambda row, col: \
    '//tbody[@class=\'yui-dt-data\']/tr[%d]/td[%d]/div/text()' % (row + 1, col,)

DELETE_JOB_LINK = lambda row: \
    '//tbody[@class=\'yui-dt-data\']/tr[%d]/td[contains(@class, \'Delete\')]/div/a/img' \
    % (row + 1,)
USER_PUBLISH = "xpath=//table[@class='cols']/tbody/tr/td[2]//div/a"


class PublishToWebAppliances(GuiCommon):
    """Keywords for Web -> Utilities -> Publish to Web Appliances"""

    def get_keyword_names(self):
        return ['publish_to_web_appliances_configuration_master_now',
                'publish_to_web_appliances_configuration_file_now',
                'publish_to_web_appliances_configuration_master_schedule',
                'publish_to_web_appliances_configuration_file_schedule',
                'publish_to_web_appliances_get_scheduled_jobs',
                'publish_to_web_appliances_delete_scheduled_job', ]

    def _open_page(self):
        try:
            if "Account Privileges" in self.get_title():
                self.click_element(USER_PUBLISH, "don't wait")
            else:
                self._navigate_to('Web', 'Utilities', 'Publish to Web Appliances')
        except Exception as error:
            # Handle only the case when Configuration Masters are not
            # initialized, 'Publish to Web Appliances' menu item is not present
            # then.
            if re.search('Publish to Web Appliances.*?not found',
                         error.message):
                raise guiexceptions.GuiFeatureDisabledError(
                    'Configuration Masters are not initialized')
            # dont care about the rest, let the caller handle this
            raise

    def _select_job_name(self, job_name):
        if job_name.lower() == 'system-generated':
            self._click_radio_button(SYSTEM_JOB_NAME_RADIOBUTTON)
        else:
            self._click_radio_button(CUSTOM_JOB_NAME_RADIOBUTTON)
            self.input_text(CUSTOM_JOB_NAME_FIELD, job_name)

    def _select_configuration_master(self, master):
        masters = self.get_list_items(CONFIGURATION_MASTERS_LIST)

        if master not in masters:
            raise guiexceptions.GuiValueError('`%s` master was not found in ' \
                                              'Configuration Masters select list' % (master,))

        self.select_from_list(CONFIGURATION_MASTERS_LIST, master)

    def _select_file_to_publish(self, filepath):
        self.select_from_list(CONFIGURATION_MASTERS_LIST,
                              'Advanced file options...')
        self.choose_file(FILEPATH_FIELD, filepath)

    def _get_available_appliances_names(self):
        num_of_rows = int(
            self.get_matching_xpath_count(APPLIANCES_NAME_CELL('*')))

        return [self.get_text(APPLIANCES_NAME_CELL(row)) \
                for row in range(1, num_of_rows + 1)]

    def _select_appliances(self, appliances):
        all_appliances_map = {
            'All': 'All assigned appliances',
            sma_config_masters.CM91: 'Master 9.1',
            sma_config_masters.CM110: 'Master 11.0',
            sma_config_masters.CM105: 'Master 10.5',
            sma_config_masters.CM115: 'Master 11.5',
            sma_config_masters.CM117: 'Master 11.7',
        }

        if appliances in all_appliances_map:
            self._info(self.get_list_items(APPLIANCES_LIST))
            self.select_from_list(APPLIANCES_LIST,
                                  'label=%s' % all_appliances_map[appliances])
        else:
            Applainces = self.get_list_items(APPLIANCES_LIST)
            if 'Select appliances in list' not in Applainces:
                self.select_from_list(APPLIANCES_LIST,
                                      'label=Selected appliances...')
            else:
                self.select_from_list(APPLIANCES_LIST,
                                      'label=Select appliances in list')
            available_appliances = self._get_available_appliances_names()
            self._info(available_appliances)

            for appliance in self._convert_to_tuple(appliances):
                if appliance in available_appliances:
                    row = available_appliances.index(appliance) + 1
                    self.select_checkbox(APPLIANCES_CHECKBOX_CELL(row))
                else:
                    raise guiexceptions.GuiValueError(
                        '%s appliance is not in Appliances table' % \
                        (appliance,))

    def _select_start_time(self, start_time):
        try:
            s_date, s_time = start_time.split()
        except ValueError:
            raise guiexceptions.GuiValueError(
                'Start time should be in `MM/DD/YYYY HH:MM` format')
        else:
            self.input_text(DATE_FIELD, s_date)
            self.input_text(TIME_FIELD, s_time)

    def _click_publish_button(self):
        self.click_button(PUBLISH_BUTTON, 'dont wait')

        if self._is_element_present(CONTINUE_PUBLISH_BUTTON):
            self.click_button(CONTINUE_PUBLISH_BUTTON, 'dont wait')

    def _get_status(self):
        # wait for results
        timeout = 120
        interval = 1
        for i in xrange(0, timeout, interval):
            if not (self._is_text_present("Establishing Connection")
                    or self._is_text_present("Connection Established")
                    or self._is_text_present("Sending Data")):
                # until() returns True we got what we wait for
                break
            time.sleep(interval)

        time.sleep(1)
        if int(self.get_matching_xpath_count(STATUS_TABLE)) > 0:
            _status_rows = STATUS_TABLE + "/tbody/tr"
            _status_rows_count = int(self.get_matching_xpath_count(_status_rows))
            if _status_rows_count < 1:
                return None
            else:
                _appl_status = {}
                self._debug("_status_rows_count: %s" % (_status_rows_count,))
                _appl_count = range(1, 1 + _status_rows_count)
                self._debug("_appl_count: %s" % (_appl_count,))
                for row in range(1, 1 + _status_rows_count):
                    self._debug("row: %s" % (row,))
                    _status_row = _status_rows + "[" + str(row) + "]"
                    self._debug("_status_row: %s" % (_status_row,))
                    _appliance = self.get_text(_status_row + "/td[1]")
                    self._debug("_appliance: %s" % (_appliance,))
                    _status = self.get_text(_status_row + "/td[3]")
                    self._debug("_status: %s" % (_status,))
                    _appl_status[_appliance] = _status
                    self._debug("_appl_status: %s" % (_appl_status,))
                return _appl_status
        else:
            self._info("status table %s was not found" % (STATUS_TABLE,))
            return None

    def _fill_publish_page(self, job_name, master, filepath, appliances,
                           start_time):

        self._select_job_name(job_name)

        if master is not None:
            master = re.sub('Configuration Master', '', master)
            self._select_configuration_master(master.strip())

        if filepath is not None:
            self._select_file_to_publish(filepath)

        self._select_appliances(appliances)

        if start_time is not None:
            self._select_start_time(start_time)

    def _publish_configuration(self, publish_now, job_name, master, filepath,
                               appliances, start_time=None):

        publish_button = PUBLISH_NOW_BUTTON if publish_now else \
            SCHEDULE_PUBLISH_BUTTON

        self._open_page()

        self.click_button(publish_button)

        self._fill_publish_page(job_name, master, filepath, appliances,
                                start_time)

        self._click_publish_button()

        if publish_now:
            return self._get_status()

    def publish_to_web_appliances_configuration_master_now(self, job_name,
                                                           master, appliances):
        """Publish Configuration Master to web appliances.

        Parameters:
        - `job_name`: name for the job. 'system-generated' to let the system
           generate the job name or any other string which will be used as
           job name.
        - `master`: configuration master name to publish. Can be one of
           sma_config_masters constants from sma/constants.py file.
        - `appliances`: appliances to publish master to. 'All' to publish to
           all assigned aplliances, string of comma-separated names of the
           appliances to publish to specific appliances.

        Return:
            A dictionary with appliance names (as keys) and
            publishing statuses (as values) for them.
            'None' is returned if no publishing results.

        Examples:
        | Publish To Web Appliances Configuration Master Now | myjob |
        | ... | ${sma_config_masters.CM80} | All |
        | Publish To Web Appliances Configuration Master Now |
        | ... | system-generated | ${sma_config_masters.CM77} | wsa0, wsa1 |

        Exceptions:
        - `GuiValueError`: in case of invalid Configuration Master or appliance
           name.
        - `GuiFeatureDisabledError`: in case Configuration Masters are not
           initialized.
        """
        return self._publish_configuration(True, job_name, master, None, appliances)

    def publish_to_web_appliances_configuration_file_now(self, job_name,
                                                         filepath, appliances):
        """Publish configuration file to web appliances.

        Parameters:
        - `job_name`: name for the job. 'system-generated' to let the system
           generate the job name or any other string which will be used as
           job name.
        - `filepath`: path to configuration file to publish.
        - `appliances`: appliances to publish file to. Either a string of
           comma-separated names of the appliances or configuration master
           name to publish file to all appliances assigned to given master.
           Master can be one of sma_config_masters constants from
           sma/constants.py file.

        Return:
            A dictionary with appliance names (as keys) and
            publishing statuses (as values) for them.
            'None' is returned if no publishing results.

        Examples:
        | Publish To Web Appliances Configuration File Now | myjob |
        | ... | /home/testuser/wsaconfig.xml | wsa0, wsa1 |
        | Publish To Web Appliances Configuration File Now | system-generated |
        | ... | /home/testuser/wsaconfig.xml | ${sma_config_masters.CM77} |

        Exceptions:
        - `GuiValueError`: in case of invalid Configuration Master or appliance
           name.
        - `GuiFeatureDisabledError`: in case Configuration Masters are not
           initialized.
        """
        return self._publish_configuration(True, job_name, None, filepath, appliances)

    def publish_to_web_appliances_configuration_master_schedule(self, job_name,
                                                                start_time, master, appliances):
        """Schedule publish of Configuration Master to web appliances.

        Parameters:
        - `job_name`: name for the job. 'system-generated' to let the system
           generate the job name or any other string which will be used as
           job name.
        - `start_time`: date and time in 'MM/DD/YYYY HH:MM' format when to
           publish the Configuration Master.
        - `master`: configuration master name to publish. Either configuration
           master name or one of sma_config_masters constants from
           sma/constants.py file.
        - `appliances`: appliances to publish master to. 'All' to publish to
           all assigned aplliances, string of comma-separated names of the
           appliances to publish to specific appliances.

        Examples:
        | Publish To Web Appliances Configuration Master Schedule | myjob |
        | ... | 01/11/2011 14:12 | ${sma_config_masters.CM80} | All |
        | Publish To Web Appliances Configuration Master Schedule |
        | ... | system-generated | 01/11/2011 14:12 |
        | ... | ${sma_config_masters.CM80} | wsa1 |

        Exceptions:
        - `GuiValueError`: in case of invalid Configuration Master, appliance
           name or malformed `start_time`.
        - `GuiFeatureDisabledError`: in case Configuration Masters are not
           initialized.
        """
        self._publish_configuration(False, job_name, master, None, appliances,
                                    start_time)

    def publish_to_web_appliances_configuration_file_schedule(self, job_name,
                                                              start_time, filepath, appliances):
        """Schedule publish of configuration file to web appliances.

        Parameters:
        - `job_name`: name for the job. 'system-generated' to let the system
           generate the job name or any other string which will be used as
           job name.
        - `start_time`: date and time in 'MM/DD/YYYY HH:MM' format when to
           publish configuration file.
        - `filepath`: path to configuration file to publish.
        - `appliances`: appliances to publish file to. Either a string of
           comma-separated names of the appliances or configuration master
           name to publish file to all appliances assigned to given master.
           Master can be one of sma_config_masters constants from
           sma/constants.py file.

        Examples:
        | Publish To Web Appliances Configuration File Schedule |
        | ... | system-generated | 12/15/2011 23:00 |
        | ... | /home/testuser/config.xml | ${sma_config_masters.CM77} |
        | Publish To Web Appliances Configuration File Schedule |
        | ... | myjobname | 12/15/2011 23:00 |
        | ... | /home/testuser/config.xml | wsa0, wsa1 |

        Exceptions:
        - `GuiValueError`: in case of invalid appliance name or malformed
          `start_time`.
        - `GuiFeatureDisabledError`: in case Configuration Masters are not
           initialized.
        """
        self._publish_configuration(False, job_name, None, filepath,
                                    appliances, start_time)

    def publish_to_web_appliances_get_scheduled_jobs(self):
        """Get the list of scheduled jobs.

        *Parameters:*
            None

        *Return:*
        - list of scheduled jobs.

        *Examples:*
        | ${result} | Publish To Web Appliances Get Scheduled Job |

        *Exceptions:*
            None
        """
        self._info('publish_to_web_appliances_get_scheduled_jobs')
        self._open_page()
        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(SCHEDULED_JOBS_LINK))

        for row in xrange(0, num_of_entries):
            job_name = self.get_text(SCHEDULED_JOB_NAME_LINK(row, ))
            job_time = self.get_text(SCHEDULED_JOB_FIELD_LINK(row, 2, ))
            job_cm = self.get_text(SCHEDULED_JOB_FIELD_LINK(row, 3, ))
            job_appliances = self.get_text(SCHEDULED_JOB_FIELD_LINK(row, 4, ))
            entries[job_name] = [job_time, job_cm, job_appliances]
        return entries

    def publish_to_web_appliances_delete_scheduled_job(self, job_name_for_deletion=None):
        """Delete a scheduled job.

        *Parameters:*
        - `job_name_for_deletion`: job which will be deleted.

        *Return:*
        - `True`: when job was deleted successfully.
        - `False`: in other cases.

        *Examples:*
        | ${result} | Publish To Web Appliances Delete Scheduled Job |
        | ... | special_job |

        *Exceptions:*
            None
        """
        self._info('publish_to_web_appliances_delete_scheduled_job')
        self._open_page()
        num_of_entries = int(self.get_matching_xpath_count(SCHEDULED_JOBS_LINK))
        for row in xrange(0, num_of_entries):
            job_name = self.get_text(SCHEDULED_JOB_NAME_LINK(row, ))
            if job_name == job_name_for_deletion:
                self.click_element(DELETE_JOB_LINK(row), "Don't wait")
                self._click_continue_button()
                return True
        return False

#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/services/pac_file_hosting.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

EXP_CHECKBOX = 'pac_expire'
UPLOAD_FIELD = lambda index: 'uploaded_files[%d][FILE]' % (index,)
PAC_TABLE = lambda table_id: "//table[@id=\'%s\']" % (table_id,)
PAC_ITEM = lambda table_name, index, table_column: ('%s//tr[%s]//td[%d]' % \
                                         (table_name, index, table_column,))
PAC_DEL = lambda index, delete_column: \
          "//table[@class='itable layout-bare']//tr[%s]//td[%s]/img" % \
                                                  (index, delete_column)
HOSTNAME_FIELD = lambda row: 'hostname_pac[%d][hostname]' % (row,)
PAC_FILE_ID = lambda row: 'hostname_pac[%d][pacfile]' % (row,)
PAC_FILE_ERROR= "css=div.bd"


class PacFileHosting(GuiCommon):
    """PAC File Hosting page interaction class.

    This class designed to interact with GUI elements of 'Services' ->
    'PAC File Hosting' page.
    """

    def get_keyword_names(self):
        return ['pac_file_hosting_disable',
                'pac_file_hosting_enable',
                'pac_file_hosting_add_pac_file',
                'pac_file_hosting_delete_pac_file',
                'pac_file_hosting_add_host',
                'pac_file_hosting_delete_host',
                'pac_file_hosting_edit_settings',]

    def _open_page(self):
        """Open 'PAC File Hosting' """

        self._navigate_to('Security Services', 'PAC File Hosting')

    def _enable_or_edit(self):
        """Enable or click edit button for PAC file hosting."""

        enable_pac_button =\
            "xpath=//input[@value='Enable and Edit Settings...']"
        if self._check_feature_status(feature='pac_file_hosting'):
            self._click_edit_settings_button()
        else:
            self.click_button(enable_pac_button)

    def _set_pac_server_ports(self, ports=None):

        pac_server_ports_field = 'pacPorts'
        if ports is not None:
            self.input_text(pac_server_ports_field, ports)

    def _allow_pac_file_expiration(self, exp_allow=None):

        if exp_allow is not None:
            if exp_allow:
                if not self._is_checked(EXP_CHECKBOX):
                    self.click_button(EXP_CHECKBOX, "don't wait")
                else:
                    return
            else:
                self.unselect_checkbox(EXP_CHECKBOX)

    def _set_pac_file_exp_interval(self, exp_interval=None):

        exp_interval_field = 'pac_expiration_interval'
        if exp_interval is not None:
            if not self._is_checked(EXP_CHECKBOX):
                raise guiexceptions.GuiFeatureDisabledError\
                                  ('Cannot set PAC file interval')
            self.input_text(exp_interval_field, exp_interval)

    def _upload_pac_file(self, add_file=None):

        upload_pac_button =\
            "xpath=//input[@value='Upload']"

        add_row_button = 'uploaded_files_domtable_AddRow'
        if add_file is not None:
            add_file = self._convert_to_tuple(add_file)
            for i, pac_file in enumerate(add_file):
                if i != 0:
                     self.click_button(add_row_button, "don't wait")
                self.choose_file(UPLOAD_FIELD(i), pac_file)
            self.click_button(upload_pac_button)

    def _get_pac_file_row_index(self, name,\
                                table_id="uploaded_files", table_column=1):

        table_rows = int(self.get_matching_xpath_count('%s//tr' %\
                                                   (PAC_TABLE(table_id))))
        for i in xrange(2, table_rows):
            pac_file_name = \
            self.get_text(PAC_ITEM(PAC_TABLE(table_id), i, table_column)).\
                                                            split('\n')[0]
            if name in pac_file_name:
                return i
        return None

    def pac_file_hosting_delete_pac_file(self, filename=None):
        """Delete Proxy Auto-Configuration File(s).

        Parameters:
        - `filename`: string with comma separated file names to be deleted.

        Example:
        | Pac File Hosting Delete Pac File | filename=file1.js |
        | Pac File Hosting Delete Pac File | filename=file1.js, file2.js |
        """
        if filename is not None:
            self._perform_delete_operation(names=filename,
                                           check_for_default_pac_file=True)

    def pac_file_hosting_delete_host(self, host=None):
        """Delete hostname(s).

        Parameters:
        - `host`: string with comma separated host names to be deleted.

        Example:
        | Pac File Hosting Delete Host | host=test.com |
        | Pac File Hosting Delete Host | host=test1.com, test2.com |
        """
        if host is not None:
            self._perform_delete_operation(delete_column=3, names=host,
                                               table_id="hostname_pac")

    def _perform_delete_operation(self,
                                  delete_column=2,
                                  names=None,
                                  table_id="uploaded_files",
                                  check_for_default_pac_file=False):

        self._open_page()
        # check if PAC file hosting is disabled or not
        if not self._check_feature_status(feature='pac_file_hosting'):
            raise guiexceptions.GuiFeatureDisabledError\
             ('Cannot perform delete operation as PAC file hosting '\
                                                       'is disabled')
        self._click_edit_settings_button()
        names = self._convert_to_tuple(names)
        for name in names:
            row_index = self._get_pac_file_row_index(name, table_id)
            if row_index is None:
                raise guiexceptions.GuiControlNotFoundError\
                          ('\'%s\'' % (name,), 'PAC File Hosting')
            # check PAC file in Hostname table
            if check_for_default_pac_file:
                file_row_host = self._get_pac_file_row_index\
                                (name, table_id="hostname_pac",
                                 table_column=2)
                if file_row_host is not None:
                    raise guiexceptions.GuiFeatureDisabledError\
                   ('Cannot perform delete operation as PAC file \'%s\' '\
                    'currently selected as the default PAC file for host(s)'\
                    % (name,))
            self.click_element(PAC_DEL(row_index, delete_column),
                               "don't wait")
        self._click_submit_button()

    def _delete_all_selected_data(self, data):

        if data.lower() == 'files':
            table_id = 'uploaded_files'
            delete_column = 2
        elif data.lower() == 'hosts':
            table_id = 'hostname_pac'
            delete_column = 3
        else:
            raise ValueError('Wrong argument. '\
                             'Should be either \'files\' or \'hosts\'')
        table_rows = int(self.get_matching_xpath_count('%s//tr' %\
                                                   (PAC_TABLE(table_id))))
        for i in xrange(2, table_rows):
            self.click_element(PAC_DEL(2, delete_column),
                               "don't wait")

    def pac_file_hosting_add_pac_file(self,
                                      filename=None):
        """Add Proxy Auto-Configuration File

        Parameters:
        - `filename`: string with comma separated PAC file(s)
                    location(s) to upload.

        Example:
        | Pac File Hosting Add Pac File | filename=${CURDIR}/file.js |
        | Pac File Hosting Add Pac File | filename=${CURDIR}/file1.js, ${CURDIR}/file2.js |
        | Pac File Hosting Add Pac File | filename=/home/username/work/file.js |
        | Pac File Hosting Add Pac File | filename=/home/username/work/file1.js, /home/username/work/file2.js |
        """
        self._open_page()
        # check if PAC file hosting is disabled or not
        if not self._check_feature_status(feature='pac_file_hosting'):
            raise guiexceptions.GuiFeatureDisabledError\
            ('Cannot perform add operation as PAC file hosting '\
                                                   'is disabled')
        self._click_edit_settings_button()
        self._upload_pac_file(add_file=filename)
        self._click_submit_button()

    def pac_file_hosting_enable(self,
                                add_file=None,
                                hosts=None,
                                ports=None,
                                exp_allow=None,
                                exp_interval=None):
        """Enable Proxy Auto-Configuration File Hosting Settings.

        Parameters:
        - `add_file`: string of comma separated PAC file location(s) to upload.
        - `hosts`: string with comma separated hostname:pac_file values.
        - `ports`: PAC server ports separated with a comma.
        - `exp_allow`: allow PAC file to expire in browser's cache.
                        True to allow, False to disallow.
        - `exp_interval`: PAC file expiration interval in Minutes, available if
                           'expiration_allow' is True.

        Example:
        | Pac File Hosting Enable | add_file=${CURDIR}/file1.js, ${CURDIR}/file2.js |
        | Pac File Hosting Enable | add_file=${CURDIR}/file1.js | hosts=test1.com:file1.js, test2.com:file1.js |
        | Pac File Hosting Enable | add_file=${CURDIR}/file1.js, ${CURDIR}/file2.js | hosts=test1.com:file1.js, test2.com:file2.js | ports=6002, 9002 | exp_allow=${False} |
        | Pac File Hosting Enable | add_file=/home/username/work/file1.js | ports=6002, 9002 | exp_allow=${False} |
        | Pac File Hosting Enable | add_file=/home/username/work/file1.js | ports=9002 | exp_allow=${True} | exp_interval=20 |
        """
        self._open_page()
        self._enable_or_edit()
        if add_file is not None and add_file != "None":
            self._upload_pac_file(add_file)
        if hosts is not None and hosts != "None":
            host_dict = dict((hostname, pac) for hostname, pac in (host.split(':')\
                        for host in self._convert_to_tuple(hosts)))
            self._add_host_for_serving_pac_files(host_dict)
        if ports is not None and ports != "None":
            self._set_pac_server_ports(ports)
        if exp_allow is not None and exp_allow != "None":
            self._allow_pac_file_expiration(exp_allow)
        if exp_interval is not None and exp_interval != "None":
            self._set_pac_file_exp_interval(exp_interval)
        if add_file is not None and add_file != "None":
            self._click_submit_button()
        else:
            self._click_submit_button(wait=False)


    def pac_file_hosting_edit_settings(self,
                                       ports=None,
                                       exp_allow=None,
                                       exp_interval=None):
        """Edit Proxy Auto-Configuration File Hosting Settings.

        Parameters:
        - `ports`: PAC server ports separated with a comma.
        - `exp_allow`: allow PAC file to expire in browser's cache.
                        True to allow, False to disallow.
        - `exp_interval`: PAC file expiration interval in Minutes, available if
                           'expiration_allow' is True.

        Example:
        | Pac File Hosting Edit Settings | ports=9001, 5002 |
        | Pac File Hosting Edit Settings | ports=9001, 5002 | exp_allow=${True} | exp_interval=20 |
        """
        self._open_page()
        # Check if PAC file hosting already disabled
        if not self._check_feature_status(feature='pac_file_hosting'):
            raise guiexceptions.GuiFeatureDisabledError\
                  ('Cannot edit PAC file hosting as disabled')
        self._click_edit_settings_button()
        self._set_pac_server_ports(ports)
        self._allow_pac_file_expiration(exp_allow)
        self._set_pac_file_exp_interval(exp_interval)
        self._click_submit_button()

    def pac_file_hosting_disable(self):
        """Disable Proxy Auto-Configuration file hosting

        Example:
        | Pac File Hosting Disable |
        """
        pac_checkbox = 'enabled'
        self._open_page()
        # Check if PAC file hosting already disabled
        if not self._check_feature_status(feature='pac_file_hosting'):
            return
        self._click_edit_settings_button()
        # Cleaning all hosts and files before disabling.
        self._delete_all_selected_data('hosts')
        self._delete_all_selected_data('files')
        self.unselect_checkbox(pac_checkbox)
        self._click_submit_button()

    def _check_current_pacfiles(self, pacfile):

        current_files = self.get_list_items(PAC_FILE_ID(0))
        for filename in current_files:
            if pacfile in filename:
                return True
        else:
            raise ValueError, '"%s" is not a valid PAC file' % (pacfile,)

    def _add_host_for_serving_pac_files(self, host_dict=None):

        add_pac_row_button = 'hostname_pac_domtable_AddRow'
        if host_dict is not None:
            row = 0
            for host, pacfile in host_dict.items():
                if self._check_current_pacfiles(pacfile):
                    # add row only if pac file is valid
                    if row != 0:
                         self.click_button(add_pac_row_button,
                                               "don't wait")
                    self.input_text(HOSTNAME_FIELD(row), host)
                    self.select_from_list(PAC_FILE_ID(row), pacfile)
                    row += 1

    def pac_file_hosting_add_host(self,
                     hosts=None):
        """Add Hostnames for Serving PAC Files Directly

        Parameters:
        - `hosts`: string with comma separated hostname:pac_file values.

        Example:
        | Pac File Hosting Add Host | hosts=test1.com:file1.js, test2.com:file2.js |
        | Pac File Hosting Add Host | hosts=test.com:file.js |
        """

        host_dict = dict((hostname, pac) for hostname, pac in (host.split(':')\
                                for host in self._convert_to_tuple(hosts)))
        self._open_page()
        # Check if PAC file hosting already disabled
        if not self._check_feature_status(feature='pac_file_hosting'):
            raise guiexceptions.GuiFeatureDisabledError\
             ('Cannot add hostnames as PAC file hosting is disabled')
        self._click_edit_settings_button()
        self._add_host_for_serving_pac_files(host_dict)
        self._click_submit_button()

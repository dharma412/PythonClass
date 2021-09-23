#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/network/external_dlp_servers.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

DROP_GRP = lambda index: 'drop_customRadio_invalidGroup[%d]' % (index,)
MONITOR_GRP = lambda index: 'scan_customRadio_invalidGroup[%d]' % (index,)

load_balancing_option_dict = {
    'failover': "None (Failover)",
    'fewest'  : "Fewest Connections",
    'hash'    : "Hash Based",
    'round'   : "Round Robin"
}

failure_handling_dict = {
    'permit': "failure_handling_continue",
    'block': "failure_handling_drop"
}

SEVER_ADDRESS_FIELD = lambda index: "ext_servers[%s][host]" % index
PORT_FIELD = lambda index: "ext_servers[%s][port]" % index
RECONNECTION_ATTEMPTS_FIELD = lambda index: "ext_servers[%s][reconnect_count]" % index
SERVICE_URL_FIELD = lambda index: "ext_servers[%s][url]" % index
USE_CERT_FIELD = lambda index: "ext_servers[%s][certIsForAll]" % index
CERT_BROWSE_BUTTON= lambda index: "ext_servers[%s][uploadCertFile]" % index
CERT_UPLOAD_BUTTON= lambda index: "ext_servers[%s][uploadFiles]" % index
SERVER_DELETE_ICON = lambda index: "xpath=//tr[@id='ext_servers_row%d']/td[2]/img" % index
SETTINGS_VALUE = lambda  row:'//table[@class=\'pairs\']/tbody/tr[%s]/td[1]' % str(row)
SETTINGS_NAME = lambda  row:'//table[@class=\'pairs\']/tbody/tr[%s]/th[1]' % str(row)

class ExternalDlpServers(GuiCommon):
    """Gui configurator for 'Network -> External DLP Servers' page.
    """

    invalid_cert_keys_global = ['expired',
                     'mismatched',
                     'unrecognized',
                     'invalid_signing',
                     'invalid_leaf',
                     'other',
                     'select_all']

    def get_keyword_names(self):

        return [
                'external_dlp_servers_edit_servers',
                'external_dlp_servers_delete_all_servers',
                'external_dlp_servers_start_test',
                'external_dlp_servers_edit_settings',
                'external_dlp_servers_get_settings',
                'invalid_certificate_handling',
                'upload_server_certificate',
                'delete_server_certificate',
                ]

    def _open_page(self):
        """Go to ' Network -> External DLP Servers' configuration page """

        self._navigate_to('Network', 'External DLP Servers')

    def _fill_in_server_info(self, servers, start_index, secureIcap, server_cert=None):
        add_row_button = "ext_servers_domtable_AddRow"
        servers = self._convert_to_tuple(servers)
        #Commented by selvans
        #if start_index != 0:
        #    start_index = start_index - 1
        for i, server in enumerate(servers):
            server = server.split('%')
            entry = i + start_index
            if entry != 0:
                #Edited by selvans- add a new server after existing server row
                self.click_button(add_row_button, "don't wait")
            self.input_text(SEVER_ADDRESS_FIELD(entry), server[0])
            self.input_text(PORT_FIELD(entry), server[1])
            self.input_text(RECONNECTION_ATTEMPTS_FIELD(entry), server[2])
            self.input_text(SERVICE_URL_FIELD(entry), server[3])
            if secureIcap == "Secure ICAP":
                #Edited by selvans, in case client cert is not present
                self._set_use_cert(server[4],entry)
                if  server[5]:
                    self._info('Debug: %s server[5] value' % server[5])
                    self._info('Debug:No client cert passed')
                else:
                    self._info('Debug: %s server[5] value' % server[5])
                    self._upload_cert(server[5],entry)

        if secureIcap == "Secure ICAP":
            self._upload_server_cert(server_cert)

    def upload_server_certificate(self,server_cert):
        self._open_page()
        self._click_edit_settings_button()
        self._upload_server_cert(server_cert)


    def _upload_server_cert(self, server_cert):
        BROWSE="//input[@id='certificate']"
        UPLOAD="//input[@id='uploadServerFiles']"
        if server_cert:
            self.choose_file(BROWSE, server_cert)
            self.click_button(UPLOAD)
            self.check_for_warning()

    def _select_secureIcap(self, value):
        secure_icpa_list="//select[@id='icap_secure']"
        self.select_from_list(secure_icpa_list, value)

    def _upload_cert(self, cert,index):
        BROWSE=CERT_BROWSE_BUTTON(index)
        UPLOAD=CERT_UPLOAD_BUTTON(index)
        if cert:
            self.choose_file(BROWSE, cert)
            self.click_button(UPLOAD)
            self.check_for_warning()

    def delete_server_certificate(self):
        DELETE = "//*[@id='server_info']/dl/dd/table/tbody/tr[2]/td[4]/img"
        CONFIRM = '//button[text()="Delete"]'
        submit_button = "//input[@value='Submit']"
        self._open_page()
        self._click_edit_settings_button()
        self.click_element(DELETE,"don't wait")
        self.click_button(CONFIRM)
        self.check_for_warning()
        #No need of submit for server cert update
        #self.click_button(submit_button)


    def _set_use_cert(self,enable,index):
        CHECKBOX=USE_CERT_FIELD(index)
        if enable and not self._is_checked(CHECKBOX):
            self._info("Enabling use this certificate for all DLP servers using Secure ICAP checkbox")
            self.click_element(CHECKBOX, "don't wait")
        if not enable and self._is_checked(CHECKBOX):
            self._info("Disabling File Reputation Filtering ...")
            self.click_element(CHECKBOX, "don't wait")

    def _select_load_balancing(self, load_balancing):
        load_balancing_option_button = "load_balancing"
        if load_balancing is not None:
            self.select_from_list(load_balancing_option_button,
                          load_balancing_option_dict[load_balancing.lower()])

    def _fill_in_service_request_timeout(self, timeout):
        service_timeout_field = "service_request_timeout"
        if timeout is not None:
            self.input_text(service_timeout_field, timeout)

    def _fill_in_maximum_connections(self, max_connections):
        max_connections_field = "maxIcapServerConnects"
        if max_connections is not None:
            self.input_text(max_connections_field, max_connections)

    def _configure_failure_handling(self, failure_handling):
        if failure_handling is not None:
            self._click_radio_button(
                failure_handling_dict[failure_handling.lower()])

    def _delete_all_server(self):
        num_server = self._get_number_of_configured_server()
        if num_server == 1:
            self.click_element(SERVER_DELETE_ICON(0), "don't wait")
        else:
            for i in range(num_server):
                self.click_element(SERVER_DELETE_ICON(i), "don't wait")
        return num_server

    def _get_number_of_configured_server(self):
        dlp_server_table = "//table[@id='ext_servers']//td[@class='itable-cell left']"
        num_server =  int(self.get_matching_xpath_count(dlp_server_table))
        if num_server == 1 and not self.get_value(SEVER_ADDRESS_FIELD(0)):
        # There is alway one entry in the 'External DLP Servers:' table.  Need
        # to check to see if it is an empty entry or a defined entry.  If
        # 'Server Address' field of this first entry is empty, number of
        # configured server is 0.
            num_server = 0
        self._info('%d currently configured DLP server' % num_server)
        return num_server

    def external_dlp_servers_get_settings(self):
        """Get External DLP Settings.
        Parameters:
            None.
        Return:
            Dictionary keys of which are names of settings.
        Example:
        | ${result} | External DLP Get Settings |
        """

        self._open_page()
        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(\
                SETTINGS_NAME('*'))) + 1
        for row in xrange(1, num_of_entries):
            if not(self._is_element_present(SETTINGS_VALUE(row))):
                continue
            entries[self.get_text(SETTINGS_NAME(row))] =\
                    self.get_text(SETTINGS_VALUE(row))
        return entries

    def external_dlp_servers_edit_servers(self, servers, secureIcap=None, server_cert=None):
        """ Edits external DLP servers.
        Parameters:
           - `servers`: a string of comma separated or a list of the
                        following:
                        <address>%<port>%<reconn_attmp>%<icap://service_url>.
                        Note that % is used as delimitter.  All currently
                        configured DLP servers will be replaced by newly
                        specified DLP servers.
           - `secureIcap`: A string, Possible Value
                        1. Secure ICAP
                        2. ICAP
        Examples:
        | External DLP Servers Edit Servers | 1.1.1.1%1111%11%icap://one.one |
        | External DLP Servers Edit Servers | 1.1.1.1%1111%11%icap://one.one%True%%{SARF_HOME}/tests/testdata/cert.crt |secureIcap=Secure ICAP
        | External DLP Servers Edit Servers | 1.1.1.1%1111%11%icap://one.one, 2.2.2.2%2222%22%icap://two.two, 3.3.3.3%3333%33%icap://three.three |
        """

        submit_button = "//input[@value='Submit']"
        confirm_delete_button = "//button[@type=\'button\']"
        self._open_page()
        self._click_edit_settings_button()
        #Edited by selvans
        num_server = self._get_number_of_configured_server()
        #if num_server != 0:
        #    num_server = self._delete_all_server()
        #Done editing
        if secureIcap:
            self._select_secureIcap(secureIcap)
        self._fill_in_server_info(servers, num_server, secureIcap, server_cert)
        self._click_submit_button()

    def external_dlp_servers_delete_all_servers(self):
        """ Deletes all configured external DLP servers.
        Example:
        | External DLP Servers Delete All Servers |
        """

        submit_button = "//input[@value='Submit']"
        confirm_delete_button = "//button[@type=\'button\']"
        self._open_page()
        self._click_edit_settings_button()
        if self._get_number_of_configured_server() == 0:
            raise guiexceptions.GuiValueError('No configured DLP server to '
                                              'delete')
        self._delete_all_server()
        self._click_submit_button(wait=False, skip_wait_for_title=True)
        self._click_continue_button()

    def external_dlp_servers_start_test(self):
        """Tests DLP service for configured DLP server.
        Example:
        | External DLP Servers Start Test |
        """

        start_test_button = "ICAP_start_test"
        test_result_field = "ICAP_container"
        self._open_page()
        self._click_edit_settings_button()
        if not self._get_number_of_configured_server():
            raise guiexceptions.GuiValueError('No configured DLP server to '
                                              'test')
        self.click_button(start_test_button)
        while not self._is_visible(start_test_button):
            pass
        test_result =  self.get_text(test_result_field)
        self._info(test_result)
        if test_result.find('Errors occurred')  != -1:
            raise guiexceptions.ExternalDLPTestError('Test failed.  Check ' \
                'log run for more info')

    def external_dlp_servers_edit_settings(self,
                                           load_balancing = None,
                                           request_timeout = None,
                                           max_connections = None,
                                           failure_handling = None):
        """ Edits other settings for external DLP servers.
        Parameters:
           - `load_balancing`: type of load balancing if there are multiple
                               DLP servers.  Either 'failover', 'fewest',
                               'hash', or 'round'.
           - `request_timeout`: service request timeout.
           - `max_connections`: maximum simultaneous connections.
           - `failure_handling`: how to handle requests if all DLP servers
                                 fail.  Either 'permit' or 'block'.  Defaulted
                                 to 'permit'.
        Examples:
        | External DLP Servers Edit Settings | load_balancing=fewest | request_timeout=120 |
        | | max_connections=50 | failure_handling=permit |
        | External DLP Servers Edit Settings | load_balancing=round | failure_handling=block |
        """

        self._open_page()
        self._click_edit_settings_button()
        if self._get_number_of_configured_server() == 0:
            raise guiexceptions.GuiValueError("Can't change settings since " \
                "there is no configured DLP server")
        self._select_load_balancing(load_balancing)
        self._fill_in_service_request_timeout(request_timeout)
        self._fill_in_maximum_connections(max_connections)
        self._configure_failure_handling(failure_handling)
        self._click_submit_button()

    def invalid_certificate_handling(self,
        err_expired=None,
        err_mismatched=None,
        err_unrecognized=None,
        err_invalidsigning=None,
        err_invalidleaf=None,
        err_other=None,
        err_select_all=None):
        """Sets invalid certificate handling options.
        - `err_expired`: expired certificate error. Either 'Drop'
                    'or 'Monitor'.
        - `err_mismatched`: mismatched hostname certificate error.
                    One of 'Drop'or 'Monitor'.
        - `err_unrecognized`: unrecognized root authority certificate error.
                    One of 'Drop' or 'Monitor'.
        - `err_invalidsigning`: Invalid signing certificate error.
                    One of 'Drop' or 'Monitor'.
        - `err_invalidleaf`: Invalid leaf certificate error.
                    One of 'Drop' or 'Monitor'.
        - `err_other`: all other error types of certificate errors.
                One of 'Drop' or 'Monitor'.
        - `err_select_all`: to click 'Select all' for invalid certificate
                    handling.
                    One of 'Drop' or 'Monitor'.
        """

        self._open_page()
        self._click_edit_settings_button()
        invalid_cert_values = [err_expired,
                               err_mismatched,
                               err_unrecognized,
                               err_invalidsigning,
                               err_invalidleaf,
                               err_other,
                               err_select_all]
        if err_select_all is not None:
            invalid_cert_handling = dict(zip(self.invalid_cert_keys_global,
                                             invalid_cert_values))
        else:
            invalid_cert_keys = self.invalid_cert_keys_global[:-1]
            invalid_cert_values = invalid_cert_values[:-1]
            if any(invalid_cert_values):
                invalid_cert_handling = dict(zip(invalid_cert_keys,
                                                 invalid_cert_values))
            else:
                invalid_cert_handling = None
        if invalid_cert_handling:
            if 'select_all' in invalid_cert_handling.keys():
                self._invalid_certificate_handling_select_all\
                  (invalid_cert_select_all=invalid_cert_handling['select_all'])
            else:
                self._invalid_certificate_by_cert_error\
                                  (invalid_cert_handling=invalid_cert_handling)
        self._click_submit_button()

    def _invalid_certificate_by_cert_error(self, invalid_cert_handling=None):
        invalid_cert_keys = {
                 'expired': (DROP_GRP(0), MONITOR_GRP(0),),
                 'mismatched': (DROP_GRP(1), MONITOR_GRP(1),),
                 'unrecognized': (DROP_GRP(2), MONITOR_GRP(2),),
                 'invalid_signing': (DROP_GRP(3), MONITOR_GRP(3),),
                 'invalid_leaf': (DROP_GRP(4), MONITOR_GRP(4),),
                 'other': (DROP_GRP(5), MONITOR_GRP(5),)}
        action_index = {'drop': 0, 'monitor': 1}
        if invalid_cert_handling:
            for cert_error, cert_action in invalid_cert_handling.iteritems():
                if cert_error.lower() not in invalid_cert_keys.keys():
                    raise ValueError\
                      ('Invalid Cert. error \'%s\' for Invalid Certificate '\
                        'Handling. Here are the valid certificate errors '\
                        '%s' % (cert_error, invalid_cert_keys.keys()))
                if cert_action is None:
                    continue
                if cert_action.lower() not in action_index.keys():
                    raise ValueError\
                          ('Invalid action \'%s\' for Invalid Certificate '\
                           'Handling. Here are the valid actions '\
                           '%s' % (cert_action, action_index.keys()))
                action = action_index[\
                         invalid_cert_handling[cert_error].lower()]
                self.click_element(invalid_cert_keys[cert_error][action],
                                   "don't wait")

    def _invalid_certificate_handling_select_all(self,
                                                invalid_cert_select_all=None):
        #select_all = {'drop': "//div[@id='link_select_all_1']",
        #              'monitor': "//div[@id='link_select_all_2']"}
        select_all = {'drop': "//tbody/tr[9]/td/table/tbody/tr[2]/th[1]/div/a/span",
                      'monitor': "//tbody/tr[9]/td/table/tbody/tr[2]/th[2]/div/a/span"}
        if invalid_cert_select_all:
            if invalid_cert_select_all.lower() not in select_all.keys():
                raise guiexceptions.ConfigError\
                      ('Invalid action \'%s\' for Invalid Certificate '\
                       'Handling. Here are the valid actions '\
                       '%s' % (invalid_cert_select_all, select_all.keys()))
            self.click_element(select_all[invalid_cert_select_all.lower()],
                               "don't wait")



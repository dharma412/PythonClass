# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/ampconfig.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import time
import clictorbase as ccb
from sal.deprecated.expect import REGEX, EXACT
from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO

DEFAULT = ccb.DEFAULT


class ampconfig(ccb.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln('ampconfig')
        self.clearbuf()
        self._expect(['requires activation', 'Choose the operation'])
        lines = self.getbuf()
        if self._expectindex == 0:
            self._wait_for_prompt()
            return -1
        if self._expectindex == 1:
            return ampconfigCASE(self._get_sess())


class ampconfigCASE(ccb.IafCliConfiguratorBase):
    def setup(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['use_malware_protection'] = ['to use File Reputation', YES]
        param_map['protection_license_agreement'] = ['license agreement?', YES]
        param_map['use_malware_file_analysis'] = ['to use File Analysis', YES]
        param_map['modify_filetypes'] = ['want to modify the file types selected for File Analysis', NO]
        param_map['change_filetypes'] = ['change selected File Types for File Analysis', NO]
        param_map['select_filetypes'] = ['supported File Types', DEFAULT]
        param_map['license_agreement'] = ['license agreement?', YES]
        param_map['protection_confirm_disable'] = [
            'The system will no longer check messages for malwares. Are you sure you want to disable?', YES]
        param_map['file_analysis_confirm_disable'] = [
            'The system will no longer run file analysis for malware scan. Are you sure you want to disable?', YES]
        param_map['upload_all_filetype'] = ['upload all filetypes supported by cloud service', YES]
        param_map['upload_msdownload'] = ["upload filetype 'application/x-msdownload'", YES]
        param_map['upload_dosexec'] = ["upload filetype 'application/x-dosexec'", YES]
        param_map['upload_msdos_program'] = ["upload filetype 'application/x-msdos-program'", YES]
        param_map['none_selected_proceed'] = ['None of the files will be uploaded for File Analysis.', YES]
        param_map['processing_timeout'] = ['processing timeout', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')
        return self._process_input(param_map)

    def advanced(self, input_dict=None, **kwargs):
        param_map1 = ccb.IafCliParamMap(end_of_command='file analysis server')
        param_map1['cloud_query_timeout'] = ['cloud query timeout', DEFAULT]
        param_map1['cloud_domain'] = ['cloud domain', DEFAULT]
        param_map1['cloud_server_pool'] = ['reputation cloud server pool', DEFAULT]
        param_map1['use_recommended_threshold'] = ['recommended reputation threshold', YES]
        param_map1['reputation_threshold'] = ['reputation threshold', DEFAULT]

        actual_dict = {}
        for key in kwargs.keys():
            if key in param_map1._map.keys():
                actual_dict[key] = kwargs[key]
        param_map1.update(input_dict or actual_dict)
        self._query_response('ADVANCED')
        self._process_input(param_map1, do_restart=False)

        lines = self.getbuf()
        if 'Choose a file analysis server' in lines:
            self._query_select_list_item(kwargs['file_analysis_server_select'])
            if kwargs['file_analysis_server_select'] == 'Private Cloud':
                self._query_response(kwargs['file_analysis_server_url'])
                self._query_select_list_item(kwargs['certificate_option'])
                if kwargs['certificate_option'] == 'Paste certificate to CLI':
                    self._expect([("Paste the certificate followed by a . on a new line", EXACT)], timeout=3)
                    self._sess_split(kwargs['paste_cert'])
                    self._sess.write("\n.\n")
        else:
            self._writeln(kwargs['file_analysis_server_url'])

        param_map2 = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map2['heartbeat_interval'] = ['heartbeat interval', DEFAULT]
        param_map2['enable_SSL_communication'] = ['enable SSL communication', YES]
        param_map2['change_proxy'] = ['change proxy detail', YES]
        param_map2['server_url'] = ['tunnel(proxy) server url', DEFAULT]
        param_map2['proxy_port'] = ['proxy port', DEFAULT]
        param_map2['username'] = ['Username', DEFAULT]
        param_map2['password'] = ['password', DEFAULT]

        actual_dict = {}
        for key in kwargs.keys():
            if key in param_map2._map.keys():
                actual_dict[key] = kwargs[key]
        param_map2.update(input_dict or actual_dict)
        self._query()
        return self._process_input(param_map2)

    def cachesettings(self, input_dict=None, **kwargs):
        self._query_response('CACHESETTINGS')
        return ampConfigCacheSettings(self._get_sess())

    def _sess_split(self, send_string):
        """ Workaround for a CLI bug that doesn't allow this script to send in
            large amounts of text at once. We split it up by line, delay a
            split second, then flush the input buffer after each line. """

        send_array = send_string.split("\n")
        for line in send_array:
            self._writeln(line)
            time.sleep(0.1)
            self._read_until('\n')
        self._writeln('')


class ampConfigCacheSettings(ccb.IafCliConfiguratorBase):

    def clearcache(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['clear_cache'] = ['to clear File Reputation Cache?', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('CLEARCACHE')
        return self._process_input(param_map)

    def modifytimeout(self, input_dict=None, **kwargs):
        self._query_response('MODIFYTIMEOUT')

        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')

        if kwargs.has_key('cache_clean'):
            param_map['cache_clean'] = ['clean', DEFAULT]
        if kwargs.has_key('cache_malicious'):
            param_map['cache_malicious'] = ['malicious', DEFAULT]
        if kwargs.has_key('cache_unknown'):
            param_map['cache_unknown'] = ['unknown', DEFAULT]
        if kwargs.has_key('timeout_duration'):
            param_map['timeout_duration'] = ['cache expiry period', DEFAULT]
        else:
            param_map['timeout_duration'] = ['cache expiry period', DEFAULT]

        actual_dict = {}
        for key in kwargs.keys():
            if key in param_map._map.keys():
                actual_dict[key] = kwargs[key]
        param_map.update(input_dict or actual_dict)
        self._query()
        return self._process_input(param_map)


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()
    asc = ampconfig(cli_sess)
    asc().setup()
    asc().advanced()
    asc().clearcache()
    asc().modifytimeout()

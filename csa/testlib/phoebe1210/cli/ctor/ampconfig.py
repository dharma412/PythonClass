# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/ampconfig.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

import re
import time
import clictorbase as ccb
from sal.deprecated.expect import REGEX, EXACT
from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO, is_yes

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
        if not 'modify_filetypes' in kwargs:
            return self._process_input(param_map)
        else:
            if kwargs['modify_filetypes'].lower() == 'no':
                return self._process_input(param_map)
            else:
                param_map1 = ccb.IafCliParamMap(end_of_command='Enter comma separated numbers')
                param_map1['use_malware_protection'] = ['to use File Reputation', YES]
                param_map1['use_malware_file_analysis'] = ['to use File Analysis', YES]
                param_map1['modify_filetypes'] = ['want to modify the file types selected for File Analysis', NO]
                param_map1['protection_license_agreement'] = ['license agreement?', YES]
                actual_dict = {}
                for key in kwargs.keys():
                    if key in param_map1._map.keys():
                        actual_dict[key] = kwargs[key]
                param_map1.update(input_dict or actual_dict)
                self._process_input(param_map1, do_restart=False)

                if 'modify_filetypes' in kwargs and is_yes(kwargs['modify_filetypes']):
                    file_groups = kwargs['select_file_group'].split(',')
                    self._query_response(kwargs['select_file_group'])
                    for group in file_groups:
                        file_group_map = self._get_group_file_types_map(group, kwargs['select_filetypes'])
                        self._query_response(kwargs['select_file_action'])
                        self._query_response(self._parse_file_types(file_group_map[group]))
                        self._writeln('')

    def _get_group_file_types_map(self, group, file_types):
        files_map = {}
        if '|' in file_types:
            files = file_types.split('|')

            for file in files:
                (group, f_types) = file.split(':')
                files_map[group] = f_types
        else:
            files_map[group] = file_types

        return files_map

    def _parse_file_types(self, file_list):
        file_list = re.sub(r'\[|\]|\'|\"', '', file_list)
        return file_list

    def advanced(self, input_dict=None, **kwargs):
        param_map1 = ccb.IafCliParamMap(end_of_command='file analysis server')
        param_map1['cloud_query_timeout'] = ['cloud query timeout', DEFAULT]
        param_map1['file_reputation_server'] = ['file reputation server', DEFAULT]
        param_map1['cloud_domain'] = ['cloud domain', DEFAULT]
        param_map1['cloud_server_pool'] = ['reputation cloud server pool', DEFAULT]
        param_map1['use_recommended_analysis_threshold'] = ['recommended analysis threshold', DEFAULT]
        param_map1['analysis_threshold'] = ['Enter analysis threshold', DEFAULT]
        param_map1['heartbeat_interval'] = ['heartbeat interval', DEFAULT]
        param_map1['enable_SSL_communication'] = ['enable SSL communication', NO]
        param_map1['change_proxy'] = ['change proxy detail', YES]
        param_map1['server_url'] = ['tunnel(proxy) server url', DEFAULT]
        param_map1['proxy_port'] = ['proxy port', DEFAULT]
        param_map1['username'] = ['Username', DEFAULT]
        param_map1['password'] = ['passphrase', DEFAULT]
        param_map1['supress_alert'] = ['suppress the verdict update', DEFAULT]

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
                private_fa_config_type = str(kwargs['private_fa_config_type'])
                if private_fa_config_type == 'newconfig':
                    self._info("Entered New config")
                    if kwargs['private_tg_type'].lower() == 'delete':
                        self._query_response('DELETE')
                        self._query_response(kwargs['tg_priority'])
                        self._writeln()
                        self._expect(['configure a security certificate', 'Configure a new private analysis server'])
                        if self._expectindex == 0:
                            self._query_response(NO)
                        elif self._expectindex == 1:
                            self._writeln('1')
                        self._to_the_top(1)
                    else:
                        if kwargs['private_tg_type'].lower() == 'new':
                            self._query_response('NEW')
                            self._query_response(kwargs['tg_ip'])
                        elif kwargs['private_tg_type'].lower() == 'add':
                            self._query_response('ADD')
                            self._query_response(kwargs['tg_ip'])
                        elif kwargs['private_tg_type'].lower() == 'edit':
                            self._query_response('EDIT')
                            self._query_response(kwargs['tg_priority'])
                            self._query_response(kwargs['tg_ip'])
                        self._writeln()
                        self._expect(['configure a security certificate'])
                        if self._expectindex == 0:
                            self._query_response(YES)
                            if kwargs['certificate_option'] == 'Paste certificate to CLI':
                                self._query_response(2)
                                self._expect([("Paste the certificate followed by a . on a new line", EXACT)],
                                             timeout=3)
                                self._sess_split(kwargs['paste_cert'])
                                self._sess.write("\n.\n")
                            else:
                                self._query_response(1)
                        self._to_the_top(1)
                else:
                    self._writeln()
                    self._expect(['configure a security certificate'])
                    if self._expectindex == 0:
                        self._query_response(YES)
                        if kwargs['certificate_option'] == 'Paste certificate to CLI':
                            self._query_response(2)
                            self._expect([("Paste the certificate followed by a . on a new line", EXACT)], timeout=3)
                            self._sess_split(kwargs['paste_cert'])
                            self._sess.write("\n.\n")
                        else:
                            self._query_response(1)
                    self._to_the_top(1)
            else:
                self._to_the_top(1)
        else:
            self._writeln(kwargs['file_analysis_server_url'])
            self._to_the_top(1)

    def cachesettings(self, input_dict=None, **kwargs):
        self._query_response('CACHESETTINGS')
        return ampConfigCacheSettings(self._get_sess())

        param_map = ccb.IafCliParamMap(end_of_command='Enter comma separated numbers from the list of groups')
        param_map['use_malware_protection'] = ['to use File Reputation', YES]
        param_map['use_malware_file_analysis'] = ['to use File Analysis', YES]
        param_map['modify_filetypes'] = ['want to modify the file types selected for File Analysis', YES]
        param_map['license_agreement'] = ['license agreement?', YES]
        print "KWARGS", kwargs
        actual_dict = {}
        for key in kwargs.keys():
            if key in param_map._map.keys():
                actual_dict[key] = kwargs[key]
        param_map.update(input_dict or actual_dict)
        self._query_response('SETUP')
        self._process_input(param_map, do_restart=False)
        self._query_response(kwargs['select_file_group'])
        self.clearbuf()
        self._query_response('PRINT')
        out = self._read_until('Choose the operation you want to perform:')
        self._to_the_top(3)
        return out

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

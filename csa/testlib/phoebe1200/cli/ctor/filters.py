#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/filters.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
SARF CLI command: filters
"""
import clictorbase
from clictorbase import REQUIRED, DEFAULT, IafCliError, \
    IafCliConfiguratorBase, NO_DEFAULT

from sal.deprecated.expect import REGEX, EXACT
from sal.containers import cfgholder
from sal.containers.yesnodefault import YES, NO, is_yes

DEBUG = True


class filters(clictorbase.IafCliConfiguratorBase):
    class DuplicateFilterError(IafCliError):
        pass

    class LogsConfigureError(IafCliError):
        pass

    class FilterInvalidError(IafCliError):
        pass

    class FilterSyntaxError(IafCliError):
        pass

    class ProcessingError(IafCliError):
        pass

    class FilterNameError(IafCliError):
        pass

    class FileExistError(IafCliError):
        pass

    class EncodingError(IafCliError):
        pass

    class FileNameError(IafCliError):
        pass

    class FilterRangeError(IafCliError):
        pass

    level = 1

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('error occurred during processing', EXACT): self.ProcessingError,
            ('No logs currently configured', EXACT): self.LogsConfigureError,
            ('Duplicate filter name', EXACT): self.DuplicateFilterError,
            ('has been marked invalid', EXACT): self.FilterInvalidError,
            ('the file \S+ does not exist', REGEX): self.FileExistError,
            ('Invalid filter syntax', EXACT): self.FilterSyntaxError,
            ('pick a different encoding', EXACT): self.EncodingError,
            ('Invalid filter name', EXACT): self.FilterNameError,
            ('Invalid filename', EXACT): self.FileNameError,
            ('Invalid filter range', EXACT): self.FilterRangeError,
        })

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def new(self, script=REQUIRED):
        self._writeln('NEW')
        self._query_response(script + '\n' + '.')
        self._to_the_top(self.level)

    def delete(self, filter=REQUIRED):
        self._query_response('DELETE')
        self._query_response(filter)
        self._to_the_top(self.level)

    def import_filter(self, filename=DEFAULT, encoding=DEFAULT):
        self._query_response('IMPORT')
        self._query_response(filename)
        self._query_select_list_item(encoding)
        self._to_the_top(self.level)

    def export_filter(self, filename=DEFAULT, encoding=DEFAULT):
        self._query_response('EXPORT')
        self._query_response(filename)
        self._query_select_list_item(encoding)
        self._to_the_top(self.level)

    def move(self, filter_to_move=REQUIRED, target_filter=REQUIRED):
        self._query_response('MOVE')
        self._query_response(filter_to_move)
        self._query_response(target_filter)
        self._to_the_top(self.level)

    def filter_set(self, filter=DEFAULT, attribute=DEFAULT):
        self._query_response('SET')
        self._query_response(filter)
        self._query_select_list_item(attribute)
        self._to_the_top(self.level)

    def filter_list(self, parse=NO):
        self._query_response('LIST')
        self._expect('\n')
        raw = self._read_until('Choose the operation ')
        self._to_the_top(self.level)
        if parse:
            return self._parse_list_output(raw)
        return raw

    def detail(self, filter=REQUIRED):
        self._query_response('DETAIL')
        self._query_response(filter)
        self._expect('\n')
        raw = self._read_until('Choose the operation ')
        self._to_the_top(self.level)
        return raw

    def logconfig(self):
        self._query_response('LOGCONFIG')
        return filtersLogconfig(self._get_sess())

    def rollovernow(self, log_to_roll=REQUIRED):
        self._query_response('ROLLOVERNOW')
        self._query_select_list_item(log_to_roll)
        self._to_the_top(self.level)

    def _parse_list_output(self, raw):
        """ Return parsed filters as list of cfgholder objects.  """
        res = []
        lines = map(lambda l: l.split(), raw.splitlines()[2:-1])
        for line in lines:
            res.append(cfgholder.CfgHolder({'num': line[0],
                                            'active': line[1],
                                            'valid': line[2],
                                            'name': line[3],
                                            }))
        return res


class filtersLogconfig(clictorbase.IafCliConfiguratorBase):
    """filters -> Logconfig"""

    class ScanHostError(IafCliError):
        pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Failed to scan host', EXACT): self.ScanHostError,
        })

    def edit(self,
             log_to_edit=REQUIRED,
             method=DEFAULT,
             filename_to_log=DEFAULT,
             file_size=DEFAULT,
             file_numbers=DEFAULT,
             allow_alerts=DEFAULT,
             allow_time_based_rollover=DEFAULT,
             rollover_interval=DEFAULT,
             day_of_week=REQUIRED,
             time_of_day=REQUIRED,
             time_interval=DEFAULT,
             hostname=REQUIRED,
             port=DEFAULT,
             user_name=REQUIRED,
             password=REQUIRED,
             directory=REQUIRED,
             ssh_ver_protocol=DEFAULT,
             enable_key_checking=DEFAULT):

        def _is_time_based():
            self._query_response(allow_time_based_rollover)
            if is_yes(allow_time_based_rollover):
                index = self._query_select_list_item(rollover_interval)
                if index == 1:
                    self._query_response(time_interval)
                elif index == 2:
                    self._query_select_list_item(day_of_week)
                    self._query_response(time_of_day)

        self.level = 1
        self._query_parse_input_list()
        self._writeln('EDIT')
        self._query()
        self._select_list_item(log_to_edit)
        idx = self._query_select_list_item(method)
        if idx == 1:
            self._query_response(filename_to_log)
            self._query_response(file_size)
            self._query_response(file_numbers)
            self._query_response(allow_alerts)
            _is_time_based()
        elif idx == 2:
            self._query_response(hostname)
            self._query_response(user_name)
            self._query_response(password)
            self._query_response(directory)
            self._query_response(filename_to_log)
            self._query_response(file_size)
            _is_time_based()
        elif idx == 3:
            self._query_response(hostname)
            self._query_response(port)
            self._query_response(user_name)
            self._query_response(directory)
            self._query_response(filename_to_log)
            self._query_response(file_size)
            _is_time_based()
            self._query_select_list_item(ssh_ver_protocol)
            self._query_response(enable_key_checking)
        self._to_the_top(self.level + 1)


if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    filt = filters(cli_sess)

    filt().new(filter_script="test5: if (true) { log('testing_log'); }")
    filt().export_filter(export_file='file',
                         encoding='Korean (KS-C-5601/EUC-KR)')
    filt().delete(filter_to_delete='test5')
    filt().import_filter(import_file='file',
                         encoding='Traditional Chinese (Big 5)')
    print filt().list()
    print filt().detail(filter='test5')
    filt().set(filter='test5', attribute='Inactive')
    filt().new(filter_script="test1: if (true) { log('testing_log'); }")
    filt().move(filter_to_move='1', target_filter='2')
    filt().logconfig().edit(log_to_edit='1', method='SCP Push',
                            hostname='192.168.1.1', user_name='safr',
                            directory='dir', protocol='SSH1',
                            key_checking=YES, manual_auto='2',
                            ssh_key='ssh-rsa AAAAB3NzaC1yc2E')
    filt().logconfig().edit(log_to_edit='1', method='3',
                            hostname='192.168.1.1', user_name='safr',
                            directory='dir1', protocol='2', key_checking=YES,
                            manual_auto='2')
    filt().logconfig().edit(log_to_edit='1', method='FTP Push',
                            hostname='192.168.1.1', user_name='safr',
                            password='pass', directory='dir2')
    filt().logconfig().edit(log_to_edit='1', method='1')
    filt().logconfig().edit(log_to_edit='"testing_log"', method='3',
                            hostname='192.168.1.1', user_name='safr',
                            directory='dir3', protocol='SSH1',
                            key_checking=NO)
    filt().delete(filter_to_delete='test5')
    filt().delete(filter_to_delete='test1')

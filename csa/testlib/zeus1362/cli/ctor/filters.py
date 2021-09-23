#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/filters.py#1 $

"""
IAF 2 CLI command: filters
"""

# import clictorbase properly depending on automation or dev env
# if automation, import the classes and constants we'll need
try:
    import clictorbase
    from clictorbase import REQUIRED, DEFAULT, IafCliError, \
                                      IafCliConfiguratorBase
except ImportError:
    clictorbase = libipt_import('cli.ctor.clictorbase',
                                 os.environ['SW_VERSION'])

from iafframework.libiptimport import libipt_import
from sal.deprecated.expect import REGEX, EXACT
from sal.containers.yesnodefault import YES, NO

DEBUG = True

class filters(clictorbase.IafCliConfiguratorBase):
    # import classes and constants from here if we're in a dev env
    # so they'll be in the right scope
    try:
        IafCliConfiguratorBase
    except NameError:
        exec('from %s.cli.ctor.clictorbase import ' % os.environ['SW_VERSION'] +
         'IafCliConfiguratorBase, IafCliError, REQUIRED, DEFAULT')

    class DuplicateFilterError(IafCliError): pass
    class LogsConfigureError(IafCliError): pass
    class FilterInvalidError(IafCliError): pass
    class FilterSyntaxError(IafCliError): pass
    class ProcessingError(IafCliError): pass
    class FilterNameError(IafCliError): pass
    class FileExistError(IafCliError): pass
    class EncodingError(IafCliError): pass
    class FileNameError(IafCliError): pass

    level=1

    def __init__(self, sess):
        global REGEX, EXACT
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('error occurred during processing', EXACT) : self.ProcessingError,
            ('No logs currently configured', EXACT) : self.LogsConfigureError,
            ('Duplicate filter name', EXACT) : self.DuplicateFilterError,
            ('has been marked invalid', EXACT) : self.FilterInvalidError,
            ('the file \S+ does not exist', REGEX) : self.FileExistError,
            ('Invalid filter syntax', EXACT) : self.FilterSyntaxError,
            ('pick a different encoding', EXACT) : self.EncodingError,
            ('Invalid filter name', EXACT) : self.FilterNameError,
            ('Invalid filename', EXACT) : self.FileNameError
            })

    def __call__(self):
        self._writeln('filters')
        return self

    def new(self, filter_script=REQUIRED):
        self._writeln('NEW')
        self._query_response(filter_script+'\n'+'.')
        self._to_the_top(self.level)

    def delete(self, filter_to_delete=REQUIRED):
        self._query_response('DELETE')
        self._query_response(filter_to_delete)
        self._to_the_top(self.level)

    def import_filter(self, import_file=DEFAULT, encoding=DEFAULT):
        self._query_response('IMPORT')
        self._query_response(import_file)
        self._query_select_list_item(encoding)
        self._to_the_top(self.level)

    def export_filter(self, export_file=DEFAULT, encoding=DEFAULT):
        self._query_response('EXPORT')
        self._query_response(export_file)
        self._query_select_list_item(encoding)
        self._to_the_top(self.level)

    def move(self, filter_to_move=REQUIRED, target_filter=REQUIRED):
        self._query_response('MOVE')
        self._query_response(filter_to_move)
        self._query_response(target_filter)
        self._to_the_top(self.level)

    def set(self, filter=DEFAULT, attribute=DEFAULT):
        self._query_response('SET')
        self._query_response(filter)
        self._query_select_list_item(attribute)
        self._to_the_top(self.level)

    def list(self):
        self._query_response('LIST')
        self._expect('\n')
        raw = self._read_until('Choose the operation ')
        self._to_the_top(self.level)
        return raw

    def detail(self, filter=REQUIRED):
        self._query_response('DETAIL')
        self._query_response(filter)
        self._expect('\n')
        raw = self._read_until('Choose the operation ')
        self._to_the_top(self.level)
        return raw

    def logconfig(self):
        global filtersLogconfig
        self._query_response('LOGCONFIG')
        return filtersLogconfig(self._get_sess())

    def rollovernow(self, log_to_roll=REQUIRED):
        self._query_response('ROLLOVERNOW')
        self._query_select_list_item(log_to_roll)
        self._to_the_top(self.level)

class filtersLogconfig(clictorbase.IafCliConfiguratorBase):
    """filters -> Logconfig"""
    # import classes and constants from here if we're in a dev env
    # so they'll be in the right scope
    try:
        IafCliConfiguratorBase
    except NameError:
        exec('from %s.cli.ctor.clictorbase import ' % os.environ['SW_VERSION'] +
         'IafCliConfiguratorBase, IafCliError, REQUIRED, DEFAULT')

    class ScanHostError(IafCliError): pass

    def __init__(self, sess):
        global EXACT
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess) 
        self._set_local_err_dict({
            ('Failed to scan host', EXACT) : self.ScanHostError,
            })

    def edit(self, log_to_edit=REQUIRED, method=DEFAULT,
             filename_to_log=DEFAULT, file_size=DEFAULT,
             file_numbers=DEFAULT, hostname=REQUIRED, user_name=REQUIRED,
             password=REQUIRED, directory=REQUIRED, time_to_wait=DEFAULT,
             protocol=DEFAULT, key_checking=DEFAULT, manual_auto=DEFAULT,
             ssh_key=REQUIRED):
        self.level=1
        self._query_parse_input_list() 
        self._writeln('EDIT')
        self._query()
        self._select_list_item(log_to_edit)
        self._query_select_list_item(method)
        if (method == '1') | (method == 'FTP Poll'):
            self._query_response(filename_to_log)
            self._query_response(file_size)
            self._query_response(file_numbers)
        elif (method == '2') | (method == 'FTP Push'):
            self._query_response(hostname)
            self._query_response(user_name)
            self._query_response(password)
            self._query_response(directory)
            self._query_response(filename_to_log)
            self._query_response(time_to_wait)
            self._query_response(file_size)
        elif (method == '3') | (method == 'SCP Push'):
            self._query_response(hostname)
            self._query_response(user_name)
            self._query_response(directory)
            self._query_response(filename_to_log)
            self._query_response(time_to_wait)
            self._query_response(file_size)
            self._query_select_list_item(protocol)
            self._query_response(key_checking)

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

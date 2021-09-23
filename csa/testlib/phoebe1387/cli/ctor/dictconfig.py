#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/dictconfig.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

"""
SARF CLI command: dictconfig
"""
import clictorbase
from clictorbase import REQUIRED, DEFAULT, IafCliError, NO_DEFAULT, \
    IafCliParamMap, IafCliConfiguratorBase
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import is_yes

DEBUG = True

class dictconfig(clictorbase.IafCliConfiguratorBase):

    class DictionaryQuantityError(IafCliError): pass
    class DictionaryNameUseError(IafCliError): pass
    class DictionaryNameError(IafCliError): pass
    class WordError(IafCliError): pass
    class FileNameError(IafCliError): pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('not already be in use', EXACT): self.DictionaryNameUseError,
            ('may be composed of the', EXACT): self.DictionaryNameError,
            ('does not exist', EXACT): self.FileNameError,
            ('Illegal word', EXACT): self.WordError,
            ('Exceeded maximum of \S+ content dictionaries',
                                     REGEX): self.DictionaryQuantityError
            })

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def new(self,
            name=REQUIRED,
            file_import=DEFAULT,
            file_name=NO_DEFAULT,
            encoding=DEFAULT,
            regular_expr=NO_DEFAULT,
            turn_on_matching=DEFAULT,
            match_anyway=DEFAULT):
        # TODO
        # options for 'turn_on_matching' and 'match_anyway' are not seen in CLI,
        # but leaving them as is here in ctor as they don't break anything;
        # not adding them into corresponding keyword
        self._query_response('NEW')
        self._query_response(name)
        self._query_response(file_import)
        edit = dictconfigEdit(self._get_sess())
        if is_yes(file_import):
             if turn_on_matching:
                 edit.import_dict_main(file_name=file_name, encoding=encoding,
                 turn_on_matching=turn_on_matching)
             else:
                 edit.import_dict_main(file_name=file_name, encoding=encoding)
        else:
            self._writeln(regular_expr+'\n')
            if match_anyway:
                edit.check_matching(match_anyway=match_anyway)
            else:
                edit.check_matching()

    def delete(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['name']   = \
                        ['Enter the number of the dictionary', REQUIRED, True]
        param_map['confirm'] = ['will invalidate those filters', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('DELETE')
        return self._process_input(param_map)

    def rename(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['name']   = \
                             ['dictionary you want to rename', REQUIRED, True]
        param_map['confirm'] = ['will invalidate those filters', DEFAULT]
        param_map['new_name']         = ['Enter a new name', REQUIRED]
        param_map.update(input_dict or kwargs)

        self._query_response('RENAME')
        return self._process_input(param_map)

    def edit(self, name=REQUIRED):
       self._query_response('EDIT')
       self._query_select_list_item(name)
       return dictconfigEdit(self._get_sess())

class dictconfigEdit(clictorbase.IafCliConfiguratorBase):
    """dictconfig -> Edit"""

    class FileImportNameError(IafCliError): pass
    class WordMatchingError(IafCliError): pass
    class WordQuantityError(IafCliError): pass
    class ImportError(IafCliError): pass
    class ExportError(IafCliError): pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
                ('maximum of \S+ words or regular',
                                       REGEX): self.WordQuantityError,
                ('should probably answer', EXACT): self.WordMatchingError,
                ('does not exist', EXACT): self.FileImportNameError,
                ('not importing', EXACT): self.ImportError,
                ('Export failed', EXACT): self.ExportError
                })

    def new(self, regular_expr=REQUIRED, match=DEFAULT):
        self._query_response('NEW')
        self._writeln(regular_expr+'\n')
        # TODO
        # option for 'match' is not seen in CLI,
        # but leaving it as is here in ctor as it doesn't break anything;
        # not adding into corresponding keyword.
        if match:
            self.check_matching(match=match)
        else:
            self.check_matching()

    def check_matching(self, input_dict=None, **kwargs):
        # TODO
        # may be not needed
        param_map = IafCliParamMap(end_of_command='to finish')

        param_map['match_anyway'] = ['word matching on anyway', DEFAULT]
        param_map.update(input_dict or kwargs)

        return self._process_input(param_map)

    def delete(self, dict_entry=REQUIRED):
        self.level=2
        self._query_response('DELETE')
        self._query_select_list_item(dict_entry)
        self._to_the_top(self.level)

    def settings(self, ignore_case=DEFAULT, match_words=DEFAULT,
                 encoding=DEFAULT):
        self.level=2
        self._query_response('SETTINGS')
        self._query_response(ignore_case)
        self._query_response(match_words)
        self._query_select_list_item(encoding)
        self._to_the_top(self.level)

    def print_dict(self):
        self.level=2
        self._query_response('PRINT')
        self._expect('\n')
        raw = self._read_until('Choose the operation ')
        self._to_the_top(self.level)
        return raw

    def export_dict(self, file_name=REQUIRED, encoding=DEFAULT):
        self.level=2
        self._query_response('EXPORT')
        self._query_response(file_name)
        self._query_select_list_item(encoding)
        self._to_the_top(self.level)

    def import_dict(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['file_name']        = ['to import', REQUIRED]
        param_map['encoding']         = ['encoding to use', DEFAULT, True]
        # TODO
        # option for 'turn_on_matching' is not seen in CLI,
        # but leaving it as is here in ctor as it doesn't break anything;
        # not adding into corresponding keyword.
        param_map['turn_on_matching'] = \
                                      ['turn on whole word matching', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('IMPORT')
        return self._process_input(param_map)

    def import_dict_main(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['file_name']        = ['to import', REQUIRED]
        param_map['encoding']         = ['encoding to use', DEFAULT, True]
        # TODO
        # option for 'turn_on_matching' is not seen in CLI,
        # but leaving it as is here in ctor as it doesn't break anything;
        # not adding into corresponding keyword.
        param_map['turn_on_matching'] = \
                                      ['turn on whole word matching', DEFAULT]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)
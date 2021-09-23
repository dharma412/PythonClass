#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/scanconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import clictorbase
from clictorbase import IafCliConfiguratorBase, DEFAULT, \
    IafCliValueError, IafCliParamMap

from sal.deprecated.expect import REGEX, EXACT
from sal.containers.yesnodefault import YES, NO


class scanconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('The value \S+ is already in the table.', \
             REGEX): IafCliValueError,
            ('Could not reach target machine:', EXACT): IafCliValueError,
            ('Unable to perform operation due to an I/O error.', \
             EXACT): IafCliValueError,
            ('Configuration filesystem is full.', EXACT): IafCliValueError,
            ('Error writing file.', EXACT): IafCliValueError,
            ('Invalid type', EXACT): IafCliValueError,
            ('Parse error', EXACT): IafCliValueError,
            ('Error reading file.', EXACT): IafCliValueError,
            ('MIME types may only contain', EXACT): IafCliValueError,
        })

    def __call__(self):
        self._writeln('scanconfig')
        return self

    def new(self, mime_type):
        self._query_response('NEW')
        self._query_response(mime_type)
        self._to_the_top(self.newlines)

    def delete(self, num_or_type, choice=YES):
        self._query_response('DELETE')
        self._query_response(num_or_type)
        # It'is the confirmation to delete:
        # Question: Are you sure you want to delete the MIME type image/*?
        self._query_response(choice)
        self._to_the_top(self.newlines)

    def Print(self):
        self._query_response('PRINT')
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.newlines)
        return raw

    def Import(self, file_name):
        self._query_response('IMPORT')
        self._query_response(file_name)
        self._to_the_top(self.newlines)

    def export(self, file_name):
        self._query_response('EXPORT')
        self._query_response(file_name)
        self._to_the_top(self.newlines)

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self.newlines)

    def setup(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        # operation values are: Scan, Skip.
        param_map['operation'] = ['Choose one:', DEFAULT, 1]
        param_map['depth'] = ['Enter the maximum depth', DEFAULT]
        param_map['max_size'] = ['Enter the maximum size', DEFAULT]
        param_map['scan_metadata'] = ['scan attachment metadata', DEFAULT]
        param_map['timeout'] = ['attachment scanning timeout', DEFAULT]
        param_map['assume_dirty'] = ['assume the attachment matches' \
                                     ' the search pattern', DEFAULT]
        param_map['bypass_on_error'] = ['should all filters be bypassed',
                                        DEFAULT]
        param_map['timeout_for_zipfiles'] = ['zip file to be unscannable if', DEFAULT]
        # fail_action values are: Deliver, Bounce, Drop
        param_map['fail_action'] = ['message could not be deconstructed', \
                                    DEFAULT, 1]
        # encoding requires unique indent one of the following rows:
        # 1. US-ASCII
        # 2. Unicode (UTF-8)
        # 3. Unicode (UTF-16)
        # 4. Western European/Latin-1 (ISO 8859-1)
        # 5. Western European/Latin-1 (Windows CP1252)
        # 6. Traditional Chinese (Big 5)
        # 7. Simplified Chinese (GB 2312)
        # 8. Simplified Chinese (HZ GB 2312)
        # 9. Korean (ISO 2022-KR)
        # 10. Korean (KS-C-5601/EUC-KR)
        # 11. Japanese (Shift-JIS (X0123))
        # 12. Japanese (ISO-2022-JP)
        # 13. Japanese (EUC)
        param_map['encoding'] = ['Configure encoding to use', \
                                 DEFAULT, 1]
        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')
        self._process_input(param_map)

    def smime(self, use_smime=NO):
        self._query_response('SMIME')
        self._query_response(use_smime)
        self._to_the_top(self.newlines)

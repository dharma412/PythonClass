#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/localeconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $


import clictorbase
from clictorbase import DEFAULT, IafCliConfiguratorBase

from sal.containers.yesnodefault import YES, NO


class localeconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __call__(self):
        self._writeln('localeconfig')
        return self

    def setup(self, force_headers_to_body_charset=DEFAULT,
              use_body_charset_for_untagged_header=DEFAULT,
              use_footer_encoding_for_ascii_message_body=DEFAULT,
              ignore_message_body_decoding_error=DEFAULT):
        self._query_response('SETUP')
        self._query_response(force_headers_to_body_charset)
        self._query_response(use_body_charset_for_untagged_header)
        self._query_response(use_footer_encoding_for_ascii_message_body)
        self._query_response(ignore_message_body_decoding_error)
        self._to_the_top(self.newlines)

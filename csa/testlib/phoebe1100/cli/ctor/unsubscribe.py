#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/unsubscribe.py#1 $

import clictorbase
from clictorbase import IafCliConfiguratorBase, DEFAULT, \
    IafIpHostnameError, IafCliValueError
from sal.deprecated.expect import REGEX, EXACT


class unsubscribe(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('The address can be one of the following', EXACT):
                IafIpHostnameError,
            ('Please answer Yes or No', EXACT): IafCliValueError,
            ('The entry \S* already exists.', REGEX): IafIpHostnameError,
            ('That entry does not exist.', EXACT): IafCliValueError,
            ('maximum number of unsubscribe entries has been reached (\d*).', \
             REGEX): IafCliValueError,
            ('Invalid entry', EXACT): IafCliValueError,
        })

    def __call__(self):
        self._writeln('unsubscribe')
        return self

    def new(self, host_name):
        self._query_response('NEW')
        self._query_response(host_name)
        self._to_the_top(self.newlines)

    def delete(self, key):
        self._query_response('DELETE')
        self._query_response(key)
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

    def setup(self, feature_allowing, action=DEFAULT):
        import re
        self._query_response('SETUP')
        p = re.compile('y', re.IGNORECASE)
        if p.match(feature_allowing):
            self._query_response(feature_allowing)
            self._query_select_list_item(action)
        else:
            self._query_response(feature_allowing)

        self._to_the_top(self.newlines)


if __name__ == "__main__":
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    cli = unsubscribe(cli_sess)

    # test cases
    cli().new('@.example.com')
    cli().delete('@.example.com')
    cli().new('@.example.com')
    cli().Print()
    cli().export('test')
    cli().clear()
    cli().Import('test')
    cli().setup('YES', 'Bounce')
    cli().setup('Yes', 'Drop')
    cli().setup('YeS', 'Bounce')
    cli().setup('Y')
    cli().setup('n')
    cli().setup('NO')
    cli().setup('No')
    cli().setup('N')
# passsed

# exceptions
#   cli().new('')
#   cli().new('qa')
#   cli().new('@qa')
#   cli().new('@qa.')
#   cli().new('1.1.1')
#   cli().new('@.example.com')
#   cli().new('@.example.com')
#   cli().new('1.1.1.1')
#   cli().new('1.1.1.1')
# passed
#   cli().delete('')
#   cli().delete('qa')
#   cli().delete('qa')
#   cli().delete('@qa')
#   cli().delete('@qa.')
#   cli().delete('1.1.1')
#   cli().delete('@.unknown.unknown')
# passed
#   cli().Import('unknown')
#   cli().Import('.')
#   cli().Import('test_10000')
#   cli().new('@.test.test1')
# passed
#   cli().export('')
#   cli().export('.')
#   cli().export('unknown(13)')
# passed
#   cli().setup('')
#   cli().setup('test', 'test')
#   cli().setup('yes', 'test')

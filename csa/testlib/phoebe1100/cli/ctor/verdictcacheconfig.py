#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/verdictcacheconfig.py#1 $

from clictorbase import IafCliConfiguratorBase, IafCliParamMap, \
    IafCliError, REQUIRED, NO_DEFAULT, DEFAULT

DEBUG = True


class verdictcacheconfig(IafCliConfiguratorBase):
    """verdictcacheconfig
        -
    """

    newlines = 2

    def __call__(self):
        self._writeln('verdictcacheconfig')
        return self

    def cloudmark(self, operation=REQUIRED, use_cache=DEFAULT):
        self._query_response('CLOUDMARK')
        if operation.lower() == 'setup':
            self._query_response('setup')
            self._query_response(use_cache)
            self._to_the_top(self.newlines)
        elif operation.lower() == 'status':
            self.clearbuf()
            self._query_response('status')
            output = self.getbuf()
            self._to_the_top(self.newlines)
            return output

    def case(self, operation=REQUIRED, use_cache=DEFAULT):
        self._query_response('CASE')
        if operation.lower() == 'setup':
            self._query_response('setup')
            self._query_response(use_cache)
            self._to_the_top(self.newlines)
        elif operation.lower() == 'status':
            self.clearbuf()
            self._query_response('status')
            output = self.getbuf()
            self._to_the_top(self.newlines)
            return output

    def matching(self):
        raise clictorbase.IafCliCtorNotImplementedError

    def imageanalysis(self, operation=REQUIRED, use_cache=DEFAULT):
        self._query_response('IMAGEANALYSIS')
        if operation.lower() == 'setup':
            self._query_response('setup')
            self._query_response(use_cache)
            self._to_the_top(self.newlines)
        elif operation.lower() == 'status':
            self.clearbuf()
            self._query_response('status')
            output = self.getbuf()
            self._to_the_top(self.newlines)
            return output


if __name__ == '__main__':
    from clictorbase import get_sess

    sess = get_sess()
    vcc = verdictcacheconfig(sess)
    # "license_agreement" needs to be taken out if it's been answered before
    print vcc().case(operation='setup', use_cache='y')
    print vcc().case(operation='status')
    print vcc().case(operation='setup', use_cache='n')
    print vcc().case(operation='status')
    print vcc().imageanalysis(operation='setup', use_cache='n')
    print vcc().matching()

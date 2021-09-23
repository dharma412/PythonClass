#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/createcomputerobject.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $
"""
    IAF 2 CLI ctor - createcomputerobject
"""

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, \
                IafCliError, IafUnknownOptionError, REQUIRED, DEFAULT
from sal.containers.yesnodefault import YES, NO

DEBUG = True

class DomainJoinError(clictorbase.IafCliValueError): pass

class createcomputerobject(clictorbase.IafCliConfiguratorBase):
    """createcomputerobject
        - Create the computer object at the specified location
    """

    def __call__(self, location='', user='', password=''):
        self._writeln('createcomputerobject')
        self._query_response('1')
        self._query_response(location)
        self._query_response(user)
        self._query_response(password)
        output = self._wait_for_prompt()
        if output.find('Failure') == -1:
            return output
        else:
            raise DomainJoinError(output)

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    comp = createcomputerobject(cli_sess)

    status = comp(user='foo', password='foobar')
    print status

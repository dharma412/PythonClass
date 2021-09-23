#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/archivemessage.py#1 $
"""
IAF2 CLI command archivemessage
"""

from sal.containers.yesnodefault import YES, NO
from sal.deprecated.expect import EXACT
import clictorbase

REQUIRED = clictorbase.REQUIRED


class TargetUnaccessibleError(clictorbase.IafCliError): pass


class FileSaveError(clictorbase.IafCliError): pass


class FilesystemFullError(clictorbase.IafCliError): pass


class archivemessage(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('Could not reach target machine', EXACT): TargetUnaccessibleError,
            ('The file', EXACT): FileSaveError,
            ('Configuration filesystem is full', EXACT): FilesystemFullError,
        })

    def __call__(self, mid=REQUIRED):
        self._writeln(self.__class__.__name__)
        self._query_response(mid)
        return self._wait_for_prompt()


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    am = archivemessage(cli_sess)
    print am(mid=1)

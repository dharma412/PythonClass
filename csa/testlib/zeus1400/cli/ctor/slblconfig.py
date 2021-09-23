#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/slblconfig.py#1 $


import re

import clictorbase
from sal.exceptions import ConfigError
from sal.deprecated.expect import EXACT

DEFAULT = clictorbase.DEFAULT


class slblconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
            {('must be enabled through GUI', EXACT): ConfigError,
             ('No End-User Safelist/Blocklist files present', EXACT): ConfigError})

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def Import(self, filename=DEFAULT, ignore=DEFAULT):
        self._query_response('IMPORT')
        self._query_select_list_item(filename)
        self._query_response(ignore)
        result = self._read_until('Choose the operation', timeout=20)
        self._to_the_top(self.newlines)
        if result.find("End-User Safelist/Blocklist successfully imported.") < 0:
            raise ConfigError, "Importing of SlBl was not finished successfully.\nCommand output was:\n%s" % (result)

    def export(self):
        self._sess.clearbuf()
        self._query_response('EXPORT')
        result = self._read_until('Choose the operation', timeout=20)
        filename = re.search('\S+?\.csv', result)
        self._restart()
        if filename:
            return filename.group(0)
        else:
            raise ConfigError, "Exporting of SlBl was not finished successfully.\nCommand output was:\n%s" % (result)


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    slbl = slblconfig(cli_sess)

    filename = slbl().export()
    if filename:
        print 'SLBL was exported to %s' % (filename,)
        slbl().Import(filename=filename)


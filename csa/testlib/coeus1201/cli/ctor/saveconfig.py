#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/saveconfig.py#1 $

"""
IAF 2 CLI command: saveconfig
"""

import re
import clictorbase
import sal.containers.yesnodefault as yesnodefault
from sal.exceptions import ConfigError

class saveconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self, save_pw = 'Y', system_generates_name = 'Y', name = None):
        self._sess.writeln('saveconfig')
        self._query_response(save_pw)
        self._query_response(system_generates_name)
        if yesnodefault.is_no(system_generates_name):
            self._writeln(name)
        results = self._read_until(timeout=5)
        match = re.search('(\S+\.xml)\s*has\s*been\s*saved', results)
        if not match:
            raise ConfigError, "File '%s' was not saved!" % name
        return match.group(1)

if __name__ == '__main__':
    sess = clictorbase.get_sess()
    sconfig = saveconfig(sess)

    save_file = sconfig(save_pw = 'Y')
    print "configuration file %s saved" % save_file

    save_file = sconfig(save_pw = 'N')
    print "configuration file %s saved" % save_file

    save_file = sconfig(save_pw = 'Yes')
    print "configuration file %s saved" % save_file

    save_file = sconfig(save_pw = 'No')
    print "configuration file %s saved" % save_file

    save_file = sconfig(save_pw = 'Y', system_generates_name = 'N', name = 'wsa_config')
    print "configuration file %s saved" % save_file

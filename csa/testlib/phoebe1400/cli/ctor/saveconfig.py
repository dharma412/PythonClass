#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/saveconfig.py#1 $

"""
IAF 2 CLI command: saveconfig
"""
from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO

import clictorbase

class saveconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self, option):
        import re
        self._sess.writeln('saveconfig')

        idx = self._query('Do you want to mask the passphrase?',
                          'Choose the passphrase',
                           timeout=30)
        if idx == 0:
            if option == 1:
                mask_pw = 'yes'
            else:
                mask_pw = 'no'
            self._query_response(mask_pw)

        elif idx == 1:
            self._query_response(option)

        results = self._read_until(timeout=45)
        xml_file_list = re.findall('\S+.xml', results)
        if len(xml_file_list) != 1:
            raise ConfigError, "No xml filename was output from saveconfig!"
        config_file_name=re.findall('\S+.xml',xml_file_list[0])[0].split("/")[-1]
        return config_file_name


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    sconfig = saveconfig(cli_sess)
    save_file = sconfig(option=1)
    print "configuration file %s saved with masked passwords" % save_file
    save_file = sconfig(option=2)
    print "configuration file %s saved with encrypted passwords" % save_file
    save_file = sconfig(option=3)
    print "configuration file %s saved with plain passwords" % save_file

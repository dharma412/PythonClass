#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/ctor/saveconfig.py#1 $

"""
IAF 2 CLI command: saveconfig
"""

import clictorbase
import re

from sal.containers.yesnodefault import YES, NO

class saveconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self, mask_pw=NO):
        self._sess.writeln('saveconfig')
        try:
           self._query_response(mask_pw)
           results = self._read_until(timeout=10)
        except:
           mask_pw = '2'
           self._query_select_list_item(mask_pw)
           results = self._read_until(timeout=10)
        xml_file_list = re.findall('\S+.xml', results)
        if len(xml_file_list) != 1:
            raise ConfigError, "No xml filename was output from saveconfig!"
        return xml_file_list[0]

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    sconfig = saveconfig(cli_sess)
    save_file = sconfig(save_pw=YES)
    print "configuration file %s saved with passwords" % save_file
    save_file = sconfig(save_pw=NO)
    print "configuration file %s saved without passwords" % save_file

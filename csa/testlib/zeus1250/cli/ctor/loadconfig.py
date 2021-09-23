#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/loadconfig.py#3 $

"""
IAF 2 CLI command: loadconfig
"""

from sal.exceptions import ConfigError
import re
import clictorbase
from sal.deprecated import expect

class loadconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self,
        load_method='Load from file',
        filename=None,
        config_str=None,
        load_network_settings='',
        load_disk_quota_settings='',
    ):
        self._sess.writeln('loadconfig')
        # is first question about clearing uncommitted changes?  must check.
        first_q = self._read_until(self._sub_prompt_user_match, timeout=7)
        mo = re.search('uncommitted changes', first_q)

        if mo:    # always answer yes to wiping out uncommitted changes
            self._sess.writeln('Y')
            first_q = self._read_until(self._sub_prompt_user_match, timeout=7)

        mo = re.search('network settings', first_q)
        if mo:
            self._sess.writeln(load_network_settings)
            first_q = self._read_until(self._sub_prompt_user_match, timeout=7)

        mo = re.search('load disk quota settings', first_q)
        if mo:
            self._sess.writeln(load_disk_quota_settings)
            first_q = self._read_until(self._sub_prompt_user_match, timeout=7)

        # work with existing response, conveniently in first_q now
        entry = int(self._select_list_item(load_method, first_q))
        if entry == 2:      # Load from file
            self._query_response(filename)
        else:               # Paste via CLI
            # Break up the very large config_str string (~40 Kbytes)
            # into single lines. Write the line then immediately read it
            # back.  If you try to write a 40KB chunk of text, not
            # all the text will get written (the mga's buffer isn't
            # large enough to hold all the text) and when you try and
            # read all that text back it'll be really slow and timeout.
            self._read_until('Press CTRL-D on a blank line when done.')
            for line in config_str.split("\n"):
                self._sess.writeln(line)
                self._sess.readline()
            self._sess.write("\x04")    # ^D means end of config file

        # need a long timeout here as cut/paste configs take a while
        idx = self._query('Values have been loaded',
                          'Parsing failed',
                          'No data to load',
                          'Error: the file ".+?" does not exist',
                          'No changes detected',
                          timeout=60)
        if idx == 1:
            raise ConfigError, "loadconfig: Parse of config file failed."
        elif idx == 2:
            raise ConfigError, "loadconfig: No configuration data entered."
        elif idx == 3:
            raise ConfigError, "loadconfig: Config filename does not exist."
        else:
            pass

        return idx == 0

if __name__ == '__main__':
    import saveconfig
    import sal.net.sshlib
    import sal.irontools

    # saveconfig
    sess = clictorbase.get_sess()
    sc = saveconfig.saveconfig(sess)
    fname = sc()

    # scp saved config to local host
    dir = '/var/log/godspeed/configuration/'
    src = sal.irontools.get_ruser() + '@marla.qa:' + dir + fname
    dst = '/tmp/mgacfg.xml'
    sal.net.sshlib.scp(src, dst)

    # load config
    lcf = loadconfig(sess)
    result = lcf(filename=fname)

    conf_file = open(dst)
    cfdata = conf_file.read()
    conf_file.close()
    result = lcf(load_method='Paste', config_str=cfdata)

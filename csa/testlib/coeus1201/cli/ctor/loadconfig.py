#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/loadconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
IAF 2 CLI command: loadconfig
"""

import re
import clictorbase
from clictorbase import REQUIRED, DEFAULT
from sal.exceptions import ConfigError

class loadconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self, load_method='Load from file',
                 filename=None, config_str=None, clear_net_settings=DEFAULT):
        """ Return True if there are changes to commit, False
            if there are no changes to commit. Otherwise, raise
            ConfigError for all error conditions.
        """
        self._restart()
        self._sess.writeln('loadconfig')

        # is first question about clearing uncommitted changes?  must check.
        first_q = self._read_until(self._sub_prompt_user_match, timeout=3)
        mo = re.search('uncommitted changes', first_q)

        if mo:    # always answer yes to wiping out uncommitted changes
            self._sess.writeln('Y')
            first_q = self._read_until(self._sub_prompt_user_match, timeout=3)

        mo = re.search('network settings', first_q)
        if mo:
            self._sess.writeln(clear_net_settings)
            first_q = self._read_until(self._sub_prompt_user_match, timeout=3)

        # work with existing response, conveniently in first_q now
        entry = int(self._select_list_item(load_method, first_q))

        if entry == 2:      # Load from file
            self._query_response(filename)
        else:               # Paste via CLI
            # NOTE: this doesn't work as-is since there are problems
            # with LOOOOONG strings and the expect module.
            # But it's not working in ironport.py/IAF1 either, so we
            # won't worry about it for now.
            self._sess.writeln(config_str)
            self._sess.write("\x04")    # ^D means end of config file

        # need a long timeout here as cut/paste configs take a while
        idx = self._query('Values have been loaded',
                          'Parsing failed',
                          'No data to load',
                          'Error: the file ".+?" does not exist',
                          'No changes detected from current configuration',
                          'Parse Error',
                          timeout=300)
        # Let's be nice and process the prompt. Not doing this confuses
        # future configurators that assume this has been done.
        self._wait_for_prompt()
        if idx == 1 or idx == 5:
            raise ConfigError, "loadconfig: Parse of config file failed."
        elif idx == 2:
            raise ConfigError, "loadconfig: No configuration data entered."
        elif idx == 3:
            raise ConfigError, "loadconfig: Config filename does not exist."
        elif idx == 4:
            return False

        return True

if __name__ == '__main__':
    conf_file = open('C600-001143ECE931-44MNP61-20051206T144924.xml', 'r')
    cfdata = conf_file.read()
    conf_file.close()

    sess = clictorbase.get_sess()
    lcf = loadconfig(sess)
    result = lcf(filename='C600-001143ECE931-44MNP61-20051206T144924.xml')
    result = lcf(load_method='Paste', config_str=cfdata)

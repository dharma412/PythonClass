#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/featurekey.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

"""
CLI command: featurekey
"""
import re

import clictorbase
from sal.exceptions import ConfigError
from sal.exceptions import TimeoutError

class featurekey(clictorbase.IafCliConfiguratorBase):

    def __call__(self, key=None, batch_cmd=None):
        cmd = 'featurekey'

        if batch_cmd is not None:
            self._writeln(' '.join((cmd, batch_cmd)))
            return self._wait_for_prompt()

        self._writeln(cmd)
        if key:
            self.activate(key)
        return self

    def get_featurekey(self, key_str):
        """Returns installed featurekey.
        Key matches given `key_str`.
        :
        :Exceptions:
            - assert if no keysting given
        """
        import re

        raw = ''
        try:
            assert key_str, 'keystring is not defined'
            raw = self._read_until('Choose the operation')
            if not re.search('Module.*Remaining', raw, re.MULTILINE):
                #Detected no certificates
                raw =  ''
        finally:
            # return to the CLI prompt
            self._to_the_top(1)
        # pattern searches for remaining time of installed
        # featurekey searching in:
        # Cisco IronPort Spam Quarantine   30 days     Sat Oct 21 06:59:37 2006
        # returns regex match object

        patt = r'%s.+?\s+(.+?)\s{2,}(.+)'% (key_str,)
        return re.search(patt, raw)

    def activate(self, key):
        """ activates given feature key

        TODO: allow activating pending keys
        :Parameters:
            - `key`: the key to activate
        :Exceptions:
            - `ConfigError` if key has already been used or is malformed/invalid
        """
        self._query_response('ACTIVATE')
        self._query_response(key)
        while 1:
             idx = self._query('-Press Any Key For More-','Feature key accepted', 'has already been used',
                   'malformed', 'above license agreement',
                    self._sub_prompt, self._get_prompt())
             if idx == 0:
                  self._writeln("\n")
                  continue
             elif idx == 1:
                  self._to_the_top(1, timeout=40)
                  break
             elif idx == 2:
                  self._to_the_top(1, timeout=40)
                  raise ConfigError, "featurekey: Feature key has already been used."
                  break
             elif idx == 3:
                  self._to_the_top(1, timeout=40)
                  raise ConfigError, "featurekey: Feature key is malformed/invalid."
                  break
             elif idx == 4:
                  self._query_response('YES') # accept license
                  self._to_the_top(1, timeout=40)
                  break
             elif idx == 5: # sub prompt
                  self._writeln()
                  self._wait_for_prompt()
                  break
             else:
                  pass
                  break

    def checknow(self):
        """Checks, if there are some pending keys

        :Return:
            Dictionary of pending keys. Dictionary will be empty if threre
            are no pending keys
        """
        self.clearbuf()
        self._query_response('CHECKNOW')
        result = {}

        try:
            buffer = self._read_until(
                                'Choose the operation you want to perform')
            result = self._get_key(buffer)

        finally:
            self._to_the_top(1)

        return result

    def _get_key(self, buffer):
        """Parse buffer to get feature keys and their names

        :Parameters:
            -`buffer`: text to search in

        :Return:
            dictionary {<feature key name>: <feature key>}
        """
        dict = {}

        keys = re.findall(r'\d+\. (.*?)\s*(.*?),', buffer)
        for key, feature in keys:
            dict[feature] = key

        return dict


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    fkey = featurekey(cli_sess)
    # TODO: write unit tests that generate feature keys on the fly
    print 'Pending feature keys:'
    print fkey().checknow()

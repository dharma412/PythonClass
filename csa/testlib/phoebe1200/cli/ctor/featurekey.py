#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/featurekey.py#1 $

"""
IAF 2 CLI command: featurekey
"""

from sal.exceptions import ConfigError
import re

import clictorbase


class featurekey(clictorbase.IafCliConfiguratorBase):
    def __call__(self, key=None, pendingkey=None):
        self._writeln('featurekey')
        if key:
            self.activate(key)
        if pendingkey:
            self.activate(pendingkey)
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
            if not re.search('Module.*Quantity', raw, re.MULTILINE):
                # Detected no featurekey
                raw = ''
        finally:
            # return to the CLI prompt
            self._to_the_top(1)
        # pattern searches for quantity and remaining time of installed
        # featurekey searching in:
        # Bounce Verification   1          30 days     Sat Oct 21 06:59:37 2006
        # returns "1" and "30 days"

        patt = r'(%s.+?)(\d+)\s+(.+?)\s{2,}(.+)' % (key_str,)
        if re.search(patt, raw):
            return re.search(patt, raw).group(0)
        else:
            return 'FeatureKeyNotFound'

    def activate(self, key=None, pendingkey=None):
        """ activates given feature key

        :Parameters:
            - `key`: the key to activate
            - `pendingkey`: the pending key to activate, can be int(index) or str(key)
        :Exceptions:
            - `ConfigError` if key has already been used or is malformed/invalid
        """
        if pendingkey:
            self.clearbuf()
            self._query_response('CHECKNOW')
            pkeys = {}
            try:
                buffer = \
                    self._read_until('Choose the operation you want to perform')
                pkeys = self._get_key(buffer)
            finally:
                pass
            if any(pkeys.values()):
                self._query_response('ACTIVATE')
                if (isinstance(pendingkey, int) \
                    and pendingkey <= len(pkeys.values())) \
                        or (isinstance(pendingkey, str) \
                            and pendingkey in pkeys.values()):
                    self._query_response(pendingkey)
                else:
                    raise ConfigError, \
                        "Value should be in range [1..%s] or one of the %s" \
                        % (len(pkeys.values()), str(pkeys.values()))
            else:
                raise ConfigError, "There are no pending keys"
        if key:
            self._query_response('ACTIVATE')
            self._query_response(key)

        while 1:
            idx = self._query('Feature key accepted', 'has already been used',
                              'malformed', 'above license agreement', 'Press Any Key For More',
                              self._sub_prompt, self._get_prompt())
            if idx == 0:
                self._to_the_top(1, timeout=40)
                break
            elif idx == 1:
                self._to_the_top(1, timeout=40)
                raise ConfigError, "featurekey: Feature key has already been used."
            elif idx == 2:
                self._to_the_top(1, timeout=40)
                raise ConfigError, "featurekey: Feature key is malformed/invalid."
            elif idx == 3:
                self._query_response('YES')  # accept license
                self._to_the_top(1, timeout=40)
                break
            elif idx == 4:
                self._writeln()
                continue
            elif idx == 5:  # sub prompt
                self._writeln()
                self._wait_for_prompt()
                break
            elif idx == 6:
                break

        return idx

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
    fkey()

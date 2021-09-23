#!/usr/bin/env python

"""
  smartaccountinfo ctor
"""
import re
import clictorbase as ccb

class smartaccountinfo(ccb.IafCliConfiguratorBase):
    def __call__(self):
        self.clearbuf()
        self._writeln('smartaccountinfo')
        return self

    def smart_account_info(self):
        account_info = self._read_until()
        self.accountinfo = {}

        lines =  account_info.split('\n')
        for line in lines:
            if re.search(":",line):
                key,value = line.split(':')
                self.accountinfo[key.strip()] = value.strip()
            else:
                self._debug("Smart Account Deatils not displayed")

        return self.accountinfo

"""
cli -> smartaccountinfo

"""
import re

from clictorbase import IafCliConfiguratorBase


class smartaccountinfo(IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        smart_account_info = {}
        self._restart()
        self._writeln('smartaccountinfo')
        result = re.findall(r'(.*):\s+(.*)', self._wait_for_prompt())
        if result:
            for res in result:
                smart_account_info[res[0].strip()] = res[1].strip()
        return smart_account_info

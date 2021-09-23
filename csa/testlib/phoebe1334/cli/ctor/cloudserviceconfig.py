import clictorbase
import time
from sal.exceptions import ConfigError, TimeoutError, ExpectError
from clictorbase import IafCliConfiguratorBase, IafCliError, \
    REQUIRED, DEFAULT, IafCliValueError


class cloudserviceconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        time.sleep(30)
        self._writeln('cloudserviceconfig')
        return self

    def settrs(self, settrs=REQUIRED):
        self.new_lines = 1
        self._query_response('SETTRS')
        self._query_select_list_item(settrs)
        self._expect('\n')
        self._to_the_top(self.new_lines)

    def register(self, token_id=REQUIRED):
        self._query_response('REGISTER')
        self._query_response(token_id)
        output = self._wait_for_prompt()
        if 'The registration failed because of an invalid or expired token key' in  output:
            raise ConfigError('The registration failed because of an invalid or expired token key')
        return output
 
    def deregister(self):
        self._query_response('DEREGISTER')
        self._query_response('Y')
        self._to_the_top(1)


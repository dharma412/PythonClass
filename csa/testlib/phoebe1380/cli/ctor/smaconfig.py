import clictorbase
from clictorbase import DEFAULT, REQUIRED, IafCliParamMap, IafCliConfiguratorBase
from sal.containers.yesnodefault import is_yes, YES, NO

class smaconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('smaconfig')
        return self

    def add(self, hostname, ssh_key):
        self._writeln('ADD')
        self._expect('Enter the hostname of the system that you want to add.')
        self._writeln(hostname)
        self._expect('Press enter on a blank line to finish.')
        self._writeln(ssh_key+'\n')
        self._to_the_top(self.newlines)

    def print_key(self):
        self.clearbuf()
        self._query_response('PRINT')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.newlines)
        return raw.strip("\r\n")

    def delete(self, keynumber):
        self._query_response('DELETE')
        self._query_response(keynumber)
        self._to_the_top(self.newlines)

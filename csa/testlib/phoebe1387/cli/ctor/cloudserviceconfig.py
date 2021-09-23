from sal.exceptions import ConfigError, TimeoutError, ExpectError
from clictorbase import IafCliConfiguratorBase, IafCliError, IafCliValueError
from clictorbase import REQUIRED, DEFAULT

class cloudserviceconfig(IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self.new_lines = 1
        self._sess.clearbuf()

    def __call__(self):
        self._writeln('cloudserviceconfig')
        return self

    def enable(self, server):
        self._query_response('ENABLE')
        self._read_until('Enter Cisco Secure Cloud Server to connect to the Cisco Cloud Service')
        self._query_response(server)

    def status(self):
        self._to_the_top(self.new_lines)
        session_buffer = self._sess.getbuf()
        if 'appliance is successfully registered' in session_buffer:
            return 'REGISTERED'
        elif 'Cisco Cloud Service is busy' in session_buffer:
            return 'INPROGRESS'
        else:
            return 'DISABLED'

    def disable(self):
        self._query_response('DISABLE')
        self._read_until('The Cisco Cloud Service is currently disabled on your appliance')

    def settrs(self, settrs=REQUIRED):
        self._query_response('SETTRS')
        self._query_select_list_item(settrs)
        self._expect('\n')
        self._to_the_top(self.new_lines)

    def register(self, token_id=REQUIRED):
        self._query_response('REGISTER')
        self._query_response(token_id)
        output = self._wait_for_prompt(timeout=120)
        if 'The registration failed because of an invalid or expired token key' in  output:
            raise ConfigError('The registration failed because of an invalid or expired token key')
        return output

    def deregister(self):
        self._query_response('DEREGISTER')
        self._query_response('Y')
        self._to_the_top(self.new_lines)

    def setfqdn(self, label=REQUIRED, fqdn=REQUIRED):
        self._query_response('setfqdn')
        fqdnval = None
        try:
            fqdnval = self._read_until('Enter a label for Cisco Cloud Service region. eg. APJC')
            self._query_response(label)
            fqdnval = self._read_until('Enter fqdn for SSE connector')
            self._query_response(fqdn)
        finally:
            self._to_the_top(self.new_lines)
        return fqdnval

    def fetch_certificate(self):
        self._sess.clearbuf()
        self._query_response('FETCHCERTIFICATE')
        return self._sess.getbuf()

    def securex_enable(self):
        self._writeln('ENABLESECUREX')
        self._to_the_top(self.new_lines)

    def securex_disable(self):
        self._writeln('DISABLESECUREX')
        self._to_the_top(self.new_lines)

    def csnconfig_enable(self):
        self._writeln('ENABLECSN')
        self._to_the_top(self.new_lines)

    def csnconfig_disable(self):
        self._writeln('DISABLECSN')
        self._to_the_top(self.new_lines)

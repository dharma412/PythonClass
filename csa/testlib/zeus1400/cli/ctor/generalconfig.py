from sal.exceptions import ConfigError, TimeoutError, ExpectError
from clictorbase import IafCliConfiguratorBase, IafCliError, IafCliValueError
from clictorbase import REQUIRED, DEFAULT
from sal.containers.yesnodefault import YES, NO, is_yes

class generalconfig(IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self.new_lines = 1
        self._sess.clearbuf()

    def __call__(self):
        self._writeln('generalconfig')
        return self

    def enable_securex(self):
        self._writeln('SECUREX')
        self._expect(['Would you like to enable Cisco SecureX/ Threat Response feature',
                      'Cisco SecureX / Threat Response feature is currently enabled'])
        if self._expectindex == 0:
           enable = 'YES'
        elif self._expectindex == 1:
           enable = 'NO'

        self._query_response(enable)
        self._writeln()
        self._to_the_top(self.new_lines)

    def disable_securex(self):
         self._sess.clearbuf()
         self._writeln('SECUREX')
         self._expect(['Would you like to disable Cisco SecureX/ Threat Response feature',
                       'Cisco SecureX / Threat Response feature is currently disabled'])

         if self._expectindex == 0:
            disable =  'YES'
         elif self._expectindex == 1:
            disable =  'NO'

         self._writeln(disable)
         self._writeln()
         self._to_the_top(self.new_lines)

    def get_securex_status(self):
           self._sess.clearbuf()
           self._writeln('SECUREX')
           self._expect(['Cisco SecureX / Threat Response feature is currently disabled',
                       'Cisco SecureX / Threat Response feature is currently enabled'])
           if self._expectindex == 0:
               return 'DISABLED'
           elif self._expectindex == 1:
               return 'ENABLED'


"""
cli -> trailblazerconfig

"""
from clictorbase import IafCliConfiguratorBase, IafCliValueError

class trailblazerconfig(IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self, **args):
        self.clearbuf()
        command = 'trailblazerconfig'
        if args.has_key('action'):
            command += ' %s' %args['action']
        if args.has_key('port'):
            command += ' %s' %args['port']
        self._writeln(command)
        output = self._wait_for_prompt()
        if 'At least one parameter is needed' in  output:
            raise IafCliValueError('At least one parameter is needed')
        return output
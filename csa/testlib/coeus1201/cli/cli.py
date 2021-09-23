#!/usr/bin/env python

import sal.net.sshlib
import sal.net.ipmilib
from sal.deprecated import expect
import sal.multiprompt as multiprompt
from sal.exceptions import ConfigError

def get_cli(host, user, password, logger=None, model=None, transport='ssh', reset_password=False):
    if transport == 'ssh':
        sess = sal.net.sshlib.get_ssh_unsafe(host, user, password,
                logfile=logger, reset_password=reset_password)
        sess.set_prompt(multiprompt.MultiPrompt(host))
    elif transport == 'ipmi':
        sess = sal.net.ipmilib.get_ipmi_sol_unsafe(host, user, password,
                logfile=logger)
        sess.set_prompt(expect.RegexUserMatch('%s>|ironport.example.com>' % host))
    else:
        raise ConfigError, 'unknown transport'

    sess.wait_for_prompt()
    sess.writeln('setttymode 0 1')
    sess.wait_for_prompt()

    return IronCli(sess, model=model, logger=logger)

class IronCli(object):
    def __init__(self, sess, model=None, logger=None):
        self._sess = sess
        self._logger = logger
        self._model = model

    def __getattr__(self, name):
        #if not hasattr(self,name):
        if 1:
            # Effectively the code does this (if name='setgatway'):
            #   import cli.ctor.setgateway
            #   self.setgateway = cli.ctor.setgateway.setgateway(self._sess)
            #   self.setgateway.set_model(self._model)
            #   return self.setgateway
            exec('import ctor.%s as imported_mod' % name)
            ctor_class = getattr(imported_mod, name)
            # Instantiate the ctor. ctor is saved in the IronCli object.
            setattr(self, name, ctor_class(self._sess))
            getattr(self,name).set_model(self._model) # update model
        return getattr(self,name)

    def set_model(self, model):
        self._model = model
    def get_model(self, model):
        return self._model

    def get_sess(self):
        return self._sess

    def close(self):
        return self._sess.close()


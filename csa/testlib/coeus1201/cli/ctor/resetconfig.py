#!/usr/bin/env python

import clictorbase
import re
from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO

class resetconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self, reset_network):
        """Resets the DUT configuration to a default set."""
        self._writeln('resetconfig')

        idx = self._query('only works in the offline state',
                          'Are you sure you want to reset')

        if idx == 0:
            raise ConfigError, "not offline"
        elif idx == 1:
            self._query_response(YES)
            # resetconfig will take us out of cluster mode
            #self.DisableClusterMode() ##TODO
        else:
            raise ConfigError, "resetconfig: unexpected response"
        self._read_until('Do you want to reset network settings')
        self._query_response(reset_network)

        self._wait_for_prompt(120)

    def DisableClusterMode(self):
        raise NotImplementedError


if __name__ == '__main__':

    reset_cfg = resetconfig(clictorbase.get_sess())

    print 'resetconfig test before suspend '
    try:
        reset_cfg()
    except ConfigError, ce:
        if (str(ce).find('not offline') == -1):
           raise
        else:
            print 'Config error found, as expected in negative test case'

    print 'DONE!'

    reset_cfg._writeln("suspend")
    reset_cfg._query_response(10)
    reset_cfg._restart()

    print 'resetconfig test after suspend'
    reset_cfg()
    print 'resetconfig DONE!'

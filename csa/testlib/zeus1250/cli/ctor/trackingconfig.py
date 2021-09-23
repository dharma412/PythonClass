#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/trackingconfig.py#3 $

import clictorbase
from sal.containers.yesnodefault import NO, YES
DEFAULT = clictorbase.DEFAULT

class trackingconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
                                         end_of_command='Choose the operation')
        param_map['license_agreement'] = ['license agreement?', YES]
        param_map['enable_tracking'] = ['enable Centralized Email Message Tracking', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)

    def alert_timeout(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
                        end_of_command='Choose the operation')
        param_map['enable'] = ['timeout alerts to be enabled', DEFAULT]
        param_map['timeout'] = ['many minutes should an alert be sent', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('ALERT_TIMEOUT')
        return self._process_input(param_map)

if __name__ == '__main__':

    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    tc = trackingconfig(cli_sess)

    tc().setup()
    tc().setup(enable_tracking=YES)
    tc().setup(enable_tracking=NO)
    tc().alert_timeout(enable=YES, timeout=30)
    tc().alert_timeout(enable=NO)

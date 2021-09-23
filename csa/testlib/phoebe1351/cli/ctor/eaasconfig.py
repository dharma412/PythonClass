# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/eaasconfig.py#1 $
# $DateTime: 2020/01/17 04:04:23 $
# $Author: aminath $

import clictorbase as ccb


class eaasconfig(ccb.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def register(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command=self._get_prompt())
        param_map['eaas_region'] = ['Select the EAAS region to connect', ccb.DEFAULT, 1]
        param_map['eaas_passphrase'] = ['Enter passphrase obtained from APP portal', ccb.REQUIRED]
        param_map['eaas_enable_app'] = ['Would you like enable APP', ccb.DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('REGISTER')
        self._process_input(param_map)
        return False if 'Failed to register' in self._sess.getbuf() else True

    def edit(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command=self._get_prompt())
        param_map['eaas_region'] = ['Select the EAAS region to connect', ccb.DEFAULT, 1]
        param_map['eaas_passphrase'] = ['Enter passphrase obtained from APP portal', ccb.REQUIRED]
        param_map.update(input_dict or kwargs)
        self._query_response('EDIT')
        self._process_input(param_map)

    def enable(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command=self._get_prompt())
        param_map['eaas_enable_app'] = ['Are you sure you want to enable APP', ccb.DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('ENABLE')
        self._process_input(param_map)

    def disable(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command=self._get_prompt())
        param_map['eaas_disable_app'] = ['Are you sure you want to disable APP', ccb.DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('DISABLE')
        self._process_input(param_map)

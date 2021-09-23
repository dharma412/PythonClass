#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/updateconfig.py#1 $

import clictorbase as ccb

DEFAULT = ccb.DEFAULT
DEBUG = True

class updateconfig(ccb.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('updateconfig')
        return self

    def setup(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')

        param_map['update_from'] = ['download updates', DEFAULT, 1]
        param_map['update_server'] = ['HTTP server to download', DEFAULT]
        param_map['update_list_from'] = ['download the list of available ' \
                                         'updates from', DEFAULT, 1]
        param_map['update_list_server'] = ['full HTTP URL of the update ' \
                                           'list', DEFAULT]
        param_map['web_rep_interval'] = \
            ['interval between checks for new data for Web Reputation', DEFAULT]
        param_map['interval'] = ['time interval between checks', DEFAULT]
        param_map['routing_table'] = ['routing table to use', DEFAULT, 1]
        param_map['use_proxy'] = ['HTTP updates for ALL of', DEFAULT]
        param_map['proxy_server'] = ['the URL of the proxy server', DEFAULT]
        param_map['use_https_proxy'] = ['HTTPS updates for ALL of', DEFAULT]
        param_map['https_proxy_server'] = ['the URL of the proxy server',
                                           DEFAULT]
        param_map['check_asyncos_upgrade'] = ['check for AsyncOS upgrades',
                                              DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)

    def dynamichost(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['dynamic_host']    = ['new manifest hostname', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('DYNAMICHOST')
        return self._process_input(param_map)

    def validate_certificates(self, input_dict=None, **kwargs):
        self.clearbuf()
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['validate']    = ['Should server certificates from Cisco update servers be validated', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('VALIDATE_CERTIFICATES')
        return self._process_input(param_map)

if __name__ == '__main__':
    from sal.containers.yesnodefault import YES, NO

    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()
    udc = updateconfig(cli_sess)

    udc().setup()
    udc._restart()
    udc().setup(update_from='Use own', update_server='myserver.com:80',
                use_proxy=YES, proxy_server='http://proxy.com')
    udc._restart()
    udc().setup(update_from='Use own', update_server='myserver.com:80',
                update_list_from='Use own',
                update_list_server='http://list.com',
                interval='33m', routing_table='Management',
                use_proxy=YES, proxy_server='http://proxy.com',
                use_https_proxy=YES,
                https_proxy_server='http://https_proxy.com')

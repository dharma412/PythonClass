# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/updateconfig.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

import clictorbase as ccb

DEFAULT = ccb.DEFAULT
DEBUG = True


class updateconfig(ccb.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('updateconfig')
        self._warn('Will ignore unanswered questions!')
        ccb.set_ignore_unanswered_questions(ignore=True)
        return self

    def setup(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['update_from'] = ['download updates', DEFAULT, 1]
        param_map['update_server'] = ['base URL of the update server', DEFAULT]
        param_map['update_images_from'] = \
            ['the system will download updates from', DEFAULT, 1]
        param_map['autoupdates_disabled_alert_frequency'] = \
            ['Enter the frequency of alerts to be sent when', DEFAULT]
        param_map['update_images_server'] = \
            ['hostname and port of the HTTP server', DEFAULT]
        param_map['update_upgrade_images_from'] = \
            ['the system will download updates from', DEFAULT, 1]
        param_map['update_upgrade_images_server'] = \
            ['hostname and port of the HTTP server', DEFAULT]
        param_map['update_ims_and_cloudmark_from'] = \
            ['please select where the system will', DEFAULT, 1]
        param_map['update_ims_and_cloudmark_server'] = \
            ['hostname of the HTTP server', DEFAULT]
        param_map['update_list_from'] = \
            ['download the list of available updates from', DEFAULT, 1]
        param_map['update_list_server'] = \
            ['full HTTP URL of the update list', DEFAULT]
        param_map['update_upgrade_list_from'] = \
            ['download the list of available updates from', DEFAULT, 1]
        param_map['update_upgrade_list_server'] = \
            ['full HTTP URL of the update list', DEFAULT]
        param_map['interval'] = ['time interval between checks', DEFAULT]
        param_map['interface'] = ['specific interface', DEFAULT, 1]
        param_map['use_proxy'] = ['HTTP updates for ALL of', DEFAULT]
        param_map['proxy_server'] = ['the URL of the proxy server', DEFAULT]
        param_map['use_https_proxy'] = ['HTTPS updates for ALL of', DEFAULT]
        param_map['https_proxy_server'] = \
            ['the URL of the proxy server', DEFAULT]
        # temp fix. have to add this twice
        param_map['use_proxy1'] = ['HTTP updates for ALL of', DEFAULT]
        param_map['proxy_server1'] = ['the URL of the proxy server', DEFAULT]
        #
        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')
        return self._process_input(param_map)

    def dynamichost(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['dynamic_host'] = ['new manifest hostname', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('dynamichost')
        return self._process_input(param_map)

    def validate_certificates(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['validate_certificates'] = ['certificates from Cisco update servers be validated', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('validate_certificates')
        return self._process_input(param_map)

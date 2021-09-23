#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/antispamconfig.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

"""
    IAF 2 CLI ctor - antispamconfig
"""
import clictorbase as ccb

from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO

REQUIRED = ccb.REQUIRED
NO_DEFAULT = ccb.NO_DEFAULT
DEFAULT = ccb.DEFAULT
DEBUG = True

class antispamconfig(ccb.IafCliConfiguratorBase):
    """antispamconfig
        - will return -1 when there's no feature key for either BM or CASE
    """

    _vendors = ('brightmail', 'ironport','cloudmark','multiscan')

    def __call__(self, vendor=REQUIRED):
        vendor = vendor.lower()
        if not vendor in self._vendors:
            raise ConfigError('Illegal vendor: %s. Allowed vendors: %s'
                              %(vendor, '; '.join(self._vendors)))

        self._writeln('antispamconfig')
        self.clearbuf()
        self._expect(['requires activation', 'Choose the operation'])
        lines = self.getbuf()
        if self._expectindex == 0:
            self._wait_for_prompt()
            return -1
        if self._expectindex == 1:
            if vendor == 'multiscan':
                if lines.find(' Multi-Scan:') == -1:
                    self._query_response(vendor)
                    lines = self._read_until(' Multi-Scan:')
                    return antispamconfigMultiscan(self._get_sess())
            if lines.find(' scanning:') == -1:
                self._query_response(vendor)
                lines = self._read_until(' scanning:')

            if lines.find('Symantec Brightmail') >= 0 and \
                                                        vendor == 'brightmail':
                return antispamconfigBM(self._get_sess())
            elif lines.find('IronPort') >= 0 and vendor == 'ironport':
                return antispamconfigCASE(self._get_sess())
            elif lines.find('Cloudmark') >= 0 and vendor == 'cloudmark':
                return antispamconfigCloudmark(self._get_sess())
            else:
                raise ccb.IafCliError('Feature is not activated. Please make '\
                    'sure that featurekey is valid and the feature is bundled')


class antispamconfigMultiscan(ccb.IafCliConfiguratorBase):
    """antispamconfig -> Multiscan """
    global ccb

    def setup(self, input_dict=None, **kwargs):
        global DEFAULT, NO_DEFAULT, YES, NO

        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['use_ims']              = ['to use IronPort Intelligent Multi-Scan scanning', DEFAULT]
        param_map['scan_size']      = ['largest size message that Intelligent Multi-Scan', DEFAULT]
        param_map['scan_timeout'] = ['Intelligent Multi-Scan scanning timeout', DEFAULT]
        param_map['reputation_filter_incoming'] = ['filtering for incoming messages', DEFAULT]
        param_map['reputation_filter_outgoing'] = ['filtering for outgoing messages', DEFAULT]
        param_map['region_scan']     = ['regional scanning',DEFAULT]
        param_map['confirm_disable']     = ['want to disable', NO]
        param_map['choose_region']     = ['Choose your region', DEFAULT]
        param_map['license_agreement']   = ['license agreement?', YES]
        param_map['mesg_larger_than']   = ['Never scan message larger than',DEFAULT]
        param_map['mesg_smaller_than']   = ['Always scan message smaller than', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)


class antispamconfigBM(ccb.IafCliConfiguratorBase):
    """antispamconfig -> BM """


    def setup(self, input_dict=None, **kwargs):


        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['use_bm']              = ['to use Symantec', DEFAULT]
        param_map['spam_threshold']      = ['Spam Threshold', DEFAULT]
        param_map['use_reinsertion_key'] = ['specify a reinsertion', DEFAULT]
        param_map['reinsertion_key']     = ['Enter Reinsertion', NO_DEFAULT]
        param_map['use_open_proxy_list'] = ['Open Proxy List', DEFAULT]
        param_map['use_open_safe_list']  = ['Safe List', DEFAULT]
        param_map['use_language_id']     = ['Language Identification', DEFAULT]
        param_map['max_msg_size']        = ['size of message', DEFAULT]
        param_map['enable_caching']      = ['cache verdicts', DEFAULT]
        param_map['cache_duration']      = ['how long to cache', DEFAULT]
        param_map['confirm_disable']     = ['want to disable', YES]
        param_map['license_agreement']   = ['license agreement?', YES]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)

    def tune(self, input_dict=None, **kwargs):


        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['num_servers'] = ['number of brightmail', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('TUNE')
        return self._process_input(param_map)

    def clusterset(self, input_dict=None, **kwargs):


        param_map = ccb.IafCliParamMap(end_of_command='Settings')
        param_map['action'] = ['can copy the current settings', REQUIRED, True]
        param_map['group_copy'] = ['group name or number to copy', DEFAULT]
        param_map['machine_copy'] = ['machine name or number to copy', DEFAULT]
        param_map['cluster_copy'] = ['cluster name or number to copy', DEFAULT]
        param_map['group_move'] = ['group name or number to move', DEFAULT]
        param_map['machine_move'] = ['machine name or number to move', DEFAULT]
        param_map['cluster_move'] = ['cluster name or number to move', DEFAULT]
        param_map['delete_cluster'] = ['from the cluster', DEFAULT]
        param_map['delete_group'] = ['from the Group', DEFAULT]
        param_map['delete_machine'] = ['from the machine', DEFAULT]
        param_map['force'] = ['you sure you want to continue', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('CLUSTERSET')
        return self._process_input(param_map)

    def clustershow(self):
        self._query_response('CLUSTERSHOW')
        raw = self._read_until('Choose the operation')
        self._to_the_top(2)
        return raw

class antispamconfigCASE(ccb.IafCliConfiguratorBase):
    """antispamconfig -> CASE """


    def setup(self, input_dict=None, **kwargs):

        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['use_case']             = ['to use IronPort', DEFAULT]
        param_map['timeout']              = ['scanning timeout', DEFAULT]
        param_map['scan_profile']         = ['Choose Scanning profile', DEFAULT, 1]
        param_map['region']               = ['Regional(China)', DEFAULT]
        param_map['aggressive']           = ['Aggressive', DEFAULT]
        param_map['normal']               = ['Normal', DEFAULT]
        param_map['license_agreement']    = ['license agreement?', YES]
        param_map['mesg_larger_than']   = ['Never scan message larger than',DEFAULT]
        param_map['mesg_smaller_than']   = ['Always scan message smaller than', DEFAULT]
        param_map['confirm_disable']      = ['want to disable', YES]
        param_map['confirm_large']       = ['Are you sure that you want this set to', YES]
        param_map['confirm_small'] = \
              ['may significantly disrupt the ability of this appliance to function', YES]
        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')
        return self._process_input(param_map)

    def clusterset(self):
        raise ccb.IafCliCtorNotImplementedError

    def clustershow(self):
        raise ccb.IafCliCtorNotImplementedError

class antispamconfigCloudmark(ccb.IafCliConfiguratorBase):
    """antispamconfig -> CLOUDMARK """


    def setup(self, input_dict=None, **kwargs):


        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['use_cloudmark']        = ['to use Cloudmark Service', DEFAULT]
        param_map['max_msg_size']         = ['largest size message', DEFAULT]
        param_map['timeout']              = ['scanning timeout', DEFAULT]
        param_map['reputation_filter_incoming'] = ['filtering for incoming messages', DEFAULT]
        param_map['reputation_filter_outgoing'] = ['filtering for outgoing messages', DEFAULT]
        param_map['confirm_disable']      = ['want to disable', YES]
        param_map['license_agreement']    = ['license agreement?', YES]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)

    def clusterset(self):
        raise ccb.IafCliCtorNotImplementedError

    def clustershow(self):
        raise ccb.IafCliCtorNotImplementedError

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    asc = antispamconfig(cli_sess)
    # "license_agreement" needs to be taken out if it's been answered before
    #asc(vendor='multiscan').setup(use_ims='Y',scan_size='12345',scan_timeout='10',region_scan='Y')
    #asc(vendor='brightmail').setup()
    asc(vendor='ironport').setup()
    #asc(vendor='ironport').setup(use_case=NO, confirm_disable=YES)
    #asc(vendor='ironport').setup(use_case=NO, confirm_disable=YES)


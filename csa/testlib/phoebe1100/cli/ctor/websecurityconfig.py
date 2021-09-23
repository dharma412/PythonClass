#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/websecurityconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap

from sal.containers.yesnodefault import YES, NO


class websecurityconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self, input_dict=None, **kwargs):
        self._writeln('websecurityconfig')
        param_map = IafCliParamMap(end_of_command=self._get_prompt())

        param_map['url_enable'] = ['Enable URL Filtering', DEFAULT]
        param_map['url_disable'] = ['Disable URL Filtering', DEFAULT]
        param_map['urllist_add'] = ['whitelist URLs using a URL list', DEFAULT]
        param_map['clientcert_set'] = ['want to set client certificate', DEFAULT]
        param_map['urllist_number'] = ['Enter the number of URL list', REQUIRED]
        param_map['certificate_number'] = ['Choose the certificate', REQUIRED]
        param_map['enable_url_clicktracking'] = ['enable Web Interaction Tracking', DEFAULT]
        param_map['disable_url_clicktracking'] = ['disable Web Interaction Tracking', DEFAULT]

        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

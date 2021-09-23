#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/websecurityadvancedconfig.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap


class websecurityadvancedconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self, input_dict=None, **kwargs):
        self._writeln('websecurityadvancedconfig')
        param_map = IafCliParamMap(end_of_command=self._get_prompt())

        param_map['timeout_value'] = ['Enter URL lookup timeout', DEFAULT]
        param_map['cache_size'] = ['Enter the URL cache size', DEFAULT]
        param_map['disable_dns'] = ['Do you want to disable DNS lookups', DEFAULT]
        param_map['max_urls'] = [
            'Enter the maximum number of URLs that can be scanned in the attachments in a message:', DEFAULT]
        param_map['max_urls_msg_body'] = ['Enter the maximum number of URLs that can be scanned in a message body',
                                          DEFAULT]
        param_map['web_hostname'] = ['Enter the Web security service hostname:', DEFAULT]
        param_map['threshold_value'] = ['Enter the threshold value for outstanding requests:', DEFAULT]
        param_map['verify_servercert'] = ['Do you want to verify server certificate', DEFAULT]
        param_map['url_shortened_url'] = ['Do you want to enable URL filtering for shortened URLs', DEFAULT]
        param_map['ttl_value'] = ['Enter the default time-to-live value', DEFAULT]
        param_map['rewrite_url_text_href'] = ['want to rewrite both the URL text and the href in the message', DEFAULT]
        param_map['additional_headers'] = ['want to include additional headers', DEFAULT]
        param_map['headers_name'] = ['Enter the headers', REQUIRED]
        param_map['loglevel_rpc'] = ['default debug log level for RPC server:', DEFAULT]
        param_map['loglevel_sds'] = ['default debug log level for URL cache:', DEFAULT]
        param_map['loglevel_http'] = ['default debug log level for HTTP client:', DEFAULT]

        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

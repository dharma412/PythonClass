#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/websecurityadvancedconfig.py#2 $
# $DateTime: 2020/01/16 23:03:15 $
# $Author: saurgup5 $

import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap

class websecurityadvancedconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self, input_dict=None, **kwargs):
        self._writeln('websecurityadvancedconfig')
        param_map = IafCliParamMap(end_of_command=self._get_prompt())

        param_map['timeout_value'] = ['Enter URL lookup timeout', DEFAULT]
        param_map['max_urls'] = ['Enter the maximum number of URLs', DEFAULT]
        param_map['max_urls_attachment'] = ['Enter the maximum number of URLs', DEFAULT]
        param_map['rewrite_url_text_href'] = ['want to rewrite both the URL text and the href in the message', DEFAULT]
        param_map['additional_headers'] = ['want to include additional headers', DEFAULT]
        param_map['headers_name'] = ['Enter the headers', REQUIRED]

        param_map.update(input_dict or kwargs)
        self._process_input(param_map)
        output = self.getbuf()
        return output

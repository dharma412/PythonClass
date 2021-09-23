#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/supportrequest.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

"""
CLI command: supportrequest
"""

import socket
import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliParamMap,\
                        ConfigError, DEFAULT, REQUIRED
from sal.containers.yesnodefault import YES, NO

class supportrequest(IafCliConfiguratorBase):

    def __call__(self, def_rcp=DEFAULT, add_rcp=DEFAULT, rcp_email=None,
                exist_tick=DEFAULT, tick_num=None, tech=DEFAULT,
                sub_tech=DEFAULT, appliance=DEFAULT, categ=DEFAULT,
                input_dict=None, **kwargs):
        param_map = \
        IafCliParamMap(end_of_command='This may take about 5 minutes...')
        self._restart()
        self._writeln(self.__class__.__name__)

        # Do you want to send the support request to supportrequest@mail.qa?
        self._query_response(def_rcp)
        # Do you want to send the support request to additional recipient(s)
        self._query_response(add_rcp)
        if add_rcp.lower() == 'y':
            self._query_response(rcp_email)
        # Is this support request associated with an existing support ticket
        self._query_response(exist_tick)
        if exist_tick.lower() == 'y':
            self._query_response(tick_num)
        # Please select a technology related to this support request
        self._query_response(tech)
        # Please select a subtechnology related to this support request
        self._query_response(sub_tech)

        idx = self._query('the appliance to which this support request applies',
                          'select the problem category')
        if idx == 0:
            self._query_select_list_item(appliance)
            self._query_response(categ)
        elif idx == 1:
            self._query_response(categ)
        else:
            raise ConfigError('supportrequest: unexpected response')

        param_map['sub_categ'] = ['select a problem sub-category', DEFAULT, True]
        param_map['subject'] = ['enter a subject line', REQUIRED]
        param_map['descr'] = ['enter a description of your issue', REQUIRED]
        param_map['select_ccoid'] = ['It is important to associate all your service contracts', DEFAULT]
        param_map['ccoid_contact'] = ['Please enter the CCOID of the contact person', REQUIRED]
        param_map['ccoid_name'] = ['Please enter the name of the contact person', REQUIRED]
        param_map['contract_id'] = ['Please enter the contract ID', REQUIRED]
        param_map['add_info'] = ['enter any additional contact', DEFAULT]
        param_map['corr_email']  = ['email address of your CCO User ID', REQUIRED]

        params = input_dict or kwargs
        print_req_ans = params.pop('print_req', DEFAULT)

        param_map.update(params)
        self._process_input(param_map, do_restart=False, timeout=400)

        self._sess.clearbuf()
        self._query_response(print_req_ans, timeout=120)

        return self._wait_for_prompt_line()


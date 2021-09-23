#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/supportrequest.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
CLI command: supportrequest
"""
import clictorbase

from clictorbase import IafCliConfiguratorBase, IafCliParamMap,\
    DEFAULT, REQUIRED

class supportrequest(IafCliConfiguratorBase):

    def __call__(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command=self._get_prompt())
        global DEFAULT, REQUIRED
        self._restart()
        self._writeln('supportrequest')
        param_map['def_rcp']    = \
        ['Do you wish to send this information to Cisco', DEFAULT]
        param_map['add_rcp']    = ['request to additional recipient(s)', DEFAULT]
        param_map['rcp_email']  = \
        ['email address(es) to which you want to send the support request', REQUIRED]
        param_map['select_ccoid'] = ['Select the CCOID', DEFAULT, True]
        param_map['new_ccoid'] = ['enter the CCOID', REQUIRED]
        param_map['name']       = ['name of the contact person', REQUIRED]
        param_map['contract_id'] = ['enter the contract ID', REQUIRED]
        param_map['email']      = ['email address of your CCO User ID', REQUIRED]
        param_map['phone']      = ['contact phone number', DEFAULT]
        param_map['subject']    = ['provide a subject for the issue', REQUIRED]
        param_map['comment']    = ['enter some comments describing', REQUIRED]
        param_map['exist_tick'] = ['Is this support request', DEFAULT]
        param_map['tick_num']   = ['enter the ticket number', REQUIRED]
        param_map['tech']       = ['select a technology', DEFAULT, 1]
        param_map['subtech']    = ['select a subtechnology', DEFAULT, 1]
        param_map['cat']        = ['select the problem category', DEFAULT, 1]
        param_map['subcat']     = ['select a problem sub-category', DEFAULT, 1]
        params = input_dict or kwargs

        param_map.update(params)
        return self._process_input(param_map, do_restart=False, timeout=20)

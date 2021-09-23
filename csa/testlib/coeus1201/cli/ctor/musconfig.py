#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/musconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import clictorbase

class musconfig(clictorbase.IafCliConfiguratorBase):
    """Configure settings for AnyConnect Secure Mobility."""
    def __call__(self):
        command = 'musconfig'
        self._writeln(command)
        self._validate_agreement()
        return self

    def _validate_agreement(self):
        """Agreement handling."""
        idx = self._query(self._sub_prompt, ' you want to accept AnyConnect')
        if idx == 1:
            # confirm agreement
            self._writeln('Y')
            self._writeln()

    def _setup_mode(self, mode):
        modes = {'ip': 1, 'asa': 2}
        self._writeln('SETUP')
        self._query_response('Y')
        self._query_response(modes[mode.lower()])

    def edit(self, item_old='', item_new='', port='', mode=''):
        self._setup_mode(mode)
        self._query_response('EDIT')
        self._query_select_list_item(item_old)
        self._query_response(item_new)
        if mode == 'asa':
            self._query_response(port)
        self._to_the_top(1)

    def new(self, item='', port='', mode=''):
        self._setup_mode(mode)
        self._query_response('NEW')
        self._query_response(item)
        if mode == 'asa':
            self._query_response(port)
        self._to_the_top(1)

    def delete(self, item='', mode=''):
        if item.lower() != 'all':
            self._setup_mode(mode)
            self._query_response('DELETE')
            self._query_select_list_item(item)
        else:
            self._to_the_top(1)
            command = 'musconfig setup yes configure_%s clear' % (mode,)
            self._writeln(command)
        self._to_the_top(1)

    def shared_secret(self, secret=''):
        self._setup_mode('asa')
        self._query_response('shared_secret')
        self._query("Please enter the shared password")
        self._writeln(secret)
        self._query("Please enter shared password again")
        self._writeln(secret)
        self._to_the_top(1)

    def disable(self):
        self._to_the_top(1)
        self._writeln('musconfig setup no')

    def enable(self, mode=''):
        self._to_the_top(1)
        modes = {'ip': 'configure_ip', 'asa': 'configure_asa'}
        command = 'musconfig setup yes'
        if mode:
            command = ' '.join([command, mode])
        self._writeln(command)

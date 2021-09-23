#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/trace.py#1 $

import socket
import time

import clictorbase
import sal
from sal.containers.yesnodefault import YES, NO


class trace(clictorbase.IafCliConfiguratorBase):

    def __call__(self, source_ip=None, fqdn=None, injector_name=None,
                 use_smtp=NO, smtp_user=None,
                 domain_name=None,
                 owner_id=None, sbrs_score=None, mail_from=None, rcpt_addrs=None,
                 load_from_disk=YES, file_name=None, msg_body=None,
                 reuse_msg_body=NO, see_result=YES, debug_session=NO):
        """ trace the flow of a message """

        self.clearbuf()
        self._writeln('trace')
        self._query_response(source_ip)
        self._query_response(fqdn)
        self._query_select_list_item(injector_name)

        ##89374
        idx = self._query('configure the SMTP Authentication', 'domain name')
        if idx == 0:
            self._query_response(use_smtp)
            if use_smtp:
                self._query_response(smtp_user)

        self._query_response(domain_name)
        self._query_response(owner_id)
        self._query_response(sbrs_score)
        self._query_response(mail_from)
        self._query_response(rcpt_addrs)

        idx = self._query('Re-use last message body', 'Load message from disk')
        if idx == 0:
            self._query_response(reuse_msg_body)
        if (idx == 0 and reuse_msg_body == NO) or idx == 1:
            self._query_response(load_from_disk)
            if load_from_disk == YES:
                self._query_response(file_name)
            else:
                msg_body = msg_body or 'test Body'
                self._query('Enter or paste the message body here')
                self._writeln(msg_body + '\n.')

        tmr = sal.time.CountDownTimer(60).start()
        while tmr.is_active():
            exc = None
            try:
                idx = self._query('resulting message', 'debug session')
                break
            except Exception as e:
                exc = e
                time.sleep(1)
        else:
            raise exc
        if idx == 0:
            self._query_response(see_result)
        self._query_response(debug_session)
        self._wait_for_prompt()
        return self.getbuf()

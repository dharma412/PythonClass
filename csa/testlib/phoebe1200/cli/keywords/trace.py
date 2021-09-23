#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/trace.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class trace(CliKeywordBase):
    """Keywords for trace cli command. """

    def get_keyword_names(self):
        return ['trace']

    def trace(self, *args):
        """
        Parameters:
        - `source_ip` : The source ip address of the remote client for the trace
        - `fqdn` : fully qualified domain name of the source IP (If left blank,
         a reverse DNS lookup will be performed on the source IP. To clear the
         existing value, enter 'NONE')
        - `injector_name` :  One of the listeners configured from the system to
           emulate sending the test message to.
        - `use_smtp` : Do you want to configure SMTP Authentication username to
           simulate the session. Either YES or NO
        - `smtp_user` : SMTP Authentication Username
        - `domain_name` : the domain name that has to be passed to HELO/EHLO
        - `owner_id` : the SenderBase Network Owner ID of the source IP.
           The actual ID is N/A
        - `sbrs_score` : the SenderBase Reputation Score of the source IP.
           The actual score is N/A.
        - `mail_from` : the Envelope Sender address. Can be proper email id.
        - `rcpt_addrs` : the Envelope Recipient addresses. Multiple email ids
           should be seperated by commas.
        - `load_from_disk` : Specify if we would want to load form the disk.
           Values can be YES or NO.
        - `file_name` : The name of the filename to be loaded form the disk .
          This option is present when YES is given for the load-from-disk value.
        - `msg_body` : The message body to be sent. This option is valid only
           when we give NO in the load_from_disk option.
        - `reuse_msg_body` : This option is available only if trace is run for
           second time.
        - `see_result` : If we would want to check for the result. Values can be
           YES or NO
        - `debug_session` : If we would want to have another Trace Session.
           Value can be yes or no.

        Examples:
        | ${log}= |  Trace | source_ip=10.1.1.1 | fqdn=smtp.example.com |
        | ... | injector_name=public_smtp |
        | ... | owner_id=66 | sbrs_score=5 | mail_from=test@qa42.qa |
        | ... | rcpt_addrs=test0@qa42.qa | load_from_disk=NO | file_name=None |
        | ... | msg_body=Testing | reuse_msg_body=NO | see_result=YES |
        | ... | debug_session=NO |

        | Trace | source_ip=10.2.2.2 | fqdn=smtp.example.com |
        | ... | injector_name=public_smtp |
        | ... | owner_id=66 | sbrs_score=5 | mail_from=test@qa42.qa |
        | ... | rcpt_addrs=test0@qa42.qa | load_from_disk=NO |
        | ... | file_name=Test.txt | reuse_msg_body=NO |
        | ... | see_result=NO | debug_session=NO |
        """
        kwargs = self._convert_to_dict(args)
        if kwargs.has_key('reuse_msg_body'):
            kwargs['reuse_msg_body'] = self._set_yes_no_object(kwargs['reuse_msg_body'])
        if kwargs.has_key('load_from_disk'):
            kwargs['load_from_disk'] = self._set_yes_no_object(kwargs['load_from_disk'])
        return str(self._cli.trace(**kwargs))

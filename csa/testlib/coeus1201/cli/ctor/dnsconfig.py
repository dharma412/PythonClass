#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/dnsconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import clictorbase as ccb
from sal.deprecated.expect import EXACT, REGEX
REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT

class DuplicateEntry(ccb.IafCliError):
    """Did we enter a DNS server that already exists?, Raise this error """
    pass

class dnsconfig(ccb.IafCliConfiguratorBase):
    local_server = '1'
    alt_server  = '2'

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
               {('already appears to be configured for domain',
                        EXACT): DuplicateEntry,
                ('already configured with priority', EXACT): DuplicateEntry}
        )

    def __call__(self, command_str=None):

        self.clearbuf()
        command = 'dnsconfig'
        if command_str:
            command = ' '.join([command, command_str,])

        self._writeln(command)

        self._query(('Currently using the (\w+) ', REGEX))
        self.root_servers = {
            'local':False,
            'Internet':True
        }[self._get_last_mo().group(1)]

        if not command_str:
            self._query('Choose the operation')
            self.configured_server_text = self._get_last_matched_text()
        else:
            self._wait_for_prompt(3)

        return self


    def new(self, input_dict=None, **kwargs):
        self.clearbuf()
        self._query_response('NEW')
        param_map = ccb.IafCliParamMap(end_of_command= 'Choose the operation')
        if self.root_servers:
            param_map['ip_addr'] = ('enter the IP address', REQUIRED)  ##For the secondary DNS server option
            param_map['dns_set'] = ('Primary DNS nameserver list or secondary', REQUIRED)  ##New option for secondary DNS
            param_map['priority'] = ('enter the priority', REQUIRED)   ##For the secondary DNS server option
            param_map['auth_domain'] = ('enter the domain', REQUIRED)
            param_map['hostname'] = ('fully qualified hostname', REQUIRED)

        else:
            param_map['dns_set'] = ('or secondary DNS nameserver', REQUIRED)
            param_map['which_server'] = ('Do you want to add', REQUIRED)
            param_map['domain_name'] = ('enter the domain', REQUIRED)
            param_map['ip_addr'] = ('enter the IP address', REQUIRED)
            param_map['priority'] = ('enter the priority', DEFAULT)

        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def setup(self, input_dict=None, **kwargs):
        self._query_response('SETUP')
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['use_own']=['use your own DNS servers', DEFAULT, 1]
        param_map['routing_table']=['the routing table to use', DEFAULT, 1]
        param_map['ip_addr']=['enter the IP address', REQUIRED]
        param_map['priority']=['enter the priority', DEFAULT]
        param_map['rev_dns_timeout']=['before timing out reverse DNS', DEFAULT]
        param_map['min_ttl'] = ['minimum TTL in seconds', DEFAULT]
        param_map['preference']=['Choose a preference', DEFAULT, 1]
        param_map['failed_attempts']=['number of failed attempts before', DEFAULT]
        param_map['polling_interval']=['interval in seconds for polling', DEFAULT]
        param_map.update(input_dict or kwargs)

        return self._process_input(param_map)

    def edit(self, ip_addr, auth_domain='', hostname='',
                                        new_ip_addr='',
                                        priority='',
                                        domain_name='',
                                        dns_set='',
                                        which_server=''):
        self._writeln('EDIT')
        if self.root_servers:
            self._parse_input_list(self.getbuf())
            i = self._query('Primary DNS nameserver list or secondary','Alternate authoritative DNS')
            if i == 0:
                 self._query_response(dns_set)
                 n = self._query('server you wish to edit','Alternate authoritative DNS')
                 self._info("DEBUG****")
                 self._info(n)
                 if n == 1:
                     self._select_list_item(ip_addr, self.getbuf())
                     self._query_response(domain_name)
                     self._query_response(hostname)
                     self._query_response(new_ip_addr)
                 else :
                     self._select_list_item(ip_addr, self.getbuf())
                     self._query_response(new_ip_addr)
                     self._query('enter the priority')
                     self._query_response(priority)
            else:
                 self._select_list_item(ip_addr, self.getbuf())
                 self._query_response(domain_name)
                 self._query_response(hostname)
                 self._query_response(new_ip_addr)
        else:
            #Do you want to edit a new local DNS cache server or an
            # alternate domain server?
            #1. Edit a new local DNS cache server.
            #2. Edit a new alternate domain server.
            self._query_parse_input_list()
            i = self._query('Primary DNS nameserver list or secondary','Do you want to edit a local DNS')
            if i == 0 : self._query_response(dns_set)
            if int(dns_set) == 1:
                if which_server == '1':
                    self._query_response(which_server)
                    self._query('Currently using the')
                    self._query_select_list_item(ip_addr, self.getbuf())
                    self._query_response(new_ip_addr)
                    self._query_response(priority)
                elif which_server == '2':
                    self._query_response(which_server)
                    self._query('Alternate DNS servers')
                    self._query_select_list_item(ip_addr, self.getbuf())
                    self._query_response(domain_name)
                    self._query_response(new_ip_addr)
                else:
                    raise ValueError('Wrong server type.')
            else:
                self._query('Currently using the')
                self._query_select_list_item(ip_addr, self.getbuf())
                self._query_response(new_ip_addr)
                self._query_response(priority)
        self._to_the_top(1)

    #def delete(self, input_dict=None, **kwargs):
    def delete(self, which_server='', ip_addr='', dns_set=''):
        self.clearbuf()
        self._query_response('DELETE')
        n = self._query(
            'Do you want to make changes in the Primary DNS',
            'Do you want to delete a local DNS cache server or' \
            ,'Alternate authoritative DNS'
        )
        self._info(self.getbuf())
        if n == 0 :
            self._query_response(dns_set)
            i = self._query(
                'Delete a local DNS cache server',
                'Currently using the following Secondary'
            )
            if i == 0:
                n = 1
            else:
                pass
        if n == 1:
            self._query_response(which_server)
            self._query('Currently using the','Alternate DNS servers')

        self._query_select_list_item(ip_addr, self.getbuf())
        self._to_the_top(1)

    def current(self):
        self._parse_input_list(self.getbuf())
        self._writeln()
        self._wait_for_prompt()
        return self._get_input_list_dict()

    # We are not composing cluster methods at this time because we
    # cannot test them.
    def clusterset(self):
        raise ccb.IafCliNotImplementedError

    def clustershow(self):
        raise ccb.IafCliNotImplementedError

    def search(self, list=None):

        self._to_the_top(1)
        self._to_the_top(1)
        command = 'dnsconfig search'

        if list is not None:
            for option in list:
                if str(option).lower().find('delete') != 0:
                    command = ' '.join([command, 'delete'])
                    self._writeln(command)
                    return

            command = ' '.join([command, list])
        self._writeln(command)


if __name__=='__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    from iafframework import iafcfg
    dns_prefix = '172.28.0'
    iface = 'Management'

    try:
        cli_sess
        dns_prefix = '172.28.0'
        iface = 'main'
    except NameError:
        cli_sess = ccb.get_sess()
        my_host = iafcfg.get_hostname()
        if my_host.find('.eng') > -1:
            dns_prefix = '172.16.0'
            iface = 'main'

    dc = dnsconfig(cli_sess)

    print dc().current()
    dc().new(ip_addr='%s.4' % dns_prefix, priority=15,
             which_server=dc.local_server)
    print dc().current()
    dc().edit(ip_addr='%s.4' % dns_prefix, priority=10)
    print dc().current()
    dc().edit(ip_addr='%s.4' % dns_prefix, new_ip_addr='%s.5' % dns_prefix)
    print dc().current()
    dc().delete(which_server=dc.local_server, ip_addr='%s.5' % dns_prefix)
    print dc().current()
    dc().setup(use_own='Internet', rev_dns_timeout='40')
    dc().setup(use_own='Internet', routing_table='Data', rev_dns_timeout='30')
    dc().new(auth_domain='foobar', hostname='a.foobar', ip_addr='1.2.3.4')
    print dc().current()
    dc().edit(ip_addr='1.2.3.4', auth_domain='foo',
                            hostname='a.foo', new_ip_addr='1.2.3.5')
    print dc().current()
    dc().delete(which_server=dc.alt_server, ip_addr='1.2.3.5')
    print dc().current()

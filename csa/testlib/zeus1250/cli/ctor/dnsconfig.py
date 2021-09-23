#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/dnsconfig.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

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

    def __call__(self):
        self._writeln('dnsconfig')
        self._query(('Currently using the (\w+) ', REGEX))
        self.root_servers = {'local':False, 'Internet':True}[
                                                self._get_last_mo().group(1)]
        self._query('Choose the operation')
        self.configured_server_text = self._get_last_matched_text()
        return self

    def new(self, input_dict=None, **kwargs):
        self.clearbuf()
        self._query_response('NEW')
        param_map = ccb.IafCliParamMap(end_of_command= 'Choose the operation')
        if self.root_servers:
            param_map['auth_domain'] = ('enter the domain', REQUIRED)
            param_map['hostname'] = ('fully qualified hostname', REQUIRED)
            param_map['ip_addr'] = ('enter the IP address', REQUIRED)
        else:
            param_map['which_server'] = ('Do you want to add', REQUIRED, 1)
            param_map['domain_name'] = ('enter the domain', REQUIRED)
            param_map['ip_addr'] = ('enter the IP address', REQUIRED)
            param_map['priority'] = ('enter the priority', DEFAULT)

        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def setup(self, input_dict=None, **kwargs):
        self._query_response('SETUP')
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['use_own']=['use your own DNS servers', DEFAULT, 1]
        param_map['iface']=['IP interface for DNS', DEFAULT, 1]
        param_map['ip_addr']=['enter the IP address', REQUIRED]
        param_map['priority']=['enter the priority', DEFAULT]
        param_map['rev_dns_timeout']=['before timing out reverse DNS', DEFAULT]
        param_map['minimum_ttl']=['minimum TTL in seconds', DEFAULT]
        param_map.update(input_dict or kwargs)

        return self._process_input(param_map)

    def edit(self, ip_addr, auth_domain='', hostname='', new_ip_addr='',
        priority=''):
        self._writeln('EDIT')
        if self.root_servers:
            self._parse_input_list(self.getbuf())
            self._query()
            self._select_list_item(ip_addr)
            self._query_response(auth_domain)
            self._query_response(hostname)
            self._query_response(new_ip_addr)
        else:
            #Do you want to edit a new local DNS cache server or an
            # alternate domain server?
            #1. Edit a new local DNS cache server.
            #2. Edit a new alternate domain server.
            self._query_parse_input_list()
            self._query_response('1') # hack: hard code for now. needs fixing
            self._query_select_list_item(ip_addr)
            self._query_response(new_ip_addr)
            self._query_response(priority)
        self._to_the_top(1)

    def delete(self, which_server=DEFAULT, ip_addr=REQUIRED):
        self._query_response('DELETE')
        if self.root_servers:
            self._parse_input_list(self.configured_server_text)
            self._query()
            self._select_list_item(ip_addr)
        else:
            self._query_select_list_item(which_server)
            self._query_select_list_item(ip_addr)

        self._to_the_top(1)


if __name__=='__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    from iafframework import iafcfg
    dns_prefix = '172.17.0'
    iface = 'Management'

    try:
        cli_sess
        dns_prefix = '172.16.0'
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
    dc().setup(use_own='Internet', iface=iface, rev_dns_timeout='40')
    dc().new(auth_domain='foobar', hostname='a.foobar', ip_addr='1.2.3.4')
    print dc().current()
    dc().edit(ip_addr='1.2.3.4', auth_domain='foo',
                            hostname='a.foo', new_ip_addr='1.2.3.5')
    print dc().current()
    dc().delete(which_server=dc.local_server, ip_addr='1.2.3.5')
    print dc().current()

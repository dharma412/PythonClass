#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/dig.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

import clictorbase


class dig(clictorbase.IafCliConfiguratorBase):
    """
    CLI command: dig
    """

    def __call__(self, input_dict=None, **kwargs):
        params = input_dict or kwargs
        host = params.get('hostname', None)
        if not host:
            raise clictorbase.IafCliValueError \
                ('Enter the host or IP address to look up. Input was: "%s"' % host)
        self._sess.writeln(self.__class__.__name__)
        self._query_response(host)
        self._query_select_list_item \
            (params.get('query_type', 1), exact_match=True)
        self._query_select_list_item(params.get('query_from_interface', 1))
        self._query_response(params.get('dns_server', clictorbase.DEFAULT))
        self._query_response(params.get('query_over_tcp', clictorbase.DEFAULT))
        return self._sess.read_until()

    def dig_batch_lookup_record(self, input_dict=None, **kwargs):
        cmd = self.__class__.__name__
        opts = input_dict or kwargs
        if not opts:
            return cmd
        host = opts.get('hostname', None)
        if not host:
            raise clictorbase.IafCliValueError \
                ('Host parameter is required.')
        if opts.has_key('source_ip'):
            cmd += " -s %s" % (opts['source_ip'])
        if opts.has_key('query_over_tcp'):
            cmd += ' -t'
        if opts.has_key('query_over_udp'):
            cmd += ' -u'
        if opts.has_key('dns_ip'):
            cmd += ' @%s' % opts['dns_ip']
        if opts.has_key('query_type'):
            cmd += ' %s' % opts['query_type']
        cmd += ' %s' % host
        self._sess.writeln(cmd)
        return self._sess.read_until()

    def dig_batch_lookup_reverse(self, input_dict=None, **kwargs):
        cmd = self.__class__.__name__ + ' -x '
        opts = input_dict or kwargs
        if not opts:
            return cmd
        ip = opts.get('reverse_ip', None)
        if not ip:
            raise clictorbase.IafCliValueError \
                ('Reverse lookup IP address is required.')
        cmd += ' %s' % ip
        if opts.has_key('query_over_tcp'):
            cmd += ' -t'
        if opts.has_key('query_over_udp'):
            cmd += ' -u'
        if opts.has_key('dns_ip'):
            cmd += ' @%s' % opts['dns_ip']
        self._sess.writeln(cmd)
        return self._sess.read_until()

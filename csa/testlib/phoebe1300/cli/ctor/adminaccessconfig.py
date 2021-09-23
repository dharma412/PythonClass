#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/adminaccessconfig.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

"""
SARF CLI command: adminaccessconfig
"""

import clictorbase
from sal.deprecated.expect import REGEX

command_adminaccessconfig = 'adminaccessconfig'


class adminaccessconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    class NonExistedFileError(clictorbase.IafCliError):
        pass

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Error: the file ".+?" does not exist.', REGEX): \
                self.NonExistedFileError})

    def __call__(self):
        self._restart()
        self._writeln(command_adminaccessconfig)
        return self

    def banner(self):
        self._query_response('BANNER')
        return BannerAdminAccessConfig(self._get_sess())

    def welcome(self):
        self._query_response('WELCOME')
        return WelcomeAdminAccessConfig(self._get_sess())

    def timeout(self):
        self._query_response('TIMEOUT')
        return TimeoutAdminAccessConfig(self._get_sess())

    def ipaccess(self, mode=None):
        self._query_response('IPACCESS')

        if mode is None:
            next_step = IpAccessAdminAccessConfig(self._get_sess())
        elif mode.lower() == 'restrict':
            response_string = 'RESTRICT'
            next_step = RestrictIpAccessAdminAccessConfig(self._get_sess())
        elif mode.lower() == 'proxy':
            response_string = 'PROXY'
            next_step = ProxyIpAccessAdminAccessConfig(self._get_sess())
        elif mode.lower() == 'proxyonly':
            response_string = 'PROXYONLY'
            next_step = ProxyIpAccessAdminAccessConfig(self._get_sess())

        if mode is not None:
            self._query_response(response_string)
        return next_step

    def csrf(self):
        self._query_response('CSRF')
        return CsrfAdminAccessConfig(self._get_sess())

    def print_info(self, command=None):
        if command == None:
            return None
        self._to_the_top(self.newlines)
        self.clearbuf()
        self._writeln(command_adminaccessconfig + ' ' + command + ' print')
        output_string = self._wait_for_prompt(timeout=180)
        output_string = output_string[output_string.find('\n'):output_string.rfind('\n')]
        return output_string.replace('\n', '')

    def how_tos(self):
        self._query_response('HOW-TOS')
        return HowTosAdminAccessConfig(self._get_sess())


class IpAccessAdminAccessConfig(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def __init__(self, sess, mode=None):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def allow_all(self):
        self._query_response('ALL')
        self._to_the_top(self.newlines)

    def change_mode(self, mode):
        self._query_response(mode)
        steps = self.newlines

        if mode.lower() != 'all':
            if mode.lower() == 'restrict':
                steps = steps + 1
            else:
                steps = steps + 2

        self._to_the_top(steps)


class RestrictIpAccessAdminAccessConfig(clictorbase.IafCliConfiguratorBase):
    edit_ip = True

    def __init__(self, sess, newlines=3):
        self.newlines = newlines
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def _to_the_top(self, lines):
        buf = self._sess.getbuf()
        # Asks for confirmation when ip other than current host is given
        if buf.find('the host you are currently using') != -1:
            self._writeln('Y')
        clictorbase.IafCliConfiguratorBase._to_the_top(self, lines)

    def new(self, ip=clictorbase.REQUIRED):
        self._query_response('NEW')
        self._query_response(ip)
        self._to_the_top(self.newlines)

    def get_right_buffer(self):
        got_buffer = self._sess.getbuf()

        if not self.edit_ip:
            got_buffer = got_buffer[got_buffer.rfind('allowed proxy'):-1]
            got_buffer = got_buffer[:got_buffer.find(self._get_prompt().hostname)]
        return got_buffer

    def edit(self, old_ip=clictorbase.REQUIRED,
             new_ip=clictorbase.REQUIRED):
        self._query_response('EDIT')

        got_buffer = self.get_right_buffer()
        self._select_list_item(old_ip, got_buffer)
        self._query_response(new_ip)
        self._to_the_top(self.newlines)

    def delete(self, ip=clictorbase.REQUIRED):
        self._query_response('DELETE')
        got_buffer = self.get_right_buffer()
        self._select_list_item(ip, got_buffer)
        self._to_the_top(self.newlines)

    def clear(self, ip=clictorbase.REQUIRED):
        self._query_response('CLEAR')

        if ip is not None:
            self.new(ip)
        else:
            self._to_the_top(self.newlines)


class ProxyIpAccessAdminAccessConfig(RestrictIpAccessAdminAccessConfig,
                                     clictorbase.IafCliConfiguratorBase):
    newlines = 4

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def proxylist(self):
        self._writeln('')
        self._writeln('PROXY_LIST')
        proxy_edit = RestrictIpAccessAdminAccessConfig(self._get_sess(), 4)
        proxy_edit.edit_ip = False
        return proxy_edit

    def proxyheader(self, header_name=None):
        self._writeln('')
        self._writeln('ORIGIN_IP_HEADER')
        self._query_response(header_name)
        self._to_the_top(self.newlines - 1)


class CsrfAdminAccessConfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def enable(self):
        self._writeln('Y')
        self._to_the_top(self.newlines)

    def disable(self):
        self._writeln('N')
        self._to_the_top(self.newlines)


class BannerAdminAccessConfig(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def new(self, banner_str):
        self._query_response('NEW')
        self._sess.writeln(banner_str)
        self._sess.write("\x04")  # ^D (CTRL-D)
        self._to_the_top(self.newlines)

    def delete(self):
        self._query_response('DELETE')
        self._to_the_top(self.newlines)

    def import_banner(self, filename):
        self._query_response('IMPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)


class WelcomeAdminAccessConfig(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def new(self, welcome_str):
        self._query_response('NEW')
        self._sess.writeln(welcome_str)
        self._sess.writeln("\x04")  # ^D (CTRL-D)
        self._to_the_top(self.newlines)

    def delete(self):
        self._query_response('DELETE')
        self._to_the_top(self.newlines)

    def import_welcome(self, filename):
        self._query_response('IMPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def export_welcome(self, filename):
        self._query_response('EXPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)


class TimeoutAdminAccessConfig(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def settime(self, webui, cli):
        self._query_response(webui)
        self._query_response(cli)
        self._to_the_top(self.newlines)


class HowTosAdminAccessConfig(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def enable(self):
        self._query_response('Y')
        self._to_the_top(self.newlines)

    def disable(self):
        self._query_response('N')
        self._to_the_top(self.newlines)

    def status(self):
        self.clearbuf()
        self._query_response('\n')
        self._to_the_top(self.newlines)
        return self._sess.getbuf()

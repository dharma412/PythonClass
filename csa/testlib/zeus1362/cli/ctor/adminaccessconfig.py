#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/adminaccessconfig.py#2 $ $DateTime: 2020/06/18 05:28:57 $ $Author: mrmohank $

"""
SARF CLI command: adminaccessconfig
"""

import clictorbase
#import sal.containers.yesnodefault as yesnodefault
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
             self.NonExistedFileError })

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

    def hostheader(self):
        self._query_response('HOSTHEADER')
        return HostHeaderAdminAccessConfig(self._get_sess())

    def print_info(self, command=None):
        if command == None:
            return None
        self._to_the_top(self.newlines)
        self.clearbuf()
        self._writeln(command_adminaccessconfig + ' ' + command +' print')
        output_string = self._wait_for_prompt(timeout=180)
        output_string = output_string[output_string.find('\n'):output_string.rfind('\n')]
        return output_string.replace('\n','').replace('\r','')

class IpAccessAdminAccessConfig(clictorbase.IafCliConfiguratorBase):

    newlines = 2

    def __init__(self, sess, mode=None):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def allow_all(self):
        self._query_response('ALL')
        self._to_the_top(self.newlines)

    def change_mode(self,mode):
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

    def new(self, ip = clictorbase.REQUIRED):
        self._query_response('NEW')
        self._query_response(ip)
        self._writeln('')
        try:
            if self._query('Current mode:')==0:
                self._to_the_top(self.newlines)
        except:
            self._writeln('Y')
            self._to_the_top(self.newlines)

    def get_right_buffer(self):
        got_buffer = self._sess.getbuf(clear_buf = False)

        if not self.edit_ip:
            got_buffer = got_buffer[got_buffer.rfind('allowed proxy'):-1]
            got_buffer = got_buffer[:got_buffer.find(self._get_prompt().hostname)]
        return got_buffer

    def edit(self, old_ip = clictorbase.REQUIRED,
             new_ip = clictorbase.REQUIRED):
        self._query_response('EDIT')

        got_buffer = self.get_right_buffer()
        self._select_list_item(old_ip, got_buffer)
        self._query_response(new_ip)
        self._to_the_top(self.newlines)

    def delete(self, ip = clictorbase.REQUIRED):
        self._query_response('DELETE')
        got_buffer = self.get_right_buffer()
        self._select_list_item(ip, got_buffer)
        self._to_the_top(self.newlines)

    def clear(self, ip = clictorbase.REQUIRED):
        self._query_response('CLEAR')

        if ip is not None:
            self.new(ip)
        else:
            self._query_response('N')
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

class BasicYesNoAdminAccessConfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def enable(self):
        self._writeln('Y')
        self._to_the_top(self.newlines)

    def disable(self):
        self._writeln('N')
        self._to_the_top(self.newlines)

class CsrfAdminAccessConfig(BasicYesNoAdminAccessConfig):
    pass

class HostHeaderAdminAccessConfig(BasicYesNoAdminAccessConfig):
    pass

class BannerAdminAccessConfig(clictorbase.IafCliConfiguratorBase):

    newlines = 1

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def clear(self):
        self._writeln('3')
        self._to_the_top(self.newlines)

    def import_banner(self, banner_text=None, banner_file=None):
        if banner_text is not None:
            self._writeln('1')
            self._sess.writeln(banner_text)
            self._sess.write("\x04")    # ^D (CTRL-D)
        elif banner_file is not None:
            self._writeln('2')
            self._sess.writeln(banner_file)
        self._to_the_top(self.newlines)

class WelcomeAdminAccessConfig(clictorbase.IafCliConfiguratorBase):

    newlines = 1

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def new(self,message):
        if message is not None:
            self._writeln('NEW')
            self._writeln(message)
            self._sess.write("\x04")
            self._to_the_top(self.newlines)
        else:
            raise ValueError('Welcome message information mandatory for configuring Welcome message')

    def clear(self):
            self._writeln('CLEAR')
            self._to_the_top(self.newlines)


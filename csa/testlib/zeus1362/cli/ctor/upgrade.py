#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/upgrade.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

"""
Command Line Interface (CLI)
command:
    - upgrade
"""

import re
import time
import clictorbase
import string

from StringIO import StringIO
from sal.exceptions import ConfigError, TimeoutError, ExpectError
from clictorbase import NO_DEFAULT, DEFAULT, IafCliError, \
    IafCliParamMap, IafCliConfiguratorBase

from sal.containers.yesnodefault import YES, NO
from sal.deprecated.expect import EXACT, REGEX

class UpgradeError(IafCliError): pass

class upgrade(clictorbase.IafCliConfiguratorBase):

    newlines = 1

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
             ('No available upgrades', EXACT) : UpgradeError,
             ('Failure downloading upgrade list', EXACT): UpgradeError,
             ('machine cannot be upgraded', EXACT) : UpgradeError,
             ('upgrade data interrupted', EXACT) : UpgradeError,
             ('Upgrade failure', EXACT) : UpgradeError,
             ('system upgrade failed', EXACT) : UpgradeError,
             })

    def __call__(self, version=None, seconds=0, input_dict=None, **kwargs):
        # save current version for possible in-place upgrade
        import version as vsn
        self.current_version = vsn.version(self._sess)().version
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        return self

    _get_build_string = lambda self, version: \
         '%s build %s upgrade For Management' % tuple(version.split('-'))
    _get_password =  lambda self, pwd: \
         '%s passwords' % pwd

    def _skip_long_output(self,
                            timeout=30,
                            filter_buffer=True,
                            bytes=500):

        # Bypass expect module methods because expect is too slow
        # for the amount of text the upgrade produces. This has the
        # added disadvantage of not catching errors from the error
        # dictionary, but I think the time savings is worth the hack.
        self._debug('_skip_long_output started')
        output = StringIO()
        while 1:
            try:
                # Read until timeout, which will happen at sub-prompt
                output.write(self._sess.read(1, timeout=timeout))
            except TimeoutError:
                break

        self._debug('_skip_long_output got timeout for read')
        buf = output.getvalue()

        if filter_buffer:
            buf = filter(lambda x: x in string.printable and x != '\r', buf)

        return buf[-bytes:]

    def _check_buffer_for_error_messages(self, buf):
        for match_tuple, exception in self._local_err_dict.iteritems():
            (patt, mtype) = match_tuple
            (so, cb) = self._sess._get_re(patt, mtype)
            mo = so.search(buf)
            if mo:
                raise exception, '\n--- buffer ---\n%s\n---' % (buf,)

    def _check_for_reboot(self):
        try:
            self._query(timeout=10)
        except ExpectError:
            pass

        else:
            self._warn('Reboot was expected, but we got command prompt')
            return False
        return True

    def downloadinstall(self, version=None, seconds=5, input_dict=None, **kwargs):
        """ perform an upgrade downloadinstall subcommand.
            version: version to upgrade zeus to.
                     should be in format N.X.Y-ZZZ (i.e., 8.1.0-400)
                     if unspecified do an upgrade-in-place
            seconds: # of seconds to close connections before reboot

            input_dict:
                - `save_cfg`: specify 'yes' to save current configuration to the
                configuration directory before upgrading, or 'no' if you don't want to
                save it.
                - `include_pw`: specify 'yes' if you want to include passwords in
                configuration file, or 'no' if you don't. Please be aware that a
                configuration without passwords will fail when reloaded with loadconfig.
                - `email`: specify 'yes' if you want saved configuration to be sent by
                email to you or 'no' if you don't.
                - `email_addr`: email address configuration to be sent to. Multiple
                email addresses separated by commas are allowed.

        """

        inputs = input_dict or kwargs
        inputs['build'] = self._get_build_string(version or self.current_version)
        inputs['pw'] = self._get_password(pwd="Encrypt")
        process_question = re.compile('proceed\s*with\s*the\s*upgrade\?')
        param_map = IafCliParamMap(end_of_command=process_question)
        param_map['build'] = ['Upgrades available.', DEFAULT, 1]
        param_map['save_cfg'] = ['save the current configuration', DEFAULT]
        param_map['email'] = ['email the current configuration', DEFAULT]
        param_map['include_pw'] = ['include passwords', DEFAULT]
        param_map['email_addr'] = ['Enter email addresses', DEFAULT]
        param_map['delete_img'] = ['Do you want to delete the image', YES]
        param_map['cancel'] = ['Do you want to cancel the download', YES]
        param_map['pw'] = ['Choose the password option:', DEFAULT,1]

        param_map.update(inputs)

        self.clearbuf()
        self._query_response('DOWNLOADINSTALL')
        self._process_input(param_map, do_restart=False, timeout=180)
        self._debug('answering yes for "proceed with the upgrade?"');
        self._query_response(YES)

        while 1:
            index = self._query(process_question, 'Downloading', timeout=150)
            if index == 0:
                self._debug('answering yes')
                self._query_response(YES)
            else:
                break

        self._debug('\nUpgrade package downloading and installing...\n')
        upgrade_output_tail = self._skip_long_output()

        self._debug('Upgrade output tail\n%s\n---' % (upgrade_output_tail,))

        # need to check the tail for errors
        # because error patterns does not work here
        self._check_buffer_for_error_messages(upgrade_output_tail)
        question = 'Enter the number of seconds to wait'

        if not question in upgrade_output_tail:
            self._read_until(question, timeout=600)

        self._writeln(str(seconds))
        time.sleep(int(seconds))
        self._check_for_reboot()

        # sma reboot initiated
        try:
            self._restart()
        except:
            self._sess = None

    def download(self, version=None, input_dict=None, **kwargs):
        """ perform an upgrade download.
            version: version to upgrade zeus to.
                     should be in format N.X.Y-ZZZ (i.e., 8.1.0-400)
                     if unspecified do an upgrade-in-place
            input_dict:
                - `delete`: specify 'yes' to delete previously downloaded image
                            or 'no' if you don't want to delete it.
        """

        clictorbase.set_ignore_unanswered_questions(ignore=True)

        inputs = input_dict or kwargs

        inputs['build'] = self._get_build_string(version or self.current_version)
        param_map = IafCliParamMap(end_of_command='Choose the operation you want to perform:')
        param_map['build'] = ['Upgrades available', DEFAULT, 1]
        param_map['cancel'] = ['Do you want to cancel the download', DEFAULT]
        param_map['delete'] = ['Do you want to delete the image', DEFAULT]


        param_map.update(inputs)
        self.clearbuf()
        self._query_response('DOWNLOAD')

        try:
            self._process_input(param_map, do_restart=False, timeout=180)
        except UpgradeError:
            self._restart_nosave()
            raise

        # go to top-level command
        self._to_the_top(self.newlines)

    def canceldownload(self, input_dict=None, **kwargs):
        """ cancel current download"""
        self._query_response('CANCELDOWNLOAD')
        inputs = input_dict or kwargs

        param_map = IafCliParamMap()
        param_map['cancel'] = ['Do you want to cancel', DEFAULT]
        param_map.update(inputs)
        self._process_input(param_map)
        self._to_the_top(self.newlines)

    def delete(self, input_dict=None, **kwargs):
        """delete downloaded image"""

        self._query_response('DELETE')
        inputs = input_dict or kwargs

        param_map = IafCliParamMap()
        param_map['delete'] = ['Do you really want to delete it', DEFAULT]
        param_map.update(inputs)
        self._process_input(param_map)
        self._to_the_top(self.newlines)

    def downloadstatus(self):

        """ Show download status.
            return integer - percentage of the download.
                            100 returns in case if image is fully downloaded.

        """

        # in case if image is downloaded already and there is
        # the following option in command prompt :
        # DELETE - Delete downloaded image

        cmd = 'DOWNLOADSTATUS'
        buf = self._read_until(self._sub_prompt_user_match)
        if buf.find("DELETE") != -1:
            # download finished
            self._to_the_top(self.newlines)
            return 100

        if buf.find(cmd) == -1:
            self._to_the_top(self.newlines)
            raise IafCliError, '%s operation not available' % (cmd,)

        self._writeln(cmd)
        status_lines = self._read_until('Choose the operation you want to perform')
        resp_patt = r'(\d+|is complete)'
        response = re.findall(resp_patt, status_lines)
        percent_complete = 0

        if response[-1].isdigit():
            percent_complete = int(response[-1])
        elif response[-1] == 'is complete':
            percent_complete = 100
        else:
            raise AssertionError('Cannot parse %s command output:\n%s' % \
                (cmd, response))

        # go to top-level command
        self._to_the_top(self.newlines)
        return percent_complete

    def install(self, seconds=5, input_dict=None, **kwargs):
        """ perform an upgrade install of already downloaded image.
            seconds: # of seconds to close connections before reboot

            input_dict:
                - `save_cfg`: specify 'yes' to save current configuration to the
                configuration directory before upgrading, or 'no' if you don't want to
                save it.
                - `include_pw`: specify 'yes' if you want to include passwords in
                configuration file, or 'no' if you don't. Please be aware that a
                configuration without passwords will fail when reloaded with loadconfig.
                - `email`: specify 'yes' if you want saved configuration to be sent by
                email to you or 'no' if you don't.
                - `email_addr`: email address configuration to be sent to. Multiple
                email addresses separated by commas are allowed.
        """

        inputs = input_dict or kwargs

        param_map = IafCliParamMap(end_of_command='Preserving configuration')
        param_map['qstn_install'] = ['Do you want to install it', YES]
        param_map['save_cfg'] = ['save the current configuration', DEFAULT]
        param_map['email'] = ['email the current configuration', DEFAULT]
        param_map['include_pw'] = ['include passwords', DEFAULT]
        param_map['email_addr'] = ['Enter email addresses', DEFAULT]
        param_map['confirm'] = ['proceed with the upgrade?', YES]
        param_map['pw'] = ['Choose the password option:', DEFAULT,1]
        param_map.update(inputs)

        self.clearbuf()
        self._query_response('INSTALL')
        self._process_input(param_map, do_restart=False, timeout=180)

        self._debug('\nUpgrade package downloading and installing...\n')
        result = self._read_until('Upgrade complete', timeout=600)
        self._debug(result)

        self._query('Enter the number of seconds to wait')
        self._query_response(str(seconds))

        time.sleep(int(seconds))
        self._check_for_reboot()

        # sma reboot initiated
        try:
            self._restart()
        except:
            self._sess = None

if __name__ == '__main__':

    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one

    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    import clear
    clr = clear.clear(cli_sess)
    clr()
    up = upgrade(cli_sess)
    up_init = up()
    up_init.download(version="8.1.0-400", delete='yes')
    up_init.downloadstatus()
    up_init.canceldownload(cancel=True)
    up_init.downloadinstall(version="8.1.0-400", seconds=5)

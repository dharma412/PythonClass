# !/usr/bin/env python/
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/upgrade.py#1 $

"""
Command Line Interface (CLI)

command:
    - upgrade
"""
import re
import time
import clictorbase
from sal.exceptions import ConfigError
from sal.exceptions import TimeoutError
from sal.exceptions import ExpectError
from sal.containers.yesnodefault import YES, NO

from clictorbase import NO_DEFAULT, DEFAULT, IafCliError, \
    IafCliParamMap, IafCliConfiguratorBase

from sal.deprecated.expect import EXACT, REGEX


class UpgradeError(IafCliError): pass


class InvalidVersionError(IafCliError): pass


class upgrade(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('No available upgrades', EXACT): UpgradeError,
            ('Failure downloading upgrade list', EXACT): UpgradeError,
            ('machine cannot be upgraded', EXACT): UpgradeError,
            ('upgrade data interrupted', EXACT): UpgradeError,
            ('Upgrade failure', EXACT): UpgradeError
        })

    def __call__(self, version=None, seconds=5, proceed_upgrade=YES, input_dict=None, **kwargs):
        self._writeln('upgrade')

        if version is not None:
            self.downloadinstall(version, seconds, proceed_upgrade, input_dict, **kwargs)
        else:
            return self

    _get_build_string = lambda self, version: \
        '%s build %s upgrade For Email' % tuple(version.split('-'))

    BUILD_SEARCH_PATT = re.compile("(\d)\.(\d)", re.M)
    _get_major_build_number = lambda self, version: \
        int(''.join(self.BUILD_SEARCH_PATT.search(version).groups()))

    def downloadinstall(self, version=None, seconds=5, proceed_upgrade=YES, input_dict=None, **kwargs):
        """ perform an upgrade downloadinstall subcommand.
            version: version to upgrade phoebe to.
                     should be in format N.X.Y-ZZZ (i.e., 8.0.0-611)
                     if unspecified do an upgrade-in-place
            seconds: # of seconds to close connections before reboot
            proceed_upgrade: proceed with upgrade or not, takes YES or NO value
            input_dict:
                - `save_cfg`: specify 'yes' to save current configuration to the
                configuration directory before upgrading, or 'no' if you don't want to
                save it.
                - `save_pw`: specify 'yes' if you want to include passwords in
                configuration file, or 'no' if you don't. Please be aware that a
                configuration without passwords will fail when reloaded with loadconfig.
                - `email_cfg`: specify 'yes' if you want saved configuration to be sent by
                email to you or 'no' if you don't.
                - `email_addr`: email address configuration to be sent to. Multiple
                email addresses separated by commas are allowed.
        """

        inputs = input_dict or kwargs
        # Setting version and build string
        # if version isn't specified, grab the version from the phoebe
        # and do an upgrade in place to the same version #
        if not version:
            import cli.ctor.version as vsn
            version = vsn.version(self._sess)().version
        inputs['build'] = self._get_build_string(version)

        self.clearbuf()
        try:
            self._read_until('Are you sure you want to proceed with upgrade', 300)
            self._query_response(proceed_upgrade)
        except TimeoutError:
            raise TimeoutError("System Analysis data not available within 5"
                               " minutes. Please cross check manually to confirm this.")

        param_map = IafCliParamMap(end_of_command='upgrade may require a reboot')
        param_map['build'] = ['Upgrades available.', DEFAULT, 1]
        param_map['save_cfg'] = ['save the current configuration', DEFAULT]
        param_map['email_cfg'] = ['email the current configuration', DEFAULT]
        param_map['save_pw'] = ['the password option', 2]
        param_map['continue'] = ['Do you wish to proceed', YES]
        param_map['email_addr'] = ['Enter email addresses', DEFAULT]
        param_map['delete_img'] = ['Do you want to delete the image', DEFAULT]
        param_map.update(inputs)

        self._query_response('DOWNLOADINSTALL')
        self._process_input(param_map, do_restart=False, timeout=60)
        self._query_response(YES)

        print '\n\n**DEBUG** Upgrade package download started ...\n'
        output = self.getbuf()
        while 1:
            self.clearbuf()
            try:
                self._query('Cisco IronPort Email Security Appliance')
                print '\n\nUpgrade package download completed ...\n\n'
                output += self.getbuf()
                break
            except Exception as e:
                block = self.getbuf()
                output += block
                if block.endswith('failed') or block.endswith('done.'):
                    print 'Upgrade package download is in progress ...\n'
                    continue
                if 'upgrade could not proceed' in block.lower():
                    print '~~~~~~~~~~~~~~~~~~~Upgrade could not proceed~~~~~~~~~~~~~~~~~~~'
                    print '**ERROR** Failure during upgrade'
                    print output
                    self._to_the_top(1)
                    return output
                print '=============================================================='
                print block
                print '=============================================================='

        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print self.getbuf()
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        while 1:
            self.clearbuf()
            try:
                self._query('Enter the number of seconds to wait before forcibly closing connections')
                self._query_response(seconds)
                output += self.getbuf()
                break
            except TimeoutError:
                block = self.getbuf()
                output += block
                if block.endswith('done.'):
                    continue

        self.clearbuf()
        time.sleep(int(seconds) + 1)
        self._query('Rebooting the system...')
        output += self.getbuf()

        # mga reboot initiated
        try:
            self._restart()
        except Exception as e:
            print e
            self._sess = None
        return output

    def download(self, version=None, proceed_upgrade=YES, input_dict=None, **kwargs):
        """ perform an upgrade download.
            version: version to upgrade phoebe to.
                     should be in format N.X.Y-ZZZ (i.e., 4.7.0-142)
                     if unspecified do an upgrade-in-place
            proceed_upgrade: proceed with upgrade or not, takes YES or NO value
            input_dict:
                - `delete`: specify 'yes' to delete previously downloaded image
                            or 'no' if you don't want to delete it.
        """
        clictorbase.set_ignore_unanswered_questions(ignore=True)

        inputs = input_dict or kwargs
        # Setting version and build string
        # if version isn't specified, grab the version from the phoebe
        # and do an upgrade in place to the same version #
        if not version:
            import cli.ctor.version as vsn
            version = vsn.version(self._sess)().version

        inputs['build'] = self._get_build_string(version)
        try:
            output = self._read_until('Are you sure you want to proceed with upgrade', 300)
        except TimeoutError:
            raise TimeoutError, "System Analysis data not available within 5 minutes." \
                                "Please cross check manually to confirm this."
        self._query_response(proceed_upgrade)

        param_map = IafCliParamMap(end_of_command='Choose the operation you want to perform')

        param_map['build'] = ['Upgrades available', DEFAULT, 1]
        param_map['cancel'] = ['Do you want to cancel the download', NO]
        param_map['delete'] = ['Do you want to delete the image', YES]

        param_map.update(inputs)

        self._query_response('DOWNLOAD')
        self._process_input(param_map, do_restart=False, timeout=60)

        self._restart_nosave()  # go to top-level command
        return output

    def canceldownload(self, cancel=True):
        """ Cancel download.
            cancel: answer the question if you want to cancel
                    current download. Can be True or False
        """
        self.clearbuf()
        self._query_response('CANCELDOWNLOAD')

        if cancel:
            param_map = IafCliParamMap(end_of_command='Download cancel')
            param_map['cancel'] = ['Do you want to cancel', DEFAULT]
        else:
            param_map = IafCliParamMap(end_of_command='Choose the operation you want to perform')
            param_map['cancel'] = ['Do you want to cancel', NO]

        self._process_input(param_map, do_restart=False, timeout=60)
        self._restart_nosave()  # go to top-level command

    def delete(self, delete=True):
        """ Delete downloaded image in case if it is
            downloaded already with DOWNLOAD command.
            delete: True or False - to delete image or not
        """
        self.clearbuf()
        self._query_response('DELETE')

        if delete:
            param_map = IafCliParamMap(end_of_command='Download image deleted')
            param_map['delete'] = ['Do you really want to delete it', DEFAULT]
        else:
            param_map = IafCliParamMap(end_of_command='Choose the operation you want to perform')
            param_map['delete'] = ['Do you really want to delete it', NO]

        self._process_input(param_map, do_restart=False, timeout=60)
        self._restart_nosave()

    def downloadstatus(self):
        """ Show download status.
            return integer - percentage of the download.
                            100 returns in case if image is fully downloaded.
        """

        # in case if image is downloaded already and there is
        # the following option in command prompt :
        # DELETE - Delete downloaded image
        buf = self._sess.getbuf(clear_buf=True)
        if buf.find("Delete downloaded image") != -1:
            percent_complete = 100
            self._restart_nosave()
            return percent_complete

        self._query_response('DOWNLOADSTATUS')

        status_lines = self._read_until('Choose the operation you want to perform')
        resp_patt = r'(\d+|is complete)'
        response = re.findall(resp_patt, status_lines)

        percent_complete = 0
        if response[-1].isdigit():
            percent_complete = int(response[-1])
        elif response[-1] == 'is complete':
            percent_complete = 100
        else:
            raise AssertionError('DOWNLOADSTATUS command failed ' \
                                 'due to unexpected output:\n%s' % response)

        self._restart_nosave()  # go to top-level command
        return percent_complete

    def install(self, seconds=5, proceed_upgrade=YES, input_dict=None, **kwargs):
        """ perform an upgrade install of already downloaded image.
            seconds: # of seconds to close connections before reboot
            proceed_upgrade: proceed with upgrade or not, takes YES or NO value
            input_dict:
                - `save_cfg`: specify 'yes' to save current configuration to the
                configuration directory before upgrading, or 'no' if you don't want to
                save it.
                - `save_pw`: specify 'yes' if you want to include passwords in
                configuration file, or 'no' if you don't. Please be aware that a
                configuration without passwords will fail when reloaded with loadconfig.
                - `email_cfg`: specify 'yes' if you want saved configuration to be sent by
                email to you or 'no' if you don't.
                - `email_addr`: email address configuration to be sent to. Multiple
                email addresses separated by commas are allowed.
        """

        inputs = input_dict or kwargs
        try:
            output = self._read_until('Are you sure you want to proceed with upgrade', 300)
        except TimeoutError:
            raise TimeoutError, "System Analysis data not available within 5 minutes." \
                                "Please cross check manually to confirm this."
        self._query_response(proceed_upgrade)

        param_map = IafCliParamMap(end_of_command='upgrade may require a reboot')

        param_map['qstn_install'] = ['Do you want to install it', DEFAULT]
        param_map['save_cfg'] = ['save the current configuration', DEFAULT]
        param_map['email_cfg'] = ['email the current configuration', DEFAULT]
        param_map['save_pw'] = ['include passphrases', DEFAULT]
        param_map['email_addr'] = ['Enter email addresses', DEFAULT]

        param_map.update(inputs)

        self.clearbuf()
        self._query_response('INSTALL')

        major_build_number = self._get_major_build_number(self.getbuf())

        self._process_input(param_map, do_restart=False, timeout=60)

        ques_text = "Warning: After upgrading to AsyncOS"
        upgrade_text = "Finding partitions"

        # Answering the question below :
        # Performing an upgrade may require a reboot of the system after the upgrade is applied.
        # You may log in again after this is done. Do you wish to proceed with the upgrade? [Y]
        self._query_response(YES)

        if major_build_number == 65:
            # Warning: After upgrading to AsyncOS 6.5.x, it will not be possible
            # to revert to a previous version. Do you wish to proceed with the upgrade?
            index = self._query(ques_text, upgrade_text)
            if index == 0:
                self._query_response(YES)

        print '\nUpgrade package downloading and installing...\n'

        # Bypass expect module methods because expect is too slow
        # for the amount of text the upgrade produces. This has the
        # added disadvantage of not catching errors from the error
        # dictionary, but I think the time savings is worth the hack.

        while 1:
            try:
                # Read until timeout, which will happen at sub-prompt
                self._sess.read(128, timeout=90)
            except TimeoutError:
                break

        # seconds to wait before closing connections
        try:
            self._query_response(str(seconds))
        except TimeoutError:
            # Only error out if we timeout and are not at a subprompt
            self._restart()
            raise ConfigError, "Installation could not be executed. Please check " \
                               "debug log for details."
        except ExpectError:
            buf = self.getbuf()
            if not (buf.find('Rebooting the system...') != -1):
                raise ConfigError, "Installation could not be executed."

        time.sleep(int(seconds) + 1)

        # mga reboot initiated
        try:
            self._restart()
        except:
            self._sess = None
        return output


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
    up_init.download(version="8.0.0-390", delete='yes')
    up_init.downloadstatus()
    up_init.canceldownload(cancel=True)
    # up_init.delete()
    up_init.downloadinstall(version="8.0.0-382", seconds=5)

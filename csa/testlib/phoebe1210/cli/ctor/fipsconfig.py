#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/fipsconfig.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from sal.exceptions import ConfigError, TimeoutError, ExpectError

from clictorbase import IafCliConfiguratorBase, IafUnknownOptionError
from common.util.systools import SysTools


class fipsconfig(IafCliConfiguratorBase):
    """
    cli->fipsconfig - Change FIPS configuration.
    """

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._restart()
        self._writeln('fipsconfig')
        self._is_fips_enabled = self._get_status()
        return self

    def _get_status(self):
        fips_status = self._read_until(self._sub_prompt_user_match,
                                       timeout=10)
        return ('currently enabled' in fips_status.lower())

    def _change_mode(self, dut, dut_version, action, always_encrypt, log_msg, timeout):
        self._writeln('SETUP')
        self._log(log_msg)
        SECONDS_TO_WAIT = 30
        try:
            self._query_response('Y')
            if action == 'enable':
                self._query_response(always_encrypt)
            self._query_response(str(SECONDS_TO_WAIT))
        except (TimeoutError, IafUnknownOptionError):
            # Only error out if we timeout and are not at a subprompt
            buf = self.getbuf()
            if buf.find('non-FIPS-compliant objects configured') >= 1:
                raise ConfigError \
                    ('There are FIPS non-compliant objects currently configured. More info: %s' % buf)
            self._restart()
            raise ConfigError('FIPS mode could not be changed.')
        except ExpectError:
            buf = self.getbuf()
            if buf.find('Rebooting the system...') == -1:
                raise ConfigError('FIPS mode could not be changed.')

        SysTools(dut, dut_version).wait_until_dut_reboots(timeout, wait_for_ports="22,80")

    def is_enabled(self):
        result = self._is_fips_enabled
        self._to_the_top(1)
        return result

    def enable(self, dut, dut_version, action, always_encrypt='yes', timeout=900):
        res = self._is_fips_enabled
        if res:
            self._to_the_top(1)
        else:
            self._change_mode(dut, dut_version, action, always_encrypt,
                              'Enabling FIPS and going for a reboot',
                              timeout)
        return res

    def disable(self, dut, dut_version, action, always_encrypt, timeout=900):
        res = self._is_fips_enabled
        if res:
            self._change_mode(dut, dut_version, action, always_encrypt,
                              'Disabling FIPS and going for a reboot',
                              timeout)
        else:
            self._to_the_top(1)
        return res

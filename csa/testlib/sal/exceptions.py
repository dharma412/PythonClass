#!/usr/bin/env python
""" Customized exceptions."""
from __future__ import absolute_import


#: Reference Symbols: SAPIError, CheckLogsError, ConfigError, TimeoutError
#: Reference Symbols: PythonVersionError, DutNotRespondingError, ExpectError

class SAPIError(Exception): pass


class CheckLogsError(SAPIError): pass


class ConfigError(Exception): pass


class TimeoutError(Exception): pass


class PythonVersionError(Exception): pass


class DutNotRespondingError(Exception):
    E1 = 'NOT_PINGABLE'
    E2 = 'SSH_NOT_OPEN'

    def __init__(self, host, error):
        self.host = host
        self.error = error

    def __str__(self):
        str_dict = {
            self.E1: "Not Pingable",
            self.E2: "SSH Not Open"
        }
        return "%s: %s" % (self.host, str_dict[self.error])


class ExpectError(Exception):
    pass


class BadEnvironment(Exception): pass


class InstallationFailed(Exception): pass


class HostDown(Exception): pass


class PackageHostError(Exception): pass


class SudoFailure(Exception): pass


class WGATestToolException(Exception):
    """ WGATestToolException is used for client side functional errors."""
    pass


class WGATestToolError(Exception): pass

class CalledProcessErrorStderr(Exception):
    """ CalledProcessErrorStderr for handling with stderr
    """
    def __init__(self, ret_code, result_cmd, stderr=None):
        self.ret_code = ret_code
        self.result_cmd = result_cmd
        self.stderr = stderr

    def __str__(self):
        if self.stderr:
            return 'CalledProcessErrorStderr:%s Commmand:%s Stderr:%s"' % (self.ret_code, self.result_cmd, self.stderr)
        else:
            return 'CalledProcessErrorStderr:%s Commmand:%s' % (self.ret_code, self.result_cmd)

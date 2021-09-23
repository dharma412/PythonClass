#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/outbreakconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
SARF CLI command: outbreakconfig
"""

import clictorbase
from clictorbase import DEFAULT, IafCliError, \
    IafCliParamMap, IafCliConfiguratorBase

from sal.containers.yesnodefault import YES, NO
from sal.deprecated.expect import EXACT

DEBUG = True


class outbreakconfig(clictorbase.IafCliConfiguratorBase):
    class RequireActivationError(IafCliError):
        pass

    class LicenseAgreementError(IafCliError):
        pass

    class InvalidArgumentError(IafCliError):
        pass

    def __init__(self, sess):
        # use the correct scoping for IafCliConfiguratorBase
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('requires activation with a software key',
             EXACT): self.RequireActivationError,
            ('interactive mode and accept the license agreement ',
             EXACT): self.LicenseAgreementError,
            ('Invalid arguments when processing outbreakconfig ',
             EXACT): self.InvalidArgumentError
        })

    def __call__(self, option=None):
        if option == None:
            self._writeln(self.__class__.__name__)
            return self
        else:
            arg = option.lower().split(' ')
            assert arg[0] in \
                   ('enable', 'tag-only', 'timeout', \
                    'disable', 'rescan', 'threshold', 'alerts')
            if arg[0] == 'timeout' and len(arg) == 2:
                assert int(arg[1]) >= 1 and int(arg[1]) <= 120
            if arg[0] == 'rescan' and len(arg) == 2:
                assert arg[1] in ('on', 'off')
            if arg[0] == 'tag-only' and len(arg) == 2:
                assert arg[1] in ('on', 'off')
            if arg[0] == 'threshold':
                assert arg[1] in ('1', '2', '3', '4', '5')
            if arg[0] == 'rescan' and len(arg) == 2:
                assert arg[1] in ('on', 'off')
            if arg[0] == 'alerts':
                assert arg[1] in ('enable', 'disable')
            self._writeln(self.__class__.__name__ + ' ' + str(option))
            return self._wait_for_prompt()

    def setup(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['use'] = \
            ['Would you like to use Outbreak Filters', DEFAULT]
        param_map['disable'] = \
            ['Are you sure you want to disable', DEFAULT]
        param_map['alerts'] = \
            ['receive Outbreak Filter alerts', DEFAULT]
        param_map['max_message_size'] = ['largest size message', DEFAULT]
        param_map['use_heuristics'] = ['use adaptive rules', DEFAULT]
        param_map['log_urls'] = ['logging of URL', DEFAULT]
        param_map['enable_urlclick_tracking'] = ['enable Web Interaction Tracking', DEFAULT]
        param_map['disable_urlclick_tracking'] = ['disable Web Interaction Tracking', DEFAULT]
        param_map['agreement'] = \
            ['Do you accept the above license agreement', YES]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)

    def proxyconfig(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['proxy_template'] = \
            ['Outbreak Filters proxy template', DEFAULT]
        param_map['proxy_key'] = \
            ['Outbreak Filters proxy key', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('proxyconfig')
        return self._process_input(param_map)


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = outbreakconfig(cli_sess)
    cli().setup()
    cli().setup(max_message_size='100000', alerts=NO, use_heuristics=NO)
    cli().setup(use=NO, disable=YES)
    print cli('enable')
    print cli('disable')
    print cli('timeout')
    print cli('timeout 80')
    print cli('rescan off')
    print cli('rescan')
    print cli('rescan on')
    print cli('threshold 3')
    print cli('tag-only')
    print cli('alerts enable')
    print cli('alerts disable')

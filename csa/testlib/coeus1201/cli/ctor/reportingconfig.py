#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/reportingconfig.py#1 $

"""
    IAF 2 CLI ctor - reportingconfig
"""

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, \
                IafCliError, IafUnknownOptionError, REQUIRED, DEFAULT
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO

DEBUG = True

class reportingconfig(clictorbase.IafCliConfiguratorBase):
    """reportingconfig
        - configure reporting system
    """

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self.newlines = 1

    def __call__(self):
        self._writeln('reportingconfig')
        return self

    def counters(self, level=''):
        self._query_response('COUNTERS')
        self._query_select_list_item(level)
        self._to_the_top(self.newlines)

    def averageobjectsize(self, size=''):
        self._query_response('AVERAGEOBJECTSIZE')
        self._query_response(size)
        self._to_the_top(self.newlines)

    def webeventbucketing(self):
        self._query_response('WEBEVENTBUCKETING')
        return webeventbucketingConfig(self._get_sess())

    def centralized(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command =
                                                       'Choose the operation')
        param_map['enable']     = ['to enable Centralized Reporting', DEFAULT]
        param_map['anonymize']  = ['anonymize usernames in reports', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('CENTRALIZED')
        return self._process_input(param_map)

class webeventbucketingConfig(clictorbase.IafCliConfiguratorBase):
    """reportingconfig -> WEBEVENTBUCKETING """
    newlines = 2

    def enable(self):
        self._query_response('ENABLE')
        self._to_the_top(self.newlines)

    def disable(self):
        self._query_response('DISABLE')
        self._to_the_top(self.newlines)

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    rc = reportingconfig(cli_sess)
                              
    rc().counters(level='Unlimited')
    rc().counters(level='Minimally')
    rc().counters(level='Moderately')

    rc().averageobjectsize(size='15000')

    rc().webeventbucketing().disable()
    rc().webeventbucketing().enable()

    rc().centralized()
    rc().centralized(enable=YES, anonymize=YES)
    rc().centralized(enable=NO, anonymize=NO)

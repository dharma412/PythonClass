# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/domainrepconfig.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from clictorbase import DEFAULT, IafCliConfiguratorBase


class domainrepconfig(IafCliConfiguratorBase):
    def __call__(self, **kwargs):
        self._sess.writeln('domainrepconfig')
        return self

    def enable(self, **kwargs):
        self.clearbuf()
        self._query_response('Y')
        if kwargs.has_key('domain_exception_list'):
            self._query_select_list_item(kwargs['domain_exception_list'])
        else:
            self._query_response(DEFAULT)
        self._to_the_top(1)
        self._debug(self.getbuf())

    def disable(self):
        self._query_response('N')

    def batch(self, domain_exception_list):
        if not domain_exception_list:
            raise ValueError('Required parameter "domain_exception_list"'
                             ' was not passed')

        cmd = 'domainrepconfig domainexceptionlist %s' % domain_exception_list
        self._info('BATCH COMMAND: %s' % cmd)
        self._to_the_top(1)
        self.clearbuf()
        self._writeln(cmd)
        self._wait_for_prompt()
        self._info(self.getbuf())

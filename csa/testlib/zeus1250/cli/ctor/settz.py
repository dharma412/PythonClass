#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/settz.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

import clictorbase
import string
from sal.exceptions import ConfigError

class settz(clictorbase.IafCliConfiguratorBase):

    def __call__(self, continent=None, zone=None, validate=False):
        if continent:
            self._writeln("settz %s %s" % (continent, zone))

            if validate:
                rsp = self._wait_for_prompt()

                if rsp.find('Invalid') >= 0:
                    raise ConfigError, string.strip(rsp)
            else:
                self._restart()

        else:
            self._writeln("settz")
            return self

    def setup(self, continent=None, country=None, zone=None):
        self._query_response('setup')
        self._query_select_list_item(continent)
        self._query_select_list_item(country)
        self._query_select_list_item(zone)
        self._restart()

    def listtimezones(self):
        # return to the CLI prompt
        self._to_the_top(1)
        self._writeln('settz print')
        result = self._read_until('>', timeout=3)
        return result


if __name__ == '__main__':

    stz = settz(clictorbase.get_sess())
    print 'positive test case'

    stz("America","Los_Angeles", True)
    print 'negative test case'

    try:
        stz("America", 99, True)
    except ConfigError, ce:
        print 'Timeout error found, as expected in negative test case'

    stz().setup("America", "United States", "Los_Angeles")
    print 'positive test case'

    try:
        stz().setup("Trial", 2 , "Los_Angeles")
    except ConfigError, ce:
        print "error - %s" % (ce, )

    print 'Settz test done!'


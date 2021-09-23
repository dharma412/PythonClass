# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/beakerconfig.py#1 $
# $DateTime: 2020/01/17 04:04:23 $
# $Author: aminath $

import clictorbase as ccb


class beakerconfig(ccb.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self, server_type):
        self._query_response('SETUP')
        self._query_select_list_item(server_type)
        self._to_the_top(1)

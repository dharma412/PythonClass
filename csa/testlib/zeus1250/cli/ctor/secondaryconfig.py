# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/secondaryconfig.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from sal.containers.yesnodefault import YES, NO, DEFAULT
import clictorbase

REQUIRED = clictorbase.REQUIRED

class secondaryconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def enable(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
            end_of_command='Choose the operation')
        param_map['enable'] = ['secondary aggregation enabled', DEFAULT]
        param_map['source_name'] = ['the data source name to aggregate from', REQUIRED]
        param_map.update(input_dict or kwargs)

        if (param_map['enable'])['answer'] != YES :
            (param_map['source_name'])['must_answer'] = 0

        self._query_response('ENABLE')
        return self._process_input(param_map)
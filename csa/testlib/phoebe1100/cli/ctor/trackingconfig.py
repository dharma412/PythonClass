#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/trackingconfig.py#1 $

import clictorbase

from sal.containers.yesnodefault import NO, YES

DEFAULT = clictorbase.DEFAULT


class trackingconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln('trackingconfig')
        return self

    def setup(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['enable_tracking'] = \
            ['use the Message Tracking Service', DEFAULT]
        param_map['track_rejected_conns'] = \
            ['track rejected connections?', DEFAULT]
        param_map['centralized_tracking'] = \
            ['use Centralized Message Tracking', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)


if __name__ == '__main__':

    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    tc = trackingconfig(cli_sess)

    tc().mode()
    tc().mode(enable_tracking=YES)
    tc().mode(enable_tracking=YES, on_box_tracking='export')
    tc().mode(enable_tracking=YES, track_rejected_conns=YES)
    tc().mode(enable_tracking=YES, track_rejected_conns=YES,
              on_box_tracking='export')

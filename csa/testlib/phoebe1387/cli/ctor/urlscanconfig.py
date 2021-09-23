#!/usr/bin/env python

import clictorbase
from clictorbase import DEFAULT, IafCliParamMap


class urlscanconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self, input_dict=None, **kwargs):
        self._writeln('urlscanconfig')
        param_map = IafCliParamMap(end_of_command=self._get_prompt())

        param_map['enable_attachment_scanning'] = [
            'Would you like to use Default url scanning in attachments', DEFAULT]

        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

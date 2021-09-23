#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/imageanalysisconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import os

import clictorbase as ccb
from clictorbase import REQUIRED, DEFAULT, IafCliError, \
    IafCliConfiguratorBase

from sal.deprecated.expect import REGEX, EXACT
from sal.containers.yesnodefault import YES, NO


class FeaturekeyError(Exception): pass


class imageanalysisconfig(ccb.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('imageanalysisconfig')
        return self

    def __init__(self, sess):

        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('feature requires activation', EXACT): FeaturekeyError,
        })

    def setup(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')

        param_map['use_iia'] = ['Would you like to use IronPort '
                                'Image Analysis?', DEFAULT]
        param_map['license_agreement'] = ['license agreement?', YES]
        param_map['img_sensitivity'] = ['image analysis sensitivity', DEFAULT]
        param_map['img_clean_verd'] = ['range for a CLEAN verdict', DEFAULT]
        param_map['img_suspect_verd'] = ['range for a SUSPECT verdict', DEFAULT]
        param_map['clean_score'] = ['score you wish to consider for '
                                    'a clean message?', DEFAULT]
        param_map['suspect_score'] = ['score you wish to consider for '
                                      'a suspect message?', DEFAULT]
        param_map['confirm_disable'] = ['Are you sure you want to disable?', YES]
        param_map['skip_smaller'] = ['skip scanning of images smaller than a '
                                     'specific size', DEFAULT]
        param_map['min_size'] = ['enter minimum image size to scan in pixels',
                                 DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)

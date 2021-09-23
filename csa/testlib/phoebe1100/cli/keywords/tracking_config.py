#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/tracking_config.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class TrackingConfig(CliKeywordBase):
    """
    trackingconfig:
            Configure tracking system.
    """

    def get_keyword_names(self):
        return ['tracking_config_setup',
                ]

    def tracking_config_setup(self, *args):
        """
        Setup tracking config

        trackingconfig -> setup

        *Parameters*:
        - `enable_tracking`: Would you like to use the Message Tracking Service?
                            Either 'yes' or 'no'
        - `track_rejected_conns`:
                            Would you like to track rejected connections?
                            Either 'yes' or 'no'
        - `centralized_tracking`:
                            use Centralized Message Tracking for this appliance?
                            Either 'yes' or 'no'

        Examples:
        | Tracking Config Setup | enable_tracking=yes | track_rejected_conns=yes |
        | Tracking Config Setup | enable_tracking=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.trackingconfig().setup(**kwargs)

#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/set_time_zone.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class SetTimeZone(CliKeywordBase):
    """
       Provides keywords related to setting time zones
    """

    def get_keyword_names(self):
        return [
            'set_time_zone',
            'set_time_zone_print',
            'set_time_zone_setup',
            'set_time_zone_status',
        ]

    def set_time_zone(self, continent=None, zone=None, validate=False):
        """Set time zone and validate continet and time zone

        *Parameters*:
        - `continent`: The continent such as "America"
        - `zone`: The timezone such as "Los_Angeles"
        - `validate`: True to validate, False to ignore validation

        *Exception*:
        - `ConfigError`: in case invalid continent or zone is tried to setup

        *Example*:
        | Set Time Zone | continent=America | zone=Los_Angeles |
        | ... | validate=${True} |
        """
        self._cli.settz(continent, zone, validate)

    def set_time_zone_setup(self, continent=None, country=None, zone=None):
        """Sets the timezone.

        settz -> setup

        *Parameters*:
        - `continent`: The continent such as "America"
        - `country`: Country such as "United States"
        - `zone`: The timezone such as "Los_Angeles"

        *Exception*:
        - `ConfigError`: in case invalid continent or zone is tried to setup

        *Example*:
        | Set Time Zone Setup | continent=America | country=United States |
        | ... | zone=Los_Angeles |
        """
        self._cli.settz().setup(continent, country, zone)

    def set_time_zone_print(self):
        """
        Displays a list of valid zones

        settz print

        *Parameters*:
            None

        *Example*:
        | Set Time Zone Print |
        """
        output = self._cli.settz().Print()
        self._info(output)
        return output

    def set_time_zone_status(self):
        """
        Get current time zone, time zone version and last update info

        *Parameters*:
            None

        *Return*:
            Dictionary containing the following keys: current_time_zone,
            current_time_zone_version and last_update

        *Example*:
        | ${Status}= | Set Time Zone Status |
        """
        output = self._cli.settz()
        self._info(output.vals)
        return output.vals

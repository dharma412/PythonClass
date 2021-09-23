#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/set_time_zone.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class SetTimeZone(CliKeywordBase):
    """Sets the current timezone."""

    def get_keyword_names(self):
        return [
                'set_time_zone',
                'set_time_zone_print',
                'set_time_zone_setup'
               ]

    def set_time_zone(self, continent=None, zone=None, validate=False):
        """Set time zone and validate continet and time zone

        Parameters:
            - `continent`: The continent such as "America"
            - `zone`: The timezone such as "Los_Angeles"
            - `validate`: True to validate, False to ignore validation

        Example:
        | Set Time Zone | continent=America | zone=Los_Angeles | validate=${True} |

        Exception:
            - `ConfigError`: in case invalid continent or zone is tried to setup
        """
        self._cli.settz(continent, zone, validate)

    def set_time_zone_setup(self, continent=None, country=None, zone=None):
        """Sets the timezone.

        settz > setup

        Parameters:
            - `continent`: The continent such as "America"
            - `country`: Country such as "United States"
            - `zone`: The timezone such as "Los_Angeles"

        Example:
        | Set Time Zone Setup | continent=America | country=United States | zone=Los_Angeles |

        Exception:
            - `ConfigError`: in case invalid continent or zone is tried to setup

        """
        self._cli.settz().setup(continent, country, zone)

    def set_time_zone_print(self):
        """displays a list of valid zones

        settz > print

        Example:
        | Set Time Zone Print |

        """
        output = self._cli.settz().listtimezones()
        self._info(output)
        return output

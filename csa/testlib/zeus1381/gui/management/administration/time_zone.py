#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/management/administration/time_zone.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $


from common.gui.guicommon import GuiCommon

REGION_LOC = 'id=continent'
COUNTRY_LOC = 'id=country'
ZONE_LOC = 'id=time_zone'


class TimeZone(GuiCommon):
    """Keywords for Management -> System Administration -> Time Zone"""

    def get_keyword_names(self):
        return [
                'time_zone_edit'
                ]

    def _open_page(self):
        self._navigate_to('Management', 'System Administration', 'Time Zone')

    def _select_region(self, region):
        regions_list = self.get_list_items(REGION_LOC)

        for item in regions_list:
            if region in item:
                self.select_from_list(REGION_LOC, item)
                self._info('Selected "%s" region' % (item,))
                break
        else:
            raise ValueError('"%s" region does not exist.' % (region,))

    def _select_country(self, country):
        countries_list = self.get_list_items(COUNTRY_LOC)

        for item in countries_list:
            if country in item:
                self.select_from_list(COUNTRY_LOC, item)
                self._info('Selected "%s" country.' % (item,))
                break
        else:
            raise ValueError('"%s" country does not exist' % (country,))

    def _select_zone(self, zone):
        zones_list = self.get_list_items(ZONE_LOC)

        for item in zones_list:
            if zone in item:
                self.select_from_list(ZONE_LOC, item)
                self._info('Selected "%s" time zone.' % (item,))
                break
        else:
            raise ValueError('"%s" time zone does not exist' % (zone,))

    def time_zone_edit(self, region, country, zone):
        """Edit time zone settings.

        Parameters:
            - `region`: name of the region.
            - `country`: name of the country.
            - `zone`: name of the time zone.

        Examples:
        | TimeZone Edit | Europe | United Kingdom | London |
        | TimeZone Edit | America | United States | Pacific Time |

        Exceptions:
            - `ValueError`: in case `region`, `country` or `zone` is not
                            present in corresponding drop-down list.

        """
        self._info('Editing time zone settings.')

        self._open_page()

        self._click_edit_settings_button()

        self._select_region(region)

        self._select_country(country)

        self._select_zone(zone)

        self._click_submit_button()

        self._info('Configured time zone settings.')


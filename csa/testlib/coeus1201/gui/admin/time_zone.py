#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/time_zone.py#1 $

from common.gui.guicommon import GuiCommon

class TimeZone(GuiCommon):
    """Keywords for System Administration -> Time Zone
    """

    def get_keyword_names(self):
        return [
                'time_zone_edit',
               ]

    def _open_page(self):
        """
       Navigate to time zone configuration page.
        """
        self._navigate_to('System Administration', 'Time Zone')

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

    def _select_region(self, region):
        region_loc = 'id=continent'
        regions_list = self.get_list_items(region_loc)

        for item in regions_list:
            if region in item:
                self.select_from_list(region_loc, item)
                self._info('Selected "%s" region' % (item,))
                break
        else:
            raise ValueError, '"%s" region does not exist.' % (region,)

    def _select_country(self, country):
        country_loc = 'id=country'
        countries_list = self.get_list_items(country_loc)

        for item in countries_list:
            if country in item:
                self.select_from_list(country_loc, item)
                self._info('Selected "%s" country.' % (item,))
                break
        else:
            raise ValueError, '"%s" country does not exist' % (country,)

    def _select_zone(self, zone):
        zone_loc = 'id=time_zone'
        zones_list = self.get_list_items(zone_loc)

        for item in zones_list:
            if zone in item:
                self.select_from_list(zone_loc, item)
                self._info('Selected "%s" time zone.' % (item,))
                break
        else:
            raise ValueError, '"%s" time zone does not exist' % (zone,)


#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/reporting/reports_base_zeus82.py#4 $
# $DateTime: 2019/12/12 01:16:18 $
# $Author: sarukakk $

from sma.constants import sma_web_reports
from common.gui.new_reports_base import ReportsBase

class ReportsBaseZeus82(ReportsBase):
    """
    Two report types added in addition to standard:
    SOCKS Proxy and My Report

    Some implementation details are corrected.
    """

    standard_reports_names = list(ReportsBase.standard_reports_names)
    standard_reports_names.append('wsa_socks_proxy')
    standard_reports_names.append('wsa_my_reports')

    TABLE_COLUMNS_LINK_SELECTOR = "//span[contains(@onclick,'showTableOptionsDlg')]"
    SECTION_EXPORT_LINK_SELECTOR = "//span[contains(@onclick,'SectionExport')]"

    def _select_chart_data(self, type, row, type_dict):
        link = "xpath=//table[@class='layout']//tr[%d]//td[2]/a" % (row,)
        if type.lower() == 'none':
            return
        if type not in type_dict.keys():
            raise guiexceptions.ConfigError(
                    "Invalid chart data type '%s'." % (type))

        radio_button_link = "xpath=//input[@id='chart_option_dlg_%s']" % \
                             (type_dict[type])
        self.click_element(link, "don't wait")
        self._click_radio_button(radio_button_link)
        self.click_element("xpath=//div[@id='chart_option_dlg']//button[text()='Save']",
                           "don't wait")

    def _find_section_area(self, section_path, timeout=60):
        old_section_loc = super(ReportsBaseZeus82, self)._find_section_area(section_path, timeout)
        if old_section_loc is None:
            return None
        container_locator = old_section_loc + "//ancestor::div[starts-with(@id,'container_')]"
        count = int(self.get_matching_xpath_count(container_locator))
        new_selector = None
        if count == 0:
            self._warn('Report section container was not found. Falling back to old locator')
            return old_section_loc
        if count > 1:
            self._warn('Found more then one report section container. Choosing the closest one')
        id = self.get_element_attribute("xpath="+container_locator+"[1]@id")
        new_selector = "//*[@id='%s']" % id
        self._debug('Report section selector is %s' % (new_selector,))
        return new_selector


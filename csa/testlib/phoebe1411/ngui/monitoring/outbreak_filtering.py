
from common.ngui.ngguicommon import NGGuiCommon


class OutbreakFiltering(NGGuiCommon):

    def get_keyword_names(self):
        return ['outbreak_filters_scroll_to_bottom']


    def outbreak_filters_scroll_to_bottom(self):
        """This keyword to scroll to the bottom of the outbreak filter table"""

        self.press_keys(OutbreakFilter.scroller, 'PAGE_DOWN')
        self.press_keys(OutbreakFilter.scroller, 'PAGE_DOWN')
        self.press_keys(OutbreakFilter.scroller, 'PAGE_DOWN')
        status = self._is_visible(OutbreakFilter.scroller)
        self._debug("scroll visible status:%s" %status)


class OutbreakFilter:
    scroller = "//*[@class='reporting__body ng-scope esa__reporting__body']"

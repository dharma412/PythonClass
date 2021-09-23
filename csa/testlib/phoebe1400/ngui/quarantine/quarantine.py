from common.gui.decorators import visit_page
from common.ngui.exceptions import UserInputError
from common.ngui.ngguicommon import NGGuiCommon

class QuarantineSearch:
    quarantine_header_xpath = "//a[@translate='header.message_quarantine']"
    quarantine_url_path = 'quarantine/search'
    side_bar = "//*[@id='sidebar-menu-icon']"
    quarantine_sidebar_options = {'Search':  "//span[@title='Search' and @class='ng-scope subItems']",
                                  'Other Quarantine': "//span[@title='Other Quarantine' and @class='ng-scope subItems']",
                                  }

class quarantine(NGGuiCommon):

    def get_keyword_names(self):
        return ['go_to_quarantine', 'open_sidebar_menu', 'go_to_quarantine_nowait']

    @visit_page(QuarantineSearch.quarantine_header_xpath, QuarantineSearch.quarantine_url_path)
    def go_to_quarantine(self):
        """
        This keyword to navigate to the Quarantine page
        :return:
        """
        self._info('Navigated to Quarantine page')

    @visit_page(QuarantineSearch.quarantine_header_xpath, QuarantineSearch.quarantine_url_path, wait=False)
    def go_to_quarantine_nowait(self):
        self._info('Navigated to Quarantine page with nowait')

    def open_sidebar_menu(self, menu):
        """
        This keyword to open the side bar menu and select menu options
        :param menu:
        :return:
        """
        self.click_element(QuarantineSearch.side_bar)
        self.wait_for_angular()
        if QuarantineSearch.quarantine_sidebar_options.has_key(menu):
            self._wait_until_element_is_present(QuarantineSearch.quarantine_sidebar_options[menu], timeout=10)
            self.click_element(QuarantineSearch.quarantine_sidebar_options[menu])
            self.wait_for_angular()
        else:
            raise UserInputError('Invalid user option')

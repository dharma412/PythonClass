
from common.gui.guicommon import GuiCommon
from common.gui.guiexceptions import GuiValueError

class EolInfo:

    eolbanner = "//*[@id='eol']"
    eollink = "//*[@id='eol']/div/a[%s]"

class EolNotification(GuiCommon):
    """Keywords for EOL NOTIFICATION on ESA GUI PAGE """

    def get_keyword_names(self):
        return ['eol_notification_is_visible',
                'eol_notification_get_content',
                'eol_notification_navigate_link']

    def eol_notification_is_visible(self):
        """
        This keyword will return status of eol notification is visible or not
        :return: True|False
        """
        return self._is_visible(EolInfo.eolbanner)

    def eol_notification_get_content(self):
        """
        This keyword will return the content of eol notification banner
        :return: notification content
        """
        return self.get_text(EolInfo.eolbanner)

    def _verify_eol_window_title(self, title):
        if title in self.get_title():
            self._debug("CURRENT TITLE :%s" % self.get_title())
        else:
            raise GuiValueError('New window title not matched')

    def eol_notification_navigate_link(self, link=None, title=''):
        """
        This keyword will navigate the link and verify the title of window navigated

        :arg link: upgrade|info
        :arg title : tile to verify on the new window tab
        :return:
        """

        link_dict = {'upgrade': 1, 'info': 2}
        if link not in link_dict:
            raise GuiValueError('Invalid link option used..')

        self.click_link(EolInfo.eollink %link_dict[link])
        if link == 'info':
            self.select_window('NEW')
            self._verify_eol_window_title(title)
            self.select_window('MAIN')
        else:
            self._verify_eol_window_title(title)

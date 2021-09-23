from common.gui.guicommon import GuiCommon
from common.gui.guiexceptions import ConfigError, GuiValueError

ENABLE_BUTTON = "//input[@value='Enable']"
ENABLE_CHECKBOX= "//input[@id='enable_csa_checkbox']"
CSA_SERVER = "//select[@name='reg_server_region']"
CSA_TOKEN = "//input[@id='password_field_name']"
HAPPY_CLICKER_LIST_POLLING_INTERVAL = "//input[@id='polling_interval']"
SUBMIT_BUTTON = "//input[@value='Submit' and @type='button']" 
CSA_EDIT_SETTINGS = "//input[@value='Edit Settings' and @type='button']"
EDIT_SETTINGS_TITLE = "//div[@class='hd']"
OK = "//div[@class='ft']/span[1]/span[1]/span[1]/button"
CANCEL = "//div[@class='ft']/span[1]/span[2]/span[1]/button"
CSA_SETTINGS_TABLE = "//table[@class='pairs']"

class  CiscoSecurityAwarwness(GuiCommon):
    """
    Library to interact with 'Security Services > Cisco Security Awarenedd' Page.
    """
    def get_keyword_names(self):
        return['csa_enable',
               'csa_edit',
               'csa_disable',
               'csa_is_enabled',
               'csa_is_disabled']

    def _open_page(self):
        self._debug('Opening Cisco Security Awareness page')
        self._navigate_to('Security Services', 'Cisco Security Awareness')

    def _select_csa_server(self, csa_server=None):
        self.select_from_list_by_label(CSA_SERVER, csa_server)

    def csa_enable(self, 
                   csa_server=None,
                   csa_token=None,
                   csa_polling_interval=None,
                   csa_polling_interval_time_unit=None,
                   confirm_edit_setting_action=None):
        """ Enable Cisco Security Awareness(CSA)

        Parameters:
         - csa_url: Available list of CSA region(s) for enable
                        1. AMERICA
                        2. EUROPEA
         - csa_token: Token obtained from CSA portal
         - csa_polling_interval: Poll interval between (60minutes/1hour - 7days)
        """
        self._info('Enabling the csa')
        self._open_page()
        if self._is_element_present(CSA_EDIT_SETTINGS):
           if self.csa_is_enabled():
                self._info('Cisco Security Awareness is already enabled')
                return
           else:
                self.click_button(CSA_EDIT_SETTINGS)
                if confirm_edit_setting_action:
                    self.click_button(CANCEL)
                else:
                    self.click_button(OK)
                    self._select_checkbox(ENABLE_CHECKBOX)
                    self._select_csa_server(csa_server=csa_server)
                    self.input_text(CSA_TOKEN, csa_token)
                    self.input_text(HAPPY_CLICKER_LIST_POLLING_INTERVAL, csa_polling_interval)
                    self.click_button(SUBMIT_BUTTON, "don't wait")
        else:
            self._open_page()
            self._debug('Opening Cisco Security Awareness page on a netinstalled appliance')
            self.click_button(ENABLE_BUTTON)
            self._select_checkbox(ENABLE_CHECKBOX)
            self._select_csa_server(csa_server=csa_server)
            self.input_text(CSA_TOKEN, csa_token)
            self.input_text(HAPPY_CLICKER_LIST_POLLING_INTERVAL, csa_polling_interval)
            self.click_button(SUBMIT_BUTTON, "don't wait")

    def csa_edit(self,
                 csa_server=None,
                 csa_token=None,
                 csa_polling_interval=None,
                 confirm_edit_setting_action=None):
        """ Edit settings for Cisco Security Awarenedd(CSA)

        Parameters:
         - csa_url: Available list of CSA region(s) for enable
                        1. AMERICA
                        2. EUROPEA
         - csa_token: Token obtained from CSA portal
         - csa_polling_interval: Poll interval between (60minutes/1hour - 7days)
        """
        self._info('Editing setting on the csa')
        self._open_page()
        self.click_button(CSA_EDIT_SETTINGS)
        if confirm_edit_setting_action.lower() == 'ok':
            self._wait_until_element_is_present(EDIT_SETTINGS_TITLE)
            self.click_button(OK)
            if csa_server:
                self._select_csa_server(csa_server=csa_server)
            if csa_token :
                self.input_text(CSA_TOKEN, csa_token)
            if csa_polling_interval:
                self._input_text_if_not_none(HAPPY_CLICKER_LIST_POLLING_INTERVAL, csa_polling_interval)
            self.click_button(SUBMIT_BUTTON, "don't wait")
        else:
            self.click_button(CANCEL)

    def _get_status(self):
        """ Check current status of the Email Cisco Security Awareness

        Return:
            Enabled or Disabled
        """
        status_info = {}
        for row in xrange(1, 2):
            key = self.get_text("%s/tbody/tr[%d]/th" % \
                                (CSA_SETTINGS_TABLE, row)).strip()
            value = self.get_text("%s/tbody/tr[%d]/td" % \
                                (CSA_SETTINGS_TABLE, row)).strip()
            status_info[key] = value
        return value

    def csa_is_enabled(self):
        """ Check whether Email Cisco Security Awareness 
        is enabled

        Return:
            Boolean True or False
        """
        self._info('Checking if Cisco Security Awareness is enabled')
        self._open_page()
        status = bool (not (self._get_status()=='Disabled'))
        return status

    def csa_is_disabled(self):
        """ Check whether Email Cisco Security Awareness
        is disable 

        Return:
            Boolean True or False
        """
        self._info('Checking if Cisco Security Awareness is enabled')
        self._open_page()
        DISABLED_MARK = 'Disabled'
        return self._is_text_present(DISABLED_MARK)

    def csa_disable(self,
                    confirm_edit_setting_action=None):
        """Disable Cisco Security Awareness 
        """
        self._info('Disabling Cisco Security Awareness')
        if not self.csa_is_enabled():
            self._info('Cisco Security Awareness is already disabled')
            return
        self.click_button(CSA_EDIT_SETTINGS)
        self._wait_until_element_is_present(EDIT_SETTINGS_TITLE)
        if confirm_edit_setting_action:
            self.click_button(CANCEL)
        else:
            self.click_button(OK)
            self._unselect_checkbox(ENABLE_CHECKBOX)
            self.click_button(SUBMIT_BUTTON, "don't wait")

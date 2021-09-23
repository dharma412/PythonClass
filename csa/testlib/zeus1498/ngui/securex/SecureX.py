import time

from common.ngui.exceptions import ElementNotFoundError, DataNotFoundError, UserInputError, BackEndWarning
from common.ngui.ngguicommon import NGGuiCommon


class SecureX(NGGuiCommon):

    def get_keyword_names(self):
        return ['securex_ribbon_is_visible',
                'securex_launch_ribbon',
                'securex_go_to_home',
                'securex_open_casebook',
                'securex_open_incidents',
                'securex_open_orbital',
                'securex_find_observables',
                'securex_get_account_details',
                'securex_change_theme',
                'securex_launch_applications',
                'securex_collapse_widget',
                'securex_login',
                'securex_get_cases',
                'securex_add_new_case',
                'securex_search_and_edit_case',
                'securex_case_investigate_in_threat_response',
                'securex_case_link_to_incident',
                'securex_case_download_json',
                'securex_case_delete',
                'securex_settings_ribbon_set_inverse_product_theme',
                'securex_settings_ribbon_reset',
                'securex_settings_casebook_auto_open',
                'securex_settings_casebook_reset',
                'securex_search_on_ribbon',
                'securex_find_observables_on_page',
                'securex_get_all_observables_on_page',
                'securex_case_pivot_menu']

    def securex_ribbon_is_visible(self):
        """
        This keyword to check the securex Ribbon is visible or not
        :return: True/False
        """
        return self._is_visible(SecurexWidget.ribbon)

    def securex_go_to_home(self):
        """
        This keyword is navigate to securex home application
        :return:
        """
        return self.click_element(SecurexWidget.home_icon)

    def securex_collapse_widget(self):
        """
        This keyword to close/collapse the opened securex widget
        :return:
        """
        return self.click_element(SecurexWidget.collapse)

    def securex_open_casebook(self, launch_from='toolbar'):
        """
        This keyword is navigate to securex open casebook application
        launch_from: toolbar/application
        toolbar:from secure ribbon
        application: From secure x home application
        :return:
        """
        if launch_from == 'toolbar':
            self.click_element(SecurexWidget.case_icon)
        elif launch_from == 'application':
            self.click_element(SecurexWidget.casebook_application)
        else:
            raise UserInputError('Invalid input for launch_from')
        self.wait_for_angular()

    def securex_open_incidents(self, launch_from='toolbar'):
        """
        This keyword is navigate to securex open incidents application
        launch_from: toolbar/application
        toolbar:from secure ribbon
        application: From secure x home application
        :return:
        """
        if launch_from == 'toolbar':
            self.click_element(SecurexWidget.incidents_icon)
        elif launch_from == 'application':
            self.click_element(SecurexWidget.incidents_application)
        else:
            raise UserInputError('Invalid input for launch_from')
        self.wait_for_angular()
        if not self._is_visible(SecurexWidget.incident_group):
            raise ElementNotFoundError('Failed to open incidents')

    def securex_open_orbital(self, launch_from='toolbar'):
        """
        This keyword is navigate to securex open oribital application
        launch_from: toolbar/application
        toolbar:from secure ribbon
        application: From secure x home application
        :return:
        """
        if launch_from == 'toolbar':
            self.click_element(SecurexWidget.orbital_icon)
        elif launch_from == 'application':
            self.click_element(SecurexWidget.orbital_application)
        else:
            raise UserInputError('Invalid input for launch_from')
        self.wait_for_angular()
        if not self._is_visible(SecurexWidget.orbital_app):
            raise ElementNotFoundError('Failed to launch orbital')
        if not self._is_visible(SecurexWidget.orbital_metrics):
            raise ElementNotFoundError('Failed to load orbital metrics')

    def securex_find_observables(self):
        """
        This is keyword to navigate to find observables
        :return:
        """
        self.click_element(SecurexWidget.find_observables)
        self.wait_for_angular()

    def securex_open_settings(self):
        """
        This is keyword to navigate to open settings
        :return:
        """
        self.click_element(SecurexWidget.settings)
        self.wait_for_angular()

    def securex_launch_ribbon(self):
        """
        This keyword is to launch SecureX Ribbon
        :return:
        """
        if self.securex_ribbon_is_visible:
            self.click_element(SecurexWidget.ribbon_container)
        else:
            raise ElementNotFoundError('SecureX widget not found.')

    def securex_get_account_details(self):
        """
        This keyword is to get SecureX account details
        :return:
        """
        self.securex_launch_ribbon()
        return self.get_text(SecurexWidget.account_details).split('\n')

    def securex_change_theme(self, theme):
        """
        To change the securex Theme
        :param theme:
        :return:
        """
        self.securex_launch_ribbon()
        self.securex_open_settings()
        if theme == 'Light':
            self.click_button(SecurexWidget.light_theme)
        elif theme == 'Dusk':
            self.click_button(SecurexWidget.dusk_theme)
        else:
            raise UserInputError('Invalid theme ...')

    def securex_launch_applications(self, name, title=None, application_url=None):
        """
        To launch securex applications
        :param name: application name like SecureX , Threat Response
        :return:
        """
        self.securex_launch_ribbon()
        self.securex_go_to_home()
        app_launched = 0
        for app_index in [index for index in range(self.get_element_count(SecurexWidget.platform_list)+1) if index%2 !=0]:
            app_name = self.get_text(SecurexWidget.platform_name%app_index)
            if app_name == name :
                self.click_element(SecurexWidget.launch_platform %app_index)
                app_launched = 1
                self.select_window('NEW')
                if title in self.get_title():
                    self._debug("CURRENT TITLE :%s" %self.get_title())
                    break
                if application_url in self.get_location():
                    self._debug("CURRENT Location :%s" % self.get_title())
                    break

        self.select_window('MAIN')
        if not app_launched:
            raise DataNotFoundError('Invalid application name.')

    def securex_login(self, server, client_id, client_secret):
        """
        SecureX Ribbon login
        :param server:APJC/EU/NAM
        :param client_id: <clientid>
        :param client_secret: <clientsecret>
        :return:
        """
        server_index = {'APJC': 1, 'EU': 2, 'NAM': 3}
        if not server_index.has_key(server):
            raise UserInputError('Invalid user input:%s' % server)

        if not self.securex_ribbon_is_visible:
            raise ElementNotFoundError('SecureX widget not found.')

        self.click_element(SecurexWidget.ribbon)
        self._wait_until_element_is_present(SecurexWidget.ribbon_component, timeout=5)
        if self._is_visible(SecurexWidget.ribbon_component):
            self.securex_collapse_widget()
            self.right_click_on_element(SecurexWidget.ribbon)
        self._wait_until_element_is_present(SecurexWidget.login_dialog, timeout=5)
        self.click_element(SecurexWidget.ctr_authentication_server % server_index[server])
        self.input_text(SecurexWidget.client_id, client_id)
        self.input_text(SecurexWidget.client_secret, client_secret)
        self.click_element(SecurexWidget.authenticate)
        self.wait_for_angular()
        if self._is_visible(SecurexWidget.ribbon_warning):
            self._debug('SecureX Warning exists')
            raise BackEndWarning('SecureX Warning exists')

    def _owned_by_group(self, group):
        search_list = ''
        if group == 'owned_by_me':
            self.click_element(Casebook.owned_by_me)
            self.wait_for_angular()
            search_list = Casebook.owned_by_me
        elif group == 'owned_by_others':
            self.click_element(Casebook.owned_by_others)
            self.wait_for_angular()
            search_list = Casebook.owned_by_others
        else:
            raise UserInputError('Invalid group for getting cases')
        return search_list

    def securex_get_cases(self, group='owned_by_me'):
        """
        This keyword is get the securex Cases from casebook
        :param group: owned_by_me/Owned_by_Others
        :return:
        """
        cases = []
        search_list = self._owned_by_group(group)
        self.set_selenium_speed('0s')
        case_count = self.get_element_count('%s%s' %(search_list, Casebook.case_list))
        for case_index in range(1, case_count+1):
            cases.append({'title': self.get_text('%s%s'%(search_list, Casebook.case_title%case_index)),
                         'detail': self.get_text('%s%s' % (search_list, Casebook.case_detail % case_index))})
        self.set_selenium_speed('0.5s')
        return cases

    def _add_observables(self, observables):
        for observable in observables:
            self.input_text(Casebook.case_observables_input, observable)
            self.press_keys(Casebook.case_observables_input, 'RETURN')
            self.wait_for_angular()

    def securex_add_new_case(self, title=None, summary=None, observables=None):
        """
        This keyword to add new case
        :param title: case title <type:str>
        :param summary: case summary <type:str>
        :param observables: observables list ( Type:List>
        :return:
        """
        if self._is_visible(Casebook.new_case):
            self.click_element(Casebook.new_case)
            self.wait_for_angular()
            if observables:
                self._add_observables(observables)
        else:
            raise ElementNotFoundError('Failed to create new case')

    def securex_search_and_edit_case(self, search_text=None, observables=None, group='owned_by_me'):
        """
        This keyword to search , select and edit the case
        :param search_text: search text of case to search
        :param observables: observables to add
        :param group: search on group
        :return:
        """
        search_list = self._owned_by_group(group)
        if self._is_visible(Casebook.case_search):
            self.click_element(Casebook.case_clear)
            self.input_text(Casebook.case_search, search_text)
            self.wait_for_angular()
            case_count = self.get_element_count('%s%s' % (search_list, Casebook.case_list))
            for case_index in range(1, case_count + 1):
                self.click_element('%s%s' % (search_list, Casebook.case_title % case_index))
                if observables:
                    self._add_observables(observables)
        else:
            raise ElementNotFoundError('Failed to search case on casebook')

    def securex_case_investigate_in_threat_response(self, title):
        """
        This keyword to perform investigate_in_threat_response
        :param title: Title of the new tab opened
        :return:
        """
        if self._is_visible(Casebook.investigate_in_threat_response):
            self.click_element(Casebook.investigate_in_threat_response)
            self.select_window('NEW')
            if title in self.get_title():
                self._debug("CURRENT TITLE :%s" % self.get_title())
            self.select_window('MAIN')
        else:
            raise ElementNotFoundError('Failed to investigate case in threat response')

    def _get_currents_incidents_in_case(self):
        return sorted([self.get_text(incident) for incident in self.find(Incident.current_incidents,
                                                                         first_only=False) if incident])

    def _check_incidents_updated(self, intial_incidents):
        count = 0
        while count <= 30:
            updated_incidents = self._get_currents_incidents_in_case()
            self._debug('Current Incidents:%s' % updated_incidents)
            if len(intial_incidents) != len(updated_incidents):
                break
            time.sleep(0.5)
            count +=1

    def _get_last_incident_added(self):
        return self._get_currents_incidents_in_case()[-1]

    def securex_case_link_to_incident(self, action=None):
        """
        This keyword to link the incident
        :param action: name (New Incident)
        :return: if action is New Incident, it will create new incident and will return the case linked to Incident
        """
        if self._is_visible(Casebook.link_to_incident):
            self.click_element(Casebook.link_to_incident)
            self.wait_for_angular()
        else:
            raise ElementNotFoundError('Failed to link incident')

        if action:
            intial_incidents = self._get_currents_incidents_in_case()
            self._debug('Intial Incidents:%s' % intial_incidents)
            if action == 'New Incident':
                self.click_element(Incident.new_incident)
                self.wait_for_angular()
                self._check_incidents_updated(intial_incidents)
                self.click_element("%s[text()='%s']" %(Incident.current_incidents, self._get_last_incident_added()))
                self.wait_for_angular()
                self.click_element(Incident.incident_linked_references)
                self.wait_for_angular()
                return self.get_text(Incident.incident_linked_case_title)
            else:
                raise UserInputError('Invalid Incident action')

    def securex_case_download_json(self):
        """
        This keyword to download the case
        :return:
        """
        if self._is_visible(Casebook.download_case):
            self.click_element(Casebook.download_case)
            self.wait_for_angular()
        else:
            raise ElementNotFoundError('Failed to download case')

    def securex_case_delete(self):
        """
        This keyword to delete the case
        :return:
        """
        if self._is_visible(Casebook.delete_case):
            self.click_element(Casebook.delete_case)
            self.wait_for_angular()
        else:
            raise ElementNotFoundError('Failed to delete case')

    def securex_settings_ribbon_set_inverse_product_theme(self):
        """
        This keyword to set the inverse product theme
        :return:
        """
        self.securex_open_settings()
        if self._is_visible(SecurexWidget.auto_set_inverse_product_theme):
            if self._is_checked(SecurexWidget.auto_set_inverse_product_theme_checkbox):
                self._info("Theme checkbox is already enabled")
            else:
                self.click_element(SecurexWidget.auto_set_inverse_product_theme)
        else:
            raise ElementNotFoundError('Failed to set inverse product theme')

    def securex_settings_ribbon_reset(self):
        """
        This keyword to do the secure x settings reset
        :return:
        """
        self.securex_open_settings()
        if self._is_visible(SecurexWidget.securex_reset):
            self.click_element(SecurexWidget.securex_reset)
            self._wait_until_element_is_present(SecurexWidget.reset_dialog, timeout=10)
            self.click_element(SecurexWidget.reset_confirm)
            self.wait_for_angular()
        else:
            raise ElementNotFoundError('Failed to do securex reset')

    def securex_settings_casebook_auto_open(self):
        """
        This keyword to do the secure x settings casebook auto open
        :return:
        """
        self.securex_open_settings()
        if self._is_visible(SecurexWidget.casebook_auto_open):
            if self._is_checked(SecurexWidget.casebook_auto_open_checkbox):
                self._info("Auto open checkbox is already enabled")
            else:
                self.click_element(SecurexWidget.casebook_auto_open)
        else:
            raise ElementNotFoundError('Failed to do securex casebook auto open')

    def securex_settings_casebook_reset(self):
        """
        This keyword to do the secure x casebook settings reset
        :return:
        """
        self.securex_open_settings()
        if self._is_visible(SecurexWidget.casebook_reset):
            self.click_element(SecurexWidget.casebook_reset)
            self._wait_until_element_is_present(SecurexWidget.reset_dialog, timeout=10)
            self.click_element(SecurexWidget.reset_confirm)
            self.wait_for_angular()
        else:
            raise ElementNotFoundError('Failed to do securex casebook reset')

    def _pivot_toolbar_action(self, case_action):
        if case_action == 'Active Case':
            self.click_button(SecurexWidget.pivot_menu_add_active_case)
        if case_action == 'New Case':
            self.click_button(SecurexWidget.pivot_menu_add_new_case)

    def _handle_pivot_menu(self, case_action, search_text):
        self.click_element(SecurexWidget.observable_pivot_menu % search_text)
        self.wait_for_angular()
        self._pivot_toolbar_action(case_action)

    def _handle_panel_menu(self, case_action):
        self.click_button(SecurexWidget.tippy_add_to_case_button)
        self.wait_for_angular()
        if case_action == 'Active Case':
            self.click_button(SecurexWidget.tippy_add_case_active)
        if case_action == 'New Case':
            self.click_button(SecurexWidget.tippy_add_case_new)

    def _handle_threat_response(self, title):
        self.click_link(SecurexWidget.tippy_threat_response_link)
        self.select_window('NEW')
        if title in self.get_title():
            self._debug("CURRENT TITLE :%s" % self.get_title())
        self.select_window('MAIN')

    def securex_search_on_ribbon(self, observable_name=None, observable_action=None, case_action=None,
                                 widget='panel', threat_response_title=None):
        """
        This keyword to search, add observables, observables action, cases action on panel/pivot menus
        :param observable_name: name of observable to search/add
        :param observable_action: Add to Case/Investigate in Threat Response
        :param case_action: Active Case/New Case
        :param widget: panel/pivot
        :param threat_response_title: title of the threat response window
        :return:
        """
        if self._is_visible(SecurexWidget.search_toolbar):
            if search_text:
                self.input_text(SecurexWidget.search_toolbar, observable_name)
                self.press_keys(SecurexWidget.search_toolbar, 'RETURN')
                self.wait_for_angular()
                self._wait_until_element_is_present(SecurexWidget.tippy_content, timeout=10)
                if observable_action == 'Add to Case':
                    if case_action:
                        self.click_element(SecurexWidget.observable_check_box % observable_name)
                        if widget == 'pivot':
                            self._handle_pivot_menu(case_action, observable_name)
                        else:
                            self._handle_panel_menu(case_action)
                    else:
                        raise UserInputError('Invalid Case Action')
                elif observable_action == 'Investigate in Threat Response':
                    self._handle_threat_response(threat_response_title)
                else:
                    raise UserInputError('Invalid Observable Action')
                self.click_element(SecurexWidget.search_toolbar)
            else:
                raise UserInputError('Search text to search Logs IP Domains')

    def securex_find_observables_on_page(self, observable_name=None, observable_action=None, case_action=None,
                                         widget='panel'):
        """
        This keywords to find the observable the particular observable on find observable on page and perform action
        :param observable_name: <obseravble name>
        :param observable_action: Add to Case/Investigate in Threat Response
        :param case_action: Active Case/New Case
        :param widget: panel/pivot
        :return:
        """
        self.securex_find_observables()
        self._wait_until_element_is_present(SecurexWidget.tippy_content, timeout=5)
        if observable_name:
            self._wait_until_element_is_present(SecurexWidget.observable_check_box% observable_name, timeout=5)
            self.click_element(SecurexWidget.observable_check_box % observable_name)
            if observable_action and widget == 'panel':
                if observable_action == 'Add to Case':
                    self._handle_panel_menu(case_action)
                elif observable_action == 'Investigate in Threat Response':
                    self._handle_threat_response(threat_response_title)
                else:
                    raise UserInputError('Invalid Observable Action')
            elif case_action and widget == 'pivot':
                self._handle_pivot_menu(case_action, observable_name)
            else:
                raise UserInputError('user invalid option')
            self.click_element(SecurexWidget.find_observables)
        else:
            raise UserInputError('observable_name is needed for find observables')

    def securex_get_all_observables_on_page(self):
        """
        This keyword to get all observables list on found observables list
        :return: observables list
        """
        self.securex_find_observables()
        self.wait_for_angular()
        self._wait_until_element_is_present(SecurexWidget.observables_finder_message, timeout=30)
        observable_list = []
        for observable in self.get_webelements(SecurexWidget.observables_list):
            observable_list.append(observable.text)
        self.click_element(SecurexWidget.find_observables)
        return observable_list

    def securex_case_pivot_menu(self, title=None, case_action=None):
        """
        This keyword is used to do actions on the pivot menu on the current page
        :param title: title of IP LOGS domain/Hash etc
        :param case_action: Active Case/New Case
        :return:
        """
        action_performed = 0
        if not title:
            raise UserInputError('Title needed')
        if not case_action:
            raise UserInputError('case_action')
        for observable in self.find(SecurexWidget.pivot_menu, first_only=False):
            self.set_focus_to_element(observable)
            self.mouse_over(observable)
            self._wait_until_element_is_present(SecurexWidget.tippy_popper, timeout=5)
            self.click_element(observable)
            self.wait_for_angular()
            self._wait_until_element_is_present(SecurexWidget.tippy_content, timeout=5)
            if str(title) == str(self.get_text(SecurexWidget.tippy_header).strip()):
                self._pivot_toolbar_action(case_action)
                action_performed = 1
                break
        if not action_performed:
            raise ElementNotFoundError('Failed to perform pivot menu case action')


class SecurexWidget:

    ribbon = "//*[@id='ats-security-ribbon']/div"
    ribbon_container = "//*[@id='ats-security-ribbon-container']"
    ribbon_component = "//*[@class='ats-ribbon-components__dragger dragger-absolute']"
    ribbon_warning ="//*[@class='ats-security-ribbon__bar__warnings']"

    login_dialog = "//*[@translate='common.ctrEditHeader']"
    ctr_authentication_server = "//*[@class='ctr-authentication__server']/div[%s]/input"
    client_id = "//*[@ng-model='$ctrl.ctrAuthenticationService.ctrClientCreds.clientId']"
    client_secret = "//*[@ng-model='$ctrl.ctrAuthenticationService.ctrClientCreds.clientSecret']"
    authenticate = "//*[@translate='buttons.authenticate']"

    account_details = "//*[@class='ats-security-ribbon__home__section ats-security-ribbon__home-account']"
    home_icon = "//*[@class='ats-security-ribbon__bar__applications__application']//*[name()='svg']//*[@href='#ats-ribbon-home']"
    case_icon = "//*[@class='ats-security-ribbon__bar__applications']/div[2]/*[name()='svg']"
    incidents_icon = "//*[@class='ats-security-ribbon__bar__applications']/div[3]/*[name()='svg']"
    orbital_icon = "//*[@class='ats-security-ribbon__bar__applications']/div[4]/*[name()='svg']"
    search = "//*[@id='a-text-input_60']"
    find_observables = "//*[@class='ats-security-ribbon__bar__toolbar']/div[2]/div/*[name()='svg']"
    settings ="//*[@class='ats-security-ribbon__bar__toolbar']/div[3]/div/*[name()='svg']"
    collapse = "//*[@class='ats-security-ribbon__bar__toolbar']/div[4]/div/*[name()='svg']"

    light_theme = "//button[@type='button' and @value='theme--default']"
    dusk_theme  = "//button[@type='button' and @value='theme--dusk']"
    auto_set_inverse_product_theme = "//*[@id='ats-security-ribbon-application']/div/div[1]/table/tbody/tr[2]/td[2]/label/span"
    auto_set_inverse_product_theme_checkbox = "//*[@id='ats-security-ribbon-application']/div/div[1]/table/tbody/tr[2]/td[2]/label/input"
    securex_reset = "//*[@id= 'ats-security-ribbon-application']/div/div[1]/table/tbody/tr[4]/td[2]/button"
    reset_dialog = "//*[@class='ats-ribbon-components__modal__dialog']"
    reset_confirm = "//*[@class='ats-ribbon-components__modal__dialog']/div/div[3]/button[2]"

    casebook_auto_open = "//*[@id='ats-security-ribbon-application']/div/div[2]/table/tbody/tr[1]/td[2]/label/span[1]"
    casebook_auto_open_checkbox = "//*[@id='ats-security-ribbon-application']/div/div[2]/table/tbody/tr[1]/td[2]/label/input"
    casebook_reset = "//*[@id='ats-security-ribbon-application']/div/div[2]/table/tbody/tr[2]/td[2]/button"
    casebook_application = "//*[@class='ats-security-ribbon__home-applications__list']/div[1]/*[name()='svg']"
    incidents_application = "//*[@class='ats-security-ribbon__home-applications__list']/div[2]/*[name()='svg']"
    orbital_application = "//*[@class='ats-security-ribbon__home-applications__list']/div[3]/*[name()='svg']"
    settings_application = "//*[@class='ats-security-ribbon__home-applications__list']/div[4]/*[name()='svg']"

    platform_list = "//*[@class='ats-security-ribbon__home-platform__list']/div"
    platform_name = "//*[@class='ats-security-ribbon__home-platform__list']/div[%s]/div[2]"
    launch_platform = "//*[@class='ats-security-ribbon__home-platform__list']/div[%s]/div[3]"
    incident_group = "//*[@class='ats-ribbon-components__search-panel__list-container__group']"
    orbital_app = "//*[@class='ats-orbital-app']"
    orbital_metrics = "//*[@id='ats-orbital__user-org-selector']"
    search_toolbar = "//*[@id ='ats-security-ribbon-enricher-input']/div/div/input"

    tippy_popper = "//*[@class='tippy-popper']"
    tippy_content = "//*[@class='tippy-content']"
    tippy_header = "//*[@class='ats-ribbon-components__pivot-menu__header__title']"
    tippy_add_to_case_button = "//*[@class='ats-ribbon-components__tippy-panel__toolbar']/div/button[contains(text(),'Add to Case')]"
    tippy_threat_response_link = "//*[@class='ats-ribbon-components__tippy-panel__toolbar']/div/a[contains(text(),'Investigate in Threat Response')]"
    tippy_add_case_active = "//*[@class='ats-ribbon-components__add-to-case-menu']/div/button[contains(text(),'Active Case')]"
    tippy_add_case_new = "//*[@class='ats-ribbon-components__add-to-case-menu']/div/button[contains(text(),'New Case')]"

    pivot_menu = "//*[@class='ats-ribbon-components__pivot']//*[name()='svg' and @class='ats-component-sprite ats-ribbon-components__pivot__sprite']"
    observables_finder_message ="//*[@class='ats-ribbon-components__finder__message']"
    observables_list = "//*[@class='ats-ribbon-components__finder__observable-list__observable__value']"
    observable_pivot_menu = "//*[@class='ats-ribbon-components__finder__observable-list__observable__value' and contains(text(), '%s')]/../div[3]/div"
    observable_check_box = "//*[@class='ats-ribbon-components__finder__observable-list__observable__value' and contains(text(), '%s')]/../div[1]/label/span[1]"
    pivot_menu_add_active_case = "//*[@class='ats-ribbon-components__pivot-menu__header__toolbar']/button[1]"
    pivot_menu_add_new_case = "//*[@class='ats-ribbon-components__pivot-menu__header__toolbar']/button[2]"


class Casebook:

    new_case = "//*[@id='ats-security-ribbon-application']/div/div[1]/div/div[2]/div[1]"
    check_mark = "//*[@id='ats-security-ribbon-application']/div/div[1]/div/div[2]/div[2]"
    investigate_in_threat_response = "//*[@class='ats-ribbon-components__panel__header__toolbar__item']/a[text()='Investigate in Threat Response']"
    link_to_incident = "//*[@class='ats-ribbon-components__panel__header__toolbar__item']/button[text()='Link to Incident']"

    download_case = "//*[@class='ats-ribbon-components__panel__header__toolbar__item']/button//*[name()='svg']//*[@href='#ats-components-download']"
    delete_case = "//*[@class='ats-ribbon-components__panel__header__toolbar__item']/button//*[name()='svg']//*[@href='#ats-components-trash']"
    owned_by_me = "//*[@id='search-list-scroll-container']/div[1]"
    owned_by_others = "//*[@id='search-list-scroll-container']/div[2]"

    case_list = '/ul/li'
    case_title = '/ul/li[%s]/div[2]/div[1]'
    case_detail = '/ul/li[%s]/div[2]/div[2]'
    case_overview = "//*[@id='ats-casebook-case']/div[1]/div[2]/div"
    case_detail_title_edit = '/div[2]/div[1]/div[2]/div/div/div[2]'
    case_detail_summary_edit = '/div[2]/div[4]/div[2]/div/div/div[2]'
    case_detail_title_input = "/div[2]/div[1]/div[2]/div[@class='ats-ribbon-components__inline-text-input']"
    case_observables_input = "//*[@id='ats-casebook-observable-enricher-input']/div/div/input"
    case_search = "//*[@class='ats-ribbon-components__search-panel__search']/div/div/div[2]/input"
    case_clear = "//*[@class='ats-ribbon-components__search-panel__search']/div/div/div[3]//*[name()='svg']"


class Incident:

    new_incident = "//*[@class='ats-ribbon-components__link-to-incident-menu__controls']/button[text()='New Incident']"
    current_incidents = "//*[@class='ats-casebook__overview']/ul/li/a"
    incident_linked_references ="//*[@class='a-tab-group']/div[contains(text(),'Linked References')]"
    incident_linked_case_title = "//*[@id='casebooks']/div/table/tbody/tr/td/a"
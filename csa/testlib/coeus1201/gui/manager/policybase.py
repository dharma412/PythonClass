#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/policybase.py#3 $
# $DateTime: 2019/12/01 23:10:23 $
# $Author: uvelayut $

from constants import (webcats, useragents)
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import Wait
import re
import time
import paramiko
from credentials import RTESTUSER, RTESTUSER_PASSWORD

# URL categories in 'Advanced Settings' -> 'URL categories membership'
# dictionary of {category name: category number used in its id}
WEBCAT_CODES = {
    webcats.ADULT: '1006',
    webcats.ADVERTISE: '1027',
    webcats.ALCOHOL: '1048',
    webcats.ARTS: '1002',
    webcats.BUSINESS: '1019',
    webcats.CHEAT: '1051',
    webcats.CHILD_PORN: '1064',
    webcats.COMPUTER_SEC: '1065',
    webcats.COMPUTING: '1003',
    webcats.CULTS: '1041',
    webcats.DATE: '1055',
    webcats.DINE: '1061',
    webcats.EDUCATION: '1001',
    webcats.FILE_XFER: '1071',
    webcats.FILTER: '1025',
    webcats.FINANCE: '1015',
    webcats.FREEWARE: '1015',
    webcats.GAMBLING: '1049',
    webcats.GAMES: '1007',
    webcats.GOVT_LAW: '1011',
    webcats.HACKING: '1050',
    webcats.HATE_SPCH: '1016',
    webcats.HLTH_NUTR: '1009',
    webcats.ILLEGAL_ACT: '1022',
    webcats.DRUGS: '1047',
    webcats.INFRA: '1018',
    webcats.IM: '1039',
    webcats.VOIP: '1067',
    webcats.JOB_SRCH: '1004',
    webcats.LINGERIE_SWIM: '1031',
    webcats.LOTTERY: '1034',
    webcats.CELL: '1070',
    webcats.NATURE: '1013',
    webcats.NEWS: '1058',
    webcats.NONSEX_NUDE: '1060',
    webcats.ONLINE_COMM: '1024',
    webcats.ONLINE_STOR: '1066',
    webcats.ONLINE_TRADE: '1028',
    webcats.PARANORMAL: '1029',
    webcats.PEER_FILE_XFER: '1056',
    webcats.PORN: '1054',
    webcats.REAL_ESTATE: '1045',
    webcats.REFERENCE: '1017',
    webcats.SAFE_KIDS: '1057',
    webcats.SCIENCE: '1012',
    webcats.SEARCH_PORT: '1020',
    webcats.SEX_EDU_ABORT: '1052',
    webcats.SHOPPING: '1005',
    webcats.SOCIAL_NET: '1069',
    webcats.SOCIAL_SCI: '1014',
    webcats.SOCIETY: '1010',
    webcats.SOFTWARE_UP: '1053',
    webcats.SPIRITUAL: '1042',
    webcats.SPORT_REC: '1008',
    webcats.STREAMING: '1026',
    webcats.TASTELESS: '1033',
    webcats.TATTOOS: '1043',
    webcats.TRANSPORTATION: '1044',
    webcats.TRAVEL: '1046',
    webcats.VIOLENCE: '1032',
    webcats.WEAPONS: '1036',
    webcats.WEBHOST: '1037',
    webcats.WEBPAGE: '1063',
    webcats.WEBCHAT: '1040',
    webcats.WEBEMAIL: '1038',

    webcats.IW_ADLT: '1006', # Adult
    webcats.IW_ADV: '1027', # Advertisements
    webcats.IW_AT: '1048', # Alcohol and Tobacco
    webcats.IW_ART: '1002', # Arts and Entertainment
    webcats.IW_BUSI: '1019', # Business and Industry
    webcats.IW_PLAG: '1051', # Cheating and Plagiarism
    webcats.IW_CPRN: '1064', # Child Porn
    webcats.IW_CSEC: '1065', # Computer Security
    webcats.IW_COMP: '1003', # Computers and Internet
    webcats.IW_CULT: '1041', # Cults
    webcats.IW_DATE: '1055', # Dating
    webcats.IW_FOOD: '1061', # Dining and Drinking
    webcats.IW_EDU: '1001', # Education
    webcats.IW_FTS: '1071', # File Transfer Services
    webcats.IW_FILT: '1025', # Filter Avoidance
    webcats.IW_FNNC: '1015', # Finance
    webcats.IW_FREE: '1068', # Freeware and Shareware
    webcats.IW_GAMB: '1049', # Gambling
    webcats.IW_GAME: '1007', # Games
    webcats.IW_GOV: '1011', # Government and Law
    webcats.IW_HACK: '1050', # Hacking
    webcats.IW_HATE: '1016', # Hate Speech
    webcats.IW_HLTH: '1009', # Health and Nutrition
    webcats.IW_ILAC: '1022', # Illegal Activities
    webcats.IW_DRUG: '1047', # Illegal Drugs
    webcats.IW_INFR: '1018', # Infrastructure
    webcats.IW_IM: '1039', # Instant Messaging
    webcats.IW_VOIP: '1067', # Internet Telephony
    webcats.IW_JOB: '1004', # Job Search
    webcats.IW_LING: '1031', # Lingerie and Swimsuits
    webcats.IW_LOTR: '1034', # Lottery and Sweepstakes
    webcats.IW_CELL: '1070', # Mobile Phones
    webcats.IW_NATR: '1013', # Nature
    webcats.IW_NEWS: '1058', # News
    webcats.IW_NSN: '1060', # Non-sexual Nudity
    webcats.IW_COMM: '1024', # Online Communities
    webcats.IW_OSB: '1066', # Online Storage and Backup
    webcats.IW_TRAD: '1028', # Online Trading
    webcats.IW_PARA: '1029', # Paranormal and Occult
    webcats.IW_P2P: '1056', # Peer File Transfer
    webcats.IW_PORN: '1054', # Porn
    webcats.IW_REST: '1045', # Real Estate
    webcats.IW_REF: '1017', # Reference
    webcats.IW_KIDS: '1057', # Safe for Kids
    webcats.IW_SCI: '1012', # Science and Technology
    webcats.IW_SRCH: '1020', # Search Engines and Portals
    webcats.IW_SXED: '1052', # Sex Ed and Abortion
    webcats.IW_SHOP: '1005', # Shopping
    webcats.IW_SNET: '1069', # Social Networking
    webcats.IW_SOCS: '1014', # Social Science
    webcats.IW_SCTY: '1010', # Society and Culture
    webcats.IW_SWUP: '1053', # Software Updates
    webcats.IW_HEAL: '1042', # Spiritual Healing
    webcats.IW_SPRT: '1008', # Sports and Recreation
    webcats.IW_MDIA: '1026', # Streaming Media
    webcats.IW_OBS: '1033', # Tasteless or Obscene
    webcats.IW_TAT: '1043', # Tattoos
    webcats.IW_TRNS: '1044', # Transportation
    webcats.IW_TRVL: '1046', # Travel
    webcats.IW_VIOL: '1032', # Violence
    webcats.IW_WEAP: '1036', # Weapons
    webcats.IW_WHST: '1037', # Web Hosting
    webcats.IW_TRAN: '1063', # Web Page Translation
    webcats.IW_CHAT: '1040', # Web-based Chat
    webcats.IW_MAIL: '1038', # Web-based Email

    webcats.UNCATEGORIZED: '1073741825',
}

# predefined User Agents locators
common_user_agent_dict = {
    'ff43': 'ff43_child',
    'ff42': 'ff42_child',
    'ff41': 'ff41_child',
    'ff40': 'ffpre40_child',
    'ff-all': 'ff-all_child',
    'msie11': 'ie11_child',
    'msie10': 'ie10_child',
    'msie9': 'ie9_child',
    'msie8': 'iepre8_child',
    'msie': 'ie-all_child',
    'gc48': 'gc48_child',
    'gc47': 'gc47_child',
    'gc46': 'gc46_child',
    'gc45': 'gcpre45_child',
    'gc': 'gc-all_child',
    'opr35': 'opr35_child',
    'opr34': 'opr34_child',
    'opr33': 'opr33_child',
    'opr32': 'oprpre32_child',
    'opr': 'opr-all_child',
    'sf9': 'sf9_child',
    'sf8': 'sf8_child',
    'sf7': 'sf7_child',
    'sf6': 'sf6_child',
    'sf5': 'sf5_child',
    'sf4': 'sfpre4_child',
    'sf': 'sf-all_child',
    'ms-update':    'windows_update_child',
    'acro-update':  'acro-update_child'}

common_agents_locators = {
    useragents.FF43: 'ff43_child',
    useragents.FF42: 'ff42_child',
    useragents.FF41: 'ff41_child',
    useragents.FF40: 'ffpre40_child',
    useragents.FF: 'ff-all_child',
    useragents.MSIE11: 'ie11_child',
    useragents.MSIE10: 'ie10_child',
    useragents.MSIE9: 'ie9_child',
    useragents.MSIE8: 'iepre8_child',
    useragents.MSIE: 'ie-all_child',
    useragents.GC48: 'gc48_child',
    useragents.GC47: 'gc47_child',
    useragents.GC46: 'gc46_child',
    useragents.GC45: 'gcpre45_child',
    useragents.GC: 'gc-all_child',
    useragents.OPR35: 'opr35_child',
    useragents.OPR34: 'opr34_child',
    useragents.OPR33: 'opr33_child',
    useragents.OPR32: 'oprpre32_child',
    useragents.OPR: 'opr-all_child',
    useragents.SF9: 'sf9_child',
    useragents.SF8: 'sf8_child',
    useragents.SF7: 'sf7_child',
    useragents.SF6: 'sf6_child',
    useragents.SF5: 'sf5_child',
    useragents.SF4: 'sfpre4_child',
    useragents.SF: 'sf-all_child',
    useragents.MS_UPDATE: 'windows_update_child',
    useragents.ADOBE_UPDATER: 'acro-update_child'
}

valid_protocols_map = {
             'http' : 'http',
             'nativeftp' : 'nativeftp',
             'ftpoverhttp' : 'ftp',
             'others' : 'others',
             }

POLICY_LINK_TMPL = "xpath=//a[strong[normalize-space(text())='%s']]"
ENABLE_POLICY_CHECKBOX = "xpath=//input[@type='checkbox' and @id='enabled']"
ENABLE_POLICY_EXPIRES_CHECKBOX = "xpath=//input[@type='checkbox' and @id='expire_confirm']"
CUSTOM_URL_CAT_SELECT_ALL="xpath=//a[contains(@onclick,'memberscustomcat')]"
PREDEFINED_URL_CAT_SELECT_ALL="xpath=//a[contains(@onclick,'memberswebcat')]"

class PolicyBase:
    """
    *Specifying identities*

    Identities can be set in different kinds of policies and the format of the
    setting is the same for all of them.

    Identities are specified as a string of comma-separated values where each
    identity is presented in the following format:

    <name>[:<auth_method>[:<list of users>[:<list of groups>]]]

    - name: name is the only required field
    - auth_method: default value is None. Other accepted values:
        * authenticated
        * selected
        * guests
        * all
     - list of users: users separated by #
     - list of groups: groups separated by #
     - list of SGT groups: groups separated by #

    Note. If identity with name "All Identification Profiles" is in the list of
    identities, it should be the only 1 in the list

    Note. List of users, list of groups, and list of STG groups are used when
    auth_method is "selected"

    Examples:
    | identities=i2 |
    | identities=Global Identification Profile:authenticated |
    | identities=i2:selected:vasia#petya:group1#group2:SGTGroup8#SGTGroup6 |
    | identities=All Identification Profiles:all |
    | identities=i2:selected::group3#group4, Global Identification Profile:guests |
    """

    def _enable(self, name):
        """Enables existing policy

        Parameters:
            - `name` policy name to enable
        """

        self._open_policy_settings(name)
        self._select_checkbox(ENABLE_POLICY_CHECKBOX)
        self._click_submit_button(wait=False, accept_confirm_dialog=True)

    def _disable(self, name):
        """Disable existing policy

        Parameters:
            - `name` policy name to disable
        """

        self._open_policy_settings(name)
        self._unselect_checkbox(ENABLE_POLICY_CHECKBOX)
        self._click_submit_button(wait=False, accept_confirm_dialog=True)

    def _is_enabled(self, name):
        """Checks if is enabled existing policy

        Parameters:
            - `name` policy name to check
        """

        self._open_policy_settings(name)
        return self._is_checked(ENABLE_POLICY_CHECKBOX)

    def _open_policy_settings(self, name):
        """Clicks on policy name to open policy settings

        Parameters:
            - `name` policy name to open
        """

        self.click_link(POLICY_LINK_TMPL % (name,))
        self._wait_until_element_is_present(ENABLE_POLICY_CHECKBOX)

    def _click_add_policy_button(self):
        add_policy_button = "AddGroup"
        self.click_button(add_policy_button)

    def _click_edit_policy_link(self, name, column):
        table_id = 'xpath=//table[@class="cols"]'
        cell_id = table_id + '//tr[%s]//td[%s]/a'

        policy_row = self._get_policy_row_index(name)
        if policy_row is None:
            raise guiexceptions.GuiControlNotFoundError(
                     'Policy "%s"' % (name,), self.get_location())
        self.click_link(cell_id % (policy_row, column))
        # allow policy page to get fully loaded
        time.sleep(2)

    def _fill_policy_page(self, name, description=None, order=None, expires=None, datetimemin=None, dut=None):
        if name is not None:
            self._fill_policy_name(name)
        if description is not None:
            self._fill_policy_description(description)
        if order is not None:
            self._set_policy_order(order)
        if expires is not None:
            self._set_expiration_for_policy(datetimemin,dut)

    def _set_expiration_for_policy(self, datetimemin, dut):
        self._select_checkbox(ENABLE_POLICY_EXPIRES_CHECKBOX)
        temp = datetimemin.split("-")
        tempdate = temp[0].lstrip("0")
        CALENDAR_LINK = "//html/body/div[1]/div/div[2]/div/table/tbody//td[contains(@class,'d%s')]"%tempdate
        date_id = "//*[@id='expire_date']"
        self.click_element(date_id, "don't wait")
        time.sleep(5)
        self.click_element(CALENDAR_LINK, "don't wait")
        hr_option = "expire_hour"
        min_option = "expire_minute"
        self.select_from_list(hr_option, temp[1])
        self.select_from_list(min_option, temp[2])

    def _delete_policy(self, name, delete_column):
        CONFIRMATION_BUTTON = "//button [text() = 'Delete']"
        table_id = 'xpath=//table[@class="cols"]'
        cell_id = table_id + '//tr[%s]//td[%s]/img'
        start_time = time.time()
        while time.time() - start_time < 60: # max possible timeout for worst scenario
            policy_row = self._get_policy_row_index(name)
            if not policy_row is None:
                break
        else:
                raise guiexceptionGuiControlNotFoundError('Policy instance: "%s"'\
                  % (name,), self.get_location())
        policy_row = self._get_policy_row_index(name)
        if policy_row is None:
            raise guiexceptions.GuiControlNotFoundError(
                    'Policy "%s"' % (name,), self.get_location())
        self.click_element(cell_id % (policy_row, delete_column), "don't wait")
        self.click_element(CONFIRMATION_BUTTON, "don't wait")

    def _edit_identity_membership(self, identities):
        """ list of identification profiles, separated by comma.
        <name>[:<auth_method[#<auth-realm>]>[:<list of users>[:<list of groups>[:<list of SGT groups>]]]]
        All fields except name are optional
        If name is "All Identities", there should be only 1 identity
        <auth_method>: one of [authenticated, selected, guests,all]
        <auth-realm> is used when auth is "selected"
        <list of users> should be either empty or contain users separated by #
        <list of groups> should be either empty or contain groups separated by #
        <list of SGT groups>] should be either empty or contain groups separated by #
        """
        IDENTITY_ID = 'id=identity'
        MULTI_ID_ROW = lambda idx: 'xpath=//tr[@id="multi_identities_row%s"]' \
             % idx
        ADD_ROW_BUTTON = 'id=multi_identities_domtable_AddRow'
        DEL_ROW_BUTTON = lambda idx: MULTI_ID_ROW(idx) + '/td[3]/img'
        M_ID_CONTROL = \
            lambda idx, ctrl: 'id=multi_identities[%s][%s]' % (idx, ctrl)
        ID_CONTROL = lambda ctrl: 'id=%s' % (ctrl,)
        # self.logger.info('Editing identity membership')
        id_auth_map = {
            'authenticated':'all_auth',
            'selected':'selected_auth',
            'guests':'guest_auth',
            'all' :'auth_noauth',
        }
        # first validating
        identities = self._convert_to_tuple(identities)
        all_identities = False
        for _identity in identities:
            identity_array = _identity.split(":")
            if len(identity_array) > 5:
                raise guiexceptions.GuiValueError(\
                    "Wrong format of identity " + str(_identity))
            if str(identity_array[0]) == 'All Identitification Profiles':
                if all_identities == False:
                    all_identities = True
                if len(identities) > 1:
                    raise guiexceptions.GuiValueError(\
                        "All Identities should be the only one in the list")

        if all_identities == False:

            self.select_from_list(IDENTITY_ID, 'Select One or More Identification Profiles')

            #find all existing rows
            rows = int(self.get_matching_xpath_count(
                    '//tr[starts-with(@id, "multi_identities_row")]'))
            # delete all identities besides the first one
            for idx in range(rows - 1, 0, -1):
                self.click_element(DEL_ROW_BUTTON(idx), "don't wait")
                # "//td[@id='itable-delete_row%s']/img" % (idx)

            # clear space for new identities
            for idx in range(1, len(identities)):
                self.click_element(ADD_ROW_BUTTON, "don't wait")

            idx = -1
            for _identity in identities:
                idx += 1
                identity = _Identity(_identity)

                #fill identity settings
                self.select_from_list(M_ID_CONTROL(idx, 'identities'),
                                       identity.name)
                if identity.auth_method is not None:
                    self.click_element(
                        M_ID_CONTROL(idx, id_auth_map[identity.auth_method]),
                             "don't wait")
                    if identity.auth_method == 'authenticated' \
                        and identity.auth_realm  is not None:
                        # setup auth realm
                        self.select_from_list(M_ID_CONTROL(idx, 'auth_realm'),
                                               identity.auth_realm)
                    elif identity.auth_method == 'selected':
                        if identity.users:
                            self._fill_id_users('members_username_%s' % (idx,),
                                                identity.users)
                        if identity.groups:
                            self._fill_id_groups('members_auth_group_%s' % idx,
                                identity.groups, identity.auth_realm)
                        if identity.sgt_groups:
                            self._fill_sgt_groups('members_sgt_%s' % idx,
                                identity.sgt_groups)
        else:
            # All identities
            self.select_from_list(IDENTITY_ID, 'All Identification Profiles')
            identity = _Identity(identities[0])
            if identity.auth_method is not None:
                self.click_element(ID_CONTROL(\
                    id_auth_map[identity.auth_method]), "don't wait")
                if identity.auth_method == 'selected':
                    if identity.users is not None:
                        self._fill_id_users('auth_users_link', identity.users)
                    if identity.groups is not None:
                        self._fill_id_groups('auth_groups_link',
                            identity.groups)
                    if identity.sgt_groups is not None:
                        self._fill_sgt_groups('auth_sgt_link',
                            identity.sgt_groups)

        # self.logger.info('Selected "%s" identities' % (identities,))
    def _edit_advanced_settings(self,
            protocols=None,
            proxy_ports=None,
            subnets=None,
            time_range=None,
            match_range=True,
            url_categories=None,
            user_agents=None,
            common_user_agents=None,
            match_agents=True):
        # advanced membership options may be invisible. Make them visible
        expose_advanced = 'id=arrow_closed'
        if      protocols    is not None    \
            or  proxy_ports  is not None    \
            or  subnets      is not None    \
            or  time_range   is not None    \
            or  url_categories is not None  \
            or  common_user_agents is not None  \
            or  user_agents  is not None:

            if self._is_element_present(expose_advanced):
                if self._is_visible(expose_advanced):
                    self.click_element(expose_advanced, "don't wait")
        if protocols is not None:
            self._edit_protocols_membership(self._convert_to_tuple(protocols))

        if proxy_ports is not None:
            self._edit_proxy_ports_membership(proxy_ports)

        if subnets is not None:
            self._edit_subnets_membership(self._convert_to_tuple(subnets))

        if time_range is not None:
            self._edit_time_range_membership(time_range, match_range)

        if url_categories is not None:
            self._edit_url_categories_membership(
                    self._convert_to_tuple(url_categories))

        if user_agents is not None:
            self._edit_user_agents_membership(
                    self._convert_to_tuple(user_agents),
                    self._convert_to_tuple(common_user_agents), match_agents)


    def _fill_id_users(self, link, users):
        if not isinstance(users, (tuple, list)):
            users = (users,)
        self.click_element(link)
        self.input_text('id=members_username', ', '.join(users))
        self._click_done_button()
        #self.check_action_result()

    def _fill_id_groups(self, link, groups, realm, action='add'):
        _timeout = 60
        _map = {
            "add": ("//select [@id='auth_group_list']",
                    "//input [@id='add_member_button']"),
            "remove": ("//select [@id='members_auth_group']",
                       "//input [@id='remove_member_button']"),
        }

        REALM_ID_LOCATOR = "xpath=//select[@id='auth_realm_sel']"

        if not groups:
            return
        self.click_element(link)

        if realm:
            self._wait_until_element_is_present(REALM_ID_LOCATOR)
            self.select_from_list(REALM_ID_LOCATOR, realm)

        self._wait_until_text_is_present('Directory search completed',
            timeout=200)
        if not isinstance(groups, (tuple, list)):
            groups = (groups,)
        start_time = time.time()
        selections = [mem.strip() for mem in groups]
        found = False
        while (not found and (time.time() - start_time < _timeout)):
            available_selections = self.get_list_items(_map[action][0])
            for available_selection in available_selections:
                if available_selection.find(selections[0]) > -1:
                    found = True
                    break

        select_list = []
        for selection in selections:
            for available_selection in available_selections:
                if available_selection.find(selection) > -1:
                    if not available_selection in select_list:
                        select_list.append(available_selection)
                    break
            else:
                raise guiexceptions.ConfigError(action + \
                    'selection "%s" not found' % selection)

        self.select_from_list(_map[action][0], *select_list)
        self.click_element(_map[action][1], "don't wait")
        self._click_done_button(wait=False)

    def _fill_sgt_groups(self, link, groups, action='add'):
        _timeout = 30
        _search = "//dt [contains(text(), 'Service Group Tag Search')]/..//tr"
        _map = {
            "add": ("//dt[contains(text(), 'Service Group Tag Search')]/..",
                    "//input [@id='add_btn']",
                    "//input [@id='select_all']",
                    ),
            "remove": ("//dt[contains(text(), 'Authorized Secure Group Tags')]/..",
                       "//input [@id='delete_btn']",
                       "//input [@id='delete_all']",
                    ),
        }
        check_box = lambda action, group: _map[action][0] + \
            "//div[contains(text(), '%s')]" % group + \
            "/../..//input[@type='checkbox']"

        if not groups:
            return
        self.click_element(link)

        # Wait until SGT are loaded
        try:
            self._wait_until_element_is_present(_search, _timeout)
        except:
            pass
        time.sleep(5)

        if not isinstance(groups, (tuple, list)):
            groups = (groups,)
        if groups[0] == 'all' and len(groups) == 1:
            self._select_checkbox(_map[action][2]) # select all
        else:
            for gr in groups:
                self._select_checkbox(check_box(action, gr))
        self.click_element(_map[action][1], "don't wait")
        self._click_done_button(wait=False)

    def _edit_protocols_membership(self, protocols):

        self.click_link('adv_membership_link_protocols')
        self._select_protocols(protocols)
        self._click_done_button()

    def _edit_proxy_ports_membership(self, proxy_ports):

        if not self._is_visible('adv_membership_link_proxy_ports'):
            txt = self.get_text('adv_membership_text_proxy_ports')
            raise guiexceptions.GuiFeatureDisabledError(txt)

        self.click_link('adv_membership_link_proxy_ports')

        self._fill_proxy_ports_membership(proxy_ports)

        self._click_done_button()

    def _edit_subnets_membership(self, subnets):

        if not self._is_visible('adv_membership_link_members_ip'):
            txt = self.get_text('adv_membership_text_members_ip')
            raise guiexceptions.GuiFeatureDisabledError(txt)

        self.click_link('adv_membership_link_members_ip')

        self._set_subnets_membership(subnets)

        self._click_done_button()

    def _edit_time_range_membership(self, time_range, match_range=True):

        if not self._is_visible('adv_membership_link_time_range'):
            txt = self.get_text('adv_membership_text_time_range')
            raise guiexceptions.GuiFeatureDisabledError(txt)

        self.click_link('adv_membership_link_time_range')

        self._set_time_range_membership(time_range, match_range)

        self._click_done_button()

    def _edit_url_categories_membership(self, categories):

        if not self._is_visible('adv_membership_link_url_categories'):
            txt = self.get_text('adv_membership_text_url_categories')
            raise guiexceptions.GuiFeatureDisabledError(txt)

        self.click_link('adv_membership_link_url_categories')

        self._select_url_categories_membership(categories)

        self._click_done_button()

    def _unselect_all_checks(self):
        """Unselect all Checks by clicking on all images check.gif
        """
        CHECK = "//div/img[contains(@src, \
            '/images/url_categories/check.gif')]"
        CHECKPATH = "xpath=" + CHECK

        count = int(self.get_matching_xpath_count(CHECK))

        self._info(str(count) + " to uncheck")
        for i in range(count):
            if self._is_visible(CHECKPATH):
                self.click_element(CHECKPATH, "don't wait")

        count = int(self.get_matching_xpath_count(CHECK))
        if count > 0:
            raise guiexceptions.GuiControlNotFoundError(\
                "Failed to uncheck " + str(count) + " checks")

    def _edit_user_agents_membership(self, user_agents,
            common_user_agents=None, match_agents=None):


        self.click_link('adv_membership_link_user_agents')
        if user_agents is not None:
            self._set_user_agents(user_agents)
        if common_user_agents is not None:
            self._set_common_user_agents(common_user_agents)
        if match_agents is not None:
            self._set_user_agents_matching(match_agents)

        self._click_done_button()

    def _get_custom_url_categories(self):
        cat_page_id = lambda cat_id: 'customActions[%s]' % (cat_id,)

        def grab_from_dialog():
            cat_name_cell = "//table[@id='dialog_grid']/tbody/tr%s/td[1]"
            cat_names_xpath = cat_name_cell % ''
            cat_name_locator = lambda row: cat_name_cell % '[%s]' % (row + 2)
            SELECT_BTN = "//input[@value='Select Custom Categories...']"
            CANCEL_BTN = "//div[@id='custom_cats_dialog']//button[text() = 'Cancel']"
            if self._is_element_present(SELECT_BTN):
                self.click_element(SELECT_BTN, "don't wait")

                try:
                    cat_count = int(
                            self.get_matching_xpath_count(cat_names_xpath))
                except:
                    cat_count = 0

                for i in xrange(cat_count):
                    cat_name = self.get_text(cat_name_locator(i))
                    custom_categories[cat_name] = cat_page_id(i)

                self.click_element(CANCEL_BTN, "don't wait")

        def grab_from_table():
            cat_name_cell = ("//table[@id='customDataGrid']/tbody/tr%s/" + \
                             "td/div/span")
            cat_names_xpath = cat_name_cell % ''
            cat_name_locator = lambda row: cat_name_cell % '[%s]' % (row + 1)

            try:
                cat_count = int(self.get_matching_xpath_count(cat_names_xpath))
            except:
                cat_count = 0

            for i in xrange(cat_count):
                cat_name = self.get_text(cat_name_locator(i))
                custom_categories[cat_name] = cat_page_id(i)

        custom_categories = {}
        grab_from_table()
        grab_from_dialog()

        return custom_categories

    def _get_predefined_url_categories(self):
        cat_name_cell = ("//table[@id='predefinedDataGrid']/tbody/tr%s/td/" + \
                         "div/span")
        cat_names_xpath = cat_name_cell % ''
        cat_name_locator = lambda row: cat_name_cell % '[%s]' % (row + 1)
        cat_page_id = lambda cat_id: 'predefinedActions[%s]' % (cat_id,)

        predefined_cats = {}

        try:
            cat_count = int(self.get_matching_xpath_count(cat_names_xpath))
        except:
            cat_count = 0

        for i in xrange(cat_count):
            cat_name = self.get_text(cat_name_locator(i))
            predefined_cats[cat_name] = cat_page_id(i)

        return predefined_cats

    def _get_policy_row_index(self, name):
        policy_table = '//table[@class="cols"]'
        table_rows = self.get_matching_xpath_count(
                                     '%s/tbody/tr' % (policy_table,))
        for i in xrange(2, int(table_rows) + 1):
            policy_name = self.get_text('xpath=%s/tbody/tr[%s]/td[2]' %
                              (policy_table, i)).split(' \n')[0]
            self._debug('Found policy "%s" in row %d' % \
                    (policy_name, i))
            if name.strip() == policy_name.strip():
                return i

        # buggy code, but some tests can rely on it
        # so if no policy is matched we will use old behavior
        for i in xrange(2, int(table_rows) + 1):
            policy_name = self.get_text('xpath=%s/tbody/tr[%s]/td[2]' %
                              (policy_table, i)).split(' \n')[0]
            if re.match('%s\s*' % name, policy_name):
                return i
        return None

    def _fill_policy_name(self, name):
        name_id = 'id=policy_group_id'
        self.input_text(name_id, text=name)

    def _fill_policy_description(self, description):
        description_id = 'id=description'
        self.input_text(description_id, text=description)

    def _set_policy_order(self, order):
        order_option_button = "insert_before"
        current_policies = self.get_list_items(order_option_button)

        if isinstance(order, int):
            try:
                insert_before = current_policies[order - 1]
            except IndexError:
                raise ValueError, 'Wrong policy order - "%s"' % (order,)
        else:
            for policy in current_policies:
                if order in policy:
                    insert_before = policy
                    break
            else:
                raise ValueError, '"%s" policy is not configured' % (order,)

        self.select_from_list(order_option_button, insert_before)

    def _click_done_button(self, wait=True):
        done_button = 'xpath=//input[@value=\'Done\']'
        if wait:
            self.click_button(done_button)
        else:
            self.click_button(done_button, None)

        # sometimes it takes long time so we want to be sure that
        # we have returned to prev page
        text_in_adv = 'following advanced membership criteria have been defined'
        try:
            self._wait_until_text_is_present(text_in_adv)
        except guiexceptions.TimeoutError:
            # some pages does not display the confirmation
            pass

    def _select_protocols(self, protocols):
        if self._is_visible('https'):
            valid_protocols_map['https'] = 'https'

        # unselect all protocols first
        for protocol in valid_protocols_map.values():
            self._unselect_checkbox(protocol)

        for protocol in protocols:
            if protocol not in valid_protocols_map.keys():
                raise ValueError, 'Invalid protocol name - "%s"' % (protocol,)
            self._select_checkbox(valid_protocols_map[protocol])

    def _fill_proxy_ports_membership(self, proxy_ports):
        proxy_ports_id = 'id=proxy_ports'

        self.input_text(proxy_ports_id, proxy_ports)

    def _set_subnets_membership(self, subnets):
        subnets_members_id = 'id=members_ip'
        subnets_text = ', '.join(subnets)

        self._click_radio_button('id=subnet_custom')
        self.input_text(subnets_members_id, subnets_text)

    def _set_time_range_membership(self, time_range, match_range):
        time_range_id = 'id=time_range'

        self.select_from_list(time_range_id, time_range)

        if match_range:
            self._click_radio_button('time_inverse_false')
        else:
            self._click_radio_button('time_inverse_true')

    def _get_custom_membership_url_categories(self):
        customcat_element = '//input[@name=\'memberscustomcat[]\']'
        custom_categories = {}
        starting_row = 3
        customcat_table = \
         "//div[s[text()='Custom and External URL Categories']]/following-sibling::table[1]"

        if self._is_element_present(customcat_element):
            # Getting the number of custom categories
            customcatsnum = int(self.get_matching_xpath_count
                                (customcat_element))

            if customcatsnum > 0:
                # Populating the custom_categoriess dict with
                # {custom category name: link to this custom category on the
                #  page}

                for i in xrange(starting_row, starting_row + customcatsnum):
                    category_name = self.get_text(customcat_table + '//tr[%s]/td[1]' % (i,))
                    custom_categories[category_name] = customcat_table + \
                        '//tr[%s]/td[3]/div' % (i,)

        return custom_categories

    def _select_url_categories_membership(self, categories):
        custom_categories = self._get_custom_membership_url_categories()

        self._debug('custom_categories=' + str(custom_categories))
        self._debug('webcat_codes=' + str(WEBCAT_CODES))
        self._unselect_all_checks()
        if len(categories) == 1 and categories[0] in ('all','all_custom','all_predefined'):
            self._select_all_url_categories(categories[0])
        else:
            for category in categories:
                self._debug('category=' + str(category))

                if custom_categories.has_key(category):
                    self.click_element('xpath=%s' % custom_categories[category], "don't wait")
                elif WEBCAT_CODES.has_key(category):
                    self.click_element('img_%s::customCheckBox::memberswebcat[]' % WEBCAT_CODES[category], "don't wait")
                else:
                    raise ValueError('"%s" URL category is not present' % category)

    def _select_all_url_categories(self, category):
        if category == 'all_predefined':
            self.click_element(PREDEFINED_URL_CAT_SELECT_ALL)
        elif category == 'all_custom':
            if self._is_visible(CUSTOM_URL_CAT_SELECT_ALL):
                self.click_element(CUSTOM_URL_CAT_SELECT_ALL)
            else:
                raise ValueError, 'No custom category selected'
        else:
            self.click_element(PREDEFINED_URL_CAT_SELECT_ALL)
            if self._is_visible(CUSTOM_URL_CAT_SELECT_ALL):
                self.click_element(CUSTOM_URL_CAT_SELECT_ALL)

    def _set_common_user_agents(self, common_user_agents):
        browser_open_arrow = 'arrow_open_browsers'
        browser_close_arrow = 'arrow_closed_browsers'
        others_open_arrow = 'arrow_open_Others'
        others_close_arrow = 'arrow_closed_Others'
        common_user_agent_dict = {
            'ff43': 'ff43_child',
            'ff42': 'ff42_child',
            'ff41': 'ff41_child',
            'ff40': 'ffpre40_child',
            'ff-all': 'ff-all_child',
            'msie11': 'ie11_child',
            'msie10': 'ie10_child',
            'msie9': 'ie9_child',
            'msie8': 'iepre8_child',
            'msie': 'ie-all_child',
            'gc48': 'gc48_child',
            'gc47': 'gc47_child',
            'gc46': 'gc46_child',
            'gc45': 'gcpre45_child',
            'gc': 'gc-all_child',
            'opr35': 'opr35_child',
            'opr34': 'opr34_child',
            'opr33': 'opr33_child',
            'opr32': 'oprpre32_child',
            'opr': 'opr-all_child',
            'sf9': 'sf9_child',
            'sf8': 'sf8_child',
            'sf7': 'sf7_child',
            'sf6': 'sf6_child',
            'sf5': 'sf5_child',
            'sf4': 'sfpre4_child',
            'sf': 'sf-all_child',
            'ms-update':    'windows_update_child',
            'acro-update':  'acro-update_child'}

        if self._is_visible(browser_close_arrow):
            self.click_element(browser_close_arrow, "don't wait")
        if self._is_visible(others_close_arrow):
            self.click_element(others_close_arrow, "don't wait")

        for common_user_agent in common_user_agent_dict:
            if common_user_agent in common_user_agents:
                self.select_checkbox(common_user_agent_dict[common_user_agent])
            else:
                self.unselect_checkbox(
                                    common_user_agent_dict[common_user_agent])

    def _set_user_agents(self, user_agents):
        custom_agents_box = 'id=custom_user_agents'
        custom_agents = []

        for user_agent in user_agents:
            if user_agent in common_agents_locators:
                self.select_checkbox(common_agents_locators[user_agent])
            else:
                custom_agents.append(user_agent)

        custom_agents_text = '\r\n'.join(custom_agents)
        self.input_text(custom_agents_box, custom_agents_text)

    def _set_user_agents_matching(self, match):
        if match:
            self._click_radio_button('user_agent_direct')
        else:
            self._click_radio_button('user_agent_reverse')

    def _select_action_combo(self, locator, action):

        actions_map = {
            'allow': 'Allow',
            'block': 'Block',
            'decrypt': 'Decrypt',
            'drop': 'Drop',
            'global': 'Use Global',
            'monitor': 'Monitor',
            'pass': 'Pass Through',
            'redirect': 'Redirect',
            'warn': 'Warn',
            }

        self.select_from_list(locator, actions_map[action])

    def _edit_url_category(self, action, cat_id, timerange=None, tb_action=None,
                           tb_otherwise=None, redirect_link=None, quota=None):
        cat_actions = {
            'allow': "//*[@id='allow_customRadio_%s[action]']",
            'block': "//*[@id='block_customRadio_%s[action]']",
            'decrypt': "//*[@id='decrypt_customRadio_%s[action]']",
            'drop': "//*[@id='drop_customRadio_%s[action]']",
            'global': "//*[@id='global_customRadio_%s[action]']",
            'monitor': "//*[@id='scan_customRadio_%s[action]']",
            'pass': "//*[@id='pass_customRadio_%s[action]']",
            'redirect': "//*[@id='redirect_customRadio_%s[action]']",
            'timebased': "//*[@id='time_customRadio_%s[action]']",
            'quotabased': "//*[@id='quota_customRadio_%s[action]']",
            'warn': "//*[@id='continue_customRadio_%s[action]']",
        }

        def enable_custom_cat(cat_id):
            cat_locator = lambda num: '%s_dialog_custom_cat' % num
            SELECT_BTN = "//input[@value='Select Custom Categories...']"
            SUBMIT_BTN = "//button[text() = 'Apply']"

            if self._is_element_present(SELECT_BTN):
                self.click_element(SELECT_BTN, "don't wait")

                # note: cat_id is of customActions[0]. we grab the number
                # and then reassembly new id
                num = re.search('customActions\[(\d+)\]', cat_id).group(1)
                self.select_from_list(cat_locator(num), 'include')

                self.click_element(SUBMIT_BTN, "don't wait")

        #if not isinstance(action, accepted_actions):
        #    raise ValueError, 'Wrong category action - "%s"' % (cat_action,)

        #Custom category may be excluded from policy. Include it.
	def exclude_custom_cat(cat_id):
            cat_locator = lambda num: '%s_dialog_custom_cat' % num
            SELECT_BTN = "//input[@value='Select Custom Categories...']"
            SUBMIT_BTN = "//button[text() = 'Apply']"

            if self._is_element_present(SELECT_BTN):
                self.click_element(SELECT_BTN, "don't wait")

                # note: cat_id is of customActions[0]. we grab the number
                # and then reassembly new id
                num = re.search('customActions\[(\d+)\]', cat_id).group(1)
                self.select_from_list(cat_locator(num), 'exclude')

                self.click_element(SUBMIT_BTN, "don't wait")

        if 'custom' in cat_id:
            # Custom category? enable it before
		if action.lower() == 'exclude':
			exclude_custom_cat(cat_id)
		else:
			enable_custom_cat(cat_id)

	if action.lower() != 'exclude':
		self.click_element(cat_actions[action] % (cat_id,), "don't wait")

        # Redirect action has URL to be filled in
        if action.lower() == 'redirect':
            self.input_text('redirect_%s[action]' % (cat_id,), redirect_link)

        # Time-Based action has complex structure
        if action.lower() == 'timebased':
            tb_action = tuple([item.strip() for item in tb_action.split('-')])
            in_action = tb_action[0]
            if len(tb_action) > 1:
                in_redirect = tb_action[1]
            else:
                in_redirect = None

            tb_otherwise = \
                tuple([item.strip() for item in tb_otherwise.split('-')])
            out_action = tb_otherwise[0]
            if len(tb_otherwise) > 1:
                out_redirect = tb_otherwise[1]
            else:
                out_redirect = None

            self._edit_time_action_settings(cat_id, action, timerange, in_action,
                                            out_action, in_redirect,
                                            out_redirect)
        # Quota-Based action has complex structure
        if action.lower() == 'quotabased':
            self.select_from_list('%s[quota_profile]' % (cat_id), quota)

    def _edit_time_action_settings(self, cat_id, action, time_range,
                                   action_in, action_out, in_redirect_url=None,
                                   out_redirect_url=None):

        # Selects time range
        self.select_from_list('%s[time_range]' % (cat_id), time_range)

        # Selects action for in and out the time range
        self._select_time_action('in', cat_id, action_in, in_redirect_url)
        self._select_time_action('out', cat_id, action_out, out_redirect_url)

    def _select_time_action(self, suffix, cat_id, action, url):

        locator = '%s[action_%s]' % (cat_id, suffix)
        self._select_action_combo(locator, action)

        if action == 'redirect' and url is not None:
            self.input_text('%s[redirect_%s_url]_field' % \
                        (cat_id, suffix), url)

class _Identity:
    def __init__(self, identity):
        identity_array = identity.split(":")
        self.name = identity_array[0]
        self.auth_method = None
        self.auth_realm = None
        self.users = None
        self.groups = None
        self.sgt_groups = None

        if len(identity_array) > 1:
            auth_array = identity_array[1].split("#")
            if len(auth_array) > 1 and len(auth_array[1]) > 0:
                self.auth_realm = auth_array[1]
            if len(auth_array[0]) > 0:
                self.auth_method = auth_array[0]

            if len(identity_array) > 2 and len(identity_array[2]):
                self.users = identity_array[2].split("#")

            if len(identity_array) > 3 and len(identity_array[3]):
                self.groups = identity_array[3].split("#")

            if len(identity_array) > 4 and len(identity_array[4]):
                self.sgt_groups = identity_array[4].split("#")

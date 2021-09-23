#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/manager/dlpmanager.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from sal.containers import cfgholder

# common locators
ADD_DLP_POLICY_BUTTON = "//input[@value='Add DLP Policy...']"
DEL_BUTTON = "//button[@type='button']"
PAIRS_TABLE = "//table[@class='pairs' and @style]"
PAIRS_TABLE_ROWS = "%s/tbody/tr" % (PAIRS_TABLE,)
COLS_TABLE = "//table[@class='cols']"
TEMPLATE_DIV_LOC = "//div[@id='arrow_closed_%d']/a"
POLICY_NAME_TB = "//*[@id='name']"
POLICY_DESCRIPTION = "//*[@id='description']"
NEW_POLICY_LINK = lambda tbl_indx, policy_indx: "//*[@id='section_%d']/tbody/tr[%d]/td/a" % (tbl_indx, policy_indx)
POLICIES_GRP_TABLE = lambda tbl_indx: "//*[@id='section_%d']/tbody/tr" % tbl_indx
DEL_LINK = lambda cols_table, policy_indx: "%s/tbody/tr[%d]/td[4]/img" % (cols_table, policy_indx)
DUP_LINK = lambda cols_table, policy_indx: "%s/tbody/tr[%d]/td[3]/a/img" % (cols_table, policy_indx)
POLICIES_DIV = "//*[@id='form']/dl/dd/div[2]"
POLICY_PAGE_TITLE = "//*[@id='page_title']"

# us licenses
USE_LICENSE_LINK = "//table[@class='pairs']//*/tr[contains(.,'Drivers Licenses')]/td/a"
ENABLE_ALL_LICENSES_LINK = "//table[@class='pairs']//a[1]"
DISABLE_ALL_LICENSES_LINK = "//table[@class='pairs']//a[2]"
US_STATE_CB = lambda state: "id=%s" % state

# dlp dictionaries
ADD_CUST_DLP_DICT = "//input[@value='Add Dictionary...']"
CUSTDICT_DELETE_CONFIRM = "//button[@type='button']"
CUSTDICT_NEXT = "//input[@value='Next >>']"
CUSTDICT_EXPORT = "//input[@value='Export Dictionary...']"
CUSTDICT_IMPORT = "//input[@title='Import Dictionary...']"
CUSTOM_DLP_DICT_ROWS = "//dl[@class='box' and contains(.,'Custom')]//table[@class='cols']/tbody/tr"
PREDEFINED_DLP_DICT_ROWS = "//dl[@class='box' and contains(.,'Predefined')]//table[@class='cols']/tbody/tr"
CUSTOM_DLP_DICT_LINK = "//form[@id='form']/dl[2]/dd/table/tbody/tr/td/a"
CUSTOM_DLP_DICT_NAME = 'name=id'
CUSTOM_DLP_DICT_TERMS = "name=add_list"
ADD_TERMS_BUTTON = "//input[@value='Add' and @type='button']"
ADD_CUST_DICT_BTN = "//input[@value='Submit' and @type='submit']"
CUST_DICT_FIRST_ROW = "//table[@class='cols']/tbody/tr"
CUST_DICT_ROW = "//table[@class='cols']/tbody/tr[%d]"
CUST_EDIT_LINK = lambda row: "//table[@class='cols']/tbody/tr[%d]/td[1]/a" % row
CUST_TERM_DEL_LINK = lambda term_indx: "//tbody[@class='yui-dt-data']/tr[%d]/td[2]/div/a" % term_indx
CUST_TERM_FIRST_ROW = "//tbody[@class='yui-dt-data']/tr"
CUST_TERM_ROW = "//tbody[@class='yui-dt-data']/tr[%d]"
CUST_DICT_DEL_LINK = lambda row: "//table[@class='cols']/tbody/tr[%d]/td[3]/img" % row
CUST_IMPORT_LOCAL_RB = "id=import_local"
IMPORT_LOCAL_PATH_TB = "name=local_file"
CUST_IMPORT_DUT_RB = "id=import_server"
CUST_IMPORT_DUT_LB = "file_server"
ENCODING_DD = "encoding"
MORE_TERMS_TA = "name=add_list"
IMPORT_SUBMIT_BTN = "//input[@class='submit']"
IMPORTED_DICT_NAME_TB = "//table[@class='pairs']/tbody/tr/td/input"
DICT_TO_EXPORT_DD = "import_id"
EXPORT_FILENAME = 'name=file_server'
EXPORT_LOCAL_RB = "id=export_local"
EXPORT_SERVER_RB = "id=export_server"

# dlp policy filter senders and recipients
RCPT_APPLY_IF_DD = "exclude_recipients"
RCPTS_TA = "name=recipients"
SENDER_APPLY_IF_DD = "exclude_senders"
SENDERS_TA = "name=senders"

# dlp policy filter attachments
BUTTON_REMOVE_ATTACHMENT_TYPE = "//*[@class='button-secondary' and contains(@value,'Remove')]"
BUTTON_ADD_ATTACHMENT_TYPE = "//*[@class='button-secondary' and contains(@value,'Add')]"
FILE_TYPE_CATEGORIES = "//*[@id='file_type_categories']"
FILE_TYPE_EXTENSION_LIST = "//*[@id='all_extensions[]']"
FILE_TYPE_ACTUAL_EXTENSION_LIST = "//*[@id='actual_extensions[]']"
APPLY_IF_DD = "negate_extensions"
ADDITIONAL_ATTACHMENTS_DD = "name=other_extensions"
APPLY_TO_ENCRYPTED_PWD_CB = "name=handle_encrypted"
MIN_ATTACHMENT_SIZE_TB = "name=min_attachment_size"

# dlp policy filter tags
MSG_TAGS_APPLY_DD = "negate_message_tags"
MSG_TAGS_TB = "name=message_tags"
FILTER_MESSAGE_TAGS_LINK = "//*[@id='form']/dl[1]/dd/table/tbody/tr[6]/th/a"
FILTER_ATTACHMENTS_LINK = "//*[@id='form']/dl[1]/dd/table/tbody/tr[5]/th/a"
FILTER_SEND_RECP_LINK = "//*[@id='form']/dl[1]/dd/table/tbody/tr[4]/th/a"

# dlp policy classifier
CLASSIFIER_LOC = "id=selected_classifier"
CLASSIFIER_ADD_BUTTON = "//*[@id='custom_content_blades_domtable_AddRow']"
CLASSIFIER_LOC = "id=selected_classifier"
RULE_TYPE_DD = lambda rule_indx: "rules[%d][rule_type]" % rule_indx
INCLUDE_PAT_LOC = lambda rule_indx: "rules[%d][values]" % rule_indx
EXCLUDE_PAT_LOC = lambda rule_indx: "rules[%d][exclude]" % rule_indx
WEIGHT_TB = lambda rule_indx: "rules[%d][weight]" % rule_indx
MAX_SCORE_TB = lambda rule_indx: "rules[%d][max_score]" % rule_indx
ADD_RULE_BUTTON = "//*[@id='rules_domtable_AddRow']"
SEVERITY_DD = lambda severity: "%s_msg_action" % severity
CLASSIFIER_TABLE = "//*[@id='custom_content_blades']"
CLASSIFIER_SUBTABLE = "%s/tbody[@id='custom_content_blades_rowContainer']" % CLASSIFIER_TABLE
CLASSIFIER_SUBTABLE_ROW = "%s/tr" % CLASSIFIER_SUBTABLE
CLASSIFIER_SUBTABLE_DELETE_LINK = lambda name: "%s[contains(.,'%s')]/td[3]" % (CLASSIFIER_SUBTABLE_ROW, name)
CLASSIFIER_SUBTABLE_MARK_NOT_LINK = lambda name: "%s[contains(.,'%s')]/td[2]/input" % (CLASSIFIER_SUBTABLE_ROW, name)
CLASSIFIER_MATCH = "//*[@id='classifier_match']"
CONTENT_MATCHING_CLASSIFIER_NAME = "name=name"
CLASSIFIER_DESCRIPTION = "name=classifier_description"
PROXIMITY = "name=proximity"
MIN_TOTAL_SCORE = "name=min_total_score"


class Dlpmanager(GuiCommon):

    def get_keyword_names(self):
        return ['dlp_policy_new',
                'dlp_policy_edit',
                'dlp_policy_duplicate',
                'dlp_policy_delete',
                'dlp_policy_get_definition',
                'dlp_policy_get_all',
                'dlp_policy_configure_severity_settings',
                'dlp_policy_configure_filter_attachments',
                'dlp_policy_configure_filter_message_tags',
                'dlp_policy_configure_filter_senders_and_recipients',
                'dlp_policy_create_classifier',
                'dlp_policy_configure_content_matching_classifier',
                'dlp_policy_edit_order',
                'dlp_policy_edit_us_drivers_licenses',
                'dlp_custom_dictionary_add',
                'dlp_custom_dictionary_edit',
                'dlp_custom_dictionary_delete',
                'dlp_custom_dictionary_import',
                'dlp_custom_dictionary_export',
                'dlp_custom_dictionary_get_all',
                'dlp_custom_dictionary_get_terms',
                'dlp_predefined_dictionary_get_all', ]

    def _open_page(self):
        self._navigate_to('Mail Policies', 'DLP Policy Manager')

    def _open_dlp_dict_page(self):
        self._open_page()
        self.click_element(CUSTOM_DLP_DICT_LINK)

    def _get_entity_indx(self, comp_str, prim_loc, sec_loc, shift_val=1):
        rows = int(self.get_matching_xpath_count(prim_loc))
        start = shift_val
        end = rows + shift_val
        for entity_indx in range(start, end):
            read_name = self.get_text(sec_loc % (entity_indx,))
            if comp_str.lower() in read_name.lower():
                return entity_indx

    def _get_policy_link(self, policy_name):
        policy_indx = self._get_entity_indx(policy_name,
                                            "%s/tbody/tr" % COLS_TABLE,
                                            "//table[@class='cols']/tbody/tr[%d]",
                                            1)
        policy_link = "%s/tbody/tr[%d]/td[2]/a" % (COLS_TABLE, policy_indx)
        return policy_link

    def _open_edit_policy_page(self, policy_name):
        if policy_name:
            self._open_page()
            policy_link = self._get_policy_link(policy_name)
            self.click_element(policy_link)

    def _handle_submit(self, submit):
        if submit:
            self._click_submit_button()

    def _handle_is_and_isnot(self, locator, option):
        if option:
            if option.lower() == 'is':
                self.select_from_list(locator, "Is")
            elif option.lower() == 'is not':
                self.select_from_list(locator, "Is Not")

    def _convert_list_to_string(self, user_input):
        # converts list to string of comma-separated values
        if isinstance(user_input, list):
            return ','.join(user_input)
        return user_input

    def _convert_to_cfgholder(self, user_input):
        """
        the same as _convert_to_dictionary() from arguments.py,
        but returns RecursiveCfgHolder.
        """
        _result = cfgholder.RecursiveCfgHolder()
        _array = user_input.split(',')
        for _pair in _array:
            _pos = _pair.find(':')
            if _pos < 0:
                _result[_pair.strip()] = ''
            else:
                _result[_pair[0:_pos].strip()] = _pair[_pos + 1:].strip()

        return _result

    def _get_list_of_dictionaries(self, base_locator):
        """
        Common method to get list of names of DLP dictionaries
        """
        self._open_dlp_dict_page()
        try:
            rows = int(self.get_matching_xpath_count(base_locator))
        except guiexceptions.SeleniumClientException as e:
            self._warn(e)
            return []
        names = []
        for dict_indx in range(2, rows + 1):
            d = str(self.get_text("%s[%d]/td[1]" % (base_locator, dict_indx)))
            self._debug(d)
            names.append(d)
        self._debug(names)
        return names

    def dlp_policy_new(self,
                       template_name,
                       policy_name,
                       change_policy_name=None,
                       description=None,
                       submit=True):
        """
        This function adds new DLP policy from existing templates or custom policy.

        Parameters:
        - `template_name`: Name of the DLP template to be added. String. Mandatory.
        - `policy_name`: Name of the DLP policy to be added. String. Mandatory.
        - `change_policy_name`: New name for the DLP policy if at all it needs
        to be changed. String.
        - `description`: Description of the DLP policy. String.
        - `submit`: If True, press Submit button. Boolean.

        Return:
        None

        Examples:
        | Dlp Policy New |
        | ... | Custom Policy |
        | ... | Custom Policy |
        | ... | change_policy_name=Basic Policy |
        | ... | submit=${True} |

        | Dlp Policy New |
        | ... | Regulatory Compliance |
        | ... | HIPAA and HITECH |
        | ... | submit=${False} |
        """
        self._info('Adding new DLP policy %s under the template %s' \
                   % (policy_name, template_name))
        self._open_page()
        self.click_button(ADD_DLP_POLICY_BUTTON)
        tbl_indx = \
            self._get_entity_indx(template_name, PAIRS_TABLE_ROWS,
                                  TEMPLATE_DIV_LOC, 0)
        self.click_element(TEMPLATE_DIV_LOC % tbl_indx, "don't wait")
        policy_indx = \
            self._get_entity_indx(policy_name, POLICIES_GRP_TABLE(tbl_indx),
                                  "//*[@id='section_%d']/tbody/" % tbl_indx + "tr[%d]/td/b", 1)
        self.click_element(NEW_POLICY_LINK(tbl_indx, policy_indx))
        if policy_name.lower() == "custom policy" or change_policy_name:
            pol_name = change_policy_name or policy_name
            self.input_text(POLICY_NAME_TB, pol_name)
        if description:
            self.input_text(POLICY_DESCRIPTION, description)
        self._handle_submit(submit)

    def dlp_policy_edit(self,
                        policy_name,
                        change_policy_name=None,
                        description=None,
                        submit=True):
        """
        This function edits DLP policy.

        Parameters:
        - `policy_name`: Name of the DLP policy to be edited. String. Mandatory.
        - `change_policy_name`: New name for the DLP policy if at all it needs
        to be changed. String.
        - `description`: Description of the DLP policy. String.
        Pass ${EMPTY} to clear the text-field.
        - `submit`: If True, press Submit button. Boolean.

        Return:
        None

        Examples:
        | Dlp Policy Edit |
        | ... | My Policy |
        | ... | change_policy_name=Basic Policy |
        | ... | submit=${True} |
        | ... | Dlp Policy Edit |
        | ... | HIPAA and HITECH |
        | ... | description=new description |
        | ... | submit=${False} |
        """
        self._info('Editing DLP policy %s.' % policy_name)
        self._open_page()
        policy_link = self._get_policy_link(policy_name)
        self.click_element(policy_link)
        if change_policy_name is not None:
            self.input_text(POLICY_NAME_TB, change_policy_name)
        if description is not None:
            self.input_text(POLICY_DESCRIPTION, description)
        self._handle_submit(submit)

    def dlp_policy_duplicate(self,
                             policy_name,
                             change_policy_name=None,
                             description=None,
                             submit=True):
        """
        This function duplicates an existing DLP policy.

        Parameters:
        - `policy_name`: Name of the DLP policy to be duplicated. String.
        Mandatory.
        - `change_policy_name`: New name for the DLP policy if at all it needs
        to be changed. String.
        - `description`: Description of the DLP policy. String.
        - `submit`: If True, press Submit button. Boolean.

        Return:
        None

        Examples:
        | Dlp Policy Duplicate |
        | ... | Custom Policy |
        | ... | change_policy_name=New Policy Name |
        | ... | description=New Policy Description |
        | ... | submit=${True} |

        | Dlp Policy Duplicate |
        | ... | New Policy Name |
        | ... | change_policy_name=My Policy Name |
        | ... | description=Another Description |
        | ... | submit=${False} |
        """
        self._info('Duplicating DLP policy %s.' % (policy_name,))
        self._open_page()
        policy_indx = self._get_entity_indx(policy_name,
                                            "%s/tbody/tr" % COLS_TABLE,
                                            "//table[@class='cols']/tbody/tr[%d]",
                                            1)
        self.click_element(DUP_LINK(COLS_TABLE, policy_indx))
        if change_policy_name is not None:
            self.input_text(POLICY_NAME_TB, change_policy_name)
        if description is not None:
            self.input_text(POLICY_DESCRIPTION, description)
        self._handle_submit(submit)

    def dlp_policy_delete(self, policy_name):
        """
        This function is used to delete the given DLP policy.

        Parameters:
        -`policy_name`: Name of the DLP policy to be deleted. String.
        Mandatory.

        Return:
        None

        Examples:
        | Dlp Policy Delete | My Policy Name |
        """
        self._info('Deleting DLP policy %s.' % policy_name)
        self._open_page()
        policy_indx = self._get_entity_indx(policy_name,
                                            "%s/tbody/tr" % COLS_TABLE,
                                            "//table[@class='cols']/tbody/tr[%d]",
                                            1)
        self.click_element(DEL_LINK(COLS_TABLE, policy_indx), "don't wait")
        self.click_element(DEL_BUTTON)

    def dlp_policy_get_all(self):
        """
        This function gets the list of names of all the DLP policies configured.

        Parameters:
        None

        Return:
        The list of configured DLP policies. List.

        Examples:
        | @{policies} | Dlp Policy Get All |
        """
        self._info('Getting all configured DLP policies')
        self._open_page()
        try:
            rows = \
                int(self.get_matching_xpath_count("%s/tbody/tr" % COLS_TABLE))
        except guiexceptions.SeleniumClientException:
            policy_text = self.get_text(POLICIES_DIV)
            return policy_text
        dlp_policies = []
        for policy_indx in range(2, rows + 1):
            policy = \
                str(self.get_text("%s/tbody/tr[%d]" % (COLS_TABLE, policy_indx)))
            dlp_policies.append(policy)
        return dlp_policies

    def dlp_policy_get_definition(self,
                                  policy_name,
                                  policy_template='Custom'):
        """
        This function gets the configured options of the DLP policy.

        Parameters:
        - `policy_name`: Name of the DLP policy to be fetch data from. String.
        - `policy_template`: Custom or one of Predefined policies.

        Return:
        The list of configured DLP policies. List.

        Examples:
        | Dlp Policy Get Definition | Policy Name |
        """
        self._info('Getting DLP policy definition for %s.' % policy_name)
        self._open_page()
        policy_link = self._get_policy_link(policy_name)
        self.click_element(policy_link)
        title_str = self.get_text(POLICY_PAGE_TITLE)
        # TODO need to take a look into the iaf tests
        # and check if this method is needed at all
        # if yes, grab a huge amount of options
        # and return in cfgholder
        return title_str

    def dlp_policy_edit_order(self,
                              policy_name,
                              order):
        """
        This function edits the order of given DLP policy.

        Parameters:
        - `policy_name`: Name of the DLP policy. String.
        - `order`: Order of the DLP policy. Number.

        Return:
        None
        """
        self.logger.info('Editing the order of DLP policy %s to %d' % \
                         (policy_name, order))
        self._open_page()
        self.click_button(ADD_DLP_POLICY_BUTTON)
        # TODO: needs dragging function

    def dlp_policy_edit_us_drivers_licenses(self,
                                            enable_list=None,
                                            disable_list=None,
                                            enable_all=None,
                                            disable_all=None):
        """
        This function enables or disables US driver license for different states.

        Parameters:
        - `enable_list`: List of states for which driver license need to be enabled.
        List or Sting of comma-separated values.
        - `disable_list`: List of states for which driver license need to be disabled.
        List or Sting of comma-separated values.
        - `enable_all`: To enable driver license for all the states. Boolean.
        - `disable_all`: To clear driver license for all the states. Boolean.

        Return:
        None

        Examples:
        | Dlp Policy Edit Us Drivers Licenses |
        | ... | enable_list=South Dakota, California, Utah, Vermont, Virginia |

        | Dlp Policy Edit Us Drivers Licenses | enable_all=${True} |
        | Dlp Policy Edit Us Drivers Licenses | disable_all=${True} |
        """
        self._info('Editing the US drivers licenses')
        self._open_page()
        self.click_element(USE_LICENSE_LINK)
        if enable_list:
            self.click_element(DISABLE_ALL_LICENSES_LINK, "don't wait")
            for c in self._convert_to_tuple(enable_list):
                c = c.replace(' ', '').lower()
                self._select_checkbox(US_STATE_CB(c))
        if disable_list:
            self.click_element(ENABLE_ALL_LICENSES_LINK, "don't wait")
            for c in self._convert_to_tuple(disable_list):
                c = c.replace(' ', '').lower()
                self._unselect_checkbox(US_STATE_CB(c))
        if enable_all is not None:
            if enable_all:
                self.click_element(ENABLE_ALL_LICENSES_LINK, "don't wait")
        if disable_all is not None:
            if disable_all:
                self.click_element(DISABLE_ALL_LICENSES_LINK, "don't wait")
        self._click_submit_button()

    def dlp_policy_configure_filter_attachments(self,
                                                policy_name=None,
                                                attachment_category=None,
                                                extensions_to_remove=None,
                                                apply_if=None,
                                                additional_attachments=None,
                                                apply_to_encrypted_pwd=None,
                                                min_attachment_size=None,
                                                submit=True):
        """
        This function limits DLP policy to given attachment types.

        Parameters:
        - `policy_name`: If policy name is defined then open page to edit the policy.
        Otherwise, consider that we are at the needed page. String.
        - `attachment_category`: A dictionary where attachment types are keys and extensions are values.
        Extensions can be passed as List or as String of comma-separated values.
        Like: {'Documents':('doc','pdf','pub'), 'Executable':'exe'}
        - `extensions_to_remove`: list of extensions to remove from filter list.
        List or String of comma-separated values.
        - `apply_if`: Possible values are: 'Is', 'Is Not'. Case insensitive. String.
        - `additional_attachments`: List of additional attachments to be filtered.
        List or String of comma-separated values. Pass ${EMPTY} to clear the text-field.
        - `apply_to_encrypted_pwd`: Only apply to encrypted or password protected attachments. Boolean.
        - `min_attachment_size`: Minimum size of the attachments to be filtered. String.
        Pass ${EMPTY} to clear the text-field.
        - `submit`: If True, press Submit button. Boolean.

        Return:
        None

        Examples:
        | @{docs} | Set Variable | pdf | pub | rtf |
        | @{executables} | Set Variable | exe | java |
        | ${attachment_category} | Create Dictionary | Documents | ${docs} | Executables | ${executables} |

        | Dlp Policy Configure Filter Attachments |
        | ... | policy_name=Advanced Policy1 |
        | ... | attachment_category=${attachment_category} |
        | ... | apply_if=Is |
        | ... | submit=${True} |

        | Dlp Policy Configure Filter Attachments |
        | ... | policy_name=Advanced Policy1 |
        | ... | extensions_to_remove=${executables} |
        | ... | min_attachment_size=1000 |
        | ... | submit=${True} |

        | @{additional_attachments} | Set Variable | lhka | boo | etc |
        | Dlp Policy Configure Filter Attachments |
        | ... | policy_name=Advanced Policy1 |
        | ... | apply_to_encrypted_pwd=${True} |
        | ... | submit=${True} |
        | ... | additional_attachments=${additional_attachments} |
        """
        self._info('Configuring filter attachments.')
        self._open_edit_policy_page(policy_name)
        if not self._is_visible(APPLY_IF_DD):
            self.click_element(FILTER_ATTACHMENTS_LINK, "don't wait")
        if attachment_category:
            for key in attachment_category.keys():
                self.select_from_list(FILE_TYPE_CATEGORIES, key)
                self.select_from_list(FILE_TYPE_EXTENSION_LIST,
                                      *self._convert_to_tuple(attachment_category[key]))
                self.click_button(BUTTON_ADD_ATTACHMENT_TYPE, "don't wait")
        if extensions_to_remove is not None:
            # if there are values - all values will be selected by default
            # passing empty list unselects all items
            self.unselect_from_list(FILE_TYPE_ACTUAL_EXTENSION_LIST, *[])
            self.select_from_list(FILE_TYPE_ACTUAL_EXTENSION_LIST,
                                  *self._convert_to_tuple(extensions_to_remove))
            self.click_button(BUTTON_REMOVE_ATTACHMENT_TYPE, "don't wait")
        self._handle_is_and_isnot(APPLY_IF_DD, apply_if)
        if additional_attachments is not None:
            self.input_text(ADDITIONAL_ATTACHMENTS_DD,
                            self._convert_list_to_string(additional_attachments))
        if apply_to_encrypted_pwd is not None:
            if apply_to_encrypted_pwd:
                self._select_checkbox(APPLY_TO_ENCRYPTED_PWD_CB)
            else:
                self._unselect_checkbox(APPLY_TO_ENCRYPTED_PWD_CB)
        if min_attachment_size is not None:
            self.input_text(MIN_ATTACHMENT_SIZE_TB, min_attachment_size)
        self._handle_submit(submit)

    def dlp_policy_configure_severity_settings(self,
                                               policy_name=None,
                                               critical=None,
                                               high=None,
                                               medium=None,
                                               low=None,
                                               submit=True):
        """ This function adds severity settings for the given DLP policy..

        Parameters:
        - `policy_name`: If policy name is defined then open page to edit the policy.
        Otherwise, consider that we are at the needed page. String.
        - `critical`: Severity incident as given in the wep page. String.
        - `high`: Severity incident as given in the wep page. String.
        - `medium`: Severity incident as given in the wep page. String.
        - `low`: Severity incident as given in the wep page. String.
        - `submit`: If True, press Submit button. Boolean.

        Note: setting with lower severity can inherit action from higher severity.
        eg 'high' inherit from 'critical', 'medium' inherit from 'high' and so on.

        Return:
        None

        Examples:
        | Dlp Policy Configure Severity Settings |
        | ... | critical=quarantine |
        | ... | high=quarantine |
        | ... | medium=deliver |
        | ... | low=deliver |
        | ... | submit=${True} |

        | Dlp Policy Configure Severity Settings |
        | ... | critical=drop |
        | ... | high=quarantine |
        | ... | medium=Default Action |
        | ... | low=deliver |
        | ... | submit=${True} |

        | Dlp Policy Configure Severity Settings |
        | ... | critical=quarantine |
        | ... | high=Inherit Action from Critical Severity Incident |
        | ... | medium=Inherit Action from High Severity Incident |
        | ... | low=Inherit Action from Medium Severity Incident |
        | ... | submit=${False} |
        """
        self._info('Configuring severity settings.')
        self._open_edit_policy_page(policy_name)
        if critical:
            self.select_from_list(SEVERITY_DD('critical'), critical)
        if high:
            self.select_from_list(SEVERITY_DD('high'), high)
        if medium:
            self.select_from_list(SEVERITY_DD('medium'), medium)
        if low:
            self.select_from_list(SEVERITY_DD('low'), low)
        self._handle_submit(submit)

    def dlp_policy_configure_filter_message_tags(self,
                                                 policy_name=None,
                                                 apply_if=None,
                                                 msg_tags=None,
                                                 submit=True):
        """ This function limits DLP policy to given message tag(s).

        Parameters:
        - `policy_name`: If policy name is defined then open page to edit the policy.
        Otherwise, consider that we are at the needed page. String.
        - `apply_if`: Possible values: 'present' or 'absent'. String.
        - `msg_tags`: Message tags. List of values or String of comma-separated values.
        Pass ${EMPTY} to clear the text-field.
        - `submit`: If True, press Submit button. Boolean.

        Return:
        None

        Examples:
        | Dlp Policy Configure Filter Message Tags |
        | ... | policy_name=Advanced Policy2 |
        | ... | apply_if=present |
        | ... | msg_tags=tag1,tag2 |
        | ... | submit=${True} |

        | @{mtags}  Set Variable  tag2  tag1 |
        | Dlp Policy Configure Filter Message Tags |
        | ... | policy_name=Advanced Policy1 |
        | ... | apply_if=absent |
        | ... | msg_tags=${mtags} |
        | ... | submit=${True} |

        | Dlp Policy Configure Filter Message Tags |
        | ... | policy_name=Advanced Policy1 |
        | ... | apply_if=absent |
        | ... | msg_tags=${EMPTY} |
        | ... | submit=${True} |
        """
        self._info('Configuring filter message tags')
        self._open_edit_policy_page(policy_name)
        if not self._is_visible(MSG_TAGS_APPLY_DD):
            self.click_element(FILTER_MESSAGE_TAGS_LINK, "don't wait")
        if apply_if:
            if apply_if.lower() == 'present':
                self.select_from_list(MSG_TAGS_APPLY_DD, "label=present")
            elif apply_if.lower() == 'absent':
                self.select_from_list(MSG_TAGS_APPLY_DD, "label=absent")
        if msg_tags is not None:
            self.input_text(MSG_TAGS_TB, self._convert_list_to_string(msg_tags))
        self._handle_submit(submit)

    def dlp_policy_configure_filter_senders_and_recipients(self,
                                                           policy_name=None,
                                                           rcpt_apply_if=None,
                                                           recipients=None,
                                                           sender_apply_if=None,
                                                           senders=None,
                                                           submit=True):
        """ This function limits DLP policy for the messages with given recipients and senders.

        Parameters:
        - `policy_name`: If policy name is defined then open page to edit the policy.
        Otherwise, consider that we are at the needed page. String.
        - `rcpt_apply_if`: Apply policy if the mail is received or not received
        from  the given recipients. Possible values: 'Is', 'Is Not'. String.
        - `recipients`: List of recipents. List or String of comma-separated values.
        Pass ${EMPTY} to clear the text-field.
        - `sender_apply_if`: Apply policy if the mail is sent top or not sent to the
        given senders. Possible values: 'Is', 'Is Not'. String.
        - `senders`: List of senders. List or String of comma-separated values.
        Pass ${EMPTY} to clear the text-field.
        - `submit`: If True, press Submit button. Boolean.

        Return:
        None

        Examples:
        | Dlp Policy Configure Filter Senders And Recipients |
        | ... | policy_name=My Policy |
        | ... | rcpt_apply_if=is |
        | ... | recipients=me@mail.qa,you@mail.qa |
        | ... | sender_apply_if=is not |
        | ... | senders=they@mail.qa,another@mail.qa |
        | ... | submit=${False} |

        | Dlp Policy Configure Filter Senders And Recipients |
        | ... | rcpt_apply_if=is not |
        | ... | recipients=${EMPTY} |
        | ... | sender_apply_if=is |
        | ... | senders={EMPTY} |
        | ... | submit=${True} |
        """
        self._info('Configuring filter sender and recipients.')
        self._open_edit_policy_page(policy_name)
        if not self._is_visible(RCPT_APPLY_IF_DD):
            self.click_element(FILTER_SEND_RECP_LINK, "don't wait")
        self._handle_is_and_isnot(RCPT_APPLY_IF_DD, rcpt_apply_if)
        if recipients is not None:
            self.input_text(RCPTS_TA, self._convert_list_to_string(recipients))
        self._handle_is_and_isnot(SENDER_APPLY_IF_DD, sender_apply_if)
        if senders is not None:
            self.input_text(SENDERS_TA, self._convert_list_to_string(senders))
        self._handle_submit(submit)

    def _add_classifier_rule(self, raw_rule, rule_indx=0):
        """
        `raw_rule`: string with key:value separated by comma. Will be converted to RecursiveCfgHolder.

        Rules explained(allowed keys):
        - 'rule_type': should be one of the following(case sensitive!!!):
        'Words or Phrases', 'Regular Expression', 'Dictionary', 'Entity'
        - 'words_phrases': List of expressions or comma-separated string. List or String.
        - 'regex_pattern': String.
        - 'dict_name': select option, either one of the custom or predefined dictionaries. String.
        - 'entity_name': select option. String.
        - 'exclude_pattern': String.
        - 'weight': String.
        - 'max_score': String.
        """
        rule = self._convert_to_cfgholder(raw_rule)
        if rule.rule_type:
            self.select_from_list(RULE_TYPE_DD(rule_indx), rule.rule_type)
        if rule.rule_type == "Words or Phrases" and rule.words_phrases:
            self.input_text(INCLUDE_PAT_LOC(rule_indx),
                            self._convert_list_to_string(rule.words_phrases))
        if rule.rule_type == "Regular Expression" and rule.regex_pattern:
            self.input_text(INCLUDE_PAT_LOC(rule_indx), rule.regex_pattern)
        if rule.rule_type == "Dictionary" and rule.dict_name:
            self.select_from_list(INCLUDE_PAT_LOC(rule_indx), rule.dict_name)
        if rule.rule_type == "Entity" and rule.entity_name:
            self.select_from_list(INCLUDE_PAT_LOC(rule_indx), rule.entity_name)
        if rule.rule_type != "Words or Phrases" and rule.exclude_pattern:
            self.input_text(EXCLUDE_PAT_LOC(rule_indx), rule.exclude_pattern)
        if rule.weight:
            self.input_text(WEIGHT_TB(rule_indx), rule.weight)
        if rule.max_score:
            self.input_text(MAX_SCORE_TB(rule_indx), rule.max_score)

    def dlp_policy_configure_content_matching_classifier(self,
                                                         policy_name=None,
                                                         match_option=None,
                                                         add_classifiers=None,
                                                         delete_classifiers=None,
                                                         enable_classifiers=None,
                                                         disable_classifiers=None,
                                                         submit=True):
        """
        This function is used to add content matching classifier for the DLP policy.
        In order to add(create) or modify custom content matching classifier use
        'Dlp Policy Create Classifier' keyword.

        Parameters:
        - `policy_name`: If policy name is defined then open page to edit the policy.
        Otherwise, consider that we are at the needed page. String.
        - `match_option`: Select option from values 'All', 'Any'. String.
        - `add_classifiers`: Classifiers to add (from drop-down except of "Create a classifier" option).
        List or String of comma-separated values.
        - `delete_classifiers`: Classifiers to delete from table of classifiers(blades) that are
        assigned to the DLP policy. List or String of comma-separated values.
        - `enable_classifiers`: Classifiers to be enabled(uncheck 'Not' option).
        List or String of comma-separated values.
        - `disable_classifiers`: Classifiers to be disabled(check 'Not' option).
        List or String of comma-separated values.
        - `submit`: If True, press Submit button. Boolean.

        Return:
        None

        Examples:
        | Dlp Policy Configure Content Matching Classifier |
        | ... | match_option=Any |
        | ... | add_classifiers=ABA Routing Numbers,Canada Social Insurance Number,Corporate Financials |
        | ... | submit=${True} |

        | Dlp Policy Configure Content Matching Classifier |
        | ... | policy_name=${custom_policy_with_predefined_blade} |
        | ... | match_option=All |
        | ... | delete_classifiers=Canada Social Insurance Number |
        | ... | disable_classifiers=ABA Routing Numbers |
        | ... | submit=${True} |
        """
        self._info('Configuring content matching classifiers')
        self._open_edit_policy_page(policy_name)
        if add_classifiers is not None:
            for cls in self._convert_to_tuple(add_classifiers):
                self.select_from_list(CLASSIFIER_LOC, cls)
                self.click_button(CLASSIFIER_ADD_BUTTON, "don't wait")
        if match_option:
            self.select_from_list(CLASSIFIER_MATCH, match_option.title())
        if delete_classifiers is not None:
            for cls in self._convert_to_tuple(delete_classifiers):
                try:
                    self.click_element(CLASSIFIER_SUBTABLE_DELETE_LINK(cls),
                                       "don't wait")
                except guiexceptions.SeleniumClientException:
                    self._warn('Could not delete blade "%s"' % cls)
        if enable_classifiers is not None:
            for cls in self._convert_to_tuple(enable_classifiers):
                try:
                    self._unselect_checkbox \
                        (CLASSIFIER_SUBTABLE_MARK_NOT_LINK(cls))
                except guiexceptions.SeleniumClientException:
                    self._warn('Could not check blade "%s"' % cls)
        if disable_classifiers is not None:
            for cls in self._convert_to_tuple(disable_classifiers):
                try:
                    self._select_checkbox \
                        (CLASSIFIER_SUBTABLE_MARK_NOT_LINK(cls))
                except guiexceptions.SeleniumClientException:
                    self._warn('Could not check blade "%s"' % cls)
        self._handle_submit(submit)

    def dlp_policy_create_classifier(self,
                                     policy_name=None,
                                     blade_name=None,
                                     description=None,
                                     proximity=None,
                                     min_total_score=None,
                                     rules=None,
                                     submit=True):
        """
        This function is used to create custom classifier for the DLP policy.

        Parameters:
        - `policy_name`: If policy name is defined then open page to edit the policy.
        Otherwise, consider that we are at the needed page. String.
        - `blade_name`: Defines name of the classifier(blade). String
        Otherwise, consider that we are at the needed page. String.
        - `description`: The description of the classifier. String.
        - `proximity`: Defines proximity of characters, Accepts digits input. String
        - `min_total_score`: Defines the minimum total score. Accepts digits input. String
        - `rules`: List of riles (which are dictionaries).
        Each dictionary may contain following keys:
        'rule_type', 'words_phrases', 'regex_pattern', 'dict_name', 'entity_name',
        'exclude_pattern', 'weight', 'max_score'
        - `submit`: If True, press Submit button. Boolean.

        Rules explained(allowed keys):
        - 'rule_type': should be one of the following(case sensitive!!!):
        'Words or Phrases', 'Regular Expression', 'Dictionary', 'Entity'
        - 'words_phrases': List of expressions or comma-separated string. List or String.
        - 'regex_pattern': String.
        - 'dict_name': select option, either one of the custom or predefined dictionaries. String.
        - 'entity_name': select option. String.
        - 'exclude_pattern': String.
        - 'weight': String.
        - 'max_score': String.

        Return:
        None

        Examples:
        | ${rule1} | Set Variable | rule_type:Words or Phrases,words_phrases:test1 |
        | ${rule2} | Set Variable | rule_type:Dictionary,dict_name:d2 |
        | @{rules} | Set Variable | ${rule1} | ${rule2} |
        | Dlp Policy Create Classifier |
        | ... | policy_name=Custom Policy With Basic Settings |
        | ... | blade_name=blade |
        | ... | description=blade description |
        | ... | rules=${rules} |
        | ... | submit=${True} |

        | Dlp Policy Create Classifier |
        | ... | blade_name=custom blade |
        | ... | description=my custom blade |
        | ... | rules=${rules1}, ${rules2} |
        """
        self._info('Create custom content matching classifier')
        self._open_edit_policy_page(policy_name)
        self.select_from_list(CLASSIFIER_LOC, 'Create a Classifier')
        self.click_button(CLASSIFIER_ADD_BUTTON)
        if blade_name is not None:
            self.input_text(CONTENT_MATCHING_CLASSIFIER_NAME, blade_name)
        if description is not None:
            self.input_text(CLASSIFIER_DESCRIPTION, description)
        if proximity is not None:
            self.input_text(PROXIMITY, proximity)
        if min_total_score is not None:
            self.input_text(MIN_TOTAL_SCORE, min_total_score)
        rule_indx = 0
        for rule in self._convert_to_tuple(rules):
            self._add_classifier_rule(rule, rule_indx)
            if (rule_indx + 1) < len(rules):
                rule_indx += 1
                self.click_button(ADD_RULE_BUTTON)
        self._click_submit_button()
        self._handle_submit(submit)

    def dlp_custom_dictionary_add(self,
                                  name,
                                  terms=None):
        """This function adds custom DLP dictionaries.

        Parameters:
        - `name`: Name of the custom dictionary. String.
        - `terms`: List of terms to be added in the custom dictionary.
        List or String of comma-separated values.

        Return:
        None

        Examples:
        | Dlp Custom Dictionary Add |
        | ... | Custom Dictionary Name |
        | ... | terms=andriy,petro,ivan |
        """
        self._info('Add custom DLP dictionary "%s"' % name)
        self._open_dlp_dict_page()
        self.click_button(ADD_CUST_DLP_DICT)
        self.input_text(CUSTOM_DLP_DICT_NAME, name)
        if terms is not None:
            self.input_text(CUSTOM_DLP_DICT_TERMS,
                            '\n'.join(self._convert_to_tuple(terms)))
            self.click_button(ADD_TERMS_BUTTON, "don't wait")
        self.click_button(ADD_CUST_DICT_BTN)

    def dlp_custom_dictionary_edit(self,
                                   name,
                                   change_name=None,
                                   add_terms=None,
                                   delete_terms=None):
        """This function edits custom DLP dictionary.

        Parameters:
        - `name`: Name of the custom dictionary to be edited. String.
        - `add_terms`: List of terms to be added in the custom dictionary.
        List or String of comma-separated values.
        - `delete_terms`: List of terms to be added in the custom dictionary.
        List or String of comma-separated values.

        Return:
        None

        Examples:
        | Dlp Custom Dictionary Edit |
        | ... | Custom Dictionary Name |
        | ... | change_name=boo |
        | ... | add_terms=term1,term2 |
        | ... | delete_terms=andriy,ivan |

        | Dlp Custom Dictionary Edit |
        | ... | boo |
        | ... | add_terms=term3,term4 |
        """
        self._info('Edit custom DLP dictionary "%s"' % name)
        self._open_dlp_dict_page()
        row = self._get_entity_indx(name, CUST_DICT_FIRST_ROW, CUST_DICT_ROW, 1)
        self.click_element(CUST_EDIT_LINK(row))
        if change_name is not None:
            self.input_text(CUSTOM_DLP_DICT_NAME, change_name)
        if add_terms:
            self.input_text(CUSTOM_DLP_DICT_TERMS,
                            '\n'.join(self._convert_to_tuple(add_terms)))
            self.click_button(ADD_TERMS_BUTTON, "don't wait")
        if delete_terms:
            for term in self._convert_to_tuple(delete_terms):
                term_indx = self._get_entity_indx(term,
                                                  CUST_TERM_FIRST_ROW,
                                                  CUST_TERM_ROW,
                                                  1)
                self.click_element(CUST_TERM_DEL_LINK(term_indx),
                                   "don't wait")
        self.click_button(ADD_CUST_DICT_BTN)

    def dlp_custom_dictionary_delete(self, name):
        """
        This function deletes custom DLP dictionaries.

        Parameters:
        - `name`: Name of the custom dictionary. String.

        Return:
        None

        Examples:
        | Dlp Custom Dictionary Delete | Dictionary Name |
        """
        self._info('Delete custom DLP dictionary "%s"' % name)
        self._open_dlp_dict_page()
        row = self._get_entity_indx(name, CUST_DICT_FIRST_ROW, CUST_DICT_ROW, 1)
        self._info("row: %s  CUST_DICT_FIRST_ROW:%s  CUST_DICT_ROW %s " \
                   % (row, CUST_DICT_FIRST_ROW, CUST_DICT_ROW))
        self.click_element(CUST_DICT_DEL_LINK(row), "don't wait")
        self.click_button(CUSTDICT_DELETE_CONFIRM)

    def dlp_custom_dictionary_import(self,
                                     import_local_file=None,
                                     import_appliance_file=None,
                                     encoding=None,
                                     import_name=None,
                                     more_terms=None):
        """
        This function imports custom DLP dictionaries from local machine or from the appliance.

        Parameters:
        - `import_local_file`: Path on the local computer to import from. String.
        - `import_appliance_file`: Config file name on the IronPort Appliance to import from. String.
        - `encoding`: Encoding to be used. String.
        - `import_name`: set new name to the dictionary. String.
        - `more_terms`: List of more custom terms to be added to the imported dictionary.
        List or String of comma-separated values.

        Return:
        None

        Examples:
        | Dlp Custom Dictionary Import |
        | ... | import_appliance_file=d2 |
        | ... | encoding=Unicode (UTF-8) |
        | ... | import_name=d22 |
        | ... | more_terms=b1,b2,b3 |

        | Dlp Custom Dictionary Import |
        | ... | import_local_file=/home/me/Documents/dlp.txt |
        | ... | import_name=from_local |
        """
        self._info('Import custom DLP dictionary.')
        self._open_dlp_dict_page()
        self.click_button(CUSTDICT_IMPORT)
        if import_local_file is not None:
            self.click_element(CUST_IMPORT_LOCAL_RB, "don't wait")
            self.input_text(IMPORT_LOCAL_PATH_TB, import_local_file)
        if import_appliance_file is not None:
            self.click_element(CUST_IMPORT_DUT_RB, "don't wait")
            self.select_from_list \
                (CUST_IMPORT_DUT_LB, "label=%s" % import_appliance_file)
        if encoding:
            self.select_from_list(ENCODING_DD, "label=%s" % encoding)
        self.click_button(CUSTDICT_NEXT)
        if import_name:
            self.input_text(CUSTOM_DLP_DICT_NAME, import_name)
        if more_terms is not None:
            self.input_text(CUSTOM_DLP_DICT_TERMS,
                            '\n'.join(self._convert_to_tuple(more_terms)))
            self.click_button(ADD_TERMS_BUTTON, "don't wait")
        self.click_button(IMPORT_SUBMIT_BTN, None)

    def dlp_custom_dictionary_export(self,
                                     dictionary_name=None,
                                     file_name=None,
                                     export_location=None,
                                     encoding=None):
        """This function exports custom DLP dictionaries to local machine or to the appliance.
        Parameters:
        - `dictionary_name`: name of the dictionary to export. String.
        - `file_name`: Name of the file to export. String.
        - `export_location`: Where to export. Possible values: 'local', 'appliance'. String.
        - `encoding`: What encoding to use. As they appear in WUI. String.

        Note: export action does not require commit.

        Return:
        None

        Examples:
        | Dlp Custom Dictionary Export |
        | ... | dictionary_name=d1 |
        | ... | file_name=d2 |
        | ... | export_location=appliance |
        | ... | encoding=US-ASCII |

        | Dlp Custom Dictionary Export |
        | ... | dictionary_name=d2 |
        | ... | file_name=d3 |
        | ... | export_location=local |
        """
        self._info('Export custom DLP dictionary.')
        self._open_dlp_dict_page()
        self.click_button(CUSTDICT_EXPORT)
        if dictionary_name:
            self.select_from_list(DICT_TO_EXPORT_DD, dictionary_name)
        if file_name:
            self.input_text(EXPORT_FILENAME, file_name)
        if 'local' in export_location.lower():
            self.click_element(EXPORT_LOCAL_RB, "don't wait")
        if 'appliance' in export_location.lower():
            self.click_element(EXPORT_SERVER_RB, "don't wait")
        if encoding:
            self.select_from_list(ENCODING_DD, encoding)
        self._click_submit_button()
        # TODO: Need to handle file saving option
        # suggest to reuse code from IAF2 wuicontrol.py
        # (used in iaf's ph76/packetcapture.py)

    def dlp_custom_dictionary_get_all(self):
        """
        This function gets the list of names of custom DLP dictionaries.

        Parameters:
        None

        Return:
        List of configured custom DLP dictionaries. List.

        Examples:
        | @{dicts} | Dlp Custom Dictionary Get All |
        """
        self._info('Getting all configured custom DLP dictionaries')
        self._get_list_of_dictionaries(CUSTOM_DLP_DICT_ROWS)

    def dlp_custom_dictionary_get_terms(self, name):
        """This function edits custom DLP dictionary.

        Parameters:
        - `name`: Name of the custom dictionary to fetch terms from. String.

        Return:
        List of terms. List.

        Examples:
        | @{terms} | Dlp Custom Dictionary Get Terms | Dict Name |
        """
        self._info('Edit custom DLP dictionary "%s"' % name)
        self._open_dlp_dict_page()
        row = self._get_entity_indx(name, CUST_DICT_FIRST_ROW, CUST_DICT_ROW, 1)
        self.click_element(CUST_EDIT_LINK(row))
        try:
            rows = int(self.get_matching_xpath_count(CUST_TERM_FIRST_ROW))
        except guiexceptions.SeleniumClientException:
            return []
        terms = []
        for r in range(1, rows + 1):
            _indx = CUST_TERM_ROW % r
            term = self.get_text('%s/td[1]' % _indx)
            terms.append(term)
        return terms

    def dlp_predefined_dictionary_get_all(self):
        """
        This function gets the list of names of predefined DLP dictionaries.

        Parameters:
        None

        Return:
        List of configured predefined DLP dictionaries. List.

        Examples:
        | @{dicts} | Dlp Predefined Dictionary Get All |
        """
        self._info('Getting all available predefined DLP dictionaries')
        self._get_list_of_dictionaries(PREDEFINED_DLP_DICT_ROWS)

#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/manager/mailpolicies.py#1 $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

DROP_DOWN_DICT = {"policy_order_list": 'name=rpolicyNewIdx',
                  "policy_ldap_query_list": "name=ldapQuery",

                  "av_scanning_action": "name=clean",
                  "av_action": "name=%s_action",

                  "as_action": "%s_action",
                  "as_subj_add": "id=%sSubjectAction",

                  "cf_enable_list": "name=enableSf",

                  "vof_ext_types": "id=pulldown_type",

                  "dlp_enable_list": "id=enable_dlp",
                  }
RADIO_BUTTON_DICT = {"find_recipient": "name=findRS",
                     "find_sender": "//input[@name='findRS' and @value='S']",
                     "policy_sender": "//input[@name='rpolicyUserType' and @value='Sender']",
                     "policy_recipient": "//input[@name='rpolicyUserType' and @value='Recipient']",
                     "policy_email_addrs": "//input[@name='listRadio' and @value='addressList']",
                     "policy_ldap_query": "//input[@name='listRadio' and @value='ldapQuery']",

                     "av_custom": "id=enable_avYes",
                     "av_default": "id=enable_avDefault",
                     "av_disable": "id=enable_avNo",

                     "av_archive_no": "id=%s_archive0",
                     "av_archive_yes": "id=%s_archive1",

                     "av_subj_no": "id=%s_subj_no",
                     "av_subj_prepend": "id=%s_subj_pre",
                     "av_subj_append": "id=%s_subj_app",

                     "av_hdr_no": "id=%s_hdr_no",
                     "av_hdr_yes": "id=%s_hdr_yes",

                     "as_default": "id=default_as",
                     "as_disable": "id=no_as",

                     "as_scanning_type": "id=%s_as",

                     "as_archive_no": "id=%s_archive_no",
                     "as_archive_yes": "id=%s_archive_yes",

                     "as_enable_no": "id=disable_%s",
                     "as_enable_yes": "id=enable_%s",

                     "modify_rcpt_no": "id=%s_rbno",
                     "modify_rcpt_yes": "id=%s_rbyes",

                     "send_alt_host_no": "id=%s_altno",
                     "send_alt_host_yes": "id=%s_altyes",

                     "as_threshold_default": "id=recommended_CASE",
                     "as_threshold_custom": "id=custom_CASE",

                     "vof_custom": "name=enable_vof",
                     "vof_default": "//input[@name='enable_vof' and @value='Default']",
                     "vof_disable": "//input[@name='enable_vof' and @value='No']",
                     }
TEXT_BOX_DICT = {
    "policy_name_tb": "name=rpolicyName",
    "policy_email_addr_tb": "id=addressList",
    "policy_ldap_group_tb": "name=ldapGroup",
    "find_email_addr": "name=findEmail",

    "av_subj": "name=%s_subject_text",
    "av_hdr": "name=%s_header_name",
    "av_hdr_val": "name=%s_header_text",

    "av_other": "name=%s_notify_other_text",
    "av_notify_subj": "name=%s_notify_subject",

    "as_alt_host": "name=%sDivertHost",
    "as_subj": "name=%sSubjectText",
    "as_hdr": "name=%sHeaderName",
    "as_hdr_val": "name=%sHeaderText",
    "as_alt_rcpt": "name=%sAltRcptTo",

    "as_spam_score": "name=threshold_pos_CASE",
    "as_suspected_score": "name=threshold_sus_CASE",

    "vof_add_ext": "name=add_type_field",

    "mod_address": "name=%s_alt_rcpt_to",
    "alt_host": "name=%s_alt_mailhost",
}
TABLE_DICT = {"policy_table": "//table[@class='cols']",
              "vof_file_exts_table": "//table[@class='cols']",
              }
BUTTON_DICT = {
    "policy_user_add_button": "//input[@id='btnAdd']",
    "policy_delete_confirm": '//button[@type="button"]',
    "find_policy_button": "//input[@value='Find Policies']",
    "submit_button": 'xpath=//input[@class="submit"]',

    "vof_add_ext": 'xpath=//input[@id="AddExtension"]',

}
CHECKBOX_DICT = {"av_sophos": "id=Sophos",
                 "av_mcafee": "id=McAfee",

                 "av_drop_attachments": "xpath=//input[@id='drop_attachments']",
                 "av_insert_xheader": "id=include_X_header",

                 "av_sender": "id=%s_generic_sender",
                 "av_recipient": "id=%s_generic_recipient",
                 "av_other": "id=%s_generic_other",

                 "cf_filter_name": "//input[@name='sfEnableItem[]' and @value='%s']",

                 "dlp_enable_all": "name=enable_all",
                 "dlp_policy_name": "//table[@class='cols']/tbody/tr[2]/td[2]/input"
                 }
ACTION_MAP = {'scan_virus': "Scan for Viruses only",
              'scan_repair': "Scan and Repair viruses",
              'deliveras_is': "Deliver As Is",
              'deliveras_attachment_plain': "Deliver as Attachment (text/plain) to New Message",
              'deliveras_attachment_msg': "Deliver as Attachment (message/rfc822) to New Message",
              'drop': "Drop Message",
              'quarantine': "Quarantine",

              'prepend': "Prepend",
              'append': "Append",
              'no': "None",

              'as_drop': 'Drop',
              'as_deliver': 'Deliver',
              'as_bounce': 'Bounce',
              'as_quarantine': 'Spam Quarantine',

              "cf_default": "Enable Content Filters (Inherit default mail policy settings)",
              "cf_custom": "Enable Content Filters (Customize settings)",
              "cf_disable": "Disable Content Filters",

              "obf_default": "Enable Outbreak Filtering (Inherit default mail policy settings)",
              "obf_custom": "Enable Outbreak Filtering (Customize settings)",
              "obf_disable": "Disable Outbreak Filtering",

              "dlp_default": "Enable DLP (Inherit default mail policy settings)",
              "dlp_custom": "Enable DLP (Customize settings)",
              "dlp_disable": "Disable DLP",
              }
DLP_ENABE_DD = "id=enable_dlp"
DLP_ENABLE_ALL_CB = "name=enable_all"
DLP_POLICY_TABLE = "//table[@class='cols']"
DLP_POLICY_ENABLE_CB = lambda row: "//table[@class='cols']/tbody/tr[%d]/td[2]/input" % ((row + 1),)
OBF_ENABLE_DD = "id=enable_AOF"
QUARANTINE_TL_DD = "id=quarantine_gtl"
MQR_VIRAL_NUM_TB = "id=virus_retention"
MQR_VIRAL_UNIT_DD = "id=virus_retention_unit"
MQR_OTHER_NUM_TB = "id=threat_retention"
MQR_OTHER_UNIT_DD = "id=threat_retention_unit"
ENABLE_MSG_MOD_CB = "xpath=//input[@id='enable_threat_options']"
MSG_MOD_THREAT_LEVEL_DD = "id=modify_gtl"
MSG_MOD_SUB_POS_DD = "id=threat_subject_action"
MSG_MOD_SUB_TB = "id=threat_subject_text"
URL_ACTION_MAP = {"enable only for unsigned messages (recommended)":
                      'unsigned', "enable for all messages": "all", "disable": "none"}
URL_REWRITE_ACTION_RB = lambda URL_ACTION: "rewrite_%s" % URL_ACTION_MAP[URL_ACTION]
BYPASS_DOMAIN_TA = "xpath=//textarea[@id='preserve_domains']"
THREAT_DISCLAIMER_DD = "id=threat_disclaimer_resource"
OBF_EXT_TYPES_DD = "id=pulldown_type"
OBF_ADD_EXT_TB = "name=add_type_field"
OBF_ADD_EXT_BTN = 'xpath=//input[@id="AddExtension"]'
POL_LINK = lambda row: '//table[@class="cols"]//tr[%s]//td[2]/a' % row
CHECKBOX_LOC = lambda row: "//div[@id='%s']//tr[%d]//input[@type='checkbox']" \
                           % (locator, row)
DEL_FILE_EXT_IMG = lambda row, col: \
    'xpath=//table[@class="cols"]//tr[%s]//td[%s]/img' % (row, col)
OBF_FILE_EXTS_TBL = "//table[@class='cols']"
BUTTON_LOCATOR = lambda row: "//div[@id='%s']//tr[%d]/td[2]/label" \
                             % (ROLES_DIV, row)
CB_LOC = lambda row: "//div[@id='%s']//tr[%d]/td/input" % (ROLES_DIV, row)
OK_BUTTON = "yui-gen7-button"

BYPASS_EXPAND_LINK = "//table[@class='pairs']/tbody/tr[3]/th/a/span/img"
SERVICE_DICT = {
    "antispam": "Anti-Spam",
    "antivirus": "Anti-Virus",
    "content_filters": "Content Filters",
    "vof": "Virus Outbreak Filters",
    "dlp": "DLP",
    "obf": "Outbreak Filters",
}

ROLES_DIV = 'role_ids_dialog_container'
CUSTOM_ROLES_LINK = "role_ids_dialog_link"
DIV = lambda div: "//div[@id='%s']//input[@type='checkbox']" % div


class mailpolicies(GuiCommon):
    """Interaction class for ESA WUI Mail Policies -> Incoming Mail
       Policies/Outgoing Mail Policies pages.
    """

    def get_keyword_names(self):
        return ['mailpolicy_add',
                'mailpolicy_edit',
                'mailpolicy_delete',
                'mailpolicy_find',
                'virus_obj_create',
                'mailpolicy_edit_antivirus',
                'mailpolicy_edit_antispam',
                'spam_obj_create',
                'mailpolicy_edit_contentfilters',
                'mailpolicy_edit_vof',
                'mailpolicy_edit_dlp',
                ]

    def _click_radiobutton(self, rb_key, substitute=None):
        self._info('Selecting by clicking radio button %s' % rb_key)
        if substitute:
            rb_locator = RADIO_BUTTON_DICT[rb_key] % substitute
        else:
            rb_locator = RADIO_BUTTON_DICT[rb_key]
        self._click_radio_button(rb_locator)

    def _click_checkbox(self, cb_key, check, substitute=None):
        self._info('Clicking checkbox %s' % cb_key)
        self._info(check)
        if substitute:
            cb_locator = CHECKBOX_DICT[cb_key] % substitute
        else:
            cb_locator = CHECKBOX_DICT[cb_key]
        if check:
            if not self._is_checked(cb_locator):
                self.select_checkbox(cb_locator)
        else:
            self.unselect_checkbox(cb_locator)

    def _onclickevent_checkbox(self, cb_key, check, substitute=None):
        self._info('Clicking Checkbox for onlclick event %s' % cb_key)
        if substitute:
            cb_locator = CHECKBOX_DICT[cb_key] % substitute
        else:
            cb_locator = CHECKBOX_DICT[cb_key]
        if not self._is_checked(cb_locator) and check:
            self.click_element(cb_locator, "don't wait")
        if self._is_checked(cb_locator) and not check:
            self.click_element(cb_locator, "don't wait")

    def _select_option(self, option_name, option_list_key, substitute=None):
        self._info('Selecting option %s' % option_name)
        if substitute:
            option_list_id = DROP_DOWN_DICT[option_list_key] % substitute
        else:
            option_list_id = DROP_DOWN_DICT[option_list_key]
        current_options = self.get_list_items(option_list_id)
        if isinstance(option_name, int):
            try:
                select_this = current_options[option_name - 1]
            except IndexError:
                raise ValueError, 'Wrong option name - "%s"' % (option_name,)
        else:
            for optn in current_options:
                if option_name in optn:
                    select_this = optn
                    break
            else:
                raise ValueError, '"%s" Option is not found' % (option_name,)
        self._info('Selected the option "%s"' % select_this)
        self.select_from_list(option_list_id, select_this)

    def _fill_policy_page(self, policy_name, order_of_policy, sender_email_addr_list,
                          rcpt_email_addr_list, sender_ldap_grp_query_dict, rcpt_ldap_grp_query_dict):
        """This function fills the details in policy page after clicking
         add policy button in incoming/outgoing mail policies page.
        """
        if policy_name:
            self.input_text(TEXT_BOX_DICT["policy_name_tb"], text=policy_name)
        if order_of_policy:
            self._select_option(order_of_policy, "policy_order_list")
        if sender_email_addr_list:
            self._click_radiobutton("policy_sender")
            self._add_email_addr_entries(sender_email_addr_list)
        if rcpt_email_addr_list:
            self._click_radiobutton("policy_recipient")
            self._add_email_addr_entries(rcpt_email_addr_list)
        if sender_ldap_grp_query_dict:
            self._click_radiobutton("policy_sender")
            self._add_ldap_group_queries(sender_ldap_grp_query_dict)
        if rcpt_ldap_grp_query_dict:
            self._click_radiobutton("policy_recipient")
            self._add_ldap_group_queries(rcpt_ldap_grp_query_dict)

    def _add_email_addr_entries(self, email_addr_list):
        """ This function adds email entries in policy page.
        """
        self._click_radiobutton("policy_email_addrs")
        self.input_text(TEXT_BOX_DICT["policy_email_addr_tb"],
                        email_addr_list)
        self.click_button(BUTTON_DICT["policy_user_add_button"], "don't wait")
        self._info('Clicked "Add" button to add email address entries')
        self._check_action_result()

    def _add_ldap_group_queries(self, ldap_grp_query_dict):
        """ This function adds ldap group queries as user entries in
            policy page.
        """
        self._info('Adding LDAP group query entries')
        self._click_radiobutton("policy_ldap_query")
        for (group_name, query) in ldap_grp_query_dict.items():
            self.input_text(TEXT_BOX_DICT["policy_ldap_group_tb"], group_name)
            self._select_option(query, "policy_ldap_query_list")
            self.click_button(BUTTON_DICT["policy_user_add_button"], "don't wait")
            self._check_action_result()

    def _delete_policy(self, name):
        """ This function deletes a given mail policy.
        """
        (rowp, colp) = self._get_table_cell_index(name, TABLE_DICT["policy_table"])
        (rowd, cold) = self._get_table_cell_index("Delete", TABLE_DICT["policy_table"])
        if rowp is None:
            raise ValueError, '"%s" policy is not present' % (name,)
        del_col = cold + 1
        del_row = rowp + 1
        self.click_element('xpath=//table[@class="cols"]//tr[%s]//td[%s]/img' % \
                           (del_row, del_col), "don't wait")
        self.click_button(BUTTON_DICT["policy_delete_confirm"])
        self._info('Clicked "Delete" button in "Confirm Delete" pop-up')

    def _click_edit_policy_service(self, policy_name, service_name):
        (rowp, colp) = self._get_table_cell_index(policy_name, TABLE_DICT["policy_table"])
        (rowe, cole) = self._get_table_cell_index(service_name, TABLE_DICT["policy_table"])
        if rowp is None:
            raise ValueError, '"%s" policy is not present' % (policy_name,)
        edit_row = rowp + 1
        edit_col = cole + 1
        self.click_element('xpath=//table[@class="cols"]//tr[%s]//td[%s]/a' %
                           (edit_row, edit_col), "don't wait")
        self._info('Clicked edit "%s" service link for the policy: %s' % (service_name,
                                                                          policy_name))

    def _fill_policy_antivirus_page(self, enable_antivirus_scanning, antivirus_types=None,
                                    msg_scanning_dict=None, repaired_obj=None, encrypted_obj=None, unscannable_obj=None,
                                    infected_obj=None):
        if not set([enable_antivirus_scanning]) <= set(['custom', 'default', 'disable']):
            raise ValueError, '"%s" is invalid. Should custom or default or disable' \
                              % (enable_antivirus_scanning,)
        rb_key = "av_%s" % (enable_antivirus_scanning)
        self._click_radiobutton(rb_key)
        if not set(antivirus_types) <= set(['sophos', 'mcafee']):
            raise ValueError, '"%s" is invalid.' \
                              % (antivirus_types,)
        for av_engine in antivirus_types:
            cb_key = "av_%s" % av_engine
            self._click_checkbox(cb_key, True)
        if msg_scanning_dict:
            self._fill_msg_scanning_det(msg_scanning_dict)
        # repaired=safe, encrypted=enc, unscannable=unscan, infected=unsafe
        if repaired_obj:
            self._fill_av_actions(repaired_obj, "safe")
        if encrypted_obj:
            self._fill_av_actions(encrypted_obj, "enc")
        if unscannable_obj:
            self._fill_av_actions(unscannable_obj, "unscan")
        if infected_obj:
            self._fill_av_actions(infected_obj, "unsafe")
        self._click_submit_button()

    def _fill_msg_scanning_det(self, msg_scanning_dict):
        if msg_scanning_dict.has_key('action'):
            action = ACTION_MAP[msg_scanning_dict['action']]
            self._select_option(action, 'av_scanning_action')
        if msg_scanning_dict.has_key('drop_attachmets'):
            self._onclickevent_checkbox('av_drop_attachments', msg_scanning_dict['drop_attachmets'])
        if msg_scanning_dict.has_key('insert_xheader'):
            self._click_checkbox('av_insert_xheader', msg_scanning_dict['insert_xheader'])

    def _fill_av_actions(self, settings_obj, settings_type):
        if settings_obj.action:
            action = ACTION_MAP[settings_obj.action]
            self._select_option(action, 'av_action', settings_type)
        if settings_obj.archive:
            rb_key = 'av_archive_%s' % settings_obj.archive
            self._click_radiobutton(rb_key, settings_type)
        if settings_obj.modify_subj:
            rb_key = 'av_subj_%s' % settings_obj.modify_subj
            self._click_radiobutton(rb_key, settings_type)
        if settings_obj.subject_text:
            tb_name = TEXT_BOX_DICT['av_subj'] % settings_type
            self.input_text(tb_name, settings_obj.subject_text)
        if settings_obj.add_custom_header:
            rb_key = 'av_hdr_%s' % settings_obj.add_custom_header
            self._click_radiobutton(rb_key, settings_type)
        if settings_obj.custom_header:
            tb_name = TEXT_BOX_DICT['av_hdr'] % settings_type
            self.input_text(tb_name, settings_obj.custom_header)
        if settings_obj.custom_value:
            tb_name = TEXT_BOX_DICT['av_hdr_val'] % settings_type
            self.input_text(tb_name, settings_obj.custom_value)
        if settings_obj.notify_sender:
            self._onclickevent_checkbox('av_sender', settings_obj.notify_sender, settings_type)
        if settings_obj.notify_recipient:
            self._onclickevent_checkbox('av_recipient', settings_obj.notify_recipient, settings_type)
        if settings_obj.notify_others:
            self._onclickevent_checkbox('av_other', settings_obj.notify_others, settings_type)
        if settings_obj.notify_address:
            comma_sep_email_ids = settings_obj.notify_address
            tb_name = TEXT_BOX_DICT['av_other'] % settings_type
            self.input_text(tb_name, comma_sep_email_ids)
        if settings_obj.notify_subj:
            tb_name = TEXT_BOX_DICT['av_notify_subj'] % settings_type
            self.input_text(tb_name, settings_obj.notify_subj)
        if settings_obj.modify_rcpt:
            rb_key = 'modify_rcpt_%s' % settings_obj.modify_rcpt
            self._click_radiobutton(rb_key, settings_type)
        if settings_obj.mod_address:
            tb_name = TEXT_BOX_DICT['mod_address'] % settings_type
            self.input_text(tb_name, settings_obj.mod_address)
        if settings_obj.send_alt_host:
            rb_key = 'send_alt_host_%s' % settings_obj.send_alt_host
            self._click_radiobutton(rb_key, settings_type)
        if settings_obj.alt_host:
            tb_name = TEXT_BOX_DICT['alt_host'] % settings_type
            self.input_text(tb_name, settings_obj.alt_host)

    def _fill_policy_antispam_page(self, enable_antispam_scanning, scanning_type=None,
                                   spam_obj=None, enable_suspected_spam=None, suspected_spam_obj=None,
                                   enable_marketing_spam=None, marketing_spam_obj=None,
                                   threshold_setting=None, spam_score=None, suspected_spam_score=None):
        if not set([enable_antispam_scanning]) <= set(['custom', 'default', 'disable']):
            raise ValueError, '"%s" is invalid. Should custom or default or disable' \
                              % (enable_antispam_scanning,)
        if enable_antispam_scanning in ('default', 'disable'):
            rb_key = "as_%s" % enable_antispam_scanning
            self._click_radiobutton(rb_key)
        elif scanning_type == 'ipas':
            self._click_radiobutton("as_scanning_type", 'case')
        elif scanning_type == 'ipas_ims':
            self._click_radiobutton("as_scanning_type", 'ims')
        if spam_obj:
            self._fill_antispam_actions(spam_obj, "pos")
        if enable_suspected_spam == 'yes':
            self._click_radiobutton('as_enable_yes', "sus")
            if suspected_spam_obj:
                self._fill_antispam_actions(suspected_spam_obj, "sus")
        elif enable_suspected_spam == 'no':
            self._click_radiobutton('as_enable_no', "sus")
        if enable_marketing_spam == 'yes':
            self._click_radiobutton('as_enable_yes', "marketing")
            if marketing_spam_obj:
                self._fill_antispam_actions(marketing_spam_obj, "marketing")
        elif enable_marketing_spam == 'no':
            self._click_radiobutton('as_enable_no', "marketing")
        if threshold_setting:
            self._fill_spam_threshold_det(threshold_setting, spam_score,
                                          suspected_spam_score)
        self._click_submit_button()

    def _fill_antispam_actions(self, settings_obj, settings_type):
        if settings_obj.action:
            action = ACTION_MAP["as_%s" % settings_obj.action]
            self._select_option(action, 'as_action', settings_type)
        if settings_obj.archive:
            rb_key = 'as_archive_%s' % settings_obj.archive
            self._click_radiobutton(rb_key, settings_type)
        if settings_obj.alternate_host:
            tb_name = TEXT_BOX_DICT['as_alt_host'] % settings_type
            self.input_text(tb_name, settings_obj.alternate_host)
        if settings_obj.modify_subj:
            action = ACTION_MAP[settings_obj.modify_subj]
            self._select_option(action, 'as_subj_add', settings_type)
        if settings_obj.subject_text:
            tb_name = TEXT_BOX_DICT['as_subj'] % settings_type
            self.input_text(tb_name, settings_obj.subject_text)
        if settings_obj.custom_header:
            tb_name = TEXT_BOX_DICT['as_hdr'] % settings_type
            self.input_text(tb_name, settings_obj.custom_header)
        if settings_obj.custom_value:
            tb_name = TEXT_BOX_DICT['as_hdr_val'] % settings_type
            self.input_text(tb_name, settings_obj.custom_value)
        if settings_obj.alt_envelope_recipient:
            tb_name = TEXT_BOX_DICT['as_alt_rcpt'] % settings_type
            self.input_text(tb_name, settings_obj.alt_envelope_recipient)

    def _fill_spam_threshold_det(self, threshold_setting=None, spam_score=None,
                                 suspected_spam_score=None):
        rb_key = "as_threshold_%s" % threshold_setting
        self._click_radiobutton(rb_key)
        if spam_score:
            tb_name = TEXT_BOX_DICT['as_spam_score']
            self.input_text(tb_name, spam_score)
        if suspected_spam_score:
            tb_name = TEXT_BOX_DICT['as_suspected_score']
            self.input_text(tb_name, suspected_spam_score)

    def _fill_policy_contentfilters_page(self, enable_contentfilters, \
                                         enable_filter_names=None, disable_filter_names=None):
        if not set([enable_contentfilters]) <= set(['custom', 'default', 'disable']):
            raise ValueError, '"%s" is invalid. Should custom or default or disable' \
                              % enable_contentfilters
        action = ACTION_MAP["cf_%s" % enable_contentfilters]
        self._select_option(action, 'cf_enable_list')
        if enable_filter_names:
            for filter in enable_filter_names:
                self._click_checkbox("cf_filter_name", True, filter)
        if disable_filter_names:
            for filter in disable_filter_names:
                self._click_checkbox("cf_filter_name", False, filter)
        self._click_submit_button()

    def _fill_policy_vof_page(self, enable_vof, from_drop_down, file_ext_add_list=None, \
                              file_ext_del_list=None):
        if not set([enable_vof]) <= set(['custom', 'default', 'disable']):
            raise ValueError, '"%s" is invalid. Should custom or default or disable' \
                              % enable_vof
        rb_key = "vof_%s" % enable_vof
        self._click_radiobutton(rb_key)
        if from_drop_down and file_ext_add_list:
            for file_ext in file_ext_add_list:
                self._select_option("-- %s" % file_ext, "vof_ext_types")
                self.click_button(BUTTON_DICT["vof_add_ext"], None)
        elif file_ext_add_list:
            for file_ext in file_ext_add_list:
                self.input_text(TEXT_BOX_DICT["vof_add_ext"], file_ext)
                self.click_button(BUTTON_DICT["vof_add_ext"], None)
        if file_ext_del_list:
            del_col = 2
            for file_ext in file_ext_del_list:
                (rowf, colf) = self._get_table_cell_index(file_ext, TABLE_DICT["vof_file_exts_table"])
                self.click_element('//table[@class="cols"]//tr[%s]//td[%s]/img' % \
                                   ((rowf + 1), del_col), "don't wait")
        self._click_submit_button()

    def _fill_policy_obf_page(self, enable_obf, quarantine_threat_level=None, \
                              mqr_viral_attachments=None, mqr_other_threats=None, file_ext_add_list=None, \
                              extra_file_add_list=None, file_ext_del_list=None, enable_msg_modification=None, \
                              msg_mod_threat_level=None, msg_mod_sub_pos=None, msg_mod_sub=None, \
                              url_rewrite_action=None, domains_to_bypass=None, threat_disclaimer=None):

        if not set([enable_obf]) <= set(['custom', 'default', 'disable']):
            raise ValueError, '"%s" is invalid. Should custom or default or disable' \
                              % enable_obf
        action = ACTION_MAP["obf_%s" % enable_obf]
        self.select_from_list(OBF_ENABLE_DD, action)
        if quarantine_threat_level:
            self.select_from_list(QUARANTINE_TL_DD, quarantine_threat_level)
        if mqr_viral_attachments:
            self.input_text(MQR_VIRAL_NUM_TB, mqr_viral_attachments[0])
            self.select_from_list(MQR_VIRAL_UNIT_DD, mqr_viral_attachments[1])
        if mqr_other_threats and self._is_visible(MQR_OTHER_NUM_TB):
            self.input_text(MQR_OTHER_NUM_TB, mqr_other_threats[0])
            self.select_from_list(MQR_OTHER_UNIT_DD, mqr_other_threats[1])
        self.click_element(BYPASS_EXPAND_LINK, "don't wait")
        if file_ext_add_list:
            for file_ext in file_ext_add_list:
                if not '--' in file_ext:
                    file_ext = "-- %s" % file_ext
                self.select_from_list(OBF_EXT_TYPES_DD, file_ext)
                self.click_element(OBF_ADD_EXT_BTN, "don't wait")
        elif extra_file_add_list:
            for file_ext in extra_file_add_list:
                self.input_text(OBF_ADD_EXT_TB, file_ext)
                self.click_button(OBF_ADD_EXT_BTN, None)
        if file_ext_del_list:
            del_col = 2
            for file_ext in file_ext_del_list:
                (rowf, colf) = self._get_table_cell_index(file_ext, OBF_FILE_EXTS_TBL)
                self._info('%s %s' % (rowf, colf))
                self.click_element(DEL_FILE_EXT_IMG((2), del_col), "don't wait")
        if enable_msg_modification and not self._is_checked(ENABLE_MSG_MOD_CB):
            self.click_element(ENABLE_MSG_MOD_CB, "don't wait")
        if not enable_msg_modification and self._is_checked(ENABLE_MSG_MOD_CB):
            self.click_element(ENABLE_MSG_MOD_CB, "don't wait")
        if msg_mod_threat_level:
            self.select_from_list(MSG_MOD_THREAT_LEVEL_DD, msg_mod_threat_level)
        if msg_mod_sub_pos:
            self.select_from_list(MSG_MOD_SUB_POS_DD, msg_mod_sub_pos)
        if msg_mod_sub:
            self.input_text(MSG_MOD_SUB_TB, msg_mod_sub)
        if url_rewrite_action:
            self._click_radio_button(URL_REWRITE_ACTION_RB(url_rewrite_action.lower()))
        if domains_to_bypass:
            self.input_text(BYPASS_DOMAIN_TA, domains_to_bypass)
        if threat_disclaimer:
            self.select_from_list(THREAT_DISCLAIMER_DD, threat_disclaimer)
        self._click_submit_button()

    def _fill_policy_dlp_page(self, enable_dlp, enable_all_dlp_policies=None,
                              disable_all_dlp_policies=None, dlp_policies_en_list=None, dlp_policies_dis_list=None):
        if not set([enable_dlp]) <= set(['custom', 'default', 'disable']):
            raise ValueError, '"%s" is invalid. Should custom or default or disable' \
                              % enable_dlp
        action = ACTION_MAP["dlp_%s" % enable_dlp]
        self.select_from_list(DLP_ENABE_DD, action)
        if enable_all_dlp_policies and not self._is_checked(DLP_ENABLE_ALL_CB):
            self.click_element(DLP_ENABLE_ALL_CB, "don't wait")
        elif disable_all_dlp_policies and self._is_checked(DLP_ENABLE_ALL_CB):
            self.click_element(DLP_ENABLE_ALL_CB, "don't wait")
        if dlp_policies_en_list:
            for dlp_policy in dlp_policies_en_list:
                (rowp, colp) = self._get_table_cell_index(dlp_policy, DLP_POLICY_TABLE)
                self.select_checkbox(DLP_POLICY_ENABLE_CB(rowp))
        if dlp_policies_dis_list:
            for dlp_policy in dlp_policies_dis_list:
                (rowp, colp) = self._get_table_cell_index(dlp_policy, DLP_POLICY_TABLE)
                self.unselect_checkbox(DLP_POLICY_ENABLE_CB(rowp))
        self._click_submit_button()

    def _find_mailpolicy(self, email_address, user_entry_type):
        if email_address:
            tb_name = TEXT_BOX_DICT['find_email_addr']
            self.input_text(tb_name, email_address)
        if user_entry_type:
            rb_key = 'find_%s' % user_entry_type
            self._click_radiobutton(rb_key)
        self.click_button(BUTTON_DICT["find_policy_button"], None)
        policy_text = self._get_table_cell("xpath=//td[@id='content']/form/dl/dd/table.1.1")
        return policy_text

    def _get_table_cell_index(self, item_name, table_name):
        self._info('Getting row, column for %s in %s table' \
                   % (item_name, table_name))
        table_loc = table_name
        rows = int(self.get_matching_xpath_count('%s//tr' % (table_loc,)))
        cols = int(self.get_matching_xpath_count('%s//th' % (table_loc,)))
        for col in xrange(0, cols):
            for row in xrange(0, rows):
                read_name = self._get_table_cell("xpath=%s.%s.%s" % (table_loc, row, col))
                if read_name == item_name:
                    return (row, col)
                elif item_name in read_name and 'view' in read_name.lower():
                    return (row, col)
        return (None, None)

    def _click_submit_button(self):
        self.click_button(BUTTON_DICT["submit_button"])
        self._info('Clicked "Submit" button')
        self._check_action_result()

    def _open_page(self, policy_type):
        submenu = {'incoming': "Incoming Mail Policies",
                   'outgoing': "Outgoing Mail Policies"
                   }
        self._navigate_to('Mail Policies', submenu[policy_type.lower()])

    def mailpolicy_add(self, policy_type, policy_name, order_of_policy=None,
                       sender_email_addr_list=None, rcpt_email_addr_list=None,
                       sender_ldap_grp_query_dict=None, rcpt_ldap_grp_query_dict=None, custom_roles=None):
        """ *DEPRECATED* Used to add incoming or outgoing mail policy.
            The mail policy should have a proper sender or recipient address.
            So either one of the four values should be given -
            sender_email_addr_list,rcpt_email_addr_list,
            sender_ldap_grp_query_dict,rcpt_ldap_grp_query_dict

        *Parameters*
            - `policy_type`: Type of mail policy being added.
              Value can be 'incoming', 'outgoing'. Mandatory.
            - `policy_name`: Name of the policy to be added. Value can be any
              String. Mandatory
            - `order_of_policy`: Order of where to insert the policy. Number or
              string. Optional.last but one by default(just above the
              default policy).
            - `sender_email_addr_list`: A tuple of email addresses of the policy
              members for sender user entries. Tuple.
            - `rcpt_email_addr_list`: A tuple of email addresses of the policy
              members for recipient user entries. Tuple
            - `sender_ldap_grp_query_dict`: A Dictionary of LDAP group name
              as keys and group query as values for sender user entries.
              Dictonary.  LDAP should be enabled.
            - `rcpt_ldap_grp_query_dict`: A Dictionary of LDAP group name as
              keys and group query as values for recipient user entries.
              Dictonary. LDAP should be enabled.
            - `custom_roles`: Roles to be assigned, List of strings.

        *Note*
             The mail policy should have a proper sender or recipient address.
             So either one of the four values should be given -
             sender_email_addr_list,rcpt_email_addr_list,
             sender_ldap_grp_query_dict,rcpt_ldap_grp_query_dict
             The address list can have values like - user@example.com, user@,
             @example.com,@.example.com

        *Examples*
        | Add MailPolicy | outgoing | testing |
        | ... | sender_email_addr_list=@qa42.qa,kannan@ |
        | ... | rcpt_email_addr_list=@qa20.qa |


        """
        self._info('Adding %s mail policy: %s' % (policy_type, policy_name))
        self._open_page(policy_type)
        add_policy_button = "name=AddPolicy"
        self.click_button(add_policy_button)
        self._fill_policy_page(policy_name, order_of_policy, sender_email_addr_list, \
                               rcpt_email_addr_list, sender_ldap_grp_query_dict, rcpt_ldap_grp_query_dict)
        self._set_custom_roles(custom_roles)
        self._click_submit_button()

    def mailpolicy_edit(self, policy_type, policy_name, new_name=None, order_of_policy=None,
                        sender_email_addr_list=None, rcpt_email_addr_list=None,
                        sender_ldap_grp_query_dict=None, rcpt_ldap_grp_query_dict=None, custom_roles=None):
        """*DEPRECATED* Used to edit incoming or outgoing mail policy.

        *Parameters*
            - `policy_type`: Type of mail policy being edited.
            Value can be 'incoming', 'outgoing'. Mandatory.
            - `policy_name`: Name of the policy to be modified.Value can be an
              String. Mandatory
            - `new_name`: New Name of the policy. String. Mandatory
            - `order_of_policy`: Order of where to insert the policy. Number or
              string. Optional.last but one by default(just above the default policy).
            - `sender_email_addr_list`: A tuple of email addresses of the
              policy members for sender  user entries. Tuple.Tuples are lists
              created using `Create List` command.
            - `rcpt_email_addr_list`: A tuple of email addresses of the policy
              members for recipient user entries. Tuple.Tuples are lists
              created using `Create List` command.
            - `sender_ldap_grp_query_dict`: A Dictionary of LDAP group name as
              keys and group query as values for sender user entries. Dictonary
            - `rcpt_ldap_grp_query_dict`: A Dictionary of LDAP group name as
              keys and group query as values for recipient user entries. Dictonary.
            - `custom_roles`: Roles to be assigned, List of strings.

        *Return*
            None

        *Examples*
        | Edit MailPolicy | outgoing | testing | sender_email_addr_list=test@qa20.qa |
        | ... | rcpt_email_addr_list=kgandhir@qa42.qa,kannan@ |

        """
        self._info('Adding %s mail policy: %s' % (policy_type, policy_name))
        self._open_page(policy_type)
        row, col = self._get_table_cell_index(policy_name, TABLE_DICT["policy_table"])
        if row is None:
            raise ValueError, '"%s" policy is not present' % (policy_name,)
        self.click_link('xpath=%s' % POL_LINK(row + 1))
        self._fill_policy_page(new_name, order_of_policy, sender_email_addr_list, \
                               rcpt_email_addr_list, sender_ldap_grp_query_dict, rcpt_ldap_grp_query_dict)
        self._set_custom_roles(custom_roles)
        self._click_submit_button()

    def _clear_user_option(self, locator, rows):
        for row in range(2, rows + 2):
            if self.selenium.is_editable(CHECKBOX_LOC(row)):
                self.uncheck_checkbox(CHECKBOX_LOC(row))

    def _set_custom_roles(self, custom_roles):
        if not custom_roles:
            return
        if not self.selenium.is_element_present(CUSTOM_ROLES_LINK):
            raise ValueError, "No custom roles found for assignment"

        self.click_element(CUSTOM_ROLES_LINK, "don't wait")
        rows = int(self.get_matching_xpath_count(DIV(ROLES_DIV)))
        # clear all checkboxes
        self._clear_user_option(ROLES_DIV, rows)
        for role in custom_roles:
            found = 0
            for row in range(2, rows + 2):
                if str(self.get_text(LOCATOR(row))) == role and \
                        self.selenium.is_editable(CB_LOC(row)):
                    self.check_checkbox(CB_LOC(row))
                    found = 1
            if not found:
                raise ValueError, "%s Role not found for assignment" % role
        self.click_button(OK_BUTTON, None)

    def mailpolicy_delete(self, policy_type, policy_name):
        """*DEPRECATED* Used to delete incoming or outgoing mail policy.

        *Parameters*
            - `policy_type`: Type of the mail policy. 'incoming'or 'outgoing'.
              Mandatory
            - `policy_name`: Name of the policy to be added. String. Mandatory

        *Return*
             None

        *Examples*
        | Delete MailPolicy | outgoing | testing |

        """
        self._info('Deleting %s mail policy: %s' % (policy_type, policy_name))
        self._open_page(policy_type)
        self._delete_policy(policy_name)

    def mailpolicy_find(self, policy_type, email_address, user_entry_type):
        """*DEPRECATED* Returns list of incoming or outgoing mail policies for
        a specified uer entry and its type.

        *Parameters*
            - `policy_type`: Type of the mail policy. 'incoming'or 'outgoing'.
              Mandatory
            - `email_address`: Email address whose policy names to be obtained.
              String. Mandatory.
            - `user_entry_type`: The email type is whether from the sender or
              receipient. 'recipient', 'sender'

        *Return*
            `policy_names`: String of incoming or outgoing mail policies for a
             user entry and its type. String.

        *Examples*
        | ${mail_policy}= | Find MailPolicy | outgoing | test@qa42.qa | sender |
        | Log | ${mail_policy} |

        """
        self._info('Finding %s mail policy for %s email address: %s' \
                   % (policy_type, user_entry_type, email_address,))
        self._open_page(policy_type)
        policy_names = self._find_mailpolicy(email_address, user_entry_type)
        msg = 'Found mail policies: %s' % policy_names
        self._info(msg)
        return policy_names

    def mailpolicy_edit_antivirus(self, policy_type, policy_name, \
                                  enable_antivirus_scanning, antivirus_types=None, msg_scanning_dict=None, \
                                  repaired_obj=None, encrypted_obj=None, unscannable_obj=None, \
                                  infected_obj=None):
        """*DEPRECATED* This function edits antivirus settings for the given incoming
             or outgoing mail policy.
        *Parameters*
            - `policy_type`: Type of the mail policy. 'incoming'or 'outgoing'.
              Mandatory
            - `policy_name`: Name of the policy to be added. String. Mandatory
            - `enable_antivirus_scanning`: Enable/Disable the antivirus scanning
              Values can be 'default' or 'custom' or 'disable'
            - `antivirus_types`: Tuple of antivirus engines to be used mcafee,
              sophos, etc. Tuple. Tuples are lists created using `Create List`
              command. This is mandatory.
            - `msg_scanning_dict`: A dictionary with parameters for message
              scanning settings.

              Dictionary.
             | Keys | Values |
             | action | `scan_virus` or `scan_repair` |
             | drop_attachmets |  True or False.Default value is False |
             | insert_xheader |  True or False. Default value is True |

            - `repaired_obj`: Object of type VirusPolicy.Should be created using
              `Create Message Obj` Command.

            - `encrypted_obj`: Object of type VirusPolicy.Should be created using
              `Create Message Obj` Command.

            - `unscannable_obj`: Object of type VirusPolicy.Should be created
              `Create Message Obj` Command.

            - `infected_obj`: Object of type VirusPolicy.Should be created using
              `Create Message Obj` Command.


        *Return*
         None

        *Examples*
        | ${msg_scan} | Create Dictionary | action | scan_virus |
        | ... | drop_attachmets | ${True} | insert_xheader | ${True} |
        | ${Repair1} | Create Message Obj | action=deliveras_is | archive=yes |
        | ... | modify_subj=prepend | subject_text=The text |
        | ... |  add_custom_header=yes | custom_header=Testing |
        | ... | custom_value=Value | notify_sender=${True} |
        | ... | notify_recipient=${True} | notify_others=${True} |
        | ... | notify_address=kannan@cisco.com | notify_subj=Testing |
        | @{virus_type} | Create List | mcafee |
        | Edit MailPolicy AntiVirus | outgoing | testing | custom |
        | ... |  antivirus_types=@{virus_type} |
        | ... | msg_scanning_dict=${msg_scan} | repaired_obj=${Repair1} |
        | ... | encrypted_obj=${Encrypt} | unscannable_obj=${Unscannable} |
        | ... |  infected_obj=${Infected} |

        """
        self._info('Adding %s mail policy: %s' % (policy_type, policy_name))
        self._open_page(policy_type)
        self._click_edit_policy_service(policy_name, SERVICE_DICT["antivirus"])
        self._fill_policy_antivirus_page(enable_antivirus_scanning, antivirus_types, \
                                         msg_scanning_dict, repaired_obj, encrypted_obj, unscannable_obj, \
                                         infected_obj)

    def virus_obj_create(self, action=None, archive=None, modify_subj=None,
                         subject_text=None, add_custom_header=None, custom_header=None,
                         custom_value=None, notify_sender=None, notify_recipient=None,
                         notify_others=None, notify_address=None, notify_subj=None,
                         modify_rcpt=None, mod_address=None, send_alt_host=None, alt_host=None):
        """*DEPRECATED* This function is used to create the Object of type VirusPolicy used in
        editing antivirus mailpolicy. This object is used to specify the
        actions required to be done on messages scanned by antivirus engine.

        *Parameters*
           - `action`: Action Applied to the messages.Drop down list.
              The Actions can be
              | Value | Action |
              | deliveras_is | Deliver As is |
              | deliveras_attachment_plain | Deliver As Attachment (text/plain) to New Message |
              | deliveras_attachment_msg | Deliver As Attachment (message/rfc822) to New Message |
              | drop | Drop the Message |
              | quarantine | Qaurantine The Message |

           - `archive`: Used to specify if we need to archive the message.
             The values to be specified are:
             | Value | Action |
             | no | Donot Archive the Message |
             | yes | Archive the Message |

           - `modify_subj`: The Subject of the repaiered Message can be modified.
              It has a three options,
              | Value to be given | Action |
              | no | Dont Modify the Subject |
              | prepend | Prepend the String given to Subject |
              | append | Append the String given to the Subject |

           - `subject_text`: The text which is to be given to modify the subject.
             Can be any text.

           - `add_custom_header`: This specifies whether we want to add custom
             header to the message.
             The values to be specified are
             | Value | Action |
             | no | No Custom Header |
             | yes | Add Custom Header |

           - `custom_header`: Specify the value of the custom header.
             Can be any text.

           - `custom_value`:  Custom Value. Can be any text.

           - `notify_sender`: If we would want to notify sender. Value can be
            ${True} or ${False}

           - `notify_recipient`: If we would want to notify receipent. Value is
             either ${True} or ${False}

           - `notify_others`: If we would want to notify other people. Value is
             either ${True} or ${False}

           - `notify_address`: The email address of others send notification.
             Should be a proper email address.

           - `notify_subj`: The Subject of the mail.

           - `modify_rcpt` : Modify the Message receipient. Value can be
             either  ${True} or ${False}

           - `mod_address`: The email address of the receipient we would
             like to send.

           - `send_alt_host`: Send to alternate host. Value can be
             either  ${True} or ${False}

           - `alt_host`: Alternate Host Value. Value should be a host name or
             ip address

      *Return*
          Returns the antivirus message object.

      *Note*
          Repaied messages dont have the following attributes:
          modify_rcpt, mod_address,send_alt_host and alt_host.

      *Examples*
        | ${Repair1} | Create Message Obj | action=deliveras_is | archive=yes |
        | ... | modify_subj=prepend | subject_text=The text | add_custom_header=yes |
        | ... | custom_header=Testing | custom_value=Value | notify_sender=${True} |
        | ... | notify_recipient=${True} | notify_others=${True} |
        | ... | notify_address=kannan@cisco.com | notify_subj=Testing |

        """
        message_obj = Message_Obj(action, archive, modify_subj, subject_text,
                                  add_custom_header, custom_header, custom_value,
                                  notify_sender, notify_recipient, notify_others,
                                  notify_address, notify_subj, modify_rcpt, mod_address,
                                  send_alt_host, alt_host)
        return message_obj

    def mailpolicy_edit_antispam(self, policy_type, policy_name, enable_antispam_scanning,
                                 scanning_type=None, spam_obj=None, enable_suspected_spam=None,
                                 suspected_spam_obj=None, enable_marketing_spam=None, marketing_spam_obj=None,
                                 threshold_setting=None, spam_score=None, suspected_spam_score=None):
        """*DEPRECATED* This function edits antispam settings for the given incoming or
             outgoing mail policy.
        *Parameters*
            - `policy_type`: Type of the mail policy. 'incoming'or 'outgoing'.
              Mandatory
            - `policy_name`: Name of the policy to be added. String. Mandatory
            - `enable_antispam_scanning`:Enable/Disable the antispam scanning.
              Values can be 'default' or 'custom' or 'disable'

            - `spam_obj`: Object of type SpamPolicy.Should be created using
              `Create Spam Obj` Command.

            - `enable_suspected_spam`: Enable scanning of suspected spam mails.
              Values can be yes or no.

            - `suspected_spam_obj`: Object of type SpamPolicy.Should be created
              `Create Spam Obj` Command.

            - `enable_marketing_spam`:  Enable scanning of Marketing spam mails.
              Values can be yes or no.

            - `marketing_spam_obj`: Object of type SpamPolicy.Should be created
              `Create Spam Obj` Command.

            - `threshold_setting`: Change the threshold values for classifying
              as spam.
              'default' or 'custom'. String. default value is 'default'.

            - `spam_score`: Score for Positively Identified Spam. Number.

            - `suspected_spam_score`: score for suspected spam. Number.

        *Return*
         None

        *Examples*
          | ${Scan_obj} | Create Spam Obj | action=deliver | archive=yes |
          | ... | alternate_host=10.1.1.1 | modify_subj=prepend |
          | ... | subject_text=The Text |
          | ... | custom_header=Header | custom_value=Value |
          | ... |  alt_envelope_recipient=kgandhir@ironport.com |
          | Edit MailPolicy AntiSpam | outgoing | testing | custom |
          | ... | scanning_type=ipas |
          | ... | spam_obj=${Scan_obj} | enable_suspected_spam=yes |
          | ... | suspected_spam_obj=${Suspected_Spam} | enable_marketing_spam=yes |
          | ... | marketing_spam_obj=${Marketing_Spam} | threshold_setting=custom |
          | ... | spam_score=100 | suspected_spam_score=70 |


        """
        self._info('Adding %s mail policy: %s' % (policy_type, policy_name))
        self._open_page(policy_type)
        self._click_edit_policy_service(policy_name, SERVICE_DICT["antispam"])
        self._fill_policy_antispam_page(enable_antispam_scanning, scanning_type,
                                        spam_obj, enable_suspected_spam, suspected_spam_obj,
                                        enable_marketing_spam, marketing_spam_obj,
                                        threshold_setting, spam_score, suspected_spam_score)
        msg = 'Edited antispam for %s mail policy: %s' % (policy_type, policy_name)
        self._info(msg)

    def spam_obj_create(self, action=None, archive=None, alternate_host=None,
                        modify_subj=None, subject_text=None,
                        custom_header=None, custom_value=None, alt_envelope_recipient=None):
        """*DEPRECATED* Object of type SpamPolicy. Used to specify the various actions
            to be taken on the mails after identified by the spam engine.
             Actions canbe specified for emails identified as spam, suspected spam,
             marketing spam.

        *Parameters*
            - `action` :Action Applied to the messages. Drop Down List.
              The actions can be
              | Value | Actions |
              | drop | Drop the mails |
              | deliver | Deliver the mails |
              | bounce | Bounce the mails |
              | quarantine | Send the mails to the spam Quarantine |

            - `archive`: Used to specify if we need to archive the message.
              The values to be specified are:
              | Value | Action |
              | no | Donot Archive the Message |
              | yes | Archive the Message |

            - `alternate_host`: Send the mail to alternate Host.
              Alternate Host Value. Value should be a host name or ip address

            - `modify_subj`: The Subject of the repaiered Message can be modified.
              It has a three options,
              | Value to be given | Action |
              | no | Dont Modify the Subject |
              | prepend | Prepend the String given to Subject |
              | append | Append the String given to the Subject |

            - `subject_text`: subject text to be changed. Can be any String.

            - `custom_header`: Value of the Custom Header. Can be any string.

            - `custom_value`: Custom Value. Can be any string.

            - `alt_envelope_recipient`: Send to an Alternate Envelope Recipient.
              Can be any valid email address.

        *Return*
            Returns an object of Spam Policy.

        *Examples*
          | ${Scan_obj} | Create Spam Obj | action=deliver | archive=yes |
          | ... | alternate_host=10.1.1.1 | modify_subj=prepend |
          | ... | subject_text=The Text | custom_header=Header |
          | ... | custom_value=Value |
          | ... | alt_envelope_recipient=kgandhir@ironport.com |

        """
        spam_obj = Spam_Obj(action, archive, alternate_host, modify_subj,
                            subject_text, custom_header, custom_value,
                            alt_envelope_recipient)
        return spam_obj

    def mailpolicy_edit_contentfilters(self, policy_type, policy_name,
                                       enable_contentfilters, enable_filter_names=None, disable_filter_names=None):
        """*DEPRECATED* This function edits content filters settings for the given
            incoming or outgoing mail policy.

        *Parameters*
            - `policy_type`: Type of the mail policy. 'incoming'or 'outgoing'.
              Mandatory

            - `policy_name`: Name of the policy to be added. String. Mandatory

            - `enable_contentfilters`: Enable/Disable the content filters.
              Values can be 'default' or 'custom' or 'disable'

            - `enable_filter_names`: Tuple of content filters' names to
              be enabled. Tuple.
              Tuples are lists created using `Create List` command.

            - `disable_filter_names`: Tuple of content filters' names to
              be disabled. Tuple.
              Tuples are lists created using `Create List` command.

        *Return*
            None

        *Examples*
          | @{enable} | Create List | testing |
          | Edit MailPolicy ContentFilters | outgoing | testing | custom |
          | ... | enable_filter_names=@{enable} |

        """
        self._info('Adding %s mail policy: %s' % (policy_type, policy_name))
        self._open_page(policy_type)
        self._click_edit_policy_service(policy_name, SERVICE_DICT["content_filters"])
        self._fill_policy_contentfilters_page(enable_contentfilters, enable_filter_names, \
                                              disable_filter_names)

    def mailpolicy_edit_vof(self, policy_type, policy_name, enable_vof, \
                            quarantine_threat_level=None, mqr_viral_attachments=None, mqr_other_threats=None, \
                            file_ext_add_list=None, extra_file_add_list=None, file_ext_del_list=None, \
                            enable_msg_modification=None, msg_mod_threat_level=None, \
                            msg_mod_sub_pos=None, msg_mod_sub=None, \
                            url_rewrite_action=None, domains_to_bypass=None, threat_disclaimer=None):
        """*DEPRECATED* This function edits outbreak filters settings for the given
            incoming or outgoing mail policy.

        *Parameters*
            - `policy_type`: Type of the mail policy. 'incoming'or 'outgoing'.
              Mandatory

            - `policy_name`: Name of the policy to be added. String. Mandatory

            - `enable_vof`: Enable/Disable the Virus Outbreak filters.
              Values can be 'default' or 'custom' or 'disable'

            - `quarantine_threat_level`: Quarantine threat level. Number. Values 1-5

            - `mqr_viral_attachments`: A tuple with number and a string specifying days or
              hours as given in the web page. Tuple. Value between 1
              hour and 365 days - 8760 hours
              Tuples are lists created using `Create List` command.

            - `mqr_other_threats`: A tuple with number and a string specifying
              days or hours.
              Value between 1 hour and 365 days - 8760 hours.
              Tuples are lists created using `Create List` command.

            - `file_ext_add_list`: A tuple of file extensions to which
              outbreak filters need
              to be bypassed. Tuple. Optional. Tuples are lists created
              using `Create List` command.

            - `extra_file_add_list`: A tuple of file extensions for which
              outbreak filters need
              to be bypassed, but not available in the given drop down list. Tuple.

            - `file_ext_del_list`: A tuple of file extensions which need to be
              deleted from the
              list of bypassed extensions. Tuple. Optional.

            - `enable_msg_modification`: Enable message modification or not.
              Boolean.

            - `msg_mod_threat_level`: Message modification threat level. Number.
              Value between 1 and 5

            - `msg_mod_sub_pos`: Message modification subject position as given
              in the web page. String.
              Values - Prepend, Append, None.

            - `msg_mod_sub`: Message modification subject content. String.

            - `url_rewrite_action`: Cisco Security proxy scans and rewrites
              suspicious or malicious URLs, this option tells what kind of
              action it should be as given in web page. String.
              The values can be
               Enable only for unsigned messages (recommended)
	       Enable for all messages
	       Disable

            - `domains_to_bypass`: Domains to bypass scanning.String.The value can
              be domain.

            - `threat_disclaimer`: Threat disclaimer as given in the web page. String.
              Values - None, System Generated.

        *Examples*
          | @{mqr_viral} | Create List | 8755 | Hours |
          | @{file1} | Create List | txt |
          | @{domains} | Create List | qa42.qa |
          | Edit MailPolicy Vof | outgoing | testing | custom |
          | ... |  quarantine_threat_level=3 |
          | ... | mqr_viral_attachments=@{mqr_viral} |
          | ... | mqr_other_threats=@{mqr_viral} |
          | ... | file_ext_add_list=@{file1} | extra_file_add_list=@{file2} |
          | ... | file_ext_del_list=@{file2} | enable_msg_modification=${True} |
          | ... | msg_mod_threat_level=1 |  msg_mod_sub_pos=Prepend |
          | ... |  msg_mod_sub=Testing |
          | ... |  url_rewrite_action=Enable for all messages |
          | ... | domains_to_bypass=qa42.qa |
          | ... | threat_disclaimer=System Generated |

        """

        self._info('Adding %s mail policy: %s' % (policy_type, policy_name))
        self._open_page(policy_type)
        self._click_edit_policy_service(policy_name, SERVICE_DICT["obf"])
        self._info(policy_name)
        self._info(mqr_viral_attachments)
        self._info(quarantine_threat_level)
        self._fill_policy_obf_page(enable_vof, quarantine_threat_level, \
                                   mqr_viral_attachments, mqr_other_threats, file_ext_add_list, \
                                   extra_file_add_list, file_ext_del_list, enable_msg_modification, \
                                   msg_mod_threat_level, msg_mod_sub_pos, msg_mod_sub, \
                                   url_rewrite_action, domains_to_bypass, threat_disclaimer)

    def mailpolicy_edit_dlp(self, policy_type, policy_name, enable_dlp, \
                            enable_all_dlp_policies=None, disable_all_dlp_policies=None, dlp_policies_en_list=None, \
                            dlp_policies_dis_list=None):
        """*DEPRECATED* This function edits content filters settings for the given
            incoming or outgoing mail policy.

        *Parameters*
            - `policy_type`: Type of the mail policy. 'incoming'or 'outgoing'.
              Mandatory

            - `policy_name`: Name of the policy to be added. String. Mandatory

            - `enable_dlp`: Enable/Disable the DLP.
              Values can be 'default' or 'custom' or 'disable'

            - `enable_all_dlp_policies`: Enable all dlp policies or not. Value can be
              either ${True} or ${False}

            - `disable_all_dlp_policies`: Disable all dlp policies.Value can be
              either ${True} or ${False}

            - `dlp_policies_en_list`: Tuple of dlp policies to be enabled. Tuple.

            - `dlp_policies_dis_list`: Tuple of dlp policies to be disabled. Tuple.

        *Return*
         None

        *Examples*
          | @{policy} | Create List | HIPAA and HITECH |
          | edit mailpolicy dlp | outgoing | testing | custom |
          | ... |  enable_all_dlp_policies=${True} |
          | ... | disable_all_dlp_policies=${True} |
          | ... | dlp_policies_en_list=@{policy} |
          | ... | dlp_policies_dis_list=@{policy} |

        """
        self._info('Adding %s mail policy: %s' % (policy_type, policy_name))
        self._open_page(policy_type)
        self._click_edit_policy_service(policy_name, SERVICE_DICT["dlp"])
        self._fill_policy_dlp_page(enable_dlp, enable_all_dlp_policies, \
                                   disable_all_dlp_policies, dlp_policies_en_list, dlp_policies_dis_list)


class Message_Obj(object):
    """Container class for creating attributes for repaiered object to be
    used in antivirus mail policies.

    *Parameters*
       - `action`: Action Applied to the messages.
       - `archive`: Used to specify if we need to archive the message.
       - `modify_subj`: The Subject of the repaiered Message can be modified.
       - `subject_text`: The text which is to be given to modify the subject.
       - `add_custom_header`: This specifies whether we would want to add custom
       - `custom_header`: Specify the value of the custom header.
       - `custom_value`:  Custom Value.
       - `notify_sender`: If we would want to notify sender.
       - `notify_recipient`: If we would want to notify receipent.
       - `notify_others`: If we would want to notify other people.
       - `notify_address`: The email address of others to be sent notification.
       - `notify_subj`: The subject to be used.
       - `modify_rcpt` : Modify the Message receipient.
       - `mod_address`: The email address of the receipient we would like to send.
       - `send_alt_host`: Send to alternate host. Value can be
       - `alt_host`: Alternate Host Value. Value should be a host name or ip address

    """

    def __init__(self, action, archive, modify_subj, subject_text,
                 add_custom_header, custom_header, custom_value,
                 notify_sender, notify_recipient, notify_others, notify_address,
                 notify_subj, modify_rcpt, mod_address, send_alt_host,
                 alt_host):
        self.action = action
        self.archive = archive
        self.modify_subj = modify_subj
        self.subject_text = subject_text
        self.add_custom_header = add_custom_header
        self.custom_header = custom_header
        self.custom_value = custom_value
        self.notify_sender = notify_sender
        self.notify_recipient = notify_recipient
        self.notify_others = notify_others
        self.notify_address = notify_address
        self.notify_subj = notify_subj
        self.modify_rcpt = modify_rcpt
        self.mod_address = mod_address
        self.send_alt_host = send_alt_host
        self.alt_host = alt_host

    def __str__(self):
        message_obj_string = ('Action: %s' % (self.action),
                              'Achive: %s' % (self.archive),
                              'Modifying Subject: %s' % (self.modify_subj),
                              'Subject Text: %s' % (self.add_custom_header),
                              'Add Custom Header: %s' % (self.add_custom_header),
                              'Cusom Header Vaue: %s' % (self.custom_header),
                              'Custom Value: %s' % (self.custom_value),
                              'Notify Sender: %s' % (self.notify_sender),
                              'Notify Recipient: %s' % (self.notify_recipient),
                              'Notify Others: %s' % (self.notify_others),
                              'Notify Email Address: %s' % (self.notify_address),
                              'Notify Subject: %s' % (self.notify_subj),
                              'Modify Receipient: %s' % (self.modify_rcpt),
                              'Modified Receipient Address: %s' % (self.mod_address),
                              'Alternate Sending Host: %s' % (self.alt_host)

                              )
        return '; '.join(message_obj_string)


class Spam_Obj(object):
    def __init__(self, action, archive, alternate_host, modify_subj,
                 subject_text, custom_header, custom_value,
                 alt_envelope_recipient):
        self.action = action
        self.archive = archive
        self.alternate_host = alternate_host
        self.modify_subj = modify_subj
        self.subject_text = subject_text
        self.custom_header = custom_header
        self.custom_value = custom_value
        self.alt_envelope_recipient = alt_envelope_recipient

    def __str__(self):
        scan_obj_string = ('Action: %s' % (self.action),
                           'Archive: %s' % (self.archive),
                           'Alternate Sending Host: %s' % (self.alternate_host),
                           'Modify Subject: %s' % (self.modify_subj),
                           'Suject Text: %s' % (self.subject_text),
                           'Custom Value: %s' % (self.custom_value),
                           'Alternate Envelope Receipient: %s' % (self.alt_envelope_recipient)
                           )
        return '; '.join(scan_obj_string)

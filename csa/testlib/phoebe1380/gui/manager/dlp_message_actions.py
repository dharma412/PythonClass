#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/dlp_message_actions.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from sal.containers import cfgholder

MA_TABLE="//td[@id='content']/form/dl/dd/table"
CC_TABLE="//td[@id='content']/form[3]/dl/dd/table"
EDIT_LINK = lambda row: "//table[@class='cols']/tbody/tr[%d]/td/a" % row
NAME_TB="id=name"
DESC_TA="id=description"
MSG_ACTION_DD="id=message_action"
EN_ENC_CB="id=encrypt_message"
ENC_RULE_DD="id=use_tls"
ENC_PROF_DD="id=encryption_profile"
ENC_MSG_SUB_TB="id=encrypted_subject"
QUARANTINE_CB="id=quarantine_copy"
QPOLICY_DD="//table[@id='encryption_params']/tbody/tr[3]/td[2]/select"
CUST_HDR_NAME_TB="id=header_name"
CUST_HDR_VALUE_TB="id=header_value"
MSG_SUBJ_TB="id=modified_subject"
DLP_DISCLAIMER_DD="id=disclaimer_resource"
BOTTOM_RB="disclaimer_position_bottom"
TOP_RB="disclaimer_position_top"
ALT_HOST_TB="id=alt_mailhost"
BCC_RPT_CB="id=enable_bcc"
BCC_RCPTS_TB="id=bcc_list"
RETURN_TB="id=bcc_return_path"
BCC_SUBJ_TB="id=bcc_subject"
NOTIFY_SENDER_CB="id=notify_sender"
NOTIFY_OTHER_CB="id=notify_others_checkbox"
NOTIFY_OTHERS_TB="id=notify_others"
NOTIFY_RETURN_TB="id=notification_return_address"
NOTIFY_SUBJ_TB="id=notification_subject"
INCLUDE_ORIG_CB="id=include_original"
CC_SETTING="id=entity_score_enabled"
NOTIFY_TEMPLATE_DD="id=notification_resource_id"
MOD_TABLE="//*[@id='form']/dl/dd/table/tbody/tr[5]/td/table/tbody/tr[4]/td[2]/table/"
NOTIFY_TABLE="//*[@id='form']/dl/dd/table/tbody/tr[5]/td/table/tbody/tr[12]/td[2]/table/"
POLICIES_DIV = "//*[@id='form']/dl/dd/div[2]"
BUTTON_ADD_MESSAGE_ACTION =  "//input[@value='Add Message Action...']"
ADVANCED_LINK = "//*[@id='advanced_row']/th/a"

class DlpMessageActions(GuiCommon):
    """
    DLP Message Actions page interaction class.
    'Mail Policies -> DLP Policy Customizations' section.
    """
    def _open_page(self):
        self._navigate_to('Mail Policies', 'DLP Policy Customizations')

    def get_keyword_names(self):
        return ['dlp_message_action_add',
                'dlp_message_action_edit',
                'dlp_message_action_duplicate',
                'dlp_message_action_delete',
                'dlp_custom_classifier_settings',
                'dlp_custom_classifier_delete',
                'dlp_message_action_get_all',
                'dlp_message_action_get_definition']

    def _click_link_to_edit(self, ac_name, table_loc):
        (rowp, colp) = self._cell_indexes(ac_name, table_loc)
        if rowp is None:
            raise ValueError, '"%s" is not present' % (ac_name,)
        self.click_element(EDIT_LINK(rowp+1))

    def _cell_indexes(self, item_name, table_loc):
        self._info('Getting row, column for %s in %s table' %\
        (item_name, table_loc))
        rows = int(self.get_matching_xpath_count('%s//tr' % (table_loc,)))
        cols = int(self.get_matching_xpath_count('%s//th' % (table_loc,)))
        for col in xrange(0, cols):
            for row in xrange(0, rows):
                read_name = self._get_table_cell("xpath=%s.%s.%s"%(table_loc, row, col))
                if read_name == item_name:
                    return (row, col)
                elif item_name in read_name and 'view' in read_name.lower():
                    return (row, col)
        return (None, None)

    def check_and_select(self, locator, param):
        if param is not None:
            if param:
                self._select_checkbox(locator)
                return True
            else:
                self._unselect_checkbox(locator)
                return False

    def _fill_msg_action(self,
                         name=None,
                         description=None,
                         msg_action=None,
                         enable_encryption=None,
                         encryption_rule=None,
                         encryption_profile=None,
                         encrypted_msg_subject=None,
                         send_to_quarantine=None,
                         quarantine_policy=None,
                         cust_header_name=None,
                         cust_header_value=None,
                         msg_subject=None,
                         dlp_disclaimer=None,
                         disclaimer_position=None,
                         msg_alt_host=None,
                         msg_bcc_rcpts=None,
                         msg_return_address=None,
                         delivery_subject=None,
                         notify_sender=None,
                         others_to_notify=None,
                         return_addrs_to_notify=None,
                         notify_subject=None,
                         include_orig_msg=None,
                         notification_template=None):
        """ Populates DLP Message Action table with data.

        Parameters:
        - `name`: name of the message action. Mandatory.
        - `description`: description of the message action. Optional.
        - `msg_action`: message action to apply.
        Options available: Quarantine, Drop, Deliver.
        - `enable_encryption`: enable/disable encryption. Boolean.
        Available only if encryption is configured.
        - `encryption_rule`: rule to use for encryption.
        - `encryption_profile`: profile to use for encryption.
        - `encrypted_msg_subject`: subject of encrypted message.
        - `send_to_quarantine`: send message to quarantine. Boolean.
        - `quarantine_policy`: quarantine to send message to.
        - `cust_header_name`: set custom header name. String.
        - `cust_header_value`: set value of custom header. String.
        - `msg_subject`: set message subject. String.
        - `dlp_disclaimer`: DLP disclaimer to use.
        - `disclaimer_position`: position of DLP disclaimer in the message.
        Options available: below, above.
        - `msg_alt_host`: alternate host to send message to. String.
        - `msg_bcc_rcpts`: send copy of message to recipients. List.
        - `msg_return_address`: return address. String. Optional.
        - `delivery_subject`: subject to use for copy of message. String. Optional.
        - `notify_sender`: send DLP notification to sender. String.
        - `others_to_notify`: send DLP notification to additional recipients. List.
        - `return_addrs_to_notify`: set return address for DLP notification.
        - `notify_subject`: subject to use for DLP notification. String.
        - `include_orig_msg`: include original message to DLP notification. Boolean.
        - `notification_template`: DLP notification template to use. Select option.

        Return:
        None
        """

        if name is not None:
            self.input_text(NAME_TB, name)
        if description is not None:
            self.input_text(DESC_TA, description)
        if msg_action is not None:
            self.select_from_list(MSG_ACTION_DD, msg_action)
        self.check_and_select(EN_ENC_CB, enable_encryption)
        if encryption_rule is not None:
            self.select_from_list(ENC_RULE_DD, encryption_rule)
        if encryption_profile is not None:
            self.select_from_list(ENC_PROF_DD, encryption_profile)
        if encrypted_msg_subject is not None:
            self.input_text(ENC_MSG_SUB_TB, encrypted_msg_subject)
        self.check_and_select(QUARANTINE_CB, send_to_quarantine)
        if quarantine_policy is not None:
            self.select_from_list(QPOLICY_DD, quarantine_policy)
        if cust_header_name is not None:
            self.input_text(CUST_HDR_NAME_TB, cust_header_name)
        if cust_header_value is not None:
            self.input_text(CUST_HDR_VALUE_TB, cust_header_value)
        if msg_subject is not None:
            self.input_text(MSG_SUBJ_TB, msg_subject)
        if dlp_disclaimer is not None:
            self.select_from_list(DLP_DISCLAIMER_DD, dlp_disclaimer)
        if disclaimer_position is not None:
            if 'below' in disclaimer_position.lower():
                self._click_radio_button(BOTTOM_RB)
            if 'above' in disclaimer_position.lower():
                self._click_radio_button(TOP_RB)
        if msg_alt_host is not None:
            self.input_text(ALT_HOST_TB, msg_alt_host)
        if self.check_and_select(BCC_RPT_CB, msg_bcc_rcpts):
            self.input_text(BCC_RCPTS_TB,
                ','.join(self._convert_to_tuple(msg_bcc_rcpts)))
        if msg_return_address is not None:
            self.input_text(RETURN_TB, msg_return_address)
        if delivery_subject is not None:
            self.input_text(BCC_SUBJ_TB, delivery_subject)
        self.check_and_select(NOTIFY_SENDER_CB, notify_sender)
        if self.check_and_select(NOTIFY_OTHER_CB, others_to_notify):
            self.input_text(NOTIFY_OTHERS_TB,
                ','.join(self._convert_to_tuple(others_to_notify)))
        if return_addrs_to_notify is not None:
            self.input_text(NOTIFY_RETURN_TB, return_addrs_to_notify)
        if notify_subject is not None:
            self.input_text(NOTIFY_SUBJ_TB, notify_subject)
        if include_orig_msg is not None:
            self.check_and_select(INCLUDE_ORIG_CB, include_orig_msg)
        if notification_template is not None:
            self.select_from_list(NOTIFY_TEMPLATE_DD, notification_template)
        self._click_submit_button(skip_wait_for_title=True)

    def dlp_message_action_add(self,
                               name=None,
                               description=None,
                               msg_action=None,
                               enable_encryption=None,
                               encryption_rule=None,
                               encryption_profile=None,
                               encrypted_msg_subject=None,
                               send_to_quarantine=None,
                               quarantine_policy=None,
                               cust_header_name=None,
                               cust_header_value=None,
                               msg_subject=None,
                               dlp_disclaimer=None,
                               disclaimer_position=None,
                               msg_alt_host=None,
                               msg_bcc_rcpts=None,
                               msg_return_address=None,
                               delivery_subject=None,
                               notify_sender=None,
                               others_to_notify=None,
                               return_addrs_to_notify=None,
                               notify_subject=None,
                               include_orig_msg=None,
                               notification_template=None,):
        """ Adds new DLP Message Action.

        Parameters:
        - `name`: name of the message action. Mandatory.
        - `description`: description of the message action. Optional.
        - `msg_action`: message action to apply.
        Options available: Quarantine, Drop, Deliver.
        - `enable_encryption`: enable/disable encryption. Boolean.
        Available only if encryption is configured.
        - `encryption_rule`: rule to use for encryption.
        - `encryption_profile`: profile to use for encryption.
        - `encrypted_msg_subject`: subject of encrypted message.
        - `send_to_quarantine`: send message to quarantine. Boolean.
        - `quarantine_policy`: quarantine to send message to.
        - `cust_header_name`: set custom header name. String.
        - `cust_header_value`: set value of custom header. String.
        - `msg_subject`: set message subject. String.
        - `dlp_disclaimer`: DLP disclaimer to use.
        - `disclaimer_position`: position of DLP disclaimer in the message.
        Options available: below, above.
        - `msg_alt_host`: alternate host to send message to. String.
        - `msg_bcc_rcpts`: send copy of message to recipients. List.
        - `msg_return_address`: return address. String. Optional.
        - `delivery_subject`: subject to use for copy of message. String. Optional.
        - `notify_sender`: send DLP notification to sender. String.
        - `others_to_notify`: send DLP notification to additional recipients. List.
        - `return_addrs_to_notify`: set return address for DLP notification.
        - `notify_subject`: subject to use for DLP notification. String.
        - `include_orig_msg`: include original message to DLP notification. Boolean.
        - `notification_template`: DLP notification template to use. Select option.

        Return:
        None

        Examples:
        | Dlp Message Action Add  |
        | ... | name=quarantine |
        | ... | description=quarantines messages |
        | ... | msg_action=Quarantine |
        | ... | cust_header_name=QuarantinedBy |
        | ... | cust_header_value=DLP |
        | ... | msg_subject=Quarantined By DLP |

        | Dlp Message Action Add  |
        | ... | name=deliver |
        | ... | description=delivers messages |
        | ... | msg_action=Deliver |
        | ... | cust_header_name=MarkedBy |
        | ... | cust_header_value=DLP |
        | ... | msg_subject=Matched DLP |
        | ... | notify_sender=${True} |
        | ... | notify_subject=This message matched DLP policies |
        | ... | include_orig_msg=${True} |
        | ... | others_to_notify=@{others} | Set Variable | me@mail.qa | yo@mail.qa |

        | Dlp Message Action Add  |
        | ... | name=deliver_and_encrypt |
        | ... | description=delivers encrypted messages |
        | ... | msg_action=Deliver |
        | ... | enable_encryption=${True} |
        """
        self._info('Adding DLP message action %s' % name)
        self._open_page()
        self.click_button(BUTTON_ADD_MESSAGE_ACTION)
        if self._is_visible(ADVANCED_LINK):
            self.click_element(ADVANCED_LINK, "don't wait")
        self._fill_msg_action(name=name,
                              description=description,
                              msg_action=msg_action,
                              enable_encryption=enable_encryption,
                              encryption_rule=encryption_rule,
                              encryption_profile=encryption_profile,
                              encrypted_msg_subject=encrypted_msg_subject,
                              send_to_quarantine=send_to_quarantine,
                              quarantine_policy=quarantine_policy,
                              cust_header_name=cust_header_name,
                              cust_header_value=cust_header_value,
                              msg_subject=msg_subject,
                              dlp_disclaimer=dlp_disclaimer,
                              disclaimer_position=disclaimer_position,
                              msg_alt_host=msg_alt_host,
                              msg_bcc_rcpts=msg_bcc_rcpts,
                              msg_return_address=msg_return_address,
                              delivery_subject=delivery_subject,
                              notify_sender=notify_sender,
                              others_to_notify=others_to_notify,
                              return_addrs_to_notify=return_addrs_to_notify,
                              notify_subject=notify_subject,
                              include_orig_msg=include_orig_msg,
                              notification_template=notification_template)

    def dlp_message_action_edit(self,
                                ac_name,
                                description=None,
                                msg_action=None,
                                enable_encryption=None,
                                encryption_rule=None,
                                encryption_profile=None,
                                encrypted_msg_subject=None,
                                send_to_quarantine=None,
                                quarantine_policy=None,
                                cust_header_name=None,
                                cust_header_value=None,
                                msg_subject=None,
                                dlp_disclaimer=None,
                                disclaimer_position=None,
                                msg_alt_host=None,
                                msg_bcc_rcpts=None,
                                msg_return_address=None,
                                delivery_subject=None,
                                notify_sender=None,
                                others_to_notify=None,
                                return_addrs_to_notify=None,
                                notify_subject=None,
                                include_orig_msg=None,
                                notification_template=None,):
        """ Adds new DLP Message Action.

        Parameters:
        - `ac_name`: name of message action to edit. String.
        - `description`: description of the message action. Optional.
        - `msg_action`: message action to apply.
        Options available: Quarantine, Drop, Deliver.
        - `enable_encryption`: enable/disable encryption. Boolean.
        Available only if encryption is configured.
        - `encryption_rule`: rule to use for encryption.
        - `encryption_profile`: profile to use for encryption.
        - `encrypted_msg_subject`: subject of encrypted message.
        - `send_to_quarantine`: send message to quarantine. Boolean.
        - `quarantine_policy`: quarantine to send message to.
        - `cust_header_name`: set custom header name. String.
        - `cust_header_value`: set value of custom header. String.
        - `msg_subject`: set message subject. String.
        - `dlp_disclaimer`: DLP disclaimer to use.
        - `disclaimer_position`: position of DLP disclaimer in the message.
        Options available: below, above.
        - `msg_alt_host`: alternate host to send message to. String.
        - `msg_bcc_rcpts`: send copy of message to recipients. List.
        If you need to disable this option and leave corresponding text field with data -
        pass ${EMPTY}
        - `msg_return_address`: return address. String. Optional.
        - `delivery_subject`: subject to use for copy of message. String. Optional.
        - `notify_sender`: send DLP notification to sender. String.
        - `others_to_notify`: send DLP notification to additional recipients. List.
        If you need to disable this option and leave corresponding text field with data -
        pass ${EMPTY}
        - `return_addrs_to_notify`: set return address for DLP notification.
        - `notify_subject`: subject to use for DLP notification. String.
        - `include_orig_msg`: include original message to DLP notification. Boolean.
        - `notification_template`: DLP notification template to use. Select option.

        Return:
        None

        Example:
        | Dlp Message Action Edit |
        | ... | ac_name |
        | ... | description=modified action |

        | Dlp Message Action Edit |
        | ... | ac_name |
        | ... | enable_encryption=${True} |
        | ... | encrypted_msg_subject |
        | ... | Message is encrypted |
        | ... | others_to_notify=${EMPTY} |
        """
        self._info('Editing DLP message action %s' % ac_name)
        self._open_page()
        self._click_link_to_edit(ac_name, MA_TABLE)
        if self._is_visible(ADVANCED_LINK):
            self.click_element(ADVANCED_LINK, "don't wait")
        self._fill_msg_action(description=description,
                              msg_action=msg_action,
                              enable_encryption=enable_encryption,
                              encryption_rule=encryption_rule,
                              encryption_profile=encryption_profile,
                              encrypted_msg_subject=encrypted_msg_subject,
                              send_to_quarantine=send_to_quarantine,
                              quarantine_policy=quarantine_policy,
                              cust_header_name=cust_header_name,
                              cust_header_value=cust_header_value,
                              msg_subject=msg_subject,
                              dlp_disclaimer=dlp_disclaimer,
                              disclaimer_position=disclaimer_position,
                              msg_alt_host=msg_alt_host,
                              msg_bcc_rcpts=msg_bcc_rcpts,
                              msg_return_address=msg_return_address,
                              delivery_subject=delivery_subject,
                              notify_sender=notify_sender,
                              others_to_notify=others_to_notify,
                              return_addrs_to_notify=return_addrs_to_notify,
                              notify_subject=notify_subject,
                              include_orig_msg=include_orig_msg,
                              notification_template=notification_template)

    def dlp_message_action_duplicate(self,
                                     ac_name,
                                     name=None,
                                     description=None,
                                     msg_action=None,
                                     enable_encryption=None,
                                     encryption_rule=None,
                                     encryption_profile=None,
                                     encrypted_msg_subject=None,
                                     send_to_quarantine=None,
                                     quarantine_policy=None,
                                     cust_header_name=None,
                                     cust_header_value=None,
                                     msg_subject=None,
                                     dlp_disclaimer=None,
                                     disclaimer_position=None,
                                     msg_alt_host=None,
                                     msg_bcc_rcpts=None,
                                     msg_return_address=None,
                                     delivery_subject=None,
                                     notify_sender=None,
                                     others_to_notify=None,
                                     return_addrs_to_notify=None,
                                     notify_subject=None,
                                     include_orig_msg=None,
                                     notification_template=None,):
        """ Duplicates an existing DLP Message Action.

        Parameters:
        - `ac_name`: name of message action to edit. String.
        - `description`: description of the message action. Optional.
        - `msg_action`: message action to apply.
        Options available: Quarantine, Drop, Deliver.
        - `enable_encryption`: enable/disable encryption. Boolean.
        Available only if encryption is configured.
        - `encryption_rule`: rule to use for encryption.
        - `encryption_profile`: profile to use for encryption.
        - `encrypted_msg_subject`: subject of encrypted message.
        - `send_to_quarantine`: send message to quarantine. Boolean.
        - `quarantine_policy`: quarantine to send message to.
        - `cust_header_name`: set custom header name. String.
        - `cust_header_value`: set value of custom header. String.
        - `msg_subject`: set message subject. String.
        - `dlp_disclaimer`: DLP disclaimer to use.
        - `disclaimer_position`: position of DLP disclaimer in the message.
        Options available: below, above.
        - `msg_alt_host`: alternate host to send message to. String.
        - `msg_bcc_rcpts`: send copy of message to recipients. List.
        If you need to disable this option and leave corresponding text field with data -
        pass ${EMPTY}
        - `msg_return_address`: return address. String. Optional.
        - `delivery_subject`: subject to use for copy of message. String. Optional.
        - `notify_sender`: send DLP notification to sender. String.
        - `others_to_notify`: send DLP notification to additional recipients. List.
        If you need to disable this option and leave corresponding text field with data -
        pass ${EMPTY}
        - `return_addrs_to_notify`: set return address for DLP notification.
        - `notify_subject`: subject to use for DLP notification. String.
        - `include_orig_msg`: include original message to DLP notification. Boolean.
        - `notification_template`: DLP notification template to use. Select option.

        Return:
        None

        Example:
        | Dlp Message Action Duplicate |
        | ... | name_of_the_action |
        | ... | name=new_name |
        | ... | description=new description |
        | ... | include_orig_msg=${False} |

        | Dlp Message Action Duplicate |
        | ... | name_of_the_action |
        | ... | send_to_quarantine=${True} |
        | ... | description=new description |
        | ... | msg_action=Quarantine |
        """
        dup_img = \
        lambda row: "//table[@class='cols']/tbody/tr[%d]/td[3]/a/img" % row
        self._info('Duplicate DLP message action %s' % ac_name)
        self._open_page()

        (rowp, colp) = self._cell_indexes(ac_name, MA_TABLE)
        if rowp is None:
            raise ValueError, '"%s" message action is not present' % ac_name
        self.click_element(dup_img(rowp+1))
        self._fill_msg_action(name=name,
                              description=description,
                              msg_action=msg_action,
                              enable_encryption=enable_encryption,
                              encryption_rule=encryption_rule,
                              encryption_profile=encryption_profile,
                              encrypted_msg_subject=encrypted_msg_subject,
                              send_to_quarantine=send_to_quarantine,
                              quarantine_policy=quarantine_policy,
                              cust_header_name=cust_header_name,
                              cust_header_value=cust_header_value,
                              msg_subject=msg_subject,
                              dlp_disclaimer=dlp_disclaimer,
                              disclaimer_position=disclaimer_position,
                              msg_alt_host=msg_alt_host,
                              msg_bcc_rcpts=msg_bcc_rcpts,
                              msg_return_address=msg_return_address,
                              delivery_subject=delivery_subject,
                              notify_sender=notify_sender,
                              others_to_notify=others_to_notify,
                              return_addrs_to_notify=return_addrs_to_notify,
                              notify_subject=notify_subject,
                              include_orig_msg=include_orig_msg,
                              notification_template=notification_template)

    def dlp_message_action_delete(self, ac_name):
        """ Deletes DLP Message Action.

        Parameters:
        - `ac_name`:- Name of the message action to be deleted. String.

        Return:
            None

        Example:
        | Dlp Message Action Delete | name_of_the_action |
        """
        del_img = \
        lambda row: "%s/tbody/tr[%d]/td[4]/img" % (MA_TABLE, row)
        self._info('Deleting DLP message action %s' % ac_name)
        self._open_page()
        (rowp, colp) = self._cell_indexes(ac_name, MA_TABLE)
        if rowp is None:
            raise ValueError, '"%s" message action is not present' % ac_name
        self.click_element(del_img(rowp+1), "don't wait")
        self._click_continue_button()

    def dlp_custom_classifier_settings(self, entity_score_enabled=None):

        """ DLP Custom classifier settings to enable and disable use entity score option
        Parametes:
        "entity_score_enabled": - enable/disable min_score for custom classifier entity
        Example:
        To Enable:
        | Dlp Custom Classifier Settings | ${True}
        To Disable:
        | Dlp Custom Classifier Settings | ${False}
        """
        self._open_page()
        self.check_and_select(CC_SETTING, entity_score_enabled)
        self._click_submit_button()

    def dlp_custom_classifier_delete(self, classifier_name):
        """ Deletes custom classifier.

        Parameters:
        - `classifier_name`:- Name of the custom classifier to be deleted. String.

        Return:
            None

        Example:
        | Dlp Custom Classifier Delete | name_of_the_classifier |
        """
        del_img = \
        lambda row: "%s/tbody/tr[%d]/td[4]/img" % (CC_TABLE, row)
        self._info('Deleting Custom Classifier %s' % classifier_name)
        self._open_page()
        (rowp, colp) = self._cell_indexes(classifier_name, CC_TABLE)
        if rowp is None:
            raise ValueError, '"%s" custom classifier is not present' % classifier_name
        self.click_element(del_img(rowp+1), "don't wait")
        self._click_continue_button()

    def dlp_message_action_get_all(self):
        """ Returns a list of names of all the DLP message actions configured.

        Parameters:
        None

        Return:
        List. The names of all the DLP message actions configured.
        """
        self._info('Getting list of all configured DLP message actions')
        self._open_page()
        try:
            rows = int(self.get_matching_xpath_count("%s/tbody/tr" % MA_TABLE))
        except guiexceptions.SeleniumClientException:
            ma_text = self.get_text(POLICIES_DIV)
            return ma_text
        msg_actions = []
        for ma_indx in range(2, rows+1):
            msg_actn = \
            str(self.get_text("%s/tbody/tr[%d]/td" % (MA_TABLE, ma_indx)))
            msg_actions.append(msg_actn)
        return msg_actions

    def dlp_message_action_get_definition(self, ac_name):
        """ Returns an object with complete details of the given DLP message action.

        Parameters:
        - `ac_name`: Name of the message action whose details need to be
        fetched. String.

        Return:
        RecursiveCfgHolder - Returns an object of type RecursiveCfgHolder with
        all the details of the given message action.
        Allows to use '.' to access its keys, like
        cfg.name, cfg.description etc

        Example:
        | Dlp Message Action Get Definition | name_of_the_action |
        """
        self._info('Getting options of "%s" message action' % ac_name)
        self._open_page()
        self.items = cfgholder.RecursiveCfgHolder()
        self._click_link_to_edit(ac_name, MA_TABLE)
        _name_loc=\
        "xpath=.//table[@class='pairs']/tbody/tr[contains(.,'Name')]/td[1]"
        self.items.name = self.get_text(_name_loc)
        self.items.description = self.get_text(DESC_TA)
        self.items.msg_action = \
        self._get_selected_label(MSG_ACTION_DD)
        if self._is_visible(EN_ENC_CB):
            self.items.enable_encryption = self._is_checked(EN_ENC_CB)
        else:
            self.items.enable_encryption = False
        if self._is_element_present(ENC_RULE_DD):
            self.items.encryption_rule = \
            self._get_selected_label(ENC_RULE_DD)
        if self._is_element_present(ENC_PROF_DD):
            self.items.encryption_profile = \
            self._get_selected_label(ENC_PROF_DD)
        if self._is_element_present(ENC_MSG_SUB_TB):
            self.items.encrypted_msg_subject = \
            self.get_value(ENC_MSG_SUB_TB)
        self.items.send_to_quarantine = self._is_checked(QUARANTINE_CB)
        if self._is_checked(QUARANTINE_CB):
            self.items.quarantine_policy = \
            self._get_selected_label(QPOLICY_DD)
        self.items.msg_modifications.cust_header_name = \
        self.get_value(CUST_HDR_NAME_TB)
        self.items.msg_modifications.cust_header_value = \
        self.get_value(CUST_HDR_VALUE_TB)
        self.items.msg_modifications.msg_subject = \
        self.get_value(MSG_SUBJ_TB)
        if self._is_element_present(DLP_DISCLAIMER_DD):
            self.items.msg_modifications.dlp_disclaimer= \
            self._get_selected_label(DLP_DISCLAIMER_DD)
            if self._is_checked(BOTTOM_RB):
                self.items.msg_modifications.disclaimer_position = \
                self.get_text("%s/tbody/tr[3]/td[2]/label" % MOD_TABLE)
            elif self._is_checked(TOP_RB):
                self.items.msg_modifications.disclaimer_position = \
                self.get_text("%s/tbody/tr[3]/td[2]/label[2]" % MOD_TABLE)
        else:
            self.items.msg_modifications.dlp_disclaimer = \
            self.get_text("%s/tbody/tr/td" % MOD_TABLE)
        self.items.msg_delivery.msg_alt_host = \
        self.get_value(ALT_HOST_TB)
        if self._is_checked(BCC_RPT_CB):
            self.items.msg_delivery.msg_bcc_rcpts = \
            self.get_value(BCC_RCPTS_TB)
            self.items.msg_delivery.msg_return_address = \
            self.get_value(RETURN_TB)
            self.items.msg_delivery.delivery_subject = \
            self.get_value(BCC_SUBJ_TB)
        self.items.msg_notification.notify_sender = \
        self._is_checked(NOTIFY_SENDER_CB)
        if self._is_checked(NOTIFY_OTHER_CB):
            self.items.msg_notification.others_to_notify = \
            self.get_value(NOTIFY_OTHERS_TB)
        if self._is_checked(NOTIFY_SENDER_CB):
            self.items.msg_notification.return_addrs_to_notify=\
                self.get_value(NOTIFY_RETURN_TB)
            self.items.msg_notification.notify_subject = \
            self.get_value(NOTIFY_SUBJ_TB)
        self.items.msg_notification.include_orig_msg = \
        self._is_checked(INCLUDE_ORIG_CB)
        if self._is_visible(NOTIFY_TEMPLATE_DD):
            self.items.msg_notification.notification_template=\
                self._get_selected_label(NOTIFY_TEMPLATE_DD)
        else:
            self.items.msg_notification.notification_template = \
            self.get_text("%s/tbody/tr[2]/td/label" % NOTIFY_TABLE)
        return self.items

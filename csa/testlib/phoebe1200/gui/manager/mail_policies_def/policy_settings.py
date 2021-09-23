#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/manager/mail_policies_def/policy_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import re
import time
from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs

ADD_USER_BUTTON = "//input[@value='Add User...']"
SENDER_RADIOGROUP = {'Any Sender': "//input[@id='Any']",
                     'Following Senders': "//input[@id='SelSender']",
                     'Following Senders are Not': "//input[@id='SenderNot']"}
RECIPIENT_RADIOGROUP = {'Any Recipient': "//input[@id='RecipientAny']",
                        'Following Recipient': "//input[@id='SelRecipient']",
                        'Following Recipient are Not': "//input[@id='RecipientNot']"}
SENDER_ADDRESSES_RADIOGROUP = {'Email Address': "//textarea[@id='addressListsender']",
                               'LDAP Group': ("//select[@id='ldapQuerysender']",
                                              "//input[@id='ldapGroupsender']"),
                               'Sender List': "//select[@id='rpolicysenderList[]']"}
RECIPIENT_ADDRESSES_RADIOGROUP = {'Condition': "//select[@id='condition']",
                                  'Email Address': "//textarea[@id='addressListrcpt']",
                                  'LDAP Group': ("//select[@id='ldapQueryrcpt']",
                                                 "//input[@id='ldapGrouprcpt']"),
                                  'Recipient List': "//select[@id='rpolicyrcptList[]']",
                                  'Excluded Email Address': "//textarea[@id='addressListrcptnot']",
                                  'Excluded LDAP Group': ("//select[@id='ldapQueryrcptnot']",
                                                          "//input[@id='ldapGrouprcptnot']"),
                                  'Excluded Recipient List': "//select[@id='rpolicyrcptnotList[]']"}
SENDER_LDAP_GROUP_ADD_BUTTON = "//input[@id='AddGroupsender']"
SENDER_LDAP_GROUP_REMOVE_BUTTON = "//input[@id='btnDeleteGrpsender']"
RECIPIENT_LDAP_GROUP_ADD_BUTTON = "//input[@id='AddGrouprcpt']"
RECIPIENT_LDAP_GROUP_REMOVE_BUTTON = "//input[@id='btnDeleteGrprcpt']"
EXCLUDED_RECIPIENT_LDAP_GROUP_ADD_BUTTON = "//input[@id='AddGrouprcptnot']"
EXCLUDED_RECIPIENT_LDAP_GROUP_REMOVE_BUTTON = "//input[@id='btnDeleteGrprcptnot']"
OK_BUTTON = "//input[@value='OK']"


class BasePolicySettings(InputsOwner):
    NAME = ('Policy Name',
            "//input[@name='rpolicyName']")
    INSERT_BEFORE_COMBO = ('Insert Before',
                           "//select[@name='rpolicyNewIdx']")

    RECIPIENT_OPTION = ('Recipient Option', 'Any Recipient')
    RECIPIENT_CONDITION = ('Recipient Condition', None)
    RECIPIENTS_TO_ADD = ('Recipients to Add', None)
    RECIPIENTS_TO_EXCLUDE = ('Recipients to Exclude', None)
    SENDER_OPTION = ('Sender Option', 'Any Sender')
    SENDERS_TO_ADD = ('Senders to Add', None)

    SENDERS_TO_DELETE = ('Senders to Delete', None)
    RECIPIENTS_TO_DELETE = ('Recipients to Delete', None)
    EXCLUDED_RECIPIENTS_TO_DELETE = ('Excluded Recipients to Delete', None)

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    def _set_insert_before_combo(self, before_policy_name):
        combo_locator = self.INSERT_BEFORE_COMBO[1]
        all_values = self.gui.get_list_items(combo_locator)
        dest_value = filter(lambda x: x.find('(%s)' % (before_policy_name,)) > 0,
                            all_values)
        if dest_value:
            self.gui.select_from_list(combo_locator, dest_value[0])
        else:
            raise ValueError('There is no mail policy named "%s"' % \
                             (before_policy_name,))

    def _get_user_dict(self, user_type, users=None, excluded_users=None):
        user_dict = {}
        user_email_addresses = ''
        user_ldap_groups = ''

        if users is not 'skip':
            if users is not None:
                users_to_add = map(lambda x: x.strip(), users.split(','))
                if len(users_to_add) > 0:
                    for user in users_to_add:
                        if user.find('@') < 0 and user.find(':') < 0:
                            raise ValueError('Incorrect "%s" "%s"' % (user_type, user,))

                        if user.find('@') > 0:
                            user_email_addresses += user + ','
                        if user.find(':') > 0:
                            user_ldap_groups += user + ','

                    user_email_addresses = user_email_addresses.lstrip(',').rstrip(',')
                    user_ldap_groups = user_ldap_groups.lstrip(',').rstrip(',')
                    user_dict[user_type + '_email_addresses'] = user_email_addresses
                    user_dict[user_type + '_ldap_groups'] = user_ldap_groups
            else:
                raise ValueError('"%s" address cannot be EMPTY' % (user_type,))

        user_email_addresses = ''
        user_ldap_groups = ''
        if user_type is 'recipient' and excluded_users:
            users_to_exclude = map(lambda x: x.strip(), excluded_users.split(','))
            if len(users_to_exclude) > 0:
                for user in users_to_exclude:
                    if user.find('@') < 0 and user.find(':') < 0:
                        raise ValueError('Incorrect "%s" "%s"' % (user_type, user,))

                    if user.find('@') > 0:
                        user_email_addresses += user + ','
                    if user.find(':') > 0:
                        user_ldap_groups += user + ','

                user_email_addresses = user_email_addresses.lstrip(',').rstrip(',')
                user_ldap_groups = user_ldap_groups.lstrip(',').rstrip(',')
                user_dict[user_type + '_excluded_email_addresses'] = user_email_addresses
                user_dict[user_type + '_excluded_ldap_groups'] = user_ldap_groups

        return user_dict

    def _add_senders(self, sender_option, sender_list):
        self.gui._click_radio_button(SENDER_RADIOGROUP[sender_option])
        if sender_option is not 'Any Sender':
            sndr_dict = self._get_user_dict('sender', sender_list)
            if sndr_dict.has_key('sender_email_addresses') and sndr_dict['sender_email_addresses']:
                self.gui.input_text(SENDER_ADDRESSES_RADIOGROUP['Email Address'], \
                                    sndr_dict['sender_email_addresses'])
            if sndr_dict.has_key('sender_ldap_groups') and sndr_dict['sender_ldap_groups']:
                ldap_groups_to_add = map(lambda x: x.strip(),
                                         sndr_dict['sender_ldap_groups'].split(','))
                for ldap_group in ldap_groups_to_add:
                    ldap_query, group_name = \
                        tuple(map(lambda x: x.strip(), ldap_group.split(':')))
                    self.gui.select_from_list( \
                        SENDER_ADDRESSES_RADIOGROUP['LDAP Group'][0], ldap_query)
                    self.gui.input_text( \
                        SENDER_ADDRESSES_RADIOGROUP['LDAP Group'][1], group_name)
                    self.gui.click_button( \
                        SENDER_LDAP_GROUP_ADD_BUTTON, 'don\'t wait')

    def _add_recipients(self,
                        recipient_option, recipient_list,
                        recipient_condition=None, excluded_list=None):
        if recipient_option is not 'Any Recipient':
            rcpt_dict = self._get_user_dict('recipient', recipient_list, excluded_list)
            if recipient_list is not 'skip':
                self.gui._click_radio_button( \
                    RECIPIENT_RADIOGROUP['Following Recipient'])
                if recipient_condition:
                    self.gui.select_from_list( \
                        RECIPIENT_ADDRESSES_RADIOGROUP['Condition'], recipient_condition)

                if rcpt_dict.has_key('recipient_email_addresses') and \
                        rcpt_dict['recipient_email_addresses']:
                    self.gui.input_text(RECIPIENT_ADDRESSES_RADIOGROUP['Email Address'], \
                                        rcpt_dict['recipient_email_addresses'])
                if rcpt_dict.has_key('recipient_ldap_groups') and \
                        rcpt_dict['recipient_ldap_groups']:
                    ldap_groups_to_add = map(lambda x: x.strip(),
                                             rcpt_dict['recipient_ldap_groups'].split(','))
                    for ldap_group in ldap_groups_to_add:
                        ldap_query, group_name = \
                            tuple(map(lambda x: x.strip(), ldap_group.split(':')))
                        self.gui.select_from_list( \
                            RECIPIENT_ADDRESSES_RADIOGROUP['LDAP Group'][0], ldap_query)
                        self.gui.input_text( \
                            RECIPIENT_ADDRESSES_RADIOGROUP['LDAP Group'][1], group_name)
                        self.gui.click_button( \
                            RECIPIENT_LDAP_GROUP_ADD_BUTTON, 'don\'t wait')

            if excluded_list:
                self.gui._select_checkbox( \
                    RECIPIENT_RADIOGROUP['Following Recipient are Not'])
                # self.gui._click_radio_button(\
                #    RECIPIENT_RADIOGROUP['Following Recipient are Not'])
                if rcpt_dict.has_key('recipient_excluded_email_addresses') and \
                        rcpt_dict['recipient_excluded_email_addresses']:
                    self.gui.input_text(RECIPIENT_ADDRESSES_RADIOGROUP['Excluded Email Address'], \
                                        rcpt_dict['recipient_excluded_email_addresses'])
                if rcpt_dict.has_key('recipient_excluded_ldap_groups') and \
                        rcpt_dict['recipient_excluded_ldap_groups']:
                    ldap_groups = map(lambda x: x.strip(),
                                      rcpt_dict['recipient_excluded_ldap_groups'].split(','))
                    for ldap_group in ldap_groups:
                        ldap_query, group_name = \
                            tuple(map(lambda x: x.strip(), ldap_group.split(':')))
                        self.gui.select_from_list( \
                            RECIPIENT_ADDRESSES_RADIOGROUP['Excluded LDAP Group'][0], ldap_query)
                        self.gui.input_text( \
                            RECIPIENT_ADDRESSES_RADIOGROUP['Excluded LDAP Group'][1], group_name)
                        self.gui.click_button( \
                            EXCLUDED_RECIPIENT_LDAP_GROUP_ADD_BUTTON, 'don\'t wait')

    def set(self, new_value, add_user=None):
        if add_user:
            self.gui.click_button(ADD_USER_BUTTON)
        if self.RECIPIENTS_TO_ADD[0] in new_value:
            if self.RECIPIENT_CONDITION[0] in new_value:
                self._add_recipients(new_value['Recipient Option'], \
                                     new_value[self.RECIPIENTS_TO_ADD[0]], \
                                     new_value[self.RECIPIENT_CONDITION[0]])
            else:
                self._add_recipients(new_value['Recipient Option'], \
                                     new_value[self.RECIPIENTS_TO_ADD[0]])
        if self.RECIPIENTS_TO_EXCLUDE[0] in new_value:
            self._add_recipients(new_value['Recipient Option'], \
                                 'skip', None, new_value[self.RECIPIENTS_TO_EXCLUDE[0]])
        if self.SENDERS_TO_ADD[0] in new_value:
            self._add_senders(new_value['Sender Option'], \
                              new_value[self.SENDERS_TO_ADD[0]])
        self.gui.click_button(OK_BUTTON)
        time.sleep(2)
        self._set_edits(new_value, self.NAME)
        if self.INSERT_BEFORE_COMBO[0] in new_value:
            self._set_insert_before_combo(new_value[self.INSERT_BEFORE_COMBO[0]])


class AddPolicySettings(BasePolicySettings):
    @set_speed(0, 'gui')
    def set(self, new_value):
        if new_value.has_key(self.RECIPIENTS_TO_ADD[0]) \
                or new_value.has_key(self.SENDERS_TO_ADD[0]):
            assert ((self.RECIPIENTS_TO_ADD[0] in new_value) or \
                    (self.SENDERS_TO_ADD[0] in new_value))
        super(AddPolicySettings, self).set(new_value, add_user=True)


class EditPolicySettings(BasePolicySettings):
    def _delete_existing_senders(self, senders_to_delete):
        sndr_dict = self._get_user_dict('sender', senders_to_delete)

        if sndr_dict.has_key('sender_email_addresses') and sndr_dict['sender_email_addresses']:
            existing_sndr_email_addrs = self.gui.get_text( \
                SENDER_ADDRESSES_RADIOGROUP['Email Address'])
            existing_sndr_email_addrs += ','
            for sndr_email_to_delete in [sndr_dict['sender_email_addresses']]:
                revised_sndr_email_addrs = \
                    existing_sndr_email_addrs.replace(sndr_email_to_delete, '')
                revised_sndr_email_addrs = re.sub(r'\s+?,\s+,\s+?', '', \
                                                  revised_sndr_email_addrs).lstrip(',').rstrip(',')
            self.gui.input_text(SENDER_ADDRESSES_RADIOGROUP \
                                    ['Email Address'], revised_sndr_email_addrs)

        if sndr_dict.has_key('sender_ldap_groups') and sndr_dict['sender_ldap_groups']:
            sndr_ldap_groups_to_delete = map(lambda x: x.strip(),
                                             sndr_dict['sender_ldap_groups'].split(','))

            for sndr_ldap_group_to_delete in sndr_ldap_groups_to_delete:
                sndr_ldap_group_info = map(lambda x: x.strip(),
                                           sndr_ldap_group_to_delete.split(':'))
                sndr_ldap_group_entry = 'ldap(' + \
                                        sndr_ldap_group_info[1] + ',' + \
                                        sndr_ldap_group_info[0] + ')'
                try:
                    self.gui.select_from_list( \
                        SENDER_ADDRESSES_RADIOGROUP['Sender List'], sndr_ldap_group_entry)
                    self.gui.click_button(SENDER_LDAP_GROUP_REMOVE_BUTTON, 'don\'t wait')
                except Exception:
                    raise ValueError('There is no "%s" ldap entry available for removal.' \
                                     % (sndr_ldap_group_entry,))

    def _delete_existing_recipients(
            self, recipients_to_delete, excluded_recipients_to_delete=None):

        rcpt_dict = self._get_user_dict(
            'recipient', recipients_to_delete, excluded_recipients_to_delete)

        if recipients_to_delete is not 'skip' and \
                rcpt_dict.has_key('recipient_email_addresses') and \
                rcpt_dict['recipient_email_addresses']:
            existing_rcpt_email_addrs = self.gui.get_text( \
                RECIPIENT_ADDRESSES_RADIOGROUP['Email Address'])
            existing_rcpt_email_addrs += ','
            for rcpt_email_to_delete in [rcpt_dict['recipient_email_addresses']]:
                revised_rcpt_email_addrs = \
                    existing_rcpt_email_addrs.replace(rcpt_email_to_delete + ',', '')
                revised_rcpt_email_addrs = revised_rcpt_email_addrs.lstrip(',').rstrip(',')
            self.gui.input_text(RECIPIENT_ADDRESSES_RADIOGROUP \
                                    ['Email Address'], revised_rcpt_email_addrs)

        if recipients_to_delete is not 'skip' and \
                rcpt_dict.has_key('recipient_ldap_groups') and \
                rcpt_dict['recipient_ldap_groups']:
            rcpt_ldap_groups_to_delete = map(lambda x: x.strip(),
                                             rcpt_dict['recipient_ldap_groups'].split(','))

            for rcpt_ldap_group_to_delete in rcpt_ldap_groups_to_delete:
                rcpt_ldap_group_info = map(lambda x: x.strip(),
                                           rcpt_ldap_group_to_delete.split(':'))
                rcpt_ldap_group_entry = 'ldap(' + \
                                        rcpt_ldap_group_info[1] + ',' + \
                                        rcpt_ldap_group_info[0] + ')'
                try:
                    self.gui.select_from_list( \
                        RECIPIENT_ADDRESSES_RADIOGROUP['Recipient List'], rcpt_ldap_group_entry)
                    self.gui.click_button(RECIPIENT_LDAP_GROUP_REMOVE_BUTTON, 'don\'t wait')
                except Exception:
                    raise ValueError('There is no "%s" ldap entry available for removal.' \
                                     % (rcpt_ldap_group_entry,))

        if rcpt_dict.has_key('recipient_excluded_email_addresses') and \
                rcpt_dict['recipient_excluded_email_addresses']:
            existing_rcpt_excluded_email_addrs = self.gui.get_text( \
                RECIPIENT_ADDRESSES_RADIOGROUP['Excluded Email Address'])
            existing_rcpt_excluded_email_addrs += ','

            for rcpt_excluded_email_to_delete in \
                    [rcpt_dict['recipient_excluded_email_addresses']]:
                revised_rcpt_excluded_email_addrs = \
                    existing_rcpt_excluded_email_addrs.replace( \
                        rcpt_excluded_email_to_delete + ',', '')
                revised_rcpt_excluded_email_addrs = \
                    revised_rcpt_excluded_email_addrs.lstrip(',').rstrip(',')
            self.gui.input_text(RECIPIENT_ADDRESSES_RADIOGROUP \
                                    ['Excluded Email Address'], revised_rcpt_excluded_email_addrs)

        if rcpt_dict.has_key('recipient_excluded_ldap_groups') and \
                rcpt_dict['recipient_excluded_ldap_groups']:
            rcpt_excluded_ldap_groups_to_delete = map(lambda x: x.strip(),
                                                      rcpt_dict['recipient_excluded_ldap_groups'].split(','))

            for rcpt_excluded_ldap_group_to_delete in rcpt_excluded_ldap_groups_to_delete:
                rcpt_excluded_ldap_group_info = map(lambda x: x.strip(),
                                                    rcpt_excluded_ldap_group_to_delete.split(':'))
                rcpt_excluded_ldap_group_entry = 'ldap(' + \
                                                 rcpt_excluded_ldap_group_info[1] + ',' + \
                                                 rcpt_excluded_ldap_group_info[0] + ')'
                try:
                    self.gui.select_from_list( \
                        RECIPIENT_ADDRESSES_RADIOGROUP['Excluded Recipient List'], \
                        rcpt_excluded_ldap_group_entry)
                    self.gui.click_button(EXCLUDED_RECIPIENT_LDAP_GROUP_REMOVE_BUTTON, \
                                          'don\'t wait')
                except Exception:
                    raise ValueError('There is no "%s" ldap entry available for removal.' \
                                     % (rcpt_excluded_ldap_group_entry,))

    @set_speed(0, 'gui')
    def set(self, new_value):
        self.gui.click_button("//input[@value='Edit']")
        if self.SENDERS_TO_DELETE[0] in new_value:
            self._delete_existing_senders(new_value[self.SENDERS_TO_DELETE[0]])
        if self.RECIPIENTS_TO_DELETE[0] in new_value:
            self._delete_existing_recipients(new_value[self.RECIPIENTS_TO_DELETE[0]])
        if self.EXCLUDED_RECIPIENTS_TO_DELETE[0] in new_value:
            self._delete_existing_recipients('skip', new_value[self.EXCLUDED_RECIPIENTS_TO_DELETE[0]])
        super(EditPolicySettings, self).set(new_value, add_user=False)

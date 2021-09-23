#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/policyconfig.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

"""
IAF 2 CLI command: policyconfig.py
"""
import clictorbase
from clictorbase import REQUIRED, DEFAULT, IafCliError, IafCliParamMap, IafCliConfiguratorBase
from sal.containers.yesnodefault import is_yes, is_no, YES, NO
from sal.deprecated.expect import EXACT, REGEX
import re

DEBUG = True
ENDOFCOMMAND = False
CONTINUE = True


class policyconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('policyconfig')
        return self

    def choose(self, policy_type=DEFAULT):
        global mail_policy_type
        if policy_type:
            if (policy_type == '1') | (policy_type.lower() == 'incoming'):
                mail_policy_type = 'Incoming'
            if (policy_type == '2') | (policy_type.lower() == 'outgoing'):
                mail_policy_type = 'Outgoing'
            if (policy_type == '3') | (policy_type.lower() == 'match'):
                mail_policy_type='Match'
        else:
            mail_policy_type = 'Incoming'
        self._query_select_list_item(mail_policy_type)

        return policyconfigMain(self._get_sess())

    def _init_param_map(self, kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['add_senders'] = ['Add senders for this policy', REQUIRED]
        if kwargs.has_key('add_senders') and is_yes(kwargs['add_senders']):
            param_map['sender_policy_applies_for'] = \
                ['Policy is applicable for', DEFAULT, 1]
            if kwargs.has_key('sender_policy_applies_for') \
                    and kwargs['sender_policy_applies_for'] != '1':
                param_map['sender_add_domain_entries'] = \
                    ['Enter domain entries', DEFAULT]
                param_map['sender_domain_entries'] = \
                    ['Enter the senders for this policy', REQUIRED]
                param_map['sender_add_ldap_group_membership'] = \
                    ['Enter LDAP group memberships', DEFAULT]
                if kwargs.has_key('sender_add_ldap_group_membership') \
                        and is_yes(kwargs['sender_add_ldap_group_membership']):
                    param_map['sender_ldap_group_name'] = \
                        ['Enter groupname for LDAP query', REQUIRED]
                    param_map['sender_ldap_group_query'] = \
                        ['Please select an LDAP group query', DEFAULT, 1]
                    param_map['sender_add_another_group_membership'] = \
                        ['Add another LDAP group membership', NO]

        param_map['add_receivers'] = ['Add receivers for this policy', REQUIRED]
        if kwargs.has_key('add_receivers') and is_yes(kwargs['add_receivers']):
            param_map['receiver_policy_applies_for'] = \
                ['Policy is applicable for', DEFAULT, 1]
            if kwargs.has_key('receiver_policy_applies_for') \
                    and kwargs['receiver_policy_applies_for'] != '1':
                param_map['receiver_add_domain_entries'] = \
                    ['Enter domain entries', DEFAULT]
                param_map['receiver_domain_entries'] = \
                    ['Enter the receivers for this policy', REQUIRED]
                param_map['receiver_add_ldap_group_membership'] = \
                    ['Enter LDAP group memberships', DEFAULT]
                if kwargs.has_key('receiver_add_ldap_group_membership') \
                        and is_yes(kwargs['receiver_add_ldap_group_membership']):
                    param_map['receiver_ldap_group_name'] = \
                        ['Enter groupname for LDAP query', None]
                    param_map['receiver_ldap_group_query'] = \
                        ['Please select an LDAP group query', DEFAULT, 1]
                    param_map['receiver_add_another_group_membership'] = \
                        ['Add another LDAP group membership', DEFAULT]

            if kwargs.has_key('receiver_policy_applies_for') \
                    and kwargs['receiver_policy_applies_for'] == '3':
                param_map['add_exceptions'] = ['Enter Exceptions', DEFAULT]
                if kwargs.has_key('add_exceptions') \
                        and is_yes(kwargs['add_exceptions']):
                    param_map['exception_add_domain_entries'] = \
                        ['Enter domain entries', DEFAULT]
                    param_map['exception_domain_entries'] = \
                        ['Enter the exceptions for this policy', REQUIRED]
                    param_map['exception_add_ldap_group_membership'] = \
                        ['Enter LDAP group membership exceptions', DEFAULT]
                    if kwargs.has_key('exception_add_ldap_group_membership') \
                            and is_yes(kwargs['exception_add_ldap_group_membership']):
                        param_map['exception_ldap_group_name'] = \
                            ['Enter groupname for LDAP query', REQUIRED]
                        param_map['exception_ldap_group_query'] = \
                            ['Please select an LDAP group query', DEFAULT, 1]
                        param_map['exception_add_another_group_membership'] = \
                            ['Add another LDAP group membership exception', DEFAULT]

        return param_map


class policyconfigMain(clictorbase.IafCliConfiguratorBase):
    class PolicyDeleteError(IafCliError):
        pass

    class PolicyDeleteAttemptError(IafCliError):
        pass

    class PolicyMoveError(IafCliError):
        pass

    class PolicyMemberEmailError(IafCliError):
        pass

    class AsciiCharactersError(IafCliError):
        pass

    class PolicyRecipientNameError(IafCliError):
        pass

    class MachineModeError(IafCliError):
        pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('The entry you have entered is invalid',
             EXACT): self.PolicyDeleteError,
            ('cannot be \S+ position of default entry',
             REGEX): self.PolicyMoveError,
            ('Delete attempted after last non-default entry',
             EXACT): self.PolicyDeleteAttemptError,
            ('Matches \S+ \S+ address',
             REGEX): self.PolicyMemberEmailError,
            ('Non ASCII characters are not allowed',
             EXACT): self.AsciiCharactersError,
            ('A Per-recipient policy name is a non-empty',
             EXACT): self.PolicyRecipientNameError,
            ('This command is restricted to',
             EXACT): self.MachineModeError,
        })
        import handlecluster
        handlecluster.handle_cluster_questions(sess)

    def new(self, input_dict=None, **kwargs):
        self.newline = 1

        self._info(kwargs)
        param_map = policyconfig(None)._init_param_map(kwargs)
        param_map['policy_name'] = ['Enter the name for this policy', REQUIRED]
        param_map['add_senders_and_receivers'] = ['Add entry for policy senders/receivers', DEFAULT]
        param_map['add_another_entry'] = ['Add another entry', NO]

        param_map['antispam_enable'] = ['enable Anti-Spam support', NO]
        if kwargs.has_key('antispam_enable') \
                and is_yes(kwargs['antispam_enable']):
            param_map['antispam_table'] = ['policy table default', YES]

        param_map['antivirus_enable'] = ['enable Anti-Virus support', NO]
        if kwargs.has_key('antivirus_enable') \
                and is_yes(kwargs['antivirus_enable']):
            param_map['antivirus_table'] = ['policy table default', YES]

        param_map['advancedmalware_enable'] = ['enable Advanced-Malware protection', NO]
        if kwargs.has_key('advancedmalware_enable') \
                and is_yes(kwargs['advancedmalware_enable']):
            param_map['advancedmalware_table'] = ['policy table default', YES]

        param_map['content_filter_enable'] = ['enable Content Filters', NO]
        if kwargs.has_key('content_filter_enable') \
                and is_yes(kwargs['content_filter_enable']):
            param_map['content_filter_table'] = ['policy table default', YES]

        param_map['vof_enable'] = ['enable Outbreak Filters', NO]
        if kwargs.has_key('vof_enable') \
                and is_yes(kwargs['vof_enable']):
            param_map['vof_table'] = ['policy table default', YES]

        param_map['graymail_enable'] = ['enable Graymail support', NO]
        if kwargs.has_key('graymail_enable') \
                and is_yes(kwargs['graymail_enable']):
            param_map['graymail_table'] = ['policy table default', YES]

        param_map['assign_user_role'] = ['assign any user roles to access', NO]

        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        self._process_input(param_map)

        buf = self.getbuf()
        self._info(buf)

        self._to_the_top(self.newline)

    def edit(self, policy=REQUIRED):
        self._query_response('EDIT')
        self._query_select_list_item(policy, exact_match=True)
        return policyconfigEdit(self._get_sess())

    def delete(self, policy=REQUIRED):
        self.newline = 1
        self._query_response('DELETE')
        self._query_select_list_item(policy, exact_match=True)
        self._to_the_top(self.newline)

    def print_policy(self, policy=REQUIRED):
        self.newline = 1
        self._query_response('PRINT')
        self._query_select_list_item(policy, exact_match=True)
        self._expect('\n')
        raw = self._read_until(mail_policy_type + ' Mail Policy Configuration')
        self._to_the_top(self.newline)
        return raw

    def search(self, policy_member=REQUIRED):
        self.newline = 1
        self._query_response('SEARCH')
        self._query_response(policy_member)
        raw = self._read_until(mail_policy_type + ' Mail Policy Configuration')
        self._to_the_top(self.newline)
        return raw

    def move(self, entry_to_move=REQUIRED, insert_before=REQUIRED):
        self.newline = 1
        self._query_response('MOVE')
        self._query_select_list_item(entry_to_move, exact_match=True)
        self._query_select_list_item(insert_before, exact_match=True)
        self._to_the_top(self.newline)

    def filters(self, file_name=REQUIRED, encoding=DEFAULT):
        self._query_response('FILTERS')
        return policyconfigFilters(self._get_sess())

    def clear(self, confirm=DEFAULT):
        self.newline = 1
        self._query_response('CLEAR')
        self._query_response(confirm)
        self._to_the_top(self.newline)

    def clusterset(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Settings')

        param_map['action'] = ['can copy the current settings', REQUIRED, True]
        param_map['group_copy'] = ['group name or number to copy', DEFAULT]
        param_map['machine_copy'] = ['machine name or number to copy', DEFAULT]
        param_map['cluster_copy'] = ['cluster name or number to copy', DEFAULT]
        param_map['group_move'] = ['group name or number to move', DEFAULT]
        param_map['machine_move'] = ['machine name or number to move', DEFAULT]
        param_map['cluster_move'] = ['cluster name or number to move', DEFAULT]
        param_map['delete_cluster'] = ['from the cluster', DEFAULT]
        param_map['delete_group'] = ['from the Group', DEFAULT]
        param_map['delete_machine'] = ['from the machine', DEFAULT]
        param_map['force'] = ['you sure you want to continue', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('CLUSTERSET')
        return self._process_input(param_map)

    def clustershow(self):
        self._query_response('CLUSTERSHOW')
        raw = self._read_until('Choose the operation')
        self._to_the_top(2)
        return raw

    def headerpriorityadd(self, input_dict=None, **kwargs):
        self.newline=1
        self._debug(kwargs)
        param_map = policyconfig(None)._init_param_map(kwargs)
        param_map['from_header'] =    ['Add header "From" Header', 2]
        param_map['replyto_header'] = ['Add header "Reply-To" Header', 2]
        param_map['sender_header'] =  ['Add header "Sender" Header', 2]
        param_map.update(input_dict or kwargs)
        self._query_response('ADD')
        self._process_input(param_map)
        self._to_the_top(self.newline)

    def headerprioritydelete(self, priority_number=REQUIRED):
        self.newline=1
        self._query_response('REMOVE')
        self._query_response(priority_number)
        self._expect('\n')
        self._to_the_top(self.newline)

class policyconfigEdit(clictorbase.IafCliConfiguratorBase):
    """policyconfig->Edit"""

    class PolicyDeleteError(IafCliError):
        pass

    class PolicyMemberNameError(IafCliError):
        pass

    class PolicyMemberCreateError(IafCliError):
        pass

    class PolicyMemberDeleteError(IafCliError):
        pass

    class PolicyMemberEmailError(IafCliError):
        pass

    class AsciiCharactersError(IafCliError):
        pass

    class PolicyRecipientNameError(IafCliError):
        pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('There is already a policy with the new name',
             EXACT): self.PolicyMemberNameError,
            ('is already a member of this policy',
             EXACT): self.PolicyMemberCreateError,
            ('Matches \S+ \S+ address',
             REGEX): self.PolicyMemberEmailError,
            ('There is only one member in the policy',
             EXACT): self.PolicyMemberDeleteError,
            ('Non ASCII characters are not allowed',
             EXACT): self.AsciiCharactersError,
            ('A Per-recipient policy name is a non-empty',
             EXACT): self.PolicyRecipientNameError
        })

    def name(self, policy_name=DEFAULT):
        self.newline = 2
        self._query_response('NAME')
        self._query_response(policy_name)
        self._to_the_top(self.newline)

    def new(self, input_dict=None, **kwargs):
        self.newline = 2
        param_map = policyconfig(None)._init_param_map(kwargs)
        self._info(kwargs)
        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        self._process_input(param_map)

        buf = self.getbuf()
        self._info(buf)

    def delete(self, member=DEFAULT):
        self.newline = 2
        self._query_response('DELETE')
        self._query_select_list_item(member)
        self._to_the_top(self.newline)

    def print_members(self):
        self.newline = 2
        self._query_response('PRINT')
        self._expect('\n')
        raw = self._read_until('Choose the operation you want to perform')
        self._to_the_top(self.newline)
        return raw

    def antispam(self):
        self._query_response('ANTISPAM')
        return policyconfigEditAntispam(self._get_sess())

    def antivirus(self):
        self._query_response('ANTIVIRUS')
        return policyconfigEditAntivirus(self._get_sess())

    def advancedmalware(self):
        self._query_response('ADVANCEDMALWARE')
        return policyconfigEditAdvancedmalware(self._get_sess())

    def vof(self):
        self._query_response('OUTBREAK')
        return policyconfigEditVof(self._get_sess())

    def filters(self):
        self._query_response('FILTERS')
        return policyconfigEditFilters(self._get_sess())

    def assign(self):
        self._query_response('ASSIGN')
        return policyconfigEditAssignUser(self._get_sess())

    def graymail(self):
        self._query_response('GRAYMAIL')
        return policyconfigEditGraymail(self._get_sess())


class policyconfigEditAssignUser(clictorbase.IafCliConfiguratorBase):
    """policyconfig->Edit->Assign"""

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

    def add(self, user_role=DEFAULT):
        self.newline = 3
        self._query_response('ADD')
        self._query_response(user_role)
        self._to_the_top(self.newline)

    def delete(self, user_role=DEFAULT):
        self.newline = 3
        self._query_response('DELETE')
        self._query_response(user_role)
        self._to_the_top(self.newline)


class policyconfigEditAntispam(clictorbase.IafCliConfiguratorBase):
    """policyconfig->Edit->Antispam"""

    class AntispamHeaderError(IafCliError):
        pass

    class AntispamLevelError(IafCliError):
        pass

    class FilterExistError(IafCliError):
        pass

    class HeaderCharacterError(IafCliError):
        pass

    class HeaderStringsError(IafCliError):
        pass

    class HeaderLengthError(IafCliError):
        pass

    class InvalidCharacterError(IafCliError):
        pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('The header text must be less than 100',
             EXACT): self.AntispamHeaderError,
            ('No machines at current level',
             EXACT): self.AntispamLevelError,
            ('Must have at least 1 filter',
             EXACT): self.FilterExistError,
            ('Headers may contain any character except',
             EXACT): self.HeaderCharacterError,
            ('Headers may not be empty strings',
             EXACT): self.HeaderStringsError,
            ('Custom header text has a maximum length of 128',
             EXACT): self.HeaderLengthError,
            ('Invalid character', EXACT): self.InvalidCharacterError,
        })

    def disable(self):
        self.newline = 2
        self._query_response('DISABLE')
        self._to_the_top(self.newline)

    def enable(self, spam_dict=None, suspected_spam_dict=None,
               marketing_spam_dict=None, new_policy=False):
        try:
            status = REQUIRED
        except NameError:
            status = self.REQUIRED
        if not new_policy:
            self._query_response('ENABLE')
        self.get_spam_param_map(spam_dict, status)
        self.get_suspected_spam_param_map(suspected_spam_dict, new_policy, status)
        self._to_the_top(2)

    def edit(self, spam_dict=None, suspected_spam_dict=None, marketing_spam_dict=None):
        self._query_response('EDIT')
        self.get_spam_param_map(spam_dict)
        self.get_suspected_spam_param_map(suspected_spam_dict)
        self._to_the_top(2)

    def default(self):
        self.newline = 2
        self._query_response('DEFAULT')
        self._to_the_top(self.newline)

    def get_spam_param_map(self, spam_dict=None, status=DEFAULT, **kwargs):
        param_map = IafCliParamMap(end_of_command= \
                                       'Do you want to enable special')

        param_map['use_ipas'] = ['to use IronPort Anti-Spam', DEFAULT]
        param_map['use_ims'] = ['to use Intelligent Multi-Scan', DEFAULT]
        param_map['use_brightmail'] = ['to use Symantec Brightmail', DEFAULT]
        param_map['use_multiscan'] = ['to use Multiscan Service', DEFAULT]
        param_map['use_cloudmark'] = ['to use Cloudmark Service', DEFAULT]
        param_map['score_ims'] = ['Intelligent Multi-Scan spam threshold', [DEFAULT, DEFAULT]]
        param_map['score'] = ['IronPort Anti-Spam spam threshold', [DEFAULT, DEFAULT]]
        param_map['score_cloudmark'] = \
            ['Service Provider Edition spam threshold', [DEFAULT, DEFAULT]]
        param_map['action_spam'] = \
            ['to do with messages identified as spam', DEFAULT, True]
        param_map['archive'] = \
            ['to archive messages identified as spam', DEFAULT]
        param_map['text_add'] = \
            ['add text to the subject of messages', DEFAULT, True]
        param_map['text'] = \
            ['What text do you want to', DEFAULT]
        param_map['sent_to'] = \
            ['spam sent to an external quarantine', DEFAULT]
        param_map['host'] = \
            ['host to send spam ', status]
        param_map['header'] = \
            ['to add a custom header', DEFAULT]
        param_map['header_name'] = \
            ['Enter the name of the header', status]
        param_map['content'] = \
            ['text for the content', status]
        param_map['envelope_recipient'] = \
            ['spam sent to an alternate envelope recipient', DEFAULT]
        param_map['email'] = \
            ['email address to send spam', status]

        # backwards compatibility for code written for phoebe46-47
        # which only allowed one antispam engine
        try:
            if spam_dict['antispam_engine'].lower().find('brightmail') > -1:
                spam_dict['use_ipas'] = NO
                spam_dict['use_brightmail'] = YES
            else:
                spam_dict['use_ipas'] = YES
                spam_dict['use_brightmail'] = NO
            del spam_dict['antispam_engine']
        except KeyError:
            pass  # antispam_engine is not specified - carry on
        except TypeError:
            # spam_dict isn't present, try with kwargs instead
            try:
                if kwargs['antispam_engine'].lower().find('brightmail') > -1:
                    kwargs['use_ipas'] = NO
                    kwargs['use_brightmail'] = YES
                else:
                    kwargs['use_ipas'] = YES
                    kwargs['use_brightmail'] = NO
                del kwargs['antispam_engine']
            except KeyError:
                pass  # antispam_engine is not specified anywhere

        param_map.update(spam_dict or kwargs)
        return self._process_input(param_map, do_restart=False)

    def get_suspected_spam_param_map(self, suspected_spam_dict=None,
                                     new_policy=False, status=DEFAULT, **kwargs):
        # since marketing mails behavior is only when Ironport antispam is used, end string need to
        # be diffrent when brightmail is used
        param_map = IafCliParamMap(end_of_command='Anti-Spam configuration complete')

        param_map['special_treatment'] = \
            ['treatment of suspected spam', DEFAULT]
        param_map['score_sus_ims'] = \
            ['Intelligent Multi-Scan suspect spam threshold', [DEFAULT, DEFAULT]]
        param_map['score_suspected'] = \
            ['suspect spam threshold', [DEFAULT]]
        param_map['score_sus_cloudmark'] = \
            ['Cloudmark Service Provider Edition suspect spam threshold', \
             [DEFAULT]]
        param_map['action_spam_suspected'] = \
            ['to do with messages identified as', DEFAULT, True]
        param_map['archive_suspected'] = \
            ['to archive messages identified as', DEFAULT]
        param_map['text_add_suspected'] = \
            ['add text to the subject of messages', DEFAULT, True]
        param_map['text_suspected'] = \
            ['What text do you want', DEFAULT]
        param_map['sent_to_suspected'] = \
            ['spam sent to an external quarantine', DEFAULT]
        param_map['host_suspected'] = \
            ['enter the host to send ', status]
        param_map['header_suspected'] = \
            ['to add a custom header', DEFAULT]
        param_map['header_name_suspected'] = \
            ['Enter the name of the header', status]
        param_map['content_suspected'] = \
            ['text for the content', status]
        param_map['envelope_recipient_suspected'] = \
            ['spam sent to an alternate envelope recipient', DEFAULT]
        param_map['email_suspected'] = \
            ['email address to send spam', status]

        param_map.update(suspected_spam_dict or kwargs)
        self._process_input(param_map, do_restart=False)


class policyconfigEditAntivirus(clictorbase.IafCliConfiguratorBase):
    """policyconfig->Edit->Antivirus"""

    class DuplicateEntriesError(IafCliError):
        pass

    class HeaderCharacterError(IafCliError):
        pass

    class HeaderStringsError(IafCliError):
        pass

    class HeaderLengthError(IafCliError):
        pass

    class InvalidCharacterError(IafCliError):
        pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Headers may contain any character except',
             EXACT): self.HeaderCharacterError,
            ('Headers may not be empty strings',
             EXACT): self.HeaderStringsError,
            ('Custom header text has a maximum length of 128',
             EXACT): self.HeaderLengthError,
            ('Invalid character', EXACT): self.InvalidCharacterError,
            ('Duplicate entries not allowed',
             EXACT): self.DuplicateEntriesError
        })

    def default(self):
        self.newline = 2
        self._query_response('DEFAULT')
        self._to_the_top(self.newline)

    def disable(self):
        self.newline = 2
        self._query_response('DISABLE')
        self._to_the_top(self.newline)

    def enable(self, antivirus_dict=None, repaired_dict=None,
               encrypted_dict=None, unscannable_dict=None, infected_dict=None,
               new_policy=False):
        try:
            status = REQUIRED
        except NameError:
            status = self.REQUIRED
        if not new_policy:
            self._query_response('ENABLE')
        self.get_antivirus_param_map(antivirus_dict)
        idx = self._query('repaired', 'encrypted')
        if idx == 0:
            self.get_repaired_param_map(repaired_dict, status)
        self.get_encrypted_param_map(encrypted_dict, status)
        self.get_unscannable_param_map(unscannable_dict, status)
        self.get_infected_param_map(infected_dict, new_policy, status)

    def edit(self, antivirus_dict=None, repaired_dict=None,
             encrypted_dict=None, unscannable_dict=None, infected_dict=None,
             new_policy=False):
        self._query_response('EDIT')
        self.get_antivirus_param_map(antivirus_dict)
        idx = self._query('repaired', 'encrypted')
        if idx == 0:
            self.get_repaired_param_map(repaired_dict)
        self.get_encrypted_param_map(encrypted_dict)
        self.get_unscannable_param_map(unscannable_dict)
        self.get_infected_param_map(infected_dict)

    def get_antivirus_param_map(self, antivirus_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Message Handling')

        param_map['antivirus_mcafee'] = \
            ['Would you like to use McAfee', DEFAULT]
        param_map['antivirus_sophos'] = \
            ['Would you like to use Sophos', DEFAULT]
        param_map['insert_xheader'] = \
            ['automatically insert an X-header', DEFAULT]
        param_map['scan_messages'] = \
            [' like the system to scan ', DEFAULT, True]
        param_map['drop_attachments'] = \
            ['Drop infected attachments', DEFAULT]

        param_map.update(antivirus_dict or kwargs)
        self._process_input(param_map, do_restart=False)

    def get_repaired_param_map(self, repaired_dict=None, status=DEFAULT,
                               **kwargs):
        param_map = IafCliParamMap(end_of_command= \
                                       'Encrypted Message Handling')

        param_map['repaired_edit'] = \
            ['actions for Repaired Message Handling', DEFAULT]
        param_map['repaired_action'] = \
            ['Action applied to the original message', DEFAULT, True]
        param_map['repaired_add_header'] = \
            ['to add a custom header', DEFAULT]
        param_map['repaired_header'] = \
            ['Enter the header name', status]
        param_map['repaired_header_content'] = \
            ['Enter the header content', status]
        param_map['repaired_message_body'] = \
            ['to use a custom message body', DEFAULT]
        param_map['repaired_message_body_template'] = \
            ['Select a custom message body', DEFAULT, 1]
        param_map['repaired_remove_config'] = \
            ['Remove configuration for template', DEFAULT]
        param_map['repaired_modify_subject'] = \
            ['to modify the subject', DEFAULT]
        param_map['repaired_text_position'] = \
            ['Select position of text', DEFAULT, True]
        param_map['repaired_text_add'] = \
            ['Enter the text to add', DEFAULT]
        param_map['repaired_archive'] = \
            ['archive the original infected message', DEFAULT]
        param_map['repaired_notific_sender'] = \
            ['notification to the message sender', DEFAULT]
        param_map['repaired_notific_recipient'] = \
            ['notification to the message recipients', DEFAULT]
        param_map['repaired_notific_third'] = \
            [' notification to a third party', DEFAULT]
        param_map['repaired_address'] = \
            ['address(es) to send notifications to', status]
        param_map['repaired_notific_subj'] = \
            [' notification subject', DEFAULT]
        param_map['repaired_deliver_mailhost'] = \
            ['deliver mail to an alternate mailhost', DEFAULT]
        param_map['repaired_mailhost'] = \
            ['the mailhost to deliver to', status]
        param_map['repaired_redirect'] = \
            ['redirect mail to an alternate email', DEFAULT]
        param_map['repaired_deliver_address'] = \
            ['the address to deliver to', status]

        param_map.update(repaired_dict or kwargs)
        self._process_input(param_map, do_restart=False)

    def get_encrypted_param_map(self, encrypted_dict=None, status=DEFAULT,
                                **kwargs):
        param_map = IafCliParamMap(end_of_command= \
                                       'Unscannable Message Handling')

        param_map['encrypted_edit'] = \
            ['actions for Encrypted Message Handling', DEFAULT]
        param_map['encrypted_action'] = \
            ['Action applied to the original message', DEFAULT, True]
        param_map['encrypted_archive'] = \
            ['archive the original infected message', DEFAULT]
        param_map['encrypted_notific_sender'] = \
            ['notification to the message sender', DEFAULT]
        param_map['encrypted_notific_recipient'] = \
            ['notification to the message recipients', DEFAULT]
        param_map['encrypted_notific_third'] = \
            [' notification to a third party', DEFAULT]
        param_map['encrypted_address'] = \
            ['address(es) to send notifications to', status]
        param_map['encrypted_notific_subj'] = \
            [' notification subject', DEFAULT]
        param_map['encrypted_deliver_mailhost'] = \
            ['deliver mail to an alternate mailhost', DEFAULT]
        param_map['encrypted_mailhost'] = \
            ['the mailhost to deliver to', status]
        param_map['encrypted_redirect'] = \
            ['redirect mail to an alternate email', DEFAULT]
        param_map['encrypted_deliver_address'] = \
            ['the address to deliver to', status]
        param_map['encrypted_add_header'] = \
            ['to add a custom header', DEFAULT]
        param_map['encrypted_header'] = \
            ['Enter the header name', status]
        param_map['encrypted_header_content'] = \
            ['Enter the header content', status]
        param_map['encrypted_message_body'] = \
            ['to use a custom message body', DEFAULT]
        param_map['encrypted_message_body_template'] = \
            ['Select a custom message body', DEFAULT, 1]
        param_map['encrypted_remove_config'] = \
            ['Remove configuration for template', DEFAULT]
        param_map['encrypted_modify_subject'] = \
            ['to modify the subject', DEFAULT]
        param_map['encrypted_text_position'] = \
            ['Select position of text', DEFAULT, True]
        param_map['encrypted_text_add'] = \
            ['Enter the text to add', DEFAULT]

        param_map.update(encrypted_dict or kwargs)
        self._process_input(param_map, do_restart=False)

    def get_unscannable_param_map(self, unscannable_dict=None, status=DEFAULT,
                                  **kwargs):
        param_map = IafCliParamMap(end_of_command= \
                                       'Virus Infected Message Handling')

        param_map['unscannable_edit'] = \
            ['actions for Unscannable Message Handling', DEFAULT]
        param_map['unscannable_action'] = \
            ['Action applied to the original message', DEFAULT, True]
        param_map['unscannable_archive'] = \
            ['archive the original infected message', DEFAULT]
        param_map['unscannable_notific_sender'] = \
            ['notification to the message sender', DEFAULT]
        param_map['unscannable_notific_recipient'] = \
            ['notification to the message recipients', DEFAULT]
        param_map['unscannable_notific_third'] = \
            [' notification to a third party', DEFAULT]
        param_map['unscannable_address'] = \
            ['address(es) to send notifications to', status]
        param_map['unscannable_notific_subj'] = \
            [' notification subject', DEFAULT]
        param_map['unscannable_deliver_mailhost'] = \
            ['deliver mail to an alternate mailhost', DEFAULT]
        param_map['unscannable_mailhost'] = \
            ['the mailhost to deliver to', status]
        param_map['unscannable_redirect'] = \
            ['redirect mail to an alternate email', DEFAULT]
        param_map['unscannable_deliver_address'] = \
            ['the address to deliver to', status]
        param_map['unscannable_add_header'] = \
            ['to add a custom header', DEFAULT]
        param_map['unscannable_header'] = \
            ['Enter the header name', status]
        param_map['unscannable_header_content'] = \
            ['Enter the header content', status]
        param_map['unscannable_message_body'] = \
            ['to use a custom message body', DEFAULT]
        param_map['unscannable_message_body_template'] = \
            ['Select a custom message body', DEFAULT, 1]
        param_map['unscannable_remove_config'] = \
            ['Remove configuration for template', DEFAULT]
        param_map['unscannable_modify_subject'] = \
            ['to modify the subject', DEFAULT]
        param_map['unscannable_text_position'] = \
            ['Select position of text', DEFAULT, True]
        param_map['unscannable_text_add'] = \
            ['Enter the text to add', DEFAULT]

        param_map.update(unscannable_dict or kwargs)
        self._process_input(param_map, do_restart=False)

    def get_infected_param_map(self, infected_dict=None, new_policy=False,
                               status=DEFAULT, **kwargs):
        param_map = IafCliParamMap(end_of_command= \
                                       'Anti-Virus configuration complete')

        param_map['infected_edit'] = \
            ['actions for Virus Infected Message Handling', DEFAULT]
        param_map['infected_action'] = \
            ['Action applied to the original message', DEFAULT, True]
        param_map['infected_archive'] = \
            ['archive the original infected message', DEFAULT]
        param_map['infected_notific_sender'] = \
            ['notification to the message sender', DEFAULT]
        param_map['infected_notific_recipient'] = \
            ['notification to the message recipients', DEFAULT]
        param_map['infected_notific_third'] = \
            [' notification to a third party', DEFAULT]
        param_map['infected_address'] = \
            ['address(es) to send notifications to', status]
        param_map['infected_notific_subj'] = \
            [' notification subject', DEFAULT]
        param_map['infected_deliver_mailhost'] = \
            ['deliver mail to an alternate mailhost', DEFAULT]
        param_map['infected_mailhost'] = \
            ['the mailhost to deliver to', status]
        param_map['infected_redirect'] = \
            ['redirect mail to an alternate email', DEFAULT]
        param_map['infected_deliver_address'] = \
            ['the address to deliver to', status]
        param_map['infected_add_header'] = \
            ['to add a custom header', DEFAULT]
        param_map['infected_header'] = \
            ['Enter the header name', status]
        param_map['infected_message_body'] = \
            ['to use a custom message body', DEFAULT]
        param_map['infected_message_body_template'] = \
            ['Select a custom message body', DEFAULT, 1]
        param_map['infected_remove_config'] = \
            ['Remove configuration for template', DEFAULT]
        param_map['infected_header_content'] = \
            ['Enter the header content', status]
        param_map['infected_modify_subject'] = \
            ['to modify the subject', DEFAULT]
        param_map['infected_text_position'] = \
            ['Select position of text', DEFAULT, True]
        param_map['infected_text_add'] = \
            ['Enter the text to add', DEFAULT]

        if not new_policy:
            do_restart = True
        else:
            do_restart = False
        param_map.update(infected_dict or kwargs)
        self._process_input(param_map, do_restart)


class policyconfigEditAdvancedmalware(clictorbase.IafCliConfiguratorBase):
    """policyconfig->Edit->Advancedmalware"""

    class AdvancedmalwareHeaderError(IafCliError):
        pass

    class AdvancedmalwareLevelError(IafCliError):
        pass

    class FilterExistError(IafCliError):
        pass

    class HeaderCharacterError(IafCliError):
        pass

    class HeaderStringsError(IafCliError):
        pass

    class HeaderLengthError(IafCliError):
        pass

    class InvalidCharacterError(IafCliError):
        pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('The header text must be less than 100',
             EXACT): self.AdvancedmalwareHeaderError,
            ('No machines at current level',
             EXACT): self.AdvancedmalwareLevelError,
            ('Must have at least 1 filter',
             EXACT): self.FilterExistError,
            ('Headers may contain any character except',
             EXACT): self.HeaderCharacterError,
            ('Headers may not be empty strings',
             EXACT): self.HeaderStringsError,
            ('Custom header text has a maximum length of 128',
             EXACT): self.HeaderLengthError,
            ('Invalid character', EXACT): self.InvalidCharacterError,
        })

    def disable(self):
        self.newline = 2
        self._query_response('DISABLE')
        self._to_the_top(self.newline)

    def enable(self, advancedmalware_dict=None, new_policy=False):
        self.newline = 2
        status = REQUIRED
        if not new_policy:
            self._query_response('ENABLE')
        self.get_advancedmalware_param_map(advancedmalware_dict, status)
        self._to_the_top(self.newline)

    def edit(self, advancedmalware_dict=None):
        self.newline = 2
        self._query_response('EDIT')
        self.get_advancedmalware_param_map(advancedmalware_dict)
        self._to_the_top(self.newline)

    def default(self):
        self.newline = 2
        self._query_response('DEFAULT')
        self._to_the_top(self.newline)

    def get_advancedmalware_param_map(self, advancedmalware_dict=None, status=DEFAULT, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['enable_file_analysis'] = ['to enable File Analysis', DEFAULT]
        param_map['edit_action_file_analysis'] = ['edit the actions for Messages with File Analysis Pending', DEFAULT]
        param_map['apply_action_message'] = ['Action applied to the original message', DEFAULT]
        param_map['insert_xheader'] = ['to automatically insert an X-header', DEFAULT]
        param_map['edit_action_rate_limit'] = ['to edit the actions for Unscannable Message due to rate limit hit',
                                               DEFAULT]
        param_map['action-message'] = ['Action applied to the original message', DEFAULT]
        param_map['add_header'] = ['to add a custom header', DEFAULT]
        param_map['header_name'] = ['the header name', DEFAULT]
        param_map['header_content'] = ['the header content', DEFAULT]
        param_map['modify_subject'] = ['modify the subject', DEFAULT]
        param_map['position_text'] = ['postion of text', DEFAULT]
        param_map['text'] = ['text to add', DEFAULT]
        param_map['archive'] = ['to archive the original message', DEFAULT]
        param_map['archive_unscannable'] = ['to archive the original message', DEFAULT]
        param_map['edit_action_malware'] = ['to edit the actions for Malware Infected Message', DEFAULT]
        param_map['rate_limit_alt_host'] = ['mail to an alternate mailhost', DEFAULT]
        param_map['rate_limit_alt_email'] = ['mail to an alternate email address', DEFAULT]
        param_map['rate_limit_add_header'] = ['to add a custom header', DEFAULT]
        param_map['rate_limit_modify_subject'] = ['modify the subject', DEFAULT]
        param_map['archive_rate_limit'] = ['to archive the original message', DEFAULT]
        param_map['action_message_malware'] = ['Action applied to the original message', DEFAULT]
        param_map['drop_infected'] = ['drop infected attachments', DEFAULT]
        param_map['mal_add_header'] = ['to add a custom header', DEFAULT]
        param_map['mal_header_name'] = ['the header name', DEFAULT]
        param_map['mal_header_content'] = ['the header content', DEFAULT]
        param_map['mal_modify_subject'] = ['modify the subject', DEFAULT]
        param_map['mal_position_text'] = ['position of text', DEFAULT]
        param_map['mal_text'] = ['text to add', DEFAULT]
        param_map['archive_malware'] = ['to archive the original message', DEFAULT]
        param_map['edit_action_file_analysis'] = ['to edit the actions for Messages with File Analysis Pending',
                                                  DEFAULT]
        param_map['edit_action_message_errors'] = ['to edit the actions for Unscannable Message due to message errors',
                                                   DEFAULT]
        param_map['edit_action_AMP_service'] = [
            'to edit the actions for Unscannable Message due to AMP Service not available', DEFAULT]
        param_map['action-message_analysis'] = ['Action applied to the original message', DEFAULT]
        param_map['drop_infected'] = ['drop infected attachments', DEFAULT]
        param_map['unscan_alt_hostname'] = ['mail to an alternate mailhost', DEFAULT]
        param_map['unscan_mailhost'] = ['mailhost to deliver to', DEFAULT]
        param_map['unscan_alt_email'] = ['mail to an alternate email address', DEFAULT]
        param_map['unscan_address'] = ['address to deliver to', DEFAULT]
        param_map['mal_alternate_mail_host'] = ['mail to an alternate mailhost', DEFAULT]
        param_map['mal_mailhost_to_deliver'] = ['mailhost to deliver to', DEFAULT]
        param_map['mal_alternate_email_address'] = ['mail to an alternate email address', DEFAULT]
        param_map['mal_address_to_deliver'] = ['address to deliver to', DEFAULT]
        param_map['analysis_alt_mail_host'] = ['mail to an alternate mailhost', DEFAULT]
        param_map['analysis_mailhost'] = ['mailhost to deliver to', DEFAULT]
        param_map['analysis_alt_email'] = ['mail to an alternate email address', DEFAULT]
        param_map['analysis_address_to_deliver'] = ['address to deliver to', DEFAULT]
        param_map['analysis_add_header'] = ['to add a custom header', DEFAULT]
        param_map['analysis_header_name'] = ['the header name', DEFAULT]
        param_map['analysis_header_content'] = ['the header content', DEFAULT]
        param_map['analysis_modify_subject'] = ['modify the subject', DEFAULT]
        param_map['analysis_position_text'] = ['position of text', DEFAULT]
        param_map['analysis_text'] = ['text to add', DEFAULT]
        param_map['archive_analysis'] = ['to archive the original message', DEFAULT]
        param_map['enable_mar'] = ['enable Mailbox Auto Remediation action', DEFAULT]
        param_map['select_mar_action'] = ['Please select an action:', DEFAULT]
        param_map['edit_mar_action'] = ['edit Mailbox Auto Remediation action', DEFAULT]
        param_map['forward_id'] = ['Forward to:', REQUIRED]
        param_map['disable_mar'] = ['disable Mailbox Auto Remediation action', DEFAULT]
        param_map.update(advancedmalware_dict or kwargs)
        return self._process_input(param_map, do_restart=False)


class policyconfigEditVof(clictorbase.IafCliConfiguratorBase):
    """policyconfig->Edit->Vof"""

    def disable(self, filter_to_toggle=REQUIRED):
        self.newline = 2
        self._query_response('DISABLE')
        self._to_the_top(self.newline)

    def enable(self, extensions_list=DEFAULT, input_dict=None, **kwargs):
        self._query_response('ENABLE')
        return self._edit(extensions_list, input_dict, **kwargs)

    def default(self):
        self.newline = 2
        self._query_response('DEFAULT')
        self._to_the_top(self.newline)

    def _edit(self, extensions_list, input_dict, **kwargs):
        if is_yes(extensions_list):
            self._query_response(extensions_list)
            param_map = self.update_param_map(input_dict or kwargs)
            return policyconfigEditVofEdit(self._get_sess(), param_map)
        else:
            self._query_response(extensions_list)
            param_map = self.update_param_map(input_dict or kwargs)
            self._process_input(param_map)

    def edit(self, extensions_list=DEFAULT, input_dict=None, **kwargs):
        self._query_response('EDIT')
        return self._edit(extensions_list, input_dict, **kwargs)

    def update_param_map(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['threshold_quarantine'] = ['threshold value to quarantine messages', DEFAULT]
        param_map['retention_attachment'] = ['maximum retention period for viral attachment', DEFAULT]
        param_map['modification'] = ['enable the message modification', DEFAULT]
        param_map['deliver_all'] = \
            ['deliver all non viral threat messages without quarantining', DEFAULT]
        param_map['include_outbreak_header'] = \
            ['X-IronPort-Outbreak headers in messages', DEFAULT]
        param_map['status_header_appear'] = \
            ['X-IronPort-Outbreak-Status header should appear', DEFAULT]
        param_map['enable_description_header'] = \
            ['enable the X-IronPort-Outbreak-Description header', DEFAULT]
        param_map['enable_alternate_destination'] = \
            ['enable Alternate Destination Mailhost', DEFAULT]
        param_map['enter_alternate_destination'] = \
            ['enter Alternate Destination Mailhost', REQUIRED]
        param_map['retention_all'] = ['maximum retention period for all', DEFAULT]
        param_map['proxy'] = ['web security proxy', DEFAULT]
        param_map['exclude_domain'] = ['like to specify a list of domains', DEFAULT]
        param_map['domains'] = ['Domain names', DEFAULT]
        param_map['signed_message'] = ['signed messages', DEFAULT]
        param_map['add_disclaimer'] = ['add a disclaimer', DEFAULT]
        param_map['disclaimer'] = ['choose a disclaimer', DEFAULT]
        param_map['threshold_modify'] = ['threshold value to modify messages', DEFAULT]
        param_map['add_text'] = ['add text to the subject', DEFAULT]
        param_map['text'] = ['text do you want', DEFAULT]
        param_map.update(input_dict)
        return param_map


class policyconfigEditVofEdit(clictorbase.IafCliConfiguratorBase):
    """policyconfig->Edit->Vof->Edit"""

    class FileExtensionDeleteError(IafCliError):
        pass

    class FileExtensionCreateError(IafCliError):
        pass

    class FileExtensionInsertError(IafCliError):
        pass

    class ExtensionFormatError(IafCliError):
        pass

    def __init__(self, sess, param_map):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
            self.param_map = param_map
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Delete attempted after last non-default entry',
             EXACT): self.FileExtensionDeleteError,
            ('are already configured to bypass',
             EXACT): self.FileExtensionCreateError,
            ('Do not include the', EXACT): self.ExtensionFormatError,
            ('Insert attempt after default entry',
             EXACT): self.FileExtensionInsertError
        })

    def new(self, file_extensions=REQUIRED):
        self._query_response('NEW')
        self._query_response(file_extensions)
        self._query_response('')
        self._process_input(self.param_map)

    def delete(self, file_extensions=DEFAULT):
        self._query_response('DELETE')
        self._query_select_list_item(file_extensions)
        self._query_response('')
        self._process_input(self.param_map)

    def print_file(self):
        self._query_response('PRINT')
        self._expect('\n')
        raw = self._read_until('Choose the operation you want to perform')
        self._query_response('')
        self._process_input(self.param_map)
        return raw

    def clear(self):
        self._query_response('CLEAR')
        self._query_response('')
        self._process_input(self.param_map)


class policyconfigEditFilters(clictorbase.IafCliConfiguratorBase):
    """policyconfig->Edit->Filters"""

    class FilterEnableError(IafCliError):
        pass

    class FilterCountError(IafCliError):
        pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('No filters defined', EXACT): self.FilterCountError,
            ('filter must be used with another filter',
             EXACT): self.FilterEnableError
        })

    def disable(self):
        self.newline = 2
        self._query_response('DISABLE')
        self._to_the_top(self.newline)

    def enable(self, filter_to_toggle=REQUIRED):
        self.newline = 3
        self._query_response('ENABLE')
        self._query_select_list_item(filter_to_toggle)
        self._to_the_top(self.newline)

    def default(self):
        self.newline = 2
        self._query_response('DEFAULT')
        self._to_the_top(self.newline)

    def edit(self, filter_to_toggle=REQUIRED):
        self.newline = 3
        self._query_response('EDIT')
        self._query_select_list_item(filter_to_toggle)
        self._to_the_top(self.newline)


class policyconfigFilters(clictorbase.IafCliConfiguratorBase):
    """policyconfig -> Filters"""

    class FilterEnableError(IafCliError):
        pass

    class FilterNameError(IafCliError):
        pass

    class FilterTargetExistError(IafCliError):
        pass

    class FilterMovePositionError(IafCliError):
        pass

    class FilterMoveSequenceError(IafCliError):
        pass

    class FilterExistError(IafCliError):
        pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('must be a letter or an underscore',
             EXACT): self.FilterNameError,
            ('must be used with another filter',
             EXACT): self.FilterEnableError,
            ('No target position given',
             EXACT): self.FilterMovePositionError,
            ('Invalid target position',
             EXACT): self.FilterTargetExistError,
            ('Must have at least 1 filter',
             EXACT): self.FilterExistError,
            ('Invalid sequence range',
             EXACT): self.FilterMoveSequenceError
        })

    def new(self, filter_name=REQUIRED, description=REQUIRED):
        self._query_response('NEW')
        self._query_response(filter_name)
        self._query_response(description)
        return policyconfigFiltersEdit(self._get_sess())

    def edit(self, filter=REQUIRED):
        self._query_response('EDIT')
        self._query_response(filter)
        return policyconfigFiltersEdit(self._get_sess())

    def delete(self, filter=REQUIRED):
        self.newline = 2
        self._query_response('DELETE')
        self._query_response(filter)
        self._to_the_top(self.newline)

    def print_filters(self):
        self.newline = 2
        self._query_response('PRINT')
        self._expect('\n')
        raw = self._read_until('Choose the operation you want to perform')
        self._to_the_top(self.newline)
        return raw

    def move(self, filter=REQUIRED, position=REQUIRED):
        self.newline = 2
        self._query_response('MOVE')
        self._query_response(filter)
        self._query_response(position)
        self._to_the_top(self.newline)

    def rename(self, filter=REQUIRED, new_name=REQUIRED):
        self.newline = 2
        self._writeln('RENAME')
        self._query_response(filter)
        self._query_response(new_name)
        self._to_the_top(self.newline)


class policyconfigFiltersEdit(clictorbase.IafCliConfiguratorBase):
    """policyconfig -> Filters -> Edit"""

    class FilterEnableError(IafCliError):
        pass

    class FilterNameError(IafCliError):
        pass

    class FilterCreateError(IafCliError):
        pass

    class FilterActionAddError(IafCliError):
        pass

    class FilterEmailError(IafCliError):
        pass

    class FilterExistError(IafCliError):
        pass

    class FilterActionMimeError(IafCliError):
        pass

    class FilterRegularExpressionError(IafCliError):
        pass

    class FilterFingerprintsError(IafCliError):
        pass

    class FilterHostnameError(IafCliError):
        pass

    class FilterLdapGroupError(IafCliError):
        pass

    class FilterHeaderError(IafCliError):
        pass

    class FilterConditionError(IafCliError):
        pass

    class FilterDuplicateNameError(IafCliError):
        pass

    class FilterParameterError(IafCliError):
        pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('Cancel new filter', EXACT): self.FilterCreateError,
            ('must be a letter or an underscore',
             EXACT): self.FilterNameError,
            ('Must have at least 1 filter', EXACT): self.FilterExistError,
            ('filter must be used with another filter',
             EXACT): self.FilterEnableError,
            ('Could not create action with given parameters',
             EXACT): self.FilterActionAddError,
            ('Duplicate entries not allowed',
             EXACT): self.FilterEmailError,
            ('Illegal regular expression',
             EXACT): self.FilterRegularExpressionError,
            ('MIME types may only contain alphanumeric',
             EXACT): self.FilterActionMimeError,
            ('Attachment fingerprints are a single word',
             EXACT): self.FilterFingerprintsError,
            ('The address must be hostname or IP',
             EXACT): self.FilterHostnameError,
            ('header must be no longer than 64 characters',
             EXACT): self.FilterHeaderError,
            ('LDAP group names must be specified',
             EXACT): self.FilterLdapGroupError,
            ('Condition not supported yet',
             EXACT): self.FilterConditionError,
            ('Duplicate filter name',
             EXACT): self.FilterDuplicateNameError,
            ('non-Filter parameter to FilterSet',
             EXACT): self.FilterParameterError
        })

    def rename(self, new_name=DEFAULT):
        self.newline = 3
        self._query_response('RENAME')
        self._query_response(new_name)
        self._to_the_top(self.newline)

    def desc(self, description=DEFAULT):
        self.newline = 3
        self._query_response('DESC')
        self._query_response(description)
        self._to_the_top(self.newline)

    def add_save(self, filter_dict=None):
        filter_dict['action_condition'] = 'Action'
        self.get_filter_add_param_map(filter_dict, save=True)
        self.save()

    def add(self, filter_dict=None):
        self.get_filter_add_param_map(filter_dict)

    def delete(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['action_condition'] = ['2. Action', DEFAULT, True]
        param_map['condition'] = \
            ['number of the Condition', DEFAULT, True]
        param_map['actions'] = \
            ['number of the Action', DEFAULT, True]
        param_map.update(input_dict or kwargs)

        self._query_response('DELETE')
        return self._process_input(param_map)

    def get_filter_add_param_map(self, filter_dict=None, save=False, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['action_condition'] = ['2. Action', DEFAULT, True]
        param_map['condition'] = \
            ['Envelope Sender in LDAP Group', DEFAULT, True]
        param_map['action'] = \
            ['Bcc', DEFAULT, True]
        param_map['put_disclaimer'] = \
            ['Select whether to put the disclaimer', DEFAULT]
        param_map['contents'] = ['message contents for', REQUIRED]
        param_map['body_contents'] = ['message body contents', REQUIRED]
        param_map['threshold'] = ['Threshold required for', DEFAULT]
        param_map['dictionary'] = \
            ['the Content Dictionary', REQUIRED, True]
        param_map['text_newname'] = ['Enter the text to replace with', DEFAULT]
        param_map['specific_text'] = \
            ['enter specific text to use ', DEFAULT]
        param_map['text'] = ['Enter the text', DEFAULT]
        param_map['message_language'] = ['Choose which Language to match', REQUIRED]
        param_map['message_language_match'] = \
            ['messages will match this rule', DEFAULT, True]
        param_map['body_size'] = ['size of the message', REQUIRED]
        param_map['body_size_match'] = ['Choose which messages will match',
                                        DEFAULT, True]
        param_map['subject_search'] = ['Subject for', REQUIRED]
        param_map['header'] = ['the header to search for', REQUIRED]
        param_map['pattern'] = ['look for a pattern', DEFAULT]
        param_map['expr_header'] = ['header for', REQUIRED]
        param_map['attachments'] = ['message attachments for', REQUIRED]
        param_map['file_type'] = ['file type to look', REQUIRED]
        param_map['mime_type'] = ['the MIME type to look', REQUIRED]
        param_map['recipient_add'] = ['Recipient address for', REQUIRED]
        param_map['ldap_recipient'] = \
            ['LDAP group to look for Recipient', REQUIRED]
        param_map['sender_add'] = ['Sender address for', REQUIRED]
        param_map['ldap_sender'] = \
            ['LDAP group to look for Sender', REQUIRED]
        param_map['bcc_email'] = \
            ['to send the Bcc message', REQUIRED]
        param_map['edit_subject'] = \
            ['edit the subject line used on the Bcc', DEFAULT]
        param_map['subject'] = \
            ['Enter the subject to use', REQUIRED]
        param_map['edit_return_path'] = \
            ['return path of the Bcc message', DEFAULT]
        param_map['return_path'] = \
            ['Enter the return path address:', REQUIRED]
        param_map['edit_bcc_alt_host'] = \
            ['alternate host of the Bcc message', DEFAULT]
        param_map['bcc_alt_host'] = \
            ['Enter alternate host to redirect mail to:', REQUIRED]
        param_map['notification_email'] = \
            ['to send the notification', REQUIRED]
        param_map['edit_subject_notific'] = \
            ['line used on the notification', DEFAULT]
        param_map['edit_return_path_notific'] = \
            ['return path of the notification', DEFAULT]
        param_map['use_custom_notific'] = \
            ['custom template for the notification?', DEFAULT]
        param_map['copy_include'] = \
            ['include a copy of the original message', DEFAULT]
        param_map['redirect_mail'] = \
            ['address to redirect mail to', REQUIRED]
        param_map['redirect_host'] = ['host to redirect mail', REQUIRED]
        param_map['insert_header'] = \
            ['name of the header to insert', REQUIRED]
        param_map['value_header'] = ['the value for this header', REQUIRED]
        param_map['strip_header'] = \
            ['name of the header to strip', REQUIRED]
        param_map['enter_text'] = ['enter specific text', DEFAULT]
        param_map['log_text'] = ['text you want to log to mail logs', REQUIRED]
        param_map['attach_filenames'] = ['filenames for', REQUIRED]
        param_map['mime_strip'] = ['MIME type to strip', REQUIRED]
        param_map['file_type_strip'] = ['file type to strip', REQUIRED]
        param_map['bytes'] = ['minimum size, in bytes', REQUIRED]
        param_map['policy'] = ['1. Policy', DEFAULT]
        param_map['encrypt_profile'] = ['Choose the encryption profile', \
                                        DEFAULT, True]
        param_map['use_custom_subj'] = ['use a custom subject line?', DEFAULT]
        param_map['use_opp_tls'] = ['use opportunistic TLS', DEFAULT]

        param_map['iia_verdict_to_match'] = \
            ['Choose Image Analysis verdict to match', DEFAULT]
        param_map['listener'] = ['Currently configured listeners', REQUIRED, True]
        param_map['mesg_matched'] = ['Messages arrived via listeners', DEFAULT, True]
        param_map['bind_interface'] = ['interfaces to bind the connection', DEFAULT, True]
        param_map['url_category'] = ['Enter the URL Categories', REQUIRED]
        param_map['url_whitelist'] = ['Use a URL Whitelist', REQUIRED]
        param_map['urlcategory_replace'] = ['Choose the URL Categories to replace', REQUIRED]
        param_map['urlcategory_defang'] = ['Choose the URL Categories to defang', REQUIRED]
        param_map['urlcategory_redirect'] = ['Choose the URL categories to redirect', REQUIRED]
        param_map['exclude_signedmessages'] = ['want to exclude signed messages', DEFAULT]
        param_map['urlreputation_range'] = ['Choose the URL Reputation range', DEFAULT]
        param_map['wbrs_min'] = ['Enter minimum WBRS value', REQUIRED]
        param_map['wbrs_max'] = ['Enter maximum WBRS value', REQUIRED]
        param_map['smime_profile'] = ['Choose the S/MIME sending profile you want to use', DEFAULT]
        param_map['macro_detection'] = ['Enter the supported file types', DEFAULT]
        param_map['threatfeed_source'] = ['Select Threatfeed Sources', REQUIRED, True]
        param_map['threatfeed_indicator'] = ['Select Indicator', REQUIRED]
        param_map['url_rep_option'] = ['Reputation by External Thread Feeds', DEFAULT]
        param_map['url_in_attachments'] = ['Do you want this filter to scan for URLs within the message attachments',
                                           DEFAULT]
        param_map['url_in_msg_body'] = ['URLs within the message body', DEFAULT]
        param_map['url_exception_list'] = ['Use a URL list', DEFAULT, True]
        param_map['urlrep_strip_attachments'] = ['Do you want to strip attachments', DEFAULT]
        param_map['url_strip_attachments'] = ['Do you want this filter to strip attachments', DEFAULT]
        param_map['sdr_external_threatfeed_source'] = ['Select the required External Threat Feed sources', DEFAULT,
                                                       True]
        param_map['sdr_mail_from_header'] = [
            'Do you want to check for the sender domain based on the "mail-from" header', DEFAULT]
        param_map['sdr_from_header'] = ['Do you want to check for the sender domain based on the "from" header',
                                        DEFAULT]
        param_map['sdr_reply_to_header'] = ['Do you want to check for the sender domain based on the "reply-to" header',
                                            DEFAULT]
        param_map['sdr_other_header'] = ['Do you want to check for the sender domain based on any other header',
                                         DEFAULT]
        param_map['sdr_header_value'] = ['Enter the header(s) separated by comma', DEFAULT]
        param_map['sender_domain_reputation_source'] = ['Sender Domain Reputation Service', DEFAULT, True]
        param_map['sender_domain_reputation_condition'] = ['Select the condition to configure', DEFAULT, True]
        param_map['sender_domain_reputation_verdict'] = ['Choose a range of sender domain reputation verdicts',
                                                         REQUIRED]
        param_map['sender_domain_reputation_age'] = ['Filter messages where the sender domain age is', DEFAULT, True]
        param_map['sender_domain_reputation_age_unit'] = ['Choose the unit of domain age', DEFAULT, True]
        param_map['sender_domain_reputation_age_value'] = ['Enter the domain age', REQUIRED]
        param_map['sender_domain_reputation_age_condition'] = [
            'Choose the condition to filter the messages based on the sender domain age', DEFAULT]
        param_map['sender_domain_reputation_configure_domain_exception'] = [
            'Do you want to select a Domain exception list', DEFAULT]
        param_map['sender_domain_reputation_domain_exception_list'] = ['Select a Domain Exception list', DEFAULT, True]

        param_map.update(filter_dict or kwargs)

        self._query_response('ADD')
        if save:
            do_restart = False
        else:
            do_restart = True
        return self._process_input(param_map, do_restart)

    def move(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['action_condition'] = ['2. Action', DEFAULT, True]
        param_map['to_move'] = ['you wish to move', DEFAULT, True]
        param_map['position'] = ['target position', REQUIRED]
        param_map.update(input_dict or kwargs)

        self._query_response('MOVE')
        return self._process_input(param_map)

    def toggle_all(self):
        self.newline = 3
        self._query_response('TOGGLE_ALL')
        self._to_the_top(self.newline)

    def save(self):
        self.newline = 2
        self._query_response('SAVE')
        self._to_the_top(self.newline)


class policyconfigEditGraymail(clictorbase.IafCliConfiguratorBase):
    """policyconfig->Edit->Graymail"""

    class GraymailHeaderError(IafCliError):
        pass

    class GraymailLevelError(IafCliError):
        pass

    class FilterExistError(IafCliError):
        pass

    class HeaderCharacterError(IafCliError):
        pass

    class HeaderStringsError(IafCliError):
        pass

    class HeaderLengthError(IafCliError):
        pass

    class InvalidCharacterError(IafCliError):
        pass

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('The header text must be less than 100',
             EXACT): self.GraymailHeaderError,
            ('No machines at current level',
             EXACT): self.GraymailLevelError,
            ('Must have at least 1 filter',
             EXACT): self.FilterExistError,
            ('Headers may contain any character except',
             EXACT): self.HeaderCharacterError,
            ('Headers may not be empty strings',
             EXACT): self.HeaderStringsError,
            ('Custom header text has a maximum length of 128',
             EXACT): self.HeaderLengthError,
            ('Invalid character', EXACT): self.InvalidCharacterError,
        })

    def disable(self):
        self.newline = 2
        self._query_response('DISABLE')
        self._to_the_top(self.newline)

    def enable(self, safe_unsubscribe_dict, marketing_email_dict,
               social_networking_email_dict, bulk_email_dict, policy_type):
        try:
            status = REQUIRED
        except NameError:
            status = self.REQUIRED

        self._query_response('ENABLE')
        if policy_type.lower() == 'incoming':
            self.get_safe_unsubscribe_param_map(safe_unsubscribe_dict)

        self.get_marketing_email_param_map(marketing_email_dict, policy_type, status)
        self.get_social_networking_email_param_map(social_networking_email_dict, policy_type, status)
        self.get_bulk_email_param_map(bulk_email_dict, policy_type, status)
        self._to_the_top(2)

    def edit(self, safe_unsubscribe_dict, marketing_email_dict,
             social_networking_email_dict, bulk_email_dict, policy_type):
        self._query_response('EDIT')

        if policy_type.lower() == 'incoming':
            self.get_safe_unsubscribe_param_map(safe_unsubscribe_dict)

        self.get_marketing_email_param_map(marketing_email_dict, policy_type)
        self.get_social_networking_email_param_map(social_networking_email_dict, policy_type)
        self.get_bulk_email_param_map(bulk_email_dict, policy_type)
        self._to_the_top(2)

    def default(self):
        self._query_response('DEFAULT')
        self._to_the_top(2)

    def get_safe_unsubscribe_param_map(self, safe_unsubscribe_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='enable actions')

        param_map['enable_safe_unsubscribe'] = ['enable Safe Unsubscribe', DEFAULT]
        param_map['safe_unsubscribe_only_unsigned_msg'] = ['action only for unsigned messages', DEFAULT]
        param_map.update(safe_unsubscribe_dict or kwargs)
        return self._process_input(param_map, do_restart=False)

    def get_marketing_email_param_map(self, marketing_email_dict=None,
                                      policy_type=None, new_policy=False, status=DEFAULT, **kwargs):

        if policy_type.lower() == 'incoming':
            param_map = IafCliParamMap(end_of_command='enable actions')
            param_map['enable_marketing_email_actions'] = ['messages identified as Marketing Email', DEFAULT]
        else:
            param_map = IafCliParamMap(end_of_command='identified as Social')
            param_map['enable_marketing_email_actions'] = ['messages identified as Marketing Email', DEFAULT]

        param_map['marketing_mail_action'] = ['to do with messages identified as Marketing', DEFAULT, True]
        param_map['marketing_mail_to_external_quarantine'] = ['Marketing Email to an external quarantine', DEFAULT]
        param_map['marketing_mail_external_host'] = ['enter the host to send Marketing', status]
        param_map['marketing_mail_archive_messages'] = ['archive messages identified as Marketing', DEFAULT]
        param_map['marketing_mail_add_subject_text'] = ['add text to the subject', DEFAULT, True]
        param_map['marketing_mail_subject_text'] = ['text do you want to ', DEFAULT]
        param_map['marketing_mail_add_custom_header'] = ['add a custom header to messages', DEFAULT]
        param_map['marketing_mail_custom_header_name'] = ['name of the header', DEFAULT]
        param_map['marketing_mail_custom_header_value'] = ['content of the header', DEFAULT]
        param_map['marketing_mail_send_to_altrcpt'] = ['to an alternate envelope recipient', DEFAULT]
        param_map['marketing_mail_altrcpt_email_address'] = ['email address to send Marketing', status]

        param_map.update(marketing_email_dict or kwargs)
        return self._process_input(param_map, do_restart=False)

    def get_social_networking_email_param_map(self, social_networking_email_dict=None,
                                              policy_type=None, new_policy=False, status=DEFAULT, **kwargs):

        if policy_type.lower() == 'incoming':
            param_map = IafCliParamMap(end_of_command='enable actions')
            param_map['enable_social_networking_email_actions'] = ['messages identified as Social Networking Email',
                                                                   DEFAULT]
        else:
            param_map = IafCliParamMap(end_of_command='identified as Bulk')
            param_map['enable_social_networking_email_actions'] = ['Networking Email', DEFAULT]

        param_map['social_networking_mail_action'] = ['to do with messages identified as Social Networking', DEFAULT,
                                                      True]
        param_map['social_networking_mail_to_external_quarantine'] = [
            'Social Networking Email to an external quarantine', DEFAULT]
        param_map['social_networking_mail_external_host'] = ['enter the host to send Social Networking', status]
        param_map['social_networking_mail_archive_messages'] = ['archive messages identified as Social Networking',
                                                                DEFAULT]
        param_map['social_networking_mail_add_subject_text'] = ['add text to the subject', DEFAULT, True]
        param_map['social_networking_mail_subject_text'] = ['text do you want to ', DEFAULT]
        param_map['social_networking_mail_add_custom_header'] = ['add a custom header to messages', DEFAULT]
        param_map['social_networking_mail_custom_header_name'] = ['name of the header', DEFAULT]
        param_map['social_networking_mail_custom_header_value'] = ['content of the header', DEFAULT]
        param_map['social_networking_mail_send_to_altrcpt'] = ['to an alternate envelope recipient', DEFAULT]
        param_map['social_networking_mail_altrcpt_email_address'] = ['email address to send Social Networking', status]

        param_map.update(social_networking_email_dict or kwargs)
        return self._process_input(param_map, do_restart=False)

    def get_bulk_email_param_map(self, bulk_email_dict=None,
                                 policy_type=None, new_policy=False, status=DEFAULT, **kwargs):

        param_map = IafCliParamMap(end_of_command='Graymail configuration complete')
        if policy_type.lower() == 'incoming':
            param_map['enable_bulk_email_actions'] = ['messages identified as Bulk', DEFAULT]
        else:
            param_map['enable_bulk_email_actions'] = ['Email?', DEFAULT]
        param_map['bulk_mail_action'] = ['to do with messages identified as Bulk', DEFAULT, True]
        param_map['bulk_mail_to_external_quarantine'] = ['Bulk Email to an external quarantine', DEFAULT]
        param_map['bulk_mail_external_host'] = ['enter the host to send Bulk', status]
        param_map['bulk_mail_archive_messages'] = ['archive messages identified as Bulk', DEFAULT]
        param_map['bulk_mail_add_subject_text'] = ['add text to the subject', DEFAULT, True]
        param_map['bulk_mail_subject_text'] = ['text do you want to ', DEFAULT]
        param_map['bulk_mail_add_custom_header'] = ['add a custom header to messages', DEFAULT]
        param_map['bulk_mail_custom_header_name'] = ['name of the header', DEFAULT]
        param_map['bulk_mail_custom_header_value'] = ['content of the header', DEFAULT]
        param_map['bulk_mail_send_to_altrcpt'] = ['to an alternate envelope recipient', DEFAULT]
        param_map['bulk_mail_altrcpt_email_address'] = ['email address to send Bulk', status]

        param_map.update(bulk_email_dict or kwargs)
        return self._process_input(param_map, do_restart=False)


if __name__ == '__main__':
    # vendor='brightmail'
    vendor = 'ironport'
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    pcfg = policyconfig(cli_sess)

    import commit, antivirusconfig, antispamconfig, ampconfig, vofconfig, clear

    vofconfig.vofconfig(cli_sess)().setup(use=YES)
    antispamconfig.antispamconfig(cli_sess)(vendor).setup()
    antivirusconfig.antivirusconfig(cli_sess)().setup(use_av=YES)
    ampconfig.ampconfig(cli_sess)().setup()
    commit.commit(cli_sess)()
    pcfg().choose().filters().new(filter_name='filter1',
                                  description='description1') \
        .add_save(filter_dict={'action': 'Bcc',
                               'bcc_email': 'email@address.ua'})
    pcfg().choose().filters().new(filter_name='filter2',
                                  description='description2').add_save(filter_dict=
                                                                       {'action': 'Notify', 'notification_email':
                                                                           'email@address.ua'})
    pcfg().choose().filters().new(filter_name='filter3',
                                  description='description3').add_save(filter_dict=
                                                                       {'action': 'Alternate Email Address',
                                                                        'redirect_mail': 'email@address.ua'})
    pcfg().choose().filters().new(filter_name='filter4',
                                  description='description4').add_save(filter_dict=
                                                                       {'action': 'Alternate Host',
                                                                        'redirect_host': '198.1.12.1'})
    pcfg().choose().filters().new(filter_name='filter5',
                                  description='description5').add_save(filter_dict=
                                                                       {'action': 'Insert A Custom Header',
                                                                        'insert_header': 'header',
                                                                        'value_header': 'value'})
    pcfg().choose().filters().new(filter_name='filter6',
                                  description='description6').add_save(filter_dict=
                                                                       {'action': 'Strip A Header',
                                                                        'strip_header': 'strip_header'})
    pcfg().choose().filters().new(filter_name='filter7',
                                  description='description7') \
        .add_save(filter_dict=
                  {'action': 'Drop Attachments By Content',
                   'contents': 'cont', 'enter_text': YES,
                   'text': 'text'})
    pcfg().choose().filters().new(filter_name='filter8',
                                  description='description8').add_save(filter_dict=
                                                                       {'action': 'Drop Attachments By Name',
                                                                        'attach_filenames': 'xls',
                                                                        'enter_text': YES, 'text': 'text'})
    pcfg().choose().filters().new(filter_name='filter9',
                                  description='description9') \
        .add_save(filter_dict=
                  {'action': 'Drop Attachments By MIME Type',
                   'mime_strip': 'AS/FE', 'enter_text': YES,
                   'text': 'text'})
    pcfg().choose().filters().new(filter_name='filter10',
                                  description='description10') \
        .add_save(filter_dict= \
                      {'action': 'Drop Attachments By File Type',
                       'file_type_strip': 'xls', 'enter_text': YES,
                       'text': 'text'})
    pcfg().choose().filters().new(filter_name='filter11',
                                  description='description11') \
        .add_save(filter_dict=
                  {'action': 'Drop Attachments By Size',
                   'bytes': '2345', 'enter_text': YES,
                   'text': 'text'})
    pcfg().choose().filters().new(filter_name='filter12',
                                  description='description12') \
        .add_save(filter_dict= \
                      {'action': 'Send To System Quarantine'})
    pcfg().choose().filters().new(filter_name='filter13',
                                  description='description13') \
        .add_save(filter_dict= \
                      {'action': 'Duplicate And Send'})
    pcfg().choose().filters().new(filter_name='filter14',
                                  description='description14'). \
        add_save(filter_dict={'action': 'Drop (Final'})
    pcfg().choose().filters().new(filter_name='filter15',
                                  description='description15') \
        .add_save(filter_dict={'action': 'Bounce (Final'})
    pcfg().choose().filters().new(filter_name='filter16',
                                  description='description16') \
        .add_save(filter_dict={'action': 'Deliver (Final'})
    pcfg().choose().filters().new(filter_name='filter17',
                                  description='description17') \
        .add_save(filter_dict= \
                      {'action': 'Skip Virus Outbreak'})
    print pcfg().choose().filters().print_filters()
    pcfg().choose().filters().move(filter='filter5', position='filter1')
    print pcfg().choose().filters().print_filters()
    pcfg().choose().filters().delete(filter='filter6')
    print pcfg().choose().filters().print_filters()
    pcfg().choose().filters().rename(filter='filter12',
                                     new_name='filter12_renamed')
    print pcfg().choose().filters().print_filters()
    pcfg().choose().filters().edit(filter='filter1') \
        .add(filter_dict={'action_condition': 'Condition',
                          'condition': 'Message Body Contains',
                          'contents': 'content'})
    pcfg().choose().filters().edit(filter='filter2') \
        .add(filter_dict={'action_condition': 'Condition',
                          'condition': 'Subject Header',
                          'subject_search': 'subjectfor'})
    pcfg().choose().filters().edit(filter='filter2') \
        .add(filter_dict={'action_condition': 'Condition',
                          'condition': 'Only Body Contains',
                          'body_contents': 'message body'})
    pcfg().choose().filters().edit(filter='filter2') \
        .add(filter_dict={'action_condition': 'Condition',
                          'condition': 'Message Body Size',
                          'body_size': '100000',
                          'body_size_match': 'Larger or equal'})
    pcfg().choose().filters().edit(filter='filter3') \
        .add(filter_dict={'action_condition': 'Condition',
                          'condition': 'Other Header', 'header': 'headerfor',
                          'pattern': 'YES', 'expr_header': 'expr_header'})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Condition',
                                                          'condition': 'Attachment Contains',
                                                          'attachments': 'attachment'})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Condition',
                                                          'condition': 'Attachment File Type',
                                                          'file_type': 'xls'})
    pcfg().choose().filters().edit(filter='filter4').add(filter_dict=
                                                         {'action_condition': 'Condition',
                                                          'condition': 'Attachment Name',
                                                          'attach_filenames': 'filenames'})
    pcfg().choose().filters().edit(filter='filter4').add(filter_dict=
                                                         {'action_condition': 'Condition',
                                                          'condition': 'Attachment MIME Type',
                                                          'mime_type': 'AAS/AS'})
    pcfg().choose().filters().edit(filter='filter5').add(filter_dict=
                                                         {'action_condition': 'Condition',
                                                          'condition': 'Recipient Address',
                                                          'recipient_add': 'email@address.ua'})
    pcfg().choose().filters().edit(filter='filter9').add( \
        filter_dict={'action_condition': 'Condition',
                     'condition': 'Recipient in LDAP',
                     'ldap_recipient': 'ldap_recipient'})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Condition',
                                                          'condition': 'Sender Address',
                                                          'sender_add': 'sender_add'})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Condition',
                                                          'condition': 'Sender in LDAP',
                                                          'ldap_sender': 'ldap_sender'})
    pcfg().choose().filters().edit(filter='filter3').add( \
        filter_dict={'action_condition': 'Action',
                     'action': 'Bcc',
                     'bcc_email': 'email@address.ua',
                     'edit_subject': YES,
                     'subject': 'subject', 'edit_return_path': YES,
                     'return_path': 'return@path.er'})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Action',
                                                          'action': 'Notify',
                                                          'notification_email': 'email@addrs.ua',
                                                          'edit_subject_notific': YES,
                                                          'subject': 'subject1234',
                                                          'edit_return_path_notific': YES,
                                                          'return_path': 'return@path.er',
                                                          'copy_include': YES})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Action',
                                                          'action': 'Alternate Email Address',
                                                          'redirect_mail': 'mail@mail.tu'})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Action',
                                                          'action': 'Alternate Host',
                                                          'redirect_host': '198.1.1.1'})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Action',
                                                          'action': 'Insert A Custom Header',
                                                          'insert_header': 'header',
                                                          'value_header': 'value_header'})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Action',
                                                          'action': 'Strip A Header',
                                                          'strip_header': 'strip_header'})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Action',
                                                          'action': 'Drop Attachments By Content',
                                                          'contents': 'contents',
                                                          'enter_text': YES,
                                                          'text': 'text to enter'})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Action',
                                                          'action': 'Drop Attachments by Name',
                                                          'attach_filenames': 'asd',
                                                          'enter_text': YES, 'text': 'text to enter'})
    pcfg().choose().filters().edit(filter='filter11') \
        .add(filter_dict={'action_condition': 'Action',
                          'action': 'Drop Attachments By MIME Type',
                          'mime_strip': 'AS/FE', 'enter_text': YES,
                          'text': 'text to enter'})
    pcfg().choose().filters().edit(filter='filter4').add(filter_dict=
                                                         {'action_condition': 'Action',
                                                          'action': 'Drop Attachments By File Type',
                                                          'file_type_strip': 'xls',
                                                          'enter_text': YES, 'text': 'text to enter'})
    pcfg().choose().filters().edit(filter='3').add(filter_dict=
                                                   {'action_condition': 'Action',
                                                    'action': 'Drop Attachments By Size',
                                                    'bytes': '13254',
                                                    'enter_text': YES, 'text': 'text to enter'})
    pcfg().choose().filters().edit(filter='filter10').add(filter_dict=
                                                          {'action_condition': 'Action',
                                                           'action': 'Send To System Quarantine'})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Action',
                                                          'action': 'Duplicate And Send To System ' \
                                                                    'Quarantine'})
    pcfg().choose().filters().edit(filter='filter3').add(filter_dict=
                                                         {'action_condition': 'Action',
                                                          'action': 'Drop (Final Action)'})
    pcfg().choose().filters().edit(filter='filter3'). \
        move(action_condition='Action',
             to_move='email@address.ua',
             position='1')
    pcfg().choose().filters().edit(filter='filter3').toggle_all()
    pcfg().choose().filters().edit(filter='filter3').delete( \
        action_condition='Condition',
        condition='mail-from-group')
    pcfg().choose().filters().edit(filter='filter8') \
        .desc(description='edited_decription')
    pcfg().choose().filters().edit(filter='filter17') \
        .rename(new_name='filter17_edited_renamed')
    pcfg().choose().filters().edit(filter='filter3') \
        .delete(action_condition='Action',
                actions='alt-rcpt-to ("email@address.ua"')

    print pcfg().choose().filters().print_filters()
    pcfg().choose(policy_type='Incoming').new(policy_name='policy1',
                                              policy_member='mail@mail.ru', entry_type='Recipient',
                                              antispam_table=NO, antispam_enable=YES, antivirus_table=NO,
                                              antivirus_enable=YES,
                                              spam_dict={
                                                  'action_spam': 'DELIVER', 'text_add': 'APPEND',
                                                  'text': 'text_to_enter', 'sent_to': YES, 'host': '191.1.1.1',
                                                  'envelope_recipient': YES, 'email': 'mail@email.com'},
                                              antivirus_dict={'insert_xheader': YES},
                                              repaired_dict={'repaired_edit': YES,
                                                             'repaired_notific_third': YES,
                                                             'repaired_address': 'mail@ua.com'},
                                              encrypted_dict={'encrypted_edit': NO},
                                              unscannable_dict={'unscannable_edit': NO},
                                              infected_dict={'infected_edit': YES},
                                              advancedmalware_enable=YES, advancedmalware_table=NO,
                                              advancedmalware_dict={'enable_file_analysis': 'YES',
                                                                    'edit_action_file_analysis': 'YES',
                                                                    'apply_action_message': '2',
                                                                    'insert_xheader': 'YES', 'edit_action': 'YES',
                                                                    'action_unscannable_message': 'NO',
                                                                    'edit_action_malware': 'YES',
                                                                    'action-message_malware': 'YES',
                                                                    'drop_infected': 'YES', 'archive': 'YES'},
                                              filters_table=NO, filter_to_toggle='1')
    pcfg().choose(policy_type='Incoming').new(policy_name='policy2',
                                              policy_member='mail@mail.ry', entry_type='Recipient',
                                              antispam_table=NO, antispam_enable=YES, antivirus_table=NO,
                                              antivirus_enable=YES,
                                              spam_dict={
                                                  'action_spam': 'DELIVER', 'text_add': 'APPEND',
                                                  'text': 'text_to_enter', 'sent_to': YES, 'host': '191.1.1.1',
                                                  'envelope_recipient': YES, 'email': 'mail@email.com'},
                                              antivirus_dict={'insert_xheader': YES},
                                              repaired_dict={'repaired_edit': YES,
                                                             'repaired_notific_third': YES,
                                                             'repaired_address': 'mail@ua.com'},
                                              encrypted_dict={'encrypted_edit': NO},
                                              unscannable_dict={'unscannable_edit': NO},
                                              infected_dict={'infected_edit': YES},
                                              advancedmalware_enable=YES, advancedmalware_table=NO,
                                              advancedmalware_dict={'enable_file_analysis': 'YES',
                                                                    'edit_action_file_analysis': 'YES',
                                                                    'apply_action_message': '2',
                                                                    'insert_xheader': 'YES', 'edit_action': 'YES',
                                                                    'action_unscannable_message': 'NO',
                                                                    'edit_action_malware': 'YES',
                                                                    'action-message_malware': 'YES',
                                                                    'drop_infected': 'YES', 'archive': 'YES'},
                                              filters_table=NO, filter_to_toggle='1')
    pcfg().choose().delete(policy='policy1')
    print pcfg().choose().print_policy(policy='policy2')
    pcfg().choose(policy_type='Incoming').new(policy_name='policy1',
                                              policy_member='mail@mail.ry', entry_type='Recipient',
                                              antispam_table=NO, antispam_enable=YES, antivirus_table=NO,
                                              antivirus_enable=YES,
                                              spam_dict={
                                                  'action_spam': 'DELIVER', 'text_add': 'APPEND',
                                                  'text': 'text_to_enter', 'sent_to': YES, 'host': '191.1.1.1',
                                                  'envelope_recipient': YES, 'email': 'mail@email.com'},
                                              antivirus_dict={'insert_xheader': YES},
                                              repaired_dict={'repaired_edit': YES,
                                                             'repaired_notific_third': YES,
                                                             'repaired_address': 'mail@ua.com'},
                                              encrypted_dict={'encrypted_edit': NO},
                                              unscannable_dict={'unscannable_edit': NO},
                                              infected_dict={'infected_edit': YES},
                                              advancedmalware_enable=YES, advancedmalware_table=NO,
                                              advancedmalware_dict={'enable_file_analysis': 'YES',
                                                                    'edit_action_file_analysis': 'YES',
                                                                    'apply_action_message': '2',
                                                                    'insert_xheader': 'YES', 'edit_action': 'YES',
                                                                    'action_unscannable_message': 'NO',
                                                                    'edit_action_malware': 'YES',
                                                                    'action-message_malware': 'YES',
                                                                    'drop_infected': 'YES', 'archive': 'YES'},
                                              filters_table=NO, filter_to_toggle='1')
    pcfg().choose().edit(policy='DEFAULT').filters().enable(
        filter_to_toggle='filter10')
    pcfg().choose().edit(policy='DEFAULT').filters().edit(
        filter_to_toggle='filter10')
    pcfg().choose().edit(policy='DEFAULT').filters().disable()
    pcfg().choose().move(entry_to_move='policy1', insert_before='policy2')
    print pcfg().choose().search(policy_member='mail@mail.ry',
                                 entry_type='Recipient')
    pcfg().choose().edit(policy='policy1').new(member='member1@mail.ru',
                                               entry_type='Sender')
    print pcfg().choose().edit(policy='policy1').print_members()
    pcfg().choose().edit(policy='policy1').delete(member='member1@mail.ru')
    pcfg().choose().edit(policy='policy1').new(member='member2@mail.ru',
                                               entry_type='Sender')
    pcfg().choose().edit(policy='policy1').name(policy_name='new_policy1')
    print pcfg().choose().edit(policy='new_policy1').print_members()
    pcfg().choose().edit(policy='DEFAULT').antispam().enable(spam_dict={
        'action_spam': 'DELIVER', 'text_add': 'APPEND',
        'text': 'text_to_enter'},
        suspected_spam_dict={'special_treatment': YES})
    pcfg().choose().edit(policy='DEFAULT').antispam().edit(
        spam_dict={'action_spam': 'DROP'})
    pcfg().choose().edit(policy='DEFAULT').antispam().disable()
    pcfg().choose().edit(policy='DEFAULT').antispam().enable(spam_dict={
        'action_spam': 'DELIVER', 'text_add': 'APPEND',
        'text': 'text_to_enter', 'sent_to': YES, 'host': '191.1.1.1',
        'envelope_recipient': YES, 'email': 'mail@ua.ru'},
        suspected_spam_dict={'special_treatment': YES})
    pcfg().choose().edit(policy='DEFAULT').antispam().disable()
    pcfg().choose().edit(policy='DEFAULT').antispam().enable(spam_dict={
        # 'action_spam':'IRONPORT QUARANTINE', 'text_add':'APPEND',
        # 'text':'text_to_enter',
        # 'header':YES, 'header_name':'HEADER', 'content':'content'},
        'action_spam': 'BOUNCE'},
        suspected_spam_dict={'special_treatment': YES,
                             'action_spam_suspected': 'BOUNCE'})
    pcfg().choose().edit(policy='DEFAULT').vof().enable(extensions_list=YES) \
        .new(file_extensions='extension1')
    pcfg().choose().edit(policy='DEFAULT').vof().edit(extensions_list=YES) \
        .new(file_extensions='extension2')
    print pcfg().choose().edit(policy='DEFAULT').vof(). \
        edit(extensions_list=YES).print_file()
    pcfg().choose().edit(policy='DEFAULT').vof().edit(extensions_list=YES) \
        .delete(file_extensions='extension2')
    print pcfg().choose().edit(policy='DEFAULT').vof(). \
        edit(extensions_list=YES).print_file()
    pcfg().choose().edit(policy='DEFAULT').vof().edit(extensions_list=YES) \
        .clear()
    pcfg().choose().edit(policy='DEFAULT').vof().disable()
    pcfg().choose().edit(policy='DEFAULT').antivirus().enable(antivirus_dict={
        'insert_xheader': YES}, repaired_dict={'repaired_edit': YES,
                                               'repaired_notific_third': YES,
                                               'repaired_address': 'mail@mailcom.com'}, encrypted_dict={
        'encrypted_edit': NO}, unscannable_dict={
        'unscannable_edit': NO},
        infected_dict={'infected_edit': YES})
    pcfg().choose().edit(policy='DEFAULT').antivirus().disable()
    pcfg().choose().edit(policy='DEFAULT').advancedmalware().enable(advancedmalware_dict={'enable_file_analysis': 'YES',
                                                                                          'edit_action_file_analysis': 'YES',
                                                                                          'apply_action_message': '2',
                                                                                          'insert_xheader': 'YES',
                                                                                          'edit_action': 'NO',
                                                                                          'edit_action_malware': 'NO'})
    pcfg().choose().edit(policy='DEFAULT').advancedmalware().edit(
        advancedmalware_dict={'enable_file_analysis': 'NO', 'insert_xheader': 'YES'})
    pcfg().choose().edit(policy='DEFAULT').advancedmalware().disable()
    pcfg().choose().clear()

    # turn off antispam, antivirus, VOF now that we're done
    clear.clear(cli_sess)()
    outbreakconfig.outbreakconfig(cli_sess)().setup(use=NO, disable=YES)
    antispamconfig.antispamconfig(cli_sess)(vendor).setup(use_case=NO,
                                                          confirm_disable=YES)
    antivirusconfig.antivirusconfig(cli_sess)().setup(use_av=NO)
    pcfg().choose().edit(policy='DEFAULT').vof().edit(NO)
    input_dict = {'threshold_quarantine': 2, 'retention_attachment': '2d', 'modification': 'Y', 'retention_all': '3d',
                  'proxy': 'y', 'exclude_domain': 'y', 'domains': 'example1.com,example2.com', 'signed_message': 'n',
                  'add_disclaimer': 'y', 'disclaimer': 1, 'threshold_modify': 4, 'add_text': 1, 'text': 'working'}
    pcfg().choose().edit(policy='DEFAULT').vof().edit(NO, input_dict)
    print pcfg().choose().edit(policy='DEFAULT').vof().edit(YES, input_dict).print_file()
    pcfg().choose().edit(policy='DEFAULT').vof().edit(YES, input_dict).new(file_extensions='exe')
    pcfg().choose().edit(policy='DEFAULT').vof().edit(YES, input_dict).delete(file_extensions='exe')
    commit.commit(cli_sess)()

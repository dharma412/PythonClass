#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/manager/hat.py#3 $
# $DateTime: 2019/08/06 10:27:05 $
# $Author: saurgup5 $


import functools
from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon
from access_table_def.access_table_base import AccessTableBase, go_to_access_table, \
    LISTENER_DROPDOWN
from access_table_def.sender_group_settings import SenderGroupSettings
from access_table_def.sender_settings import SenderSettings
from access_table_def.country_settings import CountrySettings
from access_table_def.externalthreatfeeds_settings import ExternalThreatFeedsSettings

SENDERGROUP_TABLE = '//table[@class=\'col-base\']'
ADD_SENDERGROUP_BUTTON = "//input[@value='Add Sender Group...']"
SUBMIT_AND_ADD = "//input[@value='Submit and Add Senders >>']"
EDIT_SG_SETTINGS_BUTTON = 'xpath=//input[@value=\'Edit Settings...\']'
CANCEL_BUTTON = 'xpath=//input[@value=\'Cancel\']'
EDIT_SG_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                            (SENDERGROUP_TABLE, name)
DELETE_SG_LINK = lambda name: \
    "%s//td[.//a[normalize-space()='%s']]/following-sibling::td[4]/img" % \
    (SENDERGROUP_TABLE, name)

SENDER_TABLE = "//table[@class='cols']"
EDIT_SENDER_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                                (SENDER_TABLE, name)
DELETE_SENDER_CB = lambda name: \
    "%s//td[.//a[normalize-space()='%s']]/following-sibling::td[2]/input" % \
    (SENDER_TABLE, name)
CLEAR_ALL_SENDERS_CB = "//input[@name='del_0']"
ADD_SENDER_BUTTON = "//input[@value='Add Sender...']"
ADD_COUNTRY_BUTTON = "//input[@value='Add Sender...']"
DELETE_SENDER_BUTTON = "//input[@id='_click']"
SENDER_NAME = 'xpath=//input[@name=\'sender\']'
COMMENT = 'xpath=//input[@name=\'comment\']'
ADD_ROW_BUTTON = "//input[@id='etf_selection_domtable_AddRow']"
ETF_SOURCE = lambda index: \
    "//select[@id='etf_selection[%s][etf_source]']" % index

EDIT_ORDER_BUTTON = "//input[@value='Edit Order...']"
ORDER_EDIT = lambda sg_name: "//table[@class='col-base']//" \
                             "td[.//a[normalize-space()='%s']]" \
                             "/preceding-sibling::td[1]/input" % (sg_name,)

REGEX_ETF_SELECTION = 'etf_selection'
ETF_TBODY_ROW = lambda field: '//tbody[@id=\"%s_rowContainer\"]/tr/' % (field,)
ETF_DEL = lambda etf, index, td: 'xpath=//tr[@id="%s_row%s"]/td[%d]/img[1]' % (etf, index, td,)


def go_to_sender_group_edit_table(func):
    """Decorator intended for startup method navigation
    to Sender Group Edit page

    *Notes:*
    Active page should be HAT page containing sender group list
    It is recommended to use this decorator in chain after
    @go_to_access_table
    Decorated method must accept listener_name, sender_group as the first
    and second parameters (after self)
    """

    @functools.wraps(func)
    def worker(self, listener_name, sender_group, *args, **kwargs):
        if not self._is_element_present(EDIT_SG_LINK(sender_group)):
            raise ValueError('Sender Group "%s" is not found for listener "%s"' % \
                             (sender_group, listener_name))
        self.click_button(EDIT_SG_LINK(sender_group))
        return func(self, listener_name, sender_group, *args, **kwargs)

    return worker


HAT_PAGE_PATH = ('Mail Policies', 'HAT Overview')
LISTENER_OPTS = (LISTENER_DROPDOWN, SENDERGROUP_TABLE)


class hat(AccessTableBase):
    """Interaction class for ESA WUI
       Mail Policies -> HAT Overview page.
    """

    def get_keyword_names(self):
        return ['hat_sender_group_add',
                'hat_sender_group_edit_settings',
                'hat_sender_group_delete',
                'hat_sender_group_get_details',

                'hat_edit_sender',
                'hat_delete_sender',
                'hat_find_senders',
                'hat_export',
                'hat_import',
                'hat_edit_order',

                'hat_sender_group_add_sender',
                'hat_sender_group_edit_sender',
                'hat_sender_group_delete_sender',
                'hat_sender_group_add_country',
                'hat_sender_group_edit_country',
                'hat_sender_group_delete_country',
                'hat_sender_group_find_senders',
                'hat_sender_group_clear_all_senders',
                'hat_sender_group_get_senders_list']

    def _get_senders(self):
        sender_list = []
        self._wait_for_element(SENDER_TABLE)
        rows = int(self.get_matching_xpath_count('%s/tbody/tr' % \
                                                 (SENDER_TABLE,)))
        sender_dict_keys = ('sender', 'comment', 'group', 'listener')
        for row in range(2, rows + 1):
            sender_dict = {}
            for col_num, dict_key in enumerate(sender_dict_keys):
                sender_dict[dict_key] = str(self.get_text("%s/tbody/tr[%s]/td[%d]" % \
                                                          (SENDER_TABLE, row, col_num + 1)))
            sender_list.append(sender_dict)
        return sender_list

    def _get_group_settings_controller(self):
        if not hasattr(self, '_group_settings_controller'):
            self._group_settings_controller = SenderGroupSettings(self)
        return self._group_settings_controller

    def _get_sender_settings_controller(self):
        if not hasattr(self, '_sender_settings_controller'):
            self._sender_settings_controller = SenderSettings(self)
        return self._sender_settings_controller

    def _get_country_settings_controller(self):
        if not hasattr(self, '_county_settings_controller'):
            self._country_settings_controller = CountrySettings(self)
        return self._country_settings_controller

    def _get_externalthreatfeeds_settings_controller(self):
        if not hasattr(self, '_externalthreatfeeds_settings_controller'):
            self._externalthreatfeed_settings_controller = ExternalThreatFeedsSettings(self)
        return self._externalthreatfeed_settings_controller

    @go_to_access_table(HAT_PAGE_PATH)
    def hat_find_senders(self, sender_name):
        """Return a list of senders that corresponds to
        sender_name

        *Parameters:*
        - `sender_name`: search string, a part of sender name

        *Exceptions:*
        - `ValueError`: if no listeners are configured

        *Return:*
        List of dictionaries. Each dictionary contains the next items:
        | sender | sender name |
        | comment | custom comment string |
        | group | group name to which this sender belongs |
        | listener | listener name to which this sender belongs |

        *Examples:*
        | @{senders}= | HAT Find Senders | bla.com |
        | :FOR | ${sender} | IN | @{senders} |
        |      | Log | ${sender.sender} |
        """
        FIND_SEARCH_BUTTON = "//input[@value='Find']"
        FIND_SEARCH_TEXT = 'xpath=//input[@name=\'findsender\']'

        self.input_text(FIND_SEARCH_TEXT, sender_name)
        self.click_button(FIND_SEARCH_BUTTON)
        return self._get_senders()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    def hat_sender_group_add(self, listener, **kwargs):
        """Add sender group to specific listener

        *Parameters*:
        - `listener`: name of a listener to which this group will belongs,
        mandatory
        - `name`: sender group name, mandatory
        - `policy`: the basic group policy, mandatory. In common case you can type
        one from these values:
        | BLOCKED |
        | TRUSTED |
        | ACCEPTED |
        | THROTTLED |
        | CONTINUE (no policy) |
        | RELAYED |
        - `order`: order that rules appear in the HAT, number in range 1..5
        - `comment`: your custom comment for this group
        - `sbrs_min`: minimal SenderBase Reputation Score for this group.
        Float number in range -10.0..10.0
        - `sbrs_max`: maximal SenderBase Reputation Score for this group.
        Float number in range -10.0..10.0
        - `include_sbrs_none`: whether to include "None" SBRS scores. Either
        ${True} or ${False}
        - `dns_list`: list of hostnames added to group DNS Lists. Each entry
        is separated from others with comma
        - `nx_domain`: whether to enable the "Connecting host PTR record does
        not exist in DNS" option. Either ${True} or ${False}
        - `serv_fail`: whether to enable the "Connecting host PTR record
        lookup fails due to temporary DNS failure." option. Either ${True}
        or ${False}
        - `not_double_dot_verified`: whether to enable the "Connecting host
        reverse DNS lookup  PTR) does not match the forward DNS lookup (A)."
        option. Either ${True} or ${False}
        - `sender_host`: comma separated string. First enter is sender host IPv4
        or IPv6 and the second is optional entry comment
        - `geo_location`: a dictionary with county name as key and comment as value

        *Examples:*
        | HAT Sender Group Add | InboundMail | name=my new sender group |
        | ... | order=2 | comment=my super group | sbrs_min=1.0 | sbrs_max=5.0 |
        | ... | nx_domain=${True} | policy=TRUSTED |
        | ... | sender_host=1.1.1.1, my host comment |
        """
        self.click_button(ADD_SENDERGROUP_BUTTON)

        sender_settings = {}
        etf_kwargs = {}
        if kwargs.has_key('etf_add_sources'):
            etf_kwargs['etf_add_sources'] = kwargs['etf_add_sources']
            del kwargs['etf_add_sources']
        if kwargs.has_key('sender_host'):
            sender = kwargs['sender_host']
            sender_opts = sender.split(',')
            host_ip = sender_opts[0].strip()
            sender_settings = {'sender': host_ip}
            if len(sender_opts) > 1:
                host_comment = ','.join(sender_opts[1:]).strip()
                sender_settings.update({'comment': host_comment})
            del kwargs['sender_host']
        elif kwargs.has_key('geo_location'):
            sender_settings = eval(kwargs['geo_location'])
            del kwargs['geo_location']
        else:
            sender_settings = None
        controller = self._get_group_settings_controller()
        controller.set(kwargs)
        if sender_settings is not None:
            self.click_button(SUBMIT_AND_ADD)
            if sender_settings.has_key('sender'):
                sender_controller = self._get_sender_settings_controller()
            else:
                sender_controller = self._get_country_settings_controller()
            sender_controller._listener = listener
            sender_controller._method = 'add'
            sender_controller.set(sender_settings)
        if etf_kwargs.has_key('etf_add_sources'):
            etf_controller = self._get_externalthreatfeeds_settings_controller()
            list_src = etf_kwargs['etf_add_sources']
            etf_controller.add_etf_sources(sources=list_src)
        self._click_submit_button()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    @go_to_sender_group_edit_table
    def hat_sender_group_edit_settings(self, listener, sender_group, **kwargs):
        """Edit the sender group settings of specific listener

        *Parameters*:
        - `listener`: name of a listener to which this group will belongs,
        mandatory
        - `sender_group`: name of existing sender group to be edited
        - `name`: new sender group name, mandatory
        - `policy`: the basic group policy, mandatory. In common case you can type
        one from these values:
        | BLOCKED |
        | TRUSTED |
        | ACCEPTED |
        | THROTTLED |
        | CONTINUE (no policy) |
        | RELAYED |
        - `comment`: your custom comment for this group
        - `sbrs_min`: minimal SenderBase Reputation Score for this group.
        Float number in range -10.0..10.0
        - `sbrs_max`: maximal SenderBase Reputation Score for this group.
        Float number in range -10.0..10.0
        - `include_sbrs_none`: whether to include "None" SBRS scores. Either
        ${True} or ${False}
        - `dns_list`: list of hostnames added to group DNS Lists. Each entry
        is separated from others with comma
        - `nx_domain`: whether to enable the "Connecting host PTR record does
        not exist in DNS" option. Either ${True} or ${False}
        - `serv_fail`: whether to enable the "Connecting host PTR record
        lookup fails due to temporary DNS failure." option. Either ${True}
        or ${False}
        - `not_double_dot_verified`: whether to enable the "Connecting host
        reverse DNS lookup  PTR) does not match the forward DNS lookup (A)."
        option. Either ${True} or ${False}

        *Exceptions:*
        - `ValueError`: if sender group is not found for given listener

        *Examples:*
        | HAT Sender Group Edit Settings | InboundMail | WHITELIST | name=new whitelist name |
        | ... | comment=my super group | sbrs_min=1.0 | sbrs_max=5.0 |
        | ... | nx_domain=${True} | policy=TRUSTED |
        """
        self.click_button(EDIT_SG_SETTINGS_BUTTON)

        etf_kwargs = {}
        if kwargs.has_key('etf_add_sources'):
            etf_kwargs['etf_add_sources'] = kwargs['etf_add_sources']
            del kwargs['etf_add_sources']
        if kwargs.has_key('etf_del_sources'):
            etf_kwargs['etf_del_sources'] = kwargs['etf_del_sources']
            del kwargs['etf_del_sources']
        if kwargs.has_key('etf_action'):
            etf_kwargs['etf_action'] = kwargs['etf_action']
            del kwargs['etf_action']
        controller = self._get_group_settings_controller()
        controller.set(kwargs)
        etf_controller = self._get_externalthreatfeeds_settings_controller()
        if etf_kwargs.has_key('etf_action'):
            if etf_kwargs['etf_action'].lower() == 'delete':
                list_src = etf_kwargs['etf_del_sources']
                etf_controller.delete_etf_sources(sources=list_src)
            elif etf_kwargs['etf_action'].lower() == 'delete_all':
                etf_controller.delete_all_etf_sources()
        if etf_kwargs.has_key('etf_add_sources'):
            list_src = etf_kwargs['etf_add_sources']
            etf_controller.edit_etf_sources(sources=list_src)

        self._click_submit_button(check_result=False)

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    def hat_sender_group_delete(self, listener, sender_group):
        """Delete existing Sender Group

        *Parameters:*
        - `listener`: name of a listener to which this group belongs,
        mandatory
        - `sender_group`: name of a sender group to be deleted

        *Exceptions:*
        - `ValueError`: if sender group is not found for given listener

        *Examples:*
        | HAT Sender Group Delete | InboundMail | My Super Sender Group |
        """
        CONTINUE_BUTTON = "xpath=//button[@type='button']"
        if not self._is_element_present(DELETE_SG_LINK(sender_group)):
            raise ValueError('Sender Group "%s" is not found for listener "%s"' % \
                             (sender_group, listener))
        self.click_button(DELETE_SG_LINK(sender_group), 'don\'t wait')
        self.click_button(CONTINUE_BUTTON)

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    @go_to_sender_group_edit_table
    def hat_sender_group_get_details(self, listener, sender_group):
        """Get existing Sender Group details

        *Parameters:*
        - `listener`: name of a listener to which this group belongs,
        mandatory
        - `sender_group`: name of a sender group to be scanned for details,
        mandatory

        *Return:*
        Dictionary with the next items:
        | name | sender group name |
        | policy | the basic group policy. In common case you can get
        one from these values: BLOCKED, TRUSTED, ACCEPTED, THROTTLED,
        CONTINUE (no policy), RELAYED |
        | comment | your custom comment for this group |
        | sbrs_min | minimal SenderBase Reputation Score for this group.
        Float number in range -10.0..10.0 |
        | sbrs_max | maximal SenderBase Reputation Score for this group.
        Float number in range -10.0..10.0 |
        | include_sbrs_none | whether to include "None" SBRS scores. Either
        ${True} or ${False} |
        | dns_list | list of hostnames added to group DNS Lists. Each entry
        is separated from others with comma |
        | nx_domain | whether the "Connecting host PTR record does
        not exist in DNS" option is enabled. Either ${True} or ${False} |
        | serv_fail | whether the "Connecting host PTR record
        lookup fails due to temporary DNS failure." option is enabled.
        Either ${True} or ${False} |
        | not_double_dot_verified | whether the "Connecting host reverse DNS
        lookup  PTR) does not match the forward DNS lookup (A)." option
        is enabled. Either ${True} or ${False} |

        *Examples:*
        | ${group_details} | HAT Sender Group Get Details | InboundMail |
        | ... | My Super Sender Group |
        | ${name} | Get From Dictionary | ${group_details} | name |
        | Log | ${name} |
        """
        self.click_button(EDIT_SG_SETTINGS_BUTTON)

        controller = self._get_group_settings_controller()
        details_dict = controller.get()
        self.click_button(CANCEL_BUTTON)
        return details_dict

    @go_to_access_table(HAT_PAGE_PATH)
    def hat_edit_sender(self, name, new_name=None, comment=None):
        """Edit the given sender listed using HAT find function

        *NOT IMPLEMENTED YET*

        *Parameters:*
        - `name`: sender name to be edited
        - `new_name`: new sender name to be used instead
        - `comment`: your custom comment
        """
        raise NotImplementedError()

    @go_to_access_table(HAT_PAGE_PATH)
    def hat_delete_sender(self, name):
        """Edit the given sender listed using HAT find function

        *NOT IMPLEMENTED YET*

        *Parameters:*
        - `name`: sender name to deleted
        """
        raise NotImplementedError()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    def hat_export(self, listener, filename):
        """Export list of Sender Groups for given listener

        *NOT IMPLEMENTED YET*

        *Parameters:*
        - `listener`: name of a listener which groups will be
        exported
        - `filename`: local filename for export
        """
        raise NotImplementedError()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    def hat_import(self, listener, filename):
        """Import list of Sender Groups for given listener

        *NOT IMPLEMENTED YET*

        *Parameters:*
        - `listener`: name of a listener which groups will be
        imported
        - `filename`: local filename for import
        """
        raise NotImplementedError()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    @set_speed(0)
    def hat_edit_order(self, listener, order_dict):
        """Edit order of Sender Groups for given listener

        *Parameters:*
        - `listener`: name of a listener to which group order
        will be edited
        - `order_dict`: dictionary with key as
        Sender Group name and value is the order number
        to be assigned to it

        *Exceptions:*
        - `ValueError`: if there is no Sender Group with given name

        *Examples:*
        | ${new_order}= | Create Dictionary |
        | ... | WHITELIST | 30 |
        | ... | BLACKLIST | 10 |
        | HAT Edit Order | InBoundMail | ${new_order} |
        """
        self.click_button(EDIT_ORDER_BUTTON)
        for group_name, group_num in order_dict.iteritems():
            if self._is_element_present(ORDER_EDIT(group_name)):
                self.input_text(ORDER_EDIT(group_name), group_num)
            else:
                raise ValueError('There is no Sender Group named %s' % \
                                 (group_name,))
        self._click_submit_button()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    @go_to_sender_group_edit_table
    def hat_sender_group_add_sender(self, listener, sender_group,
                                    sender_name, comment=None):
        """Add a sender to existing Sender Group

        *Parameters:*
        - `listener`: name of a listener to which this group belongs,
        mandatory
        - `sender_group`: name of a sender group to be changed,
        mandatory
        - `sender_name`: name of a new sender
        - `comment`: custom comment string, optional

        *Examples:*
        | HAT Sender Group Add Sender | InboundMail | WHITELIST |
        | ... | example.com | My custom sender |
        """
        self.click_button(ADD_SENDER_BUTTON)

        controller = self._get_sender_settings_controller()
        controller._listener = listener
        controller._method = 'add'
        settings = {'sender': sender_name}
        if comment is not None:
            settings.update({'comment': comment})
        controller.set(settings)
        self._click_submit_button()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    @go_to_sender_group_edit_table
    def hat_sender_group_edit_sender(self, listener, sender_group,
                                     sender_name, **kwargs):
        """Edit sender in existing Sender Group

        *Parameters:*
        - `listener`: name of a listener to which this group belongs,
        mandatory
        - `sender_group`: name of a sender group to be changed,
        mandatory
        - `sender_name`: name of existing sender
        - `new_sender_name`: new sender name
        - `comment`: new comment string

        *Exceptions:*
        - `ValueError`: if sender_name doesn't exist in sender_group

        *Examples:*
        | HAT Sender Group Edit Sender | InboundMail | WHITELIST |
        | ... | 1.1.1.1 | new_sender_name=2.2.2.2 | comment=new comment |
        """
        if not self._is_element_present(EDIT_SENDER_LINK(sender_name)):
            raise ValueError('Sender "%s" is not found in group "%s"' % \
                             (sender_name, sender_group))
        self.click_button(EDIT_SENDER_LINK(sender_name))

        controller = self._get_sender_settings_controller()
        controller._listener = listener
        controller._method = 'edit'
        settings = {}
        if kwargs.has_key('new_sender_name'):
            settings.update({'sender': kwargs['new_sender_name']})
        if kwargs.has_key('comment'):
            settings.update({'comment': kwargs['comment']})
        controller.set(settings)
        self._click_submit_button()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    @go_to_sender_group_edit_table
    def hat_sender_group_delete_sender(self, listener, sender_group,
                                       sender_name):
        """Delete sender from existing Sender Group

        *Parameters:*
        - `listener`: name of a listener to which this group belongs,
        mandatory
        - `sender_group`: name of a sender group to be changed,
        mandatory
        - `sender_name`: name of existing sender to be deleted

        *Exceptions:*
        - `ValueError`: if sender_name doesn't exist in sender_group

        *Examples:*
        | HAT Sender Group Delete Sender | InboundMail | WHITELIST |
        | ... | 1.1.1.1 |
        """
        if not self._is_element_present(DELETE_SENDER_CB(sender_name)):
            raise ValueError('Sender "%s" is not found in group "%s"' % \
                             (sender_name, sender_group))
        self.select_checkbox(DELETE_SENDER_CB(sender_name))
        self.click_button(DELETE_SENDER_BUTTON, 'don\'t wait')
        self._click_continue_button()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    @go_to_sender_group_edit_table
    def hat_sender_group_find_senders(self, listener, sender_group, text):
        """Find sender(s) based on search text in existing Sender Group

        *NOT IMPLEMENTED YET*

        *Parameters:*
        - `listener`: name of a listener to which this group belongs,
        mandatory
        - `sender_group`: name of a sender group to be searched,
        mandatory
        - `text`: a part of sender(s) name

        *Return:*
        List of found senders
        """
        raise NotImplementedError()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    @go_to_sender_group_edit_table
    def hat_sender_group_clear_all_senders(self, listener, sender_group):
        """Clear all senders from particular Sender Group

        *Exceptions*:
        - `ValueError`: if there are no sender for the particular sender
        group

        *Parameters:*
        - `listener`: name of a listener to which this group belongs,
        mandatory
        - `sender_group`: name of a sender group to be cleared,
        mandatory

        *Examples:*
        | HAT Sender Group Clear All Senders | InBoundMail | WHITELIST |
        """
        if self._is_text_present('There are no senders.'):
            raise ValueError('There are no senders in the sender group ' \
                             '%s of listener %s' % (listener, sender_group))
        self.select_checkbox(CLEAR_ALL_SENDERS_CB)
        self.click_button(DELETE_SENDER_BUTTON, 'don\'t wait')
        self._click_continue_button()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    @go_to_sender_group_edit_table
    def hat_sender_group_get_senders_list(self, listener, sender_group):
        """Return all senders present in Sender Group

        *NOT IMPLEMENTED YET*

        *Parameters:*
        - `listener`: name of a listener to which this group belongs,
        mandatory
        - `sender_group`: name of a sender group to be searched for senders,
        mandatory
        """
        raise NotImplementedError()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    @go_to_sender_group_edit_table
    def hat_sender_group_add_country(self, listener, sender_group, countries):
        """Add single or multple country name(s) to existing Sender Group

        *Parameters:*
        - `listener`: name of a listener to which this group belongs,
        mandatory
        - `sender_group`: name of a sender group to be changed,
        mandatory
        - `countries`: dictionary of country names with comments

        *Examples:*
        | ${countries}=       | Create Dictionary       |
        | ... | Afghanistan   | Match-for-Afghanistan   |
        | ... | Aland Islands | Match-for-Aland Islands |
        | ... | Albania       | Match-for-Albania       |
        | ... | Bahamas       | Match-for-Bahamas       |
        | ... | Bermuda       | Match-for-Bermuda       |
        | ... | China         | Match-for-China         |
        | ... | Colombia      | Match-for-Colombia      |
        | HAT Sender Group Add Sender                   |
        | ... | InboundMail                             |
        | ... | WHITELIST                               |
        | ... | ${countries}                            |
        """
        self.click_button(ADD_COUNTRY_BUTTON)
        controller = self._get_country_settings_controller()
        controller._listener = listener
        controller._method = 'add'
        controller.set(countries)
        self._click_submit_button()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    @go_to_sender_group_edit_table
    def hat_sender_group_edit_country(self, listener, sender_group, country_name, settings):
        """Edit sender in existing Sender Group

        *Parameters:*
        - `listener`: name of a listener to which this group belongs,
        mandatory
        - `sender_group`: name of a sender group to be changed,
        mandatory
        - `country_name`: name of the country to edit
        - `new_country_name`: name of the new country
        - `new_comment`: comment for the new country

        *Exceptions:*
        - `ValueError`: if country_name doesn't exist in sender_group

        *Examples:*
        | ${new_country}= | Create Dictionary | India [in] | Indian Sender |
        | HAT Sender Group Edit Country | InboundMail | WHITELIST |
        | ... | Afghanistan [af] | new_country_name=India [in] | comment=new comment |
        """
        if not self._is_element_present(EDIT_SENDER_LINK(country_name)):
            raise ValueError('Country "%s" is not found in group "%s"' % \
                             (country_name, sender_group))
        self.click_button(EDIT_SENDER_LINK(country_name))

        controller = self._get_country_settings_controller()
        controller._listener = listener
        controller._method = 'edit'
        controller.set(settings)
        self._click_submit_button()

    @go_to_access_table(HAT_PAGE_PATH, LISTENER_OPTS)
    @go_to_sender_group_edit_table
    def hat_sender_group_delete_country(self, listener, sender_group, countries):
        """Delete single or multiple country name(s) from existing Sender Group

        *Parameters:*
        - `listener`: name of a listener to which this group belongs,
        mandatory
        - `sender_group`: name of a sender group to be changed,
        mandatory
        - `countries`: name of country to be deleted. value can be a
                       string or a list.

        *Exceptions:*
        - `ValueError`: if country name doesn't exist in the given sender group

        *Examples:*
        | HAT Sender Group Delete Country |
        | ...       |       InboundMail   |
        | ...       |       WHITELIST     |
        | ...       |       China         |

        | ${countries}= | Create List     |
        | ...           | Albania         |
        | ...           | Bermuda         |
        | ...           | Afghanistan     |
        | HAT Sender Group Delete Country |
        | ...           | InboundMail     |
        | ...           | BLACKLIST       |
        | ...           | ${countries}    |
        """
        if countries:
            if type(countries) != list:
                countries = countries,
                countries = list(countries)
            for country_name in countries:
                if not self._is_element_present(DELETE_SENDER_CB(country_name)):
                    raise ValueError('Country "%s" is not found in group "%s"' % \
                                     (country_name, sender_group))
                self.select_checkbox(DELETE_SENDER_CB(country_name))

            self.click_button(DELETE_SENDER_BUTTON, "don't wait")
            self._click_continue_button("Delete Senders")

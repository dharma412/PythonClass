#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/admin/shutdown_suspend_def/mail_operations.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.guicommon import Wait
from common.gui.guicommon import GuiCommon
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

LISTENERS_DUMMY = ('Listeners', None)
DOMAINS_DUMMY = ('Suspend Delivery for', None)
SUSPEND_DELAY = ('Connections Close Timeout',
                 "//input[@name='delay_suspend']")

LISTENERS_TABLE = "//th[normalize-space()='Receiving:']/" \
                  "following::table[contains(@class, 'cols')]"
ALL_LISTENERS = "{0}//tr[.//input]".format(LISTENERS_TABLE)
LISTENER_NAME_BY_IDX = lambda row_idx: "{0}[{1}]/td". \
    format(ALL_LISTENERS, row_idx)
SUSPEND_CELL_BY_IDX = lambda row_idx: "{0}[{1}]/td[2]". \
    format(ALL_LISTENERS, row_idx)
SUSPEND_CB_BY_IDX = lambda row_idx: "{0}//input". \
    format(SUSPEND_CELL_BY_IDX(row_idx))
RESUME_CELL_BY_IDX = lambda row_idx: "{0}[{1}]/td[3]". \
    format(ALL_LISTENERS, row_idx)
RESUME_CB_BY_IDX = lambda row_idx: "{0}//input". \
    format(RESUME_CELL_BY_IDX(row_idx))
STATE_CELL_BY_LISTENER_NAME = lambda name, state_cell_idx: \
    "{0}//td[normalize-space()='{1}']/following-sibling::td[{2}]". \
        format(LISTENERS_TABLE, name, state_cell_idx)

DOMAINS_CONTAINER = "//ul[contains(@class, 'combobox-choices')]"
DOMAINS_EDIT_CONTAINER = "{0}/li[contains(@class, 'search-field')]". \
    format(DOMAINS_CONTAINER)
ALL_DOMAINS = "{0}/li[contains(@class, 'search-choice')]". \
    format(DOMAINS_CONTAINER)
DOMAIN_DELETE_BY_IDX = lambda domain_idx: "{0}[{1}]/a".format(ALL_DOMAINS,
                                                              domain_idx)
DOMAIN_TEXT_BY_IDX = lambda domain_idx: "{0}[{1}]".format(ALL_DOMAINS,
                                                          domain_idx)

COMMIT_BUTTON = "//input[@name='SuspendResume']"

DOMAIN_ADD = "//*[@id='form']/dl[2]/dd/table/tbody/tr[3]/td/div[1]/ul/li/input"


class MailOperationsForm(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def _get_listeners_mapping(self):
        listeners_count = int(self.gui.get_matching_xpath_count(ALL_LISTENERS))
        mapping = {}
        for row_idx in xrange(1, 1 + listeners_count):
            name = self.gui.get_text(LISTENER_NAME_BY_IDX(row_idx))
            if self.gui._is_element_present(SUSPEND_CB_BY_IDX(row_idx)):
                suspend_cb_locator = SUSPEND_CB_BY_IDX(row_idx)
            else:
                suspend_cb_locator = None
            if self.gui._is_element_present(RESUME_CB_BY_IDX(row_idx)):
                resume_cb_locator = RESUME_CB_BY_IDX(row_idx)
            else:
                resume_cb_locator = None
            mapping[name] = (suspend_cb_locator, resume_cb_locator)
        return mapping

    def _set_listeners_state(self, settings):
        listeners_mapping = self._get_listeners_mapping()
        if isinstance(settings, basestring):
            # state is set for all listeners
            state_to_set = settings
            settings = listeners_mapping.copy()
            for listener_name in settings.iterkeys():
                settings[listener_name] = state_to_set
        if not set(settings.keys()).issubset(set(listeners_mapping.keys())):
            raise ValueError('Unknown listener name(s) "{0}". Available ' \
                             'listener names are: {1}'.format(
                list(set(settings.keys()) - set(listeners_mapping.keys()))),
                listeners_mapping.keys())
        for listener_name, state in settings.iteritems():
            suspend_cb_locator, resume_cb_locator = listeners_mapping[listener_name]
            if state.lower() == 'suspend':
                if suspend_cb_locator is not None:
                    print "SUSPEND", suspend_cb_locator
                    self.gui._select_checkbox(suspend_cb_locator)
                else:
                    print('"{0}" listener is already set to {1}'.format(listener_name,
                                                                        state))
            elif state.lower() == 'resume':
                if resume_cb_locator is not None:
                    self.gui._select_checkbox(resume_cb_locator)
                else:
                    print('"{0}" listener is already set to {1}'.format(listener_name,
                                                                        state))
            else:
                raise ValueError('Unknown state value "{0}" is set for listener "{1}. ' \
                                 'Available states are: {2}'.format(state, listener_name,
                                                                    ('suspend', 'resume')))

    def _get_listeners_state(self):
        listeners_mapping = self._get_listeners_mapping()
        listeners_state = {}
        for listener_name, cb_locators in listeners_mapping.iteritems():
            if cb_locators[0] is None:
                state_cell_locator = STATE_CELL_BY_LISTENER_NAME(listener_name, 1)
            else:
                state_cell_locator = STATE_CELL_BY_LISTENER_NAME(listener_name, 2)
            listeners_state[listener_name] = self.gui.get_text(state_cell_locator).strip()
        return listeners_state

    def _char_to_java_keycode(self, char):
        """Works only for ASCII characters (will
        transform everything to lowercase)"""
        if ord('a') <= ord(char) <= ord('z'):
            return ord(char.upper())
        else:
            return ord(char)

    def _set_domains(self, domains):
        # clear existing domain records first
        while self.gui._is_element_present(DOMAIN_DELETE_BY_IDX(1)):
            self.gui.click_element(DOMAIN_DELETE_BY_IDX(1), "don't wait")
        self.gui.click_element(DOMAINS_EDIT_CONTAINER, "don't wait")
        self.gui.focus(DOMAINS_EDIT_CONTAINER)
        text_to_input = ' '.join(domains) + ' ' if domains else ''
        self.gui.input_text(DOMAIN_ADD, text_to_input)
        if text_to_input:
            Wait(until=self.gui._is_element_present,
                 timeout=20,
                 msg='Failed to set domains list within 20 seconds timeout'). \
                wait(DOMAIN_TEXT_BY_IDX(len(domains)))

    def _get_domains(self):
        domains_count = int(self.gui.get_matching_xpath_count(ALL_DOMAINS))
        result = []
        for domain_idx in xrange(1, 1 + domains_count):
            result.append(self.gui.get_text(DOMAIN_TEXT_BY_IDX(domain_idx)))
        return result

    @set_speed(0, 'gui')
    def set(self, new_value):
        if LISTENERS_DUMMY[0] in new_value:
            self._set_listeners_state(new_value[LISTENERS_DUMMY[0]])
        if DOMAINS_DUMMY[0] in new_value:
            domains = new_value[DOMAINS_DUMMY[0]]
            if isinstance(domains, basestring):
                self._set_domains(map(lambda x: x.strip(),
                                      new_value[DOMAINS_DUMMY[0]].split(',')))
            elif isinstance(domains, list) or isinstance(domains, tuple):
                self._set_domains(domains)
            else:
                raise ValueError('{0} value should be either string or list.' \
                                 'Current value type is {1}'.format(
                    DOMAINS_DUMMY[0], type(domains)))
        self._set_edits(new_value, SUSPEND_DELAY)

    @set_speed(0, 'gui')
    def get(self):
        result = {}
        result[LISTENERS_DUMMY[0]] = self._get_listeners_state()
        result[DOMAINS_DUMMY[0]] = self._get_domains()
        result.update(self._get_values(SUSPEND_DELAY))
        return result

    def commit(self):
        self.gui.click_button(COMMIT_BUTTON)
        self.gui._check_action_result()

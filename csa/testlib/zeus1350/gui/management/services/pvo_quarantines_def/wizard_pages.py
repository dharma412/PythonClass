#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/management/services/pvo_quarantines_def/wizard_pages.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

import time

from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs
from common.util.sarftime import CountDownTimer

# TBD: remove ESA PVO Quarantine from SMA centralized quarantine
REMOVE_FROM_CENTRALIZED_QUARANTINE_BUTTON = \
    "//input[@type='button' and contains(@value, 'Remove from Centralized Quarantine')]"

WIZARD_MODE_CUSTOM = 'Custom'
WIZARD_MODE_AUTOMATIC = 'Automatic'
WIZARD_MODE_KEY = 'PQ Migration Mode'


class PVOMigrationBasePage(InputsOwner):
    NEXT_BUTTON = "//input[@type='button' and contains(@value, 'Next')]"

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    registered_inputs = _get_registered_inputs

    def go_to_next(self):
        self.gui.click_button(self.NEXT_BUTTON)


class PVOMigrationCustomPage(PVOMigrationBasePage):
    TABLE_ROWS_WITH_CHECKBOXES = \
        "//div[@id='quarantineContainer']/div[3]/table/tbody[2]/tr[.//input]"

    PQ_CHECKBOX = lambda self, idx: \
        "%s[%s]/td[1]/div/input[@type='checkbox']" % \
        (self.TABLE_ROWS_WITH_CHECKBOXES, idx)
    PQNAME = lambda self, idx: \
        "%s[%s]/td[1]//label/text()" % \
        (self.TABLE_ROWS_WITH_CHECKBOXES, idx)
    ESA_NAME = lambda self, idx: \
        "%s[%s]/td[2]//span/text()" % (self.TABLE_ROWS_WITH_CHECKBOXES, idx)

    PQ_MAPPING = ('Policy Quarantines Mapping', None)

    NEW_QUARANTINE_INPUT_FIELD = "//input[@id='new_quarantine_name']"
    ADD_QUARANTINE_BUTTON = \
        "//input[@type='button' and contains(@value, 'Add to Centralized Quarantine')]"

    LOCAL_QUAR_SEPARATOR = '\n'
    HOSTS_SEPARATOR = '\t'

    CENTRAL_QUARANTINE_COMBO_LOCATOR = "//select[@id='central_quarantine']"
    CENTRAL_QUARANTINE_NEW_NAME = "Create new Centralized Quarantine"

    RESULT_QUARANTINE_NAME = lambda self, quar_name: \
        "//div[@id='treeviewContainer']//span[@class='ygtvlabel' and contains(.,'%s')]" % \
        (quar_name,)

    def _wait_for_result_quarantine_name_loading(self, quar_name):
        SLEEP_INTERVAL = 1
        TIMEOUT = 15
        tmr = CountDownTimer(TIMEOUT).start()
        while tmr.is_active():
            time.sleep(SLEEP_INTERVAL)
            if self.gui._is_element_present(self.RESULT_QUARANTINE_NAME(quar_name)):
                return
        raise TimeoutError('Quarantine %s has not been added' \
                           'within %d-seconds timeout' % (quar_name, TIMEOUT))

    def _get_checkbox_mapping(self):
        if hasattr(self, '_cached_mapping'):
            return self._cached_mapping
        else:
            self._cached_mapping = {}

        rows_count = int(self.gui.get_matching_xpath_count(self.TABLE_ROWS_WITH_CHECKBOXES))
        for row_idx in xrange(1, rows_count + 1):
            full_esa_name = self.gui.get_text(self.ESA_NAME(row_idx))
            esa_name = full_esa_name.split('(')[0].strip()
            policy_quarantine_name = self.gui.get_text(self.PQNAME(row_idx))
            self._cached_mapping[policy_quarantine_name + self.LOCAL_QUAR_SEPARATOR + esa_name] = \
                self.PQ_CHECKBOX(row_idx)
        return self._cached_mapping

    def _get_registered_inputs(self):
        static_inputs = super(PVOMigrationCustomPage, self)._get_registered_inputs()
        dynamic_inputs = self._get_checkbox_mapping().items()
        return static_inputs + dynamic_inputs

    def _extract_quar_name(self, checkbox_name):
        return checkbox_name.split(self.LOCAL_QUAR_SEPARATOR)[0]

    def _extract_host_name(self, checkbox_name):
        return checkbox_name.split(self.LOCAL_QUAR_SEPARATOR)[1]

    def _parse_hosts_migration_settings(self, quarantines_map):

        for sma_quar_name, local_quarantines in quarantines_map.iteritems():
            assert (isinstance(local_quarantines, basestring))

            checkbox_mapping = self._get_checkbox_mapping()
            settings = {}
            if local_quarantines.lower() == 'all':
                # set all checkboxes
                settings = dict.fromkeys(checkbox_mapping, True)
            elif local_quarantines.find(self.LOCAL_QUAR_SEPARATOR) >= 0:
                # set separate checkboxes
                # if the values are  Quarantine_name\nhostname\tQuarantine_name\nhostname
                settings = dict.fromkeys(local_quarantines.split(self.HOSTS_SEPARATOR), True)
            else:
                # set checkboxes by host
                # if the values are  hostname\thostname
                settings = dict(map(lambda x: \
                                        (x, self._extract_host_name(x) in \
                                         local_quarantines.split(self.HOSTS_SEPARATOR)),
                                    checkbox_mapping.iterkeys()))

            self._set_checkboxes(settings, *checkbox_mapping.items())

            # Add these local quarantines to sma quarntine (create if not exists)
            sma_quarantines_list = \
                self.gui.get_list_items(self.CENTRAL_QUARANTINE_COMBO_LOCATOR)
            sma_quarantines_list = filter(lambda x: \
                                              x != self.CENTRAL_QUARANTINE_NEW_NAME,
                                          sma_quarantines_list)
            quar_names_mapping = dict(map(lambda x: \
                                              (x.split('(')[0].strip(), x), sma_quarantines_list))

            if sma_quar_name in quar_names_mapping.keys():
                self.gui.select_from_list(self.CENTRAL_QUARANTINE_COMBO_LOCATOR,
                                          quar_names_mapping[sma_quar_name])
                result_quar_name = quar_names_mapping[sma_quar_name]
            else:
                self.gui.select_from_list(self.CENTRAL_QUARANTINE_COMBO_LOCATOR,
                                          self.CENTRAL_QUARANTINE_NEW_NAME)
                self.gui.input_text(self.NEW_QUARANTINE_INPUT_FIELD,
                                    sma_quar_name)
                result_quar_name = sma_quar_name

            self.gui.click_button(self.ADD_QUARANTINE_BUTTON, 'don\'t wait')
            self._wait_for_result_quarantine_name_loading(result_quar_name)

    def set(self, settings):
        assert (settings.has_key(self.PQ_MAPPING[0]))
        self._parse_hosts_migration_settings(settings[self.PQ_MAPPING[0]])


class PVOMigrationModePage(PVOMigrationBasePage):
    POLICY_QUARANTINE_MIGRATION_MODE_RADIO_GROUP = \
        (WIZARD_MODE_KEY,
         {WIZARD_MODE_AUTOMATIC: "//input[@id='automatic_mode']",
          WIZARD_MODE_CUSTOM: "//input[@id='custom_mode']"})

    def set(self, new_value):
        self._set_radio_groups(new_value,
                               self.POLICY_QUARANTINE_MIGRATION_MODE_RADIO_GROUP)


class PVOMigrationAutomaticPage(PVOMigrationBasePage):
    def set(self, new_value):
        # there's no inputs to set on the page
        pass


class PVOMigrationFinalPage(PVOMigrationBasePage):
    def set(self, new_value):
        # there's no inputs to set on the page
        pass

    def go_to_next(self):
        # go to the last page and submit
        self.gui._click_submit_button()

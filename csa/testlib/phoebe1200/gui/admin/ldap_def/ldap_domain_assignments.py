#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/admin/ldap_def/ldap_domain_assignments.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import common.gui.guiexceptions as guiexceptions
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

QUERY_NAME = ('Query Name',
              "//input[@name='query_name']")
QUERY_TYPE_COMBO = ('Query Type',
                    "//select[@id='query_type']")
DEFAULT_QUERY_COMBO = ('Default Query',
                       "//select[@id='default_domain_query']")
ADD_ROW_BUTTON = "//input[@name='domain_assignments_domtable_AddRow']"
ASSIGNMENTS_TABLE = "//table[@id='domain_assignments']"
# index starts from 1
ASSIGNMENT_DELETE_LINK = lambda index: \
    "%s/tbody/tr[%d]/td[@class='itable-delete']/img" % \
    (ASSIGNMENTS_TABLE, index)
# index starts from 0
ASSIGNMENT_DOMAIN_NAME = lambda index: \
    "%s//input[@id='domain_assignments[%d][domain]']" % \
    (ASSIGNMENTS_TABLE, index)
ASSIGNMENT_QUERY_NAME = lambda index: \
    "%s//select[@id='domain_assignments[%d][query]']" % \
    (ASSIGNMENTS_TABLE, index)
# For automated caption verification. Will be caught by get_module_inputs_pairs
DOMAIN_ASSIGNMENTS = ('Domain Assignments', None)
DOMAIN_ASSIGNMENTS_CAPTION = DOMAIN_ASSIGNMENTS[0]


class LDAPDomainAssignments(InputsOwner):
    """Methods for set/get particular domain assignments
    """

    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_edits(new_value,
                        QUERY_NAME)
        self._set_combos(new_value,
                         QUERY_TYPE_COMBO)
        # Page will be reloaded after selecting query type
        self.gui.wait_until_page_loaded()
        self._set_combos(new_value,
                         DEFAULT_QUERY_COMBO)
        if DOMAIN_ASSIGNMENTS_CAPTION in new_value.keys():
            all_assignments = new_value[DOMAIN_ASSIGNMENTS_CAPTION]
            self._set_assignments_list(all_assignments)

    def _clear_existing_assignments(self):
        while self.gui._is_element_present(ASSIGNMENT_DELETE_LINK(2)):
            self.gui.click_element(ASSIGNMENT_DELETE_LINK(2), 'don\'t wait')
        self.gui.click_element(ASSIGNMENT_DELETE_LINK(1), 'don\'t wait')

    def _set_assignments_list(self, values_dict):
        self._clear_existing_assignments()
        index = 0
        for domain_name, query_name in values_dict.iteritems():
            if index > 0:
                # It is not the first element
                self.gui.click_button(ADD_ROW_BUTTON, 'don\'t wait')
            self.gui.input_text(ASSIGNMENT_DOMAIN_NAME(index),
                                domain_name)
            all_options = self.gui.get_list_items(ASSIGNMENT_QUERY_NAME(index))
            if query_name in all_options:
                self.gui.select_from_list(ASSIGNMENT_QUERY_NAME(index),
                                          query_name)
            else:
                raise ValueError('There is no query named "%s"' % (query_name,))
            index += 1

    def get(self):
        raise NotImplementedError()

    def get_test_result(self):
        raise NotImplementedError()

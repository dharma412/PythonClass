#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/admin/ldap_def/ldap_chained_query.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import common.gui.guiexceptions as guiexceptions
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs


QUERY_NAME = ('Query Name',
              "//input[@name='query_name']")
QUERY_TYPE_COMBO = ('Query Type',
                    "//select[@name='query_type']")
ADD_ROW_BUTTON = "//input[@name='queries_domtable_AddRow']"
CHAINED_QUERY_TABLE = "//table[@id='queries']"
# index starts from 1
CHAINED_QUERY_DELETE_LINK = lambda index: \
            "%s/tbody/tr[%d]/td[@class='itable-delete']/img" % \
            (CHAINED_QUERY_TABLE, index)
# index starts from 0
CHAINED_QUERY_QUERY_NAME = lambda index: \
            "%s//select[@id='queries[%d][query]']" % \
            (CHAINED_QUERY_TABLE, index)
# For automated caption verification. Will be caught by get_module_inputs_pairs
CHAINED_QUERY = ('Chained Query', None)
CHAINED_QUERY_CAPTION = CHAINED_QUERY[0]


class LDAPChainedQuery(InputsOwner):
    """Methods for set/get particular LDAP chained query
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
        if CHAINED_QUERY_CAPTION in new_value.keys():
            all_queries = new_value[CHAINED_QUERY_CAPTION]
            self._set_queries_list(all_queries)

    def _clear_existing_queries(self):
        while self.gui._is_element_present(CHAINED_QUERY_DELETE_LINK(2)):
            self.gui.click_element(CHAINED_QUERY_DELETE_LINK(2), 'don\'t wait')
        self.gui.click_element(CHAINED_QUERY_DELETE_LINK(1), 'don\'t wait')

    def _set_queries_list(self, values_list):
        self._clear_existing_queries()
        index = 0
        for query_name in values_list:
            if index > 0:
                # It is not the first element
                self.gui.click_button(ADD_ROW_BUTTON, 'don\'t wait')
            all_options = self.gui.get_list_items(CHAINED_QUERY_QUERY_NAME(index))
            if query_name in all_options:
                self.gui.select_from_list(CHAINED_QUERY_QUERY_NAME(index),
                                          query_name)
            else:
                raise ValueError('There is no query named "%s"' % (query_name,))
            index += 1

    def get(self):
        raise NotImplementedError()

    def get_test_result(self):
        raise NotImplementedError()

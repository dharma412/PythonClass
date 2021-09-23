#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/manager/urllists.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from sal.containers import cfgholder

URL_TABLE = "//table[@class='cols']"
EDIT_LINK = lambda row, col: "//*[@id='content']/form/dl/dd/table/tbody/tr[%d]/td[%d]/a" % (row, col)
URL_LIST_NAME_FIELD = "name=name"
URL_LIST_URLS_FIELD = "name=addresses"
DELETE_ALL_CHECKBOX = "//input[@id='checkbox_all']"
URL_SUBMIT_BUTTON = "//*[@id='content']/form/input[4]"
POLICIES_DIV = "//*[@id='form']/dl/dd/div[2]"
BUTTON_ADD_URL_LIST = "//input[@value='Add URL List...']"
BUTTON_DELETE = "//input[@value='Delete']"
DEL_OPT = \
    lambda row: "//table[@class='cols']/tbody/tr[%d]/td[4]/input" % row


class URLLists(GuiCommon):
    """
    URL Lists page interaction class.
    'Mail Policies -> URL Lists' section.
    """

    def _open_page(self):
        self._navigate_to('Mail Policies', 'URL Lists')

    def get_keyword_names(self):
        return ['url_lists_add',
                'url_lists_edit',
                'url_lists_deleteall',
                'url_lists_delete',
                'url_lists_get_all',
                'url_lists_get_definition']

    def _click_link_to_edit(self, ac_name, table_loc):
        (rowp, colp) = self._cell_indexes(ac_name, table_loc)
        if rowp is None:
            raise ValueError, '"%s" is not present' % (ac_name,)
        self.click_element(EDIT_LINK(rowp + 1, colp + 1))

    def _cell_indexes(self, item_name, table_loc):
        self._info('Getting row, column for %s in %s table' % \
                   (item_name, table_loc))
        try:
            rows = int(self.get_matching_xpath_count('%s//tr' % table_loc))
            cols = int(self.get_matching_xpath_count('%s//th' % table_loc))
            for row in xrange(rows):
                result = map(lambda column: self._get_table_cell('xpath=%s.%s.%s' % \
                                                                 (table_loc, row, column)), xrange(cols))
                if item_name in result:
                    return row, result.index(item_name)
        except guiexceptions.SeleniumClientException:
            return None, None
        return None, None

    def _url_list(self,
                  url_list_name=None,
                  urls=None):
        """ Populates URL Lists table with data.

        Parameters:
        - `url_list_name`: name of the URL List. Mandatory.
        - `urls`: comma seperated urls that needs to be skipped from scanning , Mandatory

        Return:
        None
        """
        if url_list_name is not None:
            self.input_text(URL_LIST_NAME_FIELD, url_list_name)
        if urls is not None:
            self.input_text(URL_LIST_URLS_FIELD, urls)
        self.click_button(URL_SUBMIT_BUTTON, "don't wait")

    def url_lists_add(self,
                      url_list_name=None,
                      urls=None):
        """ Adds new URL Lists.

        Parameters:
        - `url_list_name`: name of the URL List. Mandatory.
        - `urls`: comma seperated urls that needs to be skipped from scanning , Mandatory
        Return:
        None

        Examples:
        | Url Lists Add  |
        | ... | url_list_name=urllist1 |
        | ... | urls=rediff.com,facebook.com |
        """
        self._info('Adding URL Lists %s' % url_list_name)
        self._open_page()
        self.click_button(BUTTON_ADD_URL_LIST)
        self._url_list(url_list_name=url_list_name,
                       urls=urls)

    def url_lists_edit(self,
                       ac_name,
                       url_list_name=None,
                       urls=None):
        """ Edits URL Lists.

        Parameters:
        - `ac_name`: name of URL List to edit. String.
        - `url_list_name`: name of the URL List
        - `urls`: comma seperated urls that needs to be skipped from scanning

        Return:
        None

        Example:
        | Url Lists Edit |
        | ... | urllist1 |
        | ... | url_list_name=urllist2 |
        | ... | urls=cisco.com,ironport.com |
        """
        self._info('Editing URL Lists %s' % ac_name)
        self._open_page()
        self._click_link_to_edit(ac_name, URL_TABLE)
        self._url_list(url_list_name=url_list_name,
                       urls=urls)

    def url_lists_deleteall(self):
        """ Deletes all URL Lists.

        Parameters:
        None

        Return:
            None

        Example:
        | Url Lists Deleteall |
        """
        self._open_page()
        self._select_checkbox(DELETE_ALL_CHECKBOX)
        self.click_button(BUTTON_DELETE, "don't wait")
        self._click_continue_button()

    def url_lists_delete(self, ac_name):
        """ Deletes URL Lists.

        Parameters:
        - `ac_name`:- Name of the url List to be deleted. String.

        Return:
            None

        Example:
        | Url Lists Delete | urllist2 |
        """
        self._info('Deleting URL Lists %s' % ac_name)
        self._open_page()
        (rowp, colp) = self._cell_indexes(ac_name, URL_TABLE)
        if rowp is None:
            raise ValueError, '"%s" url list is not present' % ac_name
        self._select_checkbox(DEL_OPT(rowp + 1))
        self.click_button(BUTTON_DELETE, "don't wait")
        self._click_continue_button()

    def url_lists_get_all(self):
        """ Returns a list of names of all the URL Lists configured.

        Parameters:
        None

        Return:
        List. The names of all the URL Lists configured.
        Example:
        | Url Lists Get All |
        """
        self._info('Getting list of all configured URL Lists')
        self._open_page()
        try:
            rows = int(self.get_matching_xpath_count("%s/tbody/tr" % URL_TABLE))
        except guiexceptions.SeleniumClientException:
            ma_text = self.get_text(POLICIES_DIV)
            return ma_text
        url_lists_configured = []
        for url_indx in range(2, rows + 1):
            urllist_actn = \
                str(self.get_text("%s/tbody/tr[%d]/td" % (URL_TABLE, url_indx)))
            url_lists_configured.append(urllist_actn)
        return url_lists_configured

    def url_lists_get_definition(self, ac_name):
        """ Returns an object with complete details of the given URL List.

        Parameters:
        - `ac_name`: Name of the URL List whose details need to be
        fetched. String.

        Return:
        RecursiveCfgHolder - Returns an object of type RecursiveCfgHolder with
        all the details of the given url list.
        Allows to use '.' to access its keys, like
        cfg.url_list_name, cfg.urls etc

        Example:
        | ${urllists} | Url Lists Get Definition | urllist1 |
        So ${urllists} = {'url_list_name': u'', 'urls': u'cisco.com ironport.com'}
        """
        self._info('Getting options of "%s" url list' % ac_name)
        self._open_page()
        self.items = cfgholder.RecursiveCfgHolder()
        self._click_link_to_edit(ac_name, URL_TABLE)
        self.items.url_list_name = self.get_text(URL_LIST_NAME_FIELD)
        self.items.urls = self.get_text(URL_LIST_URLS_FIELD)
        return self.items

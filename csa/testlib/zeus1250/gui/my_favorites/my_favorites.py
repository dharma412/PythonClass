#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/my_favorites/my_favorites.py#4 $
# $DateTime: 2019/09/16 03:24:49 $
# $Author: kathirup $

import time
from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
from sal.exceptions import ConfigError
import common.gui.guiexceptions as guiexceptions

NOT_DISABLED = "[not( contains(@class,'-disabled'))]"
ADD_PAGE_PATH = ('My Favorites', 'Add This Page to My Favorites')
LIST_PAGE_PATH = ('My Favorites', 'View All My Favorites')
ANY_PAGE_PATH = ['My Favorites']

TASKS_TABLE = "xpath=//table[contains(@class, 'tasks-table')]"
EDIT_LINK = lambda name: "%s//a[normalize-space(text()) = '%s']" \
    % (TASKS_TABLE, name)
ALL_FAVORITES = "//table[contains(@class, 'tasks-table')]//a"
NAME_BY_IDX = lambda index: "%s//tr[%s]//td[2]//a" % (TASKS_TABLE, index)
DRAG_ELEMENT = lambda name: "%s//tr/td[normalize-space(a)='%s']" \
    % (TASKS_TABLE, name)
DELETE_CHECKBOX = lambda name: "%s//tr[normalize-space(td/a) = '%s']//input" \
    % (TASKS_TABLE, name)
DELETE_ALL_CHECKBOX = "%s//tr[1]//input" % (TASKS_TABLE,)
DELETE_BUTTON = "//div[contains(@class, 'delete-button')]/input"
CONFIRM_DELETE_BUTTON = \
    "//div[@id = 'confirmation_dialog']//button[text() ='Delete']"

OK_BUTTON = lambda caption: "xpath=//*[@id='add_to_my_tasks_dialog' or "\
    "contains(dl/dt, 'Edit My Favorite')]//*[(@type='button' and "\
    "text()='%(value)s') or (@type='submit' and @value='%(value)s')]" \
    % {'value': caption}

MY_FAVORITES_MENU = "//div[@id='nav_menu']//a[contains(@class, "\
    "'yuimenubaritemlabel-hassubmenu') and text()='My Favorites']"
ADD_FAVORITE_MENU_LINK = "xpath=//div[@id='nav_menu']"\
    "//a[text()='Add This Page to My Favorites']" + NOT_DISABLED
ADD_FAVORITE_MENU_LINK_DISABLED = "//div[@id='nav_menu']//a[contains(@class, "\
    "'yuimenuitemlabel-disabled') and text()='Add This Page to My Favorites']"
ADD_NEW_BUTTON = "//input[@type='button' and @value='Add New Favorite']" \
    + NOT_DISABLED
CONFIRM_DIALOG_VISIBLE = "//div[@id='confirmation_dialog_c' and "\
    "contains(@style, 'visibility: visible')]"
EDIT_OK_BUTTON = 'Submit'

LANDING_PAGE_MARK = lambda name: "%s//tr[normalize-space(td/a) = '%s']/td[1]" \
    % (TASKS_TABLE, name)
CONFIRM_LANDING_PAGE_BUTTON = \
    "//div[@id = 'confirmation_dialog']//button[text() ='OK']"

MY_FAVORITES_FORM = "//form[contains(dl/dt, 'Edit My Favorite') or "\
    "@name='my_tasks_form']"
DESCRIPTION_INPUT = MY_FAVORITES_FORM + \
    "//textarea[contains(@name, 'description')]"

PAGE_PATH_SELECT = MY_FAVORITES_FORM + "//select[@name='screen']"
NAME_INPUT = MY_FAVORITES_FORM + "//input[@id='task_name']"

class MyFavorites(GuiCommon):
    """ Keywords for My Favorites feature. Its functionality is accessible via
    My Favorites menu in auxiliary menubar.
    """

    def get_keyword_names(self):
        return [
            'my_favorites_add',
            'my_favorites_edit',
            'my_favorites_delete',
            'my_favorites_go_to',
            'my_favorites_drag',
            'my_favorites_get_list',
            'my_favorites_set_landing_page',
        ]

    def _open_page(self):
        self._navigate_to('My Favorites', 'View All My Favorites')

    def _click_ok_button(self, caption, wait):
        self.click_element(OK_BUTTON(caption), "don't wait")
        if wait:
            self.wait_until_page_loaded()

    def _navigate_to_add_form(self):
	time.sleep(60)
        self.mouse_over(MY_FAVORITES_MENU)
	time.sleep(60)
        self.click_link(ADD_FAVORITE_MENU_LINK, "don't wait")

    def _normalize_path(self, path):
        if isinstance(path, basestring):
            path = map(lambda s: s.strip(), path.split(' -> '))
        return path

    def _set_name(self, name):
        self.input_text(NAME_INPUT, name)

    def _set_description(self, desc):
        self.input_text(DESCRIPTION_INPUT, desc)

    def _click_add_new_favorite(self):
        self.click_button(ADD_NEW_BUTTON, "don't wait")

    def _select_page_path_from_list(self, path):
        self._debug('_select_page_path_from_list path = %s' % (path,))
        assert len(path) == 3, 'List path should contain 3 elements'
        (tab, menu, submenu) = path
        LIST_ELEMENT = "/optgroup[starts-with(@label,'%s') and contains(@label,'%s')]" \
            "/option[starts-with(text(),'%s')]" % (tab, menu, submenu)
        VALUE_SELECTOR = PAGE_PATH_SELECT + LIST_ELEMENT
        self._debug('searching for value using xpath: %s' % (VALUE_SELECTOR,))
        value = self.get_value(VALUE_SELECTOR)
        self._debug('found value: %s' % (value,))
        self.select_from_list(PAGE_PATH_SELECT, value)


    def _wait_for_confirm_dialog(self):
        self.wait_until_page_contains_element(CONFIRM_DIALOG_VISIBLE, 5)


    def my_favorites_add(self, path, name=None,
                            description=None,
                            add_via_menu=False,
                            navigate_to_list=False):
        """ Add new page to My Favorites.

        *Parameters:*
        - `path` List with the menu path to the page that should be in favorites.
          Also it could be string in form 'Menu Name -> Menu Item Name'.
          Required.
        - `name` Display name to give to the new favorite. If it's not
          provided then default name will be given by feature. Optional.
        - `description` String with description for the favoried page. Optional.
        - `add_via_menu` Indicates from where to add the page to My Favorites.
          If it set to True keyword will navigate to that page and add it
          to My Favorites via top-right menu. Otherwise the page will be
          added from My Favorites list page. False by default.
        - `navigate_to_list` Ignored if `navigate_to_page` is False.
          Indicate whether to redirect to My Favorites list page after adding
          favorite (using one of form's submit buttons). False by default.

        *Exceptions:*
        - `ValueError`: Raised when `Path` key is not provided.
        - `ConfigError`: Raised when the given page is already favorited.

        *Examples:*
        | ${path}= | Create List | Network | Interfaces |
        | My Favorites Add | ${path} |
        | ... | new_name=Interfaces Page |
        | ... | description=Some Description |
        | ... | add_via_menu=${True} |
        | ... | navigate_to_list=${True} |

        | My Favorites Add | Management Appliance -> Network -> DNS |
        """

        self._debug('path = %s' % (path,))
        path = self._normalize_path(path)
        self._debug('path after = %s' % (path,))

        # this code also check if page with given path exists
        # some pages on SMA does not have tabs so navigate fails

        TAB_BAR = "//div[@id='sma_tabs_container']"

        # some pages on SMA does not have tabs so navigate fails
        if int(self.get_matching_xpath_count(TAB_BAR)) == 0:
            self.go_to('/')

        self.navigate_to(*path)

        if add_via_menu:
            try:
                self.page_should_not_contain_element \
                    (ADD_FAVORITE_MENU_LINK_DISABLED)
            except AssertionError:
                raise ConfigError('Given page is already added to My Favorites')

            self._navigate_to_add_form()

            if name is not None:
                self._set_name(name)

            if description is not None:
                self._set_description(description)

            if navigate_to_list:
                self._click_ok_button('Add and View All My Favorites', True)
            else:
                self._click_ok_button('Add', False)
        else:
            self.navigate_to(*LIST_PAGE_PATH)
            self._click_add_new_favorite()
            self._select_page_path_from_list(path)
            self._set_name(name)
            if description is not None:
                self._set_description(description)
            self._click_ok_button('Add', False)
        time.sleep(2)

    def my_favorites_edit(self, name,
                            new_name=None,
                            path=None,
                            description=None):
        """ Edit existing favorited page.

        *Parameters:*
        - `name`: String name of existing favorited page.
        - `new_name` New display name to give to the favorite. Optional.
        - `path` List with the menu path to the page that should be in favorites.
          Also it could be string in form 'Menu Name -> Menu Item Name'.
          Required.
        - `description` String with new description for the favoried
          page. Optional.

        *Exceptions:*
        - `ValueError`: Raised if given page is not exist.

        *Examples:*
        | ${path}= | Create List | Network | DNS |
        | My Favorites Edit | Interfaces Page |
        | ... | new_name=Another Name For Page |
        | ... | path=${path} |
        | ... | description=New Description |

        | My Favorites Edit | Interfaces Page |
        | ... | new_name=My DNS Page |
        | ... | path=Management Appliance -> Network -> DNS |

        """

        # cannot use @go_to_page(LIST_PAGE_PATH) here
        # because Robot passes argument incorreclty like
        # new_name = 'new_name=My Security Appliances Page'
        self._open_page()

        path = self._normalize_path(path)

        self.click_link(EDIT_LINK(name))

        if path is not None:
            self._select_page_path_from_list(path)
        if new_name is not None:
            self._set_name(new_name)
        if description is not None:
            self._set_description(description)

        self._click_ok_button(EDIT_OK_BUTTON, True)

    @go_to_page(LIST_PAGE_PATH)
    def my_favorites_delete(self, *args):
        """ Delete favorited pages.

        *Parameters:*
        - `args`: unlimited amount of positional arguments. Each argument
          should be the name of favorited page to delete. If no arguments
          passed all favorited pages will be deleted.

        *Examples:*
        | My Favorites Delete | My Page | My Other Page |
        """
        if args:
            for name in args:
                self.click_element(DELETE_CHECKBOX(name), "don't wait")
        else:
            count = int(self.get_matching_xpath_count(ALL_FAVORITES))
            if count == 0:
                return
            self.click_element(DELETE_ALL_CHECKBOX, "don't wait")

        self.click_button(DELETE_BUTTON, "don't wait")

        self._wait_for_confirm_dialog()
        self.click_button(CONFIRM_DELETE_BUTTON, "don't wait")

        ready_msg = 'successfully deleted'
        self.wait_until_page_contains(ready_msg, 5)

    def my_favorites_go_to(self, name):
        """ Navigate to favorited page via My Favorites menu.

        *Parameters:*
        - `name`: name of favorite to navigate to.

        *Examples:*
        | My Favorites Go To | My Interfaces Page |
        """
        self.navigate_to(*(ANY_PAGE_PATH + [name]))

    @go_to_page(LIST_PAGE_PATH)
    def my_favorites_drag(self, source, destination):
        """ Change the order of favorited pages in My Favorites list by drag
        and drop.

        *Parameters:*
        - `source`: name of the page the should be dragged.
        - `destination`: name of the page that `source` should be dropped onto.

        *Examples:*
        | My Favorites Drag | My Page | My Other Page |
        """
        self._drag_and_drop_to_object(DRAG_ELEMENT(source),
                                      DRAG_ELEMENT(destination))

    @go_to_page(LIST_PAGE_PATH)
    def my_favorites_get_list(self):
        """ Get all favorited pages names.

        *Return:*
        List of favorited pages names.

        *Examples:*
        | ${pages} | My Favorites Get List |
        """
        count = int(self.get_matching_xpath_count(ALL_FAVORITES))
        xpaths = map(NAME_BY_IDX, xrange(2, count + 2))
        return map(self.get_text, xpaths)


    @go_to_page(LIST_PAGE_PATH)
    def my_favorites_set_landing_page(self, name):
        """ Change Landing Page to item from My Favorites list

        *Parameters:*
        - `name`: name of favorite to become a new Landing Page.

        *Examples:*
        | My Favorites Set Landing Page | My Page |
        """
        count = int(self.get_matching_xpath_count(ALL_FAVORITES))
        name_found=False
        for i in xrange(2,count+2):
            col="//tr[%s]//td[1]" % (i)
            if self.get_text(NAME_BY_IDX(i)) == name:
                name_found=True
                home_Button=col + "/div[@class='make-button-selected']"
                home_Button_count = int(self.get_matching_xpath_count(TASKS_TABLE.lstrip('xpath=')+home_Button))
                if home_Button_count != 0:
                    self._info('This page is already a landing page')
                else:
                    cell=TASKS_TABLE + col
                    make_home_button=cell + "/div[@class='make-button']"
                    self.mouse_over(cell)
                    self.wait_until_page_contains_element(make_home_button, 2)
                    self.click_element(make_home_button, "don't wait")
                    self._wait_for_confirm_dialog()
                    self.click_button(CONFIRM_LANDING_PAGE_BUTTON, "don't wait")
                    ready_msg = 'Landing Page has been successfully changed'
                    self.wait_until_page_contains(ready_msg, 5)
            if name_found:
                break

        if name_found==False:
                raise guiexceptions.GuiFeatureDisabledError(
                      "Name "+ name+ " not found in the My Favorites list")

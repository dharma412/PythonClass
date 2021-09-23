#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/my_favorites/my_favorites.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import time

from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
from common.util.sarftime import CountDownTimer
from sal.exceptions import ConfigError


from my_favorites_def.my_favorites_add_edit import MyFavoritesAddEdit, PATH_KEY


ADD_PAGE_PATH = ('My Favorites', 'Add This Page to My Favorites')
LIST_PAGE_PATH = ('My Favorites', 'View All My Favorites')
ANY_PAGE_PATH = ['My Favorites']

NAVIGATE_TO_PAGE_KEY = 'Navigate To Page'
NAVIGATE_TO_LIST_KEY = 'Navigate To List'

FAVORITES_TITLE = "//*[@id='page_title' and normalize-space(text())='My Favorites']"
TASKS_TABLE = "//table[contains(@class,'tasks-table')]"
EDIT_LINK = lambda name: "%s//a[normalize-space(text()) = '%s']" % (TASKS_TABLE, name)
ALL_FAVORITES = "//table[contains(@class, 'tasks-table')]//a"
NAME_BY_IDX = lambda index: "%s//tr[td][%s]//a" % (TASKS_TABLE, index)
DRAG_ELEMENT = lambda name: "%s//tr/td[normalize-space(a)='%s']" % (TASKS_TABLE, name)
DELETE_CHECKBOX = lambda name: "%s//tr[normalize-space(td/a) = '%s']//input" % (TASKS_TABLE, name)
DELETE_ALL_CHECKBOX = "%s//tr[1]//input" % (TASKS_TABLE,)
DELETE_BUTTON = "//div[contains(@class, 'delete-button')]/input"
CONFIRM_DELETE_BUTTON = "//div[@id = 'confirmation_dialog']//button[text() ='Delete']"
OK_BUTTON = lambda caption: "//*[@id='add_to_my_tasks_dialog' or "\
    "contains(dl/dt, 'Edit My Favorite')]//*[(@type='button' and "\
    "text()='%(value)s') or (@type='submit' and @value='%(value)s')]" % {'value': caption}
MY_FAVORITES_MENU = "//div[@id='nav_menu']//a[contains(@class, "\
    "'yuimenubaritemlabel-hassubmenu') and text()='My Favorites']"
ADD_FAVORITE_MENU_LINK = "//div[@id='nav_menu']"\
    "//a[text()='Add This Page to My Favorites']"
ADD_FAVORITE_MENU_LINK_DISABLED = "//div[@id='nav_menu']//a[contains(@class, "\
    "'yuimenuitemlabel-disabled') and text()='Add This Page to My Favorites']"
ADD_NEW_BUTTON = "//input[@type='button' and @value='Add New Favorite']"
DELETE_CONFIRM_DIALOG_VISIBLE = "//div[@id='confirmation_dialog_c' and "\
    "contains(@style, 'visibility: visible')]"

ADD_OK_BUTTONS = (('Add', False), ('Add and View All My Favorites', True))
EDIT_OK_BUTTON = 'Submit'


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
            'my_favorites_get_list'
        ]

    def _get_add_edit_controller(self):
        if not hasattr(self, '_add_edit_controller'):
            self._add_edit_controller = MyFavoritesAddEdit(self)
        return self._add_edit_controller

    def _click_ok_button(self, caption, wait):
        self.click_element(OK_BUTTON(caption), 'don\'t wait')
        if wait:
            self.wait_until_page_loaded()

    def _navigate_to_add_form(self):
        self.mouse_over(MY_FAVORITES_MENU)
        self.click_link(ADD_FAVORITE_MENU_LINK, 'don\'t wait')

    def _normalize_path(self, path):
        if isinstance(path, basestring):
            path = map(lambda s: s.strip(), path.split(' -> '))
        return path

    def my_favorites_add(self, values):
        """ Add new page to My Favorites.

        *Parameters:*
        - `values`: dictionary describing page to add and conditions. Valid
          items are:
          | `New Name` | Optional. Display name to give to the new favorite. If
          it's not provided then default name will be given by feature. |
          | `Path` | Required. List with the menu path to the page that should
          be favorited. Also it could be string in form 'Menu Name -> Menu Item Name'. |
          | `Description` | Optional. String with description for the favotied
          page. |
          | `Navigate To Page` | Optional. Boolean. Indicates from where to add
          the page to My Favorites. If it set to True keyword will navigate to
          that page and add it to My Favorites. Otherwise the page will be
          added from My Favorites list page. False by default. |
          | `Navigate To List` | Optional. Boolean. Ignored if `Navigate To
          Page` is False. Indicate whether to redirect to My Favorites list
          page after adding favorite (using one of form's submit buttons).
          False by default. |

        *Exceptions:*
        - `ValueError`: Raised when `Path` key is not provided.
        - `ConfigError`: Raised when the given page is already favorited.

        *Examples:*
        | ${path}= | Create List | Network | Listeners |
        | ${page_settings}= | Create Dictionary | New Name | Listeners Page |
        | ... | Path | ${path} | Description | Some Description |
        | ... | Navigate To Page | ${True} | Navigate To List | ${True} |
        | My Favorites Add | ${page_settings} |

        | ${page_settings}= | Create Dictionary | New Name | HAT Page |
        | ... | Path | Mail Policies -> HAT Overview |
        | My Favorites Add | ${page_settings} |
        """

        if PATH_KEY not in values:
            raise ValueError('Path argument is required.')
        values[PATH_KEY] = self._normalize_path(values[PATH_KEY])

        settings = {NAVIGATE_TO_PAGE_KEY: False, NAVIGATE_TO_LIST_KEY: False}
        settings.update(values)

        navigate_to_page = settings[NAVIGATE_TO_PAGE_KEY]
        navigate_to_list = settings[NAVIGATE_TO_LIST_KEY]
        del settings[NAVIGATE_TO_PAGE_KEY]
        del settings[NAVIGATE_TO_LIST_KEY]

        self.navigate_to(*settings[PATH_KEY])
        try:
            self.page_should_not_contain_element(ADD_FAVORITE_MENU_LINK_DISABLED)
        except AssertionError:
            raise ConfigError('Given page is already added to My Favorites')

        if navigate_to_page:
            del settings[PATH_KEY]
            self._navigate_to_add_form()
        else:
            self.navigate_to(*LIST_PAGE_PATH)
            self.click_button(ADD_NEW_BUTTON, 'don\'t wait')

        self._get_add_edit_controller().set(settings)
        self._click_ok_button(*ADD_OK_BUTTONS[navigate_to_page and navigate_to_list])
        time.sleep(1)

    @go_to_page(LIST_PAGE_PATH)
    def my_favorites_edit(self, name, values):
        """ Edit existing favorited page.

        *Parameters:*
        - `name`: String name of existing favorited page.
        - `values`: dictionary describing changes to the favorited page. Valid
          items are:
          | `New Name` | Optional. New display name to give to the favorite. |
          | `Path` | Optional. List with the new menu path to change the page
          favorited. Also it could be string in form 'Menu Name -> Menu Item Name'. |
          | `Description` | Optional. String with new description for the
          favotied page. |

        *Exceptions:*
        - `ValueError`: Raised if given page is not exist.

        *Examples:*
        | ${path}= | Create List | Mail Policies | HAT Overview |
        | ${page_settings}= | Create Dictionary | New Name | HAT Page |
        | ... | Path | ${path} | Description | New Description |
        | My Favorites Edit | Listeners Page | ${page_settings} |

        | ${page_settings}= | Create Dictionary | New Name | HAT Page |
        | ... | Path | Mail Policies -> HAT Overview |
        | ... | Description | New Description |
        | My Favorites Edit | Listeners Page | ${page_settings} |
        """

        self.mouse_over(FAVORITES_TITLE)
        if PATH_KEY in values:
            values[PATH_KEY] = self._normalize_path(values[PATH_KEY])
        if not self._is_element_present(EDIT_LINK(name)):
            raise ValueError('Page you want to edit is not exist.')
        self.click_link(EDIT_LINK(name))
        self._get_add_edit_controller().set(values)
        self._click_ok_button(EDIT_OK_BUTTON, True)
        time.sleep(1)

    @go_to_page(LIST_PAGE_PATH)
    def my_favorites_delete(self, *args):
        """ Delete favorited pages.

        *Parameters:*
        - `args`: unlimited amount of positional arguments. Each argument
          should be the name of favorited page to delete. If no arguments
          passed all favorited pages will be deleted.

        *Examples:*
        | My Favorites Delete | Listeners Page | HAT Page |
        """
        self.mouse_over(FAVORITES_TITLE)
        if args:
            for name in args:
                self.click_element(DELETE_CHECKBOX(name), 'don\'t wait')
        else:
            self.click_element(DELETE_ALL_CHECKBOX, 'don\'t wait')
        self.click_button(DELETE_BUTTON, 'don\'t wait')
        tmr = CountDownTimer(20).start()
        while tmr.is_active():
            if self._is_element_present(DELETE_CONFIRM_DIALOG_VISIBLE):
                break
            time.sleep(1)
        else:
            raise ConfigError('Failed to confirm deletion.')
        self.click_button(CONFIRM_DELETE_BUTTON, 'don\'t wait')
        self.mouse_over(FAVORITES_TITLE)

    def my_favorites_go_to(self, name):
        """ Navigate to favorited page via My Favorites menu.

        *Parameters:*
        - `name`: name of favorite to navigate to.

        *Examples:*
        | My Favorites Go To | Listeners Page |
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
        | My Favorites Drag | Listeners Page | HAT Page |
        """
        self.drag_and_drop(DRAG_ELEMENT(source),
                           DRAG_ELEMENT(destination))

    @go_to_page(LIST_PAGE_PATH)
    def my_favorites_get_list(self):
        """ Get all favorited pages names.

        *Return:*
        List of favorited pages names.

        *Examples:*
        | ${pages} | My Favorites Get List |
        """

        self.mouse_over(FAVORITES_TITLE)
        count = int(self.get_matching_xpath_count(ALL_FAVORITES))
        xpaths = map(NAME_BY_IDX, xrange(1, count + 1))
        return map(self.get_text, xpaths)


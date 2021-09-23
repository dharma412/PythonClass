#!/usr/bin/env python -tt
# $

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon

from filehash_lists_def.filehash_lists_settings import FileHashListSettings


ADD_HASH_LIST_BUTTON = "//input[@value='Add File Hash List...']"
CONTAINER = "//table[@class='cols']"
EDIT_HASH_LIST_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                    (CONTAINER, name)
DELETE_ALL_HASH_LISTS_CHECKBOX = "//input[@id='checkbox_all']"

DELETE_HASH_LIST_CHECKBOX = lambda name:"//*[@id='%s']" %(name)

DELETE_BUTTON = "//input[@value='Delete']"

PAGE_PATH = ('Mail Policies', 'File Hash Lists')

class FileHashLists(GuiCommon):
    """Keywords for interaction with ESA GUI Mail Policies->
    File Hash Lists page
    """

    def get_keyword_names(self):
        return ['filehash_lists_add',
                'filehash_lists_edit',
                'filehash_lists_delete']

    def _get_settings_controller(self):
        if not hasattr(self, '_settings_controller'):
            self._settings_controller = FileHashListSettings(self)
        return self._settings_controller

    @go_to_page(PAGE_PATH)
    def filehash_lists_add(self, name, settings):
        """Add new filehash list

        *Parameters:*
        - `name`: filehash list name, mandatory
        - `settings`: new address list settings. Dictionary
        which items can be
        | `Description` | description of newly added list |
        | `File Hash Type` | Either MD5 or SHA256 |
        | `File Hash ` | File hashes |

        *Examples:*
        | ${list1_settings}= | Create Dictionary |
        | ... | Description | ${FILEHASHLIST1_NAME} description |
        | ... | File Hash Type | MD5 |
        | ... | File Hash | f056974ca851fd9814b3cc8609d3f79d1c67ed7f9daa9fccad09e1b3e77c9103, c92dc22060d9bc0e507cbaf919212b9c37871de56e9e13d2908bbedf0faf0ca1 |
        | FileHash Lists Add | ${FILEHASHLIST1_NAME} | ${list1_settings} |
        """
        self.click_button(ADD_HASH_LIST_BUTTON)
        controller = self._get_settings_controller()
        settings.update({'Name': name})
        controller.set(settings)
        self._click_submit_button(skip_wait_for_title=True)

    @go_to_page(PAGE_PATH)
    def filehash_lists_edit(self, name, settings={}):
        """Edit filehash list settings

        *Parameters:*
        - `name`: existing filehash list name, mandatory
        - `settings`: new filehash list settings. Dictionary
        which items can be
        | `Description` | description of newly added list |
        | `File Hash Type` | Either MD5 or SHA256 |
        | `File Hash ` | File hashes |

        *Exceptions:*
        - `ValueError`: if address list with given name is not found

        *Examples:*
        | ${list1_settings}= | Create Dictionary |
        | ... | Description | ${FILEHASHLIST1_NAME} description |
        | ... | File Hash Type | MD5 |
        | ... | File Hash | f056974ca851fd9814b3cc8609d3f79d1c67ed7f9daa9fccad09e1b3e77c9103, c92dc22060d9bc0e507cbaf919212b9c37871de56e9e13d2908bbedf0faf0ca1 |
        | FileHash Lists Add | ${FILEHASHLIST1_NAME} | ${list1_settings} |
        | Set To Dictionary | ${list1_settings} | File Hash | f056974ca851fd9814b3cc8609d3f79d1c67ed7f9daa9fccad09e1b3e77c9103 |
        | FileHash Lists Edit | ${FILEHASHLIST1_NAME} | ${list1_settings} |
        """
        if not self._is_element_present(EDIT_HASH_LIST_LINK(name)):
            raise ValueError('There is no filehash List named %s' % \
                             (name,))
        self.click_button(EDIT_HASH_LIST_LINK(name))
        controller = self._get_settings_controller()
        controller.set(settings)
        self._click_submit_button(skip_wait_for_title=True)

    @go_to_page(PAGE_PATH)
    def filehash_lists_delete(self, name):
        """Delete existing filehash list

        *Parameters:*
        - `name`: existing filehash list name or 'all' to delete all
        existing lists, mandatory

        *Exceptions:*
        - `ValueError`: if filehash list with given name is not found

        *Examples:*
        | FileHash Lists Delete | ${FILEHASHLIST1_NAME} |
        | FileHash Lists Delete | All |
        """
        if name.lower() == 'all':
            dest_locator = DELETE_ALL_HASH_LISTS_CHECKBOX
        else:
            dest_locator = DELETE_HASH_LIST_CHECKBOX(name)
        if not self._is_element_present(dest_locator):
            raise ValueError('There is no Filehash List that satisfies '\
                             '"%s" selector' % (name,))
        self._select_checkbox(dest_locator)
        self.click_button(DELETE_BUTTON, 'don\'t wait')
        self._click_continue_button()

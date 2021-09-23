# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm80/cm80_edit_policy_order.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

EDIT_POLICY_ORDER_BUTTON = 'xpath=//input[@value="Edit Policy Order..."]'
DISABLED_EDIT_POLICY_ORDER_BUTTON = \
    'xpath=//input[@value="Edit Policy Order..." and contains(@class, "disabled")]'
TABLE = "xpath=//table/tbody[contains(@class, 'yui-dt-data')]"
DRAG_ELEMENT = lambda name: "%s//tr/td[normalize-space(div)='%s']" % (TABLE, name)


class Cm80EditPolicyOrder(GuiCommon):
    """ Keywords for CM80 Edit Policy Order page where policies
    can be ordered by drag-and-drop.
    """

    def get_keyword_names(self):
        return [
            'cm80_edit_policy_order',
        ]

    def _open_policy_page(self, policy):
        """Go to specific Policies page."""
        self._navigate_to('Web', 'Configuration Master 8.0', policy)

    def _click_edit_policy_order_button(self):
        """Checking if 'Edit Policy Order' button is enabled and
        clicking on it.
        """
        if self._is_element_present(DISABLED_EDIT_POLICY_ORDER_BUTTON):
            raise guiexceptions.GuiError(
                'Edit Policy Order button is disabled.')
        self.click_button(EDIT_POLICY_ORDER_BUTTON)

    def cm80_edit_policy_order(self, policy, submit, *items):
        """ Change the order of policies by clicking "Edit Policy Order"
        button and reordering items by drag-and-drop.

        *Parameters:*
        - `policy`: name of policy category containing policies that need
        to be reordered. It is string containing name of menu item in CM80 menu.
        Requried.
        - `submit`: boolean parameter - do the submit action after policies
        reorder or not.
        - `items`: a list of item pairs. For each pair the first element
        will be draged and dropped over second one.

        *Return*
            None

        *Exceptions*
            - `GuiError`: in case if 'Edit Policy Order' button is disabled.

        *Examples:*
        | CM80 Edit Policy Order | Identities | ${True} |
        | Policy 1 | Policy 2 |

        | CM80 Edit Policy Order | SOCKS Policies | ${True} |
        | Policy 1 |
        | Policy 2 |
        | Policy 3 |
        | Policy 4 |
        """

        self._open_policy_page(policy)
        self._click_edit_policy_order_button()

        assert len(items) % 2 == 0, 'Items list should contain even nubmer of elements'
        items = list(items)

        while items:
            source = items.pop()
            destination = items.pop()
            self._debug('Dragging item "%s" over item "%s"' % (source, destination))
            self._drag_and_drop_to_object(DRAG_ELEMENT(source),
                                          DRAG_ELEMENT(destination))

        if submit:
            self._click_submit_button()

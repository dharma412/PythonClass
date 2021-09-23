#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/management/administration/system_upgrade_def/upgrade_notification.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs


class NotificationSettings(InputsOwner):
    UPGRADE_NOTIF_CHECKBOX = ('AsyncOS Upgrade Notification',
                              "//input[@id='upgrade_notification']")

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value,
                             self.UPGRADE_NOTIF_CHECKBOX)

    @set_speed(0, 'gui')
    def get(self):
        return self._get_checkboxes(self.UPGRADE_NOTIF_CHECKBOX)


# !!! DOM structure may differ for different browser versions
UPGRADE_BUTTON = "//span[@id='upgrade-button']"
TOOLTIP_ROOT = "//div[@id='tooltip']/parent::div"
VISIBLE_TOOLTIP_ROOT = "//div[normalize-space()='Upgrade Available']/parent::div"
ARROW_DOWN_IMG = "xpath={0}//img[contains(@src, 'arrow_down')]".\
                                            format(VISIBLE_TOOLTIP_ROOT)
CLEAR_CHECKBOX = "xpath={0}//input[@id='ignore_notification']".\
                                            format(VISIBLE_TOOLTIP_ROOT)
CLOSE_BUTTON = "xpath={0}//input[@value='Close']".format(VISIBLE_TOOLTIP_ROOT)

class NotificationBalloon(object):
    def __init__(self, gui_common):
        self.gui = gui_common

    def is_exist(self):
        return self.gui._is_element_present(UPGRADE_BUTTON)

    def get_text(self):
        self.gui.click_element(UPGRADE_BUTTON, 'don\'t wait')
        if self.gui._is_element_present(ARROW_DOWN_IMG):
            self.gui.click_element(ARROW_DOWN_IMG, 'don\'t wait')
        result = self.gui.get_text(VISIBLE_TOOLTIP_ROOT)
        self.gui.click_button(CLOSE_BUTTON, 'don\'t wait')
        return result

    def clear(self):
        self.gui.click_element(UPGRADE_BUTTON, 'don\'t wait')
        if self.gui._is_element_present(ARROW_DOWN_IMG):
            self.gui.click_element(ARROW_DOWN_IMG, 'don\'t wait')
        self.gui._select_checkbox(CLEAR_CHECKBOX)
        self.gui.click_button(CLOSE_BUTTON, 'don\'t wait')

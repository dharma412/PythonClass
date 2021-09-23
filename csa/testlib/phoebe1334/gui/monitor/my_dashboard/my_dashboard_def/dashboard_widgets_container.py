#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/monitor/my_dashboard/my_dashboard_def/dashboard_widgets_container.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $


import functools
import time

from common.gui.guicommon import Wait
from common.gui.decorators import set_speed
from common.gui.guiexceptions import ConfigError
from common.util.sarftime import CountDownTimer

from dashboard_widget import DashboardWidget, ACTION_RESULT_DIV


ADD_WIDGET_BUTTON = lambda container_locator: \
    "%s//div[@title='Add Module']" % (container_locator,)
ADD_MODULE_DIALOG = "//div[@id='add_module_dlg_c' and "\
                    "contains(@style, 'visibility: visible')]"
ADD_MODULE_DIALOG_OK = "%s//button[normalize-space()='OK']" % (ADD_MODULE_DIALOG,)
MODULE_SELECTOR = "%s//select[@id='select_module']" % (ADD_MODULE_DIALOG,)

ADD_MODULE_CONFIRM_DIALOG = "//div[@id='add_module_confirm_dlg_c' and "\
                    "contains(@style, 'visibility: visible')]"
ADD_MODULE_CONFIRM_DIALOG_OK = "%s//button[normalize-space()='OK']" % \
                    (ADD_MODULE_CONFIRM_DIALOG,)
ADD_WIDGET_FROM_CUSTOM_PAGE_BUTTON = lambda caption: \
        "//*[normalize-space()='%s']/following::"\
        "div[contains(@class, 'add-button') and @title='Add to My Dashboard']" % \
        (caption,)


def wait_for_loading(gui):
    tmr = CountDownTimer(15).start()
    while tmr.is_active():
        time.sleep(2)
        if not gui._is_text_present('Loading'):
            return

def wait_until_widgets_are_loaded(func):
    @functools.wraps(func)
    def worker(self, *args, **kwargs):
        wait_for_loading(self.gui)

        return func(self, *args, **kwargs)
    return worker


class DashboardWidgetsContainer(object):
    def __init__(self, gui_common):
        self.gui = gui_common
        self._locator = self._get_locator()

    @classmethod
    def create_instance(cls, gui_common, caption):
        """Use this factory method to create container instances
        """
        # We may also use inspect to extract children,
        # but since we have only 3 classes this approach is OK
        children = (SystemOverviewContainer, GeneralContainer,
                    TimeRangeContainer)
        for child in children:
            if caption == child.get_caption():
                return child(gui_common)
        raise ValueError('Unknown container caption "%s"' % (caption,))

    @classmethod
    def get_caption(cls):
        raise NotImplementedError('Should be implemented in subclasses')

    def _get_locator(self):
        raise NotImplementedError('Should be implemented in subclasses')

    def _get_widgets_locator(self):
        raise NotImplementedError('Should be implemented in subclasses')

    def _get_widget_locator_by_caption(self, widget_caption):
        raise NotImplementedError('Should be implemented in subclasses')

    def _get_widget_locator_by_idx(self, widget_idx):
        return "xpath=(%s)[%d]" % (self._get_widgets_locator(), widget_idx)

    def _get_widget_caption_locator(self, widget_idx):
        """wigdet_idx starts from 1
        """
        return "xpath=(%s)[%d]//span[contains(@class, 'display_name')]" % \
                     (self._get_widgets_locator(), widget_idx)

    @set_speed(0, 'gui')
    @wait_until_widgets_are_loaded
    def get_all_widgets(self):
        widgets = []
        widgets_count = int(self.gui.get_matching_xpath_count(
                                        self._get_widgets_locator()))
        for widget_idx in xrange(1, widgets_count + 1):
            widget_caption = self.gui.get_text(
                                self._get_widget_caption_locator(widget_idx))
            widgets.append(DashboardWidget(self.gui, widget_caption,
                                        self._get_widget_locator_by_idx(widget_idx)))
        return widgets

    @set_speed(0, 'gui')
    @wait_until_widgets_are_loaded
    def is_widget_exist(self, caption):
        self.gui._debug('Checking whether %s widget exists' % \
                        self._get_widget_locator_by_caption(caption))
        return self.gui._is_element_present(self._get_widget_locator_by_caption(caption))

    @set_speed(0, 'gui')
    @wait_until_widgets_are_loaded
    def get_widget(self, caption):
        if not self.is_widget_exist(caption):
            raise ValueError('Widget having caption "%s" does not exist in container'\
                             ' "%s"' % (caption, self.get_caption()))
        return DashboardWidget(self.gui, caption,
                            self._get_widget_locator_by_caption(caption))

    def _add_widget_from_my_dashboard_page(self, caption):
        self.gui.click_button(ADD_WIDGET_BUTTON(self._get_locator()), 'don\'t wait')
        Wait(self.gui._is_element_present, timeout=5,
             msg='Failed to detect report select dialog within given timeout')\
                .wait(ADD_MODULE_DIALOG)
        self.gui.select_from_list(MODULE_SELECTOR, caption)
        self.gui.click_button(ADD_MODULE_DIALOG_OK, 'don\'t wait')

    def _add_widget_from_custom_page(self, caption, from_page):
        self.gui.navigate_to('Monitor', from_page)
        wait_for_loading(self.gui)
        self.gui.click_button(ADD_WIDGET_FROM_CUSTOM_PAGE_BUTTON(caption),
                              'don\'t wait')
        Wait(self.gui._is_element_present, timeout=5,
             msg='Failed to detect confirmation dialog within given timeout')\
                .wait(ADD_MODULE_CONFIRM_DIALOG)
        self.gui.click_button(ADD_MODULE_CONFIRM_DIALOG_OK, 'don\'t wait')

    @set_speed(0, 'gui')
    @wait_until_widgets_are_loaded
    def add_widget(self, caption, from_page=None):
        if self.is_widget_exist(caption):
            raise ConfigError('Widget "%s" already exists in container "%s"' % \
                              (caption, self.get_caption()))
        if from_page is None:
            self._add_widget_from_my_dashboard_page(caption)
        else:
            self._add_widget_from_custom_page(caption, from_page)
        Wait(self.gui._is_element_present, timeout=10,
             msg='Failed to detect action result after report add action '\
                 'within given timeout').wait(ACTION_RESULT_DIV)
        self.gui._check_action_result()

    @set_speed(0, 'gui')
    @wait_until_widgets_are_loaded
    def delete_widget(self, caption):
        if not self.is_widget_exist(caption):
            raise ValueError('Widget "%s" does not exists in container "%s"' % \
                              (caption, self.get_caption()))
        DashboardWidget(self.gui, caption,
                     self._get_widget_locator_by_caption(caption)).delete()


class SystemOverviewContainer(DashboardWidgetsContainer):
    @classmethod
    def get_caption(cls):
        return 'System Overview'

    def _get_locator(self):
        return "//table[contains(@class, 'dashboard-container') and "\
            ".//span[contains(@class, 'display_name') "\
            "and normalize-space()='%s']]" % (self.get_caption(),)

    def _get_widgets_locator(self):
        return "%s//td[contains(@class, 'dashboard-header') and "\
            "starts-with(@id, 'header_ss')]" % (self._get_locator(),)

    def _get_widget_locator_by_caption(self, widget_caption):
        # In case of XPath 2.0 it's more convenient to use ends-with function here,
        # but since curent Selenium supports v. 1.0 only we have to put this ugly
        # substring workaround
        return "%s//td[contains(@class, 'dashboard-header') and "\
         ".//span[contains(@class, 'display_name') and "\
         "substring(normalize-space(.), string-length()-%d)='%s']]" % \
                (self._get_locator(), len(widget_caption) - 1, widget_caption)


class GeneralContainer(DashboardWidgetsContainer):
    @classmethod
    def get_caption(cls):
        return 'General'

    def _get_locator(self):
        return "//div[@id='standalone-container' and "\
            ".//strong[normalize-space()='%s']]" % (self.get_caption(),)

    def _get_widgets_locator(self):
        return "%s//*[contains(@class, 'report_section standalone') and "\
            "starts-with(@id, 's_')]" % (self._get_locator(),)

    def _get_widget_locator_by_caption(self, widget_caption):
        return "%s//*[contains(@class, 'report_section standalone') and "\
         "starts-with(@id, 's_') and .//span[contains(@class, 'display_name') and "\
         "substring(normalize-space(.), string-length()-%d)='%s']]" % \
                    (self._get_locator(), len(widget_caption) - 1, widget_caption)


class TimeRangeContainer(DashboardWidgetsContainer):
    @classmethod
    def get_caption(cls):
        return 'Time Range'

    def _get_locator(self):
        return "//dl[contains(@class, 'datebox') and "\
            ".//td[contains(normalize-space(.), '%s')]]" % (self.get_caption(),)

    def _get_widgets_locator(self):
        return "%s//div[contains(@class, 'widget-cell') and "\
            ".//span[contains(@class, 'display_name')]]" % (self._get_locator(),)

    def _get_widget_locator_by_caption(self, widget_caption):
        return "%s//div[contains(@class, 'widget-cell') and "\
         ".//span[contains(@class, 'display_name') and "\
         "substring(normalize-space(.), string-length()-%d)='%s']]" % \
                     (self._get_locator(), len(widget_caption) - 1, widget_caption)

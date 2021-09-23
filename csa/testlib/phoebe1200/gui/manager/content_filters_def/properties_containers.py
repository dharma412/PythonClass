#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/manager/content_filters_def/properties_containers.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import functools
import time

import common.gui.guiexceptions as guiexceptions
from common.util.sarftime import CountDownTimer

from content_filter_properties import get_property_class_by_name, ContentFilterProperty

# Common locators
CONTAINER = "//div[@id='rule_dialog']"
CONTAINER_OK = "%s//button[normalize-space()='OK']" % (CONTAINER,)
CONTAINER_CANCEL = "%s//button[normalize-space()='Cancel']" % (CONTAINER,)
PROPERTY_LINK = lambda property_name: \
    "%s//a[text()='%s']" % (CONTAINER, property_name)

# Conditions locators
ADD_CONDITION = "//input[@id='add_condition_button']"
CONDITIONS_LIST = "//dl[@class='box' and .//dt[text()='Conditions']]"
EDIT_CONDITION = lambda condition_name: \
    "%s//a[text()='%s']" % (CONDITIONS_LIST, condition_name)
DELETE_CONDITION = lambda condition_name: \
    "%s//td[.//text()='%s']/following-sibling::td[2]/img" % \
    (CONDITIONS_LIST, condition_name)

# Actions locators
ADD_ACTION = "//input[@id='add_action_button']"
ACTIONS_LIST = "//dl[@class='box' and .//dt[text()='Actions']]"
EDIT_ACTION = lambda action_name: \
    "%s//a[text()='%s']" % (ACTIONS_LIST, action_name)
DELETE_ACTION = lambda action_name: \
    "%s//td[.//text()='%s']/following-sibling::td[2]/img" % \
    (ACTIONS_LIST, action_name)
URL_CATEGORY_ACTION = "//a[contains(@href, 'UrlCategoryAction')]"
URL_CATEGORY_CONDITION = "//*[@id='tab_UrlCategoryCondition']/a"
URL_REPUTATION_ACTION = "//*[@id='tab_UrlReputationAction']/a"
URL_REPUTATION_CONDITION = "//*[@id='tab_UrlReputationCondition']/a"
SMIME_SIGNENCRYPTONDELIVERY = "//*[@id='tab_Smime_Gateway_Deferred_Action']/a"

# this suffix is used in internal class transformations to allow multiple
# properties with same names
PROPNAME_SUFFIX_MAGIC = '~'


class PropertiesContainer(object):
    """Base method for interactions with Actions/Properties
    GUI container dialog
    """

    def __init__(self, gui_common):
        self.gui = gui_common
        self.__properties_cache = {}
        self._available_names = map(lambda x: x.get_name(),
                                    self.get_properties())

    def _get_fixed_prop_name(self, name):
        return name.rstrip(PROPNAME_SUFFIX_MAGIC)

    def _wait_for_element(self, locator, max_wait_time=10):
        """Wait till given element appears on page

        *Parameters:*
        - `locator`: target element locator
        - `max_wait_time`: maximum seconds to wait for

        *Exceptions:*
        - `guiexceptions.TimeoutError`: if target element is not found
        within the acceptable time range
        """
        timer = CountDownTimer(max_wait_time).start()
        while timer.is_active():
            if self.gui._is_element_present(locator):
                return
            time.sleep(1.0)
        raise guiexceptions.TimeoutError('Element with locator "%s" has not been populated' \
                                         ' within %d seconds timeout' % (locator,
                                                                         max_wait_time))

    @classmethod
    def get_properties(cls):
        """Return list of contained properties

        *Return:*
        List of properties. Each property should be subclass of ContentFilterProperty
        """
        raise NotImplementedError('Should be implemented in subclasses')

    def _lookup_cache(self, property_name):
        if property_name in self.__properties_cache.keys():
            prop = self.__properties_cache[property_name]
        else:
            prop_class = get_property_class_by_name(property_name)
            prop = prop_class(self.gui)
            self.__properties_cache[property_name] = prop
        return prop

    def set_property(self, property_name, new_value):
        """Set given property

        *Parameters:*
        - `property_name`: name of a property to be set.
        Its class must be already present in tuple returned by get_properties
        method
        - `new_value`: value to be set to this property.
        Detailed description of value format you'll find in the
        corresponding value's descriptor class

        *Exceptions:*
        - `ValueError`: if incorrect value is given (wrong format or
        incorrect name)
        """
        prop = self._lookup_cache(property_name)
        prop.set(new_value)

    def get_property(self, property_name):
        """Return value of given property

        *Parameters:*
        - `property_name`: name of a property to be get.
        Its class must be already present in tuple returned by get_properties
        method

        *Exceptions:*
        - `ValueError`: if incorrect value is given (wrong format or
        incorrect name)

        *Return:*
        Property value got from Selenium.
        Detailed description of value format you'll find in the
        corresponding value's descriptor class
        """
        prop = self._lookup_cache(property_name)
        return prop.get()

    def _select(self, name):
        """Select appropriate property in parent container

        *Parameters:*
        - `name`: name of a property to be selected.
        Its class must be already present in tuple returned by get_properties
        method

        *Exceptions:*
        - `ValueError`: if incorrect property name is given
        """
        if name not in self._available_names:
            raise ValueError('Property named "%s" has not been found in its' \
                             ' parent container "%s"' % \
                             (name, self.__class__.__name__))
        try:
            self._wait_for_element(CONTAINER, 3)
        except guiexceptions.TimeoutError:
            raise guiexceptions.ConfigError('Unable to select property "%s" because' \
                                            ' its container dialog is not opened' % (name,))
        # Thera is a common Condition and Action called URL CATEGORY/REPUTATION . So to distinguish
        # between them while selecting Action/Condition the below if else condition is added
        if name == "URL Category Action":
            self.gui.click_button(URL_CATEGORY_ACTION, 'don\'t wait')
        elif name == "URL Category Condition":
            self.gui.click_button(URL_CATEGORY_CONDITION, 'don\'t wait')
        elif name == "URL Reputation Action":
            self.gui.click_button(URL_REPUTATION_ACTION, 'don\'t wait')
        elif name == "URL Reputation Condition":
            self.gui.click_button(URL_REPUTATION_CONDITION, 'don\'t wait')
        elif name == "S/MIME Sign/Encrypt on Delivery":
            self.gui.click_button(SMIME_SIGNENCRYPTONDELIVERY, 'don\'t wait')
        else:
            self.gui.click_button(PROPERTY_LINK(name), 'don\'t wait')

    def _accept(self):
        """Accept properties list dialog
        """
        self.gui.click_button(CONTAINER_OK)

    def _reject(self):
        """Reject properties list dialog
        """
        self.gui.click_button(CONTAINER_CANCEL, 'don\'t wait')

    def add(self, name, params):
        """Add new property to filter

        - `name`: name of a property to be added.
        Its class must be already present in tuple returned by get_properties
        method
        - `params`: value to set. Detailed description of value format you'll
        find in the corresponding value's descriptor class
        """
        self._select(name)
        self.set_property(name, params)

    def edit(self, name, params):
        """Edit filter property

        - `name`: name of a property to be edited.
        Its class must be already present in tuple returned by get_properties
        method
        - `params`: value to set. Detailed description of value format you'll
        find in the corresponding value's descriptor class
        """
        self._select(name)
        self.set_property(name, params)

    def get_details(self, name):
        """Return particular property details

        - `name`: name of a property.
        Its class must be already present in tuple returned by get_properties
        method

        *Return*:
        Property details got via Selenium. Detailed description of value format
        you'll find in the corresponding value's descriptor class
        """
        self._select(name)
        info = self.get_property(name)
        return info


def set_speed(speed):
    def wrapper(func):
        @functools.wraps(func)
        def worker(self, *args, **kwargs):
            old = self.gui.set_selenium_speed(speed)
            try:
                result = func(self, *args, **kwargs)
            finally:
                self.gui.set_selenium_speed(old)
            return result

        return worker

    return wrapper


class FilterActions(PropertiesContainer):
    @set_speed(0)
    def add(self, actions):
        for name, params in actions.iteritems():
            action_name = self._get_fixed_prop_name(name)
            self.gui.click_button(ADD_ACTION, 'don\'t wait')
            super(FilterActions, self).add(action_name, params)
            self._accept()
            time.sleep(2)


class FilterConditions(PropertiesContainer):
    @set_speed(0)
    def add(self, conditions):
        for name, params in conditions.iteritems():
            condition_name = self._get_fixed_prop_name(name)
            self.gui.click_button(ADD_CONDITION, 'don\'t wait')
            super(FilterConditions, self).add(condition_name, params)
            self._accept()
            time.sleep(2)

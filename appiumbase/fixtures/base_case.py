import sys
import requests
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
import time
import unittest

from appium.webdriver.common.touch_action import TouchAction

from appiumbase.core import appium_launcher
from appiumbase import config as ab_config
from appiumbase.config import settings
from selenium.common.exceptions import (
    ElementClickInterceptedException as ECI_Exception,
    ElementNotInteractableException as ENI_Exception,
    StaleElementReferenceException,
)
from appiumbase.fixtures import page_utils, page_actions


class BaseCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseCase, self).__init__(*args, **kwargs)
        self.driver = None
        self.dc = {}
        self.__called_setup = False
        self.__called_teardown = False

    def click(self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None, delay=0, scroll=True):
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        original_selector = selector
        original_by = by
        selector, by = self.__recalculate_selector(selector, by)
        if delay and (type(delay) in [int, float]) and delay > 0:
            time.sleep(delay)

        if self.__is_shadow_selector(selector):
            self.__shadow_click(selector)
            return
        element = page_actions.wait_for_element_visible(self.driver, selector, by, timeout=timeout)
        if scroll:
            self.__scroll_to_element(element, selector, by)
        element.click()

    def tap(self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None, delay=0):
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        if delay and (type(delay) in [int, float]) and delay > 0:
            time.sleep(delay)
        element = page_actions.wait_for_element_visible(self.driver, selector, by, timeout=timeout)
        actions = TouchAction(self.driver)
        actions.tap(element).perform()

    def back(self):
        self.driver.back()

    def close(self):
        self.driver.close_app()

    def launch(self):
        self.driver.launch_app()

    def swipe_between_element(self, start_selector, dest_selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None):
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_selector, by = self.__recalculate_selector(start_selector, by)
        dest_selector, by = self.__recalculate_selector(dest_selector, by)
        start_element = page_actions.wait_for_element_visible(self.driver, start_selector, by, timeout=timeout)
        dest_element = page_actions.wait_for_element_visible(self.driver, dest_selector, by, timeout=timeout)
        self.driver.scroll(start_element,dest_element)

    def swipe_to_element(self, selector, by=MobileBy.ACCESSIBILITY_ID, start_x=100, start_y=100, end_x=0, end_y=0, duration=0, count=10, timeout=None):
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        for i in range(count):
            try:
                self.is_element_visible(selector,by)
                break
            except Exception as e:
                self.driver.swipe(start_x, start_y, end_x, end_y, duration)


    def tap_by_coordinates(self, x, y):
        self.__check_scope()
        time.sleep(2)
        actions = TouchAction(self.driver)
        actions.tap(x=x, y=y).perform()

    def double_tap(self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None, delay=0):
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        if delay and (type(delay) in [int, float]) and delay > 0:
            time.sleep(delay)
        element = page_actions.wait_for_element_visible(self.driver, selector, by, timeout=timeout)
        actions = TouchAction(self.driver)
        actions.tap(element, count=2).perform()



    def scroll_to_element(self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None):
        self.scroll_to(selector, by=by, timeout=timeout)



    def scroll_to(self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None):
        """ Fast scroll to destination """
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout
        )
        try:
            self.__scroll_to_element(element, selector, by)
        except (StaleElementReferenceException, ENI_Exception):
            time.sleep(0.12)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout
            )
            self.__scroll_to_element(element, selector, by)



    def __recalculate_selector(self, selector, by, xp_ok=True):
        """Use autodetection to return the correct selector with "by" updated.
        If "xp_ok" is False, don't call convert_css_to_xpath(), which is
        used to make the ":contains()" selector valid outside JS calls."""
        _type = type(selector)  # First make sure the selector is a string
        not_string = False
        if sys.version_info[0] < 3:
            if _type is not str and _type is not unicode:  # noqa: F821
                not_string = True
        else:
            if _type is not str:
                not_string = True
        if not_string:
            msg = "Expecting a selector of type: \"<class 'str'>\" (string)!"
            raise Exception('Invalid selector type: "%s"\n%s' % (_type, msg))
        if page_utils.is_xpath_selector(selector):
            by = MobileBy.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = MobileBy.LINK_TEXT
        if page_utils.is_partial_link_text_selector(selector):
            selector = page_utils.get_partial_link_text_from_selector(selector)
            by = MobileBy.PARTIAL_LINK_TEXT
        if page_utils.is_name_selector(selector):
            name = page_utils.get_name_from_selector(selector)
            selector = '[name="%s"]' % name
            by = MobileBy.CSS_SELECTOR
        if page_utils.is_id_selector(selector):
            by = MobileBy.ID
        return (selector, by)

    def __is_shadow_selector(self, selector):
        self.__fail_if_invalid_shadow_selector_usage(selector)
        if "::shadow " in selector:
            return True
        return False

    def __fail_if_invalid_shadow_selector_usage(self, selector):
        if selector.strip().endswith("::shadow"):
            msg = (
                "A Shadow DOM selector cannot end on a shadow root element!"
                " End the selector with an element inside the shadow root!"
            )
            raise Exception(msg)

    def double_click(self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None):
        from selenium.webdriver.common.action_chains import ActionChains

        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        original_selector = selector
        original_by = by
        selector, by = self.__recalculate_selector(selector, by)
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout=timeout
        )
        # Find the element one more time in case scrolling hid it
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout=timeout
        )
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()

    def go_back(self):
        self.__check_scope()
        self.__last_page_load_url = None
        self.driver.back()

    def scroll_screen(self, start_x=100, start_y=100, end_x=0, end_y=0, duration=0):
        """Swipe from one point to another point, for an optional duration.

                Args:
                    start_x: x-coordinate at which to start
                    start_y: y-coordinate at which to start
                    end_x: x-coordinate at which to stop
                    end_y: y-coordinate at which to stop
                    duration: time to take the swipe, in ms.
        """
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)


    def is_checked(self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None):
        """Determines if a checkbox or a radio button element is checked.
        Returns True if the element is checked.
        Returns False if the element is not checked.
        If the element is not present on the page, raises an exception.
        If the element is not a checkbox or radio, raises an exception."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        kind = self.get_attribute(selector, "type", by=by, timeout=timeout)
        if kind != "checkbox" and kind != "radio":
            raise Exception("Expecting a checkbox or a radio button element!")
        is_checked = self.get_attribute(
            selector, "checked", by=by, timeout=timeout, hard_fail=False
        )
        if is_checked:
            return True
        else:  # (NoneType)
            return False

    def __select_option(
            self,
            dropdown_selector,
            option,
            dropdown_by=MobileBy.ACCESSIBILITY_ID,
            option_by="text",
            timeout=None,
    ):
        """Selects an HTML <select> option by specification.
        Option specifications are by "text", "index", or "value".
        Defaults to "text" if option_by is unspecified or unknown."""
        from selenium.webdriver.support.ui import Select

        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        dropdown_selector, dropdown_by = self.__recalculate_selector(
            dropdown_selector, dropdown_by
        )
        element = self.wait_for_element_present(
            dropdown_selector, by=dropdown_by, timeout=timeout
        )
        try:
            if option_by == "index":
                Select(element).select_by_index(option)
            elif option_by == "value":
                Select(element).select_by_value(option)
            else:
                Select(element).select_by_visible_text(option)
        except (StaleElementReferenceException, ENI_Exception):
            time.sleep(0.14)
            element = self.wait_for_element_present(
                dropdown_selector, by=dropdown_by, timeout=timeout
            )
            if option_by == "index":
                Select(element).select_by_index(option)
            elif option_by == "value":
                Select(element).select_by_value(option)
            else:
                Select(element).select_by_visible_text(option)

    def select_option_by_text(
            self,
            dropdown_selector,
            option,
            dropdown_by=MobileBy.ACCESSIBILITY_ID,
            timeout=None,
    ):
        """Selects an HTML <select> option by option text.
        @Params
        dropdown_selector - the <select> selector.
        option - the text of the option.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__select_option(
            dropdown_selector,
            option,
            dropdown_by=dropdown_by,
            option_by="text",
            timeout=timeout,
        )

    def select_option_by_index(
            self,
            dropdown_selector,
            option,
            dropdown_by=MobileBy.ACCESSIBILITY_ID,
            timeout=None,
    ):
        """Selects an HTML <select> option by option index.
        @Params
        dropdown_selector - the <select> selector.
        option - the index number of the option.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__select_option(
            dropdown_selector,
            option,
            dropdown_by=dropdown_by,
            option_by="index",
            timeout=timeout,
        )

    def select_option_by_value(
            self,
            dropdown_selector,
            option,
            dropdown_by=MobileBy.ACCESSIBILITY_ID,
            timeout=None,
    ):
        """Selects an HTML <select> option by option value.
        @Params
        dropdown_selector - the <select> selector.
        option - the value property of the option.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__select_option(
            dropdown_selector,
            option,
            dropdown_by=dropdown_by,
            option_by="value",
            timeout=timeout,
        )

    def save_screenshot(self, name, folder=None):
        """Saves a screenshot of the current page.
        If no folder is specified, uses the folder where pytest was called.
        The screenshot will be in PNG format."""
        return page_actions.save_screenshot(self.driver, name, folder)

    def sleep(self, seconds):
        self.__check_scope()
        time.sleep(seconds)
        if seconds <= 0.3:
            time.sleep(seconds)
        else:
            start_ms = time.time() * 1000.0
            stop_ms = start_ms + (seconds * 1000.0)
            for x in range(int(seconds * 5)):
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.2)

    def is_selected(self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None):
        """ Same as is_checked() """
        return self.is_checked(selector, by=by, timeout=timeout)

    def check_if_unchecked(self, selector, by=MobileBy.ACCESSIBILITY_ID):
        """ If a checkbox or radio button is not checked, will check it. """
        self.__check_scope()
        selector, by = self.__recalculate_selector(selector, by)
        if not self.is_checked(selector, by=by):
            if self.is_element_visible(selector, by=by):
                self.click(selector, by=by)

    def select_if_unselected(self, selector, by=MobileBy.ACCESSIBILITY_ID):
        """ Same as check_if_unchecked() """
        self.check_if_unchecked(selector, by=by)

    def uncheck_if_checked(self, selector, by=MobileBy.ACCESSIBILITY_ID):
        """ If a checkbox is checked, will uncheck it. """
        self.__check_scope()
        selector, by = self.__recalculate_selector(selector, by)
        if self.is_checked(selector, by=by):
            if self.is_element_visible(selector, by=by):
                self.click(selector, by=by)

    def unselect_if_selected(self, selector, by=MobileBy.ACCESSIBILITY_ID):
        """ Same as uncheck_if_checked() """
        self.uncheck_if_checked(selector, by=by)

    def is_element_visible(self, selector, by=MobileBy.ACCESSIBILITY_ID):
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.is_element_visible(self.driver, selector, by)

    def get_attribute(
            self,
            selector,
            attribute,
            by=MobileBy.ACCESSIBILITY_ID,
            timeout=None,
            hard_fail=True,
    ):
        """ This method uses JavaScript to get the value of an attribute. """
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        time.sleep(0.01)
        element = page_actions.wait_for_element_present(
            self.driver, selector, by, timeout
        )
        try:
            attribute_value = element.get_attribute(attribute)
        except (StaleElementReferenceException, ENI_Exception):
            time.sleep(0.14)
            element = page_actions.wait_for_element_present(
                self.driver, selector, by, timeout
            )
            attribute_value = element.get_attribute(attribute)
        if attribute_value is not None:
            return attribute_value
        else:
            if hard_fail:
                raise Exception(
                    "Element {%s} has no attribute {%s}!"
                    % (selector, attribute)
                )
            else:
                return None

    def __shadow_click(self, selector):
        element = self.__get_shadow_element(selector)
        element.click()

    def __get_shadow_element(self, selector, timeout=None):
        if timeout is None:
            timeout = settings.SMALL_TIMEOUT
        elif timeout == 0:
            timeout = 0.1  # Use for: is_shadow_element_* (* = present/visible)
        self.__fail_if_invalid_shadow_selector_usage(selector)
        if "::shadow " not in selector:
            raise Exception(
                'A Shadow DOM selector must contain at least one "::shadow "!'
            )
        selectors = selector.split("::shadow ")
        element = self.get_element(selectors[0])
        selector_chain = selectors[0]
        for selector_part in selectors[1:]:
            shadow_root = self.execute_script(
                "return arguments[0].shadowRoot", element
            )
            if timeout == 0.1 and not shadow_root:
                raise Exception(
                    "Element {%s} has no shadow root!" % selector_chain
                )
            elif not shadow_root:
                time.sleep(2)  # Wait two seconds for the shadow root to appear
                shadow_root = self.execute_script(
                    "return arguments[0].shadowRoot", element
                )
                if not shadow_root:
                    raise Exception(
                        "Element {%s} has no shadow root!" % selector_chain
                    )
            selector_chain += "::shadow "
            selector_chain += selector_part
            try:
                element = page_actions.wait_for_element_present(
                    shadow_root,
                    selector_part,
                    by=MobileBy.CSS_SELECTOR,
                    timeout=timeout,
                )
            except Exception:
                msg = (
                        "Shadow DOM Element {%s} was not present after %s seconds!"
                        % (selector_chain, timeout)
                )
                page_actions.timeout_exception("NoSuchElementException", msg)
        return element

    def execute_script(self, script, *args, **kwargs):
        self.__check_scope()
        return self.driver.execute_script(script, *args, **kwargs)

    def get_element(self, selector, by=MobileBy.CSS_SELECTOR, timeout=None):
        """Same as wait_for_element_present() - returns the element.
        The element does not need be visible (it may be hidden)."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        return self.wait_for_element_present(selector, by=by, timeout=timeout)

    def wait_for_element_visible(
            self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None
    ):
        """ Same as self.wait_for_element() """
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__wait_for_shadow_element_visible(selector)
        return page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout
        )

    def wait_for_element_present(
            self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None
    ):
        """Waits for an element to appear in the HTML of a page.
        The element does not need be visible (it may be hidden)."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__wait_for_shadow_element_present(selector)
        return page_actions.wait_for_element_present(
            self.driver, selector, by, timeout
        )

    def wait_for_element(self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None):
        """Waits for an element to appear in the HTML of a page.
        The element must be visible (it cannot be hidden)."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__wait_for_shadow_element_visible(selector)
        return page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout
        )

    def __wait_for_shadow_element_present(self, selector):
        element = self.__get_shadow_element(selector)
        return element

    def __wait_for_shadow_element_visible(self, selector):
        element = self.__get_shadow_element(selector)
        if not element.is_displayed():
            msg = "Shadow DOM Element {%s} was not visible!" % selector
            page_actions.timeout_exception("NoSuchElementException", msg)
        return element

    def __get_shadow_text(self, selector):
        element = self.__get_shadow_element(selector)
        return element.text

    def __wait_for_shadow_text_visible(self, text, selector):
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (settings.SMALL_TIMEOUT * 1000.0)
        for x in range(int(settings.SMALL_TIMEOUT * 10)):
            try:
                actual_text = self.__get_shadow_text(selector).strip()
                text = text.strip()
                if text not in actual_text:
                    msg = (
                            "Expected text {%s} in element {%s} was not visible!"
                            % (text, selector)
                    )
                    page_actions.timeout_exception(
                        "ElementNotVisibleException", msg
                    )
                return True
            except Exception:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
        actual_text = self.__get_shadow_text(selector).strip()
        text = text.strip()
        if text not in actual_text:
            msg = "Expected text {%s} in element {%s} was not visible!" % (
                text,
                selector,
            )
            page_actions.timeout_exception("ElementNotVisibleException", msg)
        return True

    def find_elements(self, selector, by=MobileBy.ACCESSIBILITY_ID, limit=0):
        """Returns a list of matching WebElements.
        Elements could be either hidden or visible on the page.
        If "limit" is set and > 0, will only return that many elements."""
        selector, by = self.__recalculate_selector(selector, by)
        time.sleep(0.05)
        elements = self.driver.find_elements(by=by, value=selector)
        if limit and limit > 0 and len(elements) > limit:
            elements = elements[:limit]
        return elements

    def wait_for_element_not_present(
            self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None
    ):
        """Same as self.wait_for_element_absent()
        Waits for an element to no longer appear in the HTML of a page.
        A hidden element still counts as appearing in the page HTML.
        If waiting for elements to be hidden instead of nonexistent,
        use wait_for_element_not_visible() instead.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_element_absent(
            self.driver, selector, by, timeout
        )

    def find_visible_elements(self, selector, by=MobileBy.ACCESSIBILITY_ID, limit=0):
        """Returns a list of matching WebElements that are visible.
        If "limit" is set and > 0, will only return that many elements."""
        selector, by = self.__recalculate_selector(selector, by)
        time.sleep(0.05)
        v_elems = page_actions.find_visible_elements(self.driver, selector, by)
        if limit and limit > 0 and len(v_elems) > limit:
            v_elems = v_elems[:limit]
        return v_elems

    def click_visible_elements(
            self, selector, by=MobileBy.ACCESSIBILITY_ID, limit=0, timeout=None
    ):
        """Finds all matching page elements and clicks visible ones in order.
        If a click reloads or opens a new page, the clicking will stop.
        If no matching elements appear, an Exception will be raised.
        If "limit" is set and > 0, will only click that many elements.
        Also clicks elements that become visible from previous clicks.
        Works best for actions such as clicking all checkboxes on a page.
        Example:  self.click_visible_elements('input[type="checkbox"]')"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_element_present(selector, by=by, timeout=timeout)
        elements = self.find_elements(selector, by=by)
        click_count = 0
        for element in elements:
            if limit and limit > 0 and click_count >= limit:
                return
            try:
                if element.is_displayed():
                    self.__scroll_to_element(element)
                    element.click()
                    click_count += 1

            except ECI_Exception:
                continue  # ElementClickInterceptedException (Overlay likel)
            except (StaleElementReferenceException, ENI_Exception):
                time.sleep(0.12)
                try:
                    if element.is_displayed():
                        self.__scroll_to_element(element)
                        element.click()
                        click_count += 1
                except (StaleElementReferenceException, ENI_Exception):
                    return  # Probably on new page / Elements are all stale

    def assert_true(self, expr, msg=None):
        """Asserts that the expression is True.
        Will raise an exception if the statement if False."""
        self.assertTrue(expr, msg=msg)

    def assert_false(self, expr, msg=None):
        """Asserts that the expression is False.
        Will raise an exception if the statement if True."""
        self.assertFalse(expr, msg=msg)

    def assert_equal(self, first, second, msg=None):
        """Asserts that the two values are equal.
        Will raise an exception if the values are not equal."""
        self.assertEqual(first, second, msg=msg)

    def assert_not_equal(self, first, second, msg=None):
        """Asserts that the two values are not equal.
        Will raise an exception if the values are equal."""
        self.assertNotEqual(first, second, msg=msg)

    def assert_in(self, first, second, msg=None):
        """Asserts that the first string is in the second string.
        Will raise an exception if the first string is not in the second."""
        self.assertIn(first, second, msg=msg)

    def assert_not_in(self, first, second, msg=None):
        """Asserts that the first string is not in the second string.
        Will raise an exception if the first string is in the second string."""
        self.assertNotIn(first, second, msg=msg)

    def assert_raises(self, *args, **kwargs):
        """Asserts that the following block of code raises an exception.
        Will raise an exception if the block of code has no exception.
        Usage Example =>
                # Verify that the expected exception is raised.
                with self.assert_raises(Exception):
                    raise Exception("Expected Exception!")
        """
        return self.assertRaises(*args, **kwargs)

    def click_if_visible(self, selector, by=MobileBy.ACCESSIBILITY_ID):
        """If the page selector exists and is visible, clicks on the element.
        This method only clicks on the first matching element found.
        (Use click_visible_elements() to click all matching elements.)"""
        if self.is_element_visible(selector, by=by):
            self.click(selector, by=by)

    def __check_scope(self):
        if not self.__called_setup:
            self.setup()
        if hasattr(self, "device"):  # self.browser stores the type of browser
            return  # All good: setUp() already initialized variables in "self"
        else:
            from appiumbase.common.exceptions import OutOfScopeException

            message = (
                "\n It looks like you are trying to call a AppiumBase method"
                "\n from outside the scope of your test class's `self` object,"
                "\n which is initialized by calling BaseCase's setUp() method."
                "\n The `self` object is where all test variables are defined."
                "\n If you created a custom setUp() method (that overrided the"
                "\n the default one), make sure to call super().setUp() in it."
                "\n When using page objects, be sure to pass the `self` object"
                "\n from your test class into your page object methods so that"
                "\n they can call BaseCase class methods with all the required"
                "\n variables, which are initialized during the setUp() method"
                "\n that runs automatically before all tests called by pytest."
            )
            raise OutOfScopeException(message)

    def __scroll_to_element(self, element, selector, by):
        pass

    def slow_scroll_to(self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None):
        """ Slow motion scroll to destination """
        self.__check_scope()
        pass

    def slow_scroll_to_element(self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None):
        self.slow_scroll_to(selector, by=by, timeout=timeout)

    def set_text(self, selector, text, by=MobileBy.ACCESSIBILITY_ID, timeout=None):
        """Same as self.js_update_text()
        JavaScript + send_keys are used to update a text field.
        Performs self.set_value() and triggers event listeners.
        If text ends in "\n", set_value() presses RETURN after.
        Works faster than send_keys() alone due to the JS call.
        If not an input or textarea, sets textContent instead."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        element = page_actions.wait_for_element_present(
            self.driver, selector, by, timeout
        )
        element.send_keys(text)

    def update_text(
            self, selector, text, by=MobileBy.ACCESSIBILITY_ID, timeout=None, retry=False
    ):
        """This method updates an element's text field with new text.
        Has multiple parts:
        * Waits for the element to be visible.
        * Waits for the element to be interactive.
        * Clears the text field.
        * Types in the new text.
        * Hits Enter/Submit (if the text ends in "\n").
        @Params
        selector - the selector of the text field
        text - the new text to type into the text field
        by - the type of selector to search by (Default: CSS Selector)
        timeout - how long to wait for the selector to be visible
        retry - if True, use JS if the Selenium text update fails
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            self.__shadow_type(selector, text)
            return
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout
        )
        self.__scroll_to_element(element, selector, by)
        try:
            element.clear()  # May need https://stackoverflow.com/a/50691625
            backspaces = Keys.BACK_SPACE * 42  # Is the answer to everything
            element.send_keys(backspaces)  # In case autocomplete keeps text
        except (StaleElementReferenceException, ENI_Exception):
            time.sleep(0.16)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout
            )
            try:
                element.clear()
            except Exception:
                pass  # Clearing the text field first might not be necessary
        except Exception:
            pass  # Clearing the text field first might not be necessary
        if type(text) is int or type(text) is float:
            text = str(text)
        try:
            if not text.endswith("\n"):
                element.send_keys(text)
            else:
                element.send_keys(text[:-1])
                element.send_keys(Keys.RETURN)
        except (StaleElementReferenceException, ENI_Exception):
            time.sleep(0.16)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout
            )
            element.clear()
            if not text.endswith("\n"):
                element.send_keys(text)
            else:
                element.send_keys(text[:-1])
                element.send_keys(Keys.RETURN)
        except Exception:
            raise Exception()
        if self.slow_mode:
            self.__slow_mode_pause_if_active()

    def __slow_mode_pause_if_active(self):
        if self.slow_mode:
            wait_time = settings.DEFAULT_DEMO_MODE_TIMEOUT
            if self.demo_sleep:
                wait_time = float(self.demo_sleep)
            time.sleep(wait_time)

    def __get_test_id(self):
        """ The id used in various places such as the test log path. """
        test_id = "%s.%s.%s" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self._testMethodName,
        )
        if self._sb_test_identifier and len(str(self._sb_test_identifier)) > 6:
            test_id = self._sb_test_identifier
        return test_id

    def set_time_limit(self, time_limit):
        self.__check_scope()
        if time_limit:
            try:
                ab_config.time_limit = float(time_limit)
            except Exception:
                ab_config.time_limit = None
        else:
            ab_config.time_limit = None
        if ab_config.time_limit and ab_config.time_limit > 0:
            ab_config.time_limit_ms = int(ab_config.time_limit * 1000.0)
            self.time_limit = ab_config.time_limit
        else:
            self.time_limit = None
            ab_config.time_limit = None
            ab_config.time_limit_ms = None

    def setup(self):
        if not hasattr(self, "_using_ab_fixture") and self.__called_setup:
            # This test already called setUp()
            return
        self.__called_setup = True
        self.__called_teardown = False
        self.is_pytest = None
        try:
            # This raises an exception if the test is not coming from pytest
            self.is_pytest = ab_config.is_pytest
        except Exception:
            # Not using pytest (probably nosetests)
            self.is_pytest = False
        if self.is_pytest:
            self.remote_address = "http://127.0.0.1:4723/wd/hub"
            self.device = ab_config.device
            self.data = ab_config.data
            self.var1 = ab_config.var1
            self.var2 = ab_config.var2
            self.var3 = ab_config.var3
            self.slow_mode = ab_config.slow_mode
            self.time_limit = ab_config._time_limit
            ab_config.time_limit = ab_config._time_limit
            self.environment = ab_config.environment
            self.env = self.environment  # Add a shortened version
            self.mobile_emulator = ab_config.mobile_emulator
            self.cap_file = ab_config.cap_file
            self.settings_file = ab_config.settings_file
            self._reuse_session = ab_config.reuse_session
            self.browser_stack = ab_config.browser_stack
            self.pytest_html_report = ab_config.pytest_html_report
            if not hasattr(self, "device"):
                raise Exception(
                    'AppiiumBase plugins DID NOT load! * Please REINSTALL!'
                )
            if self.settings_file:
                from appiumbase.core import settings_parser
                settings_parser.set_settings(self.settings_file)

            ab_config.start_time_ms = int(time.time() * 1000.0)

        # Configure the test time limit (if used).
        self.set_time_limit(self.time_limit)

        from appiumbase.core import capabilities_parser

        self.dc = capabilities_parser.get_desired_capabilities(self.cap_file)


        if self.browser_stack:
            self.remote_address = "http://hub-cloud.browserstack.com/wd/hub"

        appium_launcher.start_appium_service()
        self.driver = webdriver.Remote(self.remote_address, self.dc)
        return self.driver

    def app_background(self, time):
        """
        put the app in background with given time(in seconds)
        example : app_background(10)
        """
        self.driver.background_app(time)

    def check_keyboard_shown(self):
        """
        Attempts to detect whether a software keyboard is present
        Returns:
            `True` if keyboard is shown
        """
        return self.driver.is_keyboard_shown()

    def get_location_of_element(self,selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None):
        location={}
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        element = page_actions.wait_for_element_present(
            self.driver, selector, by, timeout
        )
        location = element.location_in_view
        x = location['x']
        y = location['y']

        return x , y

    def scroll_the_screen(self,x,y,a,b,d):
        '''
        Scroll the screen according to cordinates
        :param x: starting point 1
        :param y: starting point 2
        :param a: end point 1
        :param b: end point 2
        :param d: duration
        '''
        self.driver.swipe(x,y,a,b,d)

    def long_press_on_btn(self, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=None, delay=0):
        '''
        self.__check_scope()
        time.sleep(2)
        actions = TouchAction(self.driver)
        actions.long_press(selector)
        '''
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector, by = self.__recalculate_selector(selector, by)
        if delay and (type(delay) in [int, float]) and delay > 0:
            time.sleep(delay)
        element = page_actions.wait_for_element_visible(self.driver, selector, by, timeout=timeout)
        actions = TouchAction(self.driver)
        actions.long_press(element).perform()

    def tearDown(self):
        """
        Be careful if a subclass of BaseCase overrides setUp()
        You'll need to add the following line to the subclass's tearDown():
        super(SubClassOfBaseCase, self).tearDown()
        """
        self.driver.quit()
        #appium_launcher.stop_appium_service()

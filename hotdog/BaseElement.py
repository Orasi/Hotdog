import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from waiting import wait as wait_lib

from hotdog import Conditions as EC2


class BaseElement(WebElement):

    debug = False

    @property
    def driver(self):
        return self._parent

    def find(self, objectName, type=None):
        locators = getattr(self, objectName)
        if len(locators) == 3 and not type:
            type = locators[2]
        element = self.find_element(locators[0], locators[1])
        if type:
            element.__class__ = type
        else:
            element.__class__ = BaseElement
        return element

    def finds(self, objectName, type=None):
        locators = getattr(self, objectName)
        if len(locators) == 3 and not type:
            type = locators[2]
        elements = self.find_elements(locators[0], locators[1], type=type)
        return elements

    def find_element(self, by=By.ID, value=None, type=None):
        element =  super().find_element(by, value)
        if type:
             klass = type
        else:
            klass = BaseElement
        element.search_by = (by, value, self)
        element.__class__ = klass

        if hasattr(self, 'debug'):
            element.debug = self.debug
        return element

    def find_elements(self, by=By.ID, value=None, type=None):
        elements =  super().find_elements(by, value)
        if type:
             klass = type
        else:
            klass = BaseElement

        for element in elements:
            element.__class__ = klass
            element.search_by = (by, value, self)
            if hasattr(self, 'debug'):
                element.debug = self.debug
        return elements

    def reload(self):
        if len(self.search_by) == 3:
            parent = self.search_by[2]
            parent.reload()
            parent.find_element(self.search_by[0], self.search_by[1])
        else:
            self.driver.find_element(self.search_by[0], self.search_by[1])

    def javascript_async(self, script):
        script = script.replace("this", 'arguments[0]')
        self.driver.execute_async_script(script, self)

    def javascript(self, script):
        script = script.replace("this", 'arguments[0]')
        self.driver.execute_script(script, self)

    def highlight(self):
        self.javascript("this.style.border='3px solid yellow'")

    def flash(self):
        self.javascript("this.style.border='3px solid yellow'")
        time.sleep(0.5)
        self.javascript("this.style.border='0px'")
        time.sleep(0.5)
        self.javascript("this.style.border='3px solid yellow'")
        time.sleep(0.5)
        self.javascript("this.style.border='0px'")
        time.sleep(0.5)
        self.javascript("this.style.border='3px solid yellow'")
        time.sleep(0.5)
        self.javascript("this.style.border='0px'")

    def set(self, text):
        if self.debug:
            self.flash()
        super().send_keys(text)

    def clear(self):
        if self.debug:
            self.flash()
        super().clear()

    def send_keys(self, *value):
        self.set(value)

    def click(self):
        if self.debug:
            self.flash()
        super().click()

    def jsClick(self):
        if self.debug:
            self.flash()
        self.javascript('this.click()')

    def focus(self):
        if self.debug:
            self.flash()
        self.javascript('this.focus()')

    def hover(self):
        '''
        Performs Action Chain Hover on element
        :Note: Does not work in Safari Driver
        '''
        #Todo: Add check for Safari driver and throw exception
        if self.debug:
            self.flash()
        hov = ActionChains(self.driver).move_to_element(self)
        hov.perform()

    def scrollIntoView(self):
        self.javascript('this.scrollIntoView()')

    def tap(self):
        location = self.location
        size = self.size
        x_loc = location['x'] + (size['width']/2)
        y_loc = location['y'] + (size['height']/2)
        loc = (x_loc, y_loc)
        self.driver.tap([loc])

    def is_displayed(self, timeout=0):
        self.is_present(timeout=timeout)

    def is_not_displayed(self, timeout=0):
        self.is_not_present(timeout=timeout)

    def is_present(self, timeout=0):
        start = time.time()
        elapsed = 0
        while True:
            try:
                if super().is_displayed():
                    return True
                if elapsed > timeout:
                    return False
            except:
                if elapsed > timeout:
                    return False

    def is_not_present(self, timeout=None):
        start = time.time()
        elapsed = 0
        while True:
            try:
                if not super().is_displayed():
                    return True
                if elapsed > timeout:
                    return False
            except:
                if elapsed > timeout:
                    return False

    def is_element_present(self, element_name, just_in_dom=False, timeout=0):
        def _get_driver():
            driver = getattr(self, 'driver', None)
            if driver:
                return driver
            return self.driver

        _get_driver().implicitly_wait(timeout)
        try:
            def is_displayed():
                element = getattr(self, element_name, None)
                if not element:
                    raise Exception('No element "%s" within container %s' % (element_name, self))
                return element.is_displayed()

            is_displayed() if just_in_dom else self.wait(lambda: is_displayed(), timeout_seconds=timeout)
            return True
        except Exception:
            return False
        except TimeoutError:
            return False

    def wait(self, *args, **kwargs):
        '''
        Wrapping 'wait()' method of 'waiting' library with default parameter values.
        WebDriverException is ignored in the expected exceptions by default.
        '''
        kwargs.setdefault('sleep_seconds', (1, None))
        kwargs.setdefault('expected_exceptions', WebDriverException)
        kwargs.setdefault('timeout_seconds', 30)

        return wait_lib(*args, **kwargs)

    def sync_text_starts_with(self, text, timeout=30, ignore_case=False):
        ''' Waits for text attribute of element to start with provided string
        :param text:   String for matching
        :param timeout:   Allowed Time
        :param ignore_case:   Optional Parameter to ignore case when matching
        '''
        WebDriverWait(self.driver, timeout).until(EC2.wait_for_text_to_start_with(self, text, ignore_case=ignore_case))

    def sync_text_ends_with(self, text, timeout=30, ignore_case=False):
        ''' Waits for text attribute of element to end with provided string
        :param text:   String for matching
        :param timeout:   Allowed Time
        :param ignore_case:  Optional Parameter to ignore case when matching
        '''
        WebDriverWait(self.driver, timeout).until(EC2.wait_for_text_to_end_with(self, text, ignore_case=ignore_case))

    def sync_text_contains(self, text, timeout=30, ignore_case=False):
        ''' Waits for text attribute of element to contain provided string
        :param text:   String for matching
        :param timeout:   Allowed Time
        :param ignore_case:  Optional Parameter to ignore case when matching
        '''
        WebDriverWait(self.driver, timeout).until(EC2.wait_for_text_to_contain(self, text, ignore_case=ignore_case))

    def sync_enabled(self, timeout=30):
        ''' Waits for element to clickable
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(self.search_by))

    def sync_disabled(self, timeout=30):
        ''' Waits for element to not be clickable
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(not EC.element_to_be_clickable(self.search_by))

    def sync_attribute_value(self, attribute, value, timeout=30):
        ''' Waits for element attribute to have value
        :param attribute:  Attribute name to match
        :param value:    Value to match
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(EC2.wait_for_attribute_value(self))

    def sync_not_attribute_value(self, attribute, value, timeout=30):
        ''' Waits for element attribute to have value
        :param attribute:  Attribute name to match
        :param value:    Value to match
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(not EC2.wait_for_attribute_value(self))

    def sync_css_value(self, attribute, value, timeout=30):
        WebDriverWait(self.driver, timeout).until(EC2.wait_for_css_attribute_value(self))

    def sync_not_css_value(self, attribute, value, timeout=30):
        WebDriverWait(self.driver, timeout).until(not EC2.wait_for_css_attribute_value(self))

    #Todo: Add Regex support for all conditions that use text

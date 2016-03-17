import time
from random import randint

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

    def find_random(self, object_name, type=None):
        '''Returns a random collection element.
        :param object_name: the object name
        :return: randomly selected element
        '''
        locators = getattr(self, object_name)
        if len(locators) == 3 and not type:
            type = locators[2]
        elements = self.find_elements(locators[0], locators[1], type=type)
        index = randint(0, len(elements) - 1)
        return elements[index]

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
            element = parent.find_element(self.search_by[0], self.search_by[1])
        else:
            element = self.driver.find_element(self.search_by[0], self.search_by[1])
        return element

    def javascript_async(self, script):
        script = script.replace("this", 'arguments[0]')
        self.driver.execute_async_script(script, self)
        return self

    def javascript(self, script):
        script = script.replace("this", 'arguments[0]')
        self.driver.execute_script(script, self)
        return self

    def highlight(self):
        self.javascript("this.style.border='3px solid yellow'")
        return self

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
        return self

    def set(self, text):
        if self.debug:
            self.flash()
        super().send_keys(text)
        return self

    def clear(self):
        if self.debug:
            self.flash()
        super().clear()
        return self

    def send_keys(self, *value):
        return self.set(value)

    def click(self):
        if self.debug:
            self.flash()
        super().click()
        return self

    def jsClick(self):
        if self.debug:
            self.flash()
        self.javascript('this.click()')
        return self

    def focus(self):
        if self.debug:
            self.flash()
        self.javascript('this.focus()')
        return self

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
        return self

    def scrollIntoView(self):
        self.javascript('this.scrollIntoView()')
        return self

    def scrollIntoViewCenter(self):
        # scrollIntoView scrolls untill object at top of screen
        # the next javascript scrolls down half a page (1/2 the viewport height)
        # scrollTop works differently on chrome & firefox:   http://stackoverflow.com/a/28488360
        # the '||' handles this
        # have not tested on
        self.javascript('this.scrollIntoView()')
        self.javascript('window.scrollTo(0, (document.documentElement.scrollTop || document.body.scrollTop) - window.innerHeight / 2)')


    def tap(self):
        location = self.location
        size = self.size
        x_loc = location['x'] + (size['width']/2)
        y_loc = location['y'] + (size['height']/2)
        loc = (x_loc, y_loc)
        self.driver.tap([loc])
        return self

    def is_displayed(self, timeout=0):
        '''Overrides default implementation of is_displayed to allow an optional timeout
        :param timeout: Allowed Time for element to appear
        :return: Boolean: True if present, False if not
        '''
        return self.is_present(timeout=timeout)

    def is_not_displayed(self, timeout=0):
        ''' Checks if an element is not displayed.
        :param timeout: Allowed Time for an element to disappear
        :return: Boolean: True if not present. False if present
        '''
        return self.is_not_present(timeout=timeout)

    def is_present(self, timeout=0):
        '''Alias for is_displayed
        :param timeout: Allowed Time for element to appear
        :return: Boolean: True if present, False if not
        '''
        start = time.time()
        while True:
            try:
                if super().is_displayed():
                    return True
                if time.time() - start > timeout:
                    return False
            except:
                if time.time() - start > timeout:
                    return False

    def is_not_present(self, timeout=None):
        '''Alias for is_not_displayed
        :param timeout: Allowed Time for element to appear
        :return: Boolean: True if present, False if not
        '''
        start = time.time()
        while True:
            try:
                if not super().is_displayed():
                    return True

                if time.time() - start > timeout:
                    return False

            except:
                if time.time() - start > timeout:
                    return False

    def is_element_present(self, element_name, just_in_dom=False, timeout=0):
        def _get_driver():
            driver = getattr(self, 'driver', None)
            if driver:
                return driver
            return self.driver

        _get_driver().implicitly_wait(timeout)
        try:
            element = getattr(self, element_name, None)
            element = self.find_element(element[0], element[1])

            element.is_displayed(timeout=0) if just_in_dom else element.is_displayed(timeout=timeout)
            return True
        except Exception:
            return False
        except TimeoutError:
            return False

    def wait(self, *args, **kwargs):
        ''' Wrapping 'wait()' method of 'waiting' library with default parameter values.
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
        return self

    def sync_text_ends_with(self, text, timeout=30, ignore_case=False):
        ''' Waits for text attribute of element to end with provided string
        :param text:   String for matching
        :param timeout:   Allowed Time
        :param ignore_case:  Optional Parameter to ignore case when matching
        '''
        WebDriverWait(self.driver, timeout).until(EC2.wait_for_text_to_end_with(self, text, ignore_case=ignore_case))
        return self

    def sync_text_contains(self, text, timeout=30, ignore_case=False):
        ''' Waits for text attribute of element to contain provided string
        :param text:   String for matching
        :param timeout:   Allowed Time
        :param ignore_case:  Optional Parameter to ignore case when matching
        '''
        WebDriverWait(self.driver, timeout).until(EC2.wait_for_text_to_contain(self, text, ignore_case=ignore_case))
        return self

    def sync_enabled(self, timeout=30):
        ''' Waits for element to clickable
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(self.search_by))
        return self

    def sync_disabled(self, timeout=30):
        ''' Waits for element to not be clickable
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(not EC.element_to_be_clickable(self.search_by))
        return self

    def sync_attribute_value(self, attribute, value, timeout=30):
        ''' Waits for element attribute to have value
        :param attribute:  Attribute name to match
        :param value:    Value to match
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(EC2.wait_for_attribute_value(self))
        return self

    def sync_not_attribute_value(self, attribute, value, timeout=30):
        ''' Waits for element attribute to have value
        :param attribute:  Attribute name to match
        :param value:    Value to match
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(not EC2.wait_for_attribute_value(self))
        return self

    def sync_css_value(self, attribute, value, timeout=30):
        '''Waits for element css attribute to match value
        :param attribute:  CSS Attribute name to match
        :param value:    Value to match
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(EC2.wait_for_css_attribute_value(self))
        return self

    def sync_not_css_value(self, attribute, value, timeout=30):
        '''Waits for element css attribute to not match value
        :param attribute:  CSS Attribute name to match
        :param value:    Value to match
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(not EC2.wait_for_css_attribute_value(self))
        return self

    #Todo: Add Regex support for all conditions that use text

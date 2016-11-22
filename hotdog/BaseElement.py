import time
from random import randint

from hotdog.TestStep import TestStep
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.color import Color
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from appium.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from waiting import wait as wait_lib

from hotdog import Conditions as EC2, BaseElements
from hotdog.BaseElements import BaseElements


def element_action(action):

    def wrapper(*args, **kwargs):
        timeout = kwargs.pop('timeout', args[0].driver.default_wait_time)
        start = time.time()
        while True:
            try:
                if args[0].element == []:
                    raise NoSuchElementException('Element [%s] could not be found' % args[0])
                if args[0].element == None:
                    raise NoSuchElementException('Element [%s] could not be found' % args[0])
                result = action(*args, **kwargs)
                if result:
                    return result
                elif time.time() - start > timeout:
                    return result
            except StaleElementReferenceException:
                if time.time() - start > timeout:
                    raise
                try:
                    time.sleep(1)
                    args[0].load()
                except:
                    pass
            except:
                if time.time() - start > timeout:
                    raise
                try:
                    time.sleep(1)
                    args[0].load()
                except:
                    pass

    return wrapper


class BaseElement(WebElement):

    debug = False
    name = None
    value = None
    by = None
    index = None


######################## ELEMENT Properties #################################
    @property
    def driver(self):
        if hasattr(self, '_driver'):
            return self._driver
        else:
            return self.parent.driver

    @property
    @element_action
    def tag_name(self):
        return self.element.tag_name

    @property
    @element_action
    def text(self):
        return self.element.text

    @property
    @element_action
    def location_once_scrolled_into_view(self):
        return self.element.location_once_scrolled_into_view

    @property
    @element_action
    def size(self):
        return self.element.size

    @property
    @element_action
    def location(self):
        return self.element.location

    @property
    @element_action
    def rect(self):
        return self.element.rect

    @property
    @element_action
    @TestStep('Take Screenshot - {args[0].element}')
    def screenshot_as_base64(self):
        return self.element.screenshot_as_base64

    @property
    @element_action
    def screenshot_as_png(self):
        return self.element.screenshot_as_png

    @property
    def parent(self):
        if hasattr(self, '_parent'):
            return self._parent
        else:
            return self.element._parent

    @property
    def id(self):
        return self.element.id

######################## ELEMENT ACTIONS #################################
    @element_action
    def value_of_css_property(self, property_name):
        return self.element.value_of_css_property(property_name)

    @element_action
    def screenshot(self, filename):
        return self.element.screenshot

    @element_action
    def get_attribute(self, name):
        return self.element.get_attribute(name)

    @element_action
    def is_selected(self):
        return self.element.is_selected()

    @element_action
    def is_enabled(self):
        return self.element.is_enabled()

    @TestStep('Element Submitted:  {args[0]}')
    @element_action
    def submit(self):
        self.element.submit()

    @TestStep('Javascript executed:  {args[1]}')
    @element_action
    def javascript_async(self, script):
        script = script.replace("this", 'arguments[0]')
        self.driver.execute_async_script(script, self)
        return self

    @TestStep('Javascript executed:  {args[1]}')
    @element_action
    def javascript(self, script):
        script = script.replace("this", 'arguments[0]')
        value = self.driver.execute_script(script, self)
        return self if value == None else value

    def hex_color_from_css(self, property):
        rgb = self.element.value_of_css_property(property)
        return Color.from_string(rgb).hex

    def rgb_color_from_css(self, property):
        rgb = self.element.value_of_css_property(property)
        return Color.from_string(rgb).rgb

    def rgba_color_from_css(self, property):
        rgb = self.element.value_of_css_property(property)
        return Color.from_string(rgb).rgba

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
        self.clear()
        self.send_keys(text)
        return self

    @TestStep('Clear Text Field: {args[0]}')
    @element_action
    def clear(self):
        if self.debug:
            self.flash()
        self.element.clear()
        return self

    @TestStep('Set Text Value:  {args[0]} to {args[1]}')
    @element_action
    def send_keys(self, value):
        if self.debug:
            self.flash()
        self.element.send_keys(value)
        return self


    @element_action
    @TestStep('Click Element: {args[0]}')
    def click(self):
        if self.debug:
            self.flash()
        self.element.click()
        return self

    @TestStep('JSClick Element: {args[0]}')
    def jsClick(self):
        if self.debug:
            self.flash()
        self.javascript('this.click()')
        return self

    @TestStep('Focus Element: {args[0]}')
    def focus(self):
        if self.debug:
            self.flash()
        self.javascript('this.focus()')
        return self

    @element_action
    @TestStep('Hover Element: {args[0]}')
    def hover(self):
        '''
        Performs Action Chain Hover on element
        :Note: Does not work in Safari Driver
        '''

        if not self.element:
            raise Exception('Element is not loaded')

        #Todo: Add check for Safari driver and throw exception
        if self.debug:
            self.flash()
        hov = ActionChains(self.driver).move_to_element(self.element)
        hov.perform()
        return self

    @TestStep('Scroll Element Into View: {args[0]}')
    def scrollIntoView(self):
        self.javascript('this.scrollIntoView()')
        return self

    @TestStep('Scroll Element To Center: {args[0]}')
    def scroll_element_to_center(self):
        self.driver.execute_script("$('html,body').animate({scrollTop: $(arguments[0]).offset().top - $(window).height() / 2 + $(arguments[0]).height() / 2},'fast');", self)
        return self

    @TestStep('ScrollElement To View Center: {args[0]}')
    def scrollIntoViewCenter(self):
        # scrollIntoView scrolls untill object at top of screen
        # the next javascript scrolls down half a page (1/2 the viewport height)
        # scrollTop works differently on chrome & firefox:   http://stackoverflow.com/a/28488360
        # the '||' handles this
        # have not tested on
        self.javascript('this.scrollIntoView()')
        self.javascript('window.scrollTo(0, (document.documentElement.scrollTop || document.body.scrollTop) - window.innerHeight / 2)')

    @element_action
    @TestStep('Tap Element: {args[0]}')
    def tap(self):
        location = self.element.location
        size = self.element.size
        x_loc = location['x'] + (size['width']/2)
        y_loc = location['y'] + (size['height']/2)
        loc = (x_loc, y_loc)
        self.driver.tap([loc])
        return self

    def is_element_in_viewport(self):
        '''Returns whether the element is within the viewport or not
          :return: Boolean: True if in viewport, False if not
          '''
        return self.driver.execute_script(
            'function isElementInViewPort(el) { '
                'var rect = el.getBoundingClientRect(); '
                'return (rect.bottom >= 0 && rect.right >= 0 && rect.top <= '
                    '(window.innerHeight || document.documentElement.clientHeight) && '
                    'rect.left <= (window.innerWidth || document.documentElement.clientWidth));'
            '}'
            'return isElementInViewPort($(arguments[0])[0])', self)

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
                if self.element.is_displayed():
                    return True
                if time.time() - start > timeout:
                    time.sleep(1)
                    return False
            except:
                if time.time() - start > timeout:
                    return False
                else:
                    time.sleep(1)

    def is_not_present(self, timeout=0):
        '''Alias for is_not_displayed
        :param timeout: Allowed Time for element to disappear
        :return: Boolean: True if present, False if not
        '''
        start = time.time()
        while True:
            try:
                if not self.element.is_displayed():
                    return True

                if time.time() - start > timeout:
                    time.sleep(1)
                    return False

            except:
                return True


######################## Finders #################################
    def load(self):
        if not self.parent == self.driver:
            try: self.parent.load()
            except: pass
        if self.index:
            _element = self.parent.find_elements(self.by, self.value, type=self.type)[self.index]
        else:
            _element =  self.parent.find_element(self.by, self.value, type=self.type)
        try:
            self.element = WebElement(_element.element._parent, _element.element._id, w3c=_element.element._w3c)
        except:
            self.element = None
            raise


    def find(self, objectName, type=None):
        locators = getattr(self, objectName)
        self.driver.implicitly_wait(0)
        if len(locators) == 3 and not type:
            type = locators[2]
        element = self.find_element(locators[0], locators[1], type=type, name=objectName)
        if type:
            element.__class__ = type
        self.driver.implicitly_wait(self.driver.default_wait_time)
        return element

    def finds(self, objectName, type=None):
        locators = getattr(self, objectName)
        self.driver.implicitly_wait(0)
        if len(locators) == 3 and not type:
            type = locators[2]
        elements = self.find_elements(locators[0], locators[1], type=type, name=objectName)
        self.driver.implicitly_wait(self.driver.default_wait_time)
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

    def find_element(self, by=By.ID, value=None, type=None, name=None):

        try:
            element =  self.element.find_element(by, value)
        except:
            if type:
                element = type(self.driver, None, by=by, value=value, name=name, type=type)
            else:
                element = self.driver.DefaultElementType(self.driver, None, by=by, value=value, name=name, type=type)
            element._parent = self


        element.search_by = (by, value, type, self)
        element.by = by
        element.value = value
        element._driver = self.driver

        if name:
            element.name = name
        if type:
            element.__class__ = type

        if hasattr(self, 'debug'):
            element.debug = self.debug
        return element

    def find_elements(self, by=By.ID, value=None, type=None, name=None):

        elements =  self.element.find_elements(by, value)
        for element in elements:
            if type:
                element.__class__ = type
            if hasattr(self, 'debug'):
                element.debug = self.debug

        if len(elements) > 0:
            loaded = True
        else:
            loaded = False

        #Wrap elements in BaseElements
        return BaseElements(elements, self, by, value, loaded=loaded, type=type, name=name)



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


######################## Sync  #################################
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

    def sync_present(self, timeout=30):
        ''' Waits for element to clickable
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(EC2.wait_for_present(self))
        return self

    def sync_not_present(self, timeout=30):
        ''' Waits for element to clickable
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until_not(EC2.wait_for_present(self))
        return self

    def sync_enabled(self, timeout=30):
        ''' Waits for element to clickable
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((self.search_by[0], self.search_by[1])))
        return self

    def sync_disabled(self, timeout=30):
        ''' Waits for element to not be clickable
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until_not(EC.element_to_be_clickable((self.search_by[0], self.search_by[1])))
        return self

    def sync_attribute_value(self, attribute, value, timeout=30):
        ''' Waits for element attribute to have value
        :param attribute:  Attribute name to match
        :param value:    Value to match
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until(EC2.wait_for_attribute_value(self, attribute, value))
        return self

    def sync_not_attribute_value(self, attribute, value, timeout=30):
        ''' Waits for element attribute to have value
        :param attribute:  Attribute name to match
        :param value:    Value to match
        :param timeout:   Allowed Time
        '''
        WebDriverWait(self.driver, timeout).until_not(EC2.wait_for_attribute_value(self, attribute, value))
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


######################## Private Methods #################################
    def __eq__(self, element):
        return self.element.__eq__(element)

    def __ne__(self, element):
        return not self.__eq__(element)

    def _execute(self, command, params=None):
        return self.element._execute(command, params)

    def __hash__(self):
        return self.element.__hash__()

    def _upload(self, filename):
        return self.element._upload(filename)

    def __init__(self,  parent, id_, w3c=False, loaded=True, by=None, value=None, name=None, type=None, finds=False):
        self.name = name
        self.by = by
        self.value = value
        self.type = type
        self._parent = parent

        parent.driver.implicitly_wait(0)
        if id_:
            self.element = WebElement(parent, id_, w3c)
            self.loaded = True
        else:
            if finds:
                self.element = []
            else:
                self.element = None
            self.loaded = False
        parent.driver.implicitly_wait(parent.driver.default_wait_time)

    def __repr__(self):
        if self.name and self.by and self.value:
            return '<{0.__module__}.{0.__name__}.{1} By("{2}", "{3}")>'.format(type(self), self.name, self.by, self.value)
        if self.by and self.value:
            return '<{0.__module__}.{0.__name__} By({1}, {2}>'.format(type(self), self.by, self.value)
        else:
            return '<{0.__module__}.{0.__name__}>'.format(type(self))


    #Todo: Add Regex support for all conditions that use text

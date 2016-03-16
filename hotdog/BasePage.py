from selenium.common.exceptions import WebDriverException

from random import randint
from hotdog import Mustard
from hotdog.BaseDriver import get_driver
from waiting import wait

class HotDogBasePage(object):

    def __new__(cls, *args, **kwargs):
        if 'driver' in kwargs:
            driver = kwargs['driver']
            try:
                platform = driver.desired_capabilities['desired']['platformName'].lower()
            except:
                return super().__new__(cls)
            if hasattr(cls,platform):
                return getattr(cls, platform)(driver=driver)
            else:
                return super().__new__(cls)
        else:
            return super().__new__(cls)

    def find(self, objectName, type=None):
        locators = getattr(self, objectName)
        if len(locators) == 3 and not type:
            type = locators[2]
        element = self.driver.find_element(locators[0], locators[1], type=type)
        return element

    def finds(self, objectName, type=None):
        locators = getattr(self, objectName)
        if len(locators) == 3 and not type:
            type = locators[2]
        element = self.driver.find_elements(locators[0], locators[1], type=type)
        return element

    def find_element(self, *args, **kwargs):
        return self.driver.find_element(*args, **kwargs)

    def find_elements(self, *args, **kwargs):
        return self.driver.find_elements(*args, **kwargs)

    def __init__(self, driver=None, url=None):
        self.driver = driver
        self.url = url

    def uploadScreenshot(self, test, name=None):
        Mustard.UploadScreenshot(self, test, name);

    def reload(self, sync=True):
        self = self.__class__(driver=self._driver, sync=sync)
        return self

    def assert_element_present(self, elementName, timeout=10):
        assert self.is_element_present(elementName, timeout=timeout), 'The element [%s] was not found after [%s] seconds' % (elementName, timeout)

    def tap_on_element(self, element):
        location = element.location
        size = element.size
        x_loc = location['x'] + (size['width']/2)
        y_loc = location['y'] + (size['height']/2)
        loc = (x_loc, y_loc)
        self.driver.tap([loc])

    def back(self):
        self.driver.execute_script("window.history.go(-1)");


    def swipe(self, direction, element=None, duration=None):
        if element:
            location = element.location
            size = element.size
            center_x_loc = location['x'] + (size['width']/2)
            center_y_loc = location['y'] + (size['height']/2)
        else:
            size = self.driver.get_window_size()
            center_x_loc = size['width']/2
            center_y_loc = size['height']/2

        screen = self.driver.get_window_size()

        if direction.lower() == 'left':
                start_x = screen['width'] * 0.9
                end_x = screen['width'] * 0.1
                start_y = center_y_loc
                end_y = center_y_loc

        elif direction.lower() == 'right':
                start_x = screen['width'] * 0.01
                end_x = screen['width'] * 0.9
                start_y = center_y_loc
                end_y = center_y_loc

        elif direction.lower() == 'up':
                start_x = center_x_loc
                end_x = center_x_loc
                start_y = screen['height'] * 0.9
                end_y = screen['height'] * 0.1

        elif direction.lower() == 'down':
                start_x = center_x_loc
                end_x = center_x_loc
                start_y = screen['height'] * 0.1
                end_y = screen['height'] * 0.9
        else:
            raise ValueError('Invalid Direction for swipe. [%s]' % direction)

        self.driver.swipe(start_x, start_y, end_x, end_y, duration=duration)

    def open(self):
        if not self.url:
            raise Exception('Can\'t open page without url')
        self.driver.get(self.url)

    def implicitly_wait(self, *args):
        return self.driver.implicitly_wait(*args)

    def is_element_present(self, element_name, just_in_dom=False, timeout=0):
        def _get_driver():
            driver = getattr(self, 'driver', None)
            if driver:
                return driver
            return get_driver()

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
        """
        Wrapping 'wait()' method of 'waiting' library with default parameter values.
        WebDriverException is ignored in the expected exceptions by default.
        """
        kwargs.setdefault('sleep_seconds', (1, None))
        kwargs.setdefault('expected_exceptions', WebDriverException)
        kwargs.setdefault('timeout_seconds', 30)

        return wait(*args, **kwargs)

    def get_random_element(self, collection):
        '''Returns a random collection element.
        :param collection: The collection to get a random element from.
        :return: A randomly selected element.
        '''
        if isinstance(collection, (list, dict)):

            if len(collection) == 0:
                raise Exception('Collection doesnt have any elements.')

            index = randint(0, len(collection) - 1)
            return collection[index]
        else:
            raise Exception('The passed in argument for get_random_element(self, collection) must be a collection.')

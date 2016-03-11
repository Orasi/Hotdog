from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from hotdog.BaseElement import BaseElement


class BaseWebDriver(WebDriver):

    @property
    def browser(self):
        pass
    def find_element(self, by=By.ID, value=None, type=None):
        element =  super().find_element(by, value)
        if type:
            element.__class__ = type
        else:
            element.__class__ = BaseElement

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

            if hasattr(self, 'debug'):
                element.debug = self.debug
        return elements


def get_driver():
    global _driver_instance
    if not _driver_instance:
        _driver_instance = BaseWebDriver

    return _driver_instance
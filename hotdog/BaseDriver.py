from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from hotdog.BaseElement import BaseElement


class BaseWebDriver(WebDriver):

    def find_element(self, by=By.ID, value=None, type=None):
        element =  super().find_element(by, value)
        if type:
            element.__class__ = type
        else:
            element.__class__ = BaseElement
        return element
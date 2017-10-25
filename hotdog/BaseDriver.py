from selenium.webdriver.common.by import By
from appium.webdriver.webdriver import WebDriver
from hotdog.BaseElements import BaseElements
from hotdog.BaseElement import BaseElement


class BaseWebDriver(WebDriver):

    DefaultElementType = BaseElement
    default_wait_time = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.implicitly_wait(self.default_wait_time)

    @property
    def driver(self):
        return self

    def implicitly_wait(self, time_to_wait):
        pass

    def find_element(self, by=By.ID, value=None, type=None, name=None):
        self.implicitly_wait(0)
        try:
            element =  super().find_element(by, value)
        except:
            if type:
                element = type(self.driver, None, by=by, value=value, name=name, type=type)
            else:
                element = self.driver.DefaultElementType(self.driver, None, by=by, value=value, name=name, type=type)
            element._parent = self.driver

        if type:
            element.__class__ = type

        element.search_by = (by, value, type)
        element.by = by
        element.value = value
        if name:
            element.name = name

        if hasattr(self, 'debug'):
            element.debug = self.debug
        self.implicitly_wait(self.default_wait_time)
        return element

    def find_elements(self, by=By.ID, value=None, type=None, name=None):

        elements =  super().find_elements(by, value)

        for element in elements:
            if type:
                element.__class__ = type
            if hasattr(self, 'debug'):
                element.debug = self.debug

        if len(elements) > 0:
            loaded = True
        else:
            loaded = False

        #Wrap Element Collection with BaseElements
        return BaseElements(elements, self, by, value, type=type, name=name, loaded=loaded)

    def create_web_element(self, element_id):
        return self.DefaultElementType(self, element_id, w3c=self.w3c)

    def get_new_handle(self, existing_handles):
    # IE doesn't guarantee the order of window handles when a new window is opened
    #
    # @param existing_handles The handles before the action of opening a new window
        for handle in super().window_handles:
            if handle not in existing_handles:
                return handle

def get_driver():
    global _driver_instance
    if not _driver_instance:
        _driver_instance = BaseWebDriver

    return _driver_instance
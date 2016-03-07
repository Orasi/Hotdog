import time
from selenium.webdriver.remote.webdriver import WebElement

from hotdog.Retry import Retry


class BaseElement(WebElement):

    debug = False

    @property
    def driver(self):
        return self._parent

    def find(self, objectName, type=None):
        locators = getattr(self, objectName)
        element = self.driver.find_element(locators[0], locators[1])
        if type:
            element.__class__ = type
        else:
            element.__class__ = BaseElement
        return element

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

    def click(self):
        if self.debug:
            self.flash()

        super().click()

    def jsClick(self):
        self.javascript('this.click()')

    def focus(self):
        self.javascript('this.focus()')

    def scrollIntoView(self):
        self.javascript('this.scrollIntoView()')

    def tap(self):
        location = self.location
        size = self.size
        x_loc = location['x'] + (size['width']/2)
        y_loc = location['y'] + (size['height']/2)
        loc = (x_loc, y_loc)
        self.driver.tap([loc])

        #
        # syncPresent
        # syncGone
        #
        # syncVisible
        # sync hidden
        #
        # syncText
        #
        # sync enabled
        # syncDisabled
        #
        # sync attribute contains value
        # sync css property contains value
        #
        # sync attribute matches value
        # sync css property matches value
        #
        # clear
        # set
        #
        # dimensions
        # location
        # tagname
        # class
        # id
        # css_property
        #
        # getLocation
        #     middle
        #     top-left
        #     topright
        #     topmiddle
        #     rightmiddle
        #     leftmiddle
        #     bottommiddle
        #     bottomright
        #     bottomleft

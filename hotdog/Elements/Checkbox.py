from hotdog.BaseElement import BaseElement

class Checkbox(BaseElement):

    def is_checked(self):
        return self.get_attribute('checked')

    def check(self):
        if not self.is_checked():
            self.click()

    def uncheck(self):
        if self.is_checked():
            self.click()

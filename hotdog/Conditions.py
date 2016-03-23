from selenium.common.exceptions import StaleElementReferenceException

class wait_for_present(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        try:
            self.element.load()
            if self.element.element != None:
                return self.element
            return False
        except:
            return False

class wait_for_text_to_start_with(object):
    def __init__(self, element, text, ignore_case=False):
        self.ignore_case = ignore_case
        self.element = element
        self.text = text

    def __call__(self, driver):
        try:
            element_text = self.element.text
            if self.ignore_case:
                element_text = element_text.lower()
                self.text = self.text.lower()
            return element_text.startswith(self.text)
        except:
            return False

class wait_for_text_to_end_with(object):
    def __init__(self, element, text, ignore_case=False):
        self.ignore_case = ignore_case
        self.element = element
        self.text = text

    def __call__(self, driver):
        try:
            element_text = self.element.text
            if self.ignore_case:
                element_text = element_text.lower()
                self.text = self.text.lower()
            return element_text.endswith(self.text)
        except StaleElementReferenceException:
            self.element.reload()
        except:
            return False

class wait_for_text_to_contain(object):
    def __init__(self, element, text, ignore_case=False):
        self.ignore_case = ignore_case
        self.element = element
        self.text = text

    def __call__(self, driver):
        try:
            element_text = self.element.text
            if self.ignore_case:
                element_text = element_text.lower()
                self.text = self.text.lower()
            if self.text in self.element.text:
                return True
            else:
                return False
        except:
            return False

class wait_for_attribute_value(object):
    def __init__(self, element, attribute, value):
        self.element = element
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        try:
            if self.element.get_attribute(self.attribute) == self.value:
                return True
            else:
                return False
        except StaleElementReferenceException:
            self.element.reload()
            return False
        except:
            return False


class wait_for_css_attribute_value(object):
    def __init__(self, element, attribute, value):
        self.element = element
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        try:
            if self.element.value_of_css_property(self.attribute) == self.value:
                return self.element
            else:
                return False
        except:
            return False


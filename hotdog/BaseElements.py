import time
from random import randint

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


def elements_action(action):
    def wrapper(*args, **kwargs):
        args[0].parent.driver.implicitly_wait(0)
        timeout = kwargs.pop('timeout', args[0].parent.driver.default_wait_time)
        not_value = kwargs.pop('not_value', None)
        start = time.time()
        while True:
            try:
                result = action(*args, **kwargs)
                #Do not return if result == not_value
                if not_value and result == not_value:
                    if time.time() - start > timeout:
                        return result

                    try:
                        args[0].load()
                    except:
                        pass
                #Do not return if result == 0 and not_value not defined
                elif result == 0:
                    if time.time() - start > timeout:
                        return result
                    try:
                        args[0].load()
                    except:
                        pass
                else:
                    return result
            except:
                time.sleep(1)
                if time.time() - start > timeout:
                    raise
                try:
                    args[0].load()
                except:
                    pass
    return wrapper

class BaseElements(object):

    @elements_action
    def __iter__(self):
        if len(self.elements) == 0:
            raise NoSuchElementException('Returned zero elements for element [%s]' % self)
        return self.elements.__iter__()

    def next(self, arg):
        return self.elements.next(arg)

    @elements_action
    def __getitem__(self, item):
        element = self.elements.__getitem__(item)
        element.index = item
        return element


    def __len__(self):
        return len(self.elements)

    @elements_action
    def count(self):
        count = len(self)
        return count

    @elements_action
    def random(self):
        index = randint(0, len(self.elements) - 1)
        return self.elements[index]

    def load(self):
        if not self.parent == self.driver:
            try: self.parent.load()
            except: pass
        self.elements =  self.parent.find_elements(self.by, self.value, type=self.type).elements

    def __init__(self, elements,parent, by, value, type=None, name=None, loaded=True):
        self.parent = parent
        self.driver = parent.driver
        self.elements = elements
        self.by = by
        self.value = value
        self.loaded = loaded
        self.type = type
        self.name = name

    def __repr__(self):
        if self.name and self.by and self.value:
            return '<{0.__module__}.{0.__name__}.{1} By("{2}", "{3}")>'.format(type(self), self.name, self.by, self.value)
        if self.by and self.value:
            return '<{0.__module__}.{0.__name__} By({1}, {2}>'.format(type(self), self.by, self.value)
        else:
            return '<{0.__module__}.{0.__name__}>'.format(type(self))
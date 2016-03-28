import time
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


def elements_action(action):
    def wrapper(*args, **kwargs):
        args[0].parent.driver.implicitly_wait(0)
        timeout = kwargs.pop('timeout', args[0].parent.driver.default_wait_time)
        start = time.time()
        while True:
            try:
                result = action(*args, **kwargs)
                return result
            except:
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
        return self.elements.__getitem__(item)

    @elements_action
    def __len__(self):
        return len(self.elements)

    def load(self):
        self.elements =  self.parent.find_elements(self.by, self.value, type=self.type)
        time.sleep(0.5)

    def __init__(self, elements,parent, by, value, type=None, name=None, loaded=True):
        self.parent = parent

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
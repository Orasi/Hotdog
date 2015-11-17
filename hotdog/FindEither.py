from types import MethodType
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from webium import Find, Finds
from webium.base_page import is_element_present, webium
from webium.errors import WebiumException
from time import time

class FindEither(Find):
    selectors = None

    def __init__(self, ui_type=WebElement,
                 selectors=None,
                 context=None,
                 *args,
                 **kwargs):
        self.selectors = selectors
        self.ui_type = ui_type
        self.context = context
        self._target_element = None
        self.init_args = args
        self.init_kwargs = kwargs
        self._validate_params()

    def __getattribute__(self, item):
        if hasattr(FindEither, item):
            return object.__getattribute__(self, item)
        self._search_element()
        return self._target_element.__getattribute__(item)

    def _validate_params(self):
            if not issubclass(self.ui_type, WebElement):
                raise WebiumException('UI types should inherit WebElement')

    def _search_element(self):
        found = False
        startTime = time()
        originalTimeout = webium.settings.implicit_timeout
        webium.settings.implicit_timeout = 0
        notTimeout = True
        while notTimeout:
            for selector in self.selectors:
                self.by = selector[0]
                self.value = selector[1]
                try:

                    if not self.context:
                        raise WebiumException("Search context should be defined with dynamic Find usage." +
                                              " Please define context in __init__.")
                    if (self.by is not None) and (self.value is not None):
                        web_element = self.context.find_element(self.by, self.value)
                        web_element.__class__ = self.ui_type
                        self._target_element = web_element
                        found = True
                    else:
                        container = self.ui_type()
                        container.find_element = self.context.find_element
                        container.find_elements = self.context.find_elements
                        self._target_element = container
                        found = True
                    self._target_element.is_element_present = MethodType(is_element_present, self._target_element)
                    self._target_element.implicitly_wait = self.context.implicitly_wait
                    if len(self.init_args) or len(self.init_kwargs) > 0:
                        self._target_element.__init__(*self.init_args, **self.init_kwargs)
                    webium.settings.implicit_timeout = originalTimeout
                    return
                except NoSuchElementException:
                    pass
                except WebDriverException:
                    pass
                except:
                    raise

            if time() - startTime > originalTimeout:
                notTimeout = False
            raise NoSuchElementException(msg='Could not find element with identifiers [%s]' % self.selectors)

def FindsEither(ui_type=WebElement, selectors=None, context=None):
    startTime = time()
    originalTimeout = webium.settings.implicit_timeout
    webium.settings.implicit_timeout = 0
    notTimeout = True
    while notTimeout:
        for ident in selectors:
            try:
                itemsFound = Finds(ui_type=ui_type, by=ident[0], value=ident[1], context=context)
                itemsFound._search_element()
                if len(itemsFound._target_element) != 0:
                    return itemsFound._target_element
            except:
                pass
        if time() - startTime > originalTimeout:
                notTimeout = False
# class FindsEither(FindEither):
#
#     def _search_element(self):
#         found = False
#         for selector in self.selectors:
#             self.by = selector[0]
#             self.value = selector[1]
#             try:
#                 self.context.implicitly_wait(0)
#                 self._target_element = self.context.find_elements(self.by, self.value)
#                 self.context.implicitly_wait(webium.settings.implicit_timeout)
#                 for item in self._target_element:
#                     item.__class__ = self.ui_type
#                     item.is_element_present = MethodType(is_element_present, item)
#                     item.implicitly_wait = self.context.implicitly_wait
#                 return
#             except:
#                 pass
#         raise WebDriverException(msg='Could not find element with identifiers [%s]' % self.selectors)

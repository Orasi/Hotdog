import os

import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import by

from hotdog.FilePath import get_full_path

os.environ['PROJECTFOLDER'] = get_full_path('') + 'test'
from hotdog.BasePage import HotDogBasePage
from selenium.webdriver.common.by import By
from hotdog.BaseTest import HotDogBaseTest
from hotdog.BaseElement import BaseElement


class TestElement(BaseElement):
    pass


class TestContainer(BaseElement):
    testElement = (By.TAG_NAME, 'input')
    typedTestElement = (By.TAG_NAME, 'input', TestElement)
    notPresent = (By.ID, 'appear')
    notPresentTyped = (By.ID, 'appear', TestElement)


class TestPage(HotDogBasePage):
    testElement = (By.TAG_NAME, 'input')
    typedTestElement = (By.TAG_NAME, 'input', TestElement)
    notPresent = (By.ID, 'appear')
    notPresentTyped = (By.ID, 'appear', TestElement)
    containerLoc = (By.ID, 'checkboxes', TestContainer)

    @property
    def container(self):
        cont =  self.find('containerLoc')
        return cont


class GetElementTests(HotDogBaseTest):

    def test_getsBaseDriver(self):
        assert self.driver.__class__.__name__ == 'BaseWebDriver'

    def test_getsBaseElement(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        element =  self.driver.find_element(by=By.TAG_NAME, value='input')
        assert element.__class__.__name__ == 'BaseElement'
        assert element.element.__class__.__name__ == 'WebElement'

    def test_getsBaseElements(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        elements =  self.driver.find_elements(by=By.TAG_NAME, value='input')
        assert elements.__class__.__name__ == 'BaseElements'
        for element in elements:
            assert element.__class__.__name__ == 'BaseElement'
            assert element.element.__class__.__name__ == 'WebElement'
        assert len(elements) > 0

    def test_getsElementThroughPage(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.find('testElement')
        assert element.__class__.__name__ == 'BaseElement'
        assert element.element.__class__.__name__ == 'WebElement'

    def test_getsElementsThroughPage(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.finds('testElement')
        assert elements.__class__.__name__ == 'BaseElements'
        for element in elements:
              assert element.__class__.__name__ == 'BaseElement'
              assert element.element.__class__.__name__ == 'WebElement'
        assert len(elements) > 0

    def test_getsTypedElementThroughPage(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element =  test.find('typedTestElement')
        assert element.__class__.__name__ == 'TestElement'
        assert element.element.__class__.__name__ == 'WebElement', 'expected WebElement got %s' % element.element.__class__.__name__

    def test_getsTypedElementsThroughPage(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.finds('typedTestElement')
        assert elements.__class__.__name__ == 'BaseElements'
        for element in elements:
              assert element.__class__.__name__ == 'TestElement'
              assert element.element.__class__.__name__ == 'WebElement'
        assert len(elements) > 0

    def test_getsTypedElementThroughPageOverride(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element =  test.find('typedTestElement', type=BaseElement)
        assert element.__class__.__name__ == 'BaseElement'
        assert element.element.__class__.__name__ == 'WebElement'

    def test_getsTypedElementsThroughPageOverride(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.finds('typedTestElement', type=BaseElement)
        assert elements.__class__.__name__ == 'BaseElements'
        for element in elements:
              assert element.__class__.__name__ == 'BaseElement'
              assert element.element.__class__.__name__ == 'WebElement'
        assert len(elements) > 0

    def test_getsElementThroughPageContainer(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.container.find('testElement')
        assert element.__class__.__name__ == 'BaseElement'
        assert element.element.__class__.__name__ == 'WebElement'

    def test_getsElementsThroughPageContainer(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.container.finds('testElement')
        assert elements.__class__.__name__ == 'BaseElements'
        for element in elements:
              assert element.__class__.__name__ == 'BaseElement'
              assert element.element.__class__.__name__ == 'WebElement'
        assert len(elements) > 0

    def test_getsTypedElementThroughPageContainer(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.container.find('typedTestElement')
        assert element.__class__.__name__ == 'TestElement'
        assert element.element.__class__.__name__ == 'WebElement'

    def test_getsTypedElementsThroughPageContainer(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.container.finds('typedTestElement')
        assert elements.__class__.__name__ == 'BaseElements'
        for element in test.container.finds('typedTestElement'):
              assert element.__class__.__name__ == 'TestElement'
              assert element.element.__class__.__name__ == 'WebElement'
        assert len(elements) > 0


    def test_getsTypedElementThroughPageContainerThroughFind(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.container.find('testElement', type=TestElement)
        assert element.__class__.__name__ == 'TestElement'
        assert element.element.__class__.__name__ == 'WebElement'

    def test_getsTypedElementsThroughPageContainerThroughFinds(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.container.finds('testElement', type=TestElement)
        assert elements.__class__.__name__ == 'BaseElements'
        for element in test.container.finds('typedTestElement'):
              assert element.__class__.__name__ == 'TestElement'
              assert element.element.__class__.__name__ == 'WebElement'
        assert len(elements) > 0

    def test_getsTypedElementThroughPageContainerOverride(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.container.find('typedTestElement', type=BaseElement)
        assert element.__class__.__name__ == 'BaseElement'
        assert element.element.__class__.__name__ == 'WebElement'

    def test_getsTypedElementsThroughPageContainerOverride(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.container.finds('typedTestElement', type=BaseElement)
        assert elements.__class__.__name__ == 'BaseElements'
        for element in elements:
              assert element.__class__.__name__ == 'BaseElement'
              assert element.element.__class__.__name__ == 'WebElement'
        assert len(elements) > 0

    def test_elementNotWired(self):
        self.driver.get('http://orasi.github.io/Selenium-Java-Core/sites/unitTests/orasi/core/interfaces/element.html')
        test = TestPage(driver=self.driver)
        appear = test.find_element(by=By.ID, value='appear')
        assert appear.element == None

    def test_elementNotWiredFind(self):
        self.driver.get('http://orasi.github.io/Selenium-Java-Core/sites/unitTests/orasi/core/interfaces/element.html')
        test = TestPage(driver=self.driver)
        appear = test.find('notPresent')
        assert appear.element == None

    def test_elementNotWiredFindTyped(self):
        self.driver.get('http://orasi.github.io/Selenium-Java-Core/sites/unitTests/orasi/core/interfaces/element.html')
        test = TestPage(driver=self.driver)
        appear = test.find('notPresentTyped')
        assert appear.element == None

    def test_elementNotWiredContainerFind(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        appear = test.container.find('notPresent')
        assert appear.element == None

    def test_elementNotWiredContainerFindTyped(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        cont = test.container
        appear = cont.find('notPresentTyped')
        assert appear.element == None

    def test_elementAction(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.find('testElement')
        element.click(timeout=3)

    def test_elementActionSync(self):
        self.driver.get('http://orasi.github.io/Selenium-Java-Core/sites/unitTests/orasi/core/interfaces/element.html')
        test = TestPage(driver=self.driver)
        element = test.find('notPresent')
        element.click(timeout=6)

    def test_elementActionNotPresent(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.find('notPresent')
        with self.assertRaises(NoSuchElementException):
             element.click(timeout=1)

    def test_elementsAction(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.finds('testElement')
        for e in element:
            e.click()


    def test_elementsActionSync(self):
        self.driver.get('http://orasi.github.io/Selenium-Java-Core/sites/unitTests/orasi/core/interfaces/element.html')
        test = TestPage(driver=self.driver)
        element = test.finds('notPresent')
        for e in element:
            e.click()

    def test_elementsActionNotPresentt(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.finds('notPresent')
        with self.assertRaises(NoSuchElementException):
            for e in element:
                e.click()

    def test_elementActionsReload(self):
        self.driver.get('http://orasi.github.io/Selenium-Java-Core/sites/unitTests/orasi/core/interfaces/element.html')
        test = TestPage(driver=self.driver)
        element = test.find('notPresentTyped')
        element.click(timeout=10)
        assert element.__class__.__name__ == 'TestElement', 'should be "TestElement" actually %s' % element.__class__.__name__
        assert element.element.__class__.__name__ == 'WebElement', 'should be "WebElement" actually %s' % element.__class__.__name__

    def test_elementsActionsReload(self):
        self.driver.get('http://orasi.github.io/Selenium-Java-Core/sites/unitTests/orasi/core/interfaces/element.html')
        test = TestPage(driver=self.driver)
        elements = test.finds('notPresentTyped')
        len(elements)
        assert elements.__class__.__name__ == 'BaseElements'
        for element in elements:
            assert element.__class__.__name__ == 'TestElement',  'should be "TestElement" actually %s' % element.__class__.__name__
            assert element.element.__class__.__name__ == 'WebElement'
            element.click()

    def test_getRandomElement(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.find_random('typedTestElement')
        assert element.__class__.__name__ == 'TestElement'
        assert element.element.__class__.__name__ == 'WebElement'

    def test_getRandomElementOverride(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.find_random('typedTestElement', BaseElement)
        assert element.__class__.__name__ == 'BaseElement'
        assert element.element.__class__.__name__ == 'WebElement'

    def test_getRandomElementContainer(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.container.find_random('typedTestElement')
        assert element.__class__.__name__ == 'TestElement'
        assert element.element.__class__.__name__ == 'WebElement'

    def test_getRandomElementContainerOverride(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.container.find_random('typedTestElement', BaseElement)
        assert element.__class__.__name__ == 'BaseElement'
        assert element.element.__class__.__name__ == 'WebElement'

    def test_randomElementAction(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        element = test.find_random('testElement')
        element.click(timeout=3)

    def test_randomElementActionSync(self):
        self.driver.get('http://orasi.github.io/Selenium-Java-Core/sites/unitTests/orasi/core/interfaces/element.html')
        test = TestPage(driver=self.driver)
        element = test.find_random('notPresent')
        element.click(timeout=6)

    def test_randomElementActionNotPresent(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        with self.assertRaises(NoSuchElementException):
             element = test.find_random('notPresent', timeout=2)
             element.click(timeout=1)

    def test_getElementText(self):
        self.driver.get('http://orasi.github.io/Selenium-Java-Core/sites/unitTests/orasi/core/interfaces/element.html')
        test = TestPage(driver=self.driver)
        element = test.find('notPresent')
        assert element.text == '', '[%s]' % element.text

    def test_getElementsCount(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        elements =  self.driver.find_elements(by=By.TAG_NAME, value='input')
        assert elements.count(timeout=5) == 2

    def test_getElementsCountNotValue(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        elements =  self.driver.find_elements(by=By.TAG_NAME, value='input')
        start_time=  time.time()
        assert elements.count(timeout=5, not_value=2) == 2
        assert time.time() - start_time >= 5

    def test_getElementsCountNotPresent(self):
        self.driver.get('http://orasi.github.io/Selenium-Java-Core/sites/unitTests/orasi/core/interfaces/element.html')
        test = TestPage(driver=self.driver)
        elements = test.finds('notPresent')
        assert elements.count(timeout=10) == 1


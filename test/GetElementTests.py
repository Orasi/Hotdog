import os
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


class TestPage(HotDogBasePage):
    testElement = (By.TAG_NAME, 'input')
    typedTestElement = (By.TAG_NAME, 'input', TestElement)
    containerLoc = (By.ID, 'checkboxes', TestContainer)

    @property
    def container(self):
        return self.find('containerLoc')


class GetElementTests(HotDogBaseTest):

    def test_getsBaseDriver(self):
        assert self.driver.__class__.__name__ == 'BaseWebDriver'

    def test_getsBaseElement(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        assert self.driver.find_element(by=By.TAG_NAME, value='input').__class__.__name__ == 'BaseElement'

    def test_getsBaseElements(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        elements =  self.driver.find_elements(by=By.TAG_NAME, value='input')
        for element in elements:
            assert element.__class__.__name__ == 'BaseElement'
        assert len(elements) > 0

    def test_getsElementThroughPage(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        assert test.find('testElement').__class__.__name__ == 'BaseElement'

    def test_getsElementsThroughPage(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.finds('testElement')
        for element in elements:
              assert element.__class__.__name__ == 'BaseElement'
        assert len(elements) > 0

    def test_getsTypedElementThroughPage(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        assert test.find('typedTestElement').__class__.__name__ == 'TestElement'

    def test_getsTypedElementsThroughPage(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.finds('typedTestElement')
        for element in elements:
              assert element.__class__.__name__ == 'TestElement'
        assert len(elements) > 0

    def test_getsTypedElementThroughPageOverride(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        assert test.find('typedTestElement', type=BaseElement).__class__.__name__ == 'BaseElement'

    def test_getsTypedElementsThroughPageOverride(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.finds('typedTestElement', type=BaseElement)
        for element in elements:
              assert element.__class__.__name__ == 'BaseElement'
        assert len(elements) > 0

    def test_getsElementThroughPageContainer(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        assert test.container.find('testElement').__class__.__name__ == 'BaseElement'

    def test_getsElementsThroughPageContainer(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.container.finds('testElement')
        for element in elements:
              assert element.__class__.__name__ == 'BaseElement'
        assert len(elements) > 0

    def test_getsTypedElementThroughPageContainer(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        assert test.container.find('typedTestElement').__class__.__name__ == 'TestElement'

    def test_getsTypedElementsThroughPageContainer(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.container.finds('typedTestElement')
        for element in test.container.finds('typedTestElement'):
              assert element.__class__.__name__ == 'TestElement'
        assert len(elements) > 0


    def test_getsTypedElementThroughPageContainerThroughFind(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        assert test.container.find('testElement', type=TestElement).__class__.__name__ == 'TestElement'

    def test_getsTypedElementsThroughPageContainerThroughFinds(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.container.finds('testElement', type=TestElement)
        for element in test.container.finds('typedTestElement'):
              assert element.__class__.__name__ == 'TestElement'
        assert len(elements) > 0

    def test_getsTypedElementThroughPageContainerOverride(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        assert test.container.find('typedTestElement', type=BaseElement).__class__.__name__ == 'BaseElement'

    def test_getsTypedElementsThroughPageContainerOverride(self):
        self.driver.implicitly_wait(15)
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')
        test = TestPage(driver=self.driver)
        elements = test.container.finds('typedTestElement', type=BaseElement)
        for element in elements:
              assert element.__class__.__name__ == 'BaseElement'
        assert len(elements) > 0
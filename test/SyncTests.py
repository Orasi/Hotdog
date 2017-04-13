import os
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from hotdog.FilePath import get_full_path
os.environ['PROJECTFOLDER'] = get_full_path('') + 'test'
from hotdog.BasePage import HotDogBasePage
from selenium.webdriver.common.by import By
from hotdog.BaseTest import HotDogBaseTest
from hotdog.BaseElement import BaseElement


class GetElementTests(HotDogBaseTest):

    def setUp(self):
        super().setUp()
        self.driver.default_wait_time = 0

    def test_sync_present(self):
        self.driver.get('http://orasi.github.io/Chameleon/sites/unitTests/orasi/core/interfaces/element.html')
        button = self.driver.find_element(by=By.ID,value='appear')
        button.sync_present().click()

    def test_sync_not_present(self):
        self.driver.get('http://orasi.github.io/Chameleon/sites/unitTests/orasi/core/interfaces/element.html')
        button = self.driver.find_element(by=By.ID,value='disappear')
        button.sync_not_present()
        assert button.element == None
        with self.assertRaises(NoSuchElementException):
            button.click(timeout=0)

    def test_sync_disabled(self):
        self.driver.get('http://orasi.github.io/Chameleon/sites/unitTests/orasi/core/interfaces/element.html')
        button = self.driver.find_element(by=By.ID,value='enable-disable')
        button.sync_disabled().click(timeout=0)

    def test_sync_enabled(self):
        self.driver.get('http://orasi.github.io/Chameleon/sites/unitTests/orasi/core/interfaces/element.html')
        button = self.driver.find_element(by=By.ID,value='disable-enable')
        assert button.sync_enabled().is_displayed()

    def test_sync_starts_with(self):
        self.driver.get('http://orasi.github.io/Chameleon/sites/unitTests/orasi/core/interfaces/element.html')
        button = self.driver.find_element(by=By.ID,value='change-text')
        button.sync_text_starts_with('aaaaaaaaa').click()

    def test_sync_ends_with(self):
        self.driver.get('http://orasi.github.io/Chameleon/sites/unitTests/orasi/core/interfaces/element.html')
        button = self.driver.find_element(by=By.ID,value='change-text')
        button.sync_text_ends_with('aaaaaaaaa').click()

    def test_sync_text_contains(self):
        self.driver.get('http://orasi.github.io/Chameleon/sites/unitTests/orasi/core/interfaces/element.html')
        button = self.driver.find_element(by=By.ID,value='change-text')
        button.sync_text_contains('aaaaaaaaa').click()

    def test_sync_starts_with_insensitive(self):
        self.driver.get('http://orasi.github.io/Chameleon/sites/unitTests/orasi/core/interfaces/element.html')
        button = self.driver.find_element(by=By.ID,value='change-text')
        button.sync_text_starts_with('AAAAAAAA', ignore_case=True).click()

    def test_sync_ends_with_insensitive(self):
        self.driver.get('http://orasi.github.io/Chameleon/sites/unitTests/orasi/core/interfaces/element.html')
        button = self.driver.find_element(by=By.ID,value='change-text')
        button.sync_text_ends_with('AAAAAAAA', ignore_case=True).click()

    def test_sync_text_contains_insensitive(self):
        self.driver.get('http://orasi.github.io/Chameleon/sites/unitTests/orasi/core/interfaces/element.html')
        button = self.driver.find_element(by=By.ID,value='change-text')
        button.sync_text_contains('AAAAAAAA', ignore_case=True).click()

    def test_sync_attribute_value(self):
        self.driver.get('http://orasi.github.io/Chameleon/sites/unitTests/orasi/core/interfaces/element.html')
        button = self.driver.find_element(by=By.ID,value='hidden-unhide')
        assert button.sync_attribute_value('hidden', None).is_displayed()

    def test_sync_not_attribute_value(self):
        self.driver.get('http://orasi.github.io/Chameleon/sites/unitTests/orasi/core/interfaces/element.html')
        button = self.driver.find_element(by=By.ID,value='hidden-unhide')
        assert button.sync_not_attribute_value('hidden', 'true').is_displayed()
import unittest
from appium import webdriver
from selenium import webdriver as seleniumWebdriver
from sauceclient import SauceClient
import sys
from hotdog import Mustard
from hotdog.Results import UploadResults
from hotdog.Config import GetConfig
from time import sleep, time
from appium_selector.DeviceSelector import DeviceSelector
import builtins
import threading
import webium.settings

webium.settings.implicit_timeout = 5

class HotDogBaseTest(unittest.TestCase):

    #Boilerplate Settings Do not Change
    #Change in Config.xml
    SAUCE_USERNAME = GetConfig('SAUCE_USERNAME')
    SAUCE_ACCESS = GetConfig('SAUCE_ACCESS')

    SAUCE_URL = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (SAUCE_USERNAME, SAUCE_ACCESS)
    GRID_URL = GetConfig('GRID_URL') + '/wd/hub'
    LOCAL_APPIUM_URL = GetConfig('LOCAL_APPIUM_URL')

    failed = False
    skipMustard = False
    defaultTestResult = UploadResults

    timersStart = {}
    timersTotal = {}


    @classmethod
    def setUpClass(cls):
        if not hasattr(builtins, 'threadlocal'):
            builtins.threadlocal = threading.local()
            builtins.threadlocal.config = DeviceSelector(platform='mobile').getDevice()[0]

    def setUp(self):
        runLocal = False
        self.desired_caps = builtins.threadlocal.config['desiredCaps']
        self.options = builtins.threadlocal.config['options']
        self.resultLink = None
        self.provider = self.options['provider']
        try:
            if 'grid' in self.provider:
                url = self.GRID_URL
            elif 'sauce' in self.provider:
                url = self.SAUCE_URL
            elif self.provider.lower() == 'local-chrome':
                runLocal = True
                self.driver = seleniumWebdriver.Chrome()
            elif self.provider.lower() == 'local-firefox':
                runLocal = True
                self.driver = seleniumWebdriver.Firefox()
            elif self.provider.lower() == 'local-ie':
                runLocal = True
                self.driver = seleniumWebdriver.Ie()
            else:
                url = self.GRID_URL

            if not runLocal:
                self.driver = webdriver.Remote(
                    url,
                    self.desired_caps
                )
        except:
            print("Testcase [%s] COULD NOT START on device [%s]" % (self._testMethodName, self.desired_caps['browserName']))
            raise unittest.SkipTest('Could not launch driver')


        self.deviceName = self.desired_caps['deviceName'] if 'deviceName' in self.desired_caps else self.desired_caps['udid']
        print("Testcase [%s] started on device [%s]" % (self._testMethodName, self.desired_caps['browserName']))
        sleep(3)

    def tearDown(self):
        if 'sauce' in self.provider.lower():
            sauce = SauceClient(self.SAUCE_USERNAME, self.SAUCE_ACCESS)
            self.resultLink = "https://saucelabs.com/beta/tests/%s" % self.driver.session_id
            try:
                if sys.exc_info() == (None, None, None):
                    sauce.jobs.update_job(self.driver.session_id, passed=True, name=self._testMethodName)
                else:
                    sauce.jobs.update_job(self.driver.session_id, passed=False, name=self._testMethodName)
            except:
                pass

    def run(self, result=None):
        super().run( result=UploadResults())

    def timerStart(self, name):
        self.timersStart[name] = time()

    def timerStop(self, name):
        self.timersTotal[name] = time() - self.timersStart[name]
        if self.options['mustard']:
            Mustard.UploadPerformance(self.driver.desired_capabilities['udid'], name, self.timersTotal[name])
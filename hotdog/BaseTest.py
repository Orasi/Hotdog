import unittest
import sys
import os
import builtins
import threading
from appium import webdriver
from appium_selector.DeviceSelector import DeviceSelector
from hotdog import Mustard
from hotdog.Results import UploadResults
from hotdog.Config import GetConfig
from hotdog.BaseDriver import BaseWebDriver
from hotdog.TestStep import StepLog, Step
from sauceclient import SauceClient
from selenium import webdriver as seleniumWebdriver
from selenium.webdriver import DesiredCapabilities
from time import sleep, time


class HotDogBaseTest(unittest.TestCase):

    # HotDog Defaults.  Can be overridden in child classes
    DefaultWebDriver = BaseWebDriver
    failed = False
    defaultTestResult = UploadResults

    #Boilerplate Settings Do not Change
    #Change in Config.xml
    SAUCE_USERNAME = GetConfig('SAUCE_USERNAME')
    SAUCE_ACCESS = GetConfig('SAUCE_ACCESS')

    SAUCE_URL = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (SAUCE_USERNAME, SAUCE_ACCESS)
    GRID_URL = GetConfig('GRID_URL') + '/wd/hub'
    LOCAL_APPIUM_URL = GetConfig('LOCAL_APPIUM_URL')

    # set SKIP_SELECTOR to bypass the device selector & run local with platfrom from LOCAL_BROWSER
    try:
        SKIP_SELECTOR = GetConfig('SKIP_SELECTOR')
        LOCAL_BROWSER = GetConfig('LOCAL_BROWSER')
        DEFAULT_CONFIG = {
                    'desiredCaps': {'browserName':  'Local',
                                    'deviceName':   'Local',
                                    'platformName': 'Local',
                                    'version':      'Local'},
                    'options': {'manufacturer': 'local',
                                'mustard':       False,
                                'provider':     'local-'+ LOCAL_BROWSER,
                                'osv':          'Local',
                                'model':        'local',
                                "idleTimeout":   360
                                }
                }
    except:
        #xml file is missing SKIP_SELECTOR/LOCAL_BROWSER
        SKIP_SELECTOR = 'False'


    timersStart = {}
    timersTotal = {}
    testcase_id = ''
    try:
        app_env =  os.environ['APP_DATA'].split('<|>')
        app_env = app_env[0]
        print('APP_DATA Environment Data found.  Appending app_env [%s] to test' % app_env[0])
        app_url = app_env[1]
        print('APP_DATA Environment Data found.  Appending app_url [%s] to test' % app_env[1])
    except:
        pass



    @classmethod
    def setUpClass(cls, platform='mobile'):
        if not hasattr(builtins, 'threadlocal'):

            builtins.threadlocal = threading.local()

            #Use Default Driver or display device selector
            if HotDogBaseTest.SKIP_SELECTOR == 'True':
                builtins.threadlocal.config = HotDogBaseTest.DEFAULT_CONFIG
            else:
                builtins.threadlocal.config = DeviceSelector(platform=platform).getDevice()[0]

            # If testing mobile apps, append app info into desired caps
            if 'platformName' in builtins.threadlocal.config['desiredCaps']:
                if builtins.threadlocal.config['desiredCaps']['platformName'].upper() == 'ANDROID':
                    builtins.threadlocal.config['desiredCaps']['app'] = GetConfig('ANDROID_APP_URL')
                else:
                    builtins.threadlocal.config['desiredCaps']['app'] = GetConfig('IOS_APP_URL')

            # Instantiate Driver
            desired_caps = builtins.threadlocal.config['desiredCaps']
            provider = builtins.threadlocal.config['options']['provider']
            try:
                builtins.threadlocal.driver = cls.select_driver(cls, desired_caps, provider)
            except:
                print(sys.exc_info()[1])
                raise unittest.SkipTest('Could not launch driver')


    def setUp(self):

        # Setup Test
        self.desired_caps = builtins.threadlocal.config['desiredCaps']
        self.options = builtins.threadlocal.config['options']
        self.options['deviceName'] = self.environmentName()
        self.provider = self.options['provider']
        self.resultLink = None

        # Reinitialize driver if destroyed
        if not builtins.threadlocal.driver:

            try:
                self.driver = self.__class__.select_driver(self, self.desired_caps, self.provider)
                builtins.threadlocal.driver = self.driver
                self.continueWithDriver = False
            except:
                print("Testcase [%s] COULD NOT START on device [%s]" % (self._testMethodName, self.options['deviceName']))
                print(sys.exc_info()[1])
                raise unittest.SkipTest('Could not launch driver')

        else:
            self.driver = builtins.threadlocal.driver
            self.continueWithDriver = True

        # Create root node for Step Log
        builtins.threadlocal.driver.step_log = StepLog()
        self.end_step = self.add_test_step(self._testMethodName)

        print("Testcase [%s] started on device [%s]" % (self._testMethodName, self.options['deviceName']))


    def environmentName(self):
        if 'deviceName' in self.options:
            return self.options['deviceName']
        elif 'udid' in self.desired_caps:
            return self.desired_caps['udid']
        else:
            return self.options['provider']

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


    @classmethod
    def tearDownClass(cls):
        cls.RemoveApp()

    @classmethod
    def RemoveApp(self):
        if 'mobile' in builtins.threadlocal.config['options']['provider']:
            try: builtins.threadlocal.driver.close_app()
            except: pass
            try: builtins.threadlocal.driver.remove_app(GetConfig('IOS_BUNDLE_ID'))
            except: pass
            try: builtins.threadlocal.driver.remove_app(GetConfig('ANDROID_BUNDLE_ID'))
            except: pass
        try: builtins.threadlocal.driver.quit()
        except: pass

    def add_test_step(self, step_name):
        self.driver.step_log.add_step(Step(step_name))
        return self.driver.step_log.close_step

    def run(self, result=None):
        try:
            super().run( result= self.defaultTestResult())
        except:
            try:
                self.driver.quit()
            except:
                pass
            raise

    def timerStart(self, name):
        self.timersStart[name] = time()

    def timerStop(self, name):
        self.timersTotal[name] = time() - self.timersStart[name]
        if self.options['mustard']:
            Mustard.UploadPerformance(Mustard.getDeviceID(self), name, self.timersTotal[name])

    @staticmethod
    def select_driver(cls, dc, provider):
        runLocal = False
        browser_profile = None

        if 'grid' in provider:
            # if self.desired_caps['browserName'].lower() == 'firefox':
            #     browser_profile = seleniumWebdriver.FirefoxProfile('/home/matt/l7539ezh.GridTest')
            if dc['platform'].lower() == 'windows':
                dc['marionette'] = False
            url = cls.GRID_URL
        elif 'sauce' in provider:
            url = cls.SAUCE_URL
            if dc['browserName'] == 'internet explorer':
                dc['requireWindowFocus'] = True
            elif dc['browserName'] == 'chrome' and dc.get('chromeOptions') is None:
                builtins.threadlocal.config['desiredCaps']['chromeOptions'] = {
                    'excludeSwitches': ['disable-component-update']}
        elif provider.lower() == 'local-chrome':
            runLocal = True
            driver = seleniumWebdriver.Chrome()
        elif provider.lower() == 'local-firefox:marionette':
            runLocal = True
            caps = DesiredCapabilities.FIREFOX
            caps['marionette'] = True
            driver = seleniumWebdriver.Firefox(caps)
        elif provider.lower() == 'local-firefox':
            caps = DesiredCapabilities.FIREFOX
            caps['marionette'] = False
            runLocal = True
            driver = seleniumWebdriver.Firefox(caps)
        elif provider.lower() == 'local-safari':
            runLocal = True
            driver = seleniumWebdriver.Safari()
        elif provider.lower() == 'local-ie':
            runLocal = True
            driver = seleniumWebdriver.Ie()
        elif provider.lower() == 'mcweb':
            url = GetConfig('MC_URL') + '/wd/hub'
        elif provider.lower() == 'mcmobile':
            url = GetConfig('MC_URL') + '/wd/hub'
        else:
            url = cls.GRID_URL

        if not runLocal:
            driver = webdriver.Remote(
                url,
                dc,
                browser_profile=browser_profile
            )

        driver.__class__ = cls.DefaultWebDriver
        driver.test_steps = []
        driver.tracelog = []

        return driver


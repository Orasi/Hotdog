import unittest
from hotdog.Mustard import *


class UploadResults(unittest.TestResult):

    def addError(self, test, err):
        stack = self._exc_info_to_string(err, test)
        error_message = self.get_error_message(stack)

        UploadToMustard(test, 'fail', error_message=error_message, stacktrace=stack)
        try:
            test.driver.close_app()
            self.RemoveApp(test)
            test.driver.quit()
        except:
            pass

        super().addError( test, err)
        print("Testcase [%s] ended with status [%s] on device [%s]\n %s" % (test._testMethodName,
                                                                       'ERROR',
                                                                       test.desired_caps['browserName'],
                                                                       stack))
    def addFailure(self, test, err):
        stack = self._exc_info_to_string(err, test)
        error_message = self.get_error_message(stack)

        UploadToMustard(test, 'fail', error_message=error_message, stacktrace=stack)
        test.driver.close_app()
        self.RemoveApp(test)

        test.driver.quit()
        super().addFailure(test, err)
        print("Testcase [%s] ended with status [%s] on device [%s] \n %s" % (test._testMethodName,
                                                                       'FAIL',
                                                                       test.desired_caps['browserName'],
                                                                       stack))

    def addSuccess(self, test):
        UploadToMustard(test, 'pass')
        test.driver.close_app()
        self.RemoveApp(test)
        test.driver.quit()
        super().addSuccess(test)
        print("Testcase [%s] ended with status [%s] on device [%s]" % (test._testMethodName,
                                                                       'PASS',
                                                                       test.desired_caps['browserName']))

    def get_error_message(self, stacktrace):
        stackArray = stacktrace.split('\n')
        stackArray.reverse()
        for stack in stackArray:
            if len(stack) > 5:
                splitMessage = stack.split(':')
                return splitMessage[len(splitMessage)-1]

    def RemoveApp(self, test):
        try: test.driver.remove_app(GetConfig('IOS_BUNDLE_ID'))
        except: pass
        try: test.driver.remove_app(GetConfig('ANDROID_BUNDLE_ID'))
        except: pass
import unittest
import builtins

from hotdog.Mustard import *


class UploadResults(unittest.TestResult):
    projectFolder = os.environ['PROJECTFOLDER']

    def end_steps(self, step_log, status):
        for step in  step_log.open_step:
            step.end_step(status)

    def addError(self, test, err):
        stack = self._exc_info_to_string(err, test)
        error_message = self.get_error_message(err, stack)

        try:
            self.end_steps(test.driver.step_log, 'error')
        except:
            pass

        UploadToMustard(test, 'fail', error_message=error_message, stacktrace=stack)
        self.RemoveApp(test)
        builtins.threadlocal.driver = None
        super().addError( test, err)

        print("Testcase [%s] ended with status [%s] on device [%s]\n %s" % (test._testMethodName,
                                                                       'ERROR',
                                                                       test.options['deviceName'],
                                                                       stack))
    def addFailure(self, test, err):
        stack = self._exc_info_to_string(err, test)
        error_message =  self.get_error_message(err, stack)

        try:
            self.end_steps(test.driver.step_log, 'error')
        except:
            pass

        UploadToMustard(test, 'fail', error_message=error_message, stacktrace=stack)

        self.RemoveApp(test)
        builtins.threadlocal.driver = None
        super().addFailure(test, err)
        print("Testcase [%s] ended with status [%s] on device [%s] \n %s" % (test._testMethodName,
                                                                       'FAIL',
                                                                       test.options['deviceName'],
                                                                       stack))

    def addSuccess(self, test):

        try:
            self.end_steps(test.driver.step_log, 'complete')
        except:
            pass

        UploadToMustard(test, 'pass')
        try:
            if not builtins.threadlocal.keepSession:
                builtins.threadlocal.driver = None
        except:
            builtins.threadlocal.driver = None
            self.RemoveApp(test)
        super().addSuccess(test)

        print("Testcase [%s] ended with status [%s] on device [%s]" % (test._testMethodName,
                                                                       'PASS',
                                                                       test.options['deviceName']))

    def addSkip(self, test, reason):
        UploadToMustard(test, 'skip')
        try:
            if not builtins.threadlocal.keepSession:
                builtins.threadlocal.driver = None
        except:
            builtins.threadlocal.driver = None
            self.RemoveApp(test)
        super().addSuccess(test)
        print("Testcase [%s] skipped on device [%s] because [%s]" % (test._testMethodName,
                                                                       test.options['deviceName'],
                                                                     reason))


    def get_error_message(self, error, stacktrace):
        try:
            errmsg=  str(error[1])
            if len(errmsg) > 100:
                return errmsg[0:100]
            else:
                return errmsg
        except:
            stackArray = stacktrace.split('\n')
            stackArray.reverse()
            for stack in stackArray:
                if len(stack) > 5:
                    splitMessage = stack.split(':')
                    return splitMessage[len(splitMessage)-1]

    def RemoveApp(self, test):
        if 'mobile' in test.options['provider']:
            try: test.driver.close_app()
            except: pass
            try: test.driver.remove_app(GetConfig('IOS_BUNDLE_ID'))
            except: pass
            try: test.driver.remove_app(GetConfig('ANDROID_BUNDLE_ID'))
            except: pass
        try: test.driver.quit()
        except: pass
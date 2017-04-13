def Testcase(testcase_id=None):
    def test_case(function):
        def wrapper(*args,**kwargs):
            if testcase_id:
                args[0].testcase_id = testcase_id
            else:
                args[0].testcase_id = args[0]._testMethodName
            return function(*args,**kwargs)
        return wrapper
    return test_case
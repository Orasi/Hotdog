import builtins
import json
import time
import re


def TestStep(argument=False, log_result=False):
    def test_step(function):
        def wrapper(*args, **kwargs):

            step = Step(argument)

            matches = re.findall('\{(.*?)\}', step.step_name)
            for m in matches:
                try:
                    step.step_name = step.step_name.replace('{%s}' % m, str(eval(m)))
                except:
                    step.step_name = step.step_name.replace('{%s}' % m, '<ERROR>')

            builtins.threadlocal.driver.step_log.add_step(step)
            try:
                result = function(*args, **kwargs)
            except:
                step.end_step('error')
                raise
            else:
                if log_result:
                    result_step = Step('Result [%s]' % result)
                    builtins.threadlocal.driver.step_log.add_step(result_step)
                    result_step.end_step('complete')
                    builtins.threadlocal.driver.step_log.close_step()
                step.end_step('complete')
            builtins.threadlocal.driver.step_log.close_step()
            return result

        return wrapper
    return test_step


class Step(object):

    def __init__(self, step_name):
        super().__init__()
        self.step_name = step_name
        self.sub_steps = []
        self.start_time = time.time()
        self.end_time = ''
        self.elapsed_time = ''
        self.status = ''

    def add_step(self, sub):

        self.sub_steps.append(sub)

    def end_step(self, status):
        self.status = status
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time


def encode_step(obj):
    if isinstance(obj, Step):
        return obj.__dict__
    else:
        return obj


class StepLog(object):

    def __init__(self):
       self.steps = []
       self.open_step = []

    def add_step(self, step):
        if self.open_step:
            self.open_step[-1].add_step(step)
            self.open_step.append(step)
        else:
            self.steps.append(step)
            self.open_step.append(step)

    def close_step(self, status='complete'):
        self.open_step[-1].end_step(status)
        del self.open_step[-1]

    def to_json(self):
        return json.dumps(self.steps, default=encode_step)


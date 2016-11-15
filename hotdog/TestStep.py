import builtins


def TestStep(argument=False):
    def test_step(function):
        def wrapper(*args, **kwargs):

            step = Step(argument)
            builtins.threadlocal.driver.step_log.add_step(step)
            try:
                function(*args, **kwargs)
            except:
                step.end_step('error')
                raise
            else:
                step.end_step('complete')
            builtins.threadlocal.driver.step_log.close_step()
        return wrapper
    return test_step


class Step:

    def __init__(self, step_name):
        self.step_name = step_name
        self.sub_steps = []
        self.status = ''

    def add_step(self, sub):
        self.sub_steps.append(sub)

    def end_step(self, status):
        self.status = status


class StepLog:

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
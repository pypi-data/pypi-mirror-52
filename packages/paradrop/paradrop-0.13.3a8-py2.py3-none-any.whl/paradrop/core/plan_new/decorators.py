from .step import Step


def step(gets=[], sets=[]):
    def wrapper(func):
        step_def = Step(func, gets, sets)
        func.step = step_def

        return func

    return wrapper

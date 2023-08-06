class Step(object):
    """
    Defines a step in an update execution plan.  Steps can have inputs/outputs
    and dependencies that define their ordering as well as conditions that
    determine whether they should be applied.
    """

    def __init__(self, func, gets=[], sets=[]):
        self.func = func
        self.gets = set(gets)
        self.sets = set(sets)

    def __cmp__(self, other):
        if (self.sets & other.gets):
            return -1
        elif (other.sets & self.gets):
            return 1
        else:
            return 0


class AbortStep(Step):
    """
    A specific execution step that should be applied during abort sequence.
    """

    def __init__(self, func, target):
        super(AbortStep, self).__init__(func)

"""Contains objects for creating policies"""

policy_count = 0


class WrappedPolicy(object):
    """The wrapper for the policy function"""

    func = None
    policy_info = None
    tests = None

    def __init__(self):
        self.tests = []

    def __call__(self, context, event):
        self.func(context, event) # pylint: disable=not-callable

    def test(self, context_factory):
        """Test the policy"""

        for event, test in self.tests:
            context = context_factory()
            self(context, event)
            test(context, event)

    def add_test(self, event):
        """Function decorator to add a test to a policy"""

        def wrapper(func):
            """wrapper for test functions"""
            self.tests.append(event, func)
            return func
        return wrapper


def policy(**kwargs):
    """Function decorator to allow for anotated policies"""

    wrapped_policy = WrappedPolicy()
    wrapped_policy.policy_info = kwargs

    def wrapper(func):
        """policy function wrapper"""
        wrapped_policy.func = func
        return wrapped_policy

    return wrapper


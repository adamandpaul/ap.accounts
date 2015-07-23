
_policy_count = 0



def policy(**kwargs):
    kwargs = kwargs.copy()
    def policy_wrapper(func):

        # Set Policy Info
        global _policy_count
        _policy_count = _policy_count + 1
        kwargs["order"] = _policy_count
        func.policy_info = kwargs

        # Set Null test data
        func.test_data = None

        # Set Empty
        func._test = None
        def test_decorator(f):
            func._test = f
            return f
        func.test = test_decorator

        return func


    return policy_wrapper



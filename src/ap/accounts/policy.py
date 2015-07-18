
_policy_count = 0

def policy(**kwargs):
    kwargs = kwargs.copy()
    def policy_wrapper(func):
        global _policy_count
        _policy_count = _policy_count + 1
        kwargs["order"] = _policy_count
        func.policy_info = kwargs
        return func
    return policy_wrapper



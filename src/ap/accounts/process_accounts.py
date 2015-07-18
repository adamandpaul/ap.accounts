
import sys
import os.path
import imp
import hashlib

def process_accounts():
    argv = sys.argv
    accounts_folder = argv[1]
    policy_module = os.path.join(accounts_folder, "policies.py")

    policy_module_name = "policy"
    policy_module_name += hashlib.md5(policy_module).hexdigest()

    policies = imp.load_source(policy_module_name, policy_module)

    import pdb; pdb.set_trace()




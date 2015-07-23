
import sys
import os.path
import imp
import hashlib

from ap.accounts.Book import Book

class ProcContext(object):

    def set_event_from_input_dict (self, input):
        pass

    @property
    def event(self):
        return self._data
    @event.setter
    def event(self, v):
        self._data = v

    @property
    def bookyear(self):
        return self.book.get_year(event.date.finyear)
    
    @property
    def bookquarter(self):
        finquarter = self.event.date.quarter
        return self.book_year.quarters[finquarter]

    @property
    def book(self):
        try:
            return self._book
        except AttributeError:
            self._book = Book()
    


def process_accounts():
    argv = sys.argv
    accounts_folder = argv[1]
    policy_module = os.path.join(accounts_folder, "policies.py")

    policy_module_name = "policy"
    policy_module_name += hashlib.md5(policy_module).hexdigest()

    policies = imp.load_source(policy_module_name, policy_module)

    import pdb; pdb.set_trace()




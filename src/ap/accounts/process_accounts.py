"""Module to manage the processing of an accounts dir"""
import sys
import os.path
import imp
import hashlib

from ap.accounts.Book import Book

class ProcContext(object):
    """A manager class for an accounts context"""

    def set_event_from_input_dict(self, input_dict):
        """set the current event from input"""
        pass

    _data = None

    @property
    def event(self):
        """return the current event object"""
        return self._data

    @event.setter
    def event(self, value):
        """set the current event with an event object"""
        self._data = value

    @property
    def bookyear(self):
        """Return the current book year for the current event"""
        return self.book.get_bookyear(self.event.date.finyear)

    @property
    def bookquarter(self):
        """Return the current bookquarter for the current event"""
        finquarter = self.event.date.quarter
        return self.bookyear.quarters[finquarter]

    _book = None
    @property
    def book(self):
        """Return the accounts book"""
        if self._book is None:
            self._book = Book()
        return self._book


def process_accounts():
    """Script entry point to process an accounts folder"""

    argv = sys.argv
    accounts_folder = argv[1]
    policy_module = os.path.join(accounts_folder, "policies.py")

    policy_module_name = "policy"
    policy_module_name += hashlib.md5(policy_module).hexdigest()

    policies = imp.load_source(policy_module_name, policy_module)

    # import pdb; pdb.set_trace()

    return policies



# -*- coding: utf-8 -*-
"""Deltas concerns objects which record changes in an accouting system.

These objects are used as the basis of accouting transactions themselvs
and metrics operations
"""

from ap.accounts import DEBIT, NEUTRAL, CREDIT
from ap.accounts.Entry import Entry

class AccountsDelta(object):
    """Represents a change in accounts"""

    _entries = None
    @property
    def entries(self):
        if self._entries is None:
            self._entries = {}
        return self._entries

    @property
    def balanced(self):
        total = Entry(NEUTRAL, 0)
        for entry in self.entries.values():
            total += entry
        return total.direction == NEUTRAL
                

    def add_entry (self, account, entry):
        current_entry = self.entries.get(account, Entry(NEUTRAL, 0))
        new_entry = current_entry + entry
        self.entries[account] = new_entry

        # Remove entry if it doens't have meaning
        if new_entry.direction == NEUTRAL:
            del self.entries[account]

    def __add__ (self, other):
        delta = AccountsDelta()

        for account, entry in self.entries.items():
            delta.add_entry(account, entry)

        for account, entry in other.entries.items():
            delta.add_entry(account, entry)

        return delta






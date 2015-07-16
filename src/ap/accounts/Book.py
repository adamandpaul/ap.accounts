
from ap.accounts.FinDate import FinDate
from ap.accounts.BookYear import BookYear
from ap.accounts.AccountsDelta import AccountsDelta

class Book(object):

    def __init__ (self):
        self._bookyears = {}


    def get_bookyear(self, finyear):
        try:
            return self._bookyears[finyear]
        except KeyError:
            self._bookyears[finyear] = BookYear(finyear)
        return self._bookyears[finyear]

    @property
    def years(self):
        return self._bookyears.keys()

    @property
    def accounts_delta(self):
        delta = AccountsDelta()
        for year in self.years:
            delta += self.get_bookyear(year).accounts_delta
        return delta


    def add_transaction (self, tx, suffix_tx_id=None):
        tx_date = FinDate(tx.date)
        bookyear = self.get_bookyear(tx_date.finyear)
        return bookyear.add_transaction(tx, suffix_tx_id)

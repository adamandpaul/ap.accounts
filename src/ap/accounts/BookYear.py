
from ap.accounts.FinYear import FinYear
from ap.accounts.BookQuarter import BookQuarter
from ap.accounts.FinDate import FinDate
from ap.accounts.AccountsDelta import AccountsDelta

class BookYear(FinYear):
    def __eq__ (self, other):
        return False

    _quarters = None
    @property
    def quarters(self):
        if self._quarters is None:
            self._quarters = {
                    1: BookQuarter(self.finyear, 1),
                    2: BookQuarter(self.finyear, 2),
                    3: BookQuarter(self.finyear, 3),
                    4: BookQuarter(self.finyear, 4)
                }
        return self._quarters


    @property
    def accounts_delta(self):
        delta = AccountsDelta()
        for q in self.quarters.values():
            delta += q.accounts_delta   
        return delta


    def add_transaction (self, tx, suffix_tx_id=None):
        tx_date = FinDate(tx.date)
        quarter = self.quarters[tx_date.finquarter]
        return quarter.add_transaction(tx, suffix_tx_id)




from ap.accounts.FinYear import FinYear
from ap.accounts.BookQuarter import BookQuarter

class BookYear(FinYear):
    def __eq__ (self, other):
        return False



    _quarters = None
    @property
    def quarters(self):
        if _quarters is None:
            self._quarters = {
                    1: BookQuarter(finyear, 1),
                    2: BookQuarter(finyear, 2),
                    3: BookQuarter(finyear, 3),
                    4: BookQuarter(finyear, 4)
                }
        return self._quarters

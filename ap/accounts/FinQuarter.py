

from datetime import date
import ap.accounts.FinYear

class FinQuarter(object):

    def __init__ (self, finyear, finquarter):
        self.finyear = finyear
        self.finquarter = finquarter

    @property
    def year(self):
        if self.finquarter >=3:
            return self.finyear + 1
        return self.finyear

    @property
    def quarter(self):
        return {
            1: 3,
            2: 4,
            3: 1,
            4: 2,
            }[self.finquarter]

    @property
    def start_month(self):
        return {
            1: 7,
            2: 10,
            3: 1,
            4: 4,
            }[self.finquarter]

    @property
    def end_month(self):
        return {
            1: 9,
            2: 12,
            3: 3,
            4: 6,
            }[self.finquarter]

    @property
    def start(self):
        return date(self.year, self.start_month, 1)

    @property
    def end(self):
        try:
            return date(self.year, self.end_month, 31)
        except ValueError:
            return date(self.year, self.end_month, 30)

    def __str__ (self):
        fy = str(ap.accounts.FinYear.FinYear(self.finyear))
        return "%sQ%s" % (fy, self.finquarter)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self))






    


    
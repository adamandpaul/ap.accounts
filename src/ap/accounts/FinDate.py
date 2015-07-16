

from datetime import date


quarter_for_month = {
            1: 1,
            2: 1,
            3: 1,
            4: 2,
            5: 2,
            6: 2,
            7: 3,
            8: 3,
            9: 3,
            10: 4,
            11: 4,
            12: 4,
        }

finquarter_for_month = {
            1: 3,
            2: 3,
            3: 3,
            4: 4,
            5: 4,
            6: 4,
            7: 1,
            8: 1,
            9: 1,
            10: 2,
            11: 2,
            12: 2,
        }


class FinDate (date):

    @property
    def quarter(self):
        return quarter_for_month[self.month]

    @property
    def finquarter(self):
        return finquarter_for_month[self.month]
    
    @property
    def finyear(self):
        if self.month <= 6:
            return self.year - 1
        return self.year




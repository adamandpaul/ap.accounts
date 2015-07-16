
from datetime import date

class FinYear(object):

    def __init__(self, finyear):
        self.finyear = finyear

    @property
    def end_year(self):
        return self.finyear + 1

    @property
    def start(self):
        return date(self.finyear, 7, 1)

    @property
    def end(self):
        return date(self.end_year, 6, 30)

    def __str__(self):
        return "%s-%s" % (self.finyear, str(self.end_year)[2:])

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self))

    def __eq__ (self, other):
        return self.finyear == other.finyear
   

    
     
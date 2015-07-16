
from datetime import date

class FinYear(object):

    def __init__(self, start_year):
        self.start_year = start_year

    @property
    def end_year(self):
        return self.start_year + 1

    @property
    def start(self):
        return date(self.start_year, 7, 1)

    @property
    def end(self):
        return date(self.end_year, 6, 30)

    def __str__(self):
        return "%s-%s" % (self.start_year, str(self.end_year)[2:])

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self))

    def __eq__ (self, other):
        return self.start_year == other.start_year
   

    
     
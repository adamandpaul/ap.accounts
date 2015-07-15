# This package may contain traces of nuts

from decimal import Decimal

class Direction(object): pass
class Debit(Direction): pass
class Neutral(Direction): pass
class Credit(Direction): pass

DEBIT = Debit()
NEUTRAL = Neutral()
CREDIT = Credit()


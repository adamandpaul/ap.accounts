from decimal import Decimal
from ap.accounts import DEBIT, NEUTRAL, CREDIT

class Entry(object):
    def __init__ (self, direction, amount):
        """Initiate an Entry object

        Args:
          direction (Direction): Either a DEBIT, CREDIT or NEUTRAL
        """

        if direction not in (DEBIT, CREDIT, NEUTRAL):
            raise ValueError()

        if direction == NEUTRAL:
            if amount != 0:
                raise ValueError()

        if amount < 0:

            if direction == DEBIT:
                new_direction = CREDIT
            else:
                new_direction = DEBIT

            direction = new_direction
            amount = amount * Decimal("-1")

        if amount == 0:
            direction = NEUTRAL

        self.direction, self.amount = direction, amount


    def __add__ (self, other):
        """Add two Entries together
        """

        if self.direction == other.direction:
            return Entry(self.direction, self.amount + other.amount)
        else:
            # find the largest
            if self.amount > other.amount:
                result = Entry(self.direction, self.amount - other.amount)
            else:
                result = Entry(other.direction, other.amount - self.amount)

            if result.amount == 0:
                return Entry(NEUTRAL, Decimal("0.0"))
            else:
                return result

        raise NotImplementedError()


    def __eq__ (self, other):
        """Test if two entries are equal"""

        direction_test = self.direction == other.direction
        amount_test = self.amount == other.amount
        return direction_test and amount_test and True
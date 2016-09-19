# -*- coding: utf-8 -*-
"""Code relating to an accounting "entry" as it relates to the ap.accounts package.

In this case an entry is just a Decimal number with the DR/CR information added.
""" 

from decimal import Decimal

DEBIT = "DEBIT"
NEUTRAL = "NEUTRAL"
CREDIT = "CREDIT"

class Entry(object):
    """An entry object represent the financial component in a change in a single account

    For ap.accounts. This object doens't store meta information or date. These
    extra bits of information are stored on the Transaction object.
    """

    def __init__ (self, direction, amount):
        """Initiate an Entry object

        The Entry object likes the amount to be positive. If it is negitive then
        the direction will be flipped in order to make the amount positive.

        If a direction is specified as non NEUTRAL, yet the amount is zero. Then
        the drection property will be set to NEUTRAL.

        Args:
          direction (Direction): Either a DEBIT, CREDIT or NEUTRAL
          amount (Decimal): the magnitude of the entry
        """

        amount = Decimal(amount)

        if direction not in (DEBIT, CREDIT, NEUTRAL):
            raise ValueError('Invalid direction given')

        if direction == NEUTRAL:
            if amount != Decimal('0'):
                raise ValueError('Non-zero amount {!r} given for an Entry of NEUTRAL direction'.format(amount))

        if amount < Decimal('0'):

            if direction == DEBIT:
                new_direction = CREDIT
            else:
                new_direction = DEBIT

            direction = new_direction
            amount = amount * Decimal("-1")

        if amount == Decimal(0):
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

            if result.amount == Decimal('0'):
                return Entry(NEUTRAL, Decimal("0.0"))
            else:
                return result

        raise NotImplementedError()


    def __eq__ (self, other):
        """Test if two entries are equal"""

        direction_test = self.direction == other.direction
        amount_test = self.amount == other.amount
        return direction_test and amount_test and True


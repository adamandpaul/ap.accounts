


===========
ap.accounts
===========

Accounting system of Adam and Paul Pty Ltd


Directions
==========

There are two directions defined in ap.accounts

ap.accounts.DEBIT - means left or debit
ap.accounts.CREDIT - means right or credit
ap.accounts.NEUTRAL - neither a credit or debit, an ammount associated with
  this direction must be equal to zero


Currency Ammounts
=================

ap.accounts uses decimal.Decimal as it's currency type


Accounts
========

Accounts are identified by a label. Account labels must start with either
- assets.
- liabilities.
- equity.

Where assets are treated as left hand side accounts and liabilities and
equity account as treated as right hand side accounts


ap.accounts.check_entry
=======================

check_entry(e) - check that the entry is a valid entry.

raises ValueError if it is not correct


Entry Type
==========

An Entry type consists of a direction and a Decimal ammount.


__init__ (direction, amount):

        Initiate an Entry object

        Args:
          direction (Direction): Either a DEBIT, CREDIT or NEUTRAL


Accounts Delta
==============

An AccountsDelta  is a grouped series of credits and debits to verious 
accounts.

ap.accounts.AccountsDelta.AccountsDelta
=======================================

An AccountsDelta is a grouped series of changes to accounts.


add_entries(a, b)  (@classmethod)

        Adds two account entries together to form the resoultant entry

        Args:
           a (tuple): two member tuple (direction, amount)
           b (tuple): two member tuple (direction, amount)

        Returns: two member tuple (direction, amount)
        
__getitem__(account):
        Gets the entry assosiated with this account

        Returns: two member tuple (direction, amount)

__setitem__(account, entry):
        Sets an entry for an account

        Args:
           account (str): the account label to set
           entry (tuple): two member tupele (direction, amount) which
              is the account entry
        
credit(account, amount):
        Creaete a credit entry in the AccountsDelta

        Args:
            account (str): The account label for the entry
            amount (Decimal): The amount to be credited


debit(account, amount):
        Creaete a debit entry in the AccountsDelta

        Args:
            account (str): The account label for the entry
            amount (Decimal): The amount to be debited

is_balanced():
        Check if the entry credits and debits balance

        Returns: bool
        
entries():
        Returns the entries in the AccountsDelta

        Returns: dict of two memeber tuples (direction, amount).
          where direction is CREDIT or DEBIT and amount is a Decimal
     
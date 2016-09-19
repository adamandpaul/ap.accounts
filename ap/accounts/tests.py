from unittest import TestCase
from ap.accounts.entry import DEBIT, CREDIT, NEUTRAL
from decimal import Decimal

from datetime import date

import unittest
import pkg_resources

from unittest import TestLoader

def test_suite():
    # We need to specificy the top level dir because namespaces don't work too good with unittest
    top_level_dir = pkg_resources.Environment()['ap.accounts'][0].location
    return TestLoader().discover('ap.accounts', pattern='*_test.py', top_level_dir=top_level_dir)


class TestAccountsDelta(TestCase):
    def setUp(self):
        from ap.accounts.Entry import Entry
        from ap.accounts.AccountsDelta import AccountsDelta
        self.Entry = Entry
        self.AccountsDelta = AccountsDelta

    def tearDown(self):
        pass

    def test_transaction_init (self):
        tx = self.AccountsDelta()
        self.assertTrue (tx.balanced)


    def test_transaction_adding_entries (self):
        E = self.Entry
        tx = self.AccountsDelta()

        e1 = E(CREDIT, Decimal("1.0"))
        tx.add_entry("assets.cash", e1)
        self.assertEqual(tx.entries["assets.cash"], e1)

        e2 = E(CREDIT, Decimal("32.0"))
        e3 = E(DEBIT, Decimal("100.0"))
        tx.add_entry("assets.cash", e2)
        tx.add_entry("assets.paintings", e3)
        self.assertEqual(tx.entries["assets.cash"], e1 + e2)
        self.assertEqual(tx.entries["assets.paintings"], e3)

    def test_transaction_adding_nurtralized (self):

        E = self.Entry
        tx = self.AccountsDelta()

        e1 = E(CREDIT, Decimal("40.00"))
        e2 = E(DEBIT, Decimal("40.00"))

        tx.add_entry("assets.cash", e1)
        self.assertIsNotNone(tx.entries.get("assets.cash", None))

        tx.add_entry("assets.cash", e2)
        self.assertIsNone(tx.entries.get("assets.cash", None))

        e3 = E(NEUTRAL, Decimal("0.0"))
        tx.add_entry("assets.blah", e3)
        self.assertIsNone(tx.entries.get("assets.blah", None))

    def test_transaction_balancing (self):
        E = self.Entry
        tx = self.AccountsDelta()

        self.assertTrue(tx.balanced)

        e1 = E(CREDIT, Decimal("20.00"))
        tx.add_entry("assets.cash", e1)
        self.assertFalse(tx.balanced)

        e2 = E(DEBIT, Decimal("8.00"))
        tx.add_entry("equity.profets", e2)
        self.assertFalse(tx.balanced)

        e3 = E(DEBIT, Decimal("12.00"))
        tx.add_entry("liabilities.debt", e3)
        self.assertTrue(tx.balanced)


class TestTransaction(TestCase):
    def setUp(self):
        from ap.accounts.Transaction import Transaction
        self.Transaction = Transaction

    def tearDown(self):
        pass

    def test_transaction_init (self):
        tx = self.Transaction()
        tx.description = "some description"
        tx.date = date(2000,01,01)
        self.assertEqual(tx.description, "some description")
        self.assertEqual(tx.date, date(2000,01,01))




class TestFinDate(TestCase):
    def setUp(self):
        from ap.accounts.FinDate import FinDate
        from ap.accounts.FinYear import FinYear
        self.FinDate = FinDate
        self.FinYear = FinYear
    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.FinDate(date(2010,1,1)), self.FinDate(2010,1,1))
        self.assertEqual(self.FinDate(self.FinDate(2010,1,1)), self.FinDate(2010,1,1))


    def test_quarter(self):
        self.assertEqual(self.FinDate(2000,1,1).quarter, 1)
        self.assertEqual(self.FinDate(2000,4,1).quarter, 2)
        self.assertEqual(self.FinDate(2000,7,1).quarter, 3)
        self.assertEqual(self.FinDate(2000,10,1).quarter, 4)

    def test_finquarter(self):
        self.assertEqual(self.FinDate(2000,1,1).finquarter, 3)
        self.assertEqual(self.FinDate(2000,4,1).finquarter, 4)
        self.assertEqual(self.FinDate(2000,7,1).finquarter, 1)
        self.assertEqual(self.FinDate(2000,10,1).finquarter, 2)

    def test_finyear(self):
        self.assertEqual(self.FinDate(2000,1,1).finyear, 1999)
        self.assertEqual(self.FinDate(2000,10,1).finyear, 2000)



class TestFinYear(TestCase):
    def setUp(self):
        from ap.accounts.FinYear import FinYear
        from ap.accounts.FinDate import FinDate
        self.FinYear = FinYear
        self.FinDate = FinDate

    def tearDown(self):
        pass

    def test_properties(self):
        fy = self.FinYear(2010)
        self.assertEqual(fy.finyear, 2010)
        self.assertEqual(fy.end_year, 2011)
        self.assertEqual(str(fy), "2010-11")
        self.assertEqual(repr(fy), "<FinYear 2010-11>")
        self.assertEqual(fy.start, date(2010,7,1))
        self.assertEqual(fy.end, date(2011,6,30))


class TestFinQuarter(TestCase):
    def setUp(self):
        from ap.accounts.FinQuarter import FinQuarter
        self.FinQuarter = FinQuarter

    def tearDown(self):
        pass


    def test_properties(self):
        fq = self.FinQuarter(2000, 1)
        self.assertEqual(fq.year, 2000)
        self.assertEqual(fq.quarter, 3)
        self.assertEqual(fq.start_month,7)
        self.assertEqual(fq.end_month,9)
        self.assertEqual(fq.start, date(2000,7,1))
        self.assertEqual(fq.end, date(2000,9,30))
        self.assertEqual(str(fq), "2000-01Q1")
        self.assertEqual(repr(fq), "<FinQuarter 2000-01Q1>")



class TestBookQuarter(TestCase):
    def setUp(self):
        from ap.accounts.BookQuarter import BookQuarter
        from ap.accounts.Transaction import Transaction
        self.BookQuarter = BookQuarter
        self.Transaction = Transaction

        from ap.accounts.Entry import Entry
        self.Entry = Entry

    def tearDown(self):
        pass

    def test_quarter (self):
        q = self.BookQuarter(2000, 1)
        tx = self.Transaction()

        q.transactions["1234"] = tx
        self.assertIsInstance(q.transactions["1234"], self.Transaction)

    def test_construct_id(self):
        q = self.BookQuarter(2000, 1)
        tx = self.Transaction()
        tx.date = date(2000, 6, 10)

        id1 = q.construct_id(tx)
        id2 = q.construct_id(tx)
        self.assertNotEqual(id1, id2)

        id3 = q.construct_id(tx, "my-ending")
        self.assertIn("my-ending", id3)

    def test_add_transaction(self):


        q = self.BookQuarter(2000, 1)
        tx1 = self.Transaction()
        tx1.date = date(2000, 6, 10)
        tx1.add_entry("assets.cash", self.Entry(CREDIT, Decimal("10.00")))
        tx2 = self.Transaction()
        tx2.date = date(2000, 6, 10)
        tx2.add_entry("assets.cash", self.Entry(CREDIT, Decimal("10.00")))

        q.add_transaction(tx1)
        q.add_transaction(tx2)

        self.assertEqual(len(q.transactions),2)

        self.assertEqual(
                q.accounts_delta.entries["assets.cash"],
                self.Entry(CREDIT,Decimal("20.00"))
            )


class TestBookYear(TestCase):
    def setUp(self):
        from ap.accounts.BookYear import BookYear
        self.BookYear = BookYear

        from ap.accounts.Transaction import Transaction
        self.Transaction = Transaction

        from ap.accounts.Entry import Entry
        self.Entry = Entry



    def tearDown(self):
        pass


    def test_bookyear(self):

        by = self.BookYear(2000)

        self.assertIsNotNone(by.quarters[1])
        self.assertIsNotNone(by.quarters[2])
        self.assertIsNotNone(by.quarters[3])
        self.assertIsNotNone(by.quarters[4])

        tx1 = self.Transaction()
        tx1.date = date(2000, 7, 10)
        tx1.add_entry("assets.cash", self.Entry(CREDIT, Decimal("10.00")))
        tx2 = self.Transaction()
        tx2.date = date(2000, 10, 10)
        tx2.add_entry("assets.cash", self.Entry(CREDIT, Decimal("10.00")))

        by.add_transaction(tx1)
        by.add_transaction(tx2)

        self.assertEqual(by.quarters[1].transactions.values()[0], tx1)
        self.assertEqual(by.quarters[2].transactions.values()[0], tx2)

        self.assertEqual(
                by.accounts_delta.entries["assets.cash"],
                self.Entry(CREDIT,Decimal("20.00"))
            )

class TestBook(TestCase):
    def setUp(self):
        from ap.accounts.Book import Book
        self.Book = Book

        from ap.accounts.BookYear import BookYear
        self.BookYear = BookYear

        from ap.accounts.Transaction import Transaction
        self.Transaction = Transaction

        from ap.accounts.Entry import Entry
        self.Entry = Entry
    def tearDown(self):
        pass

    def test_book(self):
        bk = self.Book()

        tx1 = self.Transaction()
        tx1.date = date(2000, 7, 10)
        tx1.add_entry("assets.cash", self.Entry(CREDIT, Decimal("10.00")))
        tx2 = self.Transaction()
        tx2.date = date(2001, 10, 10)
        tx2.add_entry("assets.cash", self.Entry(CREDIT, Decimal("10.00")))

        bk.add_transaction(tx1)
        bk.add_transaction(tx2)
        self.assertTrue(
                bk.accounts_delta,
                self.Entry(CREDIT,Decimal("20.00"))
            )

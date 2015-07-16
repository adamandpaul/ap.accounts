from unittest import TestCase
from ap.accounts import DEBIT, CREDIT, NEUTRAL
from decimal import Decimal

from datetime import date

class TestDirections(TestCase):
    def test_directions(self):
        from ap.accounts import CREDIT, DEBIT, NEUTRAL
        self.assertIsNotNone(DEBIT)
        self.assertIsNotNone(CREDIT)
        self.assertIsNotNone(NEUTRAL)
        self.assertNotEqual(DEBIT, CREDIT)
        self.assertNotEqual(DEBIT, NEUTRAL)
        self.assertNotEqual(CREDIT, NEUTRAL)


class TestEntry(TestCase):
    def setUp(self):
        from ap.accounts.Entry import Entry
        self.Entry = Entry


    def assertAddEntriesResult(self, a, b, t):
        r1 = a + b
        r2 = b + a
        self.assertEqual(r1, t)
        self.assertEqual(r2, t)


    def test_init_entry(self):
        e = self.Entry(DEBIT, Decimal("110.00"))
        self.assertIsNotNone(e)
        self.assertEqual(e.direction, DEBIT)
        self.assertEqual(e.amount, Decimal("110.00"))

        self.assertRaises(ValueError, self.Entry, NEUTRAL, Decimal("1.0"))

        eneg_debit = self.Entry(DEBIT, Decimal("-30.00"))
        self.assertEqual(eneg_debit.direction, CREDIT)
        self.assertEqual(eneg_debit.amount, Decimal("30.00"))

        eneg_credit = self.Entry(CREDIT, Decimal("-20.00"))
        self.assertEqual(eneg_credit.direction, DEBIT)
        self.assertEqual(eneg_credit.amount, Decimal("20.00"))


        ezero_debit = self.Entry(DEBIT, Decimal("0"))
        self.assertEqual(ezero_debit.direction, NEUTRAL)

        ezero_credit = self.Entry(CREDIT, Decimal("0"))
        self.assertEqual(ezero_credit.direction, NEUTRAL)



    def test_two_debits(self):
        a = self.Entry(DEBIT, Decimal("1.0"))
        b = self.Entry(DEBIT, Decimal("2.0"))
        t = self.Entry(DEBIT, Decimal("3.0"))
        self.assertAddEntriesResult(a, b, t)



    def test_two_credits(self):
        a = self.Entry(CREDIT, Decimal("1.0"))
        b = self.Entry(CREDIT, Decimal("2.0"))
        t = self.Entry(CREDIT, Decimal("3.0"))
        self.assertAddEntriesResult(a, b, t)



    def test_debit_and_smaller_credit(self):
        a = self.Entry(DEBIT, Decimal("10.0"))
        b = self.Entry(CREDIT, Decimal("1.0"))
        t = self.Entry(DEBIT, Decimal("9.0"))
        self.assertAddEntriesResult(a, b, t)

    def test_credit_and_smaller_debit(self):
        a = self.Entry(CREDIT, Decimal("10.0"))
        b = self.Entry(DEBIT, Decimal("1.0"))
        t = self.Entry(CREDIT, Decimal("9.0"))
        self.assertAddEntriesResult(a, b, t)



    def test_debit_and_larger_credit(self):
        a = self.Entry(CREDIT, Decimal("10.0"))
        b = self.Entry(DEBIT, Decimal("11.0"))
        t = self.Entry(DEBIT, Decimal("1.0"))
        self.assertAddEntriesResult(a, b, t)

    def test_credit_and_larger_debit(self):
        a = self.Entry(DEBIT, Decimal("10.0"))
        b = self.Entry(CREDIT, Decimal("11.0"))
        t = self.Entry(CREDIT, Decimal("1.0"))
        self.assertAddEntriesResult(a, b, t)


    def test_debit_and_credit_equal(self):
        a = self.Entry(DEBIT, Decimal("10.0"))
        b = self.Entry(CREDIT, Decimal("10.0"))
        t = self.Entry(NEUTRAL, Decimal("0.0"))
        self.assertAddEntriesResult(a, b, t)



    def test_debit_and_neutral(self):
        a = self.Entry(DEBIT, Decimal("10.0"))
        b = self.Entry(NEUTRAL, Decimal("0.0"))
        t = a
        self.assertAddEntriesResult(a, b, t)


    def test_credit_and_neutral(self):
        a = self.Entry(CREDIT, Decimal("10.0"))
        b = self.Entry(NEUTRAL, Decimal("0.0"))
        t = a
        self.assertAddEntriesResult(a, b, t)



    def test_neutral_and_neutral(self):
        a = self.Entry(NEUTRAL, Decimal("0.0"))
        b = a
        t = a
        self.assertAddEntriesResult(a, b, t)



    def tearDown(self):
        pass


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
        self.assertEqual(fy.start_year, 2010)
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



class TestQuarter(TestCase):
    def setUp(self):
        from ap.accounts.BookQuarter import BookQuarter
        from ap.accounts.Transaction import Transaction
        self.BookQuarter = BookQuarter
        self.Transaction = Transaction

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





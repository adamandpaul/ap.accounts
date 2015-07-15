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


class TestTransaction(TestCase):
    def setUp(self):
        from ap.accounts.Entry import Entry
        from ap.accounts.Transaction import Transaction
        self.Entry = Entry
        self.Transaction = Transaction

    def tearDown(self):
        pass

    def test_transaction_init (self):
        tx = self.Transaction()
        tx.description = "some description"
        tx.date = date(2000,01,01)
        self.assertEqual(tx.description, "some description")
        self.assertEqual(tx.date, date(2000,01,01))
        self.assertTrue (tx.balanced)


    def test_transaction_adding_entries (self):
        E = self.Entry
        tx = self.Transaction()

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
        tx = self.Transaction()

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
        tx = self.Transaction()

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





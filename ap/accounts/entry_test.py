# -*- coding: utf-8 -*-
"""Testing of the entry module"""

from unittest import TestCase
from ap.accounts.entry import DEBIT, CREDIT, NEUTRAL
from decimal import Decimal

from datetime import date

class TestDirections(TestCase):
    """Testing that the directions are indipendent non None values"""

    def test_directions(self):
        from ap.accounts.entry import CREDIT, DEBIT, NEUTRAL
        self.assertIsNotNone(DEBIT)
        self.assertIsNotNone(CREDIT)
        self.assertIsNotNone(NEUTRAL)
        self.assertNotEqual(DEBIT, CREDIT)
        self.assertNotEqual(DEBIT, NEUTRAL)
        self.assertNotEqual(CREDIT, NEUTRAL)


class TestEntry(TestCase):

    def setUp(self):
        super(TestEntry, self).setUp()
        from ap.accounts.entry import Entry
        self.Entry = Entry

    def test_init_entry(self):
        """Test that creating entries creates the correct properties"""

        e = self.Entry(DEBIT, Decimal("110.00"))
        self.assertIsNotNone(e)
        self.assertEqual(e.direction, DEBIT, "Expected a DEBIT direction as given in the Entry factory")
        self.assertEqual(e.amount, Decimal("110.00"), "Excpected 110.00 as given int the Entry factory")

        etxt = self.Entry(DEBIT, "110.00")
        self.assertIsNotNone(etxt)
        self.assertEqual(etxt.amount, Decimal("110.00"), "Excpected string input '110.00' to convert to a Decimal.")

        self.assertRaises(ValueError, self.Entry, NEUTRAL, "1.0", 
                "Expected a value error to be raised when a NEUTRAL direction yet non-zero amount is given in the Entry factory")

        eneg_debit = self.Entry(DEBIT, "-30.00")
        self.assertEqual(eneg_debit.direction, CREDIT, 
                "Expected a negitive amount to flip the direction from DEBIT to CREDIT")
        self.assertEqual(eneg_debit.amount, Decimal("30.00"), 
                "Expected a negitive amount to make the amount positive when creating an Entry")

        eneg_credit = self.Entry(CREDIT, "-20.00")
        self.assertEqual(eneg_credit.direction, DEBIT,
                "Expected a negitive amount to flip the direction from CREDIT to DEBIT")
        self.assertEqual(eneg_credit.amount, Decimal("20.00"),
                "Expected a negitive amount to make the amount positive when creating an Entry")

        ezero_debit = self.Entry(DEBIT, "0")
        self.assertEqual(ezero_debit.direction, NEUTRAL,
                "Expected a zero amount to change a DEBIT direction to a NEUTRAL one")

        ezero_credit = self.Entry(CREDIT, "0")
        self.assertEqual(ezero_credit.direction, NEUTRAL,
                "Expected a zero amount to change a CREDIT direction to a NEUTRAL one")

    def test_entry_str(self):

        Entry = self.Entry

        test_data = [
                (Entry(DEBIT, '11'), '11.00 DR'),
                (Entry(CREDIT, '11.00'), '11.00 CR'),
                (Entry(NEUTRAL, '0'), '0.00   '),
                ]

        for entry, expected_result in test_data:
            self.assertEqual(str(entry), expected_result, 'Expected {!r} to convert to str {}'.format(entry, expected_result))


    def test_entry_str(self):

        Entry = self.Entry

        test_data = [
                (Entry(DEBIT, '11'), '<Entry 11.00 DR>'),
                (Entry(CREDIT, '11.00'), '<Entry 11.00 CR>'),
                (Entry(NEUTRAL, '0'), '<Entry 0.00   >'),
                ]

        for entry, expected_result in test_data:
            self.assertEqual(repr(entry), expected_result, 'Expected {!r} to convert to str {}'.format(entry, expected_result))


    def test_entry_equality(self):
        """Tests that the __eq__ magic mthod works"""

        test_data = [(DEBIT, "0", DEBIT, "0"),
                     (NEUTRAL, "0", NEUTRAL, "0"),
                     (CREDIT, "0", CREDIT, "0"),
                     (DEBIT, "1", DEBIT, "1"),
                     (CREDIT, "1", CREDIT, "1"),

                     # Test where the direction gets changed or flipped
                     (DEBIT, "-1", DEBIT, "-1"),
                     (CREDIT, "-1", CREDIT, "-1"),
                     (NEUTRAL, "0", NEUTRAL, "0"), 
                     (DEBIT, "0", CREDIT, "0"),
                     (DEBIT, "0", NEUTRAL, "0"),
                     (CREDIT, "0", NEUTRAL, "0"),
                     (DEBIT, "1", CREDIT, "-1"), 
                     (DEBIT, "-1", CREDIT, "1"), ]

        for a_direction, a_amount, b_direction, b_amount in test_data:
            a = self.Entry(a_direction, a_amount)
            b = self.Entry(b_direction, b_amount)
            self.assertTrue(a == b, "Expected two identical entries to evaluate a == b to be true")
            self.assertEqual(a.amount, b.amount, "Expected two identical entries to have the same amount")
            self.assertEqual(a.direction, b.direction, "Expected two identiacl entries to have the same direction")


    def test_entry_inequality(self):
        """Tests that the __eq__ magic mthod works"""

        test_data = [(DEBIT, "1", DEBIT, "2"),
                     (CREDIT, "1", CREDIT, "2"),
                     (DEBIT, "1", NEUTRAL, "0"),
                     (CREDIT, "1", NEUTRAL, "0"),
                     (DEBIT, "1", CREDIT, "1"),

                     # Test where the direction gets changed or flipped
                     (DEBIT, "-1", DEBIT, "-1"),
                     (CREDIT, "-1", CREDIT, "-1"),]

        for a_direction, a_amount, b_direction, b_amount in test_data:
            a = self.Entry(a_direction, a_amount)
            b = self.Entry(b_direction, b_amount)
            self.assertFalse(a == b, "Expected two different entries to evaluate a == b to be false")
            self.assertTrue( (a.amount != b.amount) or (a.direction != b.direction),
                    "Expected that two different entries would differ on either amount or direction")

    def test_addition(self):

        test_data = [
                # test_name, a_direction, a_amount, b_direction, b_amount, expected_result_direction, expected_result_amount
                ('two_debits', DEBIT, "1.0", DEBIT, "2.0", DEBIT, "3.0"),
                ('two_credits', CREDIT, "1.0", CREDIT, "2.0", CREDIT, "3.0"),
                ('debit_and_smaller_credit', DEBIT, "10.0", CREDIT, "1.0", DEBIT, "9.0"),
                ('credit_and_smaller_debit', CREDIT, "10.0", DEBIT, "1.0", CREDIT, "9.0"),
                ('debit_and_larger_credit', CREDIT, "10.0", DEBIT, "11.0", DEBIT, "1.0"),
                ('credit_and_larger_debit', DEBIT, "10.0", CREDIT, "11.0", CREDIT, "1.0"),
                ('debit_and_credit_equal', DEBIT, "10.0", CREDIT, "10.0", NEUTRAL, "0.0"),
                ('debit_and_neutral', DEBIT, "10.0", NEUTRAL, "0.0", DEBIT, "10.0"),
                ('credit_and_neutral', CREDIT, "10.0", NEUTRAL, "0.0", CREDIT, "10.0"),
                ('neutral_and_neutral', NEUTRAL, "0.0", NEUTRAL, "0.0", NEUTRAL, "0.0"),
            ]

        for test_name, a_direction, a_amount, b_direction, b_amount, expected_result_direction, expected_result_amount in test_data:
            entry_a = self.Entry(a_direction, a_amount)
            entry_b = self.Entry(b_direction, b_amount)
            expected_result = self.Entry(expected_result_direction, expected_result_amount)

            result = entry_a + entry_b
            reverse_result = entry_b + entry_a

            self.assertEqual(result, expected_result, 'Addition faild for test data ' + test_name)
            self.assertEqual(reverse_result, expected_result, 'Reverse addition failed for test data ' + test_name)






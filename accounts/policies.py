# pylint: disable=import-error,missing-docstring,unused-argument

from decimal import Decimal
from ap.accounts.policy import policy
from ap.accounts.Entry import Entry
from ap.accounts import DEBIT, CREDIT




@policy(is_has=('inc-gst', 'purchase'))
def payed_gst_on_purchase(context, data):
    gst_payed = data["amount"]
    context.transaction.add_entry("liabilities.gst", Entry(DEBIT, gst_payed))
    context.transaction.add_entry("equity.retained_profets", Entry(CREDIT, gst_payed))

@payed_gst_on_purchase.test(payed_gst_on_purchase, {
    'amount': Decimal("11.00")
})
def test_payed_gst_on_purchase(context, data):
    assert context.transaction.entries["liabilities.gst"] == Entry(CREDIT, Decimal("1"))
    assert context.transaction.entries["equity.retained_profets"] == Entry(DEBIT, Decimal("1"))
    assert context.transaction.balanced





@policy(is_has=('cost-of-sales', 'purchase'))
def tax_cost_of_sales(context, data):
    context.transaction["tax.expense.cost-of-sales"] = data["amount"]


@policy(is_has=('purchase',))
def purchase(context, data):
    amount = data["amount"]
    context.transaction.add_entry("assets.cash", Entry(CREDIT, amount))
    context.transaction.add_entry("equity.retained_profets", Entry(DEBIT, amount))

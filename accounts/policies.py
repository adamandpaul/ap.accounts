

from ap.accounts.policy import policy


@policy(is_has=('inc-gst','purchase'))
def payed_gst_on_purchase(context, data):
    gst_payed = 234
    transaction.add_entry("liabilities.gst", Entry(DEBIT, gst_payed)
    transaction.add_entry("equity.retained_profets", Entry(CREDIT, gst_payed))


@policy(is_has=('cost-of-sales','purchase'))
def tax_cost_of_sales(context, data):
    context.transaction["tax.expense.cost-of-sales"] = data["amount"]


@policy(is_has=('purchase',))
def purchase(context, data):
    amount = data["amount"]
    transaction.add_entry("assets.cash", Entry(CREDIT, amount))
    transaction.add_entry("equity.retained_profets", Entry(DEBIT, amount))

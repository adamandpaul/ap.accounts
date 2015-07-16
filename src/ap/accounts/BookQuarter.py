


from ap.accounts.AccountsDelta import AccountsDelta
from ap.accounts.FinQuarter import FinQuarter

class BookQuarter(FinQuarter):
    

    @property
    def transactions(self):
        try:
            return self._transactions
        except AttributeError:
            self._transactions = {}
            return self._transactions

    @property
    def accounts_delta(self):
        delta = AccountsDelta()
        for tx in self.transactions.values():
            for account, entry in tx.entries.values():
                delta.add_entry(account, entry)
        return delta

    
    _counter = 0
    def construct_id (self, tx, suffix_tx_id=''):
        suffix_tx_id = suffix_tx_id or None
        self._counter += 1
        tx_id = "%s.%s" % (tx.date.isoformat(), self._counter)
        if suffix_tx_id is not None:
            tx_id = "%s.%s" % (tx_id, suffix_tx_id)

        if tx_id in self.transactions:
            raise RuntimeError()

        return tx_id

    def add_transaction (self, tx, suffix_tx_id=None):
        tx_id = self.construct_id(tx, suffix_tx_id)
        self.transactions[tx_id] = tx
        return tx_id



        

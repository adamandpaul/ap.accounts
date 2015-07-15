


from ap.accounts.AccountsDelta import AccountsDelta


class Quarter(object):


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

    


        

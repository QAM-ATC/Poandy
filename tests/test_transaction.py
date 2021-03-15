import pytest

from poandy.controller.transaction import TransactionController
from poandy.controller.account import AccountController

class TestTransactionController:
    account_id = AccountController.get_default_account_id()

    def test_get_transactions(self):
        transactions = TransactionController.get_transactions(self.account_id)
        assert isinstance(transactions, dict)
        assert "from" in transactions
        assert "to" in transactions
        assert "pageSize" in transactions
        assert "count" in transactions
        assert "pages" in transactions
        assert "lastTransactionID" in transactions

    def test_get_transaction(self):
        transaction = TransactionController.get_transaction(self.account_id,"1")
        assert isinstance(transaction, dict)
        assert "transaction" in transaction
        assert "lastTransactionID" in transaction
    
    def test_get_transactions_in_id_range(self):
        transactions = TransactionController.get_transactions_in_id_range(self.account_id, "1", "1")
        assert isinstance(transactions, dict)
        assert "transactions" in transactions
        assert "lastTransactionID" in transactions
    
    def test_get_transactions_since_id(self):
        transactions = TransactionController.get_transactions_since_id(self.account_id, "1")
        assert isinstance(transactions, dict)
        assert "transactions" in transactions
        assert "lastTransactionID" in transactions

    def test_stream_transactions(self):
        with TransactionController.stream_transactions(self.account_id) as stream_response:
            for line in stream_response.iter_lines():
                output = str(line)
                break
        assert output[0:2] == "b\'"

import pytest

from poandy.controller.account import AccountController


class TestAccountController:
    def test_get_accounts(self):
        accounts = AccountController.get_accounts()
        assert isinstance(accounts, dict)
        assert 'accounts' in accounts

    def test_get_default_account_id(self):
        account_id = AccountController.get_default_account_id()
        assert isinstance(account_id, str)
        assert len(account_id) == 20

    def test_get_account_details(self):
        account_id = AccountController.get_default_account_id()
        account_details = AccountController.get_account_details(account_id)
        assert isinstance(account_details, dict)
        assert 'account' in account_details
        assert 'lastTransactionID' in account_details

    def test_get_account_summary(self):
        account_id = AccountController.get_default_account_id()
        account_summary = AccountController.get_account_summary(account_id)
        assert isinstance(account_summary, dict)
        assert 'account' in account_summary
        assert 'lastTransactionID' in account_summary

    def test_get_tradeable_instruments(self):
        account_id = AccountController.get_default_account_id()
        tradeable_instruments = AccountController.get_tradeable_instruments(
            account_id)
        assert isinstance(tradeable_instruments, dict)
        assert 'instruments' in tradeable_instruments
        assert 'lastTransactionID' in tradeable_instruments

    def test_get_tradeable_instruments_one_instrument(self):
        account_id = AccountController.get_default_account_id()
        tradeable_instruments = AccountController.get_tradeable_instruments(
            account_id, instruments=['USB05Y_USD'])
        assert isinstance(tradeable_instruments, dict)
        assert 'instruments' in tradeable_instruments
        assert len(tradeable_instruments['instruments']) == 1
        assert 'lastTransactionID' in tradeable_instruments

    def test_get_tradeable_instruments_invalid(self):
        account_id = AccountController.get_default_account_id()
        with pytest.raises(Exception):
            tradeable_instruments = AccountController.get_tradeable_instruments(
                account_id, names_only=True, instruments=['USB05Y_USD'])

    def test_get_tradeable_instruments_names_only(self):
        account_id = AccountController.get_default_account_id()
        tradeable_instruments = AccountController.get_tradeable_instruments(
            account_id, names_only=True)
        assert isinstance(tradeable_instruments, list)

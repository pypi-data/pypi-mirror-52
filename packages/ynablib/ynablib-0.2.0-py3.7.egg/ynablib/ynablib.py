#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: ynablib.py
#
# Copyright 2019 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for ynablib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from requests import Session

from .ynablibexceptions import InvalidBudget, AuthenticationFailed

__author__ = '''Gary Hawker <dogfish@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''26-07-2019'''
__copyright__ = '''Copyright 2019, Gary Hawker, Costas Tyfoxylos'''
__credits__ = ["Gareth Hawker", "Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<costas.tyf@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''ynablib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Ynab:
    """Models the ynab service."""

    def __init__(self, token, url='https://api.youneedabudget.com'):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self._api_version = 'v1'
        self._base_url = url
        self._budgets = None
        self.api_url = f'{self._base_url}/{self._api_version}'
        self.session = self._get_authenticated_session(token)

    def _get_authenticated_session(self, token):
        self._logger.debug('Trying to authenticate with provided token.')
        budget_url = f'{self.api_url}/budgets'
        session = Session()
        headers = {'Authorization': f'Bearer {token}'}
        session.headers.update(headers)
        response = session.get(budget_url)
        if not response.ok:
            raise AuthenticationFailed(response.text)
        self._logger.debug('Successfully authenticated to YNAB.')
        return session

    @property
    def budgets(self):
        """Retrieves the budgets."""
        if self._budgets is None:
            budget_url = f'{self.api_url}/budgets'
            response = self.session.get(budget_url)
            if not response.ok:
                self._logger.error('Error retrieving budgets, response was : %s with status code : %s',
                                   response.text,
                                   response.status_code)
                return []
            self._budgets = [Budget(self, budget)
                             for budget in response.json().get('data', {}).get('budgets', [])]
        return self._budgets

    def get_budget_by_name(self, budget_name):
        """Retrieves a budget by it's name.

        Args:
            budget_name (str): The name of the budget to retrieve

        Returns:
            budget (Budget): A budget object on success, None otherwise

        """
        return next((budget for budget in self.budgets
                     if budget.name.lower() == budget_name.lower()), None)

    def get_accounts_for_budget(self, budget_name):
        """Retrieves the accounts for a budget.

        Args:
            budget_name (str): The budget's name to retrieve accounts for

        Returns:
            accounts (list): A list of accounts that belong to that budget

        """
        budget = self.get_budget_by_name(budget_name)
        if not budget:
            raise InvalidBudget(budget_name)
        return budget.accounts

    def upload_transactions(self, budget_id, payloads):
        """Uploads transaction payloads to YNAB.

        Args:
            budget_id (str): The budget id to upload to
            payloads (list): A list of transaction payloads as specified in
                https://api.youneedabudget.com/v1#/Transactions/createTransaction

        Returns:
            boolean (bool) : True on success, False otherwise

        """
        if not isinstance(payloads, (list, tuple, set)):
            payloads = [payloads]
        transaction_url = f'{self.api_url}/budgets/{budget_id}/transactions'
        response = self.session.post(transaction_url, json={"transactions": payloads})
        if not response.ok:
            self._logger.error('Unsuccessful attempt to upload to budget "%s", response was %s with status code %s',
                               budget_id,
                               response.text,
                               response.status_code)
        else:
            self._logger.info('Successfully uploaded %s transactions to budget "%s"', len(payloads), budget_id)
        return response.ok

    def refresh(self):
        """Cleans up the cached values for budgets."""
        for budget in self.budgets:
            budget.refresh()
        self._budgets = None


class Budget:
    """Models the YNAB budget object."""

    def __init__(self, ynab, data):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self._data = data
        self._ynab = ynab
        self._accounts = None

    @property
    def currency_format(self):
        """Currency format."""
        return self._data.get('currency_format')

    @property
    def date_format(self):
        """Date format."""
        return self._data.get('date_format')

    @property
    def first_month(self):
        """First month."""
        return self._data.get('first_month')

    @property
    def id(self):  # pylint: disable=invalid-name
        """ID."""
        return self._data.get('id')

    @property
    def last_modified_on(self):
        """Last modified on."""
        return self._data.get('last_modified_on')

    @property
    def last_month(self):
        """Last month."""
        return self._data.get('last_month')

    @property
    def name(self):
        """Name."""
        return self._data.get('name')

    @property
    def accounts(self):
        """Accounts of the budget."""
        if self._accounts is None:
            url = f'{self._ynab.api_url}/budgets/{self.id}/accounts'
            response = self._ynab.session.get(url)
            if not response.ok:
                self._logger.error('Error retrieving accounts, response was : %s with status code : %s',
                                   response.text,
                                   response.status_code)
                return []
            self._accounts = [Account(self, account)
                              for account in response.json().get('data', {}).get('accounts', [])]
        return self._accounts

    def get_account_by_name(self, name):
        """Retrieves an account by name.

        Args:
            name (str): The name of the account to retrieve

        Returns:
            account (Account): An account object on success, None otherwise.

        """
        return next((account for account in self.accounts
                     if account.name.lower() == name.lower()), None)

    def get_account_by_id(self, id_):
        """Retrieves an account by id.

        Args:
            id_ (str): The id of the account to retrieve

        Returns:
            account (Account): An account object on success, None otherwise.

        """
        return next((account for account in self.accounts
                     if account.id == id_), None)

    def refresh(self):
        """Cleans up the cached values for accounts."""
        self._accounts = None

    @property
    def transactions(self):
        """Transactions."""
        url = f'{self._ynab.api_url}/budgets/{self.id}/transactions'
        response = self._ynab.session.get(url)
        if not response.ok:
            self._logger.error('Error retrieving transactions, response was : %s with status code : %s',
                               response.text,
                               response.status_code)
            return []
        return [Transaction(self._ynab, transaction)
                for transaction in response.json().get('data', {}).get('transactions', [])]


class Account:
    """Models the account of a YNAB Budget."""

    def __init__(self, budget, data):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self._data = data
        self._budget = budget
        self._ynab = budget._ynab  # pylint: disable=protected-access

    @property
    def budget(self):
        """Budget."""
        return self._budget

    @property
    def balance(self):
        """Balance."""
        return self._data.get('balance')

    @property
    def cleared_balance(self):
        """Cleared balance."""
        return self._data.get('cleared_balance')

    @property
    def closed(self):
        """Closed."""
        return self._data.get('closed')

    @property
    def deleted(self):
        """Deleted."""
        return self._data.get('deleted')

    @property
    def id(self):  # pylint: disable=invalid-name
        """ID."""
        return self._data.get('id')

    @property
    def name(self):
        """Name."""
        return self._data.get('name')

    @property
    def note(self):
        """Note."""
        return self._data.get('note')

    @property
    def on_budget(self):
        """On budget."""
        return self._data.get('on_budget')

    @property
    def transfer_payee_id(self):
        """Transfer payee ID."""
        return self._data.get('transfer_payee_id')

    @property
    def type(self):
        """Type."""
        return self._data.get('type')

    @property
    def transactions(self):
        """Transactions."""
        url = f'{self._ynab.api_url}/budgets/{self.budget.id}/accounts/{self.id}/transactions'
        response = self._ynab.session.get(url)
        if not response.ok:
            self._logger.error('Error retrieving transactions, response was : %s with status code : %s',
                               response.text,
                               response.status_code)
            return []
        return [Transaction(self._ynab, transaction)
                for transaction in response.json().get('data', {}).get('transactions', [])]


class Transaction:
    """Models the transaction."""

    def __init__(self, ynab, data):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self._ynab = ynab
        self._data = data
        self._account = None

    @property
    def account(self):
        """Account."""
        if self._account is None:
            self._account = next((budget.get_account_by_id(self._data.get('account_id'))
                                  for budget in self._ynab.budgets),
                                 None)
        return self._account

    @property
    def account_id(self):
        """Account id."""
        return self.account.id

    @property
    def account_name(self):
        """Account name."""
        return self.account.name

    @property
    def amount(self):
        """Amount."""
        return self._data.get('amount')

    @property
    def is_approved(self):
        """Is approved."""
        return self._data.get('approved')

    @property
    def category_id(self):  # TODO implement category object here maybe?  pylint: disable=fixme
        """Category ID."""
        return self._data.get('category_id')

    @property
    def category_name(self):
        """Category name."""
        return self._data.get('category_name')

    @property
    def is_cleared(self):
        """Is cleared."""
        return self._data.get('cleared')

    @property
    def date(self):
        """Date."""
        return self._data.get('date')

    @property
    def is_deleted(self):
        """Is deleted."""
        return self._data.get('deleted')

    @property
    def flag_color(self):
        """Flag color."""
        return self._data.get('flag_color')

    @property
    def id(self):  # pylint: disable=invalid-name
        """ID."""
        return self._data.get('id')

    @property
    def import_id(self):
        """Import ID."""
        return self._data.get('import_id')

    @property
    def matched_transaction_id(self):
        """Matched transaction ID."""
        return self._data.get('matched_transaction_id')

    @property
    def memo(self):
        """Memo."""
        return self._data.get('memo')

    @property
    def payee_id(self):  # TODO implement payee object here maybe? pylint: disable=fixme
        """Payee ID."""
        return self._data.get('payee_id')

    @property
    def payee_name(self):
        """Payee name."""
        return self._data.get('payee_name')

    @property
    def subtransactions(self):
        """Subtransactions."""
        return self._data.get('subtransactions')

    @property
    def transfer_account_id(self):  # TODO implement transfer object here maybe? pylint: disable=fixme
        """Transfer account ID."""
        return self._data.get('transfer_account_id')

    @property
    def transfer_transaction_id(self):
        """Transfer transaction ID."""
        return self._data.get('transfer_transaction_id')

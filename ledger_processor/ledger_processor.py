#!/usr/bin/env python3

import csv
import datetime

from collections import defaultdict
from decimal import Decimal


class LedgerProcessor(object):
    def __init__(self, fobj):
        self._csv_reader = csv.DictReader(fobj)
        self._balances = defaultdict(self.create_opening_balance)
        self._validate_csv()

    def _validate_csv(self):
        if set(self._csv_reader.fieldnames) != set([
                'date', 'to', 'from', 'amount']):
            raise ValueError('CSV must have header row with fields: date, '
                             'to, from, amount')

    def get_balance(self, account, date):
        self._process_transactions_until(date)
        return self._balances[account]

    def get_all_balances(self, date):
        self._process_transactions_until(date)
        return self._balances

    @staticmethod
    def create_opening_balance():
        return Decimal('0.00')

    def _process_transactions_until(self, target_date):
        """
        Fast-forward through the ledger, processing transactions *before* the
        target date. Eg if you pass 2015-06-10 as the target date, process
        any transactions from 2015-06-09 but none from 2015-06-10.
        """
        if self._csv_reader is None:
            raise RuntimeError('The Ledger can only be used once; you must '
                               'create a new ledger.')

        assert isinstance(target_date, datetime.date)
        for (date, from_account, to_account, amount) in self._transactions():

            if date == target_date:
                break

            self._balances[from_account] -= amount
            self._balances[to_account] += amount

        self._csv_reader = None

    def _transactions(self):
        for row in self._csv_reader:
            yield (parse_date(row['date']), row['from'],
                   row['to'], Decimal(row['amount']))


def parse_date(date_string):
    (year_string, month_string, day_string) = date_string.split('-')
    return datetime.date(int(year_string), int(month_string), int(day_string))

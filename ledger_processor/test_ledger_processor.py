import datetime

from decimal import Decimal
from os.path import dirname, join as pjoin

from nose.tools import assert_equal, assert_raises

from .ledger_processor import LedgerProcessor

EXAMPLE_LEDGER_FILENAME = pjoin(dirname(__file__), 'example_ledger.csv')

TEST_CASES = [
    ('john', datetime.date(2015, 1, 16), Decimal('0.00')),
    ('mary', datetime.date(2015, 1, 16), Decimal('0.00')),
    ('supermarket', datetime.date(2015, 1, 16), Decimal('0.00')),
    ('insurance', datetime.date(2015, 1, 16), Decimal('0.00')),

    ('mary', datetime.date(2015, 1, 17), Decimal('125.00')),
    ('john', datetime.date(2015, 1, 17), Decimal('-125.00')),

    ('john', datetime.date(2015, 1, 18), Decimal('-145.00')),
    ('supermarket', datetime.date(2015, 1, 18), Decimal('20.00')),
    ('mary', datetime.date(2015, 1, 18), Decimal('25.00')),
    ('insurance', datetime.date(2015, 1, 18), Decimal('100.00')),
]


def test_get_balance():
    for account, test_date, expected_balance in TEST_CASES:
        yield _assert_balance_equal, account, test_date, expected_balance


def _assert_balance_equal(account, test_date, expected_balance):
    with open(EXAMPLE_LEDGER_FILENAME, 'r') as f:
        ledger = LedgerProcessor(f)
        got_balance = ledger.get_balance(account, test_date)

    assert_equal(expected_balance, got_balance)


def test_get_all_balances():
    with open(EXAMPLE_LEDGER_FILENAME, 'r') as f:
        ledger = LedgerProcessor(f)
        final_balances = ledger.get_all_balances(datetime.date(2015, 1, 18))

    expected_final_balances = {
        'john': Decimal('-145.00'),
        'mary': Decimal('25.00'),
        'supermarket': Decimal('20.00'),
        'insurance': Decimal('100.00'),
    }

    assert_equal(expected_final_balances, final_balances)


def test_ledger_cant_be_used_twice():
    with open(EXAMPLE_LEDGER_FILENAME, 'r') as f:
        ledger = LedgerProcessor(f)

        def use_ledger():
            ledger.get_all_balances(datetime.date(2015, 1, 18))

        use_ledger()
        assert_raises(RuntimeError, use_ledger)

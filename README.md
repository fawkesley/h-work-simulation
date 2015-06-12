# Work Simulation Exercise: Ledger

## Run tests

```
pip install nose
make test
```

## Example use of Ledger

```python
import datetime
from ledger_processor import LedgerProcessor

with open('ledger_processor/example_ledger.csv', 'r') as f:
    ledger_processor = LedgerProcessor(f)
    print(ledger_processor.get_all_balances(datetime.date(2015, 1, 16)))
```

Note that I took the liberty of adding a header row to the example ledger CSV:

```
date,from,to,amount
```


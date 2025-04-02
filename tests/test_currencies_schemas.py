import datetime

import pytest

from app.api.schemas.currencies import (
    ConvertedCurrencies,
    CurrenciesToExchange,
    CurrencyFromDB,
    CurrencyToDB,
    CurrencyWithRates,
    RateFromDB,
)


def test_currencies_to_exchange_model():
    currencies_to_exchange = CurrenciesToExchange(from_currency_code="USD", to_currency_code="EUR", count=10)

    assert currencies_to_exchange.from_currency_code == "USD"
    assert currencies_to_exchange.to_currency_code == "EUR"
    assert currencies_to_exchange.count == 10
    with pytest.raises(ValueError):
        CurrenciesToExchange(from_currency_code="USD", to_currency_code="EUR", count=-1)


def test_converted_currencies_model():
    converted_currencies = ConvertedCurrencies(from_currency_code="USD", to_currency_code="EUR", count=10, value=12.5)

    assert converted_currencies.from_currency_code == "USD"
    assert converted_currencies.to_currency_code == "EUR"
    assert converted_currencies.count == 10
    assert converted_currencies.value == 12.5


def test_currency_to_db_model():
    currency_to_db = CurrencyToDB(name="US Dollar", code="USD")

    assert currency_to_db.name == "US Dollar"
    assert currency_to_db.code == "USD"

    with pytest.raises(ValueError):
        CurrencyToDB(name="US Dollar")


def test_currency_from_db_model():
    currency_from_db = CurrencyFromDB(id=1, name="US Dollar", code="USD")

    assert currency_from_db.id == 1
    assert currency_from_db.name == "US Dollar"
    assert currency_from_db.code == "USD"


def test_currency_with_rates_model():
    rate1 = RateFromDB(id=1, currency_id=1, rate=1.0, updated_at=datetime.datetime(2023, 10, 28, 12, 0, 0))
    rate2 = RateFromDB(id=2, currency_id=1, rate=1.2, updated_at=datetime.datetime(2023, 10, 28, 12, 30, 0))

    currency_with_rates = CurrencyWithRates(id=1, name="US Dollar", code="USD", rates=[rate1, rate2])

    assert currency_with_rates.id == 1
    assert currency_with_rates.name == "US Dollar"
    assert currency_with_rates.code == "USD"
    assert len(currency_with_rates.rates) == 2
    assert currency_with_rates.rates[0] == rate1
    assert currency_with_rates.rates[1] == rate2

    with pytest.raises(ValueError):
        CurrencyWithRates(name="US Dollar", code="USD", rates=[rate1, rate2])

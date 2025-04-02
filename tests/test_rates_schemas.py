import datetime

import pytest

from app.api.schemas.rates import RateFromAPI, RateFromDB, RatesUpdateStatus


def test_rate_from_db_model():
    rate_db = RateFromDB(id=1, currency_id=2, rate=1.0, updated_at=datetime.datetime(2023, 10, 28, 12, 0, 0))

    assert rate_db.id == 1
    assert rate_db.currency_id == 2
    assert rate_db.rate == 1.0
    assert rate_db.updated_at == datetime.datetime(2023, 10, 28, 12, 0, 0)

    with pytest.raises(ValueError):
        RateFromDB(currency_id=2, rate=1.0, updated_at=datetime.datetime(2023, 10, 28, 12, 0, 0))


def test_rates_update_status_model():
    status = RatesUpdateStatus(status=True, updated_at=datetime.datetime(2023, 10, 28, 12, 0, 0))

    assert status.status is True
    assert status.updated_at == datetime.datetime(2023, 10, 28, 12, 0, 0)


def test_rate_from_api_model():
    rate_api = RateFromAPI(updated_at=datetime.datetime(2023, 10, 28, 12, 0, 0), rate=1.0, currency="USD")

    assert rate_api.currency == "USD"
    assert rate_api.rate == 1.0
    assert rate_api.updated_at == datetime.datetime(2023, 10, 28, 12, 0, 0)

    with pytest.raises(ValueError):
        RateFromAPI(updated_at=datetime.datetime(2023, 10, 28, 12, 0, 0), rate=1.0)

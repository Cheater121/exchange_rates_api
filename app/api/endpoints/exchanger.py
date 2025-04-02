import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError

from app.api.dependencies.dependencies import get_currency_service, get_rate_service
from app.api.schemas.currencies import CurrenciesToExchange, ConvertedCurrencies, CurrencyToDB
from app.api.schemas.rates import RatesUpdateStatus, RateFromAPI, RatesLastUpdateResponse
from app.services.currencies import CurrencyService
from app.services.network import NetworkServiceV2
from app.services.rate import RateService

router = APIRouter(
    prefix="/api",
    tags=["Currency exchange"],
)


@router.get("/update_rates", response_model=RatesUpdateStatus)
async def update_rates(currency_service: CurrencyService = Depends(get_currency_service),
                       rate_service: RateService = Depends(get_rate_service)):
    currencies_list: list[CurrencyToDB] = await NetworkServiceV2().fetch_currencies()
    rates_list: list[RateFromAPI] = await NetworkServiceV2().fetch_rates()

    for currency in currencies_list:
        try:
            await currency_service.add_currency(currency)
        except IntegrityError:
            pass
    for rate in rates_list:
        await rate_service.add_rate(rate)
        updated_at: datetime.datetime = rate.updated_at
    return {"status": True, "updated_at": updated_at}


@router.get("/last_update", response_model=RatesLastUpdateResponse)
async def get_last_update_datetime(rate_service: RateService = Depends(get_rate_service)):
    max_datetime = await rate_service.get_max_datetime()
    return {"updated_at": max_datetime}


@router.post("/convert", response_model=ConvertedCurrencies)
async def convert_currencies(currencies_to_exchange: CurrenciesToExchange,
                             currency_service: CurrencyService = Depends(get_currency_service)):
    converted_currencies = await currency_service.convert_currencies(currencies_to_exchange)
    return converted_currencies

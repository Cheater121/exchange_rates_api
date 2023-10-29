import datetime

from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

from app.api.dependencies.dependencies import UOWDep
from app.api.schemas.currencies import CurrenciesToExchange, ConvertedCurrencies, CurrencyToDB
from app.api.schemas.rates import RatesUpdateStatus, RateFromAPI, RatesLastUpdateResponse
from app.services.currencies import CurrencyService
from app.services.network import NetworkService
from app.services.rate import RateService

router = APIRouter(
    prefix="/api",
    tags=["Currency exchange"],
)


@router.get("/update_rates", response_model=RatesUpdateStatus)
async def update_rates(uow: UOWDep):
    currencies_list: list[CurrencyToDB] = await NetworkService().fetch_currencies()
    rates_list: list[RateFromAPI] = await NetworkService().fetch_rates()

    for currency in currencies_list:
        try:
            await CurrencyService().add_currency(uow, currency)
        except IntegrityError:
            pass
    for rate in rates_list:
        await RateService().add_rate(uow, rate)
        updated_at: datetime.datetime = rate.updated_at
    return {"status": True, "updated_at": updated_at}


@router.get("/last_update", response_model=RatesLastUpdateResponse)
async def get_last_update_datetime(uow: UOWDep):
    max_datetime = await RateService().get_max_datetime(uow)
    return {"updated_at": max_datetime}


@router.post("/convert", response_model=ConvertedCurrencies)
async def convert_currencies(uow: UOWDep, currencies_to_exchange: CurrenciesToExchange):
    converted_currencies = await CurrencyService().convert_currencies(uow, currencies_to_exchange)
    return converted_currencies


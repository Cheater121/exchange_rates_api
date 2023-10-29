import datetime

from sqlalchemy.exc import NoResultFound

from app.api.schemas.currencies import CurrencyFromDB
from app.api.schemas.rates import RateFromAPI, RateFromDB
from app.utils.unitofwork import IUnitOfWork


class RateService:
    async def add_rate(self, uow: IUnitOfWork, rate: RateFromAPI) -> int | None:
        rate_dict: dict = rate.model_dump()
        async with uow:
            try:
                currency: CurrencyFromDB = await uow.currency.find_one(code=rate.currency)
            except NoResultFound:
                return

            rate_dict.pop("currency")
            rate_dict.update({"currency_id": currency.id})

            rate_id_from_db = await uow.rate.add_one(rate_dict)
            await uow.commit()
            return rate_id_from_db

    async def get_rate(self, uow: IUnitOfWork, code: str) -> RateFromDB:
        async with uow:
            rate = await uow.rate.find_one(code=code)
            return rate

    async def get_max_datetime(self, uow: IUnitOfWork) -> datetime.datetime:
        async with uow:
            max_datetime = await uow.rate.find_max_field("updated_at")
            return max_datetime

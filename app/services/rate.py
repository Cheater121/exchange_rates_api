import datetime

from sqlalchemy.exc import NoResultFound

from app.api.schemas.currencies import CurrencyFromDB
from app.api.schemas.rates import RateFromAPI, RateFromDB
from app.utils.unitofwork import IUnitOfWork


class RateService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_rate(self, rate: RateFromAPI) -> int | None:
        rate_dict: dict = rate.model_dump()
        async with self.uow as uow:
            try:
                currency: CurrencyFromDB = await uow.currency.find_one(code=rate.currency)
            except NoResultFound:
                return None

            rate_dict.pop("currency")
            rate_dict.update({"currency_id": currency.id})

            rate_id_from_db = await uow.rate.add_one(rate_dict)
            await uow.commit()
            return rate_id_from_db

    async def get_rate(self, code: str) -> RateFromDB:
        async with self.uow as uow:
            rate = await uow.rate.find_one(code=code)
            return rate

    async def get_max_datetime(self) -> datetime.datetime:
        async with self.uow as uow:
            max_datetime = await uow.rate.find_max_field("updated_at")
            return max_datetime

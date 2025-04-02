from fastapi import Depends

from app.services.currencies import CurrencyService
from app.services.rate import RateService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork


async def get_currency_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> CurrencyService:
    return CurrencyService(uow)


async def get_rate_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> RateService:
    return RateService(uow)

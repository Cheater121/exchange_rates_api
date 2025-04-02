from abc import ABC, abstractmethod
from typing import Type

from app.db.database import async_session_maker
from app.repositories.currencies import CurrencyRepository
from app.repositories.rates import RateRepository


class IUnitOfWork(ABC):
    currency: Type[CurrencyRepository]
    rate: Type[RateRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.currency = CurrencyRepository(self.session)
        self.rate = RateRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

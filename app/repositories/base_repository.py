from abc import ABC, abstractmethod

from sqlalchemy import insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_max_field(self, field_name: str):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_max_field(self, field_name: str):
        max_field = func.max(getattr(self.model, field_name))
        stmt = select(max_field).limit(1)
        res = await self.session.execute(stmt)
        max_row = res.scalar_one()
        return max_row

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one().to_pydantic_model()
        return res

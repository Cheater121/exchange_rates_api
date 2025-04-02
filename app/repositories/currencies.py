from sqlalchemy import select, text
from sqlalchemy.orm import selectinload

from app.api.schemas.currencies import CurrencyWithRates
from app.db.models import Currency
from app.repositories.base_repository import SQLAlchemyRepository


class CurrencyRepository(SQLAlchemyRepository):
    model = Currency

    async def find_latest_rate(self, code: str):
        """This method will find by currency code one currency with joined latest rate and return rate"""
        query = """
                SELECT
                    currency.id AS currency_id,
                    currency.name AS currency_name,
                    currency.code AS currency_code,
                    rate.id AS rate_id,
                    rate.rate AS rate_value,
                    rate.updated_at AS rate_updated_at
                FROM
                    currency
                JOIN (
                    SELECT
                        rate.currency_id,
                        MAX(rate.updated_at) AS max_updated_at
                    FROM
                        rate
                    GROUP BY
                        rate.currency_id
                    ) AS max_rates
                ON currency.id = max_rates.currency_id
                JOIN rate
                ON rate.currency_id = max_rates.currency_id
                    AND rate.updated_at = max_rates.max_updated_at
                WHERE
                    currency.code = :code;
                """
        res = await self.session.execute(text(query).bindparams(code=code))
        row = res.fetchone()
        if row:
            rate = row[4]
            return rate

    async def find_one_with_nested_rates(self, code: str):
        """This method will find one currency by code with all nested rates and return pydandtic model of it"""
        query = select(self.model).filter_by(code=code).options(selectinload(self.model.rates))
        res = await self.session.execute(query)
        db_model = res.scalar_one()
        pydantic_model = CurrencyWithRates.model_validate(db_model)
        # ToDo datetime filter by updated_at field of nested models, which returns latest rate?
        return pydantic_model

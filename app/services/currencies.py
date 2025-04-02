from app.api.schemas.currencies import ConvertedCurrencies, CurrenciesToExchange, CurrencyFromDB, CurrencyToDB
from app.errors.exceptions import BadCurrencyCode, CurrencyZeroRate
from app.utils.unitofwork import IUnitOfWork


class CurrencyService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_currency(self, currency: CurrencyToDB) -> int:
        currency_dict: dict = currency.model_dump()
        async with self.uow as uow:
            currency_id_from_db = await uow.currency.add_one(currency_dict)
            await uow.commit()
            return currency_id_from_db

    async def get_currency(self, code: str) -> CurrencyFromDB:
        async with self.uow as uow:
            currency = await uow.currency.find_one(code=code)
            return currency

    async def convert_currencies(self, currencies_to_exchange: CurrenciesToExchange) -> ConvertedCurrencies:
        async with self.uow as uow:
            from_currency_rate = await uow.currency.find_latest_rate(currencies_to_exchange.from_currency_code)
            to_currency_rate = await uow.currency.find_latest_rate(currencies_to_exchange.to_currency_code)

            try:
                if from_currency_rate and to_currency_rate:
                    value = to_currency_rate / from_currency_rate * currencies_to_exchange.count
                else:
                    raise BadCurrencyCode
            except ZeroDivisionError:
                raise CurrencyZeroRate

            return ConvertedCurrencies(
                from_currency_code=currencies_to_exchange.from_currency_code,
                to_currency_code=currencies_to_exchange.to_currency_code,
                count=currencies_to_exchange.count,
                value=value,
            )

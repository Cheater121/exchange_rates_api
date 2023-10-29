from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.rates import RateFromDB


class CurrenciesToExchange(BaseModel):
    from_currency_code: str
    to_currency_code: str
    count: float = Field(gt=0, description="The count must be greater than zero")


class ConvertedCurrencies(CurrenciesToExchange):
    value: float


class CurrencyToDB(BaseModel):
    name: str
    code: str


class CurrencyFromDB(CurrencyToDB):
    id: int


class CurrencyWithRates(CurrencyFromDB):
    model_config = ConfigDict(from_attributes=True)

    rates: list[RateFromDB]

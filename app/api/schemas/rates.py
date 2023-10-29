import datetime

from pydantic import BaseModel, ConfigDict


class RateFromDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    currency_id: int
    rate: float
    updated_at: datetime.datetime


class RatesLastUpdateResponse(BaseModel):
    updated_at: datetime.datetime | None


class RatesUpdateStatus(RatesLastUpdateResponse):
    status: bool


class RateFromAPI(BaseModel):
    updated_at: datetime.datetime
    rate: float
    currency: str

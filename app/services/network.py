import datetime

import aiohttp

from app.api.schemas.currencies import CurrencyToDB
from app.api.schemas.rates import RateFromAPI
from app.core.config import settings
from app.errors.exceptions import ExternalApiException


class NetworkService:
    def __init__(self):
        self.base_url = "http://api.exchangeratesapi.io/v1/"
        self.path_currencies = "symbols"
        self.path_rates = "latest"
        self.api_key = settings.EXCHANGE_API_KEY

    def _create_url(self, path: str) -> str:
        url = f"{self.base_url}{path}?access_key={self.api_key}"
        return url

    @staticmethod
    async def _fetch_data(url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if response.status == 200:
                    return data
                else:
                    raise ExternalApiException(status_code=response.status, detail=data)

    async def fetch_currencies(self) -> list[CurrencyToDB]:
        url: str = self._create_url(self.path_currencies)
        data: dict = await self._fetch_data(url)
        if data.get("symbols"):
            currencies = []
            for code, name in data["symbols"].items():
                currencies.append(CurrencyToDB(code=code,
                                               name=name))
            return currencies

    async def fetch_rates(self) -> list[RateFromAPI]:
        url: str = self._create_url(self.path_rates)
        data: dict = await self._fetch_data(url)
        if data.get("rates"):
            rates = []
            now = datetime.datetime.utcnow()
            for currency, rate in data["rates"].items():
                rates.append(RateFromAPI(currency=currency,
                                         rate=rate,
                                         updated_at=now))
            return rates

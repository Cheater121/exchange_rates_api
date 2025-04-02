import datetime

import aiohttp

from app.api.schemas.currencies import CurrencyToDB
from app.api.schemas.rates import RateFromAPI
from app.core.config import settings
from app.errors.exceptions import ExternalApiException


class NetworkServiceV1:
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

    async def fetch_currencies(self) -> list[CurrencyToDB] | None:
        url: str = self._create_url(self.path_currencies)
        data: dict = await self._fetch_data(url)
        if data.get("symbols"):
            currencies = []
            for code, name in data["symbols"].items():
                currencies.append(CurrencyToDB(code=code, name=name))
            return currencies

    async def fetch_rates(self) -> list[RateFromAPI] | None:
        url: str = self._create_url(self.path_rates)
        data: dict = await self._fetch_data(url)
        if data.get("rates"):
            rates = []
            now = datetime.datetime.utcnow()
            for currency, rate in data["rates"].items():
                rates.append(RateFromAPI(currency=currency, rate=rate, updated_at=now))
            return rates


class NetworkServiceV2:
    def __init__(self):
        self.base_url = "https://api.apilayer.com/currency_data/"
        self.path_currencies = "list"
        self.path_rates = "live"
        self.api_key = settings.EXCHANGE_API_KEY

    def _create_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    async def _fetch_data(self, url: str) -> dict:
        headers = {"apikey": self.api_key}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()

                if response.status == 200 and data.get("success", False):
                    return data
                else:
                    error_info = data.get("error", {}).get("info", data)
                    raise ExternalApiException(status_code=response.status, detail=error_info)

    async def fetch_currencies(self) -> list[CurrencyToDB] | None:
        url = self._create_url(self.path_currencies)
        data = await self._fetch_data(url)

        if currencies := data.get("currencies"):
            return [CurrencyToDB(code=code, name=name) for code, name in currencies.items()]
        return None

    async def fetch_rates(self) -> list[RateFromAPI] | None:
        url = self._create_url(self.path_rates)
        data = await self._fetch_data(url)

        if quotes := data.get("quotes"):
            source_currency = data.get("source", "USD")
            timestamp = data.get("timestamp")
            updated_at = datetime.datetime.fromtimestamp(timestamp) if timestamp else datetime.datetime.utcnow()

            rates = []
            for quote, rate in quotes.items():
                if len(quote) != 6 or not quote.startswith(source_currency):
                    continue

                target_currency = quote[len(source_currency) :]
                rates.append(RateFromAPI(currency=target_currency, rate=rate, updated_at=updated_at))

            return rates
        return None

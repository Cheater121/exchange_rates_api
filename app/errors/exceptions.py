from fastapi import HTTPException


class ExternalApiException(HTTPException):
    def __init__(self, detail: str = "Something went wrong on external service", status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)


class BadCurrencyCode(HTTPException):
    def __init__(self, detail: str = "Bad user request (maybe bad currency codes)", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class CurrencyZeroRate(HTTPException):
    def __init__(self, detail: str = "One of currency rates is zero (division by zero)", status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)

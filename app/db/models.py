import datetime

from sqlalchemy import BigInteger, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.schemas.currencies import CurrencyFromDB
from app.api.schemas.rates import RateFromDB
from app.db.database import Base


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    code: Mapped[str] = mapped_column(unique=True)

    rates = relationship("Rate", back_populates="currency", cascade="all, delete-orphan")

    def to_pydantic_model(self) -> CurrencyFromDB:
        return CurrencyFromDB(
            id=self.id,
            name=self.name,
            code=self.code
        )


class Rate(Base):
    __tablename__ = "rate"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    currency_id: Mapped[int] = mapped_column(BigInteger,
                                             ForeignKey("currency.id", ondelete="CASCADE"),
                                             nullable=True)
    rate: Mapped[float]
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                          onupdate=datetime.datetime.utcnow)

    currency = relationship("Currency", back_populates="rates")

    def to_pydantic_model(self) -> RateFromDB:
        return RateFromDB(
            id=self.id,
            currency_id=self.currency_id,
            rate=self.rate,
            datetime=self.updated_at
        )

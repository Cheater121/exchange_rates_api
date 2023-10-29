from app.db.models import Rate
from app.repositories.base_repository import SQLAlchemyRepository


class RateRepository(SQLAlchemyRepository):
    model = Rate

from sqlalchemy.orm import Mapped
from db.database import intpk
from db.models.base import Base

class Channel(Base):
    __tablename__ = "channel"

    id: Mapped[intpk]
    name: Mapped[str]

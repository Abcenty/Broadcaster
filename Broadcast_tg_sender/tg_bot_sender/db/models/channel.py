from uuid import UUID
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped
from db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Channel(Base):
    __tablename__ = "channel"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str]

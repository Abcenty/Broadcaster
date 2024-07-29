from uuid import UUID
from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from db.database import intpk
from db.models.base import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    username: Mapped[str] = mapped_column(String(128), nullable=False)
    access: Mapped[bool] = mapped_column(default=False)
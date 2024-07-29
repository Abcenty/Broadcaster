from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Uuid
from uuid import UUID
from db.models.base import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    username: Mapped[str] = mapped_column(String(128), nullable=False)
    access: Mapped[bool] = mapped_column(default=False)
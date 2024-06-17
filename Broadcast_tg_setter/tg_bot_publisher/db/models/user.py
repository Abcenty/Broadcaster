from sqlalchemy.orm import Mapped, mapped_column
from db.database import intpk
from db.models.base import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str]
    access: Mapped[bool] = mapped_column(default=False)
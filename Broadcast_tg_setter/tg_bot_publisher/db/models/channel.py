from uuid import UUID
from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, relationship
from db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class ChannelChannelGroups(Base):
    __tablename__ = "channel_channel_groups"

    channel_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('channel.id'), primary_key=True)
    channel_group_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('channel_groups.id'), primary_key=True)


class ChannelGroups(Base):
    __tablename__ = "channel_groups"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    channels: Mapped[list["Channel"]] = relationship(
        back_populates="channel_groups", # ссылка на поле в модели с которой связываемся
        secondary="channel_channel_groups", # ссылка на модель зависимостей
    )
    
class Channel(Base):
    __tablename__ = "channel"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    channel_groups: Mapped[list["ChannelGroups"]] = relationship(
        back_populates="channels", # ссылка на поле в модели с которой связываемся
        secondary="channel_channel_groups", # ссылка на модель зависимостей
    )

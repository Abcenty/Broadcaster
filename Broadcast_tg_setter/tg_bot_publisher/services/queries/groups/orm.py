from sqlalchemy import select, update
from db.database import session_factory
from db.models.channel import ChannelGroups
from services.queries.base import BaseService


class ChannelGroupGateway(BaseService):
    @staticmethod
    def list():
        with session_factory() as session:
            query = select(ChannelGroups) 
            result = session.execute(query)
            scalars = result.scalars().all()
            return [channel_group for channel_group in scalars]
         
    @staticmethod
    def get(name: str):
        with session_factory() as session:
            query = select(ChannelGroups).where(ChannelGroups.name == name) 
            result = session.execute(query)
            channel_group = result.scalar()
            return channel_group
        
    def create(self, name: str):
        with session_factory() as session:
            session.add(ChannelGroups(name=name, id=self.generate_id()))
            session.commit()
            
    @staticmethod
    def delete(name: str):
        with session_factory() as session:
            query = session.query(ChannelGroups).filter(ChannelGroups.name == name).first()
            session.delete(query)
            session.commit()
            
    @staticmethod   
    def update(name: str, channels: str, update_type: str) -> None:
        channels_list = channels.split(';')
        query = (
            update(ChannelGroups)
            .where(ChannelGroups.name == name)
            .values(
                funnel_id=client.funnel_id,
                points=client.points,
                username=client.username,
                bonus_modificator=client.bonus_modificator,
            )
        )

        await self.session.execute(query)


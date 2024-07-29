from sqlalchemy import select
from db.database import session_factory
from db.models.channel import Channel
from services.queries.base import BaseService


class ChannelGateway(BaseService):
    @staticmethod
    def list():
        with session_factory() as session:
            query = select(Channel) 
            result = session.execute(query)
            scalars = result.scalars().all()
            return [channel for channel in scalars]
         
    @staticmethod
    def get(name: str):
        with session_factory() as session:
            query = select(Channel).where(Channel.name == name) 
            result = session.execute(query)
            channel = result.scalar()
            return channel
        
    def create(self, name: str):
        with session_factory() as session:
            session.add(Channel(name=name, id=self.generate_id()))
            session.commit()
            
    @staticmethod
    def delete(name: str):
        with session_factory() as session:
            session.delete(Channel(name=name))
            session.commit()

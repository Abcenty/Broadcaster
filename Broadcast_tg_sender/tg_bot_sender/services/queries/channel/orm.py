from sqlalchemy import select
from db.database import session_factory
from db.models.channel import Channel


class ChannelGateway:
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
        
    @staticmethod
    def create(name: str):
        with session_factory() as session:
            session.add(Channel(name=name))
            session.commit()

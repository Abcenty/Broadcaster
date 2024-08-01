from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from db.database import session_factory
from db.models.channel import ChannelGroups, ChannelChannelGroups, Channel
from services.queries.base import BaseService

class ChannelGroupGateway(BaseService):
    @staticmethod
    def get_list():
        with session_factory() as session:
            query = select(ChannelGroups) 
            result = session.execute(query)
            scalars = result.scalars().all()
            return [channel_group for channel_group in scalars]
         
    @staticmethod
    def get(name: str):
        with session_factory() as session:
            query = select(ChannelGroups).where(ChannelGroups.name == name).options(selectinload(ChannelGroups.channels))
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
            
    # update_type может принимать значения: 'change_name', 'add_channels', 'delete_channels'
    @staticmethod          
    def update(name: str, update_type: str, new_name: str | None = None, channels: list[str] | None = None) -> None: 
        with session_factory() as session:
            if update_type == 'change_name':
                query = (
                    update(ChannelGroups)
                    .where(ChannelGroups.name == name)
                    .values(
                        name=new_name,
                    )
                )
                session.execute(query)
            if update_type == 'add_channels':
                channels_query = select(Channel.id).filter(Channel.name.in_(channels))
                group_query = select(ChannelGroups.id).filter(ChannelGroups.name == name)
                channel_ids = session.execute(channels_query).scalars().all()
                group = session.execute(group_query).scalars().first()
                for channel in channel_ids:
                    try:
                        session.add(ChannelChannelGroups(channel_id=channel, channel_group_id=group))
                    except:
                        continue
            if update_type == 'delete_channels':
                channels_query = select(Channel.id).filter(Channel.name.in_(channels))
                group_query = select(ChannelGroups.id).filter(ChannelGroups.name == name)
                channel_ids = session.execute(channels_query).scalars().all()
                group = session.execute(group_query).scalars().first()
                for channel in channel_ids:
                    try:
                        query = session.query(ChannelChannelGroups).filter(
                            ChannelChannelGroups.channel_id == channel,
                            ChannelChannelGroups.channel_group_id == group).first()
                        session.delete(query)
                    except:
                        continue
            session.commit()

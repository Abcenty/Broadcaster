from sqlalchemy import select
from db.database import session_factory
from db.models.user import Users
from services.queries.base import BaseService


class UserGateway(BaseService):
    @staticmethod
    def list():
        with session_factory() as session:
            query = select(Users) 
            result = session.execute(query)
            scalars = result.scalars().all()
            return [user for user in scalars]
         
    @staticmethod
    def get(username: str):
        with session_factory() as session:
            query = select(Users).where(Users.username == username) 
            result = session.execute(query)
            user = result.scalar()
            return user
        
    @staticmethod
    def get_accessed(username: str):
        with session_factory() as session:
            query = select(Users).where(Users.username == username, Users.access == True)
            result = session.execute(query)
            user = result.scalar()
            return user
        
    def create(self, username: str):
        with session_factory() as session:
            session.add(Users(username=username, id=self.generate_id()))
            session.commit()

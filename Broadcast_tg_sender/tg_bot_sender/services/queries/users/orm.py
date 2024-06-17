from sqlalchemy import select
from db.database import session_factory
from db.models.user import Users


class UserGateway:
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
        
    @staticmethod
    def create(username: str):
        with session_factory() as session:
            session.add(Users(username=username))
            session.commit()

from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config_data.config import settings
from sqlalchemy.orm import mapped_column
# from sqlalchemy.ext.declarative import declarative_base

# создаем синхронный движок, который будет создавать подключения к базе данных
sync_engine = create_engine(
    url=settings.postgres.DATABASE_URL_psycopg, # 
    echo=False, # возврат логов в консоль
    pool_size=5, # количество одновременных подключений к базе (одновремененных запросов)
    max_overflow=10, # пороговое количество одновременных подключений
)

session_factory = sessionmaker(sync_engine)

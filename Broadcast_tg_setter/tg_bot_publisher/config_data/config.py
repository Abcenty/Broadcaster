from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    
    
@dataclass
class RabbitMQ:
    AMQP_USER: str
    AMQP_PASS: str
    AMQP_HOST: str
    

@dataclass
class Postgres:
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

@dataclass
class S3Client:
    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str


@dataclass
class Config:
    tg_bot: TgBot
    postgres: Postgres
    rabbit_mq: RabbitMQ
    sender: str
    s3_client: S3Client
    




def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
                      token=env('BOT_TOKEN'),
                    ),
                  postgres=Postgres(
                      DB_HOST=env('DB_HOST'),
                      DB_PORT=env('DB_PORT'),
                      DB_USER=env('DB_USER'),
                      DB_PASS=env('DB_PASS'),
                      DB_NAME=env('DB_NAME'),
                    ),
                  rabbit_mq=RabbitMQ(
                      AMQP_USER=env('AMQP_USER'),
                      AMQP_PASS=env('AMQP_PASS'),
                      AMQP_HOST=env('AMQP_HOST'),
                    ),
                  sender=env('SENDER'),
                  s3_client=S3Client(
                      access_key=env('S3_ACCESS_KEY'),
                      secret_key=env('S3_SECRET_KEY'),
                      endpoint_url=env('S3_URL'),
                      bucket_name=env('S3_BUCKET_NAME'),
                  )
                  )

# Загружаем конфиг в переменную config
settings: Config = load_config()
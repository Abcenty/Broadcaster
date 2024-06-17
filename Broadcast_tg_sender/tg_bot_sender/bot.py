from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from config_data.config import settings


def get_bot() -> Bot:
    return Bot(token=settings.tg_bot.token, 
              default=DefaultBotProperties(parse_mode='HTML'))
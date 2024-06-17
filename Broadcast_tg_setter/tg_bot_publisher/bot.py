from aiogram import Bot
from config_data.config import settings
from aiogram.client.default import DefaultBotProperties

def get_bot() -> Bot:
    return Bot(token=settings.tg_bot.token, 
              default=DefaultBotProperties(parse_mode='HTML'))
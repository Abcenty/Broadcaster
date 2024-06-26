# import telebot

# # Замените 'YOUR_BOT_TOKEN' на токен вашего бота

# bot=telebot.TeleBot('7340346900:AAFbGTLUz4mIKdu2R3rE6gmBgpebHz7rfnc')
# # Список каналов, в которые нужно отправить сообщение
# channels = ['@test_cahnnel_71', '@test_channel_81']

# # Отправка сообщения в каждый канал
# for channel in channels:
#     bot.send_message(chat_id=channel, text='Ваше сообщение здесь')
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config_data.config import settings
from handlers import other_handlers, user_handlers
from bot import get_bot

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')
    
    global bot
    # Инициализируем бот и диспетчер
    bot = get_bot()
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
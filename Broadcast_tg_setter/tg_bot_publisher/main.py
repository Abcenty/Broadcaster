import asyncio

from aiogram import Dispatcher
from handlers import general_handlers
from handlers import broadcast_handlers, channel_handlers
from bot import get_bot
from logger import logger


# Функция конфигурирования и запуска бота
async def main():
    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')
    
    global bot
    # Инициализируем бот и диспетчер
    bot = get_bot()
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(broadcast_handlers.router)
    dp.include_router(channel_handlers.router)
    dp.include_router(general_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
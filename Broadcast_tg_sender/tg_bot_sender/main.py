import asyncio
import logging

from tasks.broadcast import broadcast


logger = logging.getLogger(__name__)

async def main() -> None:
    # Perform connection
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting listening for messages')
    await broadcast()


if __name__ == "__main__":
    asyncio.run(main())
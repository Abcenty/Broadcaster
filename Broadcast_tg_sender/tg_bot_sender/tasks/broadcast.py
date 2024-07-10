import asyncio

from aiogram.exceptions import TelegramBadRequest
import logging
from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage
from bot import get_bot
from services.queries.channel.orm import ChannelGateway
from config_data.config import settings

bot = get_bot()
logger = logging.getLogger(__name__)

async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        for channel in ChannelGateway.list():
            try:
                try:
                    photo_url = settings.s3_client.s3_signature +"".join(
                        bytes.decode(message.body, encoding='utf-8')).split("/")[-1]
                    logger.info(f'URL: {photo_url}')
                    await bot.send_photo(channel.name, photo_url, caption='Попробую симитировать пост в новостном канале, для чего собственно этого бота и делаю\nВсем привет дорогие друзья, вы лицезреете процесс доработки моего сервиса по рассылке сообщений. Сейчас я научил эту херню только кидать картинки с подписью или обычный текст, но это уже успех. Самое главное, это то, что я научил 2х тг ботов обмениваться сообщениями, что на самом деле запрещено телеграммом. Для этого я использую брокер сообщений RabbitMQ, который передает то, что мне нужно в виде байтов от одного бота другому. Был отдельный гемор с тем, чтобы шифровать и дешифровать сообщения, н осейчас я это преодолел, поэтому для выхода первой релизной версии мне лишь осталос ьпривести код в порядок и адаптировать интерфейс управляющего бота, что не должно составить особо большого труда.\nА на картинке рандомный скрин 500ой ошибке при тесте моей фичи в стартапе')
                    
                except:
                    await bot.send_message(channel.name, "".join(bytes.decode(message.body, encoding='utf-8')))
                    pass
            except TelegramBadRequest:
                continue
            except:
                continue


async def broadcast() -> None:
    # Perform connection
    
    AMQP_USER = settings.rabbit_mq.AMQP_USER
    AMQP_PASS = settings.rabbit_mq.AMQP_PASS
    AMQP_HOST = settings.rabbit_mq.AMQP_HOST
    
    connection = await connect(f"amqp://{AMQP_USER}:{AMQP_PASS}@{AMQP_HOST}/")

    async with connection:
        # Creating a channel
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        logs_exchange = await channel.declare_exchange(
            "logs", ExchangeType.FANOUT,
        )

        # Declaring queue
        queue = await channel.declare_queue(exclusive=True)

        # Binding the queue to the exchange
        await queue.bind(logs_exchange)

        # Start listening the queue
        await queue.consume(on_message)

        await asyncio.Future()
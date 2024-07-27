import logging

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Конфигурируем логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
            '[%(asctime)s] - %(name)s - %(message)s')

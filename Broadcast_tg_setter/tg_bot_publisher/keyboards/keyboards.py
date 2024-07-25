from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU


# Создаем кнопки с интерфейсом управления
button_start_broadcast = KeyboardButton(text=LEXICON_RU['start_broadcast'])
button_add_channel = KeyboardButton(text=LEXICON_RU['add_channel'])
button_show_channels = KeyboardButton(text=LEXICON_RU['show_channels'])
button_delete_channel = KeyboardButton(text=LEXICON_RU['delete_channel'])

# Кнопка отмены действия
button_cancel = KeyboardButton(text=LEXICON_RU['cancel'])

# Инициализируем билдер для клавиатуры с кнопками управления
interface_buttons_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=6
interface_buttons_builder.row(button_start_broadcast,
                      button_add_channel,
                      button_show_channels,
                      button_delete_channel,
                      width=6)

# Создаем клавиатуру с кнопками управления
interface_buttons: ReplyKeyboardMarkup = interface_buttons_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)

# Создаем кнопку отмены
cancel_button = ReplyKeyboardBuilder().row(button_cancel, width=6).as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
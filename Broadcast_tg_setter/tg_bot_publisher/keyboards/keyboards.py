from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

# # ------- Создаем игровую клавиатуру без использования билдера -------

# # Создаем кнопки игровой клавиатуры
# button_1 = KeyboardButton(text=LEXICON_RU['rock'])
# button_2 = KeyboardButton(text=LEXICON_RU['scissors'])
# button_3 = KeyboardButton(text=LEXICON_RU['paper'])

# # Создаем игровую клавиатуру с кнопками "Камень 🗿",
# # "Ножницы ✂" и "Бумага 📜" как список списков
# game_kb = ReplyKeyboardMarkup(
#     keyboard=[[button_1],
#               [button_2],
#               [button_3]],
#     resize_keyboard=True
# )


# Создаем кнопки с интерфейсом управления
button_start_broadcast = KeyboardButton(text=LEXICON_RU['start_broadcast'])
button_add_channel = KeyboardButton(text=LEXICON_RU['add_channel'])
button_show_channels = KeyboardButton(text=LEXICON_RU['show_channels'])

# Инициализируем билдер для клавиатуры с кнопками управления
interface_buttons_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=4
interface_buttons_builder.row(button_start_broadcast,
                      button_add_channel,
                      button_show_channels,
                      width=6)

# Создаем клавиатуру с кнопками управления
interface_buttons: ReplyKeyboardMarkup = interface_buttons_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
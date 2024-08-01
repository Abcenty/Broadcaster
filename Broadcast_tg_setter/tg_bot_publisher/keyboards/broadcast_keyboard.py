from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards.general_keyboard import button_backward

from lexicon.lexicon_ru import LEXICON_RU

button_start_broadcast = KeyboardButton(text=LEXICON_RU['start_broadcast'])

button_total_broadcast = KeyboardButton(text=LEXICON_RU['total_broadcast'])

button_group_broadcast = KeyboardButton(text=LEXICON_RU['group_broadcast'])

broadcast_buttons_builder = ReplyKeyboardBuilder()

broadcast_type_buttons_builder = ReplyKeyboardBuilder()

broadcast_buttons_builder.row(button_start_broadcast,
                              button_backward,
                      width=6)

broadcast_type_buttons_builder.row(button_total_broadcast,
                                   button_group_broadcast,
                              button_backward,
                      width=6)

broadcast_type_buttons: ReplyKeyboardMarkup = broadcast_type_buttons_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
broadcast_buttons: ReplyKeyboardMarkup = broadcast_buttons_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
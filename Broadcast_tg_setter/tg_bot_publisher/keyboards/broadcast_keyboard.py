from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards.general_keyboard import button_backward

from lexicon.lexicon_ru import LEXICON_RU

button_start_broadcast = KeyboardButton(text=LEXICON_RU['start_broadcast'])

broadcast_buttons_builder = ReplyKeyboardBuilder()

broadcast_buttons_builder.row(button_start_broadcast,
                              button_backward,
                      width=6)

broadcast_buttons: ReplyKeyboardMarkup = broadcast_buttons_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
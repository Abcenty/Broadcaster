from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

button_broadcast_management = KeyboardButton(text=LEXICON_RU['broadcast_management'])
button_channels_management = KeyboardButton(text=LEXICON_RU['channels_management'])
button_channel_group_management = KeyboardButton(text=LEXICON_RU['channel_groups_management'])

button_backward = KeyboardButton(text=LEXICON_RU['backward'])

button_cancel = KeyboardButton(text=LEXICON_RU['cancel'])

general_buttons_builder = ReplyKeyboardBuilder()

general_buttons_builder.row(button_broadcast_management,
                      button_channels_management,
                      button_channel_group_management,
                      width=6)

general_buttons: ReplyKeyboardMarkup = general_buttons_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)

cancel_button: ReplyKeyboardMarkup = ReplyKeyboardBuilder().row(
    button_cancel,
    width=6
).as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)

backward_button: ReplyKeyboardMarkup = ReplyKeyboardBuilder().row(
    button_backward,
    width=6
).as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
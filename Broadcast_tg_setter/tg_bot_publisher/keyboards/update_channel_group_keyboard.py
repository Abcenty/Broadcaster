from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards.general_keyboard import button_backward

from lexicon.lexicon_ru import LEXICON_RU


# button_add_channel = KeyboardButton(text=LEXICON_RU['add_channel'])
# button_show_channels = KeyboardButton(text=LEXICON_RU['show_channels'])
# button_delete_channel = KeyboardButton(text=LEXICON_RU['delete_channel'])

update_group_buttons_builder = ReplyKeyboardBuilder()

# update_group_buttons_builder.row(button_add_channel,
#                       button_show_channels,
#                       button_delete_channel,
#                       button_backward,
#                       width=6)

update_group_buttons: ReplyKeyboardMarkup = update_group_buttons_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
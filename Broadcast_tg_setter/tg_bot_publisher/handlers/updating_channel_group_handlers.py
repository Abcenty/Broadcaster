from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.general_keyboard import cancel_button
from keyboards.channel_group_keyboard import channel_group_buttons
from keyboards.update_channel_group_keyboard import update_group_buttons
from lexicon.lexicon_ru import LEXICON_RU
from services.queries.users.orm import UserGateway
from fsm.fsm import FSMFillForm
from services.queries.groups.orm import ChannelGroupGateway
from bot import get_bot
from logger import logger


router = Router()

bot = get_bot()


# Этот хэндлер срабатывает на запрос изменения группы
@router.message(F.text == LEXICON_RU['update_group'], StateFilter(FSMFillForm.channel_group_management))
async def update_group(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await state.set_state(FSMFillForm.update_group)
            await message.answer(text=LEXICON_RU['update_group_answer'], reply_markup=update_group_buttons)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['update_group_error'])
        logger.info('Error while updating channel group')
        
        
# Этот хэндлер срабатывает на выход из панели изменения группы каналов
@router.message(F.text == LEXICON_RU['update_group_cancel'], StateFilter(FSMFillForm.update_group))
async def update_group_cancel(message: Message, state: FSMContext):
    try:
        await message.answer(
            text=LEXICON_RU['update_canceled'],
            reply_markup=channel_group_buttons,
        )
        await state.set_state(FSMFillForm.channel_group_management)
    except:
        await message.answer(text=LEXICON_RU['cancel_group_update_error'])
        logger.info('Error while canceling updating of channel group')
        
        
# Этот хэндлер срабатывает на отмену изменения группы каналов
@router.message(F.text == LEXICON_RU['cancel'], StateFilter(FSMFillForm.process_group_updating))
async def cancel_process_group_updating(message: Message, state: FSMContext):
    try:
        await message.answer(
            text=LEXICON_RU['update_canceled'],
            reply_markup=update_group_buttons,
        )
        await state.set_state(FSMFillForm.update_group)
    except:
        await message.answer(text=LEXICON_RU['cancel_group_update_error'])
        logger.info('Error while canceling updating process of channel group') 
        
        
# Этот хэндлер срабатывает на запрос добавления каналов в группу
@router.message(F.text == LEXICON_RU['add_channels_for_group'], StateFilter(FSMFillForm.update_group))
async def update_group_add_channels(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await state.set_state(FSMFillForm.process_group_updating)
            await message.answer(text=LEXICON_RU['add_channels_for_group_answer'], reply_markup=cancel_button)
            channels = message.text
            ChannelGroupGateway.update()
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['add_channels_for_group_error'])
        logger.info('Error while adding channels to group')
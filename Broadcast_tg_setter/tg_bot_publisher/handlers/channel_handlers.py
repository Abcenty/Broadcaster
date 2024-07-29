from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.general_keyboard import cancel_button
from keyboards.channel_keyboard import channels_buttons
from lexicon.lexicon_ru import LEXICON_RU
from services.queries.users.orm import UserGateway
from fsm.fsm import FSMFillForm
from services.queries.channel.orm import ChannelGateway
from bot import get_bot
from logger import logger


router = Router()

bot = get_bot()


# Этот хэндлер срабатывает на запрос перехода к управлению каналами
@router.message(F.text == LEXICON_RU['channels_management'], StateFilter(default_state))
async def process_channels_management(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await state.set_state(FSMFillForm.channels_management)
            await message.answer(text=LEXICON_RU['channels_management_answer'], reply_markup=channels_buttons)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['channel_management_error'])
        logger.info('Error while starting channel management')
        
        
# Этот хэндлер срабатывает на запрос подключения канала
@router.message(F.text == LEXICON_RU['add_channel'], StateFilter(FSMFillForm.channels_management))
async def add_channel(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await state.set_state(FSMFillForm.add_channel)
            await message.answer(text=LEXICON_RU['add_channel_answer'], reply_markup=cancel_button)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['adding_channel_error'])
        logger.info('Error while adding channel')       


# Этот хэндлер срабатывает на ввод канала для удаления
@router.message(F.text == LEXICON_RU['delete_channel'], StateFilter(FSMFillForm.channels_management))
async def delete_channel(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await state.set_state(FSMFillForm.delete_channel)
            await message.answer(text=LEXICON_RU['delete_channel_answer'], reply_markup=cancel_button)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['deleting_channel_error'])
        logger.info('Error while deleting channel')        

# Этот хэндлер срабатывает на отмену действия с каналом/каналами
@router.message(F.text == LEXICON_RU['cancel'], StateFilter(FSMFillForm.delete_channel, FSMFillForm.add_channel))
async def process_channel_cancel(message: Message, state: FSMContext):
    try:
        await message.answer(
            text=LEXICON_RU['canceled'],
            reply_markup=channels_buttons,
        )
        await state.set_state(FSMFillForm.channels_management)
    except:
        await message.answer(text=LEXICON_RU['cancel_channel_action_error'])
        logger.info('Error while canceling action with channel')       
    

# Этот хэндлер срабатывает на ввод канала для подключения
@router.message(F.text, StateFilter(FSMFillForm.add_channel))
async def process_add_channel(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            if message.text == LEXICON_RU['backward']:
                await message.answer(text=LEXICON_RU['backwarded'], reply_markup=channels_buttons)
            else:
                ChannelGateway.create(ChannelGateway, message.text)
                await message.answer(text=LEXICON_RU['add_channel_success'], reply_markup=channels_buttons)
            await state.set_state(FSMFillForm.channels_management)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['adding_channel_error'])
        logger.info('Error while adding channel')
            
        
# Этот хэндлер срабатывает на ввод канала для удаления
@router.message(F.text, StateFilter(FSMFillForm.delete_channel))
async def process_delete_channel(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            if message.text == LEXICON_RU['backward']:
                await message.answer(text=LEXICON_RU['backwarded'], reply_markup=channels_buttons)
            else:
                ChannelGateway.delete(message.text)
                await message.answer(text=LEXICON_RU['delete_channel_success'], reply_markup=channels_buttons)
            await state.set_state(FSMFillForm.channels_management)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['deleting_channel_error'])
        logger.info('Error while deleting channel')
    
# Этот хэндлер срабатывает на запрос списка подключенных каналов
@router.message(F.text == LEXICON_RU['show_channels'], StateFilter(FSMFillForm.channels_management))
async def process_show_channels(message: Message):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await message.answer(text=LEXICON_RU['show_channels_answer'], reply_markup=channels_buttons)
            channels = [channel.name for channel in ChannelGateway.list()]
            text = ", ".join (channels).replace(", ", "\n")
            await message.answer(text=text, reply_markup=channels_buttons)
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['show_channels_error'])
        logger.info('Error while showing list of channels')

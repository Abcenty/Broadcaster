from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from services.utills.message_former import MessageType, format_message
from keyboards.keyboards import interface_buttons, cancel_button
from lexicon.lexicon_ru import LEXICON_RU
from services.queries.users.orm import UserGateway
from fsm.fsm import FSMFillForm
from services.queries.channel.orm import ChannelGateway
from bot import get_bot
from set_broadcast import set_task
from config_data.config import settings
from services.s3.dependency import s3_client
from main import logger

router = Router()

bot = get_bot()

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    username = message.from_user.username
    if UserGateway.get(username) and UserGateway.get_accessed(username):
        await message.answer(text=LEXICON_RU['/start'], reply_markup=interface_buttons)
    elif UserGateway.get(username):
        await message.answer(text=LEXICON_RU['/access_denied'])
    else:
        UserGateway.create(username)
        await message.answer(text=LEXICON_RU['/access_denied'])
    
# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=interface_buttons)
    
    
@router.message(F.text == LEXICON_RU['cancel'], ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU['canceled'],
        reply_markup=interface_buttons,
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()

    
    
# Этот хэндлер срабатывает на запрос создания рассылки
@router.message(F.text == LEXICON_RU['start_broadcast'], StateFilter(default_state))
async def process_start_broadcast(message: Message, state: FSMContext):
    username = message.from_user.username
    if UserGateway.get_accessed(username):
        await state.set_state(FSMFillForm.start_broadcast)
        await message.answer(text=LEXICON_RU['start_broadcast_answer'], reply_markup=cancel_button)
    else:
        await message.answer(text=LEXICON_RU['/access_denied'])
        
        
# Этот хэндлер срабатывает на ввод канала для подключения

@router.message(F.text, StateFilter(FSMFillForm.start_broadcast))
async def process_broadcast(message: Message, state: FSMContext):
    username = message.from_user.username
    if UserGateway.get_accessed(username):
        await set_task(format_message(type='text', text=message.text))
        await message.answer(text=LEXICON_RU['broadcast_success'], reply_markup=interface_buttons)
        await state.clear()
    else:
        await message.answer(text=LEXICON_RU['/access_denied'])
        

@router.message(F.photo, StateFilter(FSMFillForm.start_broadcast))
async def process_broadcast_photo(message: Message, state: FSMContext):
    username = message.from_user.username
    if UserGateway.get_accessed(username):
        file = await bot.get_file(message.photo[-1].file_id)
        file_path = file.file_path
        bfile = await bot.download_file(file_path)
        s3_client.upload_file(file_path=file_path, file=bfile)
        await set_task(format_message(type='photo', file_path=file_path.split("/")[-1],
                                      text=message.caption if message.caption is not None else ""))
        await message.answer(text=LEXICON_RU['broadcast_success'], reply_markup=interface_buttons)
        await state.clear()
    else:
        await message.answer(text=LEXICON_RU['/access_denied'])
    
    
# Этот хэндлер срабатывает на запрос подключения канала
@router.message(F.text == LEXICON_RU['add_channel'], StateFilter(default_state))
async def add_channel(message: Message, state: FSMContext):
    username = message.from_user.username
    if UserGateway.get_accessed(username):
        await state.set_state(FSMFillForm.add_channel)
        await message.answer(text=LEXICON_RU['add_channel_answer'], reply_markup=cancel_button)
    else:
        await message.answer(text=LEXICON_RU['/access_denied'])
        

# Этот хэндлер срабатывает на ввод канала для подключения
@router.message(F.text, StateFilter(FSMFillForm.add_channel))
async def process_add_channel(message: Message, state: FSMContext):
    username = message.from_user.username
    if UserGateway.get_accessed(username):
        ChannelGateway.create(message.text)
        await message.answer(text=LEXICON_RU['add_channel_success'], reply_markup=interface_buttons)
        await state.clear()
    else:
        await message.answer(text=LEXICON_RU['/access_denied'])
        
        
# Этот хэндлер срабатывает на ввод канала для удаления
@router.message(F.text == LEXICON_RU['delete_channel'], StateFilter(default_state))
async def delete_channel(message: Message, state: FSMContext):
    username = message.from_user.username
    if UserGateway.get_accessed(username):
        await state.set_state(FSMFillForm.delete_channel)
        await message.answer(text=LEXICON_RU['delete_channel_answer'], reply_markup=cancel_button)
    else:
        await message.answer(text=LEXICON_RU['/access_denied'])
        
        
# Этот хэндлер срабатывает на ввод канала для подключения
@router.message(F.text, StateFilter(FSMFillForm.delete_channel))
async def process_delete_channel(message: Message, state: FSMContext):
    username = message.from_user.username
    if UserGateway.get_accessed(username):
        ChannelGateway.delete(message.text)
        await message.answer(text=LEXICON_RU['delete_channel_success'], reply_markup=interface_buttons)
        await state.clear()
    else:
        await message.answer(text=LEXICON_RU['/access_denied'])
        
    
# Этот хэндлер срабатывает на запрос списка подключенных каналов
@router.message(F.text == LEXICON_RU['show_channels'], StateFilter(default_state))
async def process_show_channels(message: Message):
    username = message.from_user.username
    if UserGateway.get_accessed(username):
        await message.answer(text=LEXICON_RU['show_channels_answer'], reply_markup=interface_buttons)
        channels = [channel.name for channel in ChannelGateway.list()]
        text = ", ".join (channels).replace(", ", "\n")
        await message.answer(text=text, reply_markup=interface_buttons)
    else:
        await message.answer(text=LEXICON_RU['/access_denied'])
        
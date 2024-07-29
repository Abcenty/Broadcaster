from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from fsm.fsm import FSMFillForm
from keyboards.general_keyboard import general_buttons
from lexicon.lexicon_ru import LEXICON_RU
from services.queries.users.orm import UserGateway
from bot import get_bot
from logger import logger


router = Router()

bot = get_bot()

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    username = message.from_user.username
    try:
        # Проверка на известность и права доступа
        if UserGateway.get(username) and UserGateway.get_is_authorized(username):
            await message.answer(text=LEXICON_RU['/start'], reply_markup=general_buttons)
        # Проверка только на известность если нет прав
        elif UserGateway.get(username):
            await message.answer(text=LEXICON_RU['/access_denied'])
        # Добавление неизвестного пользователя
        else:
            UserGateway.create(UserGateway, username)
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['start_bot_error'])
        logger.info('Error while starting bot by user')       
    
# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    try:
        await message.answer(text=LEXICON_RU['/help'], reply_markup=general_buttons)
    except:
        await message.answer(text=LEXICON_RU['help_error'])
        logger.info('Error while getting help instruction') 
    
# Этот хэндлер срабатывает на возврат в главное меню из панелей управления
@router.message(F.text == LEXICON_RU['backward'], StateFilter(FSMFillForm.channels_management, FSMFillForm.broadcast_management))
async def process_backward(message: Message, state: FSMContext):
    username = message.from_user.username
    try:
        if UserGateway.get_is_authorized(username):
            await message.answer(
                text=LEXICON_RU['backwarded'],
                reply_markup=general_buttons,
            )
            await state.clear()
        else:
            await message.answer(text=LEXICON_RU['/access_denied'])
    except:
        await message.answer(text=LEXICON_RU['bacward_error'])
        logger.info('Error while returning to main menu')
    

# Хэндлер для обработки некорректных сообщений
@router.message()
async def process_incorrect_message(message: Message):
    try:
        await message.answer(text=LEXICON_RU['other_answer'])
    except:
        await message.answer(text=LEXICON_RU['bacward_error'])
        logger.info('Error while returning to main menu')
    

    

        
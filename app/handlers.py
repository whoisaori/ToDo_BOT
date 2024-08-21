from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command


router = Router()


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Это помощь')

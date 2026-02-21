from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo


def build_webapp_keyboard(webapp_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Открыть редактор",
                    web_app=WebAppInfo(url=webapp_url),
                )
            ]
        ]
    )


def setup_bot(dp: Dispatcher, webapp_url: str) -> None:
    @dp.message(CommandStart())
    async def start_handler(message: Message) -> None:
        await message.answer(
            "Привет! Открой WebApp через кнопку ниже.",
            reply_markup=build_webapp_keyboard(webapp_url),
        )

import asyncio
import os

from aiogram import Bot, Dispatcher
from uvicorn import Config, Server

from api import app
from bot import setup_bot


async def run_api() -> None:
    config = Config(app=app, host="0.0.0.0", port=8000, log_level="info")
    server = Server(config)
    await server.serve()


async def run_bot() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is required")

    base_url = os.getenv("WEBAPP_BASE_URL", "http://localhost:8000")
    webapp_url = f"{base_url.rstrip('/')}/webapp"

    bot = Bot(token=token)
    dp = Dispatcher()
    setup_bot(dp, webapp_url)

    await dp.start_polling(bot)


async def main() -> None:
    await asyncio.gather(run_api(), run_bot())


if __name__ == "__main__":
    asyncio.run(main())

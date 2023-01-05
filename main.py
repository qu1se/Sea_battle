from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

import room_handlers
import game_handlers

import config
import asyncio
import logging

async def main():
    logging.basicConfig(level=logging.DEBUG)
    bot = Bot(config.TOKEN, parse_mode='html')

    storage = MemoryStorage()

    await storage.set_data(bot, 'general_data', {'queue':[], 'room_id':0, 'games':{}})

    dp = Dispatcher(storage)
    
    dp.include_router(game_handlers.router)
    dp.include_router(room_handlers.router)

    await bot.delete_webhook(drop_pending_updates = True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await storage.close()


asyncio.run(main())

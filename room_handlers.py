
from aiogram.dispatcher.router import Router
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.storage.base import StorageKey
from aiogram.exceptions import TelegramBadRequest
from random import randint

from keyboards import show_field
from states import UserStates

router = Router()

@router.message(commands='start')
async def start_cmd(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}; \n/new_game - приступить к битве \nРекомендуем прочитать /rules перед началом игры')

@router.message(commands  = 'rules')
async def rules_cmd(message: Message):
    await message.answer('''
    -------------------------------------Правила-------------------------------------
    1.Расположение кораблей
        ⚓️Общее количество занятых ячеек - 20
            Корабль из 4-х ячеек - 1
            Кораблей из 3-х ячеек - 2
            Кораблей из 2-х - 3
            И кораблей из 1 ячейки - 4

        ⚓️Растановку начинать строго с корабля 
            из 4-х ячеек, следом идут корабли из 3-х
            и так далее

        ⚓️Для удаления корабля следует повторно нажать
            на него
    2.Дайте боту время на мыслительные процессы
    ''')

@router.message(commands = 'new_game')
async def new_game_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Поиск противника, ожидайте ")
    bot = state.bot
    #Getting general data from memory storage
    data = await state.storage.get_data(bot, 'general_data')
    queue = data['queue']

    #if user has already joined to queue
    if message.from_user.id in queue:
        await message.answer('Вы уже в поиске. Подождите пожалуйста.')
        return

    #Setting user tp first game state
    await state.set_state(UserStates.ships_placing)
    #if someone searching game
    if queue:
        #getting first player UserObject
        first_user = await bot.get_chat(queue[0])
        key = StorageKey(bot.id, first_user.id, first_user.id)

        #Setting first user state
        await state.storage.set_state(bot, key, UserStates.ships_placing)
        await state.storage.set_data(bot, key, {'room':data['room_id']})

        #Setting second user state
        await state.set_state(UserStates.ships_placing)
        await state.set_data({'room':data['room_id']})

        #randomly choosing first player
        turn = queue[0] if randint(0, 1) else message.from_user.id

        start_field = [[' ' for j in range(8)] for i in range(8)]
        #setting new game to general data
        data['games'][str(data['room_id'])] = \
        {'players':
            {str(queue[0]):
                {'field':[[' ' for j in range(8)] for i in range(8)], 
                 'ships':{x:0 for x in range(1, 5)},
                 'atack_field':[[' ' for j in range(8)] for i in range(8)],
                 'enemy':str(message.from_user.id)},
            str(message.from_user.id):
                {'field':start_field, 
                 'ships':{x:0 for x in range(1, 5)},
                 'atack_field':[[' ' for j in range(8)] for i in range(8)],
                 'enemy':str(queue[0])
                 }},
        'turn':turn,
        'ready_list':[]
        }

        await bot.send_message(queue[0], f'Ты будешь сражаться с <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>')
        await bot.send_message(queue[0], 'Расставляйте корабли, командующий.', reply_markup = show_field('start'))

        await message.answer(f'Ты будешь сражаться с <a href="tg://user?id={queue[0]}">{first_user.first_name}</a>')
        await message.answer('Расставляйте корабли, командующий.', reply_markup = show_field('start'))

        #clearing queue
        queue.pop(0)
        #updating room number
        data['room_id'] += 1
    else:
        queue.append(message.from_user.id)



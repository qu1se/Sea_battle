import asyncio

from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.storage.base import StorageKey
from keyboards import show_field, is_ready
from states import UserStates


from game_functions import get_data, main_check, put_dorts, remove_ship, ships_count, get_ship_len, is_cracked

router = Router()

@router.callback_query(state=UserStates.ships_placing)
async def place_ship(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    y, x = [int(coord) for coord in callback.data.split(':')]
    player = (await get_data(state))['players'][str(callback.from_user.id)]
    field = player['field']
    ships = player['ships']

    if field[y][x] == '🚢':
        remove_ship(field, ships, x, y)
    else:
        if main_check(field, ships, x, y):
            field[y][x] = '🚢'
    
    #против багов
    if callback.message.reply_markup == show_field(field):
        return

    await callback.message.edit_reply_markup(show_field(field))

    if ships_count(field) == 20:
        await state.set_state(UserStates.ask_ready)
        player['field_id'] = callback.message.message_id
        player['inline_id'] = callback.inline_message_id
        await callback.message.answer('Вы готовы?', reply_markup=is_ready())

@router.callback_query(state=UserStates.ask_ready)
async def ready(callback: CallbackQuery, state: FSMContext):
    bot = state.bot
    if callback.message.text != 'Вы готовы?':
        return

    await callback.message.delete()

    data = await get_data(state)

    if callback.from_user.id in data['ready_list']:
        return

    if callback.data == 'y':
        if data['ready_list']:
            await callback.answer()
            await callback.message.answer('Второй игрок уже готов. Сейчас начнется баталия')
            await bot.send_message(data['ready_list'][0], 'Второй игрок подготовился, сейчас начнется битва.')

            await state.set_state(UserStates.battle)
            await state.storage.set_state(bot, StorageKey(bot.id, data['ready_list'][0], data['ready_list'][0]), UserStates.battle)

            first_player = await bot.get_chat(data['turn'])
            for player in data['players']:
                await bot.send_message(int(player), f'Первым атакует {first_player.first_name}')
                await bot.send_message(int(player), 'Вот ваше поле для атаки:', reply_markup=show_field('start'))
        else:
            data['ready_list'].append(callback.from_user.id)
            await callback.answer('Подождите второго игрока', show_alert=True)

    else:
        await state.set_state(UserStates.ships_placing)
        await callback.answer('Продолжайте расстановку', show_alert=True)

@router.callback_query(state=UserStates.battle)
async def battle(callback:CallbackQuery, state: FSMContext):
    bot = state.bot
    data = await get_data(state)
    y, x = [int(coord) for coord in callback.data.split(':')]
    
    if int(data['turn']) != callback.from_user.id:
        await callback.answer('Сейчас не ваш ход', show_alert=True)
        return

    player = data['players'][str(data['turn'])]
    second_player = data['players'][player['enemy']]


    if second_player['field'][y][x] == ' ':
        await callback.answer('Мимо', show_alert=True)
        player['atack_field'][y][x] = '.'
        second_player['field'][y][x] = '.'
        data['turn'] = player['enemy']
        await callback.message.edit_reply_markup(show_field(player['atack_field']))
        await bot.edit_message_reply_markup(player['enemy'], second_player['field_id'], second_player['inline_id'], reply_markup=show_field(second_player['field']))
        msg = await state.bot.send_message(int(player['enemy']), 'Враг промазал, теперь ваш ход.')
        await asyncio.sleep(30)
        await state.bot.delete_message(int(player['enemy']), msg.message_id)

    elif second_player['field'][y][x] == '🚢':
        player['atack_field'][y][x] = 'x'
        second_player['field'][y][x] = 'x'
        if is_cracked(second_player['field'], x, y):
            put_dorts(player['atack_field'], x, y)
            text = 'Корабль уничтожен'
        else:
            text = 'Есть пробитие!'

        await callback.message.edit_reply_markup(show_field(player['atack_field']))
        await state.bot.edit_message_reply_markup(int(player['enemy']), second_player['field_id'], second_player['inline_id'], reply_markup=show_field(second_player['field']))
        await callback.answer(text, show_alert=True)
        msg = await state.bot.send_message(int(player['enemy']), 'Враг попал.')

        if ships_count(second_player['field']) == 0:
            await callback.message.answer('Флот врага повержен. Мы победили, капитан!')
            await bot.send_message(int(player['enemy']), 'Ваш флот потерпел поражение, мы терпим крушение')
            await state.clear()
            await state.storage.set_state(bot, StorageKey(bot.id, int(player['enemy']), int(player['enemy'])))

        await asyncio.sleep(30)
        await state.bot.delete_message(int(player['enemy']), msg.message_id)

    await callback.answer()
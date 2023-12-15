import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
logging.basicConfig(level=logging.INFO)
API_TOKEN = 'ТУТМОЙТОКЕН'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
board = [['1️⃣', '2️⃣', '3️⃣'],
         ['4️⃣', '5️⃣', '6️⃣'],
         ['7️⃣', '8️⃣', '9️⃣']]
current_player = '❌'
def display_board():
    return "\n".join([" | ".join(row) for row in board])
@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    global board, current_player
    board = [['1️⃣', '2️⃣', '3️⃣'],
             ['4️⃣', '5️⃣', '6️⃣'],
             ['7️⃣', '8️⃣', '9️⃣']]
    current_player = '❌'
    await message.answer("Игра Крестики-Нолики началась!\n" + display_board())
    await make_move(message)
async def make_move(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for row in board:
        keyboard.row(*[InlineKeyboardButton(cell, callback_data=cell) for cell in row])
    await message.answer(f"Ход игрока {current_player}\n" + display_board(), reply_markup=keyboard)
@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    global board, current_player
    cell_number = callback_query.data
    for row in board:
        if cell_number in row:
            row[row.index(cell_number)] = current_player
            if check_winner():
                await callback_query.answer(f"Игрок {current_player} победил!\n" + display_board())
                await stop_game(callback_query.message, f"Игрок {current_player} победил!")
            elif is_board_full():
                await callback_query.answer("Ничья!\n" + display_board())
                await stop_game(callback_query.message, "Ничья!")
            else:
                current_player = '⭕' if current_player == '❌' else '❌'
                await make_move(callback_query.message)
            break
    else:
        await callback_query.answer("Клетка уже занята! Выберите другую.")
def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] or \
           board[0][i] == board[1][i] == board[2][i]:
            return True
    if board[0][0] == board[1][1] == board[2][2] or \
       board[0][2] == board[1][1] == board[2][0]:
        return True
    return False
def is_board_full():
    return all(cell in ['❌', '⭕'] for row in board for cell in row)
async def stop_game(message: types.Message, result_message: str):
    await message.answer("Игра завершена. Результат игры:")
    await message.answer(display_board())
    await message.answer(result_message)
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.session.close()
    executor.stop_polling()
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
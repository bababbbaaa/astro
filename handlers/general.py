from controller import dp
from aiogram.types import *
from aiogram.dispatcher.storage import FSMContext

@dp.message_handler(state='*', text='cancel')
async def cancel_handler(message: Message, state: FSMContext):
    """
    Allow user to cancel any action
    """

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Действие было прервано', reply_markup=ReplyKeyboardRemove())
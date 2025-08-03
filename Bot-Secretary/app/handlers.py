from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import logging

import app.keyboards as kb

router = Router()

logging.basicConfig(level=logging.INFO)

ADMIN_ID = 1111111#(Your TeleGram_ID)

class Data(StatesGroup):
    waiting_for_feedback = State()
    answer_for_feedback = State()
    user = State()


@router.message(CommandStart())
async def cmd_start(message:types.Message):
    await message.answer('👋 Hello!\n\n'
    'Your Text', reply_markup=kb.main)

@router.message(F.text == 'Leave a message⚙️')
async def ask_for_feedback(message:types.Message, state:FSMContext):
      await message.answer('Write your message💬. < 120 words')
      await state.set_state(Data.waiting_for_feedback)


#Message comes to admin
@router.message(Data.waiting_for_feedback)
async def handle_feedback(message: types.Message, state:FSMContext):
    user = message.from_user
    feedback_text = message.text

    if len(feedback_text.split()) > 120:
        await message.answer("❌ The message is too long! Please shorten to 120 words.")
        return

    admin_message = (
        f"📨 New message!\n"
        f"👤 User: {user.full_name} (@{user.username})\n"
        f"🆔 ID: {user.id}\n"
        f"✉️ Message text:\n{feedback_text}"
        
    )
    await message.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_message,
        reply_markup=kb.admin
    )

    await message.answer("✅ Thank you! Your review has been sent to the owner.")      

    await state.clear()     

@router.message(F.text == 'Answer to message')
async def handle_user(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer('Write the user of the one you want to reply to')
        await state.set_state(Data.user)
    else:
        await message.answer('You are not an admin')


@router.message(Data.user)    
async def handle_answer(message: types.Message, state: FSMContext):
    user_id = int(message.text)
    await state.update_data(user_id = user_id)    
    await message.answer('Write your answer')
    await state.set_state(Data.answer_for_feedback)
         
#admin forwards response to user
@router.message(Data.answer_for_feedback)
async def handle_peredacha(message: types.Message, state:FSMContext):         
    

    feedback_answer = message.text
    
    data = await state.get_data()

    admin_answer = (
        f"📨 Пришел ответ на ваше сообщение\n{feedback_answer}"
    )
    await message.bot.send_message(
        chat_id = data["user_id"],
        text=admin_answer
    )

    await message.answer("✅ Спасибо! Ваш ответ отправлен пользователю.")      

    await state.clear()

#Filter
@router.message(F.text)
async def error(message:types.Message):
      await message.answer('Пожалуйста следуйте инструкциям или нажмите /start')
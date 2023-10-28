from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp,bot
from states.personalData import PersonalData
from keyboards.inline.manage_post import confirmation_keyboard, post_callback
from aiogram.types import Message, CallbackQuery, InputFile
from data.config import ADMINS, CHANNELS
from states.newpost import NewPost



@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu alaykum, quyidagi ma'lumotlarni kiriting:")
    await message.answer(f"<b>To'liq ismingizni kiriting:</b>")
    await NewPost.fullName.set()



@dp.message_handler(state=NewPost.fullName)
async def enter_message(message: Message, state: FSMContext):
    await state.update_data(name=message.html_text)
    await message.answer(f"<b>Telefon raqam:</b>")
    await NewPost.next()

@dp.message_handler(state=NewPost.phoneNum)
async def enter_message(message: Message, state: FSMContext):
    await state.update_data(phone=message.html_text)
    await message.answer(f"<b>Murojaat matni:</b>")
    await NewPost.next()

@dp.message_handler(state=NewPost.NewMessage)
async def enter_message(message: Message, state: FSMContext):
    await state.update_data(text=message.html_text, mention=message.from_user.get_mention())
    await message.answer(f"Murojaat yuborishni tasdiqlang:",
                         reply_markup=confirmation_keyboard)
    await NewPost.next()



@dp.callback_query_handler(post_callback.filter(action="post"), state=NewPost.Confirm)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        name = data.get("name")
        phone = data.get("phone")
        text= data.get("text")
        mention = data.get("mention")
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer(" 🆗 Xabar administratorga  yuborildi\nTez orada siz bilan bog'lanamiz!")
    # await bot.send_message(ADMINS[0], f"Foydalanuvchi {mention}  quyidagi xabarni yuborayapti:")
    await bot.send_message(ADMINS[0],  f"Xabar\n <b>F.I.Sh:</b>{name}\n <b>Telefon:</b>{phone}\n <b>Murojaat matni:</b>\n{text}\n", reply_markup=confirmation_keyboard)





@dp.callback_query_handler(post_callback.filter(action="cancel"), state=NewPost.Confirm)
async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Xabar rad etildi.")


@dp.message_handler(state=NewPost.Confirm)
async def post_unknown(message: Message):
    await message.answer("Chop etish yoki rad etishni tanlang")


@dp.callback_query_handler(post_callback.filter(action="post"))
async def approve_post(call: CallbackQuery):
    await call.answer("Chop etishga ruhsat berildi.", show_alert=True)
    target_channel = CHANNELS[0]
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target_channel)


@dp.callback_query_handler(post_callback.filter(action="cancel"))
async def decline_post(call: CallbackQuery):
    await call.answer("Xabar rad etildi.", show_alert=True)
    await call.message.edit_reply_markup()

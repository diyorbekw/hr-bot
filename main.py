import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN, ADMIN_CHAT_ID

# Loggerni sozlash
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FSM holatlari
class Form(StatesGroup):
    ism = State()
    tugilgan_yili = State()
    malumot = State()
    viloyat = State()
    telefon = State()
    turmush = State()
    ish_tajriba = State()
    crm = State()
    sotuv = State()
    oylik = State()
    muddat = State()
    tillar = State()
    boshqa_tillar = State()
    reklama = State()
    

# Botni ishga tushirish
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Til tanlovlari uchun global dictionary
user_languages = {}

# Start komandasi
@dp.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Form.ism)
    await message.answer("HR anketa botiga xush kelibsiz!\nIsmingizni kiriting:")

# Ismni qabul qilish
@dp.message(Form.ism)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await state.set_state(Form.tugilgan_yili)
    await message.answer("Iltimos, tug'ilgan kuningizni <b>dd/mm/yyyy</b> formatida kiriting (Masalan: 12/06/1995).")

import re
from datetime import datetime

@dp.message(Form.tugilgan_yili)
async def process_birth_date(message: types.Message, state: FSMContext):
    date_text = message.text.strip()
    
    # Formatni tekshirish: dd/mm/yyyy
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", date_text):
        await message.answer("Iltimos, tug'ilgan kuningizni <b>dd/mm/yyyy</b> formatida kiriting (Masalan: 12/06/1995).")
        return

    try:
        # Sana haqiqiyligini tekshirish
        birth_date = datetime.strptime(date_text, "%d/%m/%Y")
    except ValueError:
        await message.answer("Iltimos, mavjud sana kiriting (Masalan: 12/06/1995).")
        return

    await state.update_data(tugilgan_yili=date_text)
    await state.set_state(Form.malumot)

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Oliy", callback_data="malumot_oliy"))
    builder.add(types.InlineKeyboardButton(text="O'rta maxsus", callback_data="malumot_orta_maxsus"))
    builder.add(types.InlineKeyboardButton(text="O'rta", callback_data="malumot_orta"))

    await message.answer("Ma'lumotingiz qanday?", reply_markup=builder.as_markup())


# Ma'lumot turini qabul qilish
@dp.callback_query(F.data.startswith("malumot_"), Form.malumot)
async def process_education(callback: types.CallbackQuery, state: FSMContext):
    malumot = callback.data.split("_")[1]
    await state.update_data(malumot=malumot)
    await state.set_state(Form.viloyat)
    
    viloyatlar = [
        "Toshkent", "Andijon", "Buxoro", "Farg'ona", "Jizzax",
        "Xorazm", "Namangan", "Navoiy", "Qashqadaryo",
        "Samarqand", "Sirdaryo", "Surxondaryo"
    ]
    
    builder = InlineKeyboardBuilder()
    for viloyat in viloyatlar:
        builder.add(types.InlineKeyboardButton(text=viloyat, callback_data=f"vil_{viloyat}"))
    builder.adjust(2)
    
    await callback.message.edit_text("Yashash manzilingiz (viloyat)?", reply_markup=builder.as_markup())
    await callback.answer()

# Viloyatni qabul qilish
@dp.callback_query(F.data.startswith("vil_"), Form.viloyat)
async def process_region(callback: types.CallbackQuery, state: FSMContext):
    viloyat = callback.data.replace("vil_", "")
    await state.update_data(viloyat=viloyat)
    await state.set_state(Form.telefon)
    await callback.message.edit_text("Telefon raqamingizni kiriting (+998xxxxxxxxx):")
    await callback.answer()

# Telefon raqamini qabul qilish
@dp.message(Form.telefon)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(telefon=message.text)
    await state.set_state(Form.turmush)
    
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Oilali", callback_data="turmush_oilali"))
    builder.add(types.InlineKeyboardButton(text="Turmush qurmagan", callback_data="turmush_qurmagan"))
    
    await message.answer("Turmush holatingiz?", reply_markup=builder.as_markup())

# Turmush holatini qabul qilish
@dp.callback_query(F.data.startswith("turmush_"), Form.turmush)
async def process_marital_status(callback: types.CallbackQuery, state: FSMContext):
    turmush = callback.data.replace("turmush_", "")
    await state.update_data(turmush=turmush)
    await state.set_state(Form.ish_tajriba)
    await callback.message.edit_text("Avval ishlagan joyingizdagi ma'lumotlarni kiriting:")
    await callback.answer()

# Ish tajribasini qabul qilish
@dp.message(Form.ish_tajriba)
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(ish_tajriba=message.text)
    await state.set_state(Form.crm)
    await message.answer("CRM dasturida ishlashni bilasizmi?")#Qancha oylik maoshga ishlamoqchisiz?, 

# Crm ni qabul qilish 
@dp.message(Form.crm)
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(crm=message.text)
    await state.set_state(Form.sotuv)
    await message.answer("Qanday Sotuv Texnikalarini bilasiz yozib qoldiring ! Misol uchun : SPIN")

# Sotuvni texnikalarini qabul qilish
@dp.message(Form.sotuv)
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(sotuv=message.text)
    await state.set_state(Form.oylik)
    await message.answer("Qancha oylik maoshga ishlamoqchisiz?")

# Oylik maoshni qabul qilish
@dp.message(Form.oylik)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(oylik=message.text)
    await state.set_state(Form.muddat)
    
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="6 oy", callback_data="muddat_6oy"))
    builder.add(types.InlineKeyboardButton(text="1 yil", callback_data="muddat_1yil"))
    builder.add(types.InlineKeyboardButton(text="2-3 yil", callback_data="muddat_2-3yil"))
    builder.add(types.InlineKeyboardButton(text="5 yil", callback_data="muddat_5yil"))
    
    await message.answer("Qancha muddat ishlamoqchisiz?", reply_markup=builder.as_markup())

# Ish muddatini qabul qilish
@dp.callback_query(F.data.startswith("muddat_"), Form.muddat)
async def process_work_duration(callback: types.CallbackQuery, state: FSMContext):
    muddat = callback.data.replace("muddat_", "")
    await state.update_data(muddat=muddat.replace("_", "-"))
    await state.set_state(Form.tillar)
    
    # Tillarni tanlash uchun keyboard
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Ingliz", callback_data="til_ingliz"))
    builder.add(types.InlineKeyboardButton(text="Rus", callback_data="til_rus"))
    builder.add(types.InlineKeyboardButton(text="Koreys", callback_data="til_koreys"))
    builder.add(types.InlineKeyboardButton(text="Tugatish", callback_data="til_tugatish"))
    
    await callback.message.edit_text("Tillarni bilish darajangizni tanlang:", reply_markup=builder.as_markup())
    await callback.answer()

# Til tanlovi bosqichi
@dp.callback_query(F.data.startswith("til_"), Form.tillar)
async def process_language_selection(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    
    if callback.data == "til_tugatish":
        # Tillarni saqlash va keyingi bosqichga o'tish
        await state.update_data(tillar=user_languages.get(user_id, {}))
        if user_id in user_languages:
            del user_languages[user_id]
        
        await state.set_state(Form.boshqa_tillar)
        await callback.message.edit_text("Bundan tashqari boshqa tillarni bilasizmi? (Bilgan tillaringizni yozing):")
        await callback.answer()
        return
    
    # Tanlangan tilni saqlash
    til = callback.data.split("_")[1]
    
    # Foizlarni tanlash uchun keyboard
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="25%", callback_data=f"foiz_{til}_25"))
    builder.add(types.InlineKeyboardButton(text="50%", callback_data=f"foiz_{til}_50"))
    builder.add(types.InlineKeyboardButton(text="75%", callback_data=f"foiz_{til}_75"))
    builder.add(types.InlineKeyboardButton(text="100%", callback_data=f"foiz_{til}_100"))
    builder.add(types.InlineKeyboardButton(text="Bekor qilish", callback_data=f"foiz_bekor"))
    
    await callback.message.edit_text(f"{til.capitalize()} tili bilish darajangiz?", reply_markup=builder.as_markup())
    await callback.answer()

# Foiz tanlovi uchun handler
@dp.callback_query(F.data.startswith("foiz_"), Form.tillar)
async def process_language_percentage(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    data_parts = callback.data.split("_")
    
    if data_parts[1] == "bekor":
        # Bekor qilish tugmasi bosilsa, oldingi keyboardni qayta yuboramiz
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Ingliz", callback_data="til_ingliz"))
        builder.add(types.InlineKeyboardButton(text="Rus", callback_data="til_rus"))
        builder.add(types.InlineKeyboardButton(text="Koreys", callback_data="til_koreys"))
        builder.add(types.InlineKeyboardButton(text="Tugatish", callback_data="til_tugatish"))
        
        await callback.message.edit_text("Tillarni bilish darajangizni tanlang:", reply_markup=builder.as_markup())
        await callback.answer()
        return
    
    til = data_parts[1]
    foiz = data_parts[2]
    
    # Foydalanuvchi tanlagan tillarni saqlash
    if user_id not in user_languages:
        user_languages[user_id] = {}
    
    user_languages[user_id][til] = f"{foiz}%"
    
    # Qolgan tillar uchun keyboard
    builder = InlineKeyboardBuilder()
    
    # Faqat tanlanmagan tillarni ko'rsatamiz
    if "ingliz" not in user_languages[user_id]:
        builder.add(types.InlineKeyboardButton(text="Ingliz", callback_data="til_ingliz"))
    if "rus" not in user_languages[user_id]:
        builder.add(types.InlineKeyboardButton(text="Rus", callback_data="til_rus"))
    if "koreys" not in user_languages[user_id]:
        builder.add(types.InlineKeyboardButton(text="Koreys", callback_data="til_koreys"))
    
    builder.add(types.InlineKeyboardButton(text="Tugatish", callback_data="til_tugatish"))
    
    await callback.message.edit_text(
        f"{til.capitalize()} tili {foiz}% qo'shildi.\nQo'shimcha tillar tanlang yoki Tugatish tugmasini bosing:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

# Boshqa tillarni qabul qilish
@dp.message(Form.boshqa_tillar)
async def process_other_languages(message: types.Message, state: FSMContext):
    await state.update_data(boshqa_tillar=message.text)
    await state.set_state(Form.reklama)
    
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Telegram", callback_data="reklama_telegram"))
    builder.add(types.InlineKeyboardButton(text="Instagram", callback_data="reklama_instagram"))
    builder.add(types.InlineKeyboardButton(text="Ish Bo'yicha reklamalardan", callback_data="reklama_ish"))
    builder.add(types.InlineKeyboardButton(text="Do'stim Taklif qildi", callback_data="reklama_do'st"))
    
    await message.answer("Reklama ma'lumotini qayerdan oldingiz?", reply_markup=builder.as_markup())

# Reklama manbasini qabul qilish
@dp.callback_query(F.data.startswith("reklama_"), Form.reklama)
async def process_ad_source(callback: types.CallbackQuery, state: FSMContext):
    source = callback.data.replace("reklama_", "")
    await state.update_data(reklama=source)
    
    # Barcha ma'lumotlarni yig'ish
    user_data = await state.get_data()
    
    # Tillarni formatlash
    tillar = user_data.get("tillar", {})
    tillar_str = ", ".join([f"{k.capitalize()} {v}" for k, v in tillar.items()]) if tillar else "Ko'rsatilmadi"
    
    # Ma'lumotlarni tayyorlash
    msg = (
        "📝 Yangi HR anketa:\n\n"
        f"👤 Ism: {user_data['ism']}\n"
        f"🎂 Tug'ilgan yili: {user_data['tugilgan_yili']}\n"
        f"📚 Ma'lumot: {user_data['malumot']}\n"
        f"📍 Viloyat: {user_data['viloyat']}\n"
        f"📞 Telefon: {user_data['telefon']}\n"
        f"💍 Turmush holati: {user_data['turmush']}\n"
        f"💼 Ish tajribasi: {user_data['ish_tajriba']}\n"
        f"⚔️ CRM ni BILISHI : {user_data['crm']}\n"
        f"🦾 Sotuv Texnikalari: {user_data['sotuv']}\n"
        f"💰 Maosh talabi: {user_data['oylik']}\n"
        f"⏳ Ish muddati: {user_data['muddat']}\n"
        f"🌐 Tillar: {tillar_str}\n"
        f"➕ Boshqa tillar: {user_data['boshqa_tillar']}\n"
        f"📢 Reklama manbasi: {user_data['reklama']}\n"
        
    )
    
    # Admin ga yuborish
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)
    await bot.send_message(chat_id=5515940993, text=msg)
    
    # Foydalanuvchiga javob
    await callback.message.edit_text(
        "Sizning so'rovingiz yuborildi! Tez orada siz bilan bog'lanamiz.\n\n"
        "Agar qo'shimcha savollaringiz bo'lsa, @aloqa_bot ga murojaat qiling."
    )
    await callback.answer()
    
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
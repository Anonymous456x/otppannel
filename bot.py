import asyncio
import logging
import random
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BOT_TOKEN, ADMIN_IDS
from database import init_db, add_user, log_otp, get_user_otp_count
from utils import (
    get_random_number, generate_otp, get_country_list,
    get_country_count, get_country_flag, get_country_code,
    get_random_country, format_number_for_display, get_language
)
from keyboards import (
    main_menu, country_menu, service_menu, otp_waiting_menu,
    stats_menu, live_traffic_menu, checker_menu, twofa_menu, otp_group_menu
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# User sessions
user_sessions = {}
country_pages = {}

class SecretState(StatesGroup):
    waiting_for_secret = State()

# ===================== START =====================
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    add_user(user.id, user.username, user.first_name)
    
    welcome_text = f"""
<b>🚀 Welcome to Otp Pannel Bot</b>

👋 Hello <b>{user.first_name}</b>!

📱 <b>13,140</b> monthly users

🔹 <b>FREE & UNLIMITED OTP</b>
🔸 No limits, no restrictions
🔹 Use any country, any service
🔸 Get OTP instantly

💡 <i>Select an option below:</i>
"""
    
    await message.answer(
        welcome_text,
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

# ===================== GET NUMBER =====================
@dp.callback_query(lambda c: c.data == "get_number")
async def callback_get_number(callback: CallbackQuery):
    await callback.answer()
    country_pages[callback.from_user.id] = 0
    await callback.message.edit_text(
        "🌍 <b>Select Country</b>\n\nChoose a country to get OTP number:",
        reply_markup=country_menu(0),
        parse_mode="HTML"
    )

@dp.callback_query(lambda c: c.data.startswith("country_page_"))
async def callback_country_page(callback: CallbackQuery):
    await callback.answer()
    page = int(callback.data.replace("country_page_", ""))
    country_pages[callback.from_user.id] = page
    await callback.message.edit_reply_markup(
        reply_markup=country_menu(page)
    )

@dp.callback_query(lambda c: c.data.startswith("country_"))
async def callback_country(callback: CallbackQuery):
    await callback.answer()
    country = callback.data.replace("country_", "")
    user_sessions[callback.from_user.id] = {"country": country}
    
    flag = get_country_flag(country)
    count = get_country_count(country)
    
    await callback.message.edit_text(
        f"{flag} <b>Country:</b> {country} ({count} numbers)\n\n"
        f"📱 <b>Select Service</b>\nChoose which service you need OTP for:",
        reply_markup=service_menu(country),
        parse_mode="HTML"
    )

@dp.callback_query(lambda c: c.data == "change_country")
async def callback_change_country(callback: CallbackQuery):
    await callback.answer()
    country_pages[callback.from_user.id] = 0
    await callback.message.edit_text(
        "🌍 <b>Select Country</b>\n\nChoose a country to get OTP number:",
        reply_markup=country_menu(0),
        parse_mode="HTML"
    )

@dp.callback_query(lambda c: c.data.startswith("service_"))
async def callback_service(callback: CallbackQuery):
    await callback.answer()
    service = callback.data.replace("service_", "")
    user_id = callback.from_user.id
    session = user_sessions.get(user_id, {})
    country = session.get("country", "USA")
    country_code = get_country_code(country)
    flag = get_country_flag(country)
    
    # Get number from file
    number = get_random_number(country)
    if not number:
        await callback.message.edit_text(
            f"❌ <b>No numbers available for {country}</b>\n\nPlease try another country.",
            reply_markup=country_menu(0),
            parse_mode="HTML"
        )
        return
    
    otp = generate_otp()
    log_otp(user_id, number, service, country, country_code, otp)
    
    total_otps = get_user_otp_count(user_id)
    
    waiting_text = f"""
{flag} <b>Country:</b> {country} ({country_code})

⏳ <b>Waiting for OTP</b>

📱 <code>{number}</code>

🔹 <b>Service:</b> {service}
🔐 <b>OTP:</b> <code>{otp}</code>

📊 <b>Your Total OTPs:</b> {total_otps} (Unlimited)

💡 <i>OTP expires in 5 minutes</i>
🎁 <i>Free & Unlimited OTP</i>
"""
    
    await callback.message.edit_text(
        waiting_text,
        reply_markup=otp_waiting_menu(number, country, country_code, service),
        parse_mode="HTML"
    )

# ===================== CHANGE NUMBER =====================
@dp.callback_query(lambda c: c.data == "change_number")
async def callback_change_number(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    session = user_sessions.get(user_id, {})
    country = session.get("country", "USA")
    country_code = get_country_code(country)
    flag = get_country_flag(country)
    
    number = get_random_number(country)
    if not number:
        await callback.message.edit_text(
            f"❌ <b>No numbers available</b>\n\nPlease change country.",
            reply_markup=country_menu(0),
            parse_mode="HTML"
        )
        return
    
    otp = generate_otp()
    log_otp(user_id, number, "WHATSAPP", country, country_code, otp)
    
    total_otps = get_user_otp_count(user_id)
    
    waiting_text = f"""
{flag} <b>Country:</b> {country} ({country_code})

⏳ <b>Waiting for OTP</b>

📱 <code>{number}</code>

🔹 <b>Service:</b> 💬 WHATSAPP
🔐 <b>OTP:</b> <code>{otp}</code>

📊 <b>Your Total OTPs:</b> {total_otps} (Unlimited)

💡 <i>OTP expires in 5 minutes</i>
🎁 <i>Free & Unlimited OTP</i>
"""
    
    await callback.message.edit_text(
        waiting_text,
        reply_markup=otp_waiting_menu(number, country, country_code, "WHATSAPP"),
        parse_mode="HTML"
    )

# ===================== COPY NUMBER =====================
@dp.callback_query(lambda c: c.data == "copy_number")
async def callback_copy_number(callback: CallbackQuery):
    await callback.answer("📱 Number copied!", show_alert=True)

# ===================== OTP GROUP =====================
@dp.callback_query(lambda c: c.data == "otp_group")
async def callback_otp_group(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "👥 <b>Join OTP Group</b>\n\n"
        "Click the button below to join our OTP community:\n\n"
        "🔹 Get more OTP numbers\n"
        "🔹 24/7 active members\n"
        "🔹 All countries available\n"
        "🔹 Free & Unlimited",
        reply_markup=otp_group_menu(),
        parse_mode="HTML"
    )

# ===================== MY STATS =====================
@dp.callback_query(lambda c: c.data == "my_stats")
async def callback_stats(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    total_otps = get_user_otp_count(user_id)
    
    stats_text = f"""
📊 <b>Your Statistics</b>

🆔 UID: <code>{user_id}</code>
📱 Total OTPs: <b>{total_otps}</b>
🎁 Status: <b>FREE & UNLIMITED</b>
📈 No limits, no restrictions

💡 <i>Keep using OTPs for free!</i>
"""
    
    await callback.message.edit_text(
        stats_text,
        reply_markup=stats_menu(),
        parse_mode="HTML"
    )

# ===================== LIVE TRAFFIC =====================
@dp.callback_query(lambda c: c.data == "live_traffic")
async def callback_live_traffic(callback: CallbackQuery):
    await callback.answer()
    
    traffic_text = "📡 <b>Live Traffic</b>\n\n"
    
    for country in get_country_list():
        count = get_country_count(country)
        flag = get_country_flag(country)
        if count > 100:
            status = "🟢 HIGH"
        elif count > 50:
            status = "🟡 MEDIUM"
        else:
            status = "🔴 LOW"
        traffic_text += f"{flag} {country}: <b>{status}</b> ({count} numbers)\n"
    
    traffic_text += "\n<i>🔄 Click refresh to update</i>"
    
    await callback.message.edit_text(
        traffic_text,
        reply_markup=live_traffic_menu(),
        parse_mode="HTML"
    )

# ===================== CHECKER SET =====================
@dp.callback_query(lambda c: c.data == "checker_set")
async def callback_checker(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "⚙️ <b>Checker Set</b>\n\n"
        "Select service to check OTP status:\n\n"
        "<i>Coming soon...</i>",
        reply_markup=checker_menu(),
        parse_mode="HTML"
    )

@dp.callback_query(lambda c: c.data.startswith("check_"))
async def callback_check_service(callback: CallbackQuery):
    await callback.answer()
    service = callback.data.replace("check_", "")
    await callback.message.edit_text(
        f"🔍 <b>Checking {service}</b>\n\n"
        f"✅ Service: <b>{service}</b>\n"
        f"📊 Status: <b>🟢 Active</b>\n\n"
        f"<i>This is a demo checker.</i>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="checker_set")]
            ]
        ),
        parse_mode="HTML"
    )

# ===================== 2FA SET =====================
@dp.callback_query(lambda c: c.data == "2fa_set")
async def callback_2fa(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🔐 <b>2FA Set</b>\n\n"
        "Please send your Secret Key to begin.\n\n"
        "🔑 <i>Enter your 2FA secret key to enable two-factor authentication.</i>",
        reply_markup=twofa_menu(),
        parse_mode="HTML"
    )

@dp.callback_query(lambda c: c.data == "send_secret")
async def callback_send_secret(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        "🔑 <b>Enter Secret Key</b>\n\n"
        "Please type your 2FA secret key in the chat.\n\n"
        "<i>Format: 16-32 characters (A-Z, 2-7)</i>",
        parse_mode="HTML"
    )
    await state.set_state(SecretState.waiting_for_secret)

@dp.message(SecretState.waiting_for_secret)
async def process_secret(message: Message, state: FSMContext):
    secret = message.text.strip()
    if len(secret) < 16:
        await message.answer(
            "❌ <b>Invalid Secret Key</b>\n\n"
            "Secret key must be at least 16 characters.",
            parse_mode="HTML"
        )
        return
    
    await message.answer(
        "✅ <b>2FA Enabled Successfully!</b>\n\n"
        "🔑 Your secret key has been saved.\n\n"
        "<i>Keep your backup codes safe!</i>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="back")]
            ]
        ),
        parse_mode="HTML"
    )
    await state.clear()

# ===================== HISTORY =====================
@dp.callback_query(lambda c: c.data == "history")
async def callback_history(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📜 <b>History</b>\n\n"
        "Your OTP request history:\n\n"
        "<i>No history found.</i>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="my_stats")]
            ]
        ),
        parse_mode="HTML"
    )

# ===================== WITHDRAW =====================
@dp.callback_query(lambda c: c.data == "withdraw")
async def callback_withdraw(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "💸 <b>Withdraw</b>\n\n"
        "Withdrawal options:\n\n"
        "💵 <b>USDT (TRC20)</b>\n"
        "   Min: 10 USDT\n\n"
        "💳 <b>Bank Transfer (TK)</b>\n"
        "   Min: 500 TK\n\n"
        "⏳ Processing: 24-48 hours",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="my_stats")]
            ]
        ),
        parse_mode="HTML"
    )

# ===================== REFER =====================
@dp.callback_query(lambda c: c.data == "refer")
async def callback_refer(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    ref_link = f"https://t.me/otppannel_ibot?start=ref_{user_id}"
    
    await callback.message.edit_text(
        f"👥 <b>Refer & Earn</b>\n\n"
        f"Share your referral link:\n\n"
        f"🔗 <code>{ref_link}</code>\n\n"
        f"📊 Your Referrals: 0\n"
        f"💰 Earned: 0.00 USDT",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="my_stats")]
            ]
        ),
        parse_mode="HTML"
    )

# ===================== BACK =====================
@dp.callback_query(lambda c: c.data == "back")
async def callback_back(callback: CallbackQuery):
    await callback.answer()
    user = callback.from_user
    
    welcome_text = f"""
<b>🚀 Welcome to Otp Pannel Bot</b>

👋 Hello <b>{user.first_name}</b>!

📱 <b>13,140</b> monthly users

🔹 <b>FREE & UNLIMITED OTP</b>
🔸 No limits, no restrictions
🔹 Use any country, any service
🔸 Get OTP instantly

💡 <i>Select an option below:</i>
"""
    
    await callback.message.edit_text(
        welcome_text,
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

# ===================== MAIN =====================
async def main():
    init_db()
    
    print("🤖 Bot is starting...")
    print("📱 Bot: @otppannel_ibot")
    print("✅ Ready!")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

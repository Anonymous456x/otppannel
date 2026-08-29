from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import get_country_list, get_country_count, get_country_flag

def main_menu():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📱 Get Number", callback_data="get_number")
    )
    builder.row(
        InlineKeyboardButton(text="📊 My stats", callback_data="my_stats"),
        InlineKeyboardButton(text="📡 Live Traffic", callback_data="live_traffic")
    )
    builder.row(
        InlineKeyboardButton(text="⚙️ Checker Set", callback_data="checker_set")
    )
    builder.row(
        InlineKeyboardButton(text="🔐 2FA Set", callback_data="2fa_set")
    )
    builder.row(
        InlineKeyboardButton(text="👥 OTP Group", callback_data="otp_group")
    )
    
    return builder.as_markup()

def country_menu(page=0):
    builder = InlineKeyboardBuilder()
    
    countries = get_country_list()
    per_page = 5
    total_pages = (len(countries) + per_page - 1) // per_page
    
    start = page * per_page
    end = min(start + per_page, len(countries))
    
    for country in countries[start:end]:
        count = get_country_count(country)
        flag = get_country_flag(country)
        status = "🟢" if count > 100 else "🟡" if count > 50 else "🔴"
        builder.row(
            InlineKeyboardButton(
                text=f"{flag} {country} ({count}) {status}",
                callback_data=f"country_{country}"
            )
        )
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"country_page_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"country_page_{page+1}"))
    
    if nav_buttons:
        builder.row(*nav_buttons)
    
    builder.row(
        InlineKeyboardButton(text="🔙 Back", callback_data="back")
    )
    
    return builder.as_markup()

def service_menu(country):
    builder = InlineKeyboardBuilder()
    
    services = ["WHATSAPP", "TELEGRAM", "DISCORD", "FACEBOOK", "INSTAGRAM", "GMAIL"]
    emojis = ["💬", "✈️", "🎮", "📘", "📸", "📧"]
    
    for i, service in enumerate(services):
        builder.row(
            InlineKeyboardButton(
                text=f"{emojis[i]} {service}",
                callback_data=f"service_{service}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text="🌍 Change Country", callback_data="change_country"),
        InlineKeyboardButton(text="🔙 Back", callback_data="back")
    )
    
    return builder.as_markup()

def otp_waiting_menu(number, country, country_code, service):
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text=f"📱 {number}",
            callback_data="copy_number"
        )
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Change Number", callback_data="change_number"),
        InlineKeyboardButton(text="🌍 Change Country", callback_data="change_country")
    )
    builder.row(
        InlineKeyboardButton(text="👥 OTP Group", callback_data="otp_group")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Back", callback_data="back")
    )
    
    return builder.as_markup()

def stats_menu():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📜 History", callback_data="history"),
        InlineKeyboardButton(text="💸 Withdraw", callback_data="withdraw")
    )
    builder.row(
        InlineKeyboardButton(text="👥 Refer & Earn", callback_data="refer")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Back", callback_data="back")
    )
    
    return builder.as_markup()

def live_traffic_menu():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🔄 Refresh", callback_data="live_traffic")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Back", callback_data="back")
    )
    
    return builder.as_markup()

def checker_menu():
    builder = InlineKeyboardBuilder()
    
    services = ["WHATSAPP", "TELEGRAM", "DISCORD", "FACEBOOK", "INSTAGRAM", "GMAIL"]
    for service in services:
        builder.row(
            InlineKeyboardButton(
                text=f"🔍 {service}",
                callback_data=f"check_{service}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text="🔙 Back", callback_data="back")
    )
    
    return builder.as_markup()

def twofa_menu():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🔑 Send Secret Key", callback_data="send_secret")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Back", callback_data="back")
    )
    
    return builder.as_markup()

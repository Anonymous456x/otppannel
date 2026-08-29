import random
import os

NUMBER_FOLDER = "numbers"

COUNTRIES = {
    "USA": {"code": "US", "file": "usa_fake_numbers.txt", "flag": "🇺🇸"},
    "UKRAINE": {"code": "UA", "file": "ukraine_fake_numbers.txt", "flag": "🇺🇦"},
    "RUSSIA": {"code": "RU", "file": "russia_fake_numbers.txt", "flag": "🇷🇺"},
    "PAKISTAN": {"code": "PK", "file": "pakistan_fake_numbers.txt", "flag": "🇵🇰"},
    "AUSTRIA": {"code": "AT", "file": "austria_fake_numbers.txt", "flag": "🇦🇹"},
    "ALBANIA": {"code": "AL", "file": "albania_fake_numbers.txt", "flag": "🇦🇱"},
    "AFGHANISTAN": {"code": "AF", "file": "afghanistan_fake_numbers.txt", "flag": "🇦🇫"},
    "MALI": {"code": "ML", "file": "Mali_18-53.txt", "flag": "🇲🇱"},
    "GABON": {"code": "GA", "file": "Gabon_Numbers.txt", "flag": "🇬🇦"},
    "GREENLAND": {"code": "GL", "file": "greenland_fake_numbers.txt", "flag": "🇬🇱"},
    "MALAYSIA": {"code": "MY", "file": "malaysia_fake_numbers.txt", "flag": "🇲🇾"},
    "INDIA": {"code": "IN", "file": "india_fake_numbers.txt", "flag": "🇮🇳"},
}

def load_numbers(country_name):
    country_data = COUNTRIES.get(country_name)
    if not country_data:
        return []
    
    filepath = os.path.join(NUMBER_FOLDER, country_data["file"])
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, "r", encoding="utf-8") as f:
        numbers = [line.strip() for line in f if line.strip()]
    
    return numbers

def get_random_number(country_name):
    numbers = load_numbers(country_name)
    if not numbers:
        return None
    return random.choice(numbers)

def get_country_list():
    return list(COUNTRIES.keys())

def get_country_code(country_name):
    return COUNTRIES.get(country_name, {}).get("code", "")

def get_country_flag(country_name):
    return COUNTRIES.get(country_name, {}).get("flag", "🌍")

def get_country_count(country_name):
    return len(load_numbers(country_name))

def generate_otp():
    return str(random.randint(100000, 999999))

def format_number_for_display(number):
    if len(number) <= 8:
        return number
    return f"{number[:4]}**{number[-4:]}"

def get_random_country():
    countries = get_country_list()
    available = [c for c in countries if get_country_count(c) > 0]
    if not available:
        return "USA"
    return random.choice(available)

def get_language(country):
    languages = {
        "MALI": "Indonesian",
        "GABON": "French",
        "USA": "English",
        "UKRAINE": "Ukrainian",
        "RUSSIA": "Russian",
        "PAKISTAN": "Urdu",
        "AUSTRIA": "German",
        "ALBANIA": "Albanian",
        "AFGHANISTAN": "Pashto",
        "GREENLAND": "Greenlandic",
        "MALAYSIA": "Malay",
        "INDIA": "Hindi",
    }
    return languages.get(country, "English")

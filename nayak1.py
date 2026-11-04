# NAYAK.py — COMPLETE FINAL (Fully Rebranded)
import logging
import asyncio
import os
import json
import random
import time
import re
import urllib.parse
import urllib.request
from typing import Set, Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone, timedelta
import io
import tempfile
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
from pathlib import Path
from telegram import (
    Update, ChatPermissions, ReactionTypeEmoji, ReplyParameters,
    InlineKeyboardButton, InlineKeyboardMarkup,
)
from telegram.error import RetryAfter, TimedOut, NetworkError, BadRequest, Forbidden
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes,
    CallbackQueryHandler,
)
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.CRITICAL)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("telegram").setLevel(logging.CRITICAL)

# ═══════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════
TOKENS_FILE = "Nayak_tokens.json"
GROUPS_FILE = "Nayak_groups.json"
SUDO_FILE = "Nayak_sudo.json"
PFP_FILE = "Nayak_pfp.json"
TEMPLATES_FILE = "NAYAK_templates.json"

OWNER_ID = int(os.environ.get("OWNER_ID","8463727303 "))

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(SCRIPT_DIR, "hosted_files")
LOG_DIR = os.path.join(SCRIPT_DIR, "host_logs")
FONT_DIR = "fonts"
DOWNLOAD_DIR = "downloads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

MENU_VIDEO_MAIN = "https://files.catbox.moe/m90kxp.mp4"
MENU_MASTER_USERNAME = "@Aryathe1"
MENU_BOT_NAME = "ARYA "
MENU_VERSION = "V 6 • AryA"
OVER_VIDEO_URL = "https://files.catbox.moe/4mv7tx.mp4"

NAYAK_SIG = "𓆩💢𓆪 NAYAK����𝙾𝙽 𝐓𝙾𝙿🕸️⃟𓆪 𓆩💢𓆪"
NAYAK_SIG_PAPA = "𓆩💢𓆪 𝑎AYAK����𝐏𝙰𝙿𝙰 𝙾𝙽 𝐓𝙾𝙿🕸️⃟𓆪 𓆩💢𓆪"

SPAM_EMOJIS = ["🩵","❤️‍🩹","💔","💟","💌","💕","💞","💓","💗","💖",
    "💝","💘","🩷","🤍","🩶","🖤","🤎","💜","💙","💛","🧡","❤️"]
SPAM1_TEMPLATE = "{target} 𝙇𝙐𝙉𝘿  𝘾𝙃𝙐𝙎 ✰ཽ{emoji}࿐"
SPAM2_TEMPLATE = "{target} 𝚃𝙴𝚁𝙸 𝙼𝙰 𝚁𝙰𝙽𝙳𝙸 ✰ཽ{emoji}࿐"
SPAM3_TEMPLATE = "{target} SཽUཽNཽ ƬᴇƦᎥ Mꫝꫝ ƇӇƲƊ ƓꫝƳɪ ⏤͟͟͞͞{emoji}"

BASE_TOKENS = [
"8600501378:AAHrV6znwIv_KZKMGxf8pgbHEx5XYHMNEHE",
"8920042906:AAGLhj0mdzPRAuFHP9BtuxAmHRBUU5FErqc",
"8818136194:AAFxz5DoLeBCQfSQtjvJmGko4gJBWmHIe8U",
"8715337839:AAGARPfdjc4VvwUYQdkjT4k6GARqgQDdyTU",
"8304224479:AAGFzI7xNjhxi_DG2Hokr-fRPrLNgXna3Zg",
"8950122989:AAEXsa8ORnoA25HK9YtuRucDTfSsyfIxU_Y",
"8694007493:AAF8ltyxSPcZS-_4-poHL6oWP3MA1G6Ni8I",
"8406363410:AAH8aAJtld4285oCFYtFQ8OQQt3Uk33fTUo",
"8780344482:AAHS_hL_XoLRCVn6DLUX8Uu0UwjgqjfzCYU",
"8958091021:AAGKCZEuyxLCSAG0NoNgb3DMlu83NnlxLOo"
]

RANDOM_EMOJIS = ["🎀","🌸","🔥","⚡","💀","👑","🌊","💎","🐉","🌙","☄️","🌺","💫","✨","🦋","🪷","🔱","🌟","🩸","⚔️","🫧","🌈","🌀","💥","🌑","🔮","🧿","🪬","🌿","🍀","🫐","🍇","🍒","🌹","🌷","🌻","🌼","🏵️","❄️","🌬️","🎭","🎪","🎯","🎲","🎸","🎵","🎶","🎤","🎹","🥀"]
SUFFIX_EMOJIS = ["🌸","🌺","🌻","🌹","🪷","🌷","💮","🏵️","✨","💫","⭐","🌟","💥","🔥","⚡","❄️","🌊","🫧","💧","🌀","🌈","🌙","☄️","🌟","💎","🔮","🧿","🪬","👑","💀","🦋","🐉","🍀","🌿","🍃","🫐","🍇","🍒","🌙","🌑","🩸","⚔️","🔱","🌌","🌠","☠️","🕊️","🌋"]
_SUFFIX_TPL = " 𓂃{e}་༘"

def rnd_suffix(): return _SUFFIX_TPL.format(e=random.choice(SUFFIX_EMOJIS))
def rnd_emoji(): return random.choice(RANDOM_EMOJIS)

WRAP_L = ["꧁","⭅╡","♛","𖤍","❦","⚡","☄️","💀","🌟","🔱","🌊","✨","💎","👑","🔥"]
WRAP_R = ["꧂","╞⭆","♛","𖤍","❦","🌙","💎","👑","☄️","🔱","🌊","⚡","💀","🔥","✨"]
_CHUD_WORDS = ["LUND", "TBKC", "TBR", "TMR", "aarey चुदोड़े", "BHEN CUDALE"]

# ═══════════════════════════════════════════════════════════
# PERSISTENCE
# ═══════════════════════════════════════════════════════════
def _load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path) as f: return json.load(f)
    except Exception: pass
    return default

def _save_json(path, data):
    try:
        with open(path, "w") as f: json.dump(data, f)
    except Exception as e: logger.error(f"_save_json({path}): {e}")

known_chats: Set[int] = set(_load_json(GROUPS_FILE, []))
SUDO_USERS: Set[int] = set(int(x) for x in _load_json(SUDO_FILE, []))
SUDO_USERS.add(OWNER_ID)
_pfp_pools: Dict[str, List[str]] = _load_json(PFP_FILE, {})

all_bot_instances: List[Any] = []
all_apps: List[Any] = []

mute_chats: Set[int] = set()
ncdel_chats: Set[int] = set()
autoreact_chats: Dict[int, str] = {}
autoreply_chats: Dict[int, str] = {}
targetreply_chats: Dict[int, dict] = {}
targetslide_chats: Dict[int, dict] = {}
ncwar_targets: Dict[int, str] = {}
_multiwar_active: Dict[int, bool] = {}
pfploop_active: Dict[int, bool] = {}
replyflood_chats: Dict[int, str] = {}

custom_templates: Dict[str, str] = _load_json(TEMPLATES_FILE, {})
_nc_send_gap: Optional[float] = None
BOT_START_TIME: float = time.monotonic()
_seen: Set[tuple] = set()

def is_admin(uid: int) -> bool:
    return uid == OWNER_ID or uid in SUDO_USERS

_GATE = "𝐒𝚃𝙰𝚈 𝐀𝚆𝙰𝚈 𝐊𝙸𝙳 𝐓𝙷𝙸𝚂 𝐈𝚂 𝐓𝙷𝙴 𝐌𝙾𝚂𝚃 𝐀𝙳𝚅𝙰𝙽𝙲𝙴 𝐁𝙾𝚃 𝐍𝙾𝚃 𝐅𝙾𝚁 𝐍𝙾𝚁𝙼𝙸𝙴"

# ═══════════════════════════════════════════════════════════
# HOSTED FILE DETECTION
# ═══════════════════════════════════════════════════════════
hosted_scripts: Dict[int, Dict[str, Any]] = {}
hosted_menus: Dict[int, Dict[str, Dict[str, Any]]] = {}

def _host_active(chat_id: int) -> bool:
    if chat_id not in hosted_scripts: return False
    for sid in ("script1", "script2"):
        if sid in hosted_scripts[chat_id]:
            proc = hosted_scripts[chat_id][sid].get("process")
            if proc and proc.returncode is None: return True
    return False

MANAGEMENT_CMDS = {
    "menu", "menuall", "host1", "host2", "stophost", "hoststat", "hostlog",
    "menufile1", "menufile2", "addsudo", "removesudo", "sudolist",
    "bots", "addbot", "addallbots", "promotebot", "botname",
    "status", "uptime", "ping", "globalstop", "stop",
}

# ═══════════════════════════════════════════════════════════
# LOGO / IMAGE HELPERS
# ═══════════════════════════════════════════════════════════
FONTS_TO_DOWNLOAD = {
    "Anton": "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf",
    "BebasNeue": "https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf",
    "Bungee": "https://github.com/google/fonts/raw/main/ofl/bungee/Bungee-Regular.ttf",
    "BlackOpsOne": "https://github.com/google/fonts/raw/main/ofl/blackopsone/BlackOpsOne-Regular.ttf",
    "Bangers": "https://github.com/google/fonts/raw/main/ofl/bangers/Bangers-Regular.ttf",
    "RussoOne": "https://github.com/google/fonts/raw/main/ofl/russoone/RussoOne-Regular.ttf",
    "Staatliches": "https://github.com/google/fonts/raw/main/ofl/staatliches/Staatliches-Regular.ttf",
    "Orbitron": "https://github.com/google/fonts/raw/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf",
    "SairaStencil": "https://github.com/google/fonts/raw/main/ofl/sairastencilone/SairaStencilOne-Regular.ttf",
    "Teko": "https://github.com/google/fonts/raw/main/ofl/teko/Teko%5Bwght%5D.ttf",
}
_font_paths: List[str] = []
_fonts_loaded = False

def _download_font(name, url):
    path = os.path.join(FONT_DIR, f"{name}.ttf")
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        try: ImageFont.truetype(path, 40); return path
        except Exception: os.remove(path)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r: data = r.read()
        if len(data) < 10000: return None
        with open(path, "wb") as f: f.write(data)
        ImageFont.truetype(path, 40); return path
    except Exception: return None

def load_all_fonts():
    global _font_paths, _fonts_loaded
    if _fonts_loaded: return _font_paths
    os.makedirs(FONT_DIR, exist_ok=True)
    paths = []
    for name, url in FONTS_TO_DOWNLOAD.items():
        p = _download_font(name, url)
        if p: paths.append(p)
    for sf in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","DejaVuSans-Bold.ttf","arialbd.ttf"]:
        try: ImageFont.truetype(sf, 40); paths.append(sf)
        except Exception: pass
    if not paths: paths = [None]
    _font_paths = paths; _fonts_loaded = True
    return _font_paths

def _get_font(size):
    if not _font_paths: return ImageFont.load_default()
    fp = random.choice(_font_paths)
    if fp is None: return ImageFont.load_default()
    try: return ImageFont.truetype(fp, size)
    except Exception: return ImageFont.load_default()

IMG_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def _bing_image_search(query):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    req = urllib.request.Request(url, headers=IMG_HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    urls = re.findall(r'"murl":"(https?://[^"]+?)"', html)
    urls += re.findall(r"&quot;murl&quot;:&quot;(https?://[^&]+?)&quot;", html)
    good = []
    for u in set(urls):
        if any(x in u.lower() for x in [".jpg",".jpeg",".png",".webp"]): good.append(u)
    return good

def _pinterest_html(query):
    url = f"https://in.pinterest.com/search/pins/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=IMG_HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    urls = re.findall(r'https://i\.pinimg\.com/[^\s"\\]+\.(?:jpg|jpeg|png|webp)', html)
    urls = [u for u in urls if "/originals/" in u or "/736x/" in u or "/564x/" in u]
    return list(set(urls))

def _age_to_word(age):
    if age <= 0: return ""
    if age <= 2: return "baby"
    if age <= 4: return "toddler"
    if age <= 12: return "kid"
    if age <= 18: return "teenage"
    if age <= 25: return "young"
    if age <= 45: return "adult"
    if age <= 60: return "middle aged"
    return "old"

def _build_logo_queries(gender, age):
    g = "boy" if gender == "boy" else "girl"
    age_w = _age_to_word(age)
    if age_w: return [f"{age_w} {g} portrait photography", f"{age} year old {g} dp", f"{age_w} {g} stylish photo", f"{g} {age} years attitude dp"]
    return [f"stylish {g} portrait", f"{g} attitude dp hd", f"handsome {g}" if gender == "boy" else f"beautiful {g}"]

def _fetch_best_image(queries, min_size=5000, min_wh=250):
    random.shuffle(queries)
    all_images = []
    for q in queries[:4]:
        try:
            imgs = _bing_image_search(q)
            if imgs:
                all_images.extend(imgs)
                if len(all_images) >= 25: break
        except Exception: pass
    if len(all_images) < 8:
        for q in queries[:3]:
            try:
                imgs = _pinterest_html(q)
                if imgs:
                    all_images.extend(imgs)
                    if len(all_images) >= 20: break
            except Exception: pass
    if not all_images: raise Exception("Koi image nahi mili.")
    all_images = list(set(all_images)); random.shuffle(all_images)
    for url in all_images[:15]:
        try:
            req = urllib.request.Request(url, headers={**IMG_HEADERS, "Referer": "https://www.bing.com/"})
            with urllib.request.urlopen(req, timeout=20) as r: data = r.read()
            if len(data) < min_size: continue
            try:
                im = Image.open(io.BytesIO(data)); w, h = im.size
                if w < min_wh or h < min_wh: continue
                im.verify()
            except Exception: continue
            return url, data
        except Exception: continue
    raise Exception("Image download fail.")

def fetch_random_image(gender="boy", age=0): return _fetch_best_image(_build_logo_queries(gender, age))
def fetch_famous_image(term):
    return _fetch_best_image([f"{term} famous", f"famous {term}", f"{term} hd portrait", f"{term} 4k"], min_size=8000, min_wh=300)

def _center_position(draw, text, font, W, H, sw=0):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=sw)
    tw_ = bbox[2] - bbox[0]; th_ = bbox[3] - bbox[1]
    return (W - tw_) // 2 - bbox[0], (H - th_) // 2 - bbox[1], tw_, th_

def _style_simple(draw, text, font, x, y, col=(220,20,20), stroke=(255,255,255)):
    for r in range(20, 0, -2):
        draw.text((x+r,y), text, font=font, fill=(*col, 50))
        draw.text((x-r,y), text, font=font, fill=(*col, 50))
        draw.text((x,y+r), text, font=font, fill=(*col, 50))
        draw.text((x,y-r), text, font=font, fill=(*col, 50))
    draw.text((x+6,y+6), text, font=font, fill=(0,0,0,240))
    draw.text((x,y), text, font=font, fill=(*stroke, 255), stroke_width=8, stroke_fill=col)

STYLES = [
    lambda d,t,f,x,y,tw,th: _style_simple(d,t,f,x,y,(220,20,20),(255,255,255)),
    lambda d,t,f,x,y,tw,th: _style_simple(d,t,f,x,y,(255,0,60),(255,255,255)),
    lambda d,t,f,x,y,tw,th: _style_simple(d,t,f,x,y,(255,90,0),(255,230,100)),
    lambda d,t,f,x,y,tw,th: _style_simple(d,t,f,x,y,(0,220,220),(220,250,255)),
    lambda d,t,f,x,y,tw,th: _style_simple(d,t,f,x,y,(230,180,40),(255,255,255)),
]

def create_logo(img_bytes, name, output_path, darken=0.65):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    W, H = img.size
    target = 1080
    if W < H: new_w, new_h = target, int(H * (target / W))
    else: new_h, new_w = target, int(W * (target / H))
    img = img.resize((new_w, new_h), Image.LANCZOS)
    if new_w > new_h:
        left = (new_w - target) // 2
        img = img.crop((left, 0, left + target, new_h))
    else:
        top = (new_h - target) // 2
        img = img.crop((0, top, new_w, top + target))
    tw, th = target, target
    img = ImageEnhance.Brightness(img).enhance(darken)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    vig = Image.new("L", (tw, th), 0); vd = ImageDraw.Draw(vig)
    max_r = int((tw**2 + th**2)**0.5 / 2); cx, cy = tw//2, th//2
    for i in range(40):
        a = int(140 * (i / 40))
        vd.ellipse([cx-max_r+i*4, cy-max_r+i*4, cx+max_r-i*4, cy+max_r-i*4], fill=255-a)
    vig = vig.filter(ImageFilter.GaussianBlur(80))
    black = Image.new("RGB", (tw, th), (0,0,0))
    img = Image.composite(img, black, vig).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    text = name.upper().strip()
    base_size = int(tw * 0.26); font = _get_font(base_size); size = base_size
    tmp = Image.new("RGB", (10,10)); td = ImageDraw.Draw(tmp)
    while size > 50:
        bbox = td.textbbox((0,0), text, font=font, stroke_width=10)
        if bbox[2]-bbox[0] < tw-100: break
        size -= 8; font = _get_font(size)
    x, y, tw_, th_ = _center_position(draw, text, font, tw, th, sw=10)
    try: random.choice(STYLES)(draw, text, font, x, y, tw_, th_)
    except Exception:
        draw.text((x,y), text, font=font, fill=(255,255,255), stroke_width=8, stroke_fill=(200,10,10))
    try:
        wm_font = _get_font(30)
        wb = draw.textbbox((0,0), "⚡ ARYA ⚡", font=wm_font)
        draw.text((tw-(wb[2]-wb[0])-25, th-55), "⚡ ARYA ⚡", font=wm_font, fill=(255,255,255,220), stroke_width=2, stroke_fill=(0,0,0))
    except Exception: pass
    img.convert("RGB").save(output_path, "JPEG", quality=95)
    return output_path

# ═══════════════════════════════════════════════════════════
# TASK CONTROLLER
# ═══════════════════════════════════════════════════════════
class TaskController:
    def __init__(self):
        self.tasks: Dict[str, asyncio.Task] = {}
        self.events: Dict[str, asyncio.Event] = {}
    def _k(self, cid, t): return f"{cid}::{t}"
    async def start(self, cid, t, factory):
        await self.stop(cid, t)
        k = self._k(cid, t); ev = asyncio.Event(); self.events[k] = ev
        async def _wrap():
            try: await factory(ev)
            except asyncio.CancelledError: pass
            except Exception as e: logger.error(f"Task {k}: {e}")
            finally: self.tasks.pop(k, None); self.events.pop(k, None)
        self.tasks[k] = asyncio.create_task(_wrap())
    async def stop(self, cid, t):
        k = self._k(cid, t)
        ev = self.events.pop(k, None); task = self.tasks.pop(k, None)
        if ev: ev.set()
        if task and not task.done():
            try: await asyncio.wait_for(asyncio.shield(task), timeout=0.5)
            except Exception: pass
            if not task.done():
                task.cancel()
                try: await asyncio.wait_for(asyncio.shield(task), timeout=4.0)
                except Exception: pass
        return bool(ev or task)
    async def stop_all(self, cid):
        prefix = f"{cid}::"
        types = {k[len(prefix):] for k in list(self.tasks)+list(self.events) if k.startswith(prefix)}
        results = await asyncio.gather(*[self.stop(cid, t) for t in types], return_exceptions=True)
        return sum(1 for r in results if r is True)
    def running(self, cid, t):
        k = self._k(cid, t)
        return k in self.tasks and not self.tasks[k].done()

tc = TaskController()

async def _wait_ev(ev, secs):
    if secs <= 0: return ev.is_set()
    try: await asyncio.wait_for(ev.wait(), timeout=secs); return True
    except asyncio.TimeoutError: return False

# ═══════════════════════════════════════════════════════════
# FACTORIES
# ═══════════════════════════════════════════════════════════
def _last(): return [None]

def _pure_nc_factory(txt):
    last = _last()
    tmpl = [
        lambda t,e,s: f"꧁{t}꧂{s}", lambda t,e,s: f"⚡{t}🔥{s}",
        lambda t,e,s: f"💀{t}👑{s}", lambda t,e,s: f"𖤍{t}✦{s}",
        lambda t,e,s: f"♛{t}☄️{s}", lambda t,e,s: f"🌊{t}💎{s}",
        lambda t,e,s: f"{e}{t}{s}",
    ]
    def _f():
        fn = random.choice(tmpl)
        c = fn(txt, rnd_emoji(), rnd_suffix())[:255]
        if c == last[0]: c = fn(txt, rnd_emoji(), rnd_suffix())[:255]
        last[0] = c; return c
    return _f

def _lean_nc_factory(txt):
    sfx = ["", " ·", " •", " .", " ⁺", " ⁻", " ˙", " ˢ", " ᵒ", " ᵃ", " ˣ", " ⁿ", " ᵗ", " ᵉ",
           " .·", " ··", " •·", " ·•", " ..", "  ·", " ⌁", " ∘", " ∙", " ⋅", " ◦", " ∵", " ∶"]
    idx = [0]; last = [None]
    def _f():
        c = (txt + sfx[idx[0] % len(sfx)])[:255]
        idx[0] += 1
        if c == last[0]:
            c = (txt + sfx[idx[0] % len(sfx)])[:255]; idx[0] += 1
        last[0] = c; return c
    return _f

_BOLD_MAP = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗")

def _font_factory(txt, style):
    styled = txt.translate(_BOLD_MAP) if style == "bold" else txt
    return _pure_nc_factory(styled)

def _randomcod_factory(txt):
    last = _last(); idx = [0]
    lines = ["𝑲𝑰 𝑴𝑨𝑨 𝑷𝑼𝑹𝑬 𝑹𝑨𝑵𝑫𝑶𝑴 𝑺𝑬 𝑪𝑼𝑫𝑰","𝑲𝑰 𝑴𝑨𝑨 𝑻𝑬𝑹𝑰 𝑴𝑨𝑨 𝑺𝑬 𝑪𝑼𝑫𝑰","𝑲𝑰 𝑴𝑨𝑨 𝑻𝑬𝑹𝑬 𝑩𝑨𝑨𝑷 𝑺𝑬 𝑪𝑼𝑫𝑰","𝑲𝑰 𝑴𝑨𝑨 𝑻𝑬𝑹𝑬 𝑲𝑯𝑨𝑵𝑫𝑨𝑵 𝑺𝑬 𝑪𝑼𝑫𝑰"]
    def _f():
        line = lines[idx[0] % len(lines)]; idx[0] += 1
        c = f"{txt} {line} ➪ 𓂃{rnd_emoji()}་༘"[:255]
        if c == last[0]: c = f"{txt} {line} ➪ ✦{rnd_emoji()}༘"[:255]
        last[0] = c; return c
    return _f

def _aryagod_factory(txt, idx):
    emojis = [("♛","⚜️"),("𖤍","💀"),("🔱","💎"),("🌟","🌊"),("⚡","🔥")]
    names = ["NAYAK𝑮𝑶𝑫𝟏","Nayak𝑮𝑶𝑫𝟐","NAYAK𝑮𝑶𝑫𝟑","NAYAK𝑮𝑶𝑫𝟒","NAYAK𝑮𝑶𝑫𝟓"]
    e1, e2 = emojis[idx % len(emojis)]; name = names[idx % len(names)]
    last = _last(); alt = [True]
    def _f():
        emoji = e1 if alt[0] else e2
        c = f"{emoji}{name} {txt}{rnd_suffix()}"[:255]
        alt[0] = not alt[0]
        if c == last[0]:
            emoji = e1 if alt[0] else e2
            c = f"{emoji}{name} {txt}{rnd_suffix()}"[:255]
            alt[0] = not alt[0]
        last[0] = c; return c
    return _f

def _wave_factory(txt):
    last = _last()
    waves = ["🌊","💧","🫧","🌀","🌬️","❄️","🌙","💎","🌟"]
    def _f():
        w = random.choice(waves)
        c = f"{w}{txt}{rnd_suffix()}"[:255]
        if c == last[0]: c = f"{random.choice(waves)} {txt}{rnd_suffix()}"[:255]
        last[0] = c; return c
    return _f

def _chud_nc_factory(txt):
    words = list(_CHUD_WORDS); idx = [0]; last = _last()
    def _f():
        word = words[idx[0] % len(words)]; idx[0] += 1
        c = f"{txt}𒐫𒐫𒐫𒐫𒐫𒐫💥𒐫💥𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫💥𒐫💥{word} 𒐫𒐫𒐫 ➴ྀ࿐ ·· "[:255]
        if c == last[0]:
            idx[0] += 1
            word2 = words[idx[0] % len(words)]
            c = f"{txt}𒐫𒐫𒐫💥𒐫💥{word2} 𒐫𒐫𒐫 ➴ྀ࿐ ·· "[:255]
        last[0] = c; return c
    return _f

def _custom_template_factory(template, txt):
    words = list(_CHUD_WORDS); widx = [0]; ctr = [0]; last = _last()
    def _f():
        widx[0] += 1; ctr[0] += 1
        w = words[widx[0] % len(words)]; e = rnd_emoji()
        wl = random.choice(WRAP_L); wr = random.choice(WRAP_R)
        c = (template.replace("{txt}",txt).replace("{t}",txt).replace("{w}",w).replace("{e}",e)
             .replace("{n}",str(ctr[0])).replace("{wl}",wl).replace("{wr}",wr))[:255]
        if c == last[0]: c = (c + " ·")[:255]
        last[0] = c; return c
    return _f

def _save_templates():
    try:
        with open(TEMPLATES_FILE, "w") as f: json.dump(custom_templates, f, ensure_ascii=False, indent=2)
    except Exception: pass

# ═══════════════════════════════════════════════════════════
# ENGINES
# ═══════════════════════════════════════════════════════════
async def _blaze_engine(chat_id, bots, stop_event, name_factory):
    RELAY_OFFSET = 0.15
    SEND_GAP = _nc_send_gap if _nc_send_gap is not None else 0.60
    if not bots: return
    async def _worker(bot, idx):
        until = time.monotonic() + idx * RELAY_OFFSET
        while not stop_event.is_set():
            rem = until - time.monotonic()
            if rem > 0.0:
                if await _wait_ev(stop_event, rem): return
                until = 0.0; continue
            if stop_event.is_set(): return
            try:
                await bot.set_chat_title(chat_id, name_factory()[:255])
                if await _wait_ev(stop_event, SEND_GAP): return
            except RetryAfter as e: until = time.monotonic() + e.retry_after + idx * RELAY_OFFSET
            except (BadRequest, Forbidden): pass
            except (TimedOut, NetworkError):
                if await _wait_ev(stop_event, 0.5): return
            except asyncio.CancelledError: return
            except Exception: pass
    workers = [asyncio.create_task(_worker(b, i)) for i, b in enumerate(bots)]
    try: await stop_event.wait()
    finally:
        for w in workers:
            if not w.done(): w.cancel()
        try: await asyncio.shield(asyncio.gather(*workers, return_exceptions=True))
        except Exception: pass

async def _god_engine(chat_id, bots, stop_event, name_factory):
    N = len(bots)
    if N == 0: return
    STAGGER_FLOOR = _nc_send_gap if _nc_send_gap is not None else 0.18
    STAGGER_CEIL = STAGGER_FLOOR + 0.14
    cur_stagger = [STAGGER_FLOOR]
    adapt_lock = asyncio.Lock()
    slots = asyncio.Queue(maxsize=1)
    async def _producer():
        while not stop_event.is_set():
            tick = time.monotonic()
            try: slots.put_nowait(tick)
            except asyncio.QueueFull: pass
            gap = tick + cur_stagger[0] - time.monotonic()
            if gap > 0.0:
                if await _wait_ev(stop_event, gap): return
    async def _worker(bot, idx):
        until = 0.0
        while not stop_event.is_set():
            rem = until - time.monotonic()
            if rem > 0.0:
                if await _wait_ev(stop_event, rem): return
                until = 0.0
            try: await asyncio.wait_for(slots.get(), timeout=cur_stagger[0] * 4)
            except asyncio.TimeoutError: continue
            if stop_event.is_set(): return
            try: await bot.set_chat_title(chat_id, name_factory()[:255])
            except RetryAfter as e:
                async with adapt_lock: cur_stagger[0] = min(cur_stagger[0] + 0.04, STAGGER_CEIL)
                until = time.monotonic() + min(e.retry_after, 2.5)
            except (BadRequest, Forbidden): pass
            except (TimedOut, NetworkError): until = time.monotonic() + 0.25
            except asyncio.CancelledError: return
            except Exception: pass
    producer = asyncio.create_task(_producer())
    workers = [asyncio.create_task(_worker(b, i)) for i, b in enumerate(bots)]
    try: await stop_event.wait()
    finally:
        producer.cancel()
        for w in workers:
            if not w.done(): w.cancel()
        await asyncio.gather(producer, *workers, return_exceptions=True)

async def _stagger_engine(chat_id, bots, stop_event, name_factory):
    N = len(bots)
    if N == 0: return
    STAGGER = _nc_send_gap if _nc_send_gap is not None else 0.15
    CYCLE = STAGGER * N
    async def _worker(bot, idx):
        if idx > 0:
            if await _wait_ev(stop_event, idx * STAGGER): return
        while not stop_event.is_set():
            cs = time.monotonic()
            try: await bot.set_chat_title(chat_id, name_factory()[:255])
            except RetryAfter as e:
                if await _wait_ev(stop_event, min(e.retry_after, 2.5)): return
                cs = time.monotonic()
            except (BadRequest, Forbidden): pass
            except (TimedOut, NetworkError):
                if await _wait_ev(stop_event, 0.20): return
                cs = time.monotonic()
            except asyncio.CancelledError: return
            except Exception: pass
            if await _wait_ev(stop_event, max(cs + CYCLE - time.monotonic(), 0.02)): return
    workers = [asyncio.create_task(_worker(b, i)) for i, b in enumerate(bots)]
    try: await stop_event.wait()
    finally:
        for w in workers:
            if not w.done(): w.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

async def _trio_engine(chat_id, bots, stop_event, name_factory):
    if not bots: return
    G = [bots[0:3], bots[3:6], bots[6:10]]
    NUM_G = 3
    TICK = _nc_send_gap if _nc_send_gap is not None else 0.10
    bot_until = [[0.0]*len(G[gi]) for gi in range(NUM_G)]
    g_cursor = [0]*NUM_G
    active_g = [0]
    queues = [asyncio.Queue(maxsize=4) for _ in range(NUM_G)]
    def _has_free(gi):
        now = time.monotonic()
        return any(bot_until[gi][bi] <= now for bi in range(len(G[gi])))
    def _pick(gi):
        now = time.monotonic()
        grp = G[gi]; cur = g_cursor[gi]
        for i in range(len(grp)):
            bi = (cur+i) % len(grp)
            if bot_until[gi][bi] <= now:
                g_cursor[gi] = (bi+1) % len(grp)
                return bi, grp[bi]
        return None, None
    async def _prod():
        while not stop_event.is_set():
            tick = time.monotonic(); gi = active_g[0]
            if not _has_free(gi):
                sw = False
                for off in range(1, NUM_G):
                    nxt = (gi+off) % NUM_G
                    if _has_free(nxt): active_g[0] = nxt; gi = nxt; sw = True; break
                if not sw:
                    if await _wait_ev(stop_event, 0.05): return
                    continue
            try: queues[gi].put_nowait(tick)
            except asyncio.QueueFull: pass
            wait = TICK - (time.monotonic() - tick)
            if wait > 0:
                if await _wait_ev(stop_event, wait): return
    async def _worker(gi):
        while not stop_event.is_set():
            try: await asyncio.wait_for(queues[gi].get(), timeout=TICK*40)
            except asyncio.TimeoutError: continue
            if stop_event.is_set(): return
            bi, bot = _pick(gi)
            if bot is None: continue
            try: await bot.set_chat_title(chat_id, name_factory()[:255])
            except RetryAfter as e:
                bot_until[gi][bi] = time.monotonic() + min(e.retry_after, 2.5) + bi*0.04
                if not _has_free(gi): active_g[0] = (gi+1) % NUM_G
            except (BadRequest, Forbidden): pass
            except (TimedOut, NetworkError): bot_until[gi][bi] = time.monotonic() + 0.20
            except asyncio.CancelledError: return
            except Exception: pass
    tasks = [asyncio.create_task(_prod())]
    for gi in range(NUM_G):
        tasks.append(asyncio.create_task(_worker(gi)))
        tasks.append(asyncio.create_task(_worker(gi)))
    try: await stop_event.wait()
    finally:
        for t in tasks:
            if not t.done(): t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

async def _silk_engine(chat_id, bots, stop_event, name_factory):
    N = len(bots)
    if N == 0: return
    STEP = _nc_send_gap if _nc_send_gap is not None else 0.18
    b_until = [0.0]*N
    async def _track(indices, offset):
        if offset > 0:
            if await _wait_ev(stop_event, offset): return
        ptr = [0]; T = len(indices)
        while not stop_event.is_set():
            now = time.monotonic(); found = False
            for i in range(T):
                ti = (ptr[0]+i) % T; bi = indices[ti]
                if b_until[bi] <= now:
                    ptr[0] = (ti+1) % T; found = True; break
            if not found:
                nxt = min(b_until[indices[j]] for j in range(T)) - now
                if await _wait_ev(stop_event, max(nxt, 0.02)): return
                continue
            try:
                await bots[bi].set_chat_title(chat_id, name_factory()[:255])
                if await _wait_ev(stop_event, STEP): return
            except RetryAfter as e: b_until[bi] = time.monotonic() + e.retry_after + bi*0.05
            except (BadRequest, Forbidden): pass
            except (TimedOut, NetworkError): b_until[bi] = time.monotonic() + 0.20
            except asyncio.CancelledError: return
            except Exception: pass
    track_a = list(range(0, N, 2)); track_b = list(range(1, N, 2))
    tasks = [asyncio.create_task(_track(track_a, 0.0)), asyncio.create_task(_track(track_b, STEP/2.0))]
    try: await stop_event.wait()
    finally:
        for t in tasks:
            if not t.done(): t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

async def _chud_engine(chat_id, bots, stop_event, name_factory):
    N = len(bots)
    if N == 0: return
    STEP = _nc_send_gap if _nc_send_gap is not None else 0.20
    CYCLE = STEP * N
    flooded = [0.0]*N
    async def _worker(idx):
        bot = bots[idx]; nxt = time.monotonic() + idx*STEP
        while not stop_event.is_set():
            now = time.monotonic()
            if flooded[idx] > now:
                if await _wait_ev(stop_event, min(flooded[idx]-now, 0.25)): return
                continue
            wait = nxt - time.monotonic()
            if wait > 0.005:
                if await _wait_ev(stop_event, wait): return
                if stop_event.is_set(): return
            try:
                await bot.set_chat_title(chat_id, name_factory()[:255])
                nxt = time.monotonic() + CYCLE
            except RetryAfter as e:
                flooded[idx] = time.monotonic() + e.retry_after + 0.5
                nxt = flooded[idx] + idx*STEP
            except (BadRequest, Forbidden): nxt = time.monotonic() + CYCLE*2
            except (TimedOut, NetworkError): nxt = time.monotonic() + 1.5
            except asyncio.CancelledError: return
            except Exception: nxt = time.monotonic() + CYCLE
    tasks = [asyncio.create_task(_worker(i)) for i in range(N)]
    try: await stop_event.wait()
    finally:
        for t in tasks:
            if not t.done(): t.cancel()
        try: await asyncio.shield(asyncio.gather(*tasks, return_exceptions=True))
        except Exception: pass

# ═══════════════════════════════════════════════════════════
# CATEGORIES (Menu Content)
# ═══════════════════════════════════════════════════════════
CATEGORIES: Dict[str, Dict[str, Any]] = {
    "attacks": {"emoji": "⚔️", "label": "ATTACKS", "tag": "Attack Modules", "items": [
        ("🌀 All NC","nc <text>"),("⚡ Surge NC","snc <text>"),("💥 Chud NC","chud <text>"),
        ("𝐁 Bold NC","boldnc <text>"),("🌊 Wave NC","wavenc <text>"),("👑 God 1","aryagod1 <text>"),
        ("💀 God 2","nayakgod2 <text>"),("🔱 God 3","nayakgod3 <text>"),("🌟 God 4","nayakgod4 <text>"),
        ("⚡ God 5","aryagod5 <text>"),("🎯 TrioGod","triogod <text>"),("🪡 Silk NC","silknc <text>"),
        ("🌀 All NAYAK NCs","aryancs"),("🎲 RandomCod","randomcod <text>"),("👑 GodCod","godcod <text>"),
        ("💀 Big NC 1","aryanc1 @user"),("💀 Big NC 2","aryanc2 @user"),("💀 Big NC 3","aryanc3 @user"),
        ("💀 Big NC 4","aryanc4 @user"),("💀 Big NC 5","aryanc5 @user"),
        ("💬 Spam Basic","spam <text>"),("💬 Spam 1","spam1 @user"),("💬 Spam 2","spam2 @user"),
        ("💬 Spam 3","spam3 @user"),("📜 Slide Spam","slidespam <text>"),
        ("❤️ NAYAJSpam 1","NAYAKspam1 @user"),("😊 NAYAKSpam 2","NAYAKspam2 @user"),
        ("🌊 Swipe Spam","ss <text>"),("💥 Burst Spam","bs <text>"),
        ("💥 Chud Spam","cs <text>"),("⚡ Rapid Fire","rap <text>"),
        ("🔁 Reply Flood","rf <text>"),("📢 Tag Spam","ts <uid> <text>"),
        ("💬 Reply Raid","rr <text>"),("💬 Mass Reply","mr <text>"),
        ("🔁 RR Spam Loop","rs <text>"),("🔁 RR Loop","rl <text>"),
        ("⚔️ NC Del","ncdel <text>"),("⚔️ NC War","ncwar <text>"),
        ("🎯 Multi War","multiwar <text>"),("🔥 NC + Spam","aryancspam @user"),
        ("💀 Big NAYAK NC","NAYAKbignc @user"),
    ]},
    "admin": {"emoji": "👑", "label": "ADMIN", "tag": "Admin Controls", "items": [
        ("📋 GC Info","gcinfo"),("✏️ Set Title","setgctitle <title>"),("📝 Set Desc","setgcdesc <desc>"),
        ("🔗 Get Invite","getinvite"),("📌 Pin Msg","pinmsg"),("📌 Unpin All","unpinall"),
        ("👢 Kick User","kickuser <uid>"),("🚫 Ban User","bantarget <uid>"),
        ("✅ Unban User","unbanuser <uid>"),("🔇 Mute User","muteuser <uid>"),
        ("🔊 Unmute User","unmuteuser <uid>"),("🔇 Mute Chat","mute"),("🔊 Unmute Chat","unmute"),
        ("📸 Add PFP","addpfp"),("🖼️ PFP Loop","pfploop 3"),("⏹ Stop PFP Loop","stoppfploop"),
        ("🖼️ Set PFP Once","setpfponce"),("🗑 Remove PFP","deletegcpfp"),
        ("📋 PFP Pool","pfppool"),("🧹 Clear PFP","clearpfp"),
        ("➕ Add Sudo","addsudo <uid>"),("➖ Remove Sudo","removesudo <uid>"),("📋 Sudo List","sudolist"),
        ("🤖 Bots List","bots"),("➕ Add Bot","addbot"),("➕ Add All Bots","addallbots"),
        ("👑 Promote Bot","promotebot"),("✏️ Bot Name","botname <name>"),
    ]},
    "tools": {"emoji": "🛠️", "label": "TOOLS", "tag": "Tool Modules", "items": [
        ("📜 Host 1","host1 file.py"),("📜 Host 2","host2 file.py"),
        ("🛑 Stop Host 1","stophost 1"),("🛑 Stop Host 2","stophost 2"),
        ("🛑 Stop All Host","stophost all"),("📊 Host Status","hoststat"),
        ("📋 Host Log 1","hostlog 1"),("📋 Host Log 2","hostlog 2"),
        ("📖 Menu File 1","menufile1"),("📖 Menu File 2","menufile2"),
        ("🗑 Purge","purge"),("🗑 Purge Me","purgeme 10"),("🗑 Purge Bot","purgebot"),("🗑 Purge All","purgeall"),
        ("➕ Add Template","addtemplate name tpl"),("🎨 Custom NC","cnc name <text>"),
        ("📋 Templates","templates"),("🔍 Preview","preview name <text>"),
        ("🗑 Delete Template","deltemplate name"),("🧹 Clear Templates","cleartemplates"),
        ("🎯 Target Reply","targetreply uid <text>"),("⛔ Stop TReply","stoptargetreply"),
        ("🎯 Target Slide","targetslide uid"),("⛔ Stop TSlide","stoptargetslide"),
    ]},
    "nayakfun": {"emoji": "🎨", "label": "NAYAK FUN", "tag": "Fun & Media", "items": [
        ("🎨 Logo","logo <name>"),("👧 Logo Girl","logo <name> girl"),("👦 Logo Age","logo <name> boy 15"),
        ("🐾 Famous","fem <search>"),("✍️ Famous + Name","fem <search> | <name>"),
        ("🎨 AI Image","image <prompt>"),("🎵 Song DL","song <name>"),
        ("🎬 YT Video","yt <query>"),("🎬 Over","over"),
        ("👤 User Info","info"),("🔍 Deep Info","aryainfo @user"),
    ]},
    "war": {"emoji": "⚔️", "label": "WAR", "tag": "War Controls", "items": [
        ("⚔️ NC Del","ncdel <text>"),("⚔️ NC War","ncwar <text>"),("⛔ Stop NC War","stopncwar"),
        ("🎯 Multi War","multiwar <text>"),("⛔ Stop Multi War","stopmultiwar"),
        ("🔇 Mute Chat","mute"),("🔊 Unmute Chat","unmute"),
        ("🔥 NC + Spam","aryancspam @user"),("💀 Big nayak NC","aryabignc @user"),
        ("💬 Reply Raid","rr <text>"),("💬 Mass Reply","mr <text>"),
        ("🔁 RR Spam Loop","rs <text>"),("🔁 RR Loop","rl <text>"),
        ("🔁 Reply Flood","rf <text>"),("📢 Tag Spam","ts <uid> <text>"),
        ("🎯 Target Reply","targetreply uid <text>"),("⛔ Stop TReply","stoptargetreply"),
        ("🎯 Target Slide","targetslide uid"),("⛔ Stop TSlide","stoptargetslide"),
    ]},
    "host": {"emoji": "📦", "label": "HOST", "tag": "Host & Files", "items": [
        ("📜 Host 1","host1 file.py"),("📜 Host 2","host2 file.py"),
        ("🛑 Stop Host 1","stophost 1"),("🛑 Stop Host 2","stophost 2"),
        ("🛑 Stop All Host","stophost all"),("📊 Host Status","hoststat"),
        ("📋 Host Log 1","hostlog 1"),("📋 Host Log 2","hostlog 2"),
        ("📖 Menu File 1","menufile1"),("📖 Menu File 2","menufile2"),
        ("➕ Add Template","addtemplate name tpl"),("🎨 Custom NC","cnc name <text>"),
        ("📋 Templates","templates"),("🔍 Preview","preview name <text>"),
        ("🗑 Delete Template","deltemplate name"),("🧹 Clear Templates","cleartemplates"),
    ]},
    "all": {"emoji": "🌀", "label": "ALL", "tag": "All Commands", "items": [
        ("⚡ All NC","nc <text>"),("💥 Chud NC","chud <text>"),
        ("👑 God 1","aryagod1 <text>"),("💀 God 2","aryagod2 <text>"),
        ("🔱 God 3","aryagod3 <text>"),("🌟 God 4","aryagod4 <text>"),
        ("⚡ NAYAK god5 <text>"),("🌀 All NAYAKNCs","aryancs"),
        ("🎲 RandomCod","randomcod <text>"),("👑 GodCod","godcod <text>"),
        ("💬 Spam Basic","spam <text>"),("💬 Spam 1","spam1 @user"),
        ("💬 Spam 2","spam2 @user"),("💬 Spam 3","spam3 @user"),
        ("📜 Slide Spam","slidespam <text>"),("🌊 Swipe Spam","ss <text>"),
        ("💥 Burst Spam","bs <text>"),("💥 Chud Spam","cs <text>"),
        ("⚡ Rapid Fire","rap <text>"),("🎨 Logo","logo <name>"),
        ("🐾 Famous","fem <search>"),("🎵 Song DL","song <name>"),
        ("🎬 YT Video","yt <query>"),("🎨 AI Image","image <prompt>"),
        ("📋 GC Info","gcinfo"),("📌 Pin Msg","pinmsg"),
        ("👢 Kick User","kickuser <uid>"),("🚫 Ban User","bantarget <uid>"),
        ("🔇 Mute Chat","mute"),("🔊 Unmute Chat","unmute"),
        ("📜 Host 1","host1 file.py"),("📜 Host 2","host2 file.py"),
        ("📊 Host Status","hoststat"),("⚔️ NC War","ncwar <text>"),
        ("🎯 Multi War","multiwar <text>"),("📊 Status","status"),
        ("⏱ Uptime","uptime"),("🏓 Ping","ping"),
        ("⛔ Stop All","stop"),("⛔ Stop Spam","stopspam"),
    ]},
}

def _build_main_caption(bot_name="NAYAK"):
    return (
             "𓆩💢𓆪 NAYAK𓆩 𝙾𝙽 𝐓𝙾𝙿🕸️⃟𓆪 𓆩💢𓆪\n"
        "╭──────────────────────────────╮\n"
        f"│ 🤖 𝘉𝘖𝘛    ──➤  {bot_name:<13}│\n"
        
        
        "│ 🧪 𝘝𝘌𝘙𝘲   ──➤  𝐀𝚁𝚈𝙰 𝚅 𝟼        │\n"
        
        
        f"│ 👑 𝘔𝘈𝘚𝘛𝘌𝘙 ──➤  {MENU_MASTER_USERNAME:<13}│\n"
        
        
        "│ 🟢 𝘚𝘛𝘈𝘛𝘜𝘚 ──➤  𝘓𝘐𝘓𝘌 [𝘖𝘕𝘓𝘐𝘕𝘌]  │\n"
 
        "│ ☠️ 𝘔𝘌𝘕𝘜 𝘈𝘓𝘓 ──➤  𝘈𝘓𝘓 𝘔𝘌𝘕𝘜     │\n"
        "╰──────────────────────────────╯"
    )

def _build_submenu_caption(cat_key):
    cat = CATEGORIES.get(cat_key)
    if not cat: return _build_main_caption()
    count = len(cat["items"])
    return (
        f"╭───────〔 {cat['emoji']} 〕───────╮\n"
        f"       {cat['label']}\n"
        "├──〔 CATEGORY MENU 〕──┤\n"
        f"  📦 Category › {cat['tag']}\n"
        f"  🎯 Commands › {count}\n"
        f"  👑 Master   › {MENU_MASTER_USERNAME}\n"
        "  📌 Tap a command below 👇\n"
        "╰───────〔 🍥 〕───────╯"
    )

def _main_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚔️A T T A C K S",  callback_data="menu:attacks")],
        [InlineKeyboardButton("👑  A D M I N",      callback_data="menu:admin")],
        [InlineKeyboardButton("🛠️  T O O L S",      callback_data="menu:tools")],
        [InlineKeyboardButton("🎨  A R Y A  F U N", callback_data="menu:aryafun")],
        [InlineKeyboardButton("⚔️  W A R",          callback_data="menu:war")],
        [InlineKeyboardButton("📦  H O S T",        callback_data="menu:host")],
        [InlineKeyboardButton("🌀  A L L",          callback_data="menu:all")],
    ])

def _submenu_kb(cat_key):
    cat = CATEGORIES.get(cat_key, {})
    items = cat.get("items", [])
    rows = []
    for i in range(0, len(items), 2):
        chunk = items[i:i+2]
        rows.append([InlineKeyboardButton(label, callback_data=f"showcmd:{cmd}") for (label, cmd) in chunk])
    rows.append([
        InlineKeyboardButton("◀️ BACK", callback_data="menu:main"),
        InlineKeyboardButton("❌ Close", callback_data="menu:close"),
    ])
    return InlineKeyboardMarkup(rows)

def _split_text(text, limit=4096):
    chunks = []; current = ""
    for line in text.split("\n"):
        seg = line + "\n"
        if len(current) + len(seg) > limit:
            if current: chunks.append(current.rstrip("\n"))
            current = seg
        else: current += seg
    if current.strip(): chunks.append(current.rstrip("\n"))
    return chunks or [text[:limit]]

async def _reply(msg, text):
    for chunk in _split_text(text):
        try: await msg.reply_text(chunk)
        except Exception: pass

async def _send_main_menu(msg):
    try: bot_name = msg.get_bot().username or "ARYA"
    except Exception: bot_name = "NAYAK"
    caption = _build_main_caption(bot_name)
    kb = _main_menu_kb()
    try:
        await msg.reply_video(video=MENU_VIDEO_MAIN, caption=caption[:1024],
                              reply_markup=kb, supports_streaming=True)
        return
    except Exception as e: logger.error(f"video fail: {e}")
    try:
        await msg.reply_photo(photo=MENU_VIDEO_MAIN, caption=caption[:1024], reply_markup=kb)
        return
    except Exception as e: logger.error(f"photo fail: {e}")
    for chunk in _split_text(caption):
        try: await msg.reply_text(chunk, reply_markup=kb)
        except Exception: pass

async def _menu_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query: return
    try: await query.answer()
    except Exception: pass
    user = query.from_user
    if not user or not is_admin(user.id):
        try: await query.answer("⛔ Access Denied", show_alert=True)
        except Exception: pass
        return
    data = query.data or ""
    if data == "menu:close":
        try: await query.message.delete()
        except Exception: pass
        return
    if data == "menu:main":
        try: bot_name = query.message.get_bot().username or "ARYA"
        except Exception: bot_name = "ARYA"
        caption = _build_main_caption(bot_name); kb = _main_menu_kb()
        try: await query.edit_message_caption(caption=caption[:1024], reply_markup=kb); return
        except Exception as e: logger.error(f"edit main: {e}"); return
    if data.startswith("menu:"):
        cat_key = data.split(":", 1)[1]
        if cat_key not in CATEGORIES: return
        caption = _build_submenu_caption(cat_key); kb = _submenu_kb(cat_key)
        try: await query.edit_message_caption(caption=caption[:1024], reply_markup=kb)
        except Exception as e: logger.error(f"edit sub: {e}")
        return
    if data.startswith("showcmd:"):
        cmd = data.split(":", 1)[1]
        try: await query.answer(f"📌 Usage:\n.{cmd}", show_alert=True)
        except Exception: pass
        return

# ═══════════════════════════════════════════════════════════
# MENU ALL
# ═══════════════════════════════════════════════════════════
def _menuall_parts():
    p1 = (
        "╔══════════════════════════════════════╗\n"
        "║   📖 nayak BOT — COMPLETE MENU ALL    ║\n"
        "║      Total Commands: 124             ║\n"
        "╚══════════════════════════════════════╝\n\n"
        "━━━━━ ⚡ NC ENGINE (19) ━━━━━\n"
        "  ✨ .nc <text>          ─ Basic NC\n"
        "  ✨ .snc <text>         ─ Surge NC\n"
        "  ✨ .boldnc <text>      ─ Bold NC\n"
        "  ✨ .wavenc <text>      ─ Wave NC\n"
        "  ✨ .chud <text>        ─ Chud NC\n"
        "  ✨ .aryagod1..5 <text> ─ God Modes\n"
        "  ✨ .nayak1 <text>       ─ Stagger NC\n"
        "  ✨ .triogod <text>     ─ Trio Stagger\n"
        "  ✨ .silknc <text>      ─ Silk NC\n"
        "  ✨ .nayakncs            ─ All nayak NCs\n"
        "  ✨ .randomcod <text>   ─ Random Cod\n"
        "  ✨ .godcod <text>      ─ God Cod\n"
        "  ✨ .phantom <text>     ─ Phantom NC\n"
        "  ✨ .testament <text>   ─ Testament NC\n"
        "  ✨ .shadow <text>      ─ Shadow NC\n\n"
        "━━━━━ ⚔️ WAR (7) ━━━━━\n"
        "  ✨ .ncdel .ncwar .stopncwar\n"
        "  ✨ .multiwar .stopmultiwar\n"
        "  ✨ .mute .unmute"
    )
    p2 = (
        "━━━━━ 💬 SPAM (23) ━━━━━\n"
        "  ✨ .spam .spam1 .spam2 .spam3\n"
        "  ✨ .slidespam .stopslide .stopspam\n"
        "  ✨ .ss .bs .cs .rap  (shortcuts)\n"
        "  ✨ .rf .ts .rr .mr .rs .rl\n\n"
        "━━━━━ 📋 TEMPLATES (6) ━━━━━\n"
        "  ✨ .addtemplate .cnc .templates\n"
        "  ✨ .preview .deltemplate .cleartemplates\n\n"
        "━━━━━ 🗑️ PURGE (4) ━━━━━\n"
        "  ✨ .purge .purgeme .purgebot .purgeall\n\n"
        "━━━━━ 🎯 TARGET (4) ━━━━━\n"
        "  ✨ .targetreply .stoptargetreply\n"
        "  ✨ .targetslide .stoptargetslide\n\n"
        "━━━━━ 🖼️ PFP (7) ━━━━━\n"
        "  ✨ .addpfp .pfploop .stoppfploop\n"
        "  ✨ .pfppool .clearpfp .setpfponce .deletegcpfp"
    )
    p3 = (
        "━━━━━ 👑 GC MGMT (11) ━━━━━\n"
        "  ✨ .gcinfo .setgctitle .setgcdesc\n"
        "  ✨ .getinvite .pinmsg .unpinall\n"
        "  ✨ .kickuser .bantarget .unbanuser\n"
        "  ✨ .muteuser .unmuteuser\n\n"
        "━━━━━ 🔐 SUDO (3) ━━━━━\n"
        "  ✨ .addsudo .removesudo .sudolist\n\n"
        "━━━━━ 🛠️ TOOLS (9) ━━━━━\n"
        "  ✨ .status .uptime .ping .setdelay\n"
        "  ✨ .gclist .floodstat .globalstop\n"
        "  ✨ .hostlog .botname\n\n"
        "━━━━━ 🤖 BOTS (4) ━━━━━\n"
        "  ✨ .bots .addbot .addallbots .promotebot\n\n"
        "━━━━━ 💬 AUTO (2) ━━━━━\n"
        "  ✨ .setautoreply .setautoreact\n\n"
        "━━━━━ 🎵 MISC (8) ━━━━━\n"
        "  ✨ .over .song .image .yt .logo .fem .info .aryainfo"
    )
    p4 = (
        "━━━━━ 💀 NAYAKNC 1-5 (5) ━━━━━\n"
        "  ✨ .NAYAKnc1..5 @user\n\n"
        "━━━━━ ❤️ ARYASPAM (2) ━━━━━\n"
        "  ✨ .NAYAKspam1 .nayakspam2\n\n"
        "━━━━━ 💥 BIG NC / HYBRID (2) ━━━━━\n"
        "  ✨ .aryabignc .aryancspam\n\n"
        "━━━━━ 📦 HOST (8) ━━━━━\n"
        "  ✨ .host1 <file.py>  ─ Host Slot 1\n"
        "  ✨ .host2 <file.py>  ─ Host Slot 2\n"
        "  ✨ .stophost <1/2/all>\n"
        "  ✨ .hoststat\n"
        "  ✨ .hostlog <1/2>\n"
        "  ✨ .menufile1 .menufile2\n\n"
        "━━━━━ 📖 MENU (2) ━━━━━\n"
        "  ✨ .menu .menuall\n\n"
        "━━━━━ ⛔ STOP (1) ━━━━━\n"
        "  ✨ .stop\n\n"
        "╔══════════════════════════════════════╗\n"
        "║   Total Commands: 124               ║\n"
        "║   ⚡ NAYAK BOT — FULLY LOADED ⚡      ║\n"
        "╚══════════════════════════════════════╝"
    )
    return [p1, p2, p3, p4]

# ═══════════════════════════════════════════════════════════
# GUARDS
# ═══════════════════════════════════════════════════════════
def _guard(handler):
    async def wrapper(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        msg = update.message or update.edited_message
        if not user or not is_admin(user.id):
            if msg:
                try: await msg.reply_text(_GATE)
                except Exception: pass
            return
        key = (msg.chat_id, msg.message_id) if msg else None
        if key is not None:
            if key in _seen: return
            _seen.add(key)
            if len(_seen) > 8000:
                for k in list(_seen)[:4000]: _seen.discard(k)
        await handler(update, ctx)
    wrapper.__name__ = handler.__name__
    return wrapper

_guard_any = _guard

def _bots(): return [b for b in all_bot_instances if b is not None]
def _get_args(ctx): return ctx.args or []
def _txt_arg(ctx): return " ".join(_get_args(ctx)).strip()

async def _start_nc(msg, chat_id, factory, label, engine_name="BLAZE"):
    bots = _bots()
    if not bots:
        await _reply(msg, "⚡ No bots!"); return
    async def _run(stop_ev): await _blaze_engine(chat_id, bots, stop_ev, factory)
    await tc.start(chat_id, "nc", _run)
    await _reply(msg, f"⚡ NC STARTED\n📛 {label}\n🤖 {len(bots)} bots\n.stop to stop")

# ═══════════════════════════════════════════════════════════
# HOST SYSTEM
# ═══════════════════════════════════════════════════════════
def _extract_commands_from_file(script_path):
    result = {"commands": [], "tokens": [], "owner_ids": [], "has_owner_check": False,
              "prefix": ".", "type": "unknown", "lines": 0}
    if not os.path.exists(script_path): return result
    try:
        with open(script_path, "r", encoding="utf-8", errors="ignore") as f: src = f.read()
    except Exception: return result
    result["lines"] = len(src.splitlines())
    for m in re.finditer(r'CommandHandler\(\s*["\']([^"\']+)["\']', src):
        c = m.group(1)
        if c and c not in result["commands"]: result["commands"].append(c)
    for m in re.finditer(r'PrefixHandler\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']', src):
        result["prefix"] = m.group(1); c = m.group(2)
        if c and c not in result["commands"]: result["commands"].append(c)
    for m in re.finditer(r'add_handler\(\s*["\']([a-zA-Z0-9_]+)["\']\s*,', src):
        c = m.group(1)
        if c and c not in result["commands"]: result["commands"].append(c)
    tm = re.findall(r'["\'](\d{8,12}:[A-Za-z0-9_\-]{30,40})["\']', src)
    result["tokens"] = list(dict.fromkeys(tm))
    for m in re.finditer(r'(?:OWNER_ID|OWNER_IDS|MASTER_ID)\s*=\s*(\d{6,15}|\[[\d,\s]+\])', src):
        v = m.group(1)
        if v.startswith("["):
            result["owner_ids"].extend(int(n) for n in re.findall(r"\d+", v))
        else: result["owner_ids"].append(int(v))
    if any(k in src for k in ["only_owner","only_sudo","is_admin","only_ownr"]):
        result["has_owner_check"] = True
    if "set_chat_title" in src: result["type"] = "NC / Title Changer"
    if "send_message" in src and ("spam" in src.lower() or "SPAM" in src): result["type"] = "NC + Spam Bot"
    if "leave_chat" in src and result["type"] == "unknown": result["type"] = "Group Manager"
    return result

def _find_script(name):
    if not name.endswith(".py"): name += ".py"
    cands = [name, os.path.join(SCRIPT_DIR, name), os.path.join(UPLOAD_DIR, name), os.path.join(os.getcwd(), name)]
    for c in cands:
        if os.path.exists(c) and os.path.isfile(c): return os.path.abspath(c)
    return None

async def run_script_file(script_path, chat_id, script_id):
    try:
        abs_path = os.path.abspath(script_path)
        if not os.path.exists(abs_path): return False, f"❌ Not found: {script_path}"
        workdir = os.path.dirname(abs_path)
        log_path = os.path.join(LOG_DIR, f"{chat_id}_{script_id}.log")
        log_file = open(log_path, "wb")
        try:
            process = await asyncio.create_subprocess_exec(
                sys.executable, "-u", abs_path,
                stdout=log_file, stderr=log_file, cwd=workdir,
                env={**os.environ, "PYTHONUNBUFFERED": "1"},
            )
        except Exception as e:
            log_file.close(); return False, f"❌ Spawn failed: {e}"
        await asyncio.sleep(2.0)
        if process.returncode is not None:
            log_file.close()
            err = ""
            try:
                with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                    err = f.read()[-600:].strip()
            except Exception: pass
            if not err: err = f"Exit code: {process.returncode}"
            return False, f"❌ Crashed on startup:\n{err}"
        if chat_id not in hosted_scripts: hosted_scripts[chat_id] = {}
        hosted_scripts[chat_id][script_id] = {
            "process": process, "path": abs_path,
            "started": datetime.now().strftime("%H:%M:%S"),
            "name": os.path.basename(abs_path),
            "log": log_path, "log_file": log_file,
        }
        meta = _extract_commands_from_file(abs_path)
        if chat_id not in hosted_menus: hosted_menus[chat_id] = {}
        hosted_menus[chat_id][script_id] = meta
        return True, f"✅ {os.path.basename(abs_path)} ({len(meta['commands'])} cmds)"
    except Exception as e:
        return False, f"❌ {str(e)}"

async def stop_script(chat_id, script_id):
    if chat_id not in hosted_scripts or script_id not in hosted_scripts[chat_id]:
        return False, "❌ Not running"
    try:
        info = hosted_scripts[chat_id][script_id]
        process = info["process"]; log_file = info.get("log_file")
        if process and process.returncode is None:
            process.terminate()
            try: await asyncio.wait_for(process.wait(), timeout=3.0)
            except asyncio.TimeoutError:
                process.kill()
                try: await process.wait()
                except Exception: pass
        if log_file:
            try: log_file.close()
            except Exception: pass
        del hosted_scripts[chat_id][script_id]
        if chat_id in hosted_menus: hosted_menus[chat_id].pop(script_id, None)
        if not hosted_scripts[chat_id]: del hosted_scripts[chat_id]
        return True, f"✅ {script_id} stopped"
    except Exception as e: return False, f"❌ {str(e)}"

async def _host_file(update, ctx, slot):
    msg = update.message or update.edited_message
    if not msg: return
    chat_id = msg.chat_id; sid = f"script{slot}"
    rep = msg.reply_to_message
    if rep and rep.document:
        doc = rep.document
        fname = doc.file_name or "hosted.py"
        if not fname.endswith(".py"):
            await _reply(msg, "❌ Only .py files allowed"); return
        status = await msg.reply_text(f"📥 Downloading `{fname}`...")
        try:
            tg_file = await ctx.bot.get_file(doc.file_id)
            save_path = os.path.join(UPLOAD_DIR, fname)
            await tg_file.download_to_drive(save_path)
        except Exception as e:
            await status.edit_text(f"❌ Download failed: {str(e)[:200]}"); return
        script_path = save_path
        try: await status.edit_text(f"✅ Saved → `{save_path}`\n🚀 Starting...")
        except Exception: pass
    else:
        args = _get_args(ctx)
        if not args:
            await _reply(msg,
                f"⚠️ Usage:\n  `.host{slot} <filename.py>`\n\nOR reply to a `.py` file with `.host{slot}`\n\n📁 Files dir: `{UPLOAD_DIR}`")
            return
        script_path = _find_script(args[0])
        if not script_path:
            name = args[0] if args[0].endswith(".py") else args[0]+".py"
            await _reply(msg, f"❌ Not found: `{name}`\n💡 Upload file via Telegram instead"); return
    if chat_id in hosted_scripts and sid in hosted_scripts[chat_id]:
        await stop_script(chat_id, sid)
    success, result = await run_script_file(script_path, chat_id, sid)
    meta = hosted_menus.get(chat_id, {}).get(sid, {})
    cmds = meta.get("commands", [])
    cmd_list = "\n".join(f"  ▸ `{meta.get('prefix','.')}{c}`" for c in cmds[:20]) or "  (none)"
    if success:
        await _reply(msg,
            f"╔══════════════════════════════╗\n"
            f"  📜 𝐇𝐎𝐒𝐓 {slot} — 𝐒𝐓𝐀𝐑𝐓𝐄𝐃\n"
            f"╚══════════════════════════════╝\n\n"
            f"📁 File: `{os.path.basename(script_path)}`\n"
            f"📊 Status: {result}\n"
            f"🎯 Commands: {len(cmds)} detected\n"
            f"🔤 Prefix: `{meta.get('prefix','.')}`\n"
            f"📄 Lines: {meta.get('lines', 0)}\n"
            f"🔑 Tokens: {len(meta.get('tokens', []))}\n\n"
            f"⚠️ **HOST MODE ACTIVE** — ARYA.py ke commands silent ho gaye.\n"
            f"Ab sirf hosted file ke bots respond karenge.\n\n"
            f"**Commands:**\n{cmd_list}\n\n"
            f"📖 Menu: `.menufile{slot}`")
    else:
        await _reply(msg,
            f"╔══════════════════════════════╗\n"
            f"  ❌ 𝐇𝐎𝐒𝐓 {slot} — 𝐅𝐀𝐈𝐋𝐄𝐃\n"
            f"╚══════════════════════════════╝\n\n"
            f"**Error:**\n`{result}`\n\n"
            f"💡 Use `.hostlog {slot}` for full logs")

# ═══════════════════════════════════════════════════════════
# COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════
spam1_tasks: Dict[int, List[asyncio.Task]] = {}
spam2_tasks: Dict[int, List[asyncio.Task]] = {}
spam3_tasks: Dict[int, List[asyncio.Task]] = {}

async def _spam_loop(bot, chat_id, target, tmpl):
    idx = 0; el = len(SPAM_EMOJIS)
    while True:
        try:
            emoji = SPAM_EMOJIS[(idx // 2) % el]
            await bot.send_message(chat_id, tmpl.format(target=target, emoji=emoji))
            idx += 1; await asyncio.sleep(0.1)
        except asyncio.CancelledError: break
        except Exception: pass

@_guard
async def cmd_spam1(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; args = _get_args(ctx)
    if not args: await _reply(msg, "⚠️ .spam1 @username"); return
    target = " ".join(args)
    if cid in spam1_tasks:
        for t in spam1_tasks[cid]: t.cancel()
    spam1_tasks[cid] = [asyncio.create_task(_spam_loop(b, cid, target, SPAM1_TEMPLATE)) for b in _bots()]
    await _reply(msg, f"💬 SPAM 1 — {target}")

@_guard
async def cmd_spam2(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; args = _get_args(ctx)
    if not args: await _reply(msg, "⚠️ .spam2 @username"); return
    target = " ".join(args)
    if cid in spam2_tasks:
        for t in spam2_tasks[cid]: t.cancel()
    spam2_tasks[cid] = [asyncio.create_task(_spam_loop(b, cid, target, SPAM2_TEMPLATE)) for b in _bots()]
    await _reply(msg, f"💬 SPAM 2 — {target}")

@_guard
async def cmd_spam3(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; args = _get_args(ctx)
    if not args: await _reply(msg, "⚠️ .spam3 @username"); return
    target = " ".join(args)
    if cid in spam3_tasks:
        for t in spam3_tasks[cid]: t.cancel()
    spam3_tasks[cid] = [asyncio.create_task(_spam_loop(b, cid, target, SPAM3_TEMPLATE)) for b in _bots()]
    await _reply(msg, f"💬 SPAM 3 — {target}")

@_guard
async def cmd_phantom(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx) or "PHANTOM"; bots = _bots()
    if not bots: await _reply(msg, "⚡ No bots!"); return
    async def _run(ev): await _blaze_engine(msg.chat_id, bots, ev, _lean_nc_factory(txt))
    await tc.start(msg.chat_id, "nc", _run)
    await _reply(msg, f"👻 PHANTOM — {txt}")

@_guard
async def cmd_testament(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx) or "TESTAMENT"; bots = _bots()
    if not bots: await _reply(msg, "⚡ No bots!"); return
    async def _run(ev): await _god_engine(msg.chat_id, bots, ev, _lean_nc_factory(txt))
    await tc.start(msg.chat_id, "nc", _run)
    await _reply(msg, f"⚡ TESTAMENT — {txt}")

@_guard
async def cmd_shadow(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx) or "SHADOW"; bots = _bots()
    if not bots: await _reply(msg, "⚡ No bots!"); return
    async def _run(ev): await _trio_engine(msg.chat_id, bots, ev, _lean_nc_factory(txt))
    await tc.start(msg.chat_id, "nc", _run)
    await _reply(msg, f"🌑 SHADOW — {txt}")

_spam_modes = {"swipe": {}, "burst": {}, "chud": {}, "rapid": {}}

async def _swipe_w(bot, cid, txt, ev):
    i = 0
    while not ev.is_set():
        try:
            await bot.send_message(cid, txt[:i+1])
            i = (i+1) % (len(txt)+1)
            if i == 0: await asyncio.sleep(0.4)
            await asyncio.sleep(0.25)
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(0.4)

async def _burst_w(bot, cid, txt, ev):
    while not ev.is_set():
        try:
            for _ in range(8):
                if ev.is_set(): break
                await bot.send_message(cid, txt)
            await asyncio.sleep(1.5)
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(0.5)

async def _chud_w(bot, cid, txt, ev):
    while not ev.is_set():
        try:
            w = random.choice(_CHUD_WORDS)
            await bot.send_message(cid, f"{txt} 𒐫𒐫𒐫💥 {w} 𒐫𒐫𒐫 ➴ྀ࿐")
            await asyncio.sleep(0.15)
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(0.4)

async def _rapid_w(bot, cid, txt, ev):
    while not ev.is_set():
        try: await bot.send_message(cid, txt)
        except RetryAfter as e:
            try: await asyncio.wait_for(ev.wait(), timeout=min(e.retry_after, 2.0))
            except asyncio.TimeoutError: pass
        except asyncio.CancelledError: break
        except Exception: pass

async def _run_mode(update, ctx, key, worker, banner):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; args = _get_args(ctx)
    if not args: await _reply(msg, f"⚠️ .{key}spam <text>"); return
    txt = " ".join(args); d = _spam_modes[key]
    if cid in d:
        for t in d[cid]: t.cancel()
    ev = asyncio.Event()
    d[cid] = [asyncio.create_task(worker(b, cid, txt, ev)) for b in _bots()]
    await _reply(msg, banner)

@_guard
async def cmd_swipespam(update, ctx): await _run_mode(update, ctx, "swipe", _swipe_w, "🌊 SWIPE SPAM")
@_guard
async def cmd_burstspam(update, ctx): await _run_mode(update, ctx, "burst", _burst_w, "💥 BURST SPAM")
@_guard
async def cmd_chudspam(update, ctx): await _run_mode(update, ctx, "chud", _chud_w, "💥 CHUD SPAM")
@_guard
async def cmd_rapidfire(update, ctx): await _run_mode(update, ctx, "rapid", _rapid_w, "⚡ RAPID FIRE")

replyflood_tasks: Dict[int, List[asyncio.Task]] = {}
tagspam_tasks: Dict[int, List[asyncio.Task]] = {}

@_guard
async def cmd_replyflood(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; rep = msg.reply_to_message
    if not rep: await _reply(msg, "⚠️ Reply to a msg"); return
    args = _get_args(ctx)
    replyflood_chats[cid] = " ".join(args) if args else "🔥 ARYA FLOOD 🔥"
    await _reply(msg, "🔁 REPLY FLOOD ON")

@_guard
async def cmd_tagspam(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; args = _get_args(ctx)
    if len(args) < 2: await _reply(msg, "⚠️ .tagspam <uid> <text>"); return
    target = args[0]; txt = " ".join(args[1:])
    if cid in tagspam_tasks:
        for t in tagspam_tasks[cid]: t.cancel()
    ev = asyncio.Event()
    async def w(bot):
        while not ev.is_set():
            try: await bot.send_message(cid, f"{target} {txt}"); await asyncio.sleep(0.4)
            except asyncio.CancelledError: break
            except RetryAfter as e:
                try: await asyncio.wait_for(ev.wait(), timeout=e.retry_after)
                except asyncio.TimeoutError: pass
            except Exception: await asyncio.sleep(0.4)
    tagspam_tasks[cid] = [asyncio.create_task(w(b)) for b in _bots()]
    await _reply(msg, f"📢 TAG SPAM — {target}")

rr_tasks: Dict[int, Dict[str, Any]] = {}

async def _start_raid(cid, rep_id, txt, delay, label):
    if cid in rr_tasks:
        for t in rr_tasks[cid]["tasks"]: t.cancel()
    ev = asyncio.Event()
    async def w(bot):
        while not ev.is_set():
            try:
                await bot.send_message(cid, txt, reply_parameters=ReplyParameters(message_id=rep_id, allow_sending_without_reply=True))
                await asyncio.sleep(delay)
            except RetryAfter as e:
                try: await asyncio.wait_for(ev.wait(), timeout=min(e.retry_after, 2.0))
                except asyncio.TimeoutError: pass
            except asyncio.CancelledError: break
            except Exception: await asyncio.sleep(0.3)
    rr_tasks[cid] = {"tasks": [asyncio.create_task(w(b)) for b in _bots()], "stop": ev, "label": label}

@_guard
async def cmd_rr(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    rep = msg.reply_to_message; args = _get_args(ctx)
    if not rep: await _reply(msg, "⚠️ Reply"); return
    if not args: await _reply(msg, "⚠️ .rr <text>"); return
    await _start_raid(msg.chat_id, rep.message_id, " ".join(args), 0.4, "RR")
    await _reply(msg, "💬 RR ON")

@_guard
async def cmd_mr(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    rep = msg.reply_to_message; args = _get_args(ctx)
    if not rep: await _reply(msg, "⚠️ Reply"); return
    if not args: await _reply(msg, "⚠️ .mr <text>"); return
    await _start_raid(msg.chat_id, rep.message_id, " ".join(args), 0.15, "MR")
    await _reply(msg, "💬 MR ON")

@_guard
async def cmd_rs(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    rep = msg.reply_to_message; args = _get_args(ctx)
    if not rep: await _reply(msg, "⚠️ Reply"); return
    if not args: await _reply(msg, "⚠️ .rs <text>"); return
    await _start_raid(msg.chat_id, rep.message_id, " ".join(args), 0.08, "RS")
    await _reply(msg, "🔁 RS ON")

@_guard
async def cmd_rl(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    rep = msg.reply_to_message; args = _get_args(ctx)
    if not rep: await _reply(msg, "⚠️ Reply"); return
    if not args: await _reply(msg, "⚠️ .rl <text>"); return
    await _start_raid(msg.chat_id, rep.message_id, " ".join(args), 1.2, "RL")
    await _reply(msg, "🔁 RL ON")

@_guard
async def cmd_addtemplate(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if len(args) < 2: await _reply(msg, "⚠️ .addtemplate <name> <tpl>"); return
    custom_templates[args[0].lower()] = " ".join(args[1:]); _save_templates()
    await _reply(msg, f"✅ '{args[0].lower()}' saved")

@_guard
async def cmd_cnc(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if len(args) < 2: await _reply(msg, "⚠️ .cnc <name> <text>"); return
    name = args[0].lower(); txt = " ".join(args[1:])
    if name not in custom_templates: await _reply(msg, f"⚠️ '{name}' not found"); return
    await _start_nc(msg, msg.chat_id, _custom_template_factory(custom_templates[name], txt), f"TPL:{name}")

@_guard
async def cmd_templates(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    if not custom_templates: await _reply(msg, "📋 No templates"); return
    lines = [f"📋 TEMPLATES ({len(custom_templates)})"]
    for k, v in custom_templates.items(): lines.append(f"  • {k}: {v[:60]}")
    await _reply(msg, "\n".join(lines))

@_guard
async def cmd_preview(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if len(args) < 2: await _reply(msg, "⚠️ .preview <n> <text>"); return
    name = args[0].lower(); txt = " ".join(args[1:])
    if name not in custom_templates: await _reply(msg, f"⚠️ Not found"); return
    f = _custom_template_factory(custom_templates[name], txt)
    samples = [f() for _ in range(5)]
    await _reply(msg, "🔍 PREVIEW\n" + "\n".join(f"  {i+1}. {s}" for i, s in enumerate(samples)))

@_guard
async def cmd_deltemplate(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if not args: await _reply(msg, "⚠️ .deltemplate <name>"); return
    name = args[0].lower()
    if name in custom_templates:
        del custom_templates[name]; _save_templates()
        await _reply(msg, f"🗑 '{name}' deleted")
    else: await _reply(msg, "⚠️ Not found")

@_guard
async def cmd_cleartemplates(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    custom_templates.clear(); _save_templates()
    await _reply(msg, "🧹 Cleared")

@_guard
async def cmd_purge(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; rep = msg.reply_to_message
    if not rep: await _reply(msg, "⚠️ Reply"); return
    bot = _bots()[0] if _bots() else ctx.bot
    deleted = 0
    try:
        for mid in range(rep.message_id, msg.message_id + 1):
            try: await bot.delete_message(cid, mid); deleted += 1
            except Exception: pass
            await asyncio.sleep(0.05)
        note = await bot.send_message(cid, f"🗑 Purged {deleted}")
        await asyncio.sleep(3)
        try: await note.delete()
        except Exception: pass
    except Exception as e: await _reply(msg, f"⚠️ {e}")

@_guard
async def cmd_purgeme(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; args = _get_args(ctx); n = 10
    if args:
        try: n = int(args[0])
        except ValueError: pass
    bot = _bots()[0] if _bots() else ctx.bot; deleted = 0
    try:
        async for m in bot.get_chat_history(cid, limit=200):
            if m.from_user and m.from_user.id == bot.id:
                try: await bot.delete_message(cid, m.message_id); deleted += 1
                except Exception: pass
                if deleted >= n: break
        await _reply(msg, f"🗑 Deleted {deleted}")
    except Exception as e: await _reply(msg, f"⚠️ {e}")

@_guard
async def cmd_purgebot(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; deleted = 0
    for bot in _bots():
        try:
            async for m in bot.get_chat_history(cid, limit=150):
                if m.from_user and m.from_user.id == bot.id:
                    try: await bot.delete_message(cid, m.message_id); deleted += 1
                    except Exception: pass
        except Exception: pass
    await _reply(msg, f"🗑 Bot msgs: {deleted}")

@_guard
async def cmd_purgeall(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; bot = _bots()[0] if _bots() else ctx.bot; deleted = 0
    try:
        async for m in bot.get_chat_history(cid, limit=500):
            try: await bot.delete_message(cid, m.message_id); deleted += 1
            except Exception: pass
        await _reply(msg, f"🗑 Purged {deleted}")
    except Exception as e: await _reply(msg, f"⚠️ {e}")

@_guard
async def cmd_setautoreply(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx)
    if not txt:
        autoreply_chats.pop(msg.chat_id, None)
        await _reply(msg, "❌ Auto-reply off"); return
    autoreply_chats[msg.chat_id] = txt
    await _reply(msg, f"✅ {txt}")

@_guard
async def cmd_setautoreact(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if not args:
        autoreact_chats.pop(msg.chat_id, None)
        await _reply(msg, "❌ Auto-react off"); return
    autoreact_chats[msg.chat_id] = args[0]
    await _reply(msg, f"✅ {args[0]}")

slide_tasks: Dict[int, List[asyncio.Task]] = {}

@_guard
async def cmd_stopspam(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id
    try: await tc.stop(cid, "spam")
    except Exception: pass
    for d in (spam1_tasks, spam2_tasks, spam3_tasks):
        if cid in d:
            for t in d[cid]: t.cancel()
            del d[cid]
    for d in _spam_modes.values():
        if cid in d:
            for t in d[cid]: t.cancel()
            del d[cid]
    for d in (tagspam_tasks, rr_tasks, slide_tasks):
        if cid in d:
            v = d[cid]; tasks = v["tasks"] if isinstance(v, dict) else v
            for t in tasks: t.cancel()
            del d[cid]
    replyflood_chats.pop(cid, None)
    await _reply(msg, "⛔ ALL SPAM STOPPED")

@_guard
async def cmd_over(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    target = None; tid = None; args = _get_args(ctx)
    if args:
        target = " ".join(args)
        if target.startswith("@"): target = target[1:]
    elif msg.reply_to_message and msg.reply_to_message.from_user:
        u = msg.reply_to_message.from_user
        target = u.username or u.first_name; tid = u.id
    else:
        u = update.effective_user
        target = u.username or u.first_name; tid = u.id
    if not target: target = "BABY"
    ist = timezone(timedelta(hours=5, minutes=30)); now = datetime.now(ist)
    cap = f"🎬 OVER BY ARYA\n👤 @{target}\n🆔 {tid or 'N/A'}\n⏰ {now.strftime('%I:%M:%S %p')}\n📅 {now.strftime('%A, %B %d, %Y')}"
    try: await msg.reply_video(video=OVER_VIDEO_URL, caption=cap, supports_streaming=True)
    except Exception: await _reply(msg, cap)

@_guard
async def cmd_song(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    if not ctx.args: await _reply(msg, "🎵 .song <name>"); return
    q = " ".join(ctx.args).strip()
    status = await msg.reply_text(f"🎵 Searching: {q}")
    try:
        import yt_dlp
        td = tempfile.mkdtemp(prefix="song_")
        opts = {'format': 'bestaudio[ext=m4a]/bestaudio', 'outtmpl': str(Path(td)/"%(title)s.%(ext)s"),
                'noplaylist': True, 'quiet': True, 'no_warnings': True, 'default_search': 'ytsearch1'}
        def _dl():
            with yt_dlp.YoutubeDL(opts) as y: return y.extract_info(f"ytsearch1:{q}", download=True)
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, _dl)
        if not info or not info.get('entries'):
            await status.edit_text("❌ Not found"); return
        title = info['entries'][0].get('title', q)
        files = list(Path(td).glob('*'))
        if not files: await status.edit_text("❌ Fail"); return
        await status.delete()
        with open(str(files[0]), 'rb') as a: await msg.reply_audio(audio=a, title=title, performer="ARYA")
        import shutil; shutil.rmtree(td, ignore_errors=True)
    except Exception as e: await status.edit_text(f"❌ {str(e)[:100]}")

@_guard
async def cmd_image(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if not args: await _reply(msg, "🎨 .image <prompt>"); return
    p = " ".join(args); status = await msg.reply_text(f"🎨 {p[:50]}...")
    try:
        import aiohttp
        enc = urllib.parse.quote(p)
        url = f"https://image.pollinations.ai/prompt/{enc}?width=1024&height=1024&nologo=true"
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=60) as r:
                if r.status == 200:
                    d = await r.read()
                    await msg.reply_photo(photo=io.BytesIO(d), caption=f"🎨 {p}")
                    await status.delete()
                else: await status.edit_text(f"❌ {r.status}")
    except Exception as e: await status.edit_text(f"❌ {str(e)[:100]}")

@_guard
async def cmd_yt(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    if not ctx.args: await _reply(msg, "❌ .yt <search>"); return
    q = " ".join(ctx.args); status = await msg.reply_text(f"🎬 Searching: {q}...")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True); fn = None
    try:
        import yt_dlp
        opts = {"format": "best[ext=mp4][height<=720]/best[ext=mp4]/best",
                "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
                "quiet": True, "no_warnings": True, "noplaylist": True, "default_search": "ytsearch1"}
        def _dl():
            with yt_dlp.YoutubeDL(opts) as y: return y.extract_info(f"ytsearch1:{q}", download=True)
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, _dl)
        if not info or not info.get("entries"):
            await status.edit_text("❌ Not found"); return
        v = info["entries"][0]; title = v.get("title", "Video"); vid = v.get("id"); dur = v.get("duration", 0)
        for f in os.listdir(DOWNLOAD_DIR):
            if f.startswith(str(vid)): fn = os.path.join(DOWNLOAD_DIR, f); break
        if not fn or not os.path.exists(fn):
            await status.edit_text("❌ Fail"); return
        if os.path.getsize(fn)/(1024*1024) > 50:
            await status.edit_text("❌ Too large"); return
        await status.delete()
        with open(fn, "rb") as vf:
            await msg.reply_video(video=vf, caption=f"🎬 {title}", supports_streaming=True, duration=int(dur) if dur else 0)
    except Exception as e:
        try: await status.edit_text(f"⚠️ {str(e)[:180]}")
        except Exception: pass
    finally:
        if fn and os.path.exists(fn):
            try: os.remove(fn)
            except Exception: pass

@_guard
async def cmd_logo(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    if not ctx.args: await _reply(msg, "❌ .logo <name> [boy/girl] [age]"); return
    args = list(ctx.args); gender = "boy"; age = 0
    if args and args[-1].isdigit():
        try:
            a = int(args[-1])
            if 1 <= a <= 120: age = a; args = args[:-1]
        except Exception: pass
    if args and args[-1].lower() in ("boy","girl","b","g","male","female","m","f"):
        gender = "boy" if args[-1].lower() in ("boy","b","male","m") else "girl"
        args = args[:-1]
    name = " ".join(args).strip()
    if not name: await _reply(msg, "❌ Name missing!"); return
    status = await msg.reply_text(f"🎨 {gender} {name}")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    op = os.path.join(DOWNLOAD_DIR, f"logo_{int(time.time())}.jpg")
    try:
        loop = asyncio.get_event_loop()
        _, data = await loop.run_in_executor(None, fetch_random_image, gender, age)
        await loop.run_in_executor(None, create_logo, data, name, op, 0.65)
        with open(op, "rb") as p:
            cap = f"⚡ ARYA LOGO ⚡\n🔮 {name}\n🎭 {gender.title()}"
            if age: cap += f"\n🎂 {age}"
            await msg.reply_photo(photo=p, caption=cap)
        await status.delete()
    except Exception as e:
        try: await status.edit_text(f"⚠️ {str(e)[:180]}")
        except Exception: pass
    finally:
        if os.path.exists(op):
            try: os.remove(op)
            except Exception: pass

@_guard
async def cmd_fem(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    if not ctx.args: await _reply(msg, "❌ .fem <search> | <name>"); return
    full = " ".join(ctx.args)
    if "|" in full:
        parts = full.split("|", 1); s = parts[0].strip(); w = parts[1].strip()
    else: s = full.strip(); w = s
    if not s: await _reply(msg, "❌ Search missing"); return
    if not w: w = s
    status = await msg.reply_text(f"🐾 {s} → {w}")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    op = os.path.join(DOWNLOAD_DIR, f"fem_{int(time.time())}.jpg")
    try:
        loop = asyncio.get_event_loop()
        _, data = await loop.run_in_executor(None, fetch_famous_image, s)
        await loop.run_in_executor(None, create_logo, data, w, op, 0.60)
        with open(op, "rb") as p:
            await msg.reply_photo(photo=p, caption=f"🐾 {s.title()}\n✍️ {w.title()}")
        await status.delete()
    except Exception as e:
        try: await status.edit_text(f"⚠️ {str(e)[:180]}")
        except Exception: pass
    finally:
        if os.path.exists(op):
            try: os.remove(op)
            except Exception: pass

@_guard
async def cmd_info(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    u = msg.reply_to_message.from_user if (msg.reply_to_message and msg.reply_to_message.from_user) else update.effective_user
    await _reply(msg, f"👤 {u.first_name or 'N/A'}\n@{u.username or 'N/A'}\nID: {u.id}\nBot: {u.is_bot}")

@_guard
async def cmd_aryainfo(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    tu = None; un = None
    if msg.reply_to_message and msg.reply_to_message.from_user: tu = msg.reply_to_message.from_user
    elif ctx.args: un = ctx.args[0].replace("@", "").strip()
    else: await _reply(msg, "❌ Reply or .aryainfo @username"); return
    status = await msg.reply_text("🔍 Fetching...")
    try:
        if un and not tu:
            try: tu = await ctx.bot.get_chat(f"@{un}")
            except Exception: pass
        if not tu: await status.edit_text("❌ Not found!"); return
        await status.edit_text(f"🔥 NAYAK INFO\nID: {tu.id}\nName: {getattr(tu,'first_name','N/A') or 'N/A'}\n@{getattr(tu,'username','N/A') or 'N/A'}")
    except Exception as e:
        try: await status.edit_text(f"❌ {str(e)[:180]}")
        except Exception: pass

pfp_tasks: Dict[int, List[asyncio.Task]] = {}

async def _pfp_w(bot, cid, ev):
    while not ev.is_set():
        try:
            pool = _pfp_pools.get(str(cid), [])
            if not pool: await asyncio.sleep(2.0); continue
            fid = random.choice(pool)
            try:
                pf = await bot.get_file(fid); buf = io.BytesIO()
                await pf.download_to_memory(buf); buf.seek(0)
                await bot.set_chat_photo(chat_id=cid, photo=buf)
            except Exception: await asyncio.sleep(1.0); continue
            await asyncio.sleep(3.0)
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(1.0)

@_guard
async def cmd_pfploop(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id
    pool = _pfp_pools.get(str(cid), [])
    if not pool: await _reply(msg, "⚠️ No PFPs! .addpfp"); return
    if cid in pfp_tasks:
        for t in pfp_tasks[cid]: t.cancel()
    ev = asyncio.Event()
    pfp_tasks[cid] = [asyncio.create_task(_pfp_w(b, cid, ev)) for b in _bots()]
    pfploop_active[cid] = True
    await _reply(msg, f"🖼 PFP LOOP — {len(pool)} photos")

@_guard
async def cmd_stoppfploop(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id
    if cid in pfp_tasks:
        for t in pfp_tasks[cid]: t.cancel()
        del pfp_tasks[cid]
    pfploop_active.pop(cid, None)
    await _reply(msg, "⛔ PFP LOOP STOPPED")

@_guard
async def cmd_addpfp(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    rep = msg.reply_to_message
    if not rep or not rep.photo: await _reply(msg, "📸 Reply to a photo"); return
    fid = rep.photo[-1].file_id; k = str(msg.chat_id)
    pool = _pfp_pools.get(k, [])
    if fid not in pool:
        pool.append(fid); _pfp_pools[k] = pool; _save_json(PFP_FILE, _pfp_pools)
        await _reply(msg, f"✅ Added! Total: {len(pool)}")
    else: await _reply(msg, "⚠️ Already in pool!")

@_guard
async def cmd_pfppool(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    pool = _pfp_pools.get(str(msg.chat_id), [])
    await _reply(msg, f"🖼 PFP POOL — {len(pool)}")

@_guard
async def cmd_clearpfp(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id
    if cid in pfp_tasks:
        for t in pfp_tasks[cid]: t.cancel()
        del pfp_tasks[cid]
    pfploop_active.pop(cid, None)
    _pfp_pools.pop(str(cid), None); _save_json(PFP_FILE, _pfp_pools)
    await _reply(msg, "🗑 PFP pool cleared!")

@_guard
async def cmd_setpfponce(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    rep = msg.reply_to_message
    if not rep or not rep.photo: await _reply(msg, "📸 Reply to a photo"); return
    for bot in _bots():
        try:
            await bot.set_chat_photo(msg.chat_id, rep.photo[-1].file_id)
            await _reply(msg, "✅ Set!"); return
        except Exception: pass
    await _reply(msg, "⚠️ Failed")

@_guard
async def cmd_deletegcpfp(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    for bot in _bots():
        try:
            await bot.delete_chat_photo(msg.chat_id)
            await _reply(msg, "✅ Removed!"); return
        except Exception: pass
    await _reply(msg, "⚠️ Failed")

@_guard
async def cmd_menu(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id
    known_chats.add(cid); _save_json(GROUPS_FILE, list(known_chats))
    await _send_main_menu(msg)

@_guard
async def cmd_menuall(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    for part in _menuall_parts():
        try:
            await msg.reply_text(part); await asyncio.sleep(0.4)
        except Exception: pass

@_guard
async def cmd_stop(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; count = 0
    try: count = await tc.stop_all(cid)
    except Exception: pass
    try:
        mute_chats.discard(cid); ncdel_chats.discard(cid)
        autoreact_chats.pop(cid, None); autoreply_chats.pop(cid, None)
        ncwar_targets.pop(cid, None); _multiwar_active.pop(cid, None)
        targetslide_chats.pop(cid, None); targetreply_chats.pop(cid, None)
        pfploop_active.pop(cid, None); replyflood_chats.pop(cid, None)
        for d in (spam1_tasks, spam2_tasks, spam3_tasks):
            if cid in d:
                for t in d[cid]: t.cancel()
                del d[cid]
        for d in _spam_modes.values():
            if cid in d:
                for t in d[cid]: t.cancel()
                del d[cid]
        for d in (tagspam_tasks, rr_tasks, slide_tasks):
            if cid in d:
                v = d[cid]; tasks = v["tasks"] if isinstance(v, dict) else v
                for t in tasks: t.cancel()
                del d[cid]
        if cid in pfp_tasks:
            for t in pfp_tasks[cid]: t.cancel()
            del pfp_tasks[cid]
    except Exception: pass
    await _reply(msg, f"⛔ STOPPED — {count} tasks")

@_guard
async def cmd_nc(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx)
    if not txt: await _reply(msg, "𝐔𝐬𝐞: .nc <text>"); return
    await _start_nc(msg, msg.chat_id, _pure_nc_factory(txt), txt)

@_guard
async def cmd_snc(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx)
    if not txt: await _reply(msg, "𝐔𝐬𝐞: .snc <text>"); return
    bots = _bots()
    if not bots: await _reply(msg, "⚡ No bots!"); return
    async def _run(ev): await _god_engine(msg.chat_id, bots, ev, _lean_nc_factory(txt))
    await tc.start(msg.chat_id, "nc", _run)
    await _reply(msg, f"⚡ SURGE — {txt}")

def _make_god_handler(idx):
    async def _h(update, ctx):
        msg = update.message or update.edited_message
        if not msg: return
        txt = _txt_arg(ctx) or f"NAYAKGOD{idx+1}"; bots = _bots()
        if not bots: await _reply(msg, "⚡ No bots!"); return
        async def _run(ev): await _god_engine(msg.chat_id, bots, ev, _aryagod_factory(txt, idx))
        await tc.start(msg.chat_id, "nc", _run)
        await _reply(msg, f"👑 GOD{idx+1} — {txt}")
    return _h

cmd_aryagod1 = _guard(_make_god_handler(0))
cmd_aryagod2 = _guard(_make_god_handler(1))
cmd_aryagod3 = _guard(_make_god_handler(2))
cmd_aryagod4 = _guard(_make_god_handler(3))
cmd_aryagod5 = _guard(_make_god_handler(4))

@_guard
async def cmd_arya1(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx) or "ARYA1"; bots = _bots()
    if not bots: await _reply(msg, "⚡ No bots!"); return
    async def _run(ev): await _stagger_engine(msg.chat_id, bots, ev, _lean_nc_factory(txt))
    await tc.start(msg.chat_id, "nc", _run)
    await _reply(msg, f"⚡ ARYA1 — {txt}")

@_guard
async def cmd_chud(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx)
    if not txt: await _reply(msg, "𝐔𝐬𝐞: .chud <text>"); return
    bots = _bots()
    if not bots: await _reply(msg, "⚡ No bots!"); return
    async def _run(ev): await _chud_engine(msg.chat_id, bots, ev, _chud_nc_factory(txt))
    await tc.start(msg.chat_id, "nc", _run)
    await _reply(msg, f"💥 CHUD — {txt}")

@_guard
async def cmd_triogod(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx)
    if not txt: await _reply(msg, "𝐔𝐬𝐞: .triogod <text>"); return
    bots = _bots()
    if not bots: await _reply(msg, "⚡ No bots!"); return
    async def _run(ev): await _trio_engine(msg.chat_id, bots, ev, _lean_nc_factory(txt))
    await tc.start(msg.chat_id, "nc", _run)
    await _reply(msg, f"🔱 TRIOGOD — {txt}")

@_guard
async def cmd_silknc(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx)
    if not txt: await _reply(msg, "𝐔𝐬𝐞: .silknc <text>"); return
    bots = _bots()
    if not bots: await _reply(msg, "⚡ No bots!"); return
    async def _run(ev): await _silk_engine(msg.chat_id, bots, ev, _lean_nc_factory(txt))
    await tc.start(msg.chat_id, "nc", _run)
    await _reply(msg, f"🪡 SILK — {txt}")

@_guard
async def cmd_boldnc(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx)
    if not txt: await _reply(msg, "𝐔𝐬𝐞: .boldnc <text>"); return
    await _start_nc(msg, msg.chat_id, _font_factory(txt, "bold"), f"BOLD {txt}")

@_guard
async def cmd_wavenc(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx)
    if not txt: await _reply(msg, "𝐔𝐬𝐞: .wavenc <text>"); return
    await _start_nc(msg, msg.chat_id, _wave_factory(txt), f"WAVE {txt}")

@_guard
async def cmd_aryancs(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx) or "ARYA"; idx = [0]
    facs = [_aryagod_factory(txt, i) for i in range(10)]
    def cyc():
        f = facs[idx[0] % len(facs)]; idx[0] += 1; return f()
    await _start_nc(msg, msg.chat_id, cyc, "All Arya NCs")

@_guard
async def cmd_randomcod(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx) or "ARYA"
    await _start_nc(msg, msg.chat_id, _randomcod_factory(txt), "RANDOMCOD")

@_guard
async def cmd_godcod(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx) or "ARYA"; bots = _bots()
    if not bots: await _reply(msg, "⚡ No bots!"); return
    async def _run(ev): await _god_engine(msg.chat_id, bots, ev, _randomcod_factory(txt))
    await tc.start(msg.chat_id, "nc", _run)
    await _reply(msg, f"⚡ GODCOD — {txt}")

@_guard
async def cmd_ncdel(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; txt = _txt_arg(ctx) or "ARYA"
    ncdel_chats.add(cid)
    async def _run(ev): await _blaze_engine(cid, _bots(), ev, _pure_nc_factory(txt))
    await tc.start(cid, "nc", _run)
    await _reply(msg, "⚔️ NCDEL")

@_guard
async def cmd_ncwar(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; txt = _txt_arg(ctx) or "ARYA WAR"
    ncwar_targets[cid] = txt
    await _start_nc(msg, cid, _pure_nc_factory(txt), f"WAR: {txt}")

@_guard
async def cmd_stopncwar(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    ncwar_targets.pop(msg.chat_id, None)
    await tc.stop(msg.chat_id, "nc")
    await _reply(msg, "⛔ NC WAR STOPPED")

@_guard
async def cmd_multiwar(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx)
    if not txt: await _reply(msg, "🎯 .multiwar <text>"); return
    bots = _bots()
    if not bots: await _reply(msg, "⚡ No bots!"); return
    targets = list(known_chats)
    if not targets: await _reply(msg, "⚠️ No groups"); return
    started = 0
    for cid in targets:
        fac = _pure_nc_factory(txt)
        async def _run(ev, _cid=cid, _f=fac): await _blaze_engine(_cid, bots, ev, _f)
        await tc.start(cid, "nc", _run)
        _multiwar_active[cid] = True; started += 1
    await _reply(msg, f"⚔️ MULTIWAR — {started}")

@_guard
async def cmd_stopmultiwar(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    total = 0
    for cid in list(_multiwar_active.keys()):
        if await tc.stop(cid, "nc"): total += 1
        _multiwar_active.pop(cid, None)
    await _reply(msg, f"⛔ MULTIWAR — {total}")

@_guard
async def cmd_mute(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; mute_chats.add(cid)
    for bot in _bots():
        try: await bot.set_chat_permissions(cid, ChatPermissions(can_send_messages=False))
        except Exception: pass
    await _reply(msg, "🔇 MUTED")

@_guard
async def cmd_unmute(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; mute_chats.discard(cid)
    for bot in _bots():
        try:
            await bot.set_chat_permissions(cid, ChatPermissions(can_send_messages=True, can_send_media_messages=True,
                can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True))
        except Exception: pass
    await _reply(msg, "🔊 UNMUTED")

@_guard
async def cmd_spam(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; txt = _txt_arg(ctx)
    if not txt: await _reply(msg, "𝐔𝐬𝐞: .spam <text>"); return
    async def _run(ev):
        while not ev.is_set():
            for bot in _bots():
                if ev.is_set(): break
                try: await bot.send_message(cid, txt)
                except RetryAfter as e:
                    try: await asyncio.wait_for(ev.wait(), timeout=min(e.retry_after, 2.0))
                    except asyncio.TimeoutError: pass
                except Exception: pass
            await asyncio.sleep(0)
    await tc.start(cid, "spam", _run)
    await _reply(msg, "💬 SPAM — .stopspam")

async def _slide_w(bot, cid, txt, ev):
    words = txt.split()
    if not words: return
    i = 0
    while not ev.is_set():
        try:
            await bot.send_message(cid, " ".join(words[:i+1]))
            i += 1
            if i >= len(words): i = 0; await asyncio.sleep(0.5)
            await asyncio.sleep(0.3)
        except RetryAfter as e: await asyncio.sleep(e.retry_after)
        except asyncio.CancelledError: break
        except Exception: await asyncio.sleep(0.5)

@_guard
async def cmd_slidespam(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if not args: await _reply(msg, "⚠️ .slidespam <text>"); return
    cid = msg.chat_id; txt = " ".join(args)
    if cid in slide_tasks:
        for t in slide_tasks[cid]: t.cancel()
    ev = asyncio.Event()
    slide_tasks[cid] = [asyncio.create_task(_slide_w(b, cid, txt, ev)) for b in _bots()]
    await _reply(msg, "📜 SLIDE — .stopslide")

@_guard
async def cmd_stopslide(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id
    if cid in slide_tasks:
        for t in slide_tasks[cid]: t.cancel()
        del slide_tasks[cid]
    await _reply(msg, "⛔ SLIDE STOPPED")

@_guard
async def cmd_status(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; bots = _bots()
    nc = tc.running(cid, "nc")
    ha = "🟢 HOST ACTIVE" if _host_active(cid) else "⚪ ARYA MODE"
    await _reply(msg, f"📊 {len(bots)} bots | NC:{'✅' if nc else '❌'} | {ha}")

@_guard
async def cmd_uptime(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    el = time.monotonic() - BOT_START_TIME
    h, r = divmod(int(el), 3600); m, s = divmod(r, 60)
    await _reply(msg, f"⏱ {h}h {m}m {s}s — {len(_bots())} bots")

@_guard
async def cmd_ping(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    t0 = time.monotonic(); sent = await msg.reply_text("🏓")
    await sent.edit_text(f"🏓 {int((time.monotonic()-t0)*1000)}ms")

@_guard
async def cmd_setdelay(update, ctx):
    global _nc_send_gap
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if not args:
        cur = f"{_nc_send_gap:.2f}s" if _nc_send_gap is not None else "default"
        await _reply(msg, f"Delay: {cur}"); return
    if args[0].lower() in ("reset","default","off"):
        _nc_send_gap = None; await _reply(msg, "✅ RESET"); return
    try:
        v = float(args[0])
        if v < 0.05 or v > 10.0: await _reply(msg, "⚠️ 0.05–10.0"); return
        _nc_send_gap = v; await _reply(msg, f"✅ {v}s")
    except ValueError: await _reply(msg, "Invalid")

@_guard
async def cmd_gcinfo(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    bot = _bots()[0] if _bots() else ctx.bot
    try:
        c = await bot.get_chat(msg.chat_id)
        await _reply(msg, f"📋 {c.title}\n🆔 {msg.chat_id}")
    except Exception as e: await _reply(msg, f"⚠️ {e}")

@_guard
async def cmd_setgctitle(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx)
    if not txt: await _reply(msg, "⚠️ .setgctitle <title>"); return
    for bot in _bots():
        try:
            await bot.set_chat_title(msg.chat_id, txt[:255])
            await _reply(msg, f"✅ {txt}"); return
        except Exception: pass
    await _reply(msg, "⚠️ Failed")

@_guard
async def cmd_setgcdesc(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    txt = _txt_arg(ctx)
    if not txt: await _reply(msg, "⚠️ .setgcdesc <desc>"); return
    for bot in _bots():
        try:
            await bot.set_chat_description(msg.chat_id, txt[:255])
            await _reply(msg, "✅ Set"); return
        except Exception: pass
    await _reply(msg, "⚠️ Failed")

@_guard
async def cmd_getinvite(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    for bot in _bots():
        try:
            link = await bot.export_chat_invite_link(msg.chat_id)
            await _reply(msg, f"🔗 {link}"); return
        except Exception: pass
    await _reply(msg, "⚠️ Failed")

@_guard
async def cmd_pinmsg(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    rep = msg.reply_to_message
    if not rep: await _reply(msg, "Reply to a msg"); return
    for bot in _bots():
        try:
            await bot.pin_chat_message(msg.chat_id, rep.message_id, disable_notification=True)
            await _reply(msg, "📌 Pinned"); return
        except Exception: pass
    await _reply(msg, "⚠️ Failed")

@_guard
async def cmd_unpinall(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    for bot in _bots():
        try:
            await bot.unpin_all_chat_messages(msg.chat_id)
            await _reply(msg, "📌 Unpinned"); return
        except Exception: pass
    await _reply(msg, "⚠️ Failed")

async def _resolve_uid(msg, ctx):
    args = _get_args(ctx); uid = None
    if args:
        try: uid = int(args[0])
        except ValueError: pass
    if uid is None and msg.reply_to_message and msg.reply_to_message.from_user:
        uid = msg.reply_to_message.from_user.id
    return uid

@_guard
async def cmd_kickuser(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    uid = await _resolve_uid(msg, ctx)
    if uid is None: await _reply(msg, "⚠️ .kickuser <uid>"); return
    for bot in _bots():
        try:
            await bot.ban_chat_member(msg.chat_id, uid)
            await asyncio.sleep(0.3)
            await bot.unban_chat_member(msg.chat_id, uid)
            await _reply(msg, f"👢 {uid}"); return
        except Exception: pass
    await _reply(msg, "⚠️ Failed")

@_guard
async def cmd_bantarget(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    uid = await _resolve_uid(msg, ctx)
    if uid is None: await _reply(msg, "⚠️ .bantarget <uid>"); return
    for bot in _bots():
        try:
            await bot.ban_chat_member(msg.chat_id, uid)
            await _reply(msg, f"🚫 {uid}"); return
        except Exception: pass
    await _reply(msg, "⚠️ Failed")

@_guard
async def cmd_unbanuser(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if not args: await _reply(msg, "⚠️ .unbanuser <uid>"); return
    try: uid = int(args[0])
    except ValueError: await _reply(msg, "Invalid"); return
    for bot in _bots():
        try:
            await bot.unban_chat_member(msg.chat_id, uid, only_if_banned=True)
            await _reply(msg, f"✅ {uid}"); return
        except Exception: pass
    await _reply(msg, "⚠️ Failed")

@_guard
async def cmd_muteuser(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    uid = await _resolve_uid(msg, ctx)
    if uid is None: await _reply(msg, "⚠️ .muteuser <uid>"); return
    for bot in _bots():
        try:
            await bot.restrict_chat_member(msg.chat_id, uid, permissions=ChatPermissions(can_send_messages=False), until_date=0)
            await _reply(msg, f"🔇 {uid}"); return
        except Exception: pass
    await _reply(msg, "⚠️ Failed")

@_guard
async def cmd_unmuteuser(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    uid = await _resolve_uid(msg, ctx)
    if uid is None: await _reply(msg, "⚠️ .unmuteuser <uid>"); return
    for bot in _bots():
        try:
            await bot.restrict_chat_member(msg.chat_id, uid, permissions=ChatPermissions(
                can_send_messages=True, can_send_media_messages=True,
                can_send_other_messages=True, can_add_web_page_previews=True), until_date=0)
            await _reply(msg, f"🔊 {uid}"); return
        except Exception: pass
    await _reply(msg, "⚠️ Failed")

@_guard
async def cmd_targetreply(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if len(args) < 2: await _reply(msg, "⚠️ .targetreply <uid> <text>"); return
    try: uid = int(args[0])
    except ValueError: await _reply(msg, "Invalid"); return
    targetreply_chats[msg.chat_id] = {"uid": uid, "text": " ".join(args[1:])}
    await _reply(msg, f"🎯 {uid}")

@_guard
async def cmd_stoptargetreply(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    targetreply_chats.pop(msg.chat_id, None)
    await _reply(msg, "⛔ Off")

@_guard
async def cmd_targetslide(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if not args: await _reply(msg, "⚠️ .targetslide <uid>"); return
    try: uid = int(args[0])
    except ValueError: await _reply(msg, "Invalid"); return
    targetslide_chats[msg.chat_id] = {"uid": uid, "text": " ".join(args[1:]).strip() or "💥 CHUD 💥"}
    await _reply(msg, f"🎯 {uid}")

@_guard
async def cmd_stoptargetslide(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    targetslide_chats.pop(msg.chat_id, None)
    await _reply(msg, "⛔ Off")

@_guard
async def cmd_addsudo(update, ctx):
    msg = update.message or update.edited_message
    u = update.effective_user
    if not msg or not u: return
    if u.id != OWNER_ID: await _reply(msg, "⚡ OWNER ONLY"); return
    args = _get_args(ctx); target = None
    if args:
        try: target = int(args[0])
        except ValueError: pass
    elif msg.reply_to_message and msg.reply_to_message.from_user:
        target = msg.reply_to_message.from_user.id
    if not target: await _reply(msg, "⚠️ .addsudo <uid>"); return
    SUDO_USERS.add(target)
    _save_json(SUDO_FILE, [x for x in SUDO_USERS if x != OWNER_ID])
    await _reply(msg, f"✅ {target}")

@_guard
async def cmd_removesudo(update, ctx):
    msg = update.message or update.edited_message
    u = update.effective_user
    if not msg or not u: return
    if u.id != OWNER_ID: await _reply(msg, "⚡ OWNER ONLY"); return
    args = _get_args(ctx)
    if not args: await _reply(msg, "⚠️ .removesudo <uid>"); return
    try: target = int(args[0])
    except ValueError: await _reply(msg, "Invalid"); return
    SUDO_USERS.discard(target)
    _save_json(SUDO_FILE, [x for x in SUDO_USERS if x != OWNER_ID])
    await _reply(msg, f"⛔ {target}")

@_guard
async def cmd_sudolist(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    users = [x for x in SUDO_USERS if x != OWNER_ID]
    lst = "\n".join(f"  • {x}" for x in users) if users else "  None"
    await _reply(msg, f"🔐 SUDO\n{lst}")

@_guard
async def cmd_bots(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    bots = _bots()
    lines = [f"🤖 {len(bots)} bots"]
    for i, b in enumerate(bots, 1):
        lines.append(f"  {i}. @{getattr(b, 'username', 'unknown')}")
    await _reply(msg, "\n".join(lines))

@_guard
async def cmd_floodstat(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    await _reply(msg, f"📊 {len(_bots())} bots active")

@_guard
async def cmd_gclist(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    lst = "\n".join(f"  • {c}" for c in known_chats) if known_chats else "  None"
    await _reply(msg, f"📋 GROUPS\n{lst}")

@_guard
async def cmd_addbot(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id; ok = 0
    for bot in _bots():
        try:
            await ctx.bot.promote_chat_member(cid, bot.id, can_change_info=True, can_delete_messages=True, can_manage_chat=True)
            ok += 1
        except Exception: pass
    await _reply(msg, f"✅ {ok}/{len(_bots())}")

@_guard
async def cmd_addallbots(update, ctx): await cmd_addbot(update, ctx)
@_guard
async def cmd_promotebot(update, ctx): await cmd_addbot(update, ctx)

@_guard
async def cmd_botname(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    name = _txt_arg(ctx)
    if not name: await _reply(msg, "⚠️ .botname <name>"); return
    ok = 0
    for app in all_apps:
        try: await app.bot.set_my_name(name); ok += 1
        except Exception: pass
    await _reply(msg, f"✅ {name} ({ok})")

@_guard
async def cmd_globalstop(update, ctx):
    msg = update.message or update.edited_message
    u = update.effective_user
    if not msg or not u: return
    if u.id != OWNER_ID: await _reply(msg, "⚡ OWNER ONLY"); return
    total = 0
    for cid in list(known_chats):
        total += await tc.stop_all(cid)
    mute_chats.clear(); ncdel_chats.clear()
    autoreact_chats.clear(); autoreply_chats.clear()
    ncwar_targets.clear(); _multiwar_active.clear()
    targetreply_chats.clear(); targetslide_chats.clear()
    pfploop_active.clear(); replyflood_chats.clear()
    await _reply(msg, f"🌐 GLOBAL STOP — {total}")

ARYANC_TEXTS = {
    1: "{target} мᦔC𒈙𒐫𒈙🖤𒐫𒈙𒐫🖤𒈙𒐫𒈙🖤𒈙𒐫𒈙🖤𒐫𒈙𒐫🖤𒈙𒐫𒈙",
    2: "{target} 𓆩💢𓆪 NAYAK𓆩 𝙾𝙽 𝐓𝙾𝙿🕸️⃟𓆪 𓆩💢𓆪",
    3: "𝙏𝘽𝙆𝘽 〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄🚀〄",
    4: "{target} 𝓽ꪑ𝘬ᥴ🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶🥶",
    5: "{target} 𝓽ꪑ𝘬ᥴ 🟨▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓🟨 🟨▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓🟨",
}
aryanc_tasks: Dict[int, Dict[int, List[asyncio.Task]]] = {1:{},2:{},3:{},4:{},5:{}}

async def _aryanc_loop(bot, cid, target, text):
    for _ in range(15):
        if bot is None: break
        try:
            await bot.send_message(cid, text.format(target=target))
            await asyncio.sleep(0.1)
        except asyncio.CancelledError: break
        except Exception: pass

def _make_aryanc_handler(n):
    async def _h(update, ctx):
        msg = update.message or update.edited_message
        if not msg: return
        args = _get_args(ctx)
        if not args: await _reply(msg, f"⚠️ .aryanc{n} @user"); return
        target = " ".join(args); cid = msg.chat_id
        if cid in aryanc_tasks[n]:
            for t in aryanc_tasks[n][cid]: t.cancel()
        aryanc_tasks[n][cid] = [asyncio.create_task(_aryanc_loop(b, cid, target, ARYANC_TEXTS[n])) for b in _bots()]
        await _reply(msg, f"💀 ARYANC {n} — {target}")
    return _h

cmd_aryanc1 = _guard(_make_aryanc_handler(1))
cmd_aryanc2 = _guard(_make_aryanc_handler(2))
cmd_aryanc3 = _guard(_make_aryanc_handler(3))
cmd_aryanc4 = _guard(_make_aryanc_handler(4))
cmd_aryanc5 = _guard(_make_aryanc_handler(5))

ARYASPAM1 = ["♥️","❤️‍🔥","❣️","💝","💔","❤️‍🩹","💟","❤️","🧡","💛","💚","🩵","💜","🤎","🖤"]
ARYASPAM2 = ["😭","😉","😗","😙","😚","😘","🥰","😍","🤩","🥳","🫠","🙃","🙂","🥲","🥹","😊","☺️","😌"]
aryaspam_tasks: Dict[int, Dict[int, List[asyncio.Task]]] = {1:{}, 2:{}}

async def _aryaspam_loop(bot, cid, target, emojis, count=30):
    for i in range(count):
        if bot is None: break
        e = emojis[i % len(emojis)]
        try:
            await bot.send_message(cid, f"{target} 𓆩💢𓆪 𝐀𝚁𝚈𝙰𓆩 𝙾𝙽 𝐓𝙾𝙿🕸️⃟𓆪 𓆩💢𓆪 {e}")
            await asyncio.sleep(0.1)
        except asyncio.CancelledError: break
        except Exception: pass

def _make_aryaspam_handler(n, emojis):
    async def _h(update, ctx):
        msg = update.message or update.edited_message
        if not msg: return
        args = _get_args(ctx)
        if not args: await _reply(msg, f"⚠️ .aryaspam{n} @user"); return
        target = " ".join(args); cid = msg.chat_id
        aryaspam_tasks[n][cid] = [asyncio.create_task(_aryaspam_loop(b, cid, target, emojis)) for b in _bots()]
        await _reply(msg, f"💬 ARYASPAM {n} — {target}")
    return _h

cmd_aryaspam1 = _guard(_make_aryaspam_handler(1, ARYASPAM1))
cmd_aryaspam2 = _guard(_make_aryaspam_handler(2, ARYASPAM2))

aryabignc_tasks: Dict[int, List[asyncio.Task]] = {}
BIG_NC = "{target} 𓆩💢𓆪 𝐀𝚁𝚈𝙰𓆩 𝙾𝙽 𝐓𝙾𝙿🕸️⃟𓆪 𓆩💢𓆪"

@_guard
async def cmd_aryabignc(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if not args: await _reply(msg, "⚠️ .aryabignc @user"); return
    target = " ".join(args); cid = msg.chat_id
    aryabignc_tasks[cid] = [asyncio.create_task(_aryanc_loop(b, cid, target, BIG_NC)) for b in _bots()]
    await _reply(msg, f"💀 BIG NC — {target}")

@_guard
async def cmd_aryancspam(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if not args: await _reply(msg, "⚠️ .aryancspam @user"); return
    target = " ".join(args); bots = _bots()
    if len(bots) < 2: await _reply(msg, "⚠️ Need 2+ bots"); return
    await _reply(msg, f"⚡ NC+SPAM — {target}\n.stop")

@_guard
async def cmd_host1(update, ctx): await _host_file(update, ctx, 1)

@_guard
async def cmd_host2(update, ctx): await _host_file(update, ctx, 2)

@_guard
async def cmd_stophost(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if not args: await _reply(msg, "⚠️ .stophost <1/2/all>"); return
    t = args[0].lower(); res = []
    if t == "1": res.append((await stop_script(msg.chat_id, "script1"))[1])
    elif t == "2": res.append((await stop_script(msg.chat_id, "script2"))[1])
    elif t == "all":
        for s in ["script1", "script2"]: res.append((await stop_script(msg.chat_id, s))[1])
    else: await _reply(msg, "⚠️ Use 1/2/all"); return
    still = _host_active(msg.chat_id)
    status = "\n\n🟢 HOST still active" if still else "\n\n✅ ARYA.py commands resumed"
    await _reply(msg, f"🛑 STOP\n" + "\n".join(res) + status)

@_guard
async def cmd_hoststat(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    cid = msg.chat_id
    if cid not in hosted_scripts or not hosted_scripts[cid]:
        await _reply(msg, "📋 No scripts running.\n💡 .host1 file.py"); return
    lines = ["📋 HOST STATUS\n"]
    for sid, data in hosted_scripts[cid].items():
        running = data["process"].returncode is None
        meta = hosted_menus.get(cid, {}).get(sid, {})
        slot = 1 if sid == "script1" else 2
        lines.append(f"{'🟢' if running else '🔴'} {sid.upper()}\n  📁 {os.path.basename(data['path'])}\n  ⏱ {data['started']}\n  🎯 {len(meta.get('commands', []))} cmds\n  📖 .menufile{slot}\n")
    await _reply(msg, "\n".join(lines))

@_guard
async def cmd_hostlog(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    args = _get_args(ctx)
    if not args or args[0] not in ("1", "2"):
        await _reply(msg, "⚠️ .hostlog <1/2>"); return
    slot = args[0]
    lp = os.path.join(LOG_DIR, f"{msg.chat_id}_script{slot}.log")
    if not os.path.exists(lp): await _reply(msg, "📋 No log found"); return
    try:
        with open(lp, "r", encoding="utf-8", errors="ignore") as f: content = f.read()
        if not content.strip(): await _reply(msg, "📋 Log empty"); return
        tail = content[-3000:]
        for chunk in _split_text(f"📋 HOST LOG SLOT {slot}\n\n```\n{tail}\n```"):
            try: await msg.reply_text(chunk)
            except Exception: pass
    except Exception as e: await _reply(msg, f"⚠️ {e}")

async def _show_file_menu(msg, slot):
    cid = msg.chat_id; sid = f"script{slot}"
    if cid not in hosted_scripts or sid not in hosted_scripts[cid]:
        await _reply(msg, f"❌ Slot {slot} not running\n💡 .host{slot} <file.py>"); return
    data = hosted_scripts[cid][sid]
    meta = hosted_menus.get(cid, {}).get(sid, {})
    cmds = meta.get("commands", []); prefix = meta.get("prefix", ".")
    tokens = meta.get("tokens", []); owners = meta.get("owner_ids", [])
    running = data["process"].returncode is None
    cmd_text = "\n".join(f"  ✨ `{prefix}{c}`" for c in cmds) if cmds else "  ⚠️ No commands detected"
    text = (
        f"╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮\n"
        f"  📜 HOSTED FILE MENU — SLOT {slot}\n"
        f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
        f"📁 File: `{os.path.basename(data['path'])}`\n"
        f"📊 Status: {'🟢 Running' if running else '🔴 Stopped'}\n"
        f"⏱ Started: {data['started']}\n"
        f"📄 Lines: {meta.get('lines', 0)}\n"
        f"🔤 Prefix: `{prefix}`\n"
        f"🎯 Total Commands: {len(cmds)}\n"
        f"🔑 Bot Tokens: {len(tokens)}\n"
        f"👑 Owner IDs: {', '.join(str(o) for o in owners) if owners else 'None'}\n"
        f"⚙️ Type: {meta.get('type', 'unknown')}\n"
        f"🔐 Owner Check: {'✅' if meta.get('has_owner_check') else '❌'}\n\n"
        f"╔══════════════════════════════╗\n"
        f"  📖 COMMANDS\n"
        f"╚══════════════════════════════╝\n"
        f"{cmd_text}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛑 Stop: `.stophost {slot}`\n"
        f"🔄 Refresh: `.menu{'file1' if slot==1 else 'file2'}`"
    )
    await _reply(msg, text)

@_guard
async def cmd_menufile1(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    await _show_file_menu(msg, 1)

@_guard
async def cmd_menufile2(update, ctx):
    msg = update.message or update.edited_message
    if not msg: return
    await _show_file_menu(msg, 2)

# ═══════════════════════════════════════════════════════════
# PASSIVE MESSAGE HANDLER
# ═══════════════════════════════════════════════════════════
async def _on_message(update, ctx):
    msg = update.message or update.edited_message
    if not msg or not msg.chat_id: return
    cid = msg.chat_id; uid = update.effective_user.id if update.effective_user else None
    known_chats.add(cid)
    if cid in autoreply_chats:
        try: await msg.reply_text(autoreply_chats[cid])
        except Exception: pass
    if cid in autoreact_chats:
        try: await msg.set_reaction([ReactionTypeEmoji(autoreact_chats[cid])])
        except Exception: pass
    if cid in ncdel_chats:
        try: await msg.delete()
        except Exception: pass
    if uid and cid in targetreply_chats and targetreply_chats[cid]["uid"] == uid:
        tr = targetreply_chats[cid]
        async def _s(bot):
            try: await bot.send_message(cid, tr["text"], reply_parameters=ReplyParameters(message_id=msg.message_id, allow_sending_without_reply=False))
            except Exception: pass
        asyncio.create_task(asyncio.gather(*[_s(b) for b in _bots()]))
    if uid and cid in targetslide_chats and targetslide_chats[cid]["uid"] == uid:
        ts = targetslide_chats[cid]
        async def _s(bot):
            try: await bot.send_message(cid, ts["text"], reply_parameters=ReplyParameters(message_id=msg.message_id, allow_sending_without_reply=False))
            except Exception: pass
        asyncio.create_task(asyncio.gather(*[_s(b) for b in _bots()]))
    if cid in replyflood_chats:
        ft = replyflood_chats[cid]
        async def _s(bot):
            try: await bot.send_message(cid, ft, reply_parameters=ReplyParameters(message_id=msg.message_id, allow_sending_without_reply=False))
            except Exception: pass
        asyncio.create_task(asyncio.gather(*[_s(b) for b in _bots()]))

# ═══════════════════════════════════════════════════════════
# PREFIX HANDLER
# ═══════════════════════════════════════════════════════════
_UNI_NORM = str.maketrans(
    "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

def _normalize_cmd(s): return s.translate(_UNI_NORM)

CMD_MAP = {
    "stop": cmd_stop, "menu": cmd_menu, "menuall": cmd_menuall,
    "nc": cmd_nc, "snc": cmd_snc,
    "aryagod1": cmd_aryagod1, "aryagod2": cmd_aryagod2, "aryagod3": cmd_aryagod3,
    "aryagod4": cmd_aryagod4, "aryagod5": cmd_aryagod5,
    "arya1": cmd_arya1, "chud": cmd_chud, "triogod": cmd_triogod, "silknc": cmd_silknc,
    "boldnc": cmd_boldnc, "wavenc": cmd_wavenc, "aryancs": cmd_aryancs,
    "randomcod": cmd_randomcod, "godcod": cmd_godcod,
    "phantom": cmd_phantom, "testament": cmd_testament, "shadow": cmd_shadow,
    "ncdel": cmd_ncdel, "ncwar": cmd_ncwar, "stopncwar": cmd_stopncwar,
    "multiwar": cmd_multiwar, "stopmultiwar": cmd_stopmultiwar,
    "mute": cmd_mute, "unmute": cmd_unmute,
    "spam": cmd_spam, "stopspam": cmd_stopspam,
    "spam1": cmd_spam1, "spam2": cmd_spam2, "spam3": cmd_spam3,
    "slidespam": cmd_slidespam, "stopslide": cmd_stopslide,
    "swipespam": cmd_swipespam, "ss": cmd_swipespam,
    "burstspam": cmd_burstspam, "bs": cmd_burstspam,
    "chudspam": cmd_chudspam, "cs": cmd_chudspam,
    "rapidfire": cmd_rapidfire, "rap": cmd_rapidfire,
    "replyflood": cmd_replyflood, "rf": cmd_replyflood,
    "tagspam": cmd_tagspam, "ts": cmd_tagspam,
    "rr": cmd_rr, "mr": cmd_mr, "rs": cmd_rs, "rl": cmd_rl,
    "addtemplate": cmd_addtemplate, "cnc": cmd_cnc,
    "templates": cmd_templates, "preview": cmd_preview,
    "deltemplate": cmd_deltemplate, "cleartemplates": cmd_cleartemplates,
    "purge": cmd_purge, "purgeme": cmd_purgeme,
    "purgebot": cmd_purgebot, "purgeall": cmd_purgeall,
    "setautoreply": cmd_setautoreply, "setautoreact": cmd_setautoreact,
    "addsudo": cmd_addsudo, "removesudo": cmd_removesudo, "sudolist": cmd_sudolist,
    "status": cmd_status, "uptime": cmd_uptime, "ping": cmd_ping,
    "setdelay": cmd_setdelay, "gclist": cmd_gclist, "floodstat": cmd_floodstat,
    "globalstop": cmd_globalstop,
    "bots": cmd_bots, "addbot": cmd_addbot, "addallbots": cmd_addallbots,
    "promotebot": cmd_promotebot, "botname": cmd_botname,
    "gcinfo": cmd_gcinfo, "setgctitle": cmd_setgctitle, "setgcdesc": cmd_setgcdesc,
    "getinvite": cmd_getinvite, "pinmsg": cmd_pinmsg, "unpinall": cmd_unpinall,
    "kickuser": cmd_kickuser, "bantarget": cmd_bantarget,
    "unbanuser": cmd_unbanuser, "muteuser": cmd_muteuser, "unmuteuser": cmd_unmuteuser,
    "setpfponce": cmd_setpfponce, "deletegcpfp": cmd_deletegcpfp,
    "addpfp": cmd_addpfp, "pfploop": cmd_pfploop, "stoppfploop": cmd_stoppfploop,
    "pfppool": cmd_pfppool, "clearpfp": cmd_clearpfp,
    "targetreply": cmd_targetreply, "stoptargetreply": cmd_stoptargetreply,
    "targetslide": cmd_targetslide, "stoptargetslide": cmd_stoptargetslide,
    "over": cmd_over, "song": cmd_song, "image": cmd_image, "yt": cmd_yt,
    "logo": cmd_logo, "fem": cmd_fem, "info": cmd_info, "aryainfo": cmd_aryainfo,
    "aryanc1": cmd_aryanc1, "aryanc2": cmd_aryanc2, "aryanc3": cmd_aryanc3,
    "aryanc4": cmd_aryanc4, "aryanc5": cmd_aryanc5,
    "aryaspam1": cmd_aryaspam1, "aryaspam2": cmd_aryaspam2,
    "aryabignc": cmd_aryabignc, "aryancspam": cmd_aryancspam,
    "host1": cmd_host1, "host2": cmd_host2, "stophost": cmd_stophost,
    "hoststat": cmd_hoststat, "hostlog": cmd_hostlog,
    "menufile1": cmd_menufile1, "menufile2": cmd_menufile2,
}

async def _prefix_handler(update, ctx):
    msg = update.message or update.edited_message
    if not msg or not msg.text: return
    raw = msg.text.strip()
    if not raw.startswith("."):
        await _on_message(update, ctx); return
    user = update.effective_user
    if not user or not is_admin(user.id):
        try: await msg.reply_text(_GATE)
        except Exception: pass
        return
    body = _normalize_cmd(raw[1:].strip())
    parts = body.split()
    if not parts: return
    cmd = parts[0].lower()
    ctx.args = parts[1:] if len(parts) > 1 else []

    # HOST OVERRIDE — agar file hosted + running hai to ARYA.py silent
    if _host_active(msg.chat_id) and cmd not in MANAGEMENT_CMDS:
        return

    if cmd in CMD_MAP:
        await CMD_MAP[cmd](update, ctx)
    else:
        await _on_message(update, ctx)

# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
async def _startup_msg(app):
    try:
        await app.bot.send_message(OWNER_ID,
            "⚡ ARYA STARTED\nPrefix: .\nMenu: .menu\nHost: .host1/.host2\nHost Menu: .menufile1/.menufile2")
    except Exception: pass

async def _run_one_app(app):
    try:
        await app.initialize()
        all_bot_instances.append(app.bot)
        await app.start()
        await _startup_msg(app)
        await app.updater.start_polling(drop_pending_updates=True)
        print(f"[✓] @{app.bot.username} polling")
    except Exception as e:
        print(f"[!] Bot startup failed: {e}"); return
    await _stop_event.wait()
    try: await app.updater.stop()
    except Exception: pass
    try: await app.stop()
    except Exception: pass
    try: await app.shutdown()
    except Exception: pass

_stop_event = asyncio.Event()

async def main():
    global _stop_event
    _stop_event = asyncio.Event()
    tokens = list(dict.fromkeys(BASE_TOKENS + _load_json(TOKENS_FILE, [])))
    for tok in tokens:
        tok = tok.strip()
        if not tok: continue
        try:
            app = Application.builder().token(tok).connect_timeout(10).read_timeout(30).write_timeout(10).pool_timeout(10).build()
            app.add_handler(MessageHandler(filters.ALL, _prefix_handler))
            app.add_handler(CallbackQueryHandler(_menu_callback))
            all_apps.append(app)
        except Exception as e:
            print(f"[!] Build failed {tok[:20]}: {e}")
    if not all_apps:
        print("[!] No bots built"); return
    try:
        fp = load_all_fonts()
        print(f"[*] Fonts loaded: {len(fp)}")
    except Exception as e:
        print(f"[!] Font: {e}")
    print(f"[*] Starting {len(all_apps)} bots — ARYA")
    print(f"[*] OWNER_ID: {OWNER_ID}")
    runners = [asyncio.create_task(_run_one_app(app)) for app in all_apps]
    loop = asyncio.get_running_loop()
    try:
        import signal
        loop.add_signal_handler(signal.SIGINT, _stop_event.set)
        loop.add_signal_handler(signal.SIGTERM, _stop_event.set)
    except Exception: pass
    await _stop_event.wait()
    for r in runners:
        if not r.done(): r.cancel()
    await asyncio.gather(*runners, return_exceptions=True)
    print("[✓] Stopped.")

def _self_restart():
    import subprocess
    _me = os.path.abspath(__file__)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  ARYA BOT  ")
    print("  Menu: .menu | Menuall: .menuall")
    print("  Host: .host1/.host2")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    while True:
        try: subprocess.run([sys.executable, _me, "--child"])
        except KeyboardInterrupt:
            print("\n[✓] Stopped"); break
        except Exception: pass
        print("[!] Restarting in 3s...")
        try: time.sleep(3)
        except KeyboardInterrupt: break

if __name__ == "__main__":
    if "--child" in sys.argv:
        asyncio.run(main())
    else:
        _self_restart()
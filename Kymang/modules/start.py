#Kymang

import asyncio
import random
from io import BytesIO
import subprocess
import os
import sys
from datetime import datetime, timedelta
from distutils.util import strtobool
from time import time

from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from pyrogram.types import *

from Kymang import Bot, bot
from Kymang.config import *
from Kymang.modules.func import *


def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Kymang"])


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60**2 * 24),
    ("hour", 60**2),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{"" if amount == 1 else "s"}')
    return ", ".join(parts)

selections = [f"Semoga Anda Beruntung **✗ {i} 🚀 🚀**" for i in range(1, 30)]

# Dictionary untuk menyimpan waktu terakhir pengguna menggunakan perintah
last_used = {}

MEMBER = []  # Daftar member premium
ACCESS_TIME = {}  # Menyimpan waktu akses member premium
                                 
start_msg = """
**ʜᴀʟᴏ {}👋,

sᴀʏᴀ ᴀᴅᴀʟᴀʜ {}​ 
sɪʟᴀʜᴋᴀɴ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪʙᴀᴡᴀʜ ɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪɴʏᴀ**
"""


buttons2 = [
    [
        InlineKeyboardButton("Predictor 🚀", callback_data="buat_bot"),
    ],
    [
        InlineKeyboardButton("📎 Link Daftar", url="https://suara89.info/biqz"),
        InlineKeyboardButton("👨‍💻 Admin", callback_data="cb_admines"),
    ],
    [
        InlineKeyboardButton("💌 Live Chat", callback_data="support"),
    ],
]

@bot.on_message(filters.command("start") & filters.private)
async def start_bot(c, m):
    if c.me.id == BOT_ID:
        await add_user(c.me.id, m.from_user.id)
        await m.reply(
            start_msg.format(m.from_user.mention, c.me.mention),
            reply_markup=InlineKeyboardMarkup(buttons2),
        )
        return

@bot.on_message(filters.command("predik"))
async def predik(c, m):
    user_id = m.from_user.id
    seller = await seller_info(user_id)  # Hanya menggunakan user_id untuk memeriksa seller

    # Cek apakah pengguna adalah seller
    if not seller:
        await m.reply_text("**Untuk mengakses fitur Premium ini, Anda perlu melakukan pembelian.**\n**Beli sekarang untuk menggunakan Predictor**")
        return
    current_time = datetime.now()

    # Cek apakah pengguna sudah menggunakan perintah dalam 1 menit terakhir
    if user_id in last_used:
        time_diff = current_time - last_used[user_id]
        if time_diff < timedelta(seconds=10):
            remaining_time = 10 - time_diff.seconds
            await m.reply_text(f"Silakan tunggu {remaining_time} detik sebelum menggunakan perintah ini lagi.")
            return

    # Memperbarui waktu terakhir digunakan
    last_used[user_id] = current_time

    # Mengirim pesan bahwa bot sedang memproses
    x = await m.reply_text("`Tunggu Sebentar...`")
    await asyncio.sleep(2)
    
    # Memilih prediksi secara acak
    bar = random.choice(selections)
    
    # Mendapatkan waktu saat ini dan menambahkannya 7 jam untuk WIB, lalu menambah 1 menit
    wib_time = datetime.now() + timedelta(hours=7, minutes=1)
    formatted_time = wib_time.strftime("%H:%M")  # Format jam:menit

    # Membuat tombol inline
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Dapatkan Lagi", url=f"https://t.me/{c.me.username}?start=predik")]
        [InlineKeyboardButton("Batal", callback_data="cancel")]
    ])
    
    # Mengedit pesan sebelumnya untuk menghapus pesan "Tunggu Sebentar..."
    await x.delete()

    # Mengirim prediksi dan waktu yang diprediksi
    await m.reply_text(f"{bar}\n\n**Waktu prediksi (WIB):** {formatted_time}", reply_markup=reply_markup)


        
@bot.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_bot(c, m):
    try:
        update_message = await m.reply_text("🔄 Sedang memulai ulang bot....")
        await asyncio.sleep(1)
        await update_message.delete()
        await m.reply_text("**✅ BOT BERHASIL DI MULAI ULANG.**")
        return await restart()
    except Exception as e:
        await m.reply_text("⛔ Terjadi kesalahan saat memulai ulang bot.")
        await m.reply_text(str(e))
    
    
    
@bot.on_message(filters.command("gitpull") & filters.user(ADMINS))
async def update(client, message):
    try:
        update_message = await message.reply_text("🔄 Sedang memproses...")
        out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
        if "Already up to date." in str(out):
            return await update_message.edit_text("**🤖 BOT SUDAH VERSI TERBARU!**")
        await update_message.edit_text(f"**✅ BERHASIL UPDATE BOT**\n\n```{out}```")
        return await restart()
    except Exception as e:
        await message.reply_text("⚙️ Terjadi kesalahan saat melakukan pembaruan.")
        await message.reply_text(str(e))


@bot.on_message(filters.command("help") & filters.user(ADMINS))
async def helper_text(c, m):
    if c.me.id == BOT_ID:
        kymang = await cek_seller()
        if m.from_user.id in kymang:
            return await m.reply(
                    "**Perintah Yang Tersedia**\n\n/akses - Untuk akses deploy user\n/setexp - Untuk set masa aktif bot\n/cekakses - Untuk cek masa aktif bot\n/del - Untuk menghapus pengguna"
                )


@bot.on_message(filters.command("del") & filters.user(ADMINS))
async def del_users(c, m):
    if c.me.id != BOT_ID:
        return
    if len(m.command) < 2:
        return await m.reply("Balas pesan pengguna atau berikan ID Bot/Username Bot.")
    ids = m.command[1] 
    await remove_bot(str(ids))
    await del_owner(int(ids))
    await del_timer(int(ids))
    await m.reply(f"Hapus data untuk id {ids}")
    os.popen(f"rm {ids}*")
    return await restart()


        
@bot.on_message(filters.command("setexp") & filters.user(ADMINS))
async def add_aktif_bot(c, m):
    if len(m.command) < 3:
        return await m.reply(
            "Balas pesan pengguna atau berikan user_id/username., 1 sama dengan 1 hari\ncontoh : /setexp 5081430435 30"
        )
    iya = await seller_info(m.from_user.id)
    if not iya and m.from_user.id not in ADMINS:
        return
    ids = m.command[1]
    h = int(m.command[2])
    time = (datetime.now() + timedelta(h)).strftime("%d-%m-%Y")
    await add_timer(int(ids), time)
    await m.reply(f"**User ID** : {ids}\n**Time** : {time}")


@bot.on_message(filters.command("cekakses") & filters.user(ADMINS))
async def cek_member_prem(c, m):
    iya = await seller_info(m.from_user.id)
    if not iya and m.from_user.id not in ADMINS:
        return
    anu = await cek_prem()
    msg = "**Daftar member premium**\n\n"
    ang = 0
    for ex in anu:
        try:
            afa = f"`{ex['nama']}` » {ex['aktif']}"
            ang += 1
        except Exception:
            continue
        msg += f"{ang} › {afa}\n"
    await m.reply(msg)


async def cancel(callback_query, text):
    if text.startswith("/"):
        await bot.send_message(
            callback_query.from_user.id,
            "Proses di batalkan, silahkan coba lagi",
        )
        return True
    else:
        return False


async def canceled(m):
    if (
        "/cancel" in m.text
        or "/cancel" not in m.text
        and "/clone" in m.text
        or "/cancel" not in m.text
        and "/clone" not in m.text
        and m.text.startswith("/")
    ):
        await m.reply("Proses di batalkan silahkan gunakan /setting", quote=True)
        return True
    else:
        return False



@bot.on_message(filters.command("info") & filters.private)
async def status_mem(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id == int(owner):
        act = await timer_info(c.me.id)
        await c.send_message(
            int(owner),
            f"**Nama** : {c.me.first_name}\n**Id** : `{c.me.id}`\n**Experied** : {act}",
        )
    else:
        return


@bot.on_message(filters.command("ping"))
async def ping_pong(c, m):
    start = time()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    m_reply = await m.reply("Pinging...")
    delta_ping = time() - start
    await m_reply.edit(
        "**PONG!!**🏓 \n"
        f"**• Pinger -** `{delta_ping * 1000:.3f}ms`\n"
        f"**• Uptime -** `{uptime}`\n"
    )


@bot.on_message(filters.command("uptime"))
async def get_uptime(client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        "🤖 **Bot Status:**\n"
        f"• **Uptime:** `{uptime}`\n"
        f"• **Start Time:** `{START_TIME_ISO}`"
    )



@bot.on_message(filters.command("user") & filters.user(ADMINS))
async def get_users(client, message):
    user_id = message.from_user.id
    count = 0
    user = ""
    for X in bot._bot:
        try:
            count += 1
            user += f"""
❏ FSUB KE {count}
 ├ AKUN: {X.me.username}
 ╰ ID: <code>{X.me.id}</code>
"""
        except:
            pass
    if len(str(user)) > 4096:
        with BytesIO(str.encode(str(user))) as out_file:
            out_file.name = "bot.txt"
            await message.reply_document(
                document=out_file,
            )
    else:
        await message.reply(f"<b>{user}</b>")

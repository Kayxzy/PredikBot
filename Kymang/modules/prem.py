from datetime import datetime, timedelta
from pyrogram import filters

from Kymang import Bot, bot
from Kymang.config import *
from Kymang.modules.func import *

# Daftar anggota dengan waktu akses
MEMBERS = {}  # Menggunakan dictionary untuk menyimpan user_id dan waktu akses

async def extract_user(message):
    # Implementasi fungsi ini sesuai kebutuhan Anda
    # Misalnya, mengembalikan username atau ID dari pesan
    return message.command[1] if len(message.command) > 1 else None

@bot.on_message(filters.command("prem") & filters.user(ADMINS))
async def add_members(c, m):
    if c.me.id != BOT_ID:
        return
    if m.from_user.id not in ADMINS:
        return

    args = m.command[1:]  # Ambil argumen setelah perintah
    if len(args) < 2:
        await m.reply("Format yang benar: `/prem <username/id> <durasi>`")
        return

    user_identifier = args[0]
    try:
        duration = int(args[1])  # Mengonversi durasi ke integer
    except ValueError:
        await m.reply("Durasi harus berupa angka.")
        return

    reply = m.reply_to_message
    ex = await m.reply("Processing...")

    if user_identifier:
        try:
            user = await c.get_users(user_identifier)
        except Exception:
            await ex.edit("__User  tidak ditemukan__")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await c.get_users(user_id)
    else:
        await ex.edit("User  tidak ditemukan")
        return

    try:
        if user.id in MEMBERS:
            return await ex.edit("__User  sudah menjadi member__")
        
        # Simpan waktu akses berdasarkan durasi yang diberikan
        MEMBERS[user.id] = datetime.now() + timedelta(days=duration)
        await ex.edit(f"{user.mention} ditambahkan ke members dengan akses selama {duration} hari.")

    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return


@bot.on_message(filters.command("unprem")& filters.user(ADMINS))
async def del_members(c, m):
    if c.me.id != BOT_ID:
        return
    if m.from_user.id not in ADMINS:
        return

    args = await extract_user(m)
    reply = m.reply_to_message
    ex = await m.reply("Processing...")

    if args:
        try:
            user = await c.get_users(args)
        except Exception:
            await ex.edit("User  tidak ditemukan")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await c.get_users(user_id)
    else:
        await ex.edit("User  tidak ditemukan")
        return

    try:
        if user.id not in MEMBERS:
            return await ex.edit("__User  bukan bagian dari members__")
        
        del MEMBERS[user.id]  # Hapus user dari anggota
        await ex.edit(f"{user.mention} sudah dihapus dari members.")

    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return


async def check_access(user_id):
    """Fungsi untuk memeriksa apakah pengguna memiliki akses."""
    if user_id in MEMBERS:
        end_time = MEMBERS[user_id]
        if datetime.now() < end_time:
            return True  # Pengguna memiliki akses
        else:
            del MEMBERS[user_id]  # Hapus akses jika sudah habis
    return False  # Pengguna tidak memiliki akses

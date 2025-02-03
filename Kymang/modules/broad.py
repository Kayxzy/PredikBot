#Kymang idiot

import asyncio 

import os
import sys

from datetime import datetime, timedelta
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, UserDeactivatedBan

from Kymang import bot
from Kymang.config import *
from Kymang.modules.data import *



@bot.on_message(filters.command("users"))
async def get_users(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    adm = await admin_info(c.me.id, m.from_user.id)
    for i in cek:
        owner = i["owner"]
    if not adm and m.from_user.id != owner:
        return
    msg = await c.send_message(m.chat.id, "**Tunggu Sebentar...**")
    users = await get_user(c.me.id)
    await msg.edit(f"**{len(users)} Pengguna Bot Ini.**")


@bot.on_message(filters.command("buser") & filters.user(ADMINS))
async def get_users(c, m):
    if c.me.id != BOT_ID:
        return
    msg = await c.send_message(m.chat.id, "Tunggu Sebentar...")
    users = await get_user(c.me.id)
    await msg.edit(f"{len(users)} user")


@bot.on_message(filters.command("broadcast"))
async def send_text(c: Client, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    adm = await admin_info(c.me.id, m.from_user.id)
    for i in cek:
        owner = i["owner"]
    if not adm and m.from_user.id != owner:
        return
    if not (reply := m.reply_to_message):
        return await m.reply("`/broadcast [Reply ke pesan]`")
    query = await get_user(c.me.id)
    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0

    pls_wait = await m.reply("Tunggu Sebentar...")
    for x in query:
        chat_id = x["user"]
        try:
            await reply.copy(chat_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await reply.copy(chat_id)
            successful += 1
        except UserIsBlocked:
            await del_user(c.me.id, chat_id)
            blocked += 1
        except (UserDeactivatedBan, InputUserDeactivated):
            await del_user(c.me.id, chat_id)
            deleted += 1
        except:
            unsuccessful += 1
        total += 1

    status = f"""**Berhasil Mengirim pesan ke:

Berhasil: {successful}
Gagal: {unsuccessful}
Pengguna Diblokir: {blocked}
Akun Dihapus: {deleted}
Total Pengguna: {total}**"""

    return await pls_wait.edit(status)


@bot.on_message(filters.private & filters.command("bacot") & filters.user(ADMINS))
async def send_text(c, m):
    if c.me.id != BOT_ID:
        return
    if not (reply := m.reply_to_message):
        return await m.reply("Reply Goblok")
    query = await get_user(c.me.id)
    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0

    pls_wait = await m.reply("SABAR NGENTOT")
    for x in query:
        chat_id = x["user"]
        try:
            await reply.copy(chat_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await reply.copy(chat_id)
            successful += 1
        except UserIsBlocked:
            await del_user(c.me.id, chat_id)
            blocked += 1
        except (UserDeactivatedBan, InputUserDeactivated):
            await del_user(c.me.id, chat_id)
            deleted += 1
        except:
            unsuccessful += 1
        total += 1

    status = f"""**Berhasil Mengirim pesan ke:

Berhasil: {successful}
Gagal: {unsuccessful}
Pengguna Diblokir: {blocked}
Akun Dihapus: {deleted}
Total Pengguna: {total}**"""

    return await pls_wait.edit(status)




@bot.on_message(filters.command("listadmin"))
async def cek_admin_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    msg = "**Daftar Admin**\n\n"
    admins = await cek_admin(c.me.id)
    if admins is False:
        return await m.reply("Belum ada Admin yang terdaftar.")
    for i, ex in enumerate(admins, 1):
        msg += f"{i} › `{ex['admin']}`\n"
    return await m.reply(msg)



# Misalkan kita menggunakan dictionary untuk menyimpan informasi seller
@bot.on_message(filters.command("prem") & filters.user(ADMINS))
async def add_seller_sub(c, m):
    if c.me.id != BOT_ID:
        return
    if len(m.command) < 2:
        return await m.reply(
            "Balas pesan pengguna atau berikan user_id/username."
        )
    ids = m.command[1]
    iya = await seller_info(int(ids))
    if not iya:
        await add_seller(int(ids))
        await m.reply(f"User {ids} Berhasil di tambahkan ke premium")
    else:
        await m.reply(f"User {ids} Sudah menjadi premium")


@bot.on_message(filters.command("unprem") & filters.user(ADMINS))
async def del_seller_sub(c, m):
    if c.me.id != BOT_ID:
        return
    if len(m.command) < 2:
        return await m.reply(
            "Balas pesan pengguna atau berikan user_id/username."
        )
    ids = m.command[1]
    iya = await seller_info(int(ids))
    if iya:
        await del_seller(int(ids))
        await m.reply(f"{ids} Berhasil di hapus dari premium")
    else:
        await m.reply(f"{ids} Bukan bagian dari premium")


@bot.on_message(filters.command("dprem") & filters.user(ADMINS))
async def list_sellers(c, m):
    if c.me.id != BOT_ID:
        return
    
    sellers = await cek_seller()  # Mengambil daftar seller (ID pengguna)
    
    if not sellers:
        return await m.reply("Tidak ada premium yang terdaftar.")
    
    seller_list = []
    for user_id in sellers:
        try:
            user = await bot.get_chat(user_id)  # Mengambil objek pengguna berdasarkan ID
            full_name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
            mention = f"[{full_name}](tg://user?id={user_id})"  # Format mention
            seller_list.append(f"• {mention} (ID: {user_id})")  # Menggunakan mention dan ID
        except Exception as e:
            seller_list.append(f"• User ID: {user_id} (tidak dapat diambil)")  # Menangani kesalahan jika pengguna tidak ditemukan

    await m.reply(f"Daftar Premium:\n" + "\n".join(seller_list), parse_mode='Markdown')


@bot.on_message(filters.private & filters.command("protect"))
async def set_protect(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    adm = await admin_info(c.me.id, m.from_user.id)
    for i in cek:
        owner = i["owner"]
    if not adm and m.from_user.id != owner:
        return
    if len(m.command) < 2:
        return await m.reply(
            "`/protect [True/False]`"
        )
    jk = m.command[1]
    if jk in ["True", "False"]:
        await add_protect(c.me.id, jk)
        await m.reply(f"Berhasil mengatur protect menjadi {jk}")
    else:
        await m.reply(f"{jk} Format salah, Gunakan `/protect [True/False]`.")



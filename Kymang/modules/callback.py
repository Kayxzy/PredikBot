import asyncio
import importlib
import logging
import os
import random
from datetime import datetime, timedelta
from pykeyboard import InlineKeyboard
from pyrogram import Client, filters
from pyrogram.types import *

from Kymang import Bot, bot
from Kymang.config import *
from Kymang.modules import loadModule
from Kymang.modules.data import *
from Kymang.modules.func import *


from .start import (
    buttons2,
    cancel,
    start_msg,
)

lonte = []
# Daftar pilihan untuk prediksi
selections = [f"Semoga Anda Beruntung **✗ {i} 🚀 🚀**" for i in range(1, 30)]

# Dictionary untuk menyimpan waktu terakhir pengguna menggunakan perintah
last_used = {}
current_tasks = {}

logs = logging.getLogger(__name__)


@bot.on_callback_query(filters.regex("cb_admines"))
async def _(_, query: CallbackQuery):
    return await query.edit_message_text(
        """
    <b> 💌 Silakan Hubungi Admin Dibawah Jika Anda Membutuhkan Bantuan.</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="👨‍💻 Admin", user_id=6677920913),
                ],
                [
                    InlineKeyboardButton(
                        "Back", callback_data="back_start"),
                ],
            ]
        ),
    )

@bot.on_callback_query(filters.regex("get_payment"))
async def _(_, query: CallbackQuery):
    return await query.edit_message_text(
        "**Untuk mengakses bot ini, Anda perlu mendapatkan akses penuh.**\n**Untuk menggunakan bot prediksi, hubungi Admin dibawah.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="👨‍💻 Admin", user_id=6677920913),
                ],
                [
                    InlineKeyboardButton(
                        "Back", callback_data="back_start"),
                ],
            ]
        ),
    )


@bot.on_callback_query(filters.regex("cb_about"))
async def _(c: Client, query: CallbackQuery):
    ownerObj = (await cek_owner(c.me.id))[0]
    owner = ownerObj["owner"]
    try:
        user = await c.get_users(owner)
    except BaseException as a:
        print(a)
        return
    await query.message.edit(
        about_msg.format(c.me.mention, user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data="bck_cb"),
                ],
            ]
        ),
    )
                 

@bot.on_callback_query(filters.regex("cb_tutor"))
async def _(_, callback_query: CallbackQuery):
    await callback_query.message.edit(
        text="**Berikut adalah video tutorial\n**Gabung Channel dibawah ini untuk melihat tutorial!**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🎥 Tutorial", url="https://t.me/TutorialDeploy"
                    ),
                ],
                [
                    InlineKeyboardButton("Back", callback_data="back_start"),
                ],
            ]
        ),
    )
      

@bot.on_callback_query(filters.regex("cb_status"))
async def _(_, callback_query: CallbackQuery):
    anu = await cek_prem()
    status_text = ""
    for ex in anu:
        try:
            afa = f"`{ex['nama']}` » {ex['aktif']}"
            status_text += f"{afa}\n"
        except Exception as e:
            print(f"Error: {e}")

    text_to_send = "❌ Bot belum aktif"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Back", callback_data="back_start"),
            ],
        ]
    )
    await callback_query.message.edit(
        text=text_to_send,
        reply_markup=reply_markup,
    )

@bot.on_callback_query(filters.regex("back_start"))
async def back_start_bc(c, callback_query: CallbackQuery):
    await callback_query.message.edit(
        start_msg.format(callback_query.from_user.mention, c.me.mention),
        reply_markup=InlineKeyboardMarkup(buttons2),
    )


    
@bot.on_callback_query(filters.regex("get_prediction"))
async def get_another_prediction(c, callback_query):
    user_id = callback_query.from_user.id# Mendapatkan ID pengguna
    seller = await seller_info(user_id)  # Hanya menggunakan user_id untuk memeriksa seller
    
    if not seller:
        await callback_query.message.edit(
            "**Untuk mengakses fitur Premium ini, Anda perlu melakukan pembelian.**\n**Beli sekarang untuk menggunakan Predictor**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back", callback_data="back_start")]  # Correctly wrapped in a list
            ])
        )
        return
    current_time = datetime.now()
    
    # Cek apakah pengguna sudah menggunakan perintah dalam 1 menit terakhir
    if user_id in last_used:
        time_diff = current_time - last_used[user_id]
        if time_diff < timedelta(seconds=3):
            remaining_time = 3 - time_diff.seconds
            await callback_query.message.edit(f"Silakan tunggu {remaining_time} detik sebelum menggunakan perintah ini lagi.")
            return

    # Memperbarui waktu terakhir digunakan
    last_used[user_id] = current_time
    bar = random.choice(selections)  # Memilih prediksi baru
    
    # Mendapatkan waktu saat ini dan menambahkannya 7 jam untuk WIB, lalu menambah 1 menit
    wib_time = datetime.now() + timedelta(hours=7, minutes=1)
    formatted_time = wib_time.strftime("%H:%M")  # Format jam:menit
    x = await callback_query.message.edit("`Tunggu Sebentar...`")
    await asyncio.sleep(1)
    # Mengedit pesan dengan prediksi baru dan waktu yang diprediksi
    await callback_query.message.edit_text(f"{bar}\n\n**Waktu prediksi (WIB):** {formatted_time}", 
        reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Coba Lagi", callback_data="get_prediction")],
        [InlineKeyboardButton("Back", callback_data="back_start")]
    ]))


@bot.on_callback_query(filters.regex("support"))
async def support(c, callback_query: CallbackQuery):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    

    try:
        buttons = [
            [InlineKeyboardButton("❌ Batal", callback_data=f"batal {user_id}")]
        ]
        pesan = await c.ask(
            user_id,
            "Kirimkan Pesan Anda, Admin akan membalas Pesan anda secepatnya.",
            reply_markup=InlineKeyboardMarkup(buttons),
            timeout=60,
        )
        await c.send_message(
            user_id, "✅ Pesan Anda Telah Dikirim Ke Admin, Silahkan Tunggu Balasannya"
        )
        await callback_query.message.delete()
    except asyncio.TimeoutError:
        return await c.send_message(user_id, "**Pembatalan otomatis**")

    button = [
        [
            InlineKeyboardButton(full_name, user_id=user_id),
            InlineKeyboardButton("💌 Jawab", callback_data=f"jawab_pesan {user_id}"),
        ],
    ]
    await pesan.copy(
        LOG_GRP,
        reply_markup=InlineKeyboardMarkup(button),
    )
    
@bot.on_callback_query(filters.regex("jawab_pesan"))
async def jawab_pesan(c, callback_query: CallbackQuery):
    user_id = int(callback_query.from_user.id)
    user_ids = int(callback_query.data.split()[1])
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    
        
    if user_ids == LOG_GRP:
        try:
            button = [
                [InlineKeyboardButton("Batal", callback_data=f"batal {user_id}")]
            ]
            pesan = await c.ask(
                user_id,
                "Silahkan Kirimkan Balasan Anda.",
                reply_markup=InlineKeyboardMarkup(button),
                timeout=60,
            )
            await c.send_message(
                user_id,
                "✅ Pesan Anda Telah Dikirim Ke Admin, Silahkan Tunggu Balasannya",
            )
            await callback_query.message.delete()
        except asyncio.TimeoutError:
            return await c.send_message(user_id, "**❌ Pembatalkan otomatis**")
        
        buttons = [
            [
                InlineKeyboardButton(full_name, user_id=user_id),
                InlineKeyboardButton("Jawab", callback_data=f"jawab_pesan {user_id}"),
            ],
        ]
    else:
        try:
            button = [
                [InlineKeyboardButton("Batal", callback_data=f"batal {LOG_GRP}")]
            ]
            pesan = await c.ask(
                LOG_GRP,
                "💌 Silahkan Kirimkan Balasan Anda.",
                reply_markup=InlineKeyboardMarkup(button),
                timeout=60,
            )
            await c.send_message(
                LOG_GRP,
                "✅ Pesan Anda Telah Dikirim Ke User, Silahkan Tunggu Balasannya",
            )
            await callback_query.message.delete()
        except asyncio.TimeoutError:
            return await c.send_message(LOG_GRP, "**Pembatalan otomatis**")
        
        buttons = [
            [
                InlineKeyboardButton("💌 Jawab", callback_data=f"jawab_pesan {LOG_GRP}"),
            ],
        ]

    await pesan.copy(
        user_ids,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

        
    
@bot.on_callback_query(filters.regex("batal"))
async def cancel(client, callback_query: CallbackQuery):
    user_ids = int(callback_query.data.split()[1])
    
    if user_ids in current_tasks:
        current_tasks[user_ids].cancel()  # Batalkan task yang sedang berjalan
        del current_tasks[user_ids]  # Hapus referensi task yang dibatalkan

    if user_ids == LOG_GRP:
        await client.send_message(LOG_GRP, "**❌ Pesan di batalkan**")
    else:
        await client.send_message(user_ids, "**❌ Pesan di batalkan**")
    
    await callback_query.message.delete()
    return True




@bot.on_callback_query(filters.regex("close"))
async def cb_close(c, query: CallbackQuery):
    try:
        await query.answer()
        await query.message.delete()
    except BaseException as e:
        logs.info(e)



#Kymang anak tolol

from motor.motor_asyncio import AsyncIOMotorClient

from Kymang.config import MONGO_URL

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.premiumsub


botdb = mongodb.fsubprem
ownerdb = mongodb.owner
subdb = mongodb.sub
broaddb = mongodb.broad
premdb = mongodb.premium
aktifdb = mongodb.aktif
admindb = mongodb.admin
sellerdb = mongodb.seller
protectdb = mongodb.protect
membersprem = mongodb.members

# bot
async def get_bot():
    data = []
    async for bt in botdb.find({"user_id": {"$exists": 1}}):
        data.append(
            dict(
                name=str(bt["user_id"]),
                api_id=bt["api_id"],
                api_hash=bt["api_hash"],
                bot_token=bt["bot_token"],
            )
        )
    return data


async def add_bot(user_id, api_id, api_hash, token):
    cek = await botdb.find_one({"user_id": user_id})
    if cek:
        await botdb.update_one(
            {"user_id": user_id},
            {"$set": {"api_id": api_id, "api_hash": api_hash, "bot_token": token}},
        )
    else:
        await botdb.insert_one(
            {
                "user_id": user_id,
                "api_id": api_id,
                "api_hash": api_hash,
                "bot_token": token,
            }
        )


async def remove_bot(user_id):
    return await botdb.delete_one({"user_id": user_id})


# owner
async def cek_owner(user_id):
    if r := [jo async for jo in ownerdb.find({"user_id": user_id})]:
        return r
    else:
        return False


async def add_owner(user_id, owner, channel):
    ssize = await ownerdb.find_one({"user_id": user_id})
    if ssize:
        await ownerdb.update_one(
            {"user_id": user_id},
            {"$set": {"owner": owner, "channel": channel}},
        )
    else:
        await ownerdb.insert_one(
            {
                "user_id": user_id,
                "owner": owner,
                "channel": channel,
            }
        )


async def del_owner(user_id):
    await ownerdb.delete_one({"user_id": user_id})


# sub
async def add_sub(user_id, sub):
    subs = await subdb.find_one({"user_id": user_id, "sub": sub})
    if subs:
        await subdb.update_one(
            {"user_id": user_id},
            {"$set": {"sub": sub}},
        )
    else:
        await subdb.insert_one({"user_id": user_id, "sub": sub})


async def get_subs(user_id):
    if r := [jo async for jo in subdb.find({"user_id": user_id})]:
        return r
    else:
        return None


async def sub_info(user_id, sub):
    subs = await subdb.find_one({"user_id": user_id, "sub": sub})
    return None if not subs else subs["sub"]


async def del_sub(user_id, sub):
    await subdb.delete_one({"user_id": user_id, "sub": sub})


# broad
async def add_user(user_id, user):
    ssize = await broaddb.find_one({"user_id": user_id, "user": user})
    if ssize:
        await broaddb.update_one(
            {"user_id": user_id},
            {"$set": {"user": user}},
        )
    else:
        await broaddb.insert_one({"user_id": user_id, "user": user})


async def get_user(user_id):
    if r := [jo async for jo in broaddb.find({"user_id": user_id})]:
        return r
    else:
        return False


async def del_user(user_id, user):
    await broaddb.delete_one({"user_id": user_id, "user": user})


# aktif
async def add_timer(user_id, time):
    ssize = await aktifdb.find_one({"_id": user_id})
    if ssize:
        await aktifdb.update_one(
            {"_id": user_id},
            {"$set": {"time": time}},
        )
    else:
        await aktifdb.insert_one({"_id": user_id, "time": time})


async def del_timer(user_id):
    await aktifdb.delete_one({"_id": user_id})


async def timer_info(user_id):
    active = await aktifdb.find_one({"_id": user_id})
    return "Belum" if not active else active["time"]


async def cek_prem():
    data = []
    async for i in aktifdb.find({"_id": {"$exists": 1}}):
        data.append(
            dict(
                nama=str(i["_id"]),
                aktif=i["time"],
            )
        )
    return data


# admin
async def add_admin(user_id, admin):
    await admindb.insert_one({"user_id": user_id, "admin": admin})


async def del_admin(user_id, admin):
    await admindb.delete_one({"user_id": user_id, "admin": admin})


async def cek_admin(user_id):
    if x := [jo async for jo in admindb.find({"user_id": user_id})]:
        return x
    else:
        return False


async def admin_info(user_id, admin):
    g = await admindb.find_one({"user_id": user_id, "admin": admin})
    return g if g else False


# seller
async def add_seller(user_id):
    await sellerdb.insert_one({"_id": user_id})


async def del_seller(user_id):
    await sellerdb.delete_one({"_id": user_id})


async def cek_seller():
    user_ids = []
    async for ids in sellerdb.find({"_id": {"$gt": 0}}):
        user_id = ids["_id"]
        user_ids.append(user_id)
    return user_ids


async def seller_info(user_id):
    g = await sellerdb.find_one({"_id": user_id})
    return g if g else False


# protect
async def add_protect(user_id, protect):
    ssize = await protectdb.find_one({"_id": user_id})
    if ssize:
        await protectdb.update_one(
            {"_id": user_id},
            {"$set": {"protect": protect}},
        )
    else:
        await protectdb.insert_one({"_id": user_id, "protect": protect})


async def protect_info(user_id):
    active = await protectdb.find_one({"_id": user_id})
    return "True" if not active else active["protect"]

async def add_max(user_id, maxsub):
    ssize = await maxsubdb.find_one({"_id": user_id})
    if ssize:
        await maxsubdb.update_one(
            {"_id": user_id},
            {"$set": {"maxsub": maxsub}},
        )
    else:
        await maxsubdb.insert_one({"_id": user_id, "maxsub": maxsub})

from datetime import datetime, timedelta

async def add_access(user_id, days):
    end_time = datetime.now() + timedelta(days=days)
    
    # Data yang akan disimpan
    access_data = {
        "user_id": user_id,
        "access_level": "prem",
        "start_time": datetime.now(),
        "end_time": end_time
    }
    
    # Menyimpan data ke MongoDB
    from pymongo import MongoClient
from datetime import datetime, timedelta


async def add_member(user_id, duration):
    """Menambahkan anggota dengan durasi akses."""
    end_time = datetime.now() + timedelta(days=duration)
    member_data = {
        "user_id": user_id,
        "end_time": end_time
    }
    
    # Cek apakah anggota sudah ada
    existing_member = membersprem.find_one({"user_id": user_id})
    if existing_member:
        return "User  sudah menjadi member."
    
    # Tambahkan anggota ke koleksi
    membersprem.insert_one(member_data)
    return f"User  {user_id} ditambahkan dengan akses selama {duration} hari."

async def check_access(user_id):
    """Memeriksa apakah pengguna memiliki akses."""
    member_data = membersprem.find_one({"user_id": user_id})
    if member_data:
        if datetime.now() < member_data["end_time"]:
            return True  # Pengguna memiliki akses
        else:
            # Hapus data jika akses sudah habis
            membersprem.delete_one({"user_id": user_id})
            return False  # Akses sudah habis
    return False  # Pengguna tidak ditemukan

async def remove_member(user_id):
    """Menghapus anggota dari koleksi."""
    result = membersprem.delete_one({"user_id": user_id})
    if result.deleted_count > 0:
        return f"User  {user_id} sudah dihapus dari members."
    return "User  tidak ditemukan."

# Contoh penggunaan
async def main():
    user_id = "123456789"  # Ganti dengan ID pengguna yang sesuai
    duration = 1  # Durasi dalam hari

    # Menambahkan anggota
    print(await add_member(user_id, duration))

    # Memeriksa akses
    if await check_access(user_id):
        print(f"User  {user_id} memiliki akses.")
    else:
        print(f"User  {user_id} tidak memiliki akses.")

    # Menghapus anggota
    print(await remove_member(user_id))


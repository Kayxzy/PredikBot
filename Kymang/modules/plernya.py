from Kymang.config import ADMINS
from Kymang.modules.data import *


async def plernya():
    if 6677920913 not in await cek_seller():
        await add_seller(6677920913)

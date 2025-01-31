#Kymang

import os

from dotenv import load_dotenv

load_dotenv(".env")


BOT_TOKEN = os.environ.get("BOT_TOKEN", "6177375229:AAEL2Lzw8BY9PZctShJ_mwCYcg_pafFS4zw")
API_ID = int(os.environ.get("API_ID", "17131033"))
API_HASH = os.environ.get("API_HASH", "7768488c115ac09684bb38e608c47997")
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://Kayex:Kayex@cluster0.tup4a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
ADMINS = [int(x) for x in (os.environ.get("ADMINS", "1668766845").split())]
MEMBER = [int(x) for x in (os.environ.get("MEMBER", "160").split())]
LOG_GRP = int(os.environ.get("LOG_GRP", "-1002103101233"))
BOT_ID = int(os.environ.get("BOT_ID", "6177375229"))

KITA = [int(x) for x in (os.environ.get("KITA", "1668766845").split())]

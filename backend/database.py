#conexión a mongodb

# ──────────────────────────────────────────────
#  database.py  –  Conexión a MongoDB
# ──────────────────────────────────────────────
from motor.motor_asyncio import AsyncIOMotorClient
import os
 
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME",   "nomina_db")
 
client = AsyncIOMotorClient(MONGO_URL)
db     = client[DB_NAME]
 
# Colección de empleados
empleados_col = db["empleados"]
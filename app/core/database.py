from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

uri = settings.mongo_uri

client = AsyncIOMotorClient(uri)

db = client["meeple_mind"]
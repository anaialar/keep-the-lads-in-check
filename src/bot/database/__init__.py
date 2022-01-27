import os
import motor.motor_asyncio as motor_asyncio
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from bot.database.stickers_cache import BotStickersCacheDatabase
from bot.database.permissions import BotPermissionsDatabase
from bot.database.censored_channels import BotCensoredChannelsDatabase

class BotDatabase:
    database: Database
    stickers_cache: BotStickersCacheDatabase
    permissions: BotPermissionsDatabase
    censored_channels: BotCensoredChannelsDatabase

    default_role_id: int

    def __init__(self):
        self.database = motor_asyncio.AsyncIOMotorClient((os.getenv('MONGODB_URI')))['KeepTheLadsInCheck']
        self.stickers_cache = BotStickersCacheDatabase(self.database)
        self.permissions = BotPermissionsDatabase(self.database)
        self.censored_channels = BotCensoredChannelsDatabase(self.database)

        self.default_role_id = 845110691106259004

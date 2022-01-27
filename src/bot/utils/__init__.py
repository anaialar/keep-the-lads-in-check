import discord
from bot.database import BotDatabase
from bot.utils.messages import BotMessageUtils
from bot.utils.permissions import BotPermissionUtils

class BotUtils:
    messages: BotMessageUtils
    permissions: BotPermissionUtils

    def __init__(self, database: BotDatabase):
        self.messages = BotMessageUtils()
        self.permissions = BotPermissionUtils(database)

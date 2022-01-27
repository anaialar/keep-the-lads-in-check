import discord
from profanityfilter import ProfanityFilter
from bot.utils import BotUtils
from bot.database import BotDatabase
from bot.messages import BotMessages

class BotMaintainance:
    utils: BotUtils
    database: BotDatabase
    profanity_filter: ProfanityFilter

    def __init__(self, database: BotDatabase, utils: BotUtils):
        self.utils = utils
        self.database = database
        self.profanity_filter = ProfanityFilter()
        self.profanity_filter.set_censor("^")

    async def handle_censor_channel(self, message_context: discord.Message) -> None:
        if await self.database.censored_channels.is_censored(message_context.channel.id):
            censored_message = self.profanity_filter.censor(message_context.content)
            if censored_message != message_context.content:
                await self.utils.messages.replace_message(message_context, censored_message)
                await self.utils.messages.delete_message(message_context)

    async def handle_maintainance(self, message_context: discord.Message) -> None:
        await self.handle_censor_channel(message_context)

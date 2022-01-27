import discord
from bot.commands import BotCommands
from bot.utils import BotUtils
from bot.maintainance import BotMaintainance
from bot.database import BotDatabase
from bot.apis import BotAPIs
from bot.messages import BotMessages

class Bot(discord.Client):
    database: BotDatabase
    commands: BotCommands
    utils: BotUtils
    maintainance: BotMaintainance
    apis: BotAPIs
    messages: BotMessages

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        super(Bot, self).__init__(intents = intents)

        self.apis = BotAPIs()
        self.database = BotDatabase()
        self.utils = BotUtils(self.database)
        self.commands = BotCommands(self, self.utils, self.database, self.apis)
        self.maintainance = BotMaintainance(self.database, self.utils)

    async def on_ready(self) -> None:
        print('Logged in as "{0}".'.format(self.user))

    async def message_handler(self, message_context: discord.Message) -> None:
        if message_context.author != self.user:
            await self.maintainance.handle_maintainance(message_context)

            if message_context.content.startswith('$'):
                await self.commands.handle_bot_command(message_context)

    async def on_member_join(self, member: discord.Member) -> None:
        await member.add_roles(discord.utils.get(member.guild.roles, id = self.database.default_role_id))
        await member.send('Welcome to the guild of the lads! Type **$help** in any chat where I am present and I will show you all the things I can do.')

    async def on_message(self, message_context: discord.Message) -> None:
        await self.message_handler(message_context)

    async def on_message_edit(self, before_message_context: discord.Message, after_message_context: discord.Message) -> None:
        await self.message_handler(after_message_context)

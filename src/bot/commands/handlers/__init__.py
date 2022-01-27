import os
import discord
import random
from typing import Tuple

from bot.database import BotDatabase, DuplicateKeyError
from bot.apis import BotAPIs
from bot.utils import BotUtils
from bot.messages import BotMessages

from bot.commands.handlers.fun import BotFunCommandHandlers
from bot.commands.handlers.moderator import BotModeratorCommandHandlers
from bot.commands.handlers.administrator import BotAdministratorCommandHandlers
from bot.commands.handlers.audio import BotAudioCommandHandlers

class BotCommandHandlers:
    bot: discord.Client
    utils: BotUtils
    database: BotDatabase
    apis: BotAPIs

    fun: BotFunCommandHandlers
    moderator: BotModeratorCommandHandlers
    administrator: BotAdministratorCommandHandlers
    audio: BotAudioCommandHandlers

    def __init__(self, bot: discord.Client, utils: BotUtils, database: BotDatabase, apis: BotAPIs):
        self.bot = bot
        self.utils = utils
        self.database = database
        self.apis = apis

        self.fun = BotFunCommandHandlers(utils, database, apis)
        self.moderator = BotModeratorCommandHandlers(utils, database)
        self.administrator = BotAdministratorCommandHandlers(utils, database)
        self.audio = BotAudioCommandHandlers(bot)

    async def help(self, message_context: discord.Message, params: str, **kwargs) -> None:
        embed = discord.Embed(title = 'Help')
        permission = kwargs.get('permission', self.utils.permissions.permissions.get('MUTED'))

        if hasattr(message_context.author, 'guild_permissions'):
            embed.title += f' ({message_context.guild.name})'

            if self.utils.permissions.is_muted(permission):
                embed.description = 'You are muted on this server.'

            else:
                if self.utils.permissions.is_general(permission):
                    embed.add_field(name = '__General__', value = BotMessages.help['GENERAL_HELP_MESSAGE'](kwargs.get('prefix')), inline = False)
                    embed.add_field(name = '__Audio__', value = BotMessages.help['AUDIO_HELP_MESSAGE'](kwargs.get('prefix')), inline = False)

                if self.utils.permissions.is_moderator(permission):
                    embed.add_field(name = '__Moderator__', value = BotMessages.help['MODERATOR_HELP_MESSAGE'](kwargs.get('prefix')), inline = False)

                if self.utils.permissions.is_administrator(permission):
                    embed.add_field(name = '__Administrator__', value = BotMessages.help['ADMINISTRATOR_HELP_MESSAGE'](kwargs.get('prefix')), inline = False)

        else:
            embed.add_field(name = '__General__', value = BotMessages.help['GENERAL_HELP_MESSAGE'](kwargs.get('prefix')), inline = False)

        await message_context.author.send(embed = embed)
        await self.utils.messages.delete_message(message_context)

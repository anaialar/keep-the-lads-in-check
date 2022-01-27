from typing import Callable, Dict, Coroutine

import discord

from bot.messages import BotMessages
from bot.commands.handlers import BotCommandHandlers
from bot.utils import BotUtils
from bot.database import BotDatabase
from bot.apis import BotAPIs

class BotCommand(Callable[[discord.Message, str], Coroutine]):
    permission_checker: Callable[[int], bool]
    guild_only: bool
    handler: Callable[[discord.Message, str], Coroutine]
    utils: BotUtils

    def __init__(self, utils: BotUtils, permission_checker: Callable[[int], bool], guild_only: bool, handler: Callable[[discord.Message, str, int], None]):
        self.permission_checker = permission_checker
        self.guild_only = guild_only
        self.handler = handler
        self.utils = utils

    async def __call__(self, message_context: discord.Message, params: str) -> None:
        if hasattr(message_context.author, 'guild_permissions'):
            permission = self.utils.permissions.permissions.get('MUTED')

            if message_context.author.guild_permissions.administrator:
                permission = self.utils.permissions.permissions.get('ADMINISTRATOR')

            else:
                for role in message_context.author.roles:
                    role_permission = self.utils.permissions.get_role_permission(role.id)

                    if self.utils.permissions.is_muted(role_permission):
                        permission = self.utils.permissions.permissions.get('MUTED')
                        break

                    elif role_permission < permission:
                        permission = role_permission

            if self.permission_checker(permission):
                await self.handler(message_context, params, permission = permission, prefix = '$')

            else:
                await message_context.reply(BotMessages.command_exceptions['UNAUTHORIZED'])

        elif self.guild_only:
            await message_context.reply(BotMessages.command_exceptions['GUILD_ONLY'])

        else:
            await self.handler(message_context, params)

class BotCommands:
    utils: BotUtils
    handlers: BotCommandHandlers
    commands: Dict[str, BotCommand]
    commands: Dict[str, str]

    def __init__(self, bot: discord.Client, utils: BotUtils, database: BotDatabase, apis: BotAPIs):
        self.handlers = BotCommandHandlers(bot, utils, database, apis)
        self.utils = utils
        self.commands = {
            'help': self.create_command(utils.permissions.is_general, False, self.handlers.help),
            'meme_random': self.create_command(utils.permissions.is_general, False, self.handlers.fun.meme_random),
            'joke_random': self.create_command(utils.permissions.is_general, False, self.handlers.fun.joke_random),
            'sticker': self.create_command(utils.permissions.is_general, False, self.handlers.fun.sticker),
            'weather': self.create_command(utils.permissions.is_general, False, self.handlers.fun.weather),
            'choose_random_member': self.create_command(utils.permissions.is_general, True, self.handlers.fun.choose_random_member),
            'choose_random_online_member': self.create_command(utils.permissions.is_general, True, self.handlers.fun.choose_random_online_member),
            'audio_play': self.create_command(utils.permissions.is_dj, True, self.handlers.audio.audio_play),
            'audio_stop': self.create_command(utils.permissions.is_dj, True, self.handlers.audio.audio_stop),
            'delete': self.create_command(utils.permissions.is_moderator, True, self.handlers.moderator.delete),
            'get_censored_channels': self.create_command(utils.permissions.is_moderator, True, self.handlers.moderator.get_censored_channels),
            'add_censored_channel': self.create_command(utils.permissions.is_moderator, True, self.handlers.moderator.add_censored_channel),
            'remove_censored_channel': self.create_command(utils.permissions.is_moderator, True, self.handlers.moderator.remove_censored_channel),
            'say': self.create_command(utils.permissions.is_administrator, True, self.handlers.administrator.say),
            'change_default_role': self.create_command(utils.permissions.is_administrator, True, self.handlers.administrator.change_default_role),
            'set_role_permission': self.create_command(utils.permissions.is_administrator, True, self.handlers.administrator.set_role_permission),
            'remove_role_permission': self.create_command(utils.permissions.is_administrator, True, self.handlers.administrator.remove_role_permission),
            'get_all_role_permissions': self.create_command(utils.permissions.is_administrator, True, self.handlers.administrator.get_all_role_permissions)
        }

        self.short_cuts = {
            'mr': 'meme_random',
            'jr': 'joke_random',
            'crm': 'choose_random_member',
            'crom': 'choose_random_online_member',
            'ap': 'audio_play',
            'as': 'audio_stop',
            'gcc': 'get_censored_channels',
            'acc': 'add_censored_channel',
            'rcc': 'remove_censored_channel',
            'cdr': 'change_default_role',
            'srp': 'set_role_permission',
            'rrp': 'remove_role_permission',
            'garp': 'get_all_role_permissions'
        }

    def create_command(self, permission_checker: Callable[[int], bool], guild_only: bool, handler: Callable[[discord.Message, str], None]) -> BotCommand:
        return BotCommand(self.utils, permission_checker, guild_only, handler)

    async def handle_bot_command(self, message_context: discord.Message) -> None:
        message_splitted = message_context.content.strip().split(' ', 1)
        command_name = str(message_splitted[0]).lower()

        if command_name.startswith('$'):
            command_name = command_name[1:]
            command_handler = self.commands.get(self.short_cuts.get(command_name, command_name))

            if command_handler == None:
                await message_context.reply(BotMessages.command_exceptions['UNKNOWN_COMMAND'], mention_author = True)

            else:
                params = None
                if len(message_splitted) > 1:
                    params = message_splitted[1]

                try:
                    await command_handler(message_context, params)

                except Exception as error:
                    print('Command execution error: {0}'.format(error))
                    await message_context.reply(BotMessages.command_exceptions['UNHANDLED'], mention_author = True)

import discord
from bot.database import BotDatabase
from bot.utils import BotUtils
from bot.messages import BotMessages

class BotAdministratorCommandHandlers:
    utils: BotUtils
    database: BotDatabase

    def __init__(self, utils: BotUtils, database: BotDatabase):
        self.utils = utils
        self.database = database

    async def say(self, message_context: discord.Message, params: str, **kwargs) -> None:
        if params == None:
            await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

        else:
            text = params
            await self.utils.messages.replace_message(message_context, text)

    async def change_default_role(self, message_context: discord.Message, params: str, **kwargs) -> None:
        if params == None:
            await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

        else:
            params = params.lstrip()
            if params.startswith('<@&'):
                params = params[3:]
                end_index = -1

                for i in range(len(params)):
                    if not params[i].isnumeric():
                        if params[i] == '>':
                            end_index = i

                        break

                if end_index > 0:
                    try:
                        role_id = int(params[:end_index])
                        if discord.utils.get(message_context.guild.roles, id = role_id) == None:
                            await message_context.reply(BotMessages.command_exceptions['ROLE_NOT_FOUND'], mention_author = True)

                        else:
                            self.database.default_role_id = role_id

                    except AttributeError:
                        await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

                    except Exception as error:
                        raise error

                else:
                    await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

            else:
                await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)


    async def set_role_permission(self, message_context: discord.Message, params: str, **kwargs) -> None:
        if params == None:
            await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

        else:
            params = params.lstrip()
            if params.startswith('<@&'):
                params = params[3:]
                end_index = -1

                for i in range(len(params)):
                    if not params[i].isnumeric():
                        if params[i] == '>':
                            end_index = i

                        break

                if end_index > 0:
                    try:
                        role_id = int(params[:end_index])
                        if discord.utils.get(message_context.guild.roles, id = role_id) == None:
                            await message_context.reply(BotMessages.command_exceptions['ROLE_NOT_FOUND'], mention_author = True)

                        else:
                            permission_name = params[(end_index + 1):].strip()
                            permission = self.utils.permissions.permissions.get(permission_name.upper())
                            if permission == None:
                                await message_context.reply(BotMessages.command_exceptions['PERMISSION_NOT_FOUND'], mention_author = True)

                            else:
                                await self.utils.permissions.set_role_permission(role_id, permission)
                                await self.utils.messages.delete_message(message_context)

                    except AttributeError:
                        await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

                    except Exception as error:
                        raise error

                else:
                    await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

            else:
                await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

    async def remove_role_permission(self, message_context: discord.Message, params: str, **kwargs) -> None:
        if params == None:
            await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

        else:
            params = params.lstrip()
            if params.startswith('<@&'):
                params = params[3:]
                end_index = -1

                for i in range(len(params)):
                    if not params[i].isnumeric():
                        if params[i] == '>':
                            end_index = i

                        break

                if end_index > 0:
                    try:
                        role_id = int(params[:end_index])
                        if discord.utils.get(message_context.guild.roles, id = role_id) == None:
                            await message_context.reply(BotMessages.command_exceptions['ROLE_NOT_FOUND'], mention_author = True)

                        else:
                            if await self.utils.permissions.remove_role_permission(role_id):
                                await self.utils.messages.delete_message(message_context)

                            else:
                                await message_context.reply(BotMessages.command_exceptions['ADMINISTRATOR']['ROLE_PERMISSION_NOT_FOUND'](role_id), mention_author = True)

                    except AttributeError:
                        await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

                    except Exception as error:
                        raise error

                else:
                    await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

            else:
                    await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

    async def get_all_role_permissions(self, message_context: discord.Message, params: str, **kwargs) -> None:
        message_content = ''
        for (role_name, permission_name) in await self.utils.permissions.get_all_role_permissions(message_context.guild):
            message_content += f'**@{role_name}** - {permission_name}\n'

        embed = discord.Embed(name = "Permissions", description = message_content)
        await message_context.author.send(embed = embed)
        await self.utils.messages.delete_message(message_context)

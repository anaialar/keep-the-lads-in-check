import discord
from bot.database import BotDatabase
from bot.utils import BotUtils
from bot.messages import BotMessages

class BotModeratorCommandHandlers:
    utils: BotUtils
    database: BotDatabase
    messages: BotMessages

    def __init__(self, utils: BotUtils, database: BotDatabase):
        self.utils = utils
        self.database = database

    async def delete(self, message_context: discord.Message, params: str, **kwargs) -> None:
        if params == None:
            await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

        else:
            try:
                number = int(params) + 1

                if self.utils.permissions.is_administrator(kwargs.get('permission')):
                    await message_context.channel.purge(limit = number)

                elif number <= 16:
                    await message_context.channel.purge(limit = number)

                else:
                    await message_context.reply(BotMessages.command_exceptions['MODERATOR']['DELETE_MAXIMUM_15'], mention_author = True)

            except AttributeError:
                await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

            except Exception as error:
                raise error

    async def get_censored_channels(self, message_context: discord.Message, params: str, **kwargs) -> None:
        embed = discord.Embed(title = f'Currently censored channels ({message_context.guild.name})')
        description = ''
        async for channel in self.database.censored_channels.get_censored_channels():
            description += '#{0}'.format(discord.utils.get(message_context.guild.channels, id = channel.get('channelId')).name)

        if description == '':
            embed.description = 'None'

        else:
            embed.description = description

        await message_context.author.send(embed = embed)
        await self.utils.messages.delete_message(message_context)

    async def remove_censored_channel(self, message_context: discord.Message, params: str, **kwargs) -> None:
        if params == None:
            await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

        else:
            if params.startswith('<#'):
                params = params[2:]
                end_index = -1

                for i in range(len(params)):
                    if params[i] == '>':
                        end_index = i
                        break

                if end_index > 0:
                    try:
                        channel_id = int(params[:end_index])
                        if discord.utils.get(message_context.guild.channels, id = channel_id) == None:
                            await message_context.reply(BotMessages.command_exceptions['CHANNEL_NOT_FOUND'], mention_author = True)

                        else:
                            if await self.database.censored_channels.remove_censored_channel(channel_id):
                                await self.utils.messages.delete_message(message_context)

                            else:
                                await message_context.reply(BotMessages.command_exceptions['MODERATOR']['ALREADY_NOT_CENSORED'], mention_author = True)

                    except AttributeError:
                        await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

                    except Exception as error:
                        raise error

                else:
                    await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

            else:
                await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

    async def add_censored_channel(self, message_context: discord.Message, params: str, **kwargs) -> None:
        if params == None:
            await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

        else:
            params = params.strip()

            if params.startswith('<#'):
                params = params[2:]
                end_index = -1

                for i in range(len(params)):
                    if params[i] == '>':
                        end_index = i
                        break

                if end_index > 0:
                    try:
                        channel_id = int(params[:end_index])
                        if discord.utils.get(message_context.guild.channels, id = channel_id) == None:
                            await message_context.reply(BotMessages.command_exceptions['CHANNEL_NOT_FOUND'], mention_author = True)

                        else:
                            try:
                                await self.database.censored_channels.add_censored_channel(channel_id)
                                await message_context.delete()

                            except DuplicateKeyError:
                                await message_context.reply(BotMessages.command_exceptions['MODERATOR']['ALREADY_CENSORED'], mention_author = True)

                            except Exception as error:
                                raise error

                    except AttributeError:
                        await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

                    except Exception as error:
                        raise error

                else:
                    await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

            else:
                await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

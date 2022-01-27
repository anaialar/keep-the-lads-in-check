import random

import discord

from bot.apis import BotAPIs
from bot.database import BotDatabase
from bot.utils import BotUtils
from bot.messages import BotMessages

class BotFunCommandHandlers:
    utils: BotUtils
    database: BotDatabase
    apis: BotAPIs

    def __init__(self, utils: BotUtils, database: BotDatabase, apis: BotAPIs):
        self.utils = utils
        self.database = database
        self.apis = apis

    async def meme_random(self, message_context: discord.Message, params: str, **kwargs) -> None:
        (title, url) = await self.apis.get_random_meme()
        embed = discord.Embed()
        embed.set_image(url = url)
        await self.utils.messages.replace_message(message_context, title, embed = embed)

    async def joke_random(self, message_context: discord.Message, params: str, **kwargs) -> None:
        result = await self.apis.get_random_joke()

        result_handlers = {
            BotAPIs.NOT_FOUND: lambda: message_context.reply(BotMessages.command_exceptions['FUN']['JOKE_NOT_FOUND'], mention_author = True)
        }

        result_handler = result_handlers.get(result)

        if result_handler == None:
            await self.utils.messages.replace_message(message_context, result)

        else:
            await result_handler()

    async def choose_random_member(self, message_context: discord.Message, params: str, **kwargs) -> None:
        channel_members_length = len(message_context.channel.members)

        while True:
            member = message_context.channel.members[random.randrange(0, channel_members_length)]
            if not member.bot:
                await self.utils.messages.replace_message(message_context, BotMessages.command_responses['FUN']['CHOOSE_MEMBER'](member.mention))
                break

    async def choose_random_online_member(self, message_context: discord.Message, params: str, **kwargs) -> None:
        channel_members_length = len(message_context.channel.members)

        while True:
            member = message_context.channel.members[random.randrange(0, channel_members_length)]
            if not member.bot and member.status is discord.Status.online:
                await self.utils.messages.replace_message(message_context, BotMessages.command_responses['FUN']['CHOOSE_MEMBER'](member.mention))
                break

    async def sticker(self, message_context: discord.Message, params: str, **kwargs) -> None:
        tag = params

        if tag == None:
            await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

        else:
            tag = tag.lower().strip()

            cached_sticker = await self.database.stickers_cache.find_sticker_url(tag)

            url = None

            if cached_sticker == None:
                result = await self.apis.get_sticker_from_tag(tag)

                result_handlers = {
                    BotAPIs.NOT_FOUND: lambda: message_context.reply(BotMessages.command_exceptions['FUN']['STICKER_NOT_FOUND'], mention_author = True),
                    BotAPIs.RATE_LIMITED: lambda: message_context.reply(BotMessages.command_exceptions['FUN']['STICKER_RATE_LIMITED'], mention_author = True)
                }

                if isinstance(result, int):
                    await result_handlers.get(result)()

                else:
                    url = result
                    await self.database.stickers_cache.add_sticker(tag, url)

            else:
                url = cached_sticker

            embed = discord.Embed()
            embed.set_image(url = url)
            await self.utils.messages.replace_message(message_context, params, embed = embed)

    async def weather(self, message_context: discord.Message, params: str, **kwargs) -> None:
        if params == None:
            await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

        else:
            city = params.strip()
            result = await self.apis.get_weather(city)

            result_handlers = {
                BotAPIs.NOT_FOUND: lambda: message_context.reply(BotMessages.command_exceptions['FUN']['CITY_NOT_FOUND'], mention_author = True)
            }

            if isinstance(result, int):
                await result_handlers.get(result)()

            else:
                embed = discord.Embed(title = result.get('city'), description = BotMessages.command_responses['FUN']['WEATHER_RESPONSE'](result))
                embed.set_image(url = result.get('icon_url'))
                await self.utils.messages.replace_message(message_context, '', add_dash = False, embed = embed)


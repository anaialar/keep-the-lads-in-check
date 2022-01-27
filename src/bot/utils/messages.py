import discord

class BotMessageUtils:
    async def delete_message(self, message_context: discord.Message) -> None:
        if hasattr(message_context.author, 'guild_permissions'):
            await message_context.delete()

    async def replace_message(self, message_context: discord.Message, message: str, add_dash = True, **kwargs) -> None:
        seperator = ''
        if add_dash:
            seperator = ' - '
        await message_context.channel.send(f'{message_context.author.mention}{seperator}{message}', reference = message_context.reference, **kwargs)
        await self.delete_message(message_context)

import discord
import re
import threading
import time
import asyncio
from youtube_dl import YoutubeDL
from bot.messages import BotMessages

class BotAudioCommandHandlers:
    bot: discord.Client

    audio_voice_client: discord.VoiceProtocol

    def __init__(self, bot: discord.Client):
        self.bot = bot

        self.audio_voice_client = None

    async def stop_audio(self) -> None:
        try:
            self.audio_voice_client.stop()
            await self.audio_voice_client.disconnect(force = True)
            self.audio_voice_client = None

        except:
            pass

    async def audio_play(self, message_context: discord.Message, params: str, **kwargs) -> None:
        if params == None:
            await message_context.reply(BotMessages.command_exception['UNKNOWN_SYNTAX'], mention_author = True)

        else:
            params = params.strip()

            if params[0] == '[':
                params = params[1:]
                if self.audio_voice_client == None:
                    voice_channel_name = None
                    title_start_index = -1
                    for i in range(len(params)):
                        if params[i] == ']':
                            title_start_index = i
                            break

                    if title_start_index < 0:
                        await message_context.reply(BotMessages.command_exceptions['AUDIO']['CHANNEL_NAME_REQUIRED'], mention_author = True)

                    elif len(params) <= (title_start_index + 1):
                        await message_context.reply(BotMessages.command_exceptions['AUDIO']['QUERY_OR_URL'], mention_author = True)

                    else:
                        voice_channel_name = params[:title_start_index].strip()

                        youtube_video_search_query = params[(title_start_index + 1):].strip()

                        youtube_dl_options = {
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '32'
                            }]
                        }

                        ffmpeg_options = {
                            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                            'options': '-vn'
                        }

                        voice_channel = None
                        max_matched = 0
                        for _voice_channel in message_context.guild.voice_channels:
                            result = re.search(voice_channel_name.lower(), _voice_channel.name.lower())
                            if result != None:
                                (start, end) = result.span()
                                length = end - start
                                if max_matched < length:
                                    voice_channel = _voice_channel
                                    max_matched = length

                        voice_client = discord.utils.get(self.bot.voice_clients, guild = message_context.guild)

                        if voice_channel == None:
                            await message_context.reply(BotMessages.command_exceptions['VOICE_CHANNEL_NOT_FOUND'], mention_author = True)

                        else:
                            if voice_client == None:
                                voice_client = await voice_channel.connect()

                            else:
                                await voice_client.move_to(voice_channel)

                            video_info = None

                            with YoutubeDL(youtube_dl_options) as ydl:
                                if youtube_video_search_query.startswith('http'):
                                    video_info = ydl.extract_info(youtube_video_search_query, download = False)
                                else:
                                    videos_list = ydl.extract_info(f'ytsearch:{youtube_video_search_query}', download = False)['entries']
                                    if len(videos_list) > 0:
                                        video_info = videos_list[0]

                                    else:
                                        await message_context.reply(BotMessages.command_exceptions['AUDIO']['VIDEO_NOT_FOUND'], mention_author = True)
                                        return

                            def check_youtube_audio_play_timeout(voice_channel) -> None:
                                if self.audio_voice_client != None:
                                    time.sleep(20)
                                    if len(voice_channel.members) > 1:
                                        return check_youtube_audio_play_timeout(voice_channel)

                                    else:
                                        asyncio.run_coroutine_threadsafe(self.stop_audio(), self.bot.loop).result()

                            timeout_on_no_members_thread = threading.Thread(target = check_youtube_audio_play_timeout, args = (voice_channel, ))

                            def after_audio_stopped(error) -> None:
                                if error == None:
                                    asyncio.run_coroutine_threadsafe(self.stop_audio(), self.bot.loop).result()
                                    timeout_on_no_members_thread.join()

                                else:
                                    print(error)

                                self.audio_voice_client = None

                            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(video_info["formats"][0]["url"], **ffmpeg_options), volume = 1.0)
                            await message_context.delete()

                            self.audio_voice_client = voice_client
                            voice_client.play(source, after = after_audio_stopped)
                            timeout_on_no_members_thread.start()

                else:
                    await message_context.reply(BotMessages.command_exceptions['AUDIO']['ALREADY_PLAYING'], mention_author = True)

            else:
                await message_context.reply(BotMessages.command_exceptions['UNKNOWN_SYNTAX'], mention_author = True)

    async def audio_stop(self, message_context: discord.Message, params: str, **kwargs) -> None:
        if self.audio_voice_client != None:
            await self.stop_audio()
            await message_context.delete()

        else:
            await message_context.reply(BotMessages.command_exceptions['AUDIO']['ALREADY_STOPPED'], mention_author = True)

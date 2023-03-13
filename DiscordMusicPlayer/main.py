import discord
from discord import app_commands
import asyncio
import json
import youtube_dl

config = json.load(open('config.json'))
intents = discord.Intents.all()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = ''

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        return data['title'] if stream else ytdl.prepare_filename(data)


# @tree.command(name = 'join', description = 'Joins the channel')
# async def join(ctx:discord.Interaction):
#     if not ctx.user.voice:
#         # await ctx.send('You are not connected to a voice channel')
#         return
#     else:
#         channel = ctx.user.voice.channel
#     await channel.connect()
#
# @tree.command(name = 'leave', description = 'Leaves the channel')
# async def leave(ctx:discord.Interaction):
#     voice_client = ctx.message.guild.voice_client
#     await voice_client.disconnect()
#
#
# @tree.command(name = 'play', description = 'Plays a song')
# @discord.app_commands.describe(url='The url of the song')
# async def play(ctx, *, url: str):
#     try:
#         server = ctx.message.guild
#         voice_channel = server.voice_client
#         async with ctx.typing():
#             filename = await YTDLSource.from_url(url, loop=bot.loop)
#             voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
#         await ctx.send(f'**Now playing:** {filename}')
#     except Exception as e:
#         await ctx.send(f'Something went wrong. Error: {e}')
#
# @tree.command(name = 'pause', description = 'Pauses the song')
# async def pause(ctx: discord.Interaction):
#     voice_client = ctx.message.guild.voice_client
#     if voice_client.is_playing():
#         voice_client.pause()
#     else:
#         await ctx.send('Currently no audio is playing')
#
# @tree.command(name = 'resume', description = 'Resumes the song')
# async def resume(ctx: discord.Interaction):
#     voice_client = ctx.message.guild.voice_client
#     if voice_client.is_paused():
#         voice_client.resume()
#     else:
#         await ctx.send('The audio is not paused')
#
# @tree.command(name = 'stop', description = 'Stops the song')
# async def stop(ctx: discord.Interaction):
#     voice_client = ctx.message.guild.voice_client
#     voice_client.stop()
#
# @bot.event
# async def on_ready():
#     await tree.sync()
#     print('Bot is ready')


@tree.command(name='pingle', description='Pings the bot')
async def ping(ctx: discord.Interaction):
    await bot.ping()

bot.run(config['token'])

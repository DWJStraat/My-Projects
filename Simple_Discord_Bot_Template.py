import disnake
from disnake.ext import commands
import json

command_sync_flags = commands.CommandSyncFlags.default()

config = json.load(open("config.json"))


bot = commands.Bot(
    command_prefix = config["prefix"],
    intents = disnake.Intents.all()
)

@bot.slash_command(description= "A simple ping command")
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(config["token"])
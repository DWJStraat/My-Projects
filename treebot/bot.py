import contextlib
import disnake
from disnake.ext import commands
import json
import os
from javascript import require
import time


command_sync_flags = commands.CommandSyncFlags.default()

config = json.load(open("config.json"))

bot = commands.Bot(
    command_prefix=config["prefix"],
    intents=disnake.Intents.all()
)


@bot.slash_command(description="A simple ping command")
async def ping(ctx):
    await ctx.send("Pong!")

@bot.slash_command(description="Ponder the Orb")
async def ponder(ctx):
    with contextlib.suppress(Exception):
        os.remove("images/dashboard.png")
    screenshot = require("./screenshot.js")
    await ctx.send("Pondering the Orb...")
    patience = 15
    while patience > 0:
        try:
            await ctx.send("You ponder the Orb...",file=disnake.File("images/dashboard.png"))
            patience = 0
        except Exception:
            time.sleep(1)
            patience -= 1
    os.remove("images/dashboard.png")

bot.run(config["token"])

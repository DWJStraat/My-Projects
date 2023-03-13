import disnake as discord
from disnake.ext import commands
import asyncio
import json
from main_class import *
import pickle
import random

settings = json.load(open('settings.json'))
discord_settings = settings["discord"]
intents = discord.Intents.all()
prefix = discord_settings["prefix"]

bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.command()
async def add_name(ctx, name=None):
    if name is None:
        await ctx.send("Please enter a name")
        return
    settings["name_list"].append(name)
    json.dump(settings, open('settings.json', 'w'))
    await ctx.send(f"Added {name} to the list")


@bot.command()
async def remove_name(ctx, name=None):
    if name is None:
        await ctx.send("Please enter a name")
        return
    settings["name_list"].remove(name)
    json.dump(settings, open('settings.json', 'w'))
    await ctx.send(f"Removed {name} from the list")


@bot.command()
async def list_names(ctx):
    await ctx.send(settings["name_list"])


@bot.command()
async def add_game(ctx, game_name, characters):
    character_list = []
    full_list = settings["name_list"]
    for _ in characters:
        try:
            char = random.choice(full_list)
            full_list.remove(char)
            character_list.append(char)
        except:
            await ctx.send("Not enough names")
            return
    game = Game(game_name)
    game.build_characters(character_list)
    game.save()


@bot.command()
async def new_day(ctx, game_name):
    game = Game(game_name)
    game.load()
    game.new_day()


bot.run(discord_settings["key"])

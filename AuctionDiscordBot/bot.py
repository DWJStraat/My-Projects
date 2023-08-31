import disnake
from disnake.ext import commands
import json
from auction_object import Auction
import pickle

command_sync_flags = commands.CommandSyncFlags.default()

config = json.load(open("config.json"))

bot = commands.Bot(
    command_prefix=config["prefix"],
    intents=disnake.Intents.all()
)

@bot.event
async def on_ready():
    print("Bot is ready!")
    try:
        pickle.load(open("auction.pickle", "rb"))
    except FileNotFoundError:
        auction = Auction()
        pickle.dump(auction, open("auction.pickle", "wb"))


@bot.slash_command(description="A simple ping command")
async def ping(ctx):
    await ctx.send("Pong!")


@bot.slash_command(description="Start the auction")
async def start(ctx, item_name: str, item_description: str, item_price: int):
    auction = pickle.load(open("auction.pickle", "rb"))
    auction.start(item_name, item_description, item_price)
    pickle.dump(auction, open("auction.pickle", "wb"))
    await ctx.send("The auction has started!")
    for participant in config["participants"]:
        user = await bot.fetch_user(participant)
        await user.send(f"The auction has started! The item is {item_name} and the description is {item_description}. "
                        f"The starting price is {item_price}.")


@bot.slash_command(description="Participate in the auction")
async def participate(ctx):
    auction = pickle.load(open("auction.pickle", "rb"))
    auction.participate(ctx.author.id)
    pickle.dump(auction, open("auction.pickle", "wb"))
    await ctx.send("You have participated in the auction!")

@bot.slash_command(description="Leave the auction")
async def leave(ctx):
    auction = pickle.load(open("auction.pickle", "rb"))
    auction.leave(ctx.author.id)
    pickle.dump(auction, open("auction.pickle", "wb"))
    config["participants"].remove(ctx.author.id)
    with open("config.json", "w") as f:
        json.dump(config, f)
    await ctx.send("You have left the auction!")


@bot.slash_command(description="Bid in the auction")
async def bid(ctx, bid: int):
    auction = pickle.load(open("auction.pickle", "rb"))
    bid_success = auction.bid_func(ctx.author.id, bid)
    pickle.dump(auction, open("auction.pickle", "wb"))
    if bid_success:
        await ctx.send(f"You have bid {bid}!")
        for participant in config["participants"]:
            if participant != ctx.author.id:
                user = await bot.fetch_user(participant)
                await user.send(f"{ctx.author.name} has bid {bid}!")
    else:
        await ctx.send(f"Your bid of {bid} was not high enough!")


@bot.slash_command(description="End the auction")
async def end(ctx):
    auction = pickle.load(open("auction.pickle", "rb"))
    name,price = auction.end()
    pickle.dump(auction, open("auction.pickle", "wb"))
    if name is not None:
        winner = await bot.fetch_user(name)
        await ctx.send(f"The winner is {winner} with a bid of {price}!")
        await winner.send(f"You have won the auction with a bid of {price}!")
    else:
        await ctx.send("The auction has ended with no winner!")
        for participant in config["participants"]:
            user = await bot.fetch_user(participant)
            await user.send("The auction has ended with no winner!")
    with open("config.json", "w") as f:
        json.dump(config, f)

@bot.slash_command(description="View the current auction")
async def view(ctx):
    auction = pickle.load(open("auction.pickle", "rb"))
    name, desc, bid, winner = auction.view()
    winner = await bot.fetch_user(winner)
    pickle.dump(auction, open("auction.pickle", "wb"))
    if name is not None:
        await ctx.send(f"The item is {name} and the description is {desc}. "
                       f"The current price is {bid}, bid by {winner}.")
    else:
        await ctx.send("There is no ongoing auction!")

bot.run(config["token"])

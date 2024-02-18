from discord.ext import commands 
from dotenv import load_dotenv
import discord, os, random

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='cook ', intents=intents)

@bot.event
async def on_ready(): 
    print(f'{bot.user.name} has started cooking!')

@bot.command()
async def luckynumber(ctx):
    response = f"Your lucky number today is: {random.randint(1, 100)}" 
    await ctx.send(response)

@bot.command()
async def cmds(ctx):
    response = """You can use the following commands:
`cook luckynumber`: generate a lucky number for today!
`cook cmds`: list all commands the bot currently supports. 
"""
    await ctx.send(response)

load_dotenv()
bot.run(os.getenv('TOKEN'))
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
disc_token = os.getenv("env_BotTOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = '!',intents=intents)

@client.event
async def on_ready():
    print("The bot is now ready")
    print("--------------------")



@client.command()
async def hello(ctx):
    await ctx.send("Hello, this is the bot")


client.run(f'{disc_token}')


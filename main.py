import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
import os

load_dotenv()
disc_token = os.getenv("env_BotTOKEN")

intents = discord.Intents.all()

client = commands.Bot(command_prefix = '!',intents=intents)

@client.event
async def on_ready():
    print("The bot is now ready")
    print("--------------------")


@client.command()
async def hello(ctx):
    user = ctx.author
    await ctx.send(f"Hello {user}, this is the bot")


@client.event
async def on_member_join(member):
    channel = client.get_channel(1095340792547119126)
    await channel.send(f"Hello {member.display_name}")
    

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1095340792547119126)
    await channel.send(f"Goodbye {member.display_name}")


@client.command(pass_context = True)
async def vcjoin(ctx):
    if (ctx.author.voice):
        await ctx.send("Joining the voice channel!")
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('Film.mp3')
        player = voice.play(source)

    else:
        await ctx.send("You must be in a voice channel to run this command")


@client.command(pass_context = True)
async def vcleave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I have left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")


client.run(f'{disc_token}')


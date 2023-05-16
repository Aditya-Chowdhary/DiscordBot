import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
import os

load_dotenv()
disc_token = os.getenv("env_BotTOKEN")

intents = discord.Intents.all()

queues = {}

def check_queue(ctx, id):
    if queues[id]:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

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

    else:
        await ctx.send("You must be in a voice channel to run this command")


@client.command(pass_context = True)
async def vcleave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I have left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")

@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Audio has been paused")
    else:
        await ctx.send("I am not playing anything!")


@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Audio has been resumed")
    else:
        await ctx.send("No audio has been paused!")


@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    voice.stop()


@client.command(pass_context = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.mp3'
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.guild.id))

@client.command(pass_context = True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.mp3'
    source = FFmpegPCMAudio(song)

    guild_id = ctx.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]

    await ctx.send(f"{song} has been added to queue.")

@client.event
async def on_message(message):
    print(message)


client.run(f'{disc_token}')


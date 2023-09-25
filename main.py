import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import os
from better_profanity import profanity

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

# Gabra Gay
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
    await client.process_commands(message)
    # print(message)
    if message.author.name == "JeffTheBot":
        return
    if profanity.contains_profanity(message.content):
        await message.delete()
        await message.channel.send("Please do not send a message with profanity!")

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"User {member} has been kicked")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to kick people!")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"User {member} has been banned")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to ban people!")

@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Dog", url="https://google.com", description="We love dogs", color=0x4dff4d)
    embed.set_author(name=ctx.author, url= "https://google.com", icon_url="https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg")
    await ctx.send(embed=embed)
 
client.run(f'{disc_token}')

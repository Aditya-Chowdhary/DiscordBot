import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
import os
import openai
from pytube import YouTube
from datetime import datetime
import asyncio


load_dotenv()
disc_token = os.getenv("env_BotTOKEN")
openai.api_key = os.getenv("env_OpenAI")

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '!',intents=intents)


@client.event
async def on_ready():
    print("The bot is now ready")
    print("--------------------")


@client.command()
async def hello(ctx):
    user = ctx.author.nick
    await ctx.send(f"Hello {user}, this is the bot")


@client.event
async def on_member_join(member):
    channel = client.get_channel(1095340792547119126)
    await channel.send(f"Hello {member.display_name}")
    

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1095340792547119126)
    await channel.send(f"Goodbye {member.display_name}")


def get_api_response(prompt):
    text = None

    try: 
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt = prompt,
            temperature=0.9,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop = [' Human:', ' AI:']
        )

        choices = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print('ERROR: ', e)

    return text

@client.command(pass_request = True)
async def gpt(ctx, *, arg):
    user_prompt = arg
    api_answer = get_api_response(user_prompt)
    pos = api_answer.find("\n")
    api_answer = api_answer[pos + 1:]
    await ctx.send(f"GPT Response is: {api_answer}")


@client.command(pass_context = True)
async def vcjoin(ctx):
    if (ctx.author.voice):
        await ctx.send("Joining the voice channel!")
        channel = ctx.message.author.voice.channel
        await channel.connect()

    else:
        await ctx.send("You must be in a voice channel to run this command")
        return
    

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

    link = arg
    yt = YouTube(link)
    downloader = yt.streams.filter(only_audio=True).get_audio_only()
    downloader.download()
    title = yt.title
    for i in "\\/:*?\"<>|":
        title = title.replace(i, '')
    title = title+'.mp4'


    source = FFmpegPCMAudio(title)
    voice.play(source)


@client.command(pass_context = True)
async def reminder(ctx, time_str, date_str, *args):
    try:
        if args:
            remind_msg = f" - \"{' '.join(args)}\""
        else:
            remind_msg = ''

        time =datetime.strptime(time_str, "%H:%M")
        date =datetime.strptime(date_str, "%d/%m/%Y")

        now = datetime.now()
        delay = (datetime.combine(date, time.time())-now).total_seconds()
        if delay<0:
            await ctx.send("ERROR: Cannot set a reminder for the past")
        else:
            await ctx.send("Reminder has been set successfully{remind_msg}")
            await asyncio.sleep(delay)
            await ctx.send(f"{ctx.author.mention}, you have a reminder{remind_msg}!")

    except ValueError:
        await ctx.send("ERROR: Please enter reminder in the correct format: HH:MM[24 hr format] dd/mm/yyyy")



client.run(f'{disc_token}')


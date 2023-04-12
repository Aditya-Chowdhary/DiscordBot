import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import openai

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


def get_api_response(prompt):
    text = None

    try: 
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt = prompt,
            temperature=0.9,
            max_tokens=150,
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
async def gpt(ctx, *args):
    user_prompt = ' '.join(args)
    api_answer = get_api_response(user_prompt)
    pos = api_answer.find("\n")
    api_answer = api_answer[pos + 1:]
    await ctx.send(f"GPT Response is: {api_answer}")


client.run(f'{disc_token}')


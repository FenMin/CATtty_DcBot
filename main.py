import discord
from discord.ext import commands
import json
import os


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='#',intents=intents)

with open('./data/data.json' , 'r') as f:
    data = json.load(f)

#--
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')


def addcog_path(path , pathname):
    for filename in os.listdir(path):
        if filename.endswith('.py'):
            bot.load_extension(f'{pathname}.{filename[:-3]}')
            

addcog_path('./cogs' , 'cogs')
addcog_path('./cogs/listener' , 'cogs.listener')
addcog_path('./cogs/webCrawler' , "cogs.webCrawler")


@bot.event
async def on_ready():
    print('ready')


bot.run(data["token"])
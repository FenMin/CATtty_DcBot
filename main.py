import discord
from discord.ext import commands
import json
import os


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='#',intents=intents)

with open('data.json' , 'r') as f:
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


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')



@bot.event
async def on_ready():
    print('ready')


bot.run(data['token'])
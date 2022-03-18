import discord
from discord.ext import commands
import json
import os
import random

intents = discord.Intents.all()


class CustonHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        ram_color = int(["0x"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0] , 16)
        embed=discord.Embed(title="指令列表", description="help大全", color=ram_color)
        embed.set_author(name=f'**CATtty_BOT**', icon_url="https://cdn.discordapp.com/avatars/835511836078112778/a6b842b75bc1dd27bb929440a3c64c57.png?size=4096")
        embed.set_thumbnail(url="https://imgur.com/gtoRhRQ.png")
        embed.add_field(name="> **#weather**" , value="```查詢全台各縣市的天氣狀況```" , inline=True)
        embed.add_field(name="> **#covid**" , value="```查看台灣每日確診人數```", inline=False)
        embed.add_field(name="> **#tran <中文句子/ENG sentence>**" , value="```翻譯句子 中<->英```" , inline=False)
        embed.add_field(name="> **#bg <圖片url/圖片檔>**" , value="```圖片去背```" , inline=False)
        embed.add_field(name="> **#clear <數字(小於200)>**" , value="```清除訊息 (從最新)```" , inline=False)

        await self.get_destination().send(embed = embed)
        #for cog in mapping:
        #    await self.get_destination().send(f'{[command.name for command in mapping[cog]][0]}')
        
    async def send_cog_help(self, cog):
        await self.get_destination().send("cog_help test")
    
    async def send_group_help(self, group):
        return await super().send_group_help(group)
    
    async def send_command_help(self, command):
        await self.get_destination().send("command help test")


bot = commands.Bot(command_prefix='#',intents=intents , help_command= CustonHelp())

with open('./data/data.json' , 'r') as f:
    data = json.load(f)


def detect_path(extension):    #這甚麼智障寫法 lul
    try:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        return True
    except:
        try:
            bot.unload_extension(f'cogs.listener.{extension}')
            bot.load_extension(f'cogs.listener.{extension}')
            return True
        except:
            try:
                bot.unload_extension(f'cogs.webCrawler.{extension}')
                bot.load_extension(f'cogs.webCrawler.{extension}')
                return True
            except:
                try:
                    bot.unload_extension(f'cogs.twitch_get.{extension}')
                    bot.load_extension(f'cogs.twitch_get.{extension}')
                    return True
                except:
                    return False
'''
@bot.command()
async def load(ctx, extension):
        detect_path(extension)

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
'''

@bot.command()
async def reload(ctx, extension):
    if ctx.author.id == data['my_id']:
        if detect_path(extension):
            await ctx.send("> **`succeeded in reloading`**")
        else:
            await ctx.send("> **`failed to reload`**")
    else:
        await ctx.reply(f"> ```{ctx.author.name} you can't do this command```")

def addcog_path(path , pathname):
    for filename in os.listdir(path):
        if filename.endswith('.py'):
            bot.load_extension(f'{pathname}.{filename[:-3]}')
            

addcog_path('./cogs' , 'cogs')
addcog_path('./cogs/listener' , 'cogs.listener')
addcog_path('./cogs/webCrawler' , "cogs.webCrawler")


@bot.event
async def on_ready():
    await bot.change_presence(activity  = discord.Game(name = "用\"#\"來玩我"))
    print('ready')


bot.run(data["token"])
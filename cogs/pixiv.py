from random import random
import discord
from discord.ext import commands
from pixivapi import Client
from pathlib import Path
from pixivapi import Size
import random

client = Client()



class pixiv(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
    


    @commands.command()
    async def nhentai(self,ctx):
        a = random.randint(100000,299999)
        
        await ctx.send(f'https://nhentai.net/g/{int(a)}/')







def setup(bot):
    bot.add_cog(pixiv(bot))
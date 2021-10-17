import discord
from discord.ext import commands
import time
import random

from discord.ext.commands.core import guild_only

class command(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    #--
    @commands.command()
    async def ping(self, ctx): 
        await ctx.send(f'**{round(self.bot.latency*1000)}**ms')
    
    @commands.command()
    async def clean(self, ctx, num:int):
        await ctx.channel.purge(limit=num+1)
        await ctx.channel.send(f'已刪除 ***{num}*** 則訊息')
        time.sleep(2)
        await ctx.channel.purge(limit=1)
   
    @commands.command(brief="隨機數創語音頻道")
    async def voice(self, ctx):
        x = random.randint(1,3)
        await ctx.send(f'創建 ***{x}*** 個語音頻道')
        for i in range (x):
            await ctx.guild.create_voice_channel(f'第{i+1}個')
            if i+1 == x:
                await ctx.send(f'結束')

    @commands.command(brief = "瘋狂刪頻")
    async def delete(self, ctx):     
        guild = ctx.guild
        channel = guild.channels
        await self.bot.fetch_channel(channel)
        
    

        

def setup(bot):
    bot.add_cog(command(bot))

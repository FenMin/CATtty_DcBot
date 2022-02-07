import discord
from discord.ext import commands
import time


from discord.ext.commands.core import guild_only

class command(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command()
    async def ping(self, ctx): 
        await ctx.send(f'**{round(self.bot.latency*1000)}**ms')
    
    @commands.command()
    async def clean(self, ctx, num:int):
        await ctx.channel.purge(limit=num+1)
        await ctx.channel.send(f'已刪除 ***{num}*** 則訊息')
        time.sleep(1)
        await ctx.channel.purge(limit=1)
   
    @commands.command(brief="請輸入創頻數量")
    async def voice(self, ctx, num):        
        await ctx.send(f'創建 ***{num}*** 個語音頻道')  
        if num.isdigit():
            int(num)
            for i in range(num):
                ctx.send(f'i')
                await ctx.guild.create_voice_channel("第{i}個")
        else:
            await ctx.send("請輸入數字")
            
                

    @commands.command(brief = "瘋狂刪頻")
    async def delete(self, ctx):     
        guild = ctx.guild
        channel = guild.channels
        await self.bot.fetch_channel(channel)
        
    

        

def setup(bot):
    bot.add_cog(command(bot))

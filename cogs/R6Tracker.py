import discord
from discord.ext import commands

class R6Tracker(commands.Cog):
    def __init__(self , bot):
        self.bot = bot
    
    async def r6(self,ctx):
        await ctx.send("未完工啦")
    
    
        
        

















def setup(bot):
    bot.add_cog(R6Tracker(bot))
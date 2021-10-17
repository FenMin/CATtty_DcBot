import discord
import time
from discord.ext import commands

class record(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief= "超沒效率的紀錄文字")
    async def r(self, ctx, *message):
        channel = self.bot.get_channel(836611800132878427)
        await channel.send(' '.join(message))
        time.sleep(1.5)
        await ctx.channel.purge(limit=1)








def setup(bot):
    bot.add_cog(record(bot))
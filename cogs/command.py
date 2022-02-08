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
    async def create_voice(self, ctx, num):         
        if num.isdigit():
            await ctx.send(f'創建 ***{num}*** 個語音頻道') 
            for i in range(int(num)):
                await ctx.guild.create_voice_channel(f"第{i+1}個語音頻道")
        else:
            await ctx.send("請輸入數字")
       
    @commands.command(brief="刪除開頭為 \"第\" 結尾為 \"個\" 的頻道")
    async def delete_channel(self, ctx):
        channel = ctx.guild.channels
        for i in channel:  
            if i.name[0] == "第" and (i.name[-4:] == "語音頻道" or i.name[-4:] == "文字頻道"):  
                await i.delete()
                await ctx.send(f'以刪除 ***{i.name}*** 之 ***{i.type}*** 頻道')

    @commands.command(brief="請輸入創頻數量")
    async def create_text(self, ctx, num):         
        if num.isdigit():
            await ctx.send(f'創建 ***{num}*** 個文字頻道') 
            for i in range(int(num)):
                await ctx.guild.create_text_channel(f"第{i+1}個文字頻道")
        else:
            await ctx.send("請輸入數字")

    @commands.command()
    async def test(self , ctx):
        #guild = self.bot.guilds
        #for i in guild:
        #    await ctx.send(f'{i.owner} , {type(i.owner)}')
        await ctx.send(ctx.author.voice)

def setup(bot):
    bot.add_cog(command(bot))

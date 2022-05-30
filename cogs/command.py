from async_timeout import timeout
import discord
from discord.ext import commands
from discord.ui import Button , View
import time
from datetime import datetime
import random
from discord.ext.commands.core import guild_only
from pytest import Class

class CountdownButton(Button):
    def __init__(self):
        super().__init__(label="刷新" , style=discord.ButtonStyle.primary, emoji="🔄")
    
    async def callback(self, interaction):
        present = datetime.now()
        future = datetime(2022, 4, 30, 0, 0, 0)
        diff = future - present

        count_hours, rem = divmod(diff.seconds, 3600)
        count_minutes, count_seconds = divmod(rem, 60)

        ram_color = int(["0x"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0] , 16)
        embed = discord.Embed(title="統測倒數" , color=ram_color)
        embed.add_field(name="--------------" , value=f"{diff.days}天 {count_hours}小時 {count_minutes}分 {count_seconds}秒")

        await interaction.message.edit(embed = embed)

class musicbtn(View):
    def __init__(self):
        super().__init__(timeout=30)
        self.status = 0

    @discord.ui.button(label = "暫停" , style = discord.ButtonStyle.danger , emoji="⏸️")
    async def call(self , button, interaction):    
        if not self.status:  #status == pause
            button.label = "繼續"
            button.style = discord.ButtonStyle.green
            button.emoji = "▶️"
            self.status = 1

            
        else:
            button.label = "暫停"
            button.style = discord.ButtonStyle.danger
            button.emoji = "⏸️"
            self.status = 0

        await interaction.response.edit_message(view = self)
        
    def get_status(self):
        return self.status

class testbtn(View):
    def __init__(self):
        super().__init__(timeout=None)    

    @discord.ui.button(label = "測試" , style = discord.ButtonStyle.green)
    async def call(self, button, interaction):
        await interaction.response.send_message(interaction.channel, view = self)


class command(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="test")
    @commands.is_owner()
    async def test(self , ctx):
        view = testbtn()
        await ctx.send("T",view = view)

    @commands.command()
    async def ping(self, ctx): 
        await ctx.send(f'**{round(self.bot.latency*1000)}**ms')
    
    @commands.command()
    async def clear(self, ctx, num:int):
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

    

    @commands.command(name="countdown")
    async def countdown(self,ctx):
        present = datetime.now()
        future = datetime(2022, 4, 30, 0, 0, 0)
        diff = future - present

        count_hours, rem = divmod(diff.seconds, 3600)
        count_minutes, count_seconds = divmod(rem, 60)
        btn = CountdownButton()
        view = View(timeout=None)
        view.add_item(btn)
        
        ram_color = int(["0x"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0] , 16)

        embed = discord.Embed(title="統測倒數" , color=ram_color)
        embed.add_field(name="--------------" , value=f"{diff.days}天 {count_hours}小時 {count_minutes}分 {count_seconds}秒")

        bot_msg = await ctx.send( embed=embed, view=view)

        


        


def setup(bot):
    bot.add_cog(command(bot))

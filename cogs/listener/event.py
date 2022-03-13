import discord
from discord.ext import commands
import time
import random
from datetime import datetime



class event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #--
    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        if message.content == 'loop':
            x = random.randint(1 , 10)
            await channel.send(f'共刷 *{x}* 則')

            for y in range (x):                            
               await channel.send(f'第 {y+1} 次刷頻中')
               time.sleep(0.5)
            else:
               await channel.send(f'刷頻結束,共刷了 **{y+1}** 則訊息')
    

    @commands.Cog.listener()
    async def on_message(self, msg):
        channel = msg.channel
        if msg.content == "$(countdown)":
            status = 1
            while True:
                if status:
                    present = datetime.now()
                    future = datetime(2022, 4, 30, 0, 0, 0)
                    difference = future - present
                    bot_msg = await channel.send(f"統測倒數 {str(difference)[:-7]}")
                    status=0
                else:
                    present = datetime.now()
                    future = datetime(2022, 4, 30, 0, 0, 0)
                    difference = future - present
                    await bot_msg.edit(f"統測倒數 {str(difference)[:-7]}")

    #@commands.Cog.listener()
    #async def on_message(self, msg):
    #    if msg.content.startswith('87'):
    #        pass
    
    
                
        




def setup(bot):
    bot.add_cog(event(bot))
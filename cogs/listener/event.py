import discord
from discord.ext import commands
import time
import random




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

    
    #@commands.Cog.listener()
    #async def on_message(self, msg):
    #    if msg.content.startswith('87'):
    #        pass
    
    
                
        




def setup(bot):
    bot.add_cog(event(bot))
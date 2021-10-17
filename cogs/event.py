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
        if message.content.startswith('loop'):
           y=1
           x = random.randint(1 , 10)
           channel = message.channel
           await channel.send(f'共刷 *{x}* 則')
           print(x)
           for y in range (x):                            
               y = y+1
               await channel.send(f'第 {y} 次刷頻中')
               print(y)
               time.sleep(1)
               if y==x:
                   await channel.send(f'刷頻結束,共刷了 **{y}** 則訊息')
                   break
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, channel_id, guild_id, member): 
        pass
        #print(guild_id)
        #print(channel_id)
        #channel = self.bot.get_channel(835720347809742848)
        #await channel.send(f'歡迎進入')
    
                
        




def setup(bot):
    bot.add_cog(event(bot))
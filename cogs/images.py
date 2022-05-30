import discord
from discord.ext import commands
from discord.ext.commands.core import command
import requests
import time
import shutil
import os
import json

with open('data/data.json' , 'r') as f:
    data = json.load(f)


class images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def bg(self,ctx,*arg):
        
            if arg:
                mes = arg[0]
            else:
                mes = ctx.message.attachments[0].url

            response = requests.get(mes, stream=True)

            with open('./image/images.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            time.sleep(1)

            response = requests.post(
             'https://api.remove.bg/v1.0/removebg'
             ,
             files={'image_file': open('./image/images.png', 'rb')},
             data={'size': 'auto'},
             headers={'X-Api-Key': data['removebgapi']},
            )
            if response.status_code == requests.codes.ok:
                with open('./image/no-bg.png', 'wb') as out:
                    out.write(response.content)
                    await ctx.send(file = discord.File('./image/no-bg.png'))
                 
            else:
                print("Error:", response.status_code, response.text)
            time.sleep(1)
            os.remove("./image/images.png")
            os.remove("./image/no-bg.png")
                    
        
            #await ctx.send("> `輸入錯誤 非`***`網址`***`或`***`圖片`***  **`或這張照片沒有明顯前後景特徵而無法判斷背景`**")
    
    @commands.command()
    async def image(self,mes):
        pass





def setup(bot):
    bot.add_cog(images(bot))
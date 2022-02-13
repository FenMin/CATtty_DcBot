from re import T
import discord
import time
from discord.ext import commands
from googletrans.client import Translator


translator = Translator()

class translate(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot


    @commands.command(brief= "翻譯")
    async def tran(self , ctx, *message):
        mes = (' '.join(message))
        tran = translator.detect([mes])
        
        for trans_detect in tran:  
           if trans_detect.lang == 'en':
               trans_content_en = translator.translate([mes], dest='zh-tw' , src='en')
               for trans_zh in trans_content_en:
                   tran_origin = trans_zh.origin
                   tran_text = trans_zh.text
           
           elif trans_detect.lang == 'zh-tw' or 'zh-cn':
               trans_content_zh = translator.translate([mes],dest='en' , src='zh-tw')
               for trans_en in trans_content_zh:
                   tran_origin = trans_en.origin
                   tran_text = trans_en.text
       
        embed=discord.Embed(title=" ",color=0x00e1ff)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/tuts/256/google_translate.png")
        embed.add_field(name="__原句__", value=(f'**{tran_origin}**'), inline=True)
        embed.add_field(name="__翻譯__", value=(f'**{tran_text}**'), inline=False)
        await ctx.send(embed=embed)








def setup(bot):
    bot.add_cog(translate(bot))
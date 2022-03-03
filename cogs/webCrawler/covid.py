import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bs4
import random

def find_class(doc , cl:str , index):
    return doc.find_all(class_ = cl)[index].text

def total_list():
    total = []
    url = "https://news.campaign.yahoo.com.tw/2019-nCoV/index.php"
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
        doc = bs4(r.text , "html.parser")
        refresh_time = find_class(doc, "sub" , 0)
        total = find_class(doc , "num _big",0)
        daily_add = find_class(doc, "num _big _red",0)
        local_add = find_class(doc, "num _small",0)
        import_add = find_class(doc, "num _small",1)
        died = find_class(doc, "num _small",2)
        total_local = doc.find_all("p")[0].text
        total_import = doc.find_all("p")[1].text
        total_died = doc.find_all("p")[2].text

        total_global = doc.find_all(class_="current")[0].text
        die_global = doc.find_all(class_="current")[1].text
        total = [refresh_time, total, daily_add, local_add,  total_local,import_add, total_import, died,  total_died, total_global, die_global]

        return total



class covid(commands.Cog):

    def __init__(self , bot):
        self.bot = bot


    @commands.command()
    async def covid(self,ctx):
        total = total_list()
        ram_color = int(["0x"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0] , 16)
        
        embed=discord.Embed(title="Covid-19", description=total[0], color=ram_color)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2785/2785819.png")
        embed.add_field(name="總確診", value=total[1], inline=False)
        embed.add_field(name="今日新增", value=total[2], inline=0)
        embed.add_field(name="本土病例", value=total[3], inline=True)
        embed.add_field(name="本主累計", value=total[4], inline=True)
        embed.add_field(name="-", value="-", inline=True)
        embed.add_field(name="境外移入", value=total[5], inline=True)
        embed.add_field(name="境外累計", value=total[6], inline=True)
        embed.add_field(name="-", value="-", inline=True)
        embed.add_field(name="死亡病例", value=total[7], inline=1)
        embed.add_field(name="死亡累計", value=total[8], inline=1)
        embed.add_field(name="-", value="-",inline=True)
        embed.add_field(name="全球資訊", value=f"---------",inline=False)
        embed.add_field(name="全球總確診", value=total[9], inline=False)
        embed.add_field(name="全球總死亡", value=total[10], inline=False)

        await ctx.send(embed=embed)





def setup(bot):
    bot.add_cog(covid(bot))
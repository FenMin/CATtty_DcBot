import discord
from discord.ext import commands
import requests
import json


class covid(commands.Cog):

    def __init__(self , bot):
        self.bot = bot


    @commands.command()
    async def covid(self):
        url = "https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4001&limited=TWN"
        response = requests.get(url)
        if response == "200":
            data = json.loads(response.text)



def setup(bot):
    bot.add_cog(covid(bot))
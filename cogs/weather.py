import discord
from discord.ext import commands
import requests
import json



with open('data/data.json' , 'r') as f:
    api_data = json.load(f)  


class weather(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, city_ori:str):

        if isinstance(city_ori , str):

            city = city_ori.replace("台" , "臺")
            url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
            params = {
                "Authorization": api_data["weather_api"],
                "locationName": city,
            }

            response = requests.get(url, params=params)


            if response.status_code == 200:
                data = json.loads(response.text)

                try:
                    locations = data["records"]["location"][0]["locationName"]
                    weather_elements = data["records"]["location"][0]["weatherElement"]
                    

                    embed=discord.Embed(title="天氣", description=city_ori, color=0x00abf5)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1555/1555512.png")
                    embed.add_field(name="時間 ", value=weather_elements[0]["time"][0]['startTime'], inline=False)
                    embed.add_field(name="當日最高溫", value=weather_elements[4]["time"][0]["parameter"]["parameterName"], inline=True)
                    embed.add_field(name="當日最低溫", value=weather_elements[2]["time"][0]["parameter"]["parameterName"], inline=True)
                    embed.add_field(name="降雨機率", value=weather_elements[1]["time"][0]["parameter"]["parameterName"], inline=False)
                    embed.add_field(name="本日氣候狀況", value=weather_elements[0]["time"][0]["parameter"]["parameterName"], inline=True)
                    embed.add_field(name="本日溫度狀況", value=weather_elements[3]["time"][0]["parameter"]["parameterName"], inline=True)
                    embed.set_footer(text="資料來源：中央氣象局")
                    await ctx.send(embed=embed)
                except:
                    await ctx.send("> **錯誤**  *無此城市..*")
            else:
                await ctx.send(f'api爬蟲出現問題... 哨後再試 狀況碼 **{response.status_code}**')
        else:
            await ctx.send("請輸入城市... E.g.台北市")














def setup(bot):
    bot.add_cog(weather(bot))
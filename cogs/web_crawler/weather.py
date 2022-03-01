import discord
from discord.ext import commands
import requests
import json
from ..buttonCmd import weatherButton , weatherSelect



with open('data/data.json' , 'r') as f:
    api_data = json.load(f)  

def get_data_with_time(city , time_index:int):
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
                "Authorization": api_data["weather_api"],
                "locationName": city
            }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = json.loads(response.text)

        locations = data["records"]["location"][0]["locationName"]
        weather_elements = data["records"]["location"][0]["weatherElement"]


        time = weather_elements[0]["time"][time_index]['startTime']
        maxT = weather_elements[4]["time"][time_index]["parameter"]["parameterName"]
        minT = weather_elements[2]["time"][time_index]["parameter"]["parameterName"]
        rain = weather_elements[1]["time"][time_index]["parameter"]["parameterName"]
        weather_status = weather_elements[0]["time"][time_index]["parameter"]["parameterName"]
        temp_status = weather_elements[3]["time"][time_index]["parameter"]["parameterName"]

        weather_list = [time , maxT , minT, rain, weather_status, temp_status]
        return weather_list

    else:
        print("false: " , response.status_code)
class weather(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, city_ori:str):

        if isinstance(city_ori , str):

            city = city_ori.replace("台" , "臺")
            
            try: 
                weather_list = get_data_with_time(city , 0)

                embed=discord.Embed(title="天氣", description=city_ori, color=0x00abf5)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1555/1555512.png")
                embed.add_field(name="時間 ", value=weather_list[0], inline=False)
                embed.add_field(name="當日最高溫", value=weather_list[1], inline=True)
                embed.add_field(name="當日最低溫", value=weather_list[2], inline=True)
                embed.add_field(name="降雨機率", value=weather_list[3], inline=False)
                embed.add_field(name="本日氣候狀況", value=weather_list[4], inline=True)
                embed.add_field(name="本日溫度狀況", value=weather_list[5], inline=True)
                embed.set_footer(text="資料來源：中央氣象局")
                await ctx.send(embed=embed , view=weatherButton())
            except:
                await ctx.send("> **錯誤**  *無此城市..*")

        else:
            await ctx.send("請輸入城市... E.g.台北市")














def setup(bot):
    bot.add_cog(weather(bot))
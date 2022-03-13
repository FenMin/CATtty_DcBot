import discord
import requests
import json
from discord.ext import commands
from discord.ui import Button, View, Select
import random

#from discord_components import Select,SelectOption

with open('./data/data.json' , 'r') as f:
    jdata = json.load(f)

def get_data_with_time(city , time_index:int):
    city = city.replace("台" , "臺")   
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
                "Authorization": jdata["weather_api"],
                "locationName": city
            }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = json.loads(response.text)

        locations = data["records"]["location"][0]["locationName"]
        weather_elements = data["records"]["location"][0]["weatherElement"]

        time_l = [weather_elements[0]["time"][0]['startTime'] , weather_elements[0]["time"][1]['startTime'],weather_elements[0]["time"][2]['startTime']]

        if time_index !=999:
            time = weather_elements[0]["time"][time_index]['startTime']
            maxT = weather_elements[4]["time"][time_index]["parameter"]["parameterName"]
            minT = weather_elements[2]["time"][time_index]["parameter"]["parameterName"]
            rain = weather_elements[1]["time"][time_index]["parameter"]["parameterName"]
            weather_status = weather_elements[0]["time"][time_index]["parameter"]["parameterName"]
            temp_status = weather_elements[3]["time"][time_index]["parameter"]["parameterName"]

            weather_list = [time , maxT , minT, rain, weather_status, temp_status]
            

            

            return weather_list
        
        else:
            return time_l

    else:
        print("false: " , response.status_code)



time_list = get_data_with_time("臺北市" , 999)

button_id = ["one" , "two" , "three"]


def button_detect(children , id):
    button = [x for x in children if x.custom_id == id][0] #itz a list
    return button

def weathersign(status):
    if status == "晴天":
        pic = jdata["sun"]

    elif status == "多雲":
        pic = jdata['cloud']

    elif status == "晴時多雲" or "多雲時晴":
        pic = jdata["cloudsun"]
    
    else:
        pic = jdata["rainy"]

    return pic

class weatherButton(View):
    def __init__(self,ctx):
        super().__init__(timeout= 60)
        self.value = 0
        self.ctx = ctx
        self.ram_color = int(["0x"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0] , 16)
        
    @discord.ui.button(label = time_list[0] , style=discord.ButtonStyle.red , custom_id="one" ,disabled=True)
    async def first_button(self, button , interaction): 
        
        button_num =  []

        for i in button_id:
            button_num.append(button_detect(self.children , i))

        index = 0
        for z in range(3):
            if z == index:
                button_num[index].disabled = True
                button_num[index].style = discord.ButtonStyle.red
            else:
                button_num[z].disabled = False
                button_num[z].style = discord.ButtonStyle.green
        
        
        
        weather_list = get_data_with_time(a , index)
        
        pic = weathersign(weather_list[4])

        embed=discord.Embed(title="天氣", description=a, color=self.ram_color)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=pic)
        embed.add_field(name="時間 ", value=weather_list[0], inline=False)
        embed.add_field(name="時段最高溫", value=weather_list[1], inline=True)
        embed.add_field(name="時段最低溫", value=weather_list[2], inline=True)
        embed.add_field(name="降雨機率", value=weather_list[3], inline=False)
        embed.add_field(name="時段氣候狀況", value=weather_list[4], inline=True)
        embed.add_field(name="時段溫度狀況", value=weather_list[5], inline=True)
        embed.set_footer(text="資料來源：中央氣象局")
        await interaction.response.edit_message(embed = embed, view=self)
        self.value = 1

        self.value = index
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(f"你不是操作者 , 操作者為: *{self.ctx.author.name}*" , ephemeral=True)
            return False
        else:
            return True
        

    @discord.ui.button(label = time_list[1], style=discord.ButtonStyle.green, custom_id="two")
    async def sencond_button(self , button , interaction):
        button_num = []

        for i in button_id:
            button_num.append(button_detect(self.children , i))


        index = 1
        for z in range(3):
            if z == index:
                button_num[index].disabled = True
                button_num[index].style = discord.ButtonStyle.red
            else:
                button_num[z].disabled = False
                button_num[z].style = discord.ButtonStyle.green
        

        weather_list = get_data_with_time(a , index)

        pic = weathersign(weather_list[4])

        embed=discord.Embed(title="天氣", description=a, color=self.ram_color)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=pic)
        embed.add_field(name="時間 ", value=weather_list[0], inline=False)
        embed.add_field(name="時段最高溫", value=weather_list[1], inline=True)
        embed.add_field(name="時段最低溫", value=weather_list[2], inline=True)
        embed.add_field(name="降雨機率", value=weather_list[3], inline=False)
        embed.add_field(name="時段氣候狀況", value=weather_list[4], inline=True)
        embed.add_field(name="時段溫度狀況", value=weather_list[5], inline=True)
        embed.set_footer(text="資料來源：中央氣象局")
        await interaction.response.edit_message(embed = embed, view=self)
        self.value = 1
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(f"你不是操作者 , 操作者為: *{self.ctx.author.name}*" , ephemeral=True)
            return False
        else:
            return True
    
    @discord.ui.button(label = time_list[2], style=discord.ButtonStyle.green, custom_id="three")
    async def third_button(self, button, interaction):
        button_num = []

        for i in button_id:
            button_num.append(button_detect(self.children , i))


        index = 2
        for z in range(3):
            if z == index:
                button_num[index].disabled = True
                button_num[index].style = discord.ButtonStyle.red
            else:
                button_num[z].disabled = False
                button_num[z].style = discord.ButtonStyle.green
        

       
        weather_list = get_data_with_time(a , index)

        pic = weathersign(weather_list[4])

        embed=discord.Embed(title="天氣", description=a, color=self.ram_color)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=pic)
        embed.add_field(name="時間 ", value=weather_list[0], inline=False)
        embed.add_field(name="時段最高溫", value=weather_list[1], inline=True)
        embed.add_field(name="時段最低溫", value=weather_list[2], inline=True)
        embed.add_field(name="降雨機率", value=weather_list[3], inline=False)
        embed.add_field(name="時段氣候狀況", value=weather_list[4], inline=True)
        embed.add_field(name="時段溫度狀況", value=weather_list[5], inline=True)
        embed.set_footer(text="資料來源：中央氣象局")
        await interaction.response.edit_message(embed = embed, view=self)
        self.value = 1
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(f"你不是操作者 , 操作者為: *{self.ctx.author.name}*" , ephemeral=True)
            return False
        else:
            return True

''' //<origin code> for testing//

class weatherSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="optionByClass", value="a"),
            discord.SelectOption(label="b", value="b"),
        ]

        super().__init__(placeholder="Select something!",
                        options=options,
                        custom_id="select1",)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("test")

class SelectView(View):
    def __init__(self):
        super().__init__()
        self.add_item(weatherSelect())
'''   

class weatherSelect(View):
    def __init__(self , ctx):
        super().__init__(timeout = 60)
        self.ctx = ctx
        self.value = None

    options=[discord.SelectOption(label="基隆市" , value="基隆市"),
             discord.SelectOption(label="台北市" , value="台北市"),
             discord.SelectOption(label="新北市" , value="新北市"),
             discord.SelectOption(label="桃園市" , value="桃園市"),
             discord.SelectOption(label="宜蘭縣" , value="宜蘭縣"),
             discord.SelectOption(label="新竹市" , value="新竹市"),
             discord.SelectOption(label="新竹縣" , value="新竹縣"),
             discord.SelectOption(label="苗栗縣" , value="苗栗縣"),
             discord.SelectOption(label="台中市" , value="台中市"),
             discord.SelectOption(label="彰化縣" , value="彰化縣"),
             discord.SelectOption(label="南投縣" , value="南投縣"),
             discord.SelectOption(label="雲林市" , value="雲林市"),
             discord.SelectOption(label="嘉義市" , value="嘉義市"),
             discord.SelectOption(label="花蓮縣" , value="花蓮縣"),
             discord.SelectOption(label="台東縣" , value="台東縣"),
             discord.SelectOption(label="台南市" , value="台南市"),
             discord.SelectOption(label="高雄市" , value="高雄市"),
             discord.SelectOption(label="屏東縣" , value="屏東縣"),
             ]

    @discord.ui.select(placeholder="Select something!", options=options)
    async def when_call(self, select,interaction:discord.Interaction):
        
        #await interaction.response.send_message(f"you choose {select.values[0]}")
        self.value = select.values[0]
        global a
        a = select.values[0]
        get_data_with_time(a , 0)
        self.stop()

    async def on_timeout(self):
        await self.ctx.reply("timeout" , ephemeral=True)
        return 

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(f"你不是操作者 , 操作者為: *{self.ctx.author.name}*" , ephemeral=True)
            return False
        else:
            return True

class buttonCmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testb(self , ctx):
        view = weatherButton()
        await ctx.send("test" , view=view)

    @commands.command()
    async def testc(self, ctx):

        view = weatherSelect(ctx)
        await ctx.send(f"test" , view=view )
        res = await view.wait()
        if res:
            pass
        else:
            await ctx.send(f'one step on {view.value}')





def setup(bot):
    bot.add_cog(buttonCmd(bot))
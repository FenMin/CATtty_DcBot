import discord
from discord.ext import commands
from discord.ui import Button, View, Select
#from discord_components import Select,SelectOption



button_id = ["one" , "two" , "three"]

def button_detect(children , id):
    button = [x for x in children if x.custom_id == id][0] #itz a list
    return button

class weatherButton(View):
    

    @discord.ui.button(label = "fistDay" , style=discord.ButtonStyle.green , custom_id="one")
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
            
        
        await interaction.response.edit_message(view=self)
        await interaction.channel.send(f"firstButton got activity {button_num[0]}")

    @discord.ui.button(label = "sencondDay", style=discord.ButtonStyle.green, custom_id="two")
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

        await interaction.response.edit_message(view=self)
        await interaction.channel.send(f"secondButton got activity{button_num[1]}")
    
    @discord.ui.button(label = "thirdDay", style=discord.ButtonStyle.green, custom_id="three")
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

        await interaction.response.edit_message(view=self)
        await interaction.channel.send(f"thirdButton got activity {button_num[2]}")
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
    options = [
            discord.SelectOption(label="optionByClass", value="a"),
            discord.SelectOption(label="optionByInherView", value="b"),
        ]
    @discord.ui.select(placeholder="Select something!",
                        options=options,
                        custom_id="select1")

    async def when_call(self, select,interaction:discord.Interaction):
        await interaction.response.send_message("itz test")



class buttonCmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testb(self , ctx):
        view = weatherButton()
        await ctx.send("test" , view=view)

    @commands.command()
    async def testc(self, ctx):

        view = weatherSelect()

        await ctx.send("testc" , view=view)











def setup(bot):
    bot.add_cog(buttonCmd(bot))
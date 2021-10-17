import discord
from discord.ext import commands
from types import TracebackType
from selenium import webdriver
import time



class apexTracker(commands.Cog):
    
    def __init__(self , bot):
        self.bot = bot
    
    
    @commands.command(brief = "壞了")
    async def apex(self, ctx, name_inp:str):
        name_val = []
        value_val = []
        dict_1 = {}
        i = 0
        driver = webdriver.PhantomJS('C:/Users/user/Desktop/code/phantomjs-2.1.1-windows/bin/phantomjs.exe')
        urls = f'https://apex.tracker.gg/apex/profile/origin/{name_inp}/overview'
        driver.get(f'https://apex.tracker.gg/apex/profile/origin/{name_inp}/overview')
        name_element = driver.find_elements_by_class_name("name")
        
        for names in name_element:
            if (names.text != 'Home' ) & (names.text != 'Leaderboards') & (names.text != 'Insights') & (names.text!= 'More') & (names.text!= 'Premium') & (names.text!= 'Shop'):
                name_val.append(names.text)   

        value_element = driver.find_elements_by_class_name("value")
        for values in value_element:
            value_val.append(values.text) 

        for i in range(len(value_val)):    
            if (name_val[i+3] != "Kills"):
                dict_1[name_val[i+3]] = value_val[i]
            elif(dict_1.get("Kills") == None):
                dict_1[name_val[i+3]] = value_val[i]
            else:
                break

        rating_lab = driver.find_element_by_class_name("rating__label")
        rating_val = driver.find_element_by_class_name("rating__value")
        img = driver.find_element_by_class_name("ph-avatar__image")
        rating_img = driver.find_element_by_class_name("rating__image")
        embed=discord.Embed(title="Apex Legends", url=urls, description='status')
        embed.set_author(name=name_inp, url=urls, icon_url=img.get_attribute('src'))
        embed.set_thumbnail(url=rating_img.get_attribute('src'))
        embed.add_field(name="等級", value=dict_1['Level'], inline=False)
        embed.add_field(name="總擊殺", value=dict_1['Kills'], inline=False)
        embed.add_field(name="總傷害", value=dict_1['Damage'], inline=False)
        embed.add_field(name="當前排位", value=rating_lab.text, inline=True)
        embed.add_field(name="當前分數", value=rating_val.text, inline=True)
        embed.set_footer(text=ctx.author)
        await ctx.send(embed=embed)
        dict_1.clear()
        i=0
        name_val.clear()
        value_val.clear()
        driver.quit()

        








def setup(bot):
    bot.add_cog(apexTracker(bot))
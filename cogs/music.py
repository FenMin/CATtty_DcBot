from discord import channel
import youtube_dl
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from discord import Client

class music(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    players = {}

    @commands.command()
    async def join(self, ctx):
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
        except:
            pass
    @commands.command()
    async def leave(self,ctx):
        try:
            channel = ctx.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.disconnect()

            else:
                await ctx.send("u can't do it")
        except:
            pass
    @commands.command(brief="音樂播放")
    async def play(self, ctx, url):
        pass
            





def setup(bot):
    bot.add_cog(music(bot))
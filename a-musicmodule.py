import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from youtubesearchpython import VideosSearch
import pytube
import os

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
	print('EURT bot online!')  

#Use the when_done variable  to delete video file after
Queue = []

@client.command()
async def play(ctx, song):
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='general')
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	await voiceChannel.connect()
	try:
		videosSearch = VideosSearch(f'{song}', limit = 1)
		x = str(videosSearch.result()).split(" ")[4].replace("'","").replace(',','')
	except IndexError:
		embed = discord.Embed(description='Song not found')
		await ctx.send(embed=embed)
	youtube_url = 'https://www.youtube.com/watch?v= '.replace(" ", x)
	videoDownload = pytube.YouTube(youtube_url).streams.get_highest_resolution().download('')
	song_there = os.path.isfile(videoDownload)
	voice.play(discord.FFmpegPCMAudio(f"{pytube.YouTube(youtube_url).name}.mp4"))

@client.command()
async def leave(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_connected():
		await voice.disconnect()
	else:
		embed = discord.Embed(description='The bot is not connected to a voicechannel')
		await ctx.send(embed=embed)

@client.command()
async def pause(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_playing():
		voice.pause()
	else:
		embed = discord.Embed(description='No audio is currently running')
		await ctx.send(embed=embed)

@client.command()
async def resume(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_paused():
		voice.resume()
	else:
		embed = discord.Embed(description='Audio is not paused')
		await ctx.send(embed=embed)

@client.command()
async def stop(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	voice.stop()

client.run('ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.KO5zzXVpmAYKOhv11OvIS2xBOqI')   
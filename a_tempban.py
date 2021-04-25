import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from discord.ext.commands import has_permissions, MissingPermissions
import time
import os
import random
import datetime
import steamfront
from datetime import timedelta
from discord.ext.commands import CommandNotFound
import datetime
import pymongo 
from pymongo import MongoClient
import io
import chat_exporter


intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')
dbClient = MongoClient("mongodb+srv://D1P:D1P9812@hokuspokusdb.gehgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = dbClient["EURTDatabase"]
collection = db["newSteamLink"]
wait = 0


@client.event
async def on_ready():
	print('EURT bot online!')

@client.command()
async def save(ctx):
	limit = None
	transcript = await chat_exporter.export(ctx.channel, limit)
	if transcript is None:
		return
	transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"transcript-{ctx.channel.name}.html")
	await ctx.send(file=transcript_file)

@client.event
async def ban(ctx):
	guild = client.get_guild(810954832583852083)
	banned = guild.get_role()
	try:
		cmd, user, timeAmount= ctx.message.content.split(" ", 1)
	except IndexError:
		print('Wrong format')
	await ctx.message.mentions[0].add_roles(banned)
	post = {"DiscordName": f"{ctx.message.mentions[0]}", "DiscordID": f"{ctx.message.mentions[0].id}", "bannedBy":f"{ctx.message.author}"}
	collection.insert_one(post)
	print('User has been banned')
    
async def something():
	while True:
		guild = client.get_guild(810954832583852083)
		banned = guild.get_role()#insert role id
		muted = guild.get_role()
		for dbFind in collection.find({"banType": "tempBan"}):
			userId = dbFind["memberId"]
			user = guild.get_member(int(userId))
			unbanTime = dbFind["unbanTime"]
			if unbanTime > datetime.datetime.now:
				return
			else:
				await user.remove_roles(Banned)
		for dbFind in collection.find({"muteType": "tempMute"}):
			user = guild.get_member(int(userId))
			unmuteTime = dbFind["unmuteTime"]
			if unmuteTime > datetime.datetime.now:
				return
			else:
				await user.remove_roles(muted)
		await asyncio.sleep(600)



client.run('ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.KO5zzXVpmAYKOhv11OvIS2xBOqI')

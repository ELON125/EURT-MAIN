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

@client.event
async def ban(ctx):
	banned = guild.get_role()
	try:
		cmd, user, time or None = ctx.message.content.split(" ", 1 or 0)
	except IndexError:
		print('Wrong format')
	await ctx.message.mentions[0].add_roles(banned)
	post = ["memberName": f"{ctx.message.mentions[0]}", "memberId": f"{ctx.message.mentions[0].id}", "banType":, "bannedBy":f"{ctx.message.author}"]
	collection.insert_one(post)
	print('User has been banned')
    
while True:
	banned = guild.get_role()#insert role id
	muted = guild.get_role()
	for dbFind in collection.find({"banType": "tempBan"}):
		user = guild.get_member(int(userId))
		unbanTime = dbFind["unbanTime"]
		if unbanTime > datetime.datetime.now:
			return
		else:
			await user.remove_roles(Banned)
	for dbFind in collection.find({"muteType": "tempMute"}):
		user = guild.get_member(int(userId))
		unbanTime = dbFind["unmuteTime"]
		if unmuteTime > datetime.datetime.now:
			return
		else:
			await user.remove_roles(muted)
	await asyncio.sleep(600)



client.run('ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.KO5zzXVpmAYKOhv11OvIS2xBOqI')

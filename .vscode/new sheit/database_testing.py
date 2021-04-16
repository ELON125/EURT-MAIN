import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from discord.ext.commands import has_permissions, MissingPermissions
import json
import time
import os
import random
import datetime
import steamfront
import replit
from replit import db
from datetime import timedelta
from discord.ext.commands import CommandNotFound
import re
import argparse
import datetime
import functools
import concurrent.futures
from multiprocessing.pool import ThreadPool
import requests
from steam.webapi import WebAPI
import discord.ext.commands
import steam
from steam.steamid import SteamID
import pymongo 
from pymongo import MongoClient

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
PROFILE_RX = re.compile(r"^\d+$")
STEAM_APIKEY = '370271383631C9089D74EBA5806050F9'
database = replit.database.AsyncDatabase('https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTY4ODk3NDksImlhdCI6MTYxNjc3ODE0OSwiaXNzIjoiY29ubWFuIiwiZGF0YWJhc2VfaWQiOiJmNzllMTMwZS0xZWZjLTQ4YTgtOWYyMi0wZTU2MDRkMjdjZjEifQ.5sPKa_6X__ujNyFxirs6GgSN6YOFUnT1ssn-BJ479Ak9ITsQhaSSaRMnrBJVsLlDn1r3ufiramP4erINRNqyZg')
dbClient = MongoClient("mongodb+srv://D1P:D1P9812@hokuspokusdb.gehgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = dbClient["EURTDatabase"]
collection = db["steamLink"]
wait = 0


@client.event
async def on_ready():
	guild = client.get_guild(810954832583852083)
	for document in collection.find():
		userID = document["DiscordID"]
		verified = discord.utils.get(guild.roles, name=f"Verified")
		user = guild.get_member(int(userID))
		await user.add_roles(verified)
		print(userID)
	print('Ready')



@client.command()
async def test(ctx):
	listNames = ['teico ||| https://cdn.discordapp.com/avatars/630481896559869987/7c3aaa1df10eb94b9dc4588cc76cc2fa.webp?size=1024 ||| 630481896559869987 ||| 2019-10-06 19:09:57.927000 ||| https://cdn.discordapp.com/avatars/630481896559869987/7c3aaa1df10eb94b9dc4588cc76cc2fa.webp?size=1024 ||| https://steamcommunity.com/id/7662452743588/ \n', '! Alyyyage ||| https://cdn.discordapp.com/avatars/286250067449348102/8af5ee4e3b7dcfa8aae732d9e4e4ade8.webp?size=1024 ||| 286250067449348102 ||| 2017-02-28 21:35:34.349000 ||| https://cdn.discordapp.com/avatars/286250067449348102/8af5ee4e3b7dcfa8aae732d9e4e4ade8.webp?size=1024 ||| http://steamcommunity.com/profiles/76561198316631663 \n', 'Orange ||| https://cdn.discordapp.com/avatars/320287736496128000/6674a7fd08ff63c9babddf3d03cbcd92.webp?size=1024 ||| 320287736496128000 ||| 2017-06-02 19:49:07.039000 ||| https://cdn.discordapp.com/avatars/320287736496128000/6674a7fd08ff63c9babddf3d03cbcd92.webp?size=1024 ||| http://steamcommunity.com/profiles/76561198034846253 \n', 'rango ||| https://cdn.discordapp.com/avatars/424330052319313930/a_9e6d475222ba2c05010bef1b0b89a8a0.gif?size=1024 ||| 424330052319313930 ||| 2018-03-16 22:16:08.144000 ||| https://cdn.discordapp.com/avatars/424330052319313930/a_9e6d475222ba2c05010bef1b0b89a8a0.gif?size=1024 ||| https://steamcommunity.com/profiles/76561198829510469 \n', 'lucas_p ||| https://cdn.discordapp.com/avatars/413378235385118730/0a76c8c27ff9f325d83197fa86ab22b3.webp?size=1024 ||| 413378235385118730 ||| 2018-02-14 16:57:31.512000 ||| https://cdn.discordapp.com/avatars/413378235385118730/0a76c8c27ff9f325d83197fa86ab22b3.webp?size=1024 ||| https://steamcommunity.com/profiles/76561198254872454 \n', 'Kooky ||| https://cdn.discordapp.com/embed/avatars/0.png ||| 262285739075698688 ||| 2016-12-24 18:29:53.229000 ||| https://cdn.discordapp.com/embed/avatars/0.png ||| https://steamcommunity.com/profiles/76561198204147647 \n', 'KING♚ ||| https://cdn.discordapp.com/avatars/234011199593775106/464a0ae1bca326359fa5a9475d547ce0.webp?size=1024 ||| 234011199593775106 ||| 2016-10-07 17:56:57.701000 ||| https://cdn.discordapp.com/avatars/234011199593775106/464a0ae1bca326359fa5a9475d547ce0.webp?size=1024 ||| https:/steamcommunity.com/profiles/76561198169026031/\n', 'Texa$. ||| https://cdn.discordapp.com/avatars/680870535827161134/0eedc230d8035fff933e8e8a9e515059.webp?size=1024 ||| 680870535827161134 ||| 2020-02-22 20:16:25.704000 ||| https://cdn.discordapp.com/avatars/680870535827161134/0eedc230d8035fff933e8e8a9e515059.webp?size=1024 ||| https://steamcommunity.com/profiles/76561198259188487 \n', 'PHARRA ||| https://cdn.discordapp.com/avatars/307575179138170891/20c05b33ebeacaf181260f31365627f2.webp?size=1024 ||| 307575179138170891 ||| 2017-04-28 17:53:57.177000 ||| https://cdn.discordapp.com/avatars/307575179138170891/20c05b33ebeacaf181260f31365627f2.webp?size=1024 ||| https://steamcommunity.com/id/pharra/ \n', 'Rev ||| https://cdn.discordapp.com/avatars/396699670946250752/a_1516eba6a8e56648046048c41d088ba7.gif?size=1024 ||| 396699670946250752 ||| 2017-12-30 16:22:51.877000 ||| https://cdn.discordapp.com/avatars/396699670946250752/a_1516eba6a8e56648046048c41d088ba7.gif?size=1024 ||| https://steamcommunity.com/profiles/76561198800303160 \n', '! Gigi ||| https://cdn.discordapp.com/avatars/444289761935622145/65315a50d39ac463db2c617f5eac3f41.webp?size=1024 ||| 444289761935622145 ||| 2018-05-11 00:08:53.750000 ||| https://cdn.discordapp.com/avatars/444289761935622145/65315a50d39ac463db2c617f5eac3f41.webp?size=1024 ||| https://steamcommunity.com/profiles/76561198990094369 \n', 'Gerix ||| https://cdn.discordapp.com/avatars/457441940791623700/75da7de042894c26a6012c3ec56d8deb.webp?size=1024 ||| 457441940791623700 ||| 2018-06-16 07:10:57.545000 ||| https://cdn.discordapp.com/avatars/457441940791623700/75da7de042894c26a6012c3ec56d8deb.webp?size=1024 ||| https://steamcommunity.com/profiles/76561198162573287 \n', '! Mood$ ||| https://cdn.discordapp.com/avatars/537299494945947648/8430360e7528c139294240beab4ab63b.webp?size=1024 ||| 537299494945947648 ||| 2019-01-22 15:56:22.137000 ||| https://cdn.discordapp.com/avatars/537299494945947648/8430360e7528c139294240beab4ab63b.webp?size=1024 ||| https://steamcommunity.com/profiles/76561198149693769 \n', 'Boogie ass hoe ||| https://cdn.discordapp.com/avatars/279171430376013824/975e825fd18dcae8b627df85697834d2.webp?size=1024 ||| 279171430376013824 ||| 2017-02-09 08:47:35.756000 ||| https://cdn.discordapp.com/avatars/279171430376013824/975e825fd18dcae8b627df85697834d2.webp?size=1024 ||| https://steamcommunity.com/id/frutikpts/ \n', 'NoBehaviour ||| https://cdn.discordapp.com/avatars/297318078407114753/a_1bfe0be5c485a1377e3272463ff1d4dd.gif?size=1024 ||| 297318078407114753 ||| 2017-03-31 10:35:53.795000 ||| https://cdn.discordapp.com/avatars/297318078407114753/a_1bfe0be5c485a1377e3272463ff1d4dd.gif?size=1024 ||| http://steamcommunity.com/profiles/76561198304963175 \n', '! Lem ||| https://cdn.discordapp.com/avatars/414451932267151382/b7cacee116cd93183e285023ebed7c97.webp?size=1024 ||| 414451932267151382 ||| 2018-02-17 16:04:00.797000 ||| https://cdn.discordapp.com/avatars/414451932267151382/b7cacee116cd93183e285023ebed7c97.webp?size=1024 ||| https://steamcommunity.com/profiles/76561198363875429 \n', 'KrelleS ||| https://cdn.discordapp.com/avatars/441628330551148554/f630cd53fe24e8f9343394a4cdda937b.webp?size=1024 ||| 441628330551148554 ||| 2018-05-03 15:53:19.061000 ||| https://cdn.discordapp.com/avatars/441628330551148554/f630cd53fe24e8f9343394a4cdda937b.webp?size=1024 ||| https://steamcommunity.com/profiles/76561198350943615 \n']
	for x in listNames:
		print(x)

@client.command()
async def database(ctx):
	guild = client.get_guild(810954832583852083)
	workedCheck = ""
	for member in guild.members:
		try:
			databaseSearchValue = db[f"{member}"]
			print(member, databaseSearchValue)
			workedCheck = workedCheck + member
			steamidgrabber = steam.steamid.steam64_from_url(databaseSearchValue, http_timeout=30)
			user = steamfront.user.User(id64=f'{steamidgrabber}', apiKey='370271383631C9089D74EBA5806050F9')
			post = {"DiscordName": f"{member.name}", "DiscordAvatar": f"{member.avatar_url}", "DiscordID": f"{member.id}", "DiscordCreationDate": f"{member.created_at}", "SteamName": f"{user}", "SteamProfileUrl": f"{user.profile_url}", "SteamId": f"{user.id64}"}
			collection.insert_one(post)
		except Exception:
			pass
	print(workedCheck)
		

@client.command()
async def getdiscord(ctx):
	try:
		messageContent = ctx.message.content
		cmd, steamid = messageContent.split(" ", 1)
	except IndexError:
		await ctx.send('Wrong format! [.getsteam (steam_id)]')
	if collection.count_documents({'SteamID': f'{steamid}'}) > 0:
		for dbFind in collection.find({"SteamID": f"{steamid}"}):
			steamName = dbFind["SteamName"]
			steamId = dbFind["SteamID"]
			discordName = dbFind["DiscordName"]
			discordAvatar = dbFind["DiscordAvatar"]
			discordID = dbFind["DiscordID"]
			discordCreationDate = dbFind["DiscordCreationDate"]
		embed=discord.Embed(title=f"{steamName}({steamid})")
		embed.set_thumbnail(url=discordAvatar)
		embed.add_field(name="Discord Name", value=f"{discordName}", inline=False)
		embed.add_field(name="Discord Id", value=f"{discordID}", inline=False)
		embed.add_field(name="Creation Date", value=f"{discordCreationDate}", inline=False)
		embed.set_footer(text=f"Requested by: {ctx.message.author}\nEU Rust Tournaments")
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(description='ID not in database')
		await ctx.send(embed=embed)
		return

@client.command()
async def getsteam(ctx):
	try:
		messageContent = ctx.message.content
		cmd, discordid = messageContent.split(" ", 1)
	except IndexError:
		await ctx.send('Wrong format! [.getsteam (discord_user_id)]')
	if collection.count_documents({"DiscordID":f"{discordid}"}) > 0:
		for dbFind in collection.find({"DiscordID": f"{discordid}"}):
			steamName = dbFind["SteamName"]
			steamId = dbFind["SteamID"]
			steamAvatar = dbFind["SteamAvatar"]
			steamLink = dbFind["SteamProfileUrl"]
			discordName = dbFind["DiscordName"]
			discordID = dbFind["DiscordID"]
		embed=discord.Embed(title=f"{discordName}({discordID})")
		embed.set_thumbnail(url=steamAvatar)
		embed.add_field(name="Steam Name", value=f"{steamName}", inline=False)
		embed.add_field(name="Steam ID", value=f"{steamId}", inline=False)
		embed.add_field(name="Profile Link", value=f"{steamLink}", inline=False)
		embed.set_footer(text=f"Requested by: {ctx.message.author}\nEU Rust Tournaments")
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(description='ID not in database')
		await ctx.send(embed=embed)
		return


@client.command()
async def newlink(ctx):
	member = ctx.author
	message = ctx.message.content
	try:
		cmd, steamurl = message.split(" ", 1)
	except Exception:
		embed = discord.Embed(description='Wrong format')
		await ctx.send(embed=embed)
	verified = discord.utils.get(ctx.guild.roles, name=f"Verified")
	if db.collection.count_documents({"SteamdProfileURL":f"{steamurl}"}, limit = 1):
			embed = discord.Embed(description='This account is already linked')
			await ctx.send(embed=embed)
	else:
		try:
			steamidgrabber = steam.steamid.steam64_from_url(steamurl, http_timeout=30)
			user = steamfront.user.User(id64=f'{steamidgrabber}', apiKey='370271383631C9089D74EBA5806050F9')
			post = {"DiscordName": f"{member.name}", "DiscordAvatar": f"{member.avatar_url}", "DiscordID": f"{member.id}", "DiscordCreationDate": f"{member.created_at}", "SteamName": f"{user.name}", "SteamProfileUrl": f"{user.profile_url}", "SteamID": f"{user.id64}", "SteamAvatar": f"{user.avatar}"}
			collection.insert_one(post)
		except Exception:
			embed = discord.Embed(description='Something went wrong')
			await ctx.send(embed=embed)
			await ctx.send(embed=embed)





client.run('ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.KO5zzXVpmAYKOhv11OvIS2xBOqI')

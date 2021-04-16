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
import discord.ext.commands
from steamfront import errors
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
	print('EURT bot online!')

@client.command()
async def send1(ctx):
	embed=discord.Embed(title="Arena settings!")
	embed.set_author(name="EURT")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
	embed.add_field(name="Map", value="Deadmans (unless told otherwise) ", inline=False)
	embed.add_field(name="Anti-ghost ", value="ON!", inline=False)
	embed.add_field(name="Skins", value="OFF!", inline=False)
	embed.add_field(name="Limit time", value="ON!", inline=False)
	embed.add_field(name="Funnels", value="Not allowed (It means that in any walled in area. there NEEDS to be two entrances if a entrance is smaller then the size of 1 wall. Make sure your ENTRANCE are the size of 1 wall AT LEAST) (walling yourself in is not allowed either)", inline=False)
	embed.add_field(name="Resets", value="If ur told to reset in the start of round then u must. (Its to late to ask for reset, if a player is dead. Or the opposite team reached sides.) ", inline=False)
	embed.add_field(name="Holo/no holo", value="Both teams need to agree on holo. (else its iron)", inline=False)
	embed.set_footer(text="If any problems accure, contact staff!")
	await ctx.send(embed=embed)

@client.command()
async def send2(ctx):
	embed=discord.Embed()
	embed.set_author(name="EURT")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
	embed.add_field(name="Requirements", value="•Shadowplay on with 5 minuts blayback!\n•No alt accounts!\n•Over 500 hours on your account\n•Verified on our discord!\n•Steam profile public while playing!", inline=False)
	await ctx.send(embed=embed)

@client.command()
async def send3(ctx):
	embed=discord.Embed(title="Bans?", description="Most bans, server bans, discord bans, etc, u can appeal on after 120 days, we follow the same principal. Game bans are considered that YOU cheated 100%, therefore we do not tolerate them and u can appeal after 6 months.  If u get approved after a check, then you will be able to play under these terms : Screen sharing on! 15 minutes replay! Dodging a check of any sort, will result in perm ban. (appeal-able after 120 days.) (if mid tourney then your team will be disced too.)")
	embed.set_author(name="EURT")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
	embed.set_footer(text="Ask staff if ur in doubt of anything. ")
	await ctx.send(embed=embed)

@client.command()
async def send4(ctx):
	embed=discord.Embed(title="1v1 ")
	embed.set_author(name="EURT")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
	embed.add_field(name="Match length", value="You play to 5 switch side at 3. ", inline=False)
	embed.add_field(name="subs", value="0", inline=False)
	embed.add_field(name="Limit time", value="2 minutes", inline=False)
	await ctx.send(embed=embed)

@client.command()
async def send4(ctx):
	embed=discord.Embed(title="2v2")
	embed.set_author(name="EURT")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
	embed.add_field(name="Match length", value="You play to 5 switch side at 3. ", inline=False)
	embed.add_field(name="Subs", value="1", inline=False)
	embed.add_field(name="Limit time", value="2 minutes", inline=False)
	await ctx.send(embed=embed)

@client.command()
async def send5(ctx):
	embed=discord.Embed(title="3v3")
	embed.set_author(name="EURT")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
	embed.add_field(name="Match length", value="You play to 5 switch side at 3. ", inline=False)
	embed.add_field(name="Subs", value="1", inline=False)
	embed.add_field(name="Limit time", value="2 minutes", inline=False)
	await ctx.send(embed=embed)

@client.command()
async def send6(ctx):
	embed=discord.Embed(title="4v4")
	embed.set_author(name="EURT")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
	embed.add_field(name="Match length", value="You play to 6 switch side at 3. ", inline=False)
	embed.add_field(name="Subs", value="2 (occasionally more)", inline=False)
	embed.add_field(name="Limit time", value="2 minutes", inline=False)
	await ctx.send(embed=embed)

@client.command()
async def send7(ctx):
	embed=discord.Embed(title="5v5 And above!")
	embed.set_author(name="EURT")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
	embed.add_field(name="Match length", value="You play to 6 switch side at 3. ", inline=False)
	embed.add_field(name="subs", value="2 (occasionally more)", inline=False)
	embed.add_field(name="Limit time", value="3 minutes", inline=False)
	await ctx.send(embed=embed)

#FOR INVITES USE THE LAYOUT USED IN THE EURC COUNTRY VOTE RESULTS
@client.command()
async def invites(ctx):
	invites = []
	for i in await ctx.guild.invites():
		if i.uses == 0:
			pass
		else:
			invites.append(f"{i.inviter} @|. {i.uses}")
	invites.sort(key=lambda x: int(x.split("@|.")[1]), reverse=True)
	print(invites)
	for invite in invites[:10]:
		print(invite.replace("@|.", ""))

@client.command()
async def link2(ctx):
	member = ctx.author
	message = ctx.message.content
	verified = discord.utils.get(ctx.guild.roles, name=f"Verified") 
	try:
		cmd, steamid64 = message.split(" ", 1)
	except Exception:
		embed = discord.Embed(description='Wrong format! format: .link (steamid64)')
		await ctx.send(embed=embed)
	steamIdString = steamid64
	steamIdString_lowercase = steamIdString.lower()
	ifSteamId64 = steamIdString_lowercase.islower()
	if collection.count_documents({"SteamID":f"{steamid64}"}) > 0:
		embed = discord.Embed(description='This account is already linked')
		await ctx.send(embed=embed)
		return
	else:
		if ifSteamId64 == False:
			if (len(str(steamid64))) == 17:
				post = {"DiscordName": f"{member.name}", "DiscordAvatar": f"{member.avatar_url}", "DiscordID": f"{member.id}", "DiscordCreationDate": f"{member.created_at}", "SteamID": f"{steamid64}", "isReal": "False" }
				collection.insert_one(post)
				embed = discord.Embed(description='Your steam account has been linked')
				await ctx.author.add_roles(verified)
				await ctx.send(embed=embed)
			else:
				embed = discord.Embed(description='This is not a steamid64')
				await ctx.send(embed=embed)
				return
		else:
			embed = discord.Embed(description='This is not a steamid64')
			await ctx.send(embed=embed)
			return


@client.command()
async def newapilink(ctx):
	member = ctx.author
	message = ctx.message.content
	verified = discord.utils.get(ctx.guild.roles, name=f"Verified") 
	try:
		cmd, steamid64 = message.split(" ", 1)
	except Exception:
		embed = discord.Embed(description='Wrong format! format: .link (steamid64)')
		await ctx.send(embed=embed)
	verified = discord.utils.get(ctx.guild.roles, name=f"Verified")
	steamIdString = steamid64
	steamIdString_lowercase = steamIdString.lower()
	ifSteamId64 = steamIdString_lowercase.islower()
	if collection.count_documents({"SteamID":f"{steamid64}"}) > 0:
			embed = discord.Embed(description='This account is already linked')
			await ctx.send(embed=embed)
			return
	else:
		if ifSteamId64 == True:
			embed = discord.Embed(description='This is not an id64')
			await ctx.send(embed=embed)
			return
		else:
			try:
				user = await ctx.bot.client.fetch_user((int(steamid64)))
				post = {"DiscordName": f"{member.name}", "DiscordAvatar": f"{member.avatar_url}", "DiscordID": f"{member.id}", "DiscordCreationDate": f"{member.created_at}", "SteamName": f"{user.name}", "SteamProfileUrl": f"{user.profile_url}", "SteamID": f"{user.id64}", "SteamAvatar": f"{user.avatar_url}", "SteamCreatedAt": f"{user.created_at}"}
				collection.insert_one(post)
				embed = discord.Embed(description='Your steam account has been linked')
				await ctx.author.add_roles(verified)
				await ctx.send(embed=embed)
			except steamfront.errors.UserNotFound:
				embed = discord.Embed(description='Error! User not found, make sure the id64 is correct')
				await ctx.send(embed=embed)
				return

@client.command()
async def link(ctx):
	member = ctx.author
	message = ctx.message.content
	verified = discord.utils.get(ctx.guild.roles, name=f"Verified") 
	try:
		cmd, steamid64 = message.split(" ", 1)
	except Exception:
		embed = discord.Embed(description='Wrong format! format: .link (steamid64)')
		await ctx.send(embed=embed)
	verified = discord.utils.get(ctx.guild.roles, name=f"Verified")
	steamIdString = steamid64
	steamIdString_lowercase = steamIdString.lower()
	ifSteamId64 = steamIdString_lowercase.islower()
	if collection.count_documents({"SteamID":f"{steamid64}"}) > 0:
			embed = discord.Embed(description='This account is already linked')
			await ctx.send(embed=embed)
			return
	else:
		if ifSteamId64 == True:
			embed = discord.Embed(description='This is not an id64')
			await ctx.send(embed=embed)
			return
		else:
			try:
				user = steamfront.user.User(id64=f'{int(steamid64)}', apiKey='370271383631C9089D74EBA5806050F9')
				post = {"DiscordName": f"{member.name}", "DiscordAvatar": f"{member.avatar_url}", "DiscordID": f"{member.id}", "DiscordCreationDate": f"{member.created_at}", "SteamName": f"{user.name}", "SteamProfileUrl": f"{user.profile_url}", "SteamID": f"{user.id64}", "SteamAvatar": f"{user.avatar}"}
				collection.insert_one(post)
				embed = discord.Embed(description='Your steam account has been linked')
				await ctx.author.add_roles(verified)
				await ctx.send(embed=embed)
			except steamfront.errors.UserNotFound:
				embed = discord.Embed(description='Error! User not found, make sure the id64 is correct')
				await ctx.send(embed=embed)
				return

@client.command()
async def linkqweqwe(ctx):
	member = ctx.author
	message = ctx.message.content
	verified = discord.utils.get(ctx.guild.roles, name=f"Verified") 
	try:
		cmd, steamurl = message.split(" ", 1)
	except Exception:
		embed = discord.Embed(description='Wrong format')
		await ctx.send(embed=embed)
	verified = discord.utils.get(ctx.guild.roles, name=f"Verified")
	if collection.count_documents({"SteamProfileUrl":f"{steamurl}"}) > 0:
			embed = discord.Embed(description='This account is already linked')
			await ctx.send(embed=embed)
			return
	else:
		try:
			steamidgrabber = steam.steamid.steam64_from_url(steamurl, http_timeout=30)
			user = steamfront.user.User(id64=f'{steamidgrabber}', apiKey='370271383631C9089D74EBA5806050F9')
			post = {"DiscordName": f"{member.name}", "DiscordAvatar": f"{member.avatar_url}", "DiscordID": f"{member.id}", "DiscordCreationDate": f"{member.created_at}", "SteamName": f"{user.name}", "SteamProfileUrl": f"{user.profile_url}", "SteamID": f"{user.id64}", "SteamAvatar": f"{user.avatar}"}
			collection.insert_one(post)
			embed = discord.Embed(description='Your steam account has been linked')
			await ctx.author.add_roles(verified)
			await ctx.send(embed=embed)
		except Exception:
			embed = discord.Embed(description='Something went wrong / Steam link might not be invalid')
			await ctx.send(embed=embed)




client.run('ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.KO5zzXVpmAYKOhv11OvIS2xBOqI')
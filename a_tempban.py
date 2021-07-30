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
banCollection = db["EURT-Bans/Mutes"]
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
async def on_member_join(member):
	now = datetime.datetime.today()
	two_months_ago = now - datetime.timedelta(days=120)
	account_age = member.created_at
	guild = client.get_guild(810954832583852083)
	print(now, two_months_ago, account_age)
	verified = discord.utils.get(guild.roles, name=f"Verified")
	verified = discord.utils.get(guild.roles, name=f"Muted")
	if collection.count_documents({"DiscordID":f"{member.id}"}) > 0:
		await member.add_roles(verified)
	if banCollection.count_documents({"DiscordID":f"{member.id}"}) > 0:
		await member.add_roles(muted)
	if account_age > two_months_ago:
		botlogs = client.get_channel(822442461149790230)
		embed=discord.Embed(title=f"{member} might be an alt!")
		embed.add_field(name="User id:", value=f"```{member.id}```", inline=False)
		embed.add_field(name="User creation date:", value=f"```{member.created_at}```", inline=False)
		embed.set_footer(text="EU Rust Tournaments")
		await botlogs.send(embed=embed)
	else:
		return

@client.event
@commands.has_role('Staff')
async def ban(ctx):
	guild = client.get_guild(810954832583852083)
	banned = guild.get_role()
	try:
		cmd, user, timeAmount= ctx.message.content.split(" ", 1)
	except IndexError:
		embed = discord.Embed(description=f"Wrong format! format: .ban (user) (time_in_hours)")
		await ctx.send(embed=embed)
	unbanDate = datetime.datetime.now() - datetime.timedelta(hours=int(timeAmount))
	post = {"DiscordName": f"{ctx.message.mentions[0]}", "DiscordID": f"{ctx.message.mentions[0].id}", "bannedBy":f"{ctx.message.author}", "banTime": f"{timeAmount}", "unbanTime":f"{unbanDate}"}
	banCollection.insert_one(post)
	await ctx.message.mentions[0].add_roles(banned)
	await ctx.guild.ban(user=ctx.message.mentions[0])
	embed = discord.Embed(description=f"{user} has been banned til {unbanDate}")
	await ctx.send(embed=embed)
    
async def something():
	while True:
		guild = client.get_guild(810954832583852083)
		muted = guild.get_role(811700299597086750)
		for dbFind in banCollection.find():
			userId = dbFind["memberId"]
			user = client.get_user(int(userId))
			unbanTimeUnconverted = dbFind["unbanTime"]
			unbanTime = datetime.datetime.strptime(unbanTimeUnconverted)
			if unbanTime > datetime.datetime.now:
				return
			else:
				await guild.unban(user)
		for dbFind in banCollection.find():
			user = guild.get_member(int(userId))
			unmuteTime = dbFind["unmuteTime"]
			if unmuteTime > datetime.datetime.now:
				return
			else:
				await user.remove_roles(muted)
		await asyncio.sleep(1800)



client.run('ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.KO5zzXVpmAYKOhv11OvIS2xBOqI')

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
from datetime import timezone
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
verificationCollection = db["buy-inDatabase"]
wait = 0
	
#keys = await database.keys()
	#for key in keys:
	#	value = await database.get(key)
	#	print(key, value)

#Lav challonge matchboard acceptance med deres api
#Save alle profiles som mefix example så du ikke skal gøre det i en command()(ergo lav gem i databasen alt information om deres stem profile så det er nemt at fetch information), ergo det tager langt tid at søge hele  databasen og convert
#Remvork temove team cmd
#How to make EURC style accept to get in team(wait for message.mentions reaction)


@client.event
async def on_ready():
	client.loop.create_task(playingmembers())
	client.loop.create_task(signupboard())
	print('EURT bot online!')
	global database

@client.command()
@commands.has_role('Staff')
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
@commands.has_role('Staff')
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
		embed.set_footer(text=f"Requested by: {ctx.message.author}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(description='ID not in database')
		await ctx.send(embed=embed)
		return

@client.command()
@commands.has_role('Staff')
async def unlink(ctx):
	verified = discord.utils.get(ctx.guild.roles, name=f"Verified")
	try:
		user = ctx.message.mentions[0]
	except Exception:
		embed = discord.Embed(description='You need to mention a user')
		await ctx.send(embed=embed)
	try:
		for members in ctx.message.mentions:
			try:
				collection.delete_one({"DiscordName": f"{members.name}"})
				embed = discord.Embed(description=f'{members} has been removed from the database')
				await ctx.send(embed=embed)
				await members.remove_roles(verified)
			except Exception:
				embed = discord.Embed(description=f'{members} is not in database')
				await ctx.send(embed=embed)
	except Exception:
		embed = discord.Embed(description='You need to mention a user(s)')
		await ctx.send(embed=embed)

@client.event 
async def on_member_join(member):
	now = datetime.datetime.today()
	two_months_ago = now - datetime.timedelta(days=120)
	account_age = member.created_at
	guild = client.get_guild(810954832583852083)
	print(now, two_months_ago, account_age)
	verified = discord.utils.get(guild.roles, name=f"Verified")
	if collection.count_documents({"DiscordID":f"{member.id}"}) > 0:
		await member.add_roles(verified)
	if account_age > two_months_ago:
		botlogs = client.get_channel(822442461149790230)
		embed=discord.Embed(title=f"{member} might be an alt!")
		embed.add_field(name="User id:", value=f"```{member.id}```", inline=False)
		embed.add_field(name="User creation date:", value=f"```{member.created_at}```", inline=False)
		embed.set_footer(text="EU Rust Tournaments")
		await botlogs.send(embed=embed)
	else:
		return


@client.command()
@commands.has_role('Staff')
async def timer(ctx, time):
	message = ctx.message
	embed=discord.Embed(title=f"Countdown!")
	embed.add_field(name="Time till next event:", value=f"```---```", inline=False)
	embed.set_footer(text=f"EU Rust Tournaments")
	message = await ctx.send(embed=embed)
	await ctx.message.delete()
	Europe = timezone('Europe/Copenhagen')
	now = datetime.datetime.now(Europe)
	mtimeA = time
	mtimeB = mtimeA.split(":")
	hr = int(mtimeB[0])
	min = int(mtimeB[1])
	when_to_stop = int((timedelta(hours=24) - (now - now.replace(hour=hr, minute=min, second=0, microsecond=0))).total_seconds() % (24 * 3600))
	print(when_to_stop)
	while when_to_stop > 1:
		now = datetime.datetime.now(Europe)
		hr = int(mtimeB[0])
		min = int(mtimeB[1])
		when_to_stop = int((timedelta(hours=24) - (now - now.replace(hour=hr, minute=min, second=0, microsecond=0))).total_seconds() % (24 * 3600))
		m, s = divmod(when_to_stop, 60)
		h, m = divmod(m, 60)
		if when_to_stop > 65:
			time_lefth = str(h).zfill(2)
			time_leftm = str(m).zfill(2)
			embed=discord.Embed(title=f"Countdown!")
			embed.add_field(name="Time till next event:", value=f"```{time_lefth}h:{time_leftm}m```", inline=False)
			embed.set_footer(text=f"EU Rust Tournaments")
			await message.edit(embed=embed)
			await asyncio.sleep(60)
		else:
			time_left = str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
			embed=discord.Embed(title=f"Countdown!")
			embed.add_field(name="Time till next event:", value=f"```{time_left}```", inline=False)
			embed.set_footer(text=f"EU Rust Tournaments")
			await message.edit(embed=embed)
			await asyncio.sleep(2)
	embed=discord.Embed(title=f"Countdown!")
	embed.add_field(name="Time till next event:", value=f"```Event is now!```", inline=False)
	embed.set_footer(text=f"EU Rust Tournaments")
	await message.edit(embed=embed)


@client.command()
@commands.has_role('Staff')
async def giveaway(ctx, time):
	v = ctx.message.content
	try:
		x = v.replace(",", " ,")
		y = x.replace(", ", ",")
		time2, prize, link = y.split(",", 2)
		time = time2.replace(".giveaway ", "")
	except Exception: 
		embed = discord.Embed(description='Wrong format! .giveaway (time),(prize),(url to pic)')
		await ctx.send(embed=embed)
	now = datetime.datetime.now()
	when_to_stop = 20
	mtimeA = time
	mtimeB = mtimeA.split(":")
	hr = int(mtimeB[0])
	min = int(mtimeB[1])
	embed=discord.Embed(title="Giveaway!")
	embed.set_thumbnail(url=f"{link}")
	embed.add_field(name="Prize:", value=f"```---```", inline=False)
	embed.set_footer(text="React with 🎉 to enter!\nEU Rust Tournaments")
	message = await ctx.send(embed=embed)
	await message.add_reaction('🎉')
	await ctx.message.delete()
	while when_to_stop > 1:
		now = datetime.datetime.now()
		hr = int(mtimeB[0])
		min = int(mtimeB[1])
		when_to_stop = int((timedelta(hours=24) - (now - now.replace(hour=hr, minute=min, second=0, microsecond=0))).total_seconds() % (24 * 3600))
		m, s = divmod(when_to_stop, 60)
		h, m = divmod(m, 60)
		if when_to_stop > 65:
			time_lefth = str(h).zfill(2)
			time_leftm = str(m).zfill(2)
			print(time_lefth)
			embed=discord.Embed(title="Giveaway!")
			embed.set_thumbnail(url=f"{link}")
			embed.add_field(name="Prize:", value=f"```{prize}\nTime left: {time_lefth}h:{time_leftm}m```", inline=False)
			embed.set_footer(text="React with 🎉 to enter!\nEU Rust Tournaments")
			await message.edit(embed=embed)
			await asyncio.sleep(60)
		else:
			time_left = str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
			print(time_left)
			embed=discord.Embed(title="Giveaway!")
			embed.set_thumbnail(url=f"{link}")
			embed.add_field(name="Prize:", value=f"```{prize}\nTime left: {time_left}```", inline=False)
			embed.set_footer(text="React with 🎉 to enter!\nEU Rust Tournaments")
			await message.edit(embed=embed)
			await asyncio.sleep(2)
		try:
			print(time_left)
			print(when_to_stop)
		except Exception:
			pass
	msg = await ctx.channel.fetch_message(message.id)
	reactors = await msg.reactions[0].users().flatten()
	user = random.choice(reactors)
	embed=discord.Embed(title="Giveaway ended!")
	embed.set_thumbnail(url=f"{link}")
	embed.add_field(name="Winner:", value=f"```{user}```", inline=False)
	embed.set_footer(text="React with 🎉 to enter!\nEU Rust Tournaments")
	await msg.edit(embed=embed)
	await ctx.send(f'<@{user.id}>')
	return



@client.command()
@commands.has_role('Staff')
async def whois(ctx):
	user = ctx.message.mentions[0]
	if collection.count_documents({"DiscordName":f"{user.name}"}) > 0:
		for dbFind in collection.find({"DiscordName":f"{user.name}"}):
			steamid = dbFind["SteamProfileUrl"]
	else:
		steamid = "-No profile linked-"
		pass
	try:
		user = ctx.message.mentions[0]
	except Exception:
		embed = discord.Embed(description='Wrong format! .whois (@user)')
		await ctx.send(embed=embed)
	rolesname = []
	for role in user.roles:
		if role.name != "@everyone":
			rolesname.append(role.name)
	b = " | ".join(rolesname)
	embed=discord.Embed(title=f"{ctx.message.mentions[0]} info:")
	embed.add_field(name="Name/id:", value=f"```{user.name} | {user.id}```", inline=True)
	embed.add_field(name="Profile creation time:", value=f"```{user.created_at}```", inline=True)
	embed.add_field(name="Guild joined date:", value=f"```{user.joined_at}```", inline=True)
	embed.add_field(name="Member roles:", value=f"```{b}```", inline=True)
	embed.add_field(name="Steam profile:", value=f"```{steamid}```", inline=False)
	embed.set_footer(text=f"Requested by {ctx.message.author}\nEU Rust Tournaments")
	await ctx.send(embed=embed)

@client.command()
async def invites(ctx):
	top1 = 0
	top1inv = 0
	top2 = 0
	top2inv = 0
	top3 = 0
	top3inv = 0
	for i in await ctx.guild.invites():
		invite = i
		if invite.uses > top1:
			top1 = invite.uses
			top1inv = i.inviter
		else: 
			if invite.uses > top2:
				top2 = invite.uses
				top2inv = i.inviter
			else:
				if invite.uses > top3:
					top3 = invite.uses
					top3inv = i.inviter
				else:
					pass
	embed=discord.Embed(title="Top inviters!")
	embed.add_field(name="1st:", value=f"```{top1inv} with {top1} invites!```", inline=False)
	embed.add_field(name="2nd:", value=f"```{top2inv} with {top2} invites!```", inline=False)
	embed.add_field(name="3rd:", value=f"```{top3inv} with {top3} invites!```", inline=False)
	embed.set_footer(text="EU Rust Tournaments")
	await ctx.send(embed=embed)


@client.command()
@commands.has_role('Staff')
async def removeteam(ctx):
	x = ctx.message.content 
	guild = client.get_guild(810954832583852083)
	try:
		y = x.split(" ", 2)
	except Exception:
		embed=discord.Embed(description='Wrong format! .removeteam (team number) (reason)')
		await ctx.send(embed=embed)
	team1string = y[1]
	team1string_lowercase = team1string.lower()
	team1contains_letters = team1string_lowercase.islower()	
	if team1contains_letters == False:
		removalTeam = discord.utils.get(guild.roles, name=f"Team {y[1]}")
		signedRole = discord.utils.get(guild.roles, name=f"Signed")
		for member in removalTeam.members:
			await member.remove_roles(removalTeam)
			await member.remove_roles(signedRole)
		embed = discord.Embed(description=f'Team {y[1]} has been removed')
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(description=f'Team needs to be a number(eg. 1-64)')
		await ctx.send(embed=embed)

@client.command()
@commands.has_role('Staff')
async def switch(ctx):
	checker = 0
	x = ctx.message.content
	try:
		cmd, team1, team2 = x.split(" ", 3)
	except Exception:
		embed = discord.Embed(description=f'Wrong format! .switch (team number1) (team number2)')
		await ctx.send(embed=embed)
	team1string = team1
	team1string_lowercase = team1string.lower()
	team1contains_letters = team1string_lowercase.islower()	
	team2string = team2
	team2string_lowercase = team2string.lower()
	team2contains_letters = team2string_lowercase.islower()
	print(team2contains_letters)
	print(team1contains_letters)
	guild = client.get_guild(810954832583852083)
	if team1contains_letters == False:
		if team2contains_letters == False:
			tee1 = discord.utils.get(guild.roles, name=f"Team {team1}")
			tee2 = discord.utils.get(guild.roles, name=f"Team {team2}")
			print(tee1, tee2)
			member2 = tee2.members
			member3 = tee1.members
			for member in member3:
				await member.remove_roles(tee1)
				await member.add_roles(tee2)
			for member in member2: 
				await member.remove_roles(tee2)
				await member.add_roles(tee1)
		else:
			embed = discord.Embed(description=f'Wrong format! .switch (team number1) (team number2)')
			await ctx.send(embed=embed)
	else:
		embed = discord.Embed(description=f'Wrong format! .switch (team number1) (team number2)')
		await ctx.send(embed=embed)

@client.event
async def on_message_delete(message):
	try:
		embed=discord.Embed(title='**Message Deleted**',description="", color=0x000000)
		embed.add_field(name='Content:', value=message.content, inline=False)
		embed.add_field(name='Channel:', value=f'{message.channel.name}')
		embed.set_footer(text=str(message.author.display_name))
		channel = client.get_channel(820640810986373140)
		await channel.send(embed=embed)
		return
	except Exception:
		print('Deleted message logging passed!')
		
@client.event 
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		if ctx.message.author == 816700983899848735:
			embed = discord.Embed(description=f'Command not found. Make sure your using the right format')
			await ctx.send(embed=embed)

@client.command()
@commands.has_role('Server moderator')
async def tlimit(ctx):
	print('Tlimiter recognized')
	tlimit = open("tlimit.txt", "w")
	try:
		x = ctx.message.content 
		cmd, num = x.split(" ",2)
		print('1')
	except SyntaxError:
		await ctx.send('```Something went wrong!```')
	a_string = num
	a_string_lowercase = a_string.lower()
	contains_letters = a_string_lowercase.islower()	
	print('2')
	if contains_letters == True:
		embed = discord.Embed(description=f'Team limit can only be set to a number!')
		await ctx.send(embed=embed)
	else:
		tlimit.write(num)
		embed = discord.Embed(description=f'Team limit has been set to {num}!')
		await ctx.send(embed=embed)

@client.command()
@commands.has_role('Server moderator')
async def payedtlimit(ctx):
	print('Tlimiter recognized')
	tlimit = open("payed_tlimit.txt", "w")
	try:
		x = ctx.message.content 
		cmd, num = x.split(" ",2)
		print('1')
	except SyntaxError:
		await ctx.send('```Something went wrong!```')
	a_string = num
	a_string_lowercase = a_string.lower()
	contains_letters = a_string_lowercase.islower()	
	print('2')
	if contains_letters == True:
		embed = discord.Embed(description=f'Team limit can only be set to a number!')
		await ctx.send(embed=embed)
	else:
		tlimit.write(num)
		embed = discord.Embed(description=f'Team limit has been set to {num}!')
		await ctx.send(embed=embed)


@client.command(name='clear')
@commands.has_permissions(ban_members=True, kick_members=True)
async def clear(ctx, amount = 5):
	await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_role('Server moderator')
async def status(ctx):
	print(ctx.message.content)
	x = ctx.message.content
	a,b = x.split(".status ")
	file2 = open('status.txt', 'w')
	file2.write(b)
	embed = discord.Embed(description=f'Status has been changed to {b}')
	await ctx.send(embed=embed)

@client.command()
async def signup(ctx):
	if "signup" in ctx.message.channel.name:
		if "-" in ctx.message.content:	
			global team_limit
			if ctx.message.channel.id == 811690381590790215:
				tl = open("tlimit.txt", "r")
				team_limit = tl.read()
			elif ctx.message.channel.id == 832269492582612992:
				tl = open("payed_tlimit.txt", "r")
				team_limit = tl.read()
			string = ctx.message.content
			substring = "@"
			count = string.count(substring)
			sb = open("substring.txt", "w")
			sb.write(f"{count}")
			sb.close()
			sb2 = open("substring.txt", "r")
			guild = client.get_guild(810954832583852083)
			tee1 = discord.utils.get(guild.roles, name="Signed")
			banned = discord.utils.get(guild.roles, name="Tournament banned")
			mentions = ""
			msg = ctx.message
			try:
				x = ctx.message.content
				cmd, user1 = x.split("-", 2)
			except Exception:
				embed = discord.Embed(description=f'Error! Remove subs/make sure you only @ enough members')
				await ctx.send(embed=embed)
				return
			a_string = user1
			a_string_lowercase = a_string.lower()
			contains_letters = a_string_lowercase.islower()	
			count2 = sb2.read()
			if ctx.message.author in ctx.message.mentions:
				for mention in msg.mentions:
					mentions = mentions + " " + mention.mention
				for mention in msg.mentions:
					member = mention
					if tee1 in member.roles:
						embed = discord.Embed(description=f'{member} is already in a team!')
						await ctx.send(embed=embed)
						return
					else:
						if banned in member.roles:
							embed = discord.Embed(description=f'{member} is Tournament banned!')
							await ctx.send(embed=embed)
							return
						else:
							pass
				if contains_letters == False:
					if ctx.message.channel.id == 811690381590790215:
						signup = client.get_channel(812836000228311125)
						if count2 == team_limit:
							add_reaction_msg = await signup.send(f'***{ctx.message.author}({ctx.message.author.id}) has applied! \nTeam: {user1}***')
							embed = discord.Embed(description=f'Succes! The bot will dm you when staff has approved your team!')
							await add_reaction_msg.add_reaction("✅")
							await add_reaction_msg.add_reaction("❎")
							await ctx.send(embed=embed)
						else:
							embed = discord.Embed(description=f'Error! Too many/not enough users tagged, do not @ more/less than {team_limit} members')
							await ctx.send(embed=embed)
					elif ctx.message.channel.id == 832269492582612992:
						signup = client.get_channel(834439221615001660)
						if count2 == team_limit:
							add_reaction_msg = await signup.send(f'***{ctx.message.author}({ctx.message.author.id}) has applied for buy-in tournament! \nTeam: {user1}***') # Insert new signup accept channel
							embed = discord.Embed(description=f'Succes! The bot will dm you when staff has approved your team!\n React with 💰 when your ready to pay, this needs to be done, otherwise your team wont be accepted')
							reactEmbed = await ctx.send(embed=embed)
							post = {"DiscordId":f"{ctx.message.author.id}", "ReactEmbedId": f"{reactEmbed.id}"}
							verificationCollection.insert_one(post)
							await add_reaction_msg.add_reaction("✅")
							await add_reaction_msg.add_reaction("❎")
							await reactEmbed.add_reaction("💰")
						else:
							embed = discord.Embed(description=f'Error! Too many/not enough users tagged, do not @ more/less than {team_limit} members')
							await ctx.send(embed=embed)
				else:
					embed = discord.Embed(description=f'Error! Make sure to @ all your members/remove subs from your sign-up message')
					await ctx.send(embed=embed)
					return
			else:
				embed = discord.Embed(description=f'Error! {member} You need to be in the team your trying to sign up!')
				await ctx.send(embed=embed)
				return
		else:
			if ctx.message.author.id == 816700983899848735:
				return
			else:
				embed = discord.Embed(description=f'Wrong format! .signup - @member1@member2@member3....')
				await ctx.send(embed=embed)

	
@client.event
async def on_message(message):
	await client.process_commands(message)
	if message.author.id == 816700983899848735:
		return 
	else:
		try:
			embed=discord.Embed(title='**Message sent**',description="", color=0x000000)
			embed.add_field(name='Content:', value=f"{message.content}", inline=False)
			embed.add_field(name='Channel:', value=f'{message.channel.name}')
			embed.set_footer(text=str(message.author.display_name))
			channel = client.get_channel(820640810986373140)
			await channel.send(embed=embed)
			return
		except Exception:
			pass


@client.command()
@commands.has_role('Server moderator')
async def memberc(ctx):
	guild = client.get_guild('810954832583852083')
	print(ctx.guild.member_count)
	cointer = ctx.guild.member_count
	cointer -=1
	print(cointer)

@client.command()
@commands.has_role('Staff')
async def say(ctx, channel: discord.TextChannel, *, msg):
	await ctx.send('Succesful!')
	await channel.send(f'{msg}')

wait = 0



@client.command()
async def sub(ctx):
	x = ctx.message.content
	command, message5 = x.split("sub", 2)
	print(message5)
	a_string = message5
	a_string_lowercase = a_string.lower()
	contains_letters = a_string_lowercase.islower()
	turneybanned = discord.utils.get(ctx.guild.roles, name="Tournament banned")
	print(contains_letters)
	if contains_letters == False:
		for member in ctx.message.mentions:
			if turneybanned in member.roles:
				embed = discord.Embed(description=f'Error! {member} is tournament banned!')
				await ctx.send(embed=embed)
				return
			else:
				pass
		try:
			member = ctx.message.author
			member1 = ctx.message.mentions[0]
			member2 = ctx.message.mentions[1]
		except IndexError:
			signupc = client.get_channel(817972037057511454)
			embed = discord.Embed(description=f'Wrong format! .sub - @user + @user')
			await ctx.send(embed=embed)
			return
		for h in range(1,66):
			print(h)
			te1 = discord.utils.get(ctx.guild.roles, name=f"Team {h}")
			if te1 in member.roles:
				Signed = discord.utils.get(ctx.guild.roles, name="Signed")
				await member1.remove_roles(te1)
				await member2.add_roles(te1)
				await member1.remove_roles(Signed)
				await member2.add_roles(Signed)
				embed = discord.Embed(description=f'You have subbed: - {ctx.message.mentions[0]} + {ctx.message.mentions[1]}')
				await ctx.send(embed=embed)
				return
			else:
				pass
		signupc = client.get_channel(817972037057511454)
		embed = discord.Embed(description=f'Team error! You need to be in a team/the right team!')
		await ctx.send(embed=embed)
		return
	else:
		print('Geuss this worked')
		signupc = client.get_channel(817972037057511454)
		embed = discord.Embed(description=f'Wrong format! Make sure that you @ the members your trying sub!')
		await ctx.send(embed=embed)
		return

@client.event
async def on_raw_reaction_add(payload):
	guild = client.get_guild(payload.guild_id)
	access = discord.utils.get(guild.roles, name="Server moderator")
	msg = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
	channel = client.get_channel(payload.channel_id)
	if channel.name.startswith("team-accept"):
		if payload.user_id == 816700983899848735:
			return
		else:
			if payload.emoji.name == "✅":
				global wait
				x = msg.content 
				start = "("
				end = ")"
				userIdStr = ((x.split(start))[1].split(end)[0])
				userId = int(userIdStr)
				mentions = ""
				dmUser = guild.get_member(userId)
				a, b = x.split(":", 2)
				c = b.replace("*","")
				Signed = discord.utils.get(guild.roles, name="Signed")
				accept = client.get_channel(812836000228311125)
				if wait == 0:
					wait = 1
					for x in range(1, 65):
						t1 = f't{x}.txt'
						if os.stat(t1).st_size == 0:
							tee1 = discord.utils.get(guild.roles, name=f"Team {x}")
							for mention in msg.mentions:
								await mention.add_roles(tee1)
								await mention.add_roles(Signed)
							try:
								channel2 = await dmUser.create_dm()
								embed=discord.Embed(title="Your team has been accepted!", color=0x0040ff)
								embed.add_field(name="Your team:", value=f"{c}", inline=False)
								embed.add_field(name="Accepted by:", value=f"{payload.member}", inline=False)
								embed.set_footer(text="EU Rust Tournaments")
								await channel2.send(embed=embed)
							except Exception:
								print('Passed!')
								pass
							client.loop.create_task(checker())
							break
						else:
							pass
				else:
					embed = discord.Embed(description=f'Im proccessing previous commands')
					await accept.send(embed=embed)
					await msg.remove_reaction(emoji=payload.emoji,member=payload.member)
					return																															
			if payload.emoji.name == "❎":
				mentions = ""
				x = msg.content
				start = "("
				end = ")"
				userIdStr = ((x.split(start))[1].split(end)[0])
				userId = int(userIdStr)
				dmUser = guild.get_member(userId)
				try:
					channel2 = await dmUser.create_dm()
					embed=discord.Embed(title="Your team has been denied!")
					embed.add_field(name="What to do now?:", value="Contact the staff member who denied your team", inline=False)
					embed.add_field(name="Denied by:", value=f"{payload.member}", inline=False)
					embed.set_footer(text="EU Rust Tournaments")
					await channel2.send(embed=embed)
				except Exception:
					print('Passed!')
					pass
				await msg.delete()
				return				
	if payload.channel_id == 817913002120314930:
		if payload.emoji.name == "♻️":
			if access in payload.member.roles:
				normal_signups = await guild.get_channel(811690381590790215)
				buyin_signups = await guild.get_channel(832269492582612992)
				normal_substitutions = await guild.get_channel(817972037057511454)
				buyin_substitutions = await guild.get_channel(832269645464731668)
				normal_scorechannel = await guild.get_channel(812322092023808010)
				buyin_scorechannel = await guild.get_channel(832269776800710737)
				normal_teamaccept = await guild.get_channel(812836000228311125)
				buyin_teamaccept = await guild.get_channel(834439221615001660)
				signed = discord.utils.get(guild.roles, name="Signed")
				guild = client.get_guild(payload.guild_id)
				amount = 400
				await normal_signups.purge(limit=amount)
				await buyin_signups.purge(limit=amount)
				await normal_substitutions.purge(limit=amount)
				await buyin_substitutions.purge(limit=amount)
				await normal_scorechannel.purge(limit=amount)
				await buyin_scorechannel.purge(limit=amount)
				await normal_teamaccept.purge(limit=amount)
				await buyin_teamaccept.purge(limit=amount)
				for y in range(1, 65):
					team = discord.utils.get(guild.roles, name=f"Team {y}")
					signed = discord.utils.get(guild.roles, name=f"Signed")
					for member in team.members:
						await member.remove_roles(team)
						await member.remove_roles(signed)
					await asyncio.sleep(1)
				for x in range(1,65):
					team = discord.utils.get(guild.roles, name=f"Buy-in Team {y}")
					signed = discord.utils.get(guild.roles, name=f"Signed")
					for member in team.members:
						await member.remove_roles(team)
						await member.remove_roles(signed)
					await asyncio.sleep(1)
				await msg.remove_reaction(emoji=payload.emoji,member=payload.member)
				return
		else:
			await msg.remove_reaction(emoji=payload.emoji,member=payload.member)
			return
	if payload.channel_id == 827182673457446932:
		member = payload.member
		Voted = discord.utils.get(guild.roles, name="Voted")
		await member.add_roles(Voted)
	payloadChannel = client.get_channel(payload.channel_id)
	guild = client.get_guild(810954832583852083)
	if payload.emoji.name == "📩":
		ticketCategory = discord.utils.get(guild.categories, id=832599966953766922)
		if payload.channel_id == 830523406348845066:
			userMention = f'<@{payload.member.id}>'
			requestSupportChannel = client.get_channel(830523406348845066)
			requestSupportMessage = await requestSupportChannel.fetch_message(830526877566763058) #Put id in
			for channel in ticketCategory.channels:
				userName = payload.member.name
				try:
					channelNameSplit = channel.name
					ticket, name = channelNameSplit.split("-", 1)
					if userName.lower() == name:
						await channel.send(userMention)
						embed = discord.Embed(description='You need to close this ticket to open another one!')
						await channel.send(embed=embed)
						await requestSupportMessage.remove_reaction(emoji=payload.emoji,member=payload.member)
						return
					else:
						pass
				except ValueError:
					pass
			verified = discord.utils.get(guild.roles, name=f"Verified")
			everyone = discord.utils.get(guild.roles, name=f"@everyone")
			staff = discord.utils.get(guild.roles, name="Staff")
			embed = discord.Embed(title='EURT Support', description=f"A {staff.mention} member will be with you shortly")
			embed.add_field(name="\nClosing the ticket", value="To close the ticket react with 🔒 and then ✅", inline=False)
			embed.set_footer(text='EU Rust Tournaments', icon_url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
			ticketChannel = await guild.create_text_channel(name=f'ticket-{payload.member.name}', category=ticketCategory)
			ticketEmbed = await ticketChannel.send(embed=embed)
			await ticketEmbed.add_reaction("🔒")
			await ticketChannel.set_permissions(verified, view_channel=False)
			await ticketChannel.set_permissions(everyone, view_channel=False)
			await ticketChannel.set_permissions(payload.member, view_channel=True)
			await requestSupportMessage.remove_reaction(emoji=payload.emoji,member=payload.member)
	if payload.emoji.name == "💰":
		if payload.member.id == 816700983899848735:
			return
		else:
			payloadMessage = await payloadChannel.fetch_message(payload.message_id)
			if verificationCollection.count_documents({"DiscordId":f"{payload.member.id}", "ReactEmbedId":f"{payloadMessage.id}"}) > 0:
				payloadChannel = client.get_channel(payload.channel_id)
				if payload.channel_id == 832269492582612992:
					userMention = f'<@{payload.member.id}>'
					requestSupportChannel = client.get_channel(830523406348845066)
					requestSupportMessage = await requestSupportChannel.fetch_message(830526877566763058)
					guild = client.get_guild(810954832583852083)
					buyinCategory = discord.utils.get(guild.categories, id=832601089936326666) #Put id in
					for channel in buyinCategory.channels:
						userName = payload.member.name
						try:
							channelNameSplit = channel.name
							ticket, name = channelNameSplit.split("-", 1)
							if userName.lower() == name:
								await channel.send(userMention)
								embed = discord.Embed(description='You need to close this ticket to open another one!')
								await channel.send(embed=embed)
								await requestSupportMessage.remove_reaction(emoji=payload.emoji,member=payload.member)
								return
							else:
								pass
						except ValueError:
							pass
					verified = discord.utils.get(guild.roles, name=f"Verified")
					everyone = discord.utils.get(guild.roles, name=f"@everyone")
					staff = discord.utils.get(guild.roles, name="Staff")
					embed = discord.Embed(title='EURT Payment', description=f"A {staff.mention} member will be with you shortly")
					embed.add_field(name="\nClosing the ticket", value="To close the ticket react with 🔒 and then ✅", inline=False)
					embed.set_footer(text='EU Rust Tournaments', icon_url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
					ticketChannel = await guild.create_text_channel(name=f'ticket-{payload.member.name}', category=buyinCategory)
					ticketEmbed = await ticketChannel.send(embed=embed)
					await ticketEmbed.add_reaction("🔒")
					await ticketChannel.set_permissions(verified, view_channel=False)
					await ticketChannel.set_permissions(everyone, view_channel=False)
					await ticketChannel.set_permissions(payload.member, view_channel=True)
					await requestSupportMessage.remove_reaction(emoji=payload.emoji,member=payload.member)
					return
			else:
				await payloadMessage.remove_reaction(emoji=payload.emoji,member=payload.member)
				return
	if payloadChannel.name.startswith("ticket"):
		if payload.emoji.name == "🔒":
			if payload.member.id == 816700983899848735:
				return
			else:
				embed = discord.Embed()
				embed = discord.Embed(description='React with ✅ below to close ticket')
				confirmMessage = await payloadChannel.send(embed=embed)
				await confirmMessage.add_reaction("✅")
		elif payload.emoji.name == "✅":
			if payload.member.id == 816700983899848735:
				return
			else:
				embed = discord.Embed(description='Ticket will close in 5 seconds')
				await payloadChannel.send(embed=embed)
				limit = None
				conversationUsers = []
				async for message in payloadChannel.history(limit=None):
					if message.author.id in conversationUsers or message.author.id == 816700983899848735:
						pass
					else:
						conversationUsers.append(message.author.id)
				transcript = await chat_exporter.export(payloadChannel, limit)
				transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"transcript-{payloadChannel.name}.html")
				transcriptChannel = client.get_channel(835214538004889600)
				embed = discord.Embed(title=f'{payloadChannel.name} closed', description=f"Ticket was closed by {payload.member}", timestamp=datetime.datetime.now())
				embed.set_footer(text=f"EURT",icon_url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
				for memberid in conversationUsers:
					dmUser = guild.get_member(memberid)
					dmChannel = await dmUser.create_dm()
					await dmChannel.send(embed=embed, file=transcript_file)
				await transcriptChannel.send(embed=embed)
				await payloadChannel.delete()

#DO NOT TOUCH // SIGNUP SECTION

async def statuschanger():
	while True:
		guild = client.get_guild(810954832583852083)
		statusfile = open('status.txt', 'r')
		status = statusfile.read()
		tei = discord.utils.get(guild.roles, name="🏆Current winner")
		if tei.members == []:
			await client.change_presence(status=discord.Status.idle, activity=discord.Game(f'Developed by ELON'))
			await asyncio.sleep(300)
		else:
			for member in tei.members:
				await client.change_presence(status=discord.Status.idle, activity=discord.Game(f'{status}'))
				await asyncio.sleep(4)
				await client.change_presence(status=discord.Status.idle, activity=discord.Game(f'{member.name}'))
				await asyncio.sleep(4)

async def playingmembers():
	while(True):
		guild = client.get_guild(810954832583852083)
		signed = discord.utils.get(guild.roles, name="Signed")
		for b in range(1,66):
			try:
				t1 = open(f"t{b}.txt", "w", encoding='utf-8')
				te1 = discord.utils.get(guild.roles, name=f"Team {b}")
				for member in te1.members:
					t1.write(f'{member.name} \n')	
			except Exception:
				pass
		await asyncio.sleep(300)

async def checker():
	while(True):
		global wait
		guild = client.get_guild(810954832583852083)
		signed = discord.utils.get(guild.roles, name="Signed")
		for b in range(1,66):
			try:
				t1 = open(f"t{b}.txt", "w", encoding='utf-8')
				te1 = discord.utils.get(guild.roles, name=f"Team {b}")
				for member in te1.members:
					t1.write(f'{member.name} \n')
			except Exception:
				pass
		await asyncio.sleep(2)
		wait = 0
		break 

async def signupboard():
	while(True):
		t1 = open("t1.txt", "r", encoding='utf-8')
		t2 = open("t2.txt", "r", encoding='utf-8')
		t3 = open("t3.txt", "r", encoding='utf-8')
		t4 = open("t4.txt", "r", encoding='utf-8')
		t5 = open("t5.txt", "r", encoding='utf-8')
		t6 = open("t6.txt", "r", encoding='utf-8')
		t7 = open("t7.txt", "r", encoding='utf-8')
		t8 = open("t8.txt", "r", encoding='utf-8')
		t9 = open("t9.txt", "r", encoding='utf-8')
		t10 = open("t10.txt", "r", encoding='utf-8')
		t11 = open("t11.txt", "r", encoding='utf-8')
		t12 = open("t12.txt", "r", encoding='utf-8')
		t13 = open("t13.txt", "r", encoding='utf-8')
		t14 = open("t14.txt", "r", encoding='utf-8')
		t15 = open("t15.txt", "r", encoding='utf-8')
		t16 = open("t16.txt", "r", encoding='utf-8')
		t17 = open("t17.txt", "r", encoding='utf-8')
		t18 = open("t18.txt", "r", encoding='utf-8')
		t19 = open("t19.txt", "r", encoding='utf-8')
		t20 = open("t20.txt", "r", encoding='utf-8')
		t21 = open("t21.txt", "r", encoding='utf-8')
		t22 = open("t22.txt", "r", encoding='utf-8')
		t23 = open("t23.txt", "r", encoding='utf-8')
		t24 = open("t24.txt", "r", encoding='utf-8')
		t25 = open("t25.txt", "r", encoding='utf-8')
		t26 = open("t26.txt", "r", encoding='utf-8')
		t27 = open("t27.txt", "r", encoding='utf-8')
		t28 = open("t28.txt", "r", encoding='utf-8')
		t29 = open("t29.txt", "r", encoding='utf-8')
		t30 = open("t30.txt", "r", encoding='utf-8')
		t31 = open("t31.txt", "r", encoding='utf-8')
		t32 = open("t32.txt", "r", encoding='utf-8')
		t33 = open("t33.txt", "r", encoding='utf-8')
		t34 = open("t34.txt", "r", encoding='utf-8')
		t35 = open("t35.txt", "r", encoding='utf-8')
		t36 = open("t36.txt", "r", encoding='utf-8')
		t37 = open("t37.txt", "r", encoding='utf-8')
		t38 = open("t38.txt", "r", encoding='utf-8')
		t39 = open("t39.txt", "r", encoding='utf-8')
		t40 = open("t40.txt", "r", encoding='utf-8')
		t41 = open("t41.txt", "r", encoding='utf-8')
		t42 = open("t42.txt", "r", encoding='utf-8')
		t43 = open("t43.txt", "r", encoding='utf-8')
		t44 = open("t44.txt", "r", encoding='utf-8')
		t45 = open("t45.txt", "r", encoding='utf-8')
		t46 = open("t46.txt", "r", encoding='utf-8')
		t47 = open("t47.txt", "r", encoding='utf-8')
		t48 = open("t48.txt", "r", encoding='utf-8')
		t49 = open("t49.txt", "r", encoding='utf-8')
		t50 = open("t50.txt", "r", encoding='utf-8')
		t51 = open("t51.txt", "r", encoding='utf-8')
		t52 = open("t52.txt", "r", encoding='utf-8')
		t53 = open("t53.txt", "r", encoding='utf-8')
		t54 = open("t54.txt", "r", encoding='utf-8')
		t55 = open("t55.txt", "r", encoding='utf-8')
		t56 = open("t56.txt", "r", encoding='utf-8')
		t57 = open("t57.txt", "r", encoding='utf-8')
		t58 = open("t58.txt", "r", encoding='utf-8')
		t59 = open("t59.txt", "r", encoding='utf-8')
		t60 = open("t60.txt", "r", encoding='utf-8')
		t61 = open("t61.txt", "r", encoding='utf-8')
		t62 = open("t62.txt", "r", encoding='utf-8')
		t63 = open("t63.txt", "r", encoding='utf-8')
		t64 = open("t64.txt", "r", encoding='utf-8')
		te1 = t1.read()
		te2 = t2.read()
		te3 = t3.read()
		te4 = t4.read()
		te5 = t5.read()
		te6 = t6.read()
		te7 = t7.read()
		te8 = t8.read()
		te9 = t9.read()
		te10 = t10.read()
		te11 = t11.read()
		te12 = t12.read()
		te13 = t13.read()
		te14 = t14.read()
		te15 = t15.read()
		te16 = t16.read()
		te17 = t17.read()
		te18 = t18.read()
		te19 = t19.read()
		te20 = t20.read()
		te21 = t21.read()
		te22 = t22.read()
		te23 = t23.read()
		te24 = t24.read()
		te25 = t25.read()
		te26 = t26.read()
		te27 = t27.read()
		te28 = t28.read()
		te29 = t29.read()
		te30 = t30.read()
		te31 = t31.read()
		te32 = t32.read()
		te33 = t33.read()
		te34 = t34.read()
		te35 = t35.read()
		te36 = t36.read()
		te37 = t37.read()
		te38 = t38.read()
		te39 = t39.read()
		te40 = t40.read()
		te41 = t41.read()
		te42 = t42.read()
		te43 = t43.read()
		te44 = t44.read()
		te45 = t45.read()
		te46 = t46.read()
		te47 = t47.read()
		te48 = t48.read()
		te49 = t49.read()
		te50 = t50.read()
		te51 = t51.read()
		te52 = t52.read()
		te53 = t53.read()
		te54 = t54.read()
		te55 = t55.read()
		te56 = t56.read()
		te57 = t57.read()
		te58 = t58.read()
		te59 = t59.read()
		te60 = t60.read()
		te61 = t61.read()
		te62 = t62.read()
		te63 = t63.read()
		te64 = t64.read()
		channel = client.get_channel(817559338797367316)
		message = await channel.fetch_message(817845320942747689)
		message2 = await channel.fetch_message(819127805228220417)
		message3 = await channel.fetch_message(819660877828587581)
		message4 = await channel.fetch_message(819666986052091904)
		message5 = await channel.fetch_message(820658647993548841)
		message6 = await channel.fetch_message(820668025786466336)
		await message6.edit(content=f'```---Team 49--- \n{te49}```\n```---Team 50--- \n{te50}```\n```---Team 51--- \n{te51}```\n```---Team 52--- \n{te52}```\n```---Team 53--- \n{te53}```\n```---Team 54--- \n{te54}```\n```---Team 55--- \n{te55}```\n```---Team 56--- \n{te56}```\n```---Team 57--- \n{te57}```\n```---Team 58--- \n{te58}```\n```---Team 59--- \n{te59}```\n```---Team 60--- \n{te60}```\n```---Team 61--- \n{te61}```\n```---Team 62--- \n{te62}```\n```---Team 63--- \n{te63}```\n```---Team 64--- \n{te64}```')
		await message5.edit(content=f'```---Team 33--- \n{te33}```\n```---Team 34--- \n{te34}```\n```---Team 35--- \n{te35}```\n```---Team 36--- \n{te36}```\n```---Team 37--- \n{te37}```\n```---Team 38--- \n{te38}```\n```---Team 39--- \n{te39}```\n```---Team 40--- \n{te40}```\n```---Team 41--- \n{te41}```\n```---Team 42--- \n{te42}```\n```---Team 43--- \n{te43}```\n```---Team 44--- \n{te44}```\n```---Team 45--- \n{te45}```\n```---Team 46--- \n{te46}```\n```---Team 47--- \n{te47}```\n```---Team 48--- \n{te48}```')
		await message4.edit(content=f'```---Team 25--- \n{te25}```\n```---Team 26--- \n{te26}```\n```---Team 27--- \n{te27}```\n```---Team 28--- \n{te28}```\n```---Team 29--- \n{te29}```\n```---Team 30--- \n{te30}```\n```---Team 31--- \n{te31}```\n```---Team 32--- \n{te32}```')
		await message3.edit(content=f'```---Team 17--- \n{te17}```\n```---Team 18--- \n{te18}```\n```---Team 19--- \n{te19}```\n```---Team 20--- \n{te20}```\n```---Team 21--- \n{te21}```\n```---Team 22--- \n{te22}```\n```---Team 23--- \n{te23}```\n```---Team 24--- \n{te24}```')
		await message2.edit(content=f'```---Team 9--- \n{te9}```\n```---Team 10--- \n{te10}```\n```---Team 11--- \n{te11}```\n```---Team 12--- \n{te12}```\n```---Team 13--- \n{te13}```\n```---Team 14--- \n{te14}```\n```---Team 15--- \n{te15}```\n```---Team 16--- \n{te16}```')
		await message.edit(content=f'```---Team 1--- \n{te1}```\n```---Team 2--- \n{te2}```\n```---Team 3--- \n{te3}```\n```---Team 4--- \n{te4}```\n```---Team 5--- \n{te5}```\n```---Team 6--- \n{te6}```\n```---Team 7--- \n{te7}```\n```---Team 8--- \n{te8}```')
		await asyncio.sleep(305)

#message. (team 1 (team 1.txt) /n)

#lav en anden auto process som opdaterer hver minut

client.run('ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.KO5zzXVpmAYKOhv11OvIS2xBOqI')
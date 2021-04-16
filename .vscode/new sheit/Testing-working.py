import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from discord.ext.commands import has_permissions, MissingPermissions
import json
import time
import os
import youtube_dl
import random
import datetime
from discord.ext.commands import CommandNotFound

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)

wait = 0

@client.event
async def on_ready():
	print('EURT bot online!')
	global wait 
	client.loop.create_task(tlmittcounter())
	client.loop.create_task(statuschanger())
	client.loop.create_task(playingmembers())
	client.loop.create_task(signupboard())



@client.command()
@commands.has_role('Staff')
async def timer(ctx):
	message = ctx.message
	embed=discord.Embed(title=f"Countdown!")
	embed.add_field(name="Time till next event:", value=f"```---```", inline=False)
	embed.set_footer(text=f"EU Rust Tournaments")
	msg = await ctx.channel.send(embed=embed)
	await message.delete()
	x = ctx.message.content
	try:
		cmd, time = x.split(" ", 1)
		when_to_stop = int(time)
	except IndexError:
		embed=discord.Embed(title="Wrong format!")
		embed.add_field(name="Format:", value="```.timer (time)```", inline=False)
		embed.set_footer(text="EU Rust Tournaments")
		await ctx.send(embed=embed)
	while True:
		while when_to_stop > -1:
			m, s = divmod(when_to_stop, 60)
			h, m = divmod(m, 60)
			time_left = str(h).zfill(2) + ":" + str(m).zfill(2)
			embed=discord.Embed(title=f"Countdown!")
			embed.add_field(name="Time till next event:", value=f"```{time_left}```", inline=False)
			embed.set_footer(text=f"Hour(s) : Minutes(s)\nEU Rust Tournaments")
			await msg.edit(embed=embed)
			print(time_left + "\r", end="")
			await asyncio.sleep(60)
			when_to_stop -= 60
		embed=discord.Embed(title=f"Countdown!")
		embed.add_field(name="Time till next event:", value=f"```Event is now!```", inline=False)
		embed.set_footer(text=f"EU Rust Tournaments")
		await msg.edit(embed=embed)




@client.command()
@commands.has_role('Staff')
async def giveaway(ctx):
	if ctx.message.author == 816700983899848735:
		return
	else:
		v = ctx.message.content
		channel = client.get_channel(813163133795303444)
		try:
			prizeunreal, time = v.split(",", 1)
			prize = prizeunreal.replace(".giveaway ", "")
			time2 = int(time)
			number = int(60)
			number2 = int(24)
			timecountdown = time2*number*number*number2
			print(timecountdown)
		except Exception:
			embed=discord.Embed(title="Wrong format!")
			embed.add_field(name="Format:", value="```.giveaway (prize),(time)```", inline=False)
			embed.set_footer(text="EU Rust Tournaments")
			await channel.send(embed=embed)
			return
		try:
			NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=int(time))
			embed=discord.Embed(title=f"Giveaway!")
			embed.add_field(name="Prize:", value=f"```{prize}```\n```React with 🎉 to enter!```", inline=False)
			embed.set_footer(text=f"Hosted by: {ctx.message.author}\nEU Rust Tournaments\nEnds at: {NextDay_Date}")
			message = await channel.send(embed=embed)
			await message.add_reaction('🎉')
		except Exception:
			embed=discord.Embed(title="Wrong format!")
			embed.add_field(name="Format:", value="```.giveaway (prize),(time)```", inline=False)
			embed.set_footer(text="EU Rust Tournaments")
			await channel.send(embed=embed)
			return
		await asyncio.sleep(timecountdown)
		msg = await ctx.channel.fetch_message(message.id)
		reactors = await msg.reactions[0].users().flatten()
		user = random.choice(reactors)
		embed=discord.Embed(title=f"Giveaway ended!")
		embed.add_field(name="Winner:", value=f"```{user}```", inline=False)
		embed.add_field(name="Prize:", value=f"```{prize}```", inline=False)
		embed.set_footer(text=f"Hosted by: {ctx.message.author}\nEU Rust Tournaments")
		await message.edit(embed=embed)
		print(user)



@client.command()
@commands.has_role('Staff')
async def whois(ctx):
	try:
		user = ctx.message.mentions[0]
	except Exception:
		embed=discord.Embed(title="Wrong format!")
		embed.add_field(name="Format:", value="```.whois (@user)```", inline=False)
		embed.set_footer(text="EU Rust Tournaments")
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
async def remove(ctx):
	checker = 0
	x = ctx.message.content 
	try:
		y = x.split(" ", 2)
	except Exception:
		embed=discord.Embed(title="Wrong format!")
		embed.add_field(name="Format:", value="```.dq (team number) (reason)```", inline=False)
		embed.set_footer(text="EU Rust Tournaments")
		await ctx.send(embed=embed)
	team1string = y[1]
	team1string_lowercase = team1string.lower()
	team1contains_letters = team1string_lowercase.islower()	
	GUILD = client.get_guild('810954832583852083')
	if team1contains_letters == False:
		for guild in client.guilds:
				if guild.name == GUILD:
					break
				for guild in client.guilds:
					for member in guild.members:
						checker +=1 
						print(checker)
						tee1 = discord.utils.get(guild.roles, name=f"Team {y[1]}")
						signed = discord.utils.get(guild.roles, name="Signed")
						print(member)
						if tee1 in member.roles:
							print('Found')
							try:
								await member.remove_roles(tee1)
								await member.remove_roles(signed)	
							except Exception:
								print('An error happened')
							try:
								embed2=discord.Embed(title="Team removed!")
								embed2.add_field(name="Reason:", value=f"```{y[2]}```", inline=False)
								embed2.add_field(name="Removed by:", value=f"{ctx.message.author}", inline=False)
								embed2.set_footer(text="EU Rust Tournaments")
								await member.send(embed=embed2)
							except Exception:
								print('Skipped!')
								pass
						else:
							pass
					await ctx.send(f"```Team {y[1]} has been dq'ed```")
	else:			
		embed=discord.Embed(title="Wrong format!")
		embed.add_field(name="Format:", value="```.dq (team number)```", inline=False)
		embed.set_footer(text="EU Rust Tournaments")
		await ctx.send(embed=embed)
		return

@client.command()
@commands.has_role('Staff')
async def switch(ctx):
	checker = 0
	x = ctx.message.content
	try:
		cmd, team1, team2 = x.split(" ", 3)
	except Exception:
		embed=discord.Embed(title="Wrong format!")
		embed.add_field(name="Format:", value="```.switch (team number1) (team number2)```", inline=False)
		embed.set_footer(text="EU Rust Tournaments")
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
			embed=discord.Embed(title="Wrong format!")
			embed.add_field(name="Format:", value="```.switch (team number1) (team number2)```", inline=False)
			embed.set_footer(text="EU Rust Tournaments")
			await ctx.send(embed=embed)
	else:
		embed=discord.Embed(title="Wrong format!")
		embed.add_field(name="Format:", value="```.switch (team number1) (team number2)```", inline=False)
		embed.set_footer(text="EU Rust Tournaments")
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
		if ctx.message.channel.id == 811690381590790215:
			if ctx.message.author == 816700983899848735:
				return
			else:
				print('1!')
				signupc = client.get_channel(811690381590790215)
				embed=discord.Embed(title="Wrong format!")
				embed.add_field(name="Format:", value="```.signup - @member1@member2@member3....```", inline=False)
				embed.set_footer(text="EU Rust Tournaments")
				await signupc.send(embed=embed)


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
		await ctx.send('```Team limit can only be set to a number!```')
	else:
		tlimit.write(num)
		await ctx.send(f"```Team limit has been set to {num}!```")

@client.command()
@commands.has_role('Server moderator')
async def tcounter(ctx):
	print('Tlimiter recognized')
	tcounter = open("team_counter.txt", "w")
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
		await ctx.send('```Team counter can only be set to a number!```')
	else:
		tcounter.write(num)
		await ctx.send(f"```Team counter has been set to {num}!```")


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

@client.command()
async def signup(ctx):
	if ctx.message.channel.id == 811690381590790215:
		if "-" in ctx.message.content:	
			global team_limit
			string = ctx.message.content
			substring = "@"
			count = string.count(substring)
			print(count)
			tl = open("tlimit.txt", "r")
			sb = open("substring.txt", "w")
			sb.write(f"{count}")
			sb.close()
			sb2 = open("substring.txt", "r")
			team_limit = tl.read()
			guild = client.get_guild(810954832583852083)
			tee1 = discord.utils.get(guild.roles, name="Signed")
			banned = discord.utils.get(guild.roles, name="Tournament banned")
			mentions = ""
			msg = ctx.message
			try:
				x = ctx.message.content
				user2, user1 = x.split("-", 2)
			except Exception:
				embed=discord.Embed(title="Error!")
				embed.add_field(name="User error:", value=f"```Remove subs/make sure you only @ {team_limit} members```", inline=False)
				embed.set_footer(text="EU Rust Tournaments")
				await ctx.send(embed=embed)
				return
			print(user2)
			print(user1)
			signup = client.get_channel(812836000228311125)
			signupc = client.get_channel(811690381590790215)
			a_string = user1
			a_string_lowercase = a_string.lower()
			contains_letters = a_string_lowercase.islower()	
			count2 = sb2.read()
			print(f'{count2} = counter')
			print(f'{team_limit} = teamlimit')
			if ctx.message.author in ctx.message.mentions:
				for mention in msg.mentions:
					mentions = mentions + " " + mention.mention
				for mention in msg.mentions:
					member = mention
					if tee1 in member.roles:
						embed=discord.Embed(title="Error!")
						embed.add_field(name="User error:", value=f"```{member} is already in a team!```", inline=False)
						embed.set_footer(text="EU Rust Tournaments")
						await ctx.send(embed=embed)
						return
					else:
						if banned in member.roles:
							embed=discord.Embed(title="Error!")
							embed.add_field(name="User error:", value=f"```{member} is Tournament banned!```", inline=False)
							embed.set_footer(text="EU Rust Tournaments")
							await ctx.send(embed=embed)
							return
						else:
							pass
				if contains_letters == False:
					if count2 == team_limit:
						await signup.send(f'***{ctx.message.author} has applied! \nTeam: {user1}***')
						embed=discord.Embed(title="Succes!")
						embed.add_field(name="Team applied", value="```The bot will dm you when staff has approved your team!```", inline=False)
						embed.set_footer(text="EU Rust Tournaments")
						await signupc.send(embed=embed)
					else:
						embed2=discord.Embed(title="Error!")
						embed2.add_field(name="Too many/not enough users tagged", value=f"```Do not @ more/less than {team_limit} members```", inline=False)
						embed2.set_footer(text="EU Rust Tournaments")
						await signupc.send(embed=embed2)
				else:
					embed=discord.Embed(title="Wrong format!")
					embed.add_field(name="Format:", value="```Make sure to @ all your members/remove subs from your sign-up message```", inline=False)
					embed.set_footer(text="EU Rust Tournaments")
					await signupc.send(embed=embed)
					return
			else:
				embed=discord.Embed(title="Error!")
				embed.add_field(name="User error:", value=f"```{member} You need to be in the team your trying to sign up!```", inline=False)
				embed.set_footer(text="EU Rust Tournaments")
				await ctx.send(embed=embed)
				return
		else:
			if ctx.message.author.id == 816700983899848735:
				return
			else:
				signupc = client.get_channel(811690381590790215)
				embed=discord.Embed(title="Wrong format!")
				embed.add_field(name="Format:", value="```.signup - @member1@member2@member3....```", inline=False)
				embed.set_footer(text="EU Rust Tournaments")
				await signupc.send(embed=embed)
	else:
		return

	
@client.event
async def on_message(message):
	await client.process_commands(message)
	if message.channel.id == 817972037057511454:
		if message.author.id == 816700983899848735:
			return
		else:
			if ".clear" in message.content:
				return
			else:
				if ".sub" in message.content:
					return
				else:
					substi = client.get_channel(817972037057511454)
					embed=discord.Embed(title="Wrong format!")
					embed.add_field(name="Format:", value="```.sub - @user + @user```", inline=False)
					embed.set_footer(text="EU Rust Tournaments")
					await substi.send(embed=embed)
	if message.channel.id == 811690381590790215:
		if message.author.id == 816700983899848735:
			return
		else:
			if "." in message.content:
				return
			else:
				if "closed" in message.content:
					return
				else:
					signupc = client.get_channel(811690381590790215)
					embed=discord.Embed(title="Wrong format!")
					embed.add_field(name="Format:", value="```.signup - @member1@member2@member3....```", inline=False)
					embed.set_footer(text="EU Rust Tournaments")
					await signupc.send(embed=embed)
	if message.channel.id == 811690381590790215:
		try:
			print('Deleting message...!2')
			await asyncio.sleep(4)
			await message.delete()
		except Exception:
			pass
	if message.channel.id == 817913002120314930:
		try:
			print('Deleting message...!')
			await asyncio.sleep(4)
			await message.delete()
		except Exception:
			pass
	if message.channel.id == 812836000228311125:
		if message.author.id == 816700983899848735: 
			if "Im proccessing previous commands | Wait!" in message.content:
				try:
					await asyncio.sleep(3)
					await message.delete()
				except Exception:
					pass
			else:
				print('Bot send message')
				await message.add_reaction('✅')
				await message.add_reaction('❎')
				print('It Worked, Reactions added!')
				return
	if message.channel.id == 818795394187132938:
		try:
			await asyncio.sleep(3)
			await message.delete()
		except Exception:
			pass
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

@client.command()
@commands.has_role('Server moderator')
async def send(ctx):
	channel = client.get_channel(817913002120314930)
	e = str("Team-counter status:```fix\nPending...\n```")
	ec =str("Match-board status:```diff\n+Task completed!\n```")
	a = str("Signup status:```fix\nPending...\n```")
	ac =str("Match-board status:```diff\n+Task completed!\n```")
	b = str("Match-board status:```fix\nPending...\n```")
	bc =str("Match-board status:```diff\n+Task completed!\n```")
	c = str("Score-channel status:```fix\nPending...\n```")
	cc =str("Match-board status:```diff\n+Task completed!\n```")
	d = str("Team-accept status:```fix\nPending...\n```")
	dc =str("Match-board status:```diff\n+Task completed!\n```")
	f = str("Team roles clearing status:```fix\nPending...\n```")
	fc =str("Team roles clearing status:```diff\n+Task completed!\n```")
	await channel.send(a)
	await channel.send(b)
	await channel.send(c)
	await channel.send(d)
	await channel.send(e)
	await channel.send(f)

wait = 0



#LONG COMMANDS
@client.command()
async def sub(ctx):
	x = ctx.message.content
	command, message5 = x.split("sub", 2)
	print(message5)
	a_string = message5
	a_string_lowercase = a_string.lower()
	contains_letters = a_string_lowercase.islower()	
	print(contains_letters)
	signupc = client.get_channel(817972037057511454)
	if contains_letters == False:
		try:
			member = ctx.message.author
			member1 = ctx.message.mentions[0]
			member2 = ctx.message.mentions[1]
			embed2=discord.Embed(title="Success!")
			embed2.add_field(name="You have subbed:", value=f"```- {ctx.message.mentions[0]} + {ctx.message.mentions[1]} ```", inline=False)
			embed2.set_footer(text="EU Rust Tournaments")
		except IndexError:
			signupc = client.get_channel(817972037057511454)
			embed=discord.Embed(title="Wrong format!")
			embed.add_field(name="Format:", value="```.sub - @user + @user```", inline=False)
			embed.set_footer(text="EU Rust Tournaments")
			await signupc.send(embed=embed)
			return
		for h in range(1,66):
			if h == 65:
				signupc = client.get_channel(817972037057511454)
				embed=discord.Embed(title="Error")
				embed.add_field(name="Team error:", value="```You need to be in a team/the right team!```", inline=False)
				embed.set_footer(text="EU Rust Tournaments")
				await signupc.send(embed=embed)
				return
			else:
				te1 = discord.utils.get(ctx.guild.roles, name=f"Team {h}")
				if te1 in member.roles:
					Signed = discord.utils.get(ctx.guild.roles, name="Signed")
					await member1.remove_roles(te1)
					await member2.add_roles(te1)
					await member1.remove_roles(Signed)
					await member2.add_roles(Signed)
					await signupc.send(embed=embed2)
					break
				else:
					pass
	else:
		print('Geuss this worked')
		signupc = client.get_channel(817972037057511454)
		embed=discord.Embed(title="Wrong format!")
		embed.add_field(name="Format:", value="```Make sure that you @ the members your trying sub```", inline=False)
		embed.set_footer(text="EU Rust Tournaments")
		await signupc.send(embed=embed)
		return

@client.event
async def on_raw_reaction_add(payload):
	guild = client.get_guild(payload.guild_id)
	access = discord.utils.get(guild.roles, name="Server moderator")
	msg = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
	if payload.channel_id == 812836000228311125:
		if payload.user_id == 816700983899848735:
			return
		else:
			if payload.emoji.name == "✅":
				global wait
				mentions = ""
				x = msg.content 
				a, b = x.split(":", 2)
				print(b)
				c = b.replace("*","")
				Signed = discord.utils.get(guild.roles, name="Signed")
				print(wait)
				accept = client.get_channel(812836000228311125)
				if wait == 0:
					wait = 1
					for x in range(1, 65):
						t1 = f't{x}.txt'
						if os.stat(t1).st_size == 0:
							tee1 = discord.utils.get(guild.roles, name=f"Team {x}")
							wait = 1
							for mention in msg.mentions:
								mentions = mentions + " " + mention.mention
							for mention in msg.mentions:
								await mention.add_roles(tee1)
								await mention.add_roles(Signed)
								client.loop.create_task(checker())
								try:
									channel2 = await mention.create_dm()
									embed=discord.Embed(title="Your team has been accepted!", color=0x0040ff)
									embed.add_field(name="Your team:", value=f"{c}", inline=False)
									embed.add_field(name="Accepted by:", value=f"{payload.member}", inline=False)
									embed.set_footer(text="EU Rust Tournaments")
									await channel2.send(embed=embed)
								except Exception:
									print('Passed!')
									pass
							break
						else:
							pass
				else:
					await accept.send('```Im proccessing previous commands | Wait!```')	
					await msg.remove_reaction(emoji=payload.emoji,member=payload.member)
					return																																
			if payload.emoji.name == "❎":
				mentions = ""
				for mention in msg.mentions:
					mentions = mentions + " " + mention.mention
				for mention in msg.mentions:
					try:
						channel2 = await mention.create_dm()
						embed=discord.Embed(title="Your team has been denied!", color=0x0040ff)
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
				f = str("Team roles clearing status:```fix\nPending...\n Members checked: 0\n```")
				fc =str("Team roles clearing status:```diff\n+Task completed!\n```")
				e = str("Team-counter/limit status:```fix\nPending...\n```")
				ec =str("Team-counter/limit status:```diff\n+Task completed!\n```")
				a = str("Signup status:```fix\nPending...\n```")
				ac =str("Signup status:```diff\n+Task completed!\n```")
				b = str("Subs status:```fix\nPending...\n```")
				bc =str("Subs status:```diff\n+Task completed!\n```")
				c = str("Score-channel status:```fix\nPending...\n```")
				cc =str("Score-channel status:```diff\n+Task completed!\n```")
				d = str("Team-accept status:```fix\nPending...\n```")
				dc =str("Team-accept status:```diff\n+Task completed!\n```")
				channel = client.get_channel(817913002120314930)
				signups = await channel.fetch_message(817966426097844244)
				substitutions = await channel.fetch_message(817966427092156416)
				scorechannels = await channel.fetch_message(817966427927609374)
				teamaccepts = await channel.fetch_message(817966428568289291)
				teamcounters = await channel.fetch_message(817966429924098068)
				teamclearing = await channel.fetch_message(817966447564554273)
				signed = discord.utils.get(guild.roles, name="Signed")
				await signups.edit(content=f'{a}')
				await substitutions.edit(content=f'{b}')
				await scorechannels.edit(content=f'{c}')
				await teamaccepts.edit(content=f'{d}')
				await teamcounters.edit(content=f'{e}')
				await teamclearing.edit(content=f'{e}')
				print('You have access!')
				resetchannel = client.get_channel(817913002120314930)
				await resetchannel.send('Clearing... This proccess might take multiple minutes!')
				await msg.remove_reaction(emoji=payload.emoji,member=payload.member)
				GUILD = client.get_guild('810954832583852083')
				amount = 200
				signupc = client.get_channel(811690381590790215)
				await signupc.purge(limit=amount)
				await signupc.send('```Use this format! \n.signup - @member1@member2@member3....```')
				await signups.edit(content=f'{ac}')
				await resetchannel.send('Signup channel cleard!')
				print('Signup channel purged!')
				subs = client.get_channel(817972037057511454)
				await subs.purge(limit=amount)
				await substitutions.edit(content=f'{bc}')
				await subs.send('```Use this format! \n.sub - (@user1) + (@user2)```')
				await resetchannel.send('Substitutions channel cleard!')
				print('Subs channel purged!')
				score = client.get_channel(812322092023808010)
				await score.purge(limit=amount)
				await score.send('```Use this format! \nWin: (@Your team) vs (@Enemy team) score: (score)```')
				await scorechannels.edit(content=f'{cc}')
				await resetchannel.send('Score channel cleard!')
				print('Score channel purged!')
				ta = client.get_channel(812836000228311125)
				await ta.purge(limit=amount)
				await teamaccepts.edit(content=f'{dc}')
				await resetchannel.send('Team-accept channel cleard!')
				print('Team Accept channel purged!')
				tcounter = open("team_counter.txt", "w")
				tlimit = open("tlimit.txt", "w")
				tlimit.write('0')
				await teamcounters.edit(content=f'{ec}')
				print('Team counter/Team limit has been reset!')
				await resetchannel.send('Team counter/Team limit has been reset!')
				print('1')
				guild = client.get_guild(payload.guild_id)
				for y in range(1, 65):
					print(y)
					team = discord.utils.get(guild.roles, name=f"Team {y}")
					signed = discord.utils.get(guild.roles, name=f"Signed")
					print(team)
					for member in team.members:
						print(member)
						await member.remove_roles(team)
						await member.remove_roles(signed)
					await asyncio.sleep(1)
				teamclearing = await channel.fetch_message(817966447564554273)
				fc =str("Team roles clearing status:```diff\n+Task completed!\n```")
				await teamclearing.edit(content=f'{fc}')
				await resetchannel.send('Roles have been reset!')
		else:
			await msg.remove_reaction(emoji=payload.emoji,member=payload.member)
			return

#DO NOT TOUCH // SIGNUP SECTION

async def statuschanger():
	while True:
		guild = client.get_guild(810954832583852083)
		statusfile = open('status.txt', 'r')
		status = statusfile.read()
		tei = discord.utils.get(guild.roles, name="🏆Current winner")
		for member in tei.members:
			await client.change_presence(status=discord.Status.idle, activity=discord.Game(f'{status}'))
			await asyncio.sleep(4)
			await client.change_presence(status=discord.Status.idle, activity=discord.Game(f'{member.name}'))
			await asyncio.sleep(4)

async def tlmittcounter():
	while True:
		try:
			tlimit = open("tlimit.txt", "r")
			teamlimit = tlimit.read()
			tcounter = open("team_counter.txt", "r")
			team_counter = tcounter.read()
			channel = client.get_channel(818795394187132938)
			message = await channel.fetch_message(818795506699862036)
			await message.edit(content=f"```Team limit: {teamlimit}```")
			await asyncio.sleep(2)
		except Exception:
			pass

async def playingmembers():
	while(True):
		guild = client.get_guild(810954832583852083)
		signed = discord.utils.get(guild.roles, name="Signed")
		for b in range(1,65):
			t1 = open(f"t{b}.txt", "w", encoding='utf-8')
			te1 = discord.utils.get(guild.roles, name=f"Team {b}")
			for member in te1.members:
				t1.write(f'{member.name} \n')	
		await asyncio.sleep(2)

async def checker():
	while(True):
		guild = client.get_guild(810954832583852083)
		signed = discord.utils.get(guild.roles, name="Signed")
		for b in range(1,65):
			t1 = open(f"t{b}.txt", "w", encoding='utf-8')
			te1 = discord.utils.get(guild.roles, name=f"Team {b}")
			for member in te1.members:
				t1.write(f'{member.name} \n')	
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
		t1name = t1.readlines()
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
		await asyncio.sleep(4)

#message. (team 1 (team 1.txt) /n)

#lav en anden auto process som opdaterer hver minut
	
client.run('ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.3jMwdiwaJo5W8iC5Eotf86lQTGk')
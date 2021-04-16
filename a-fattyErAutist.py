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
async def on_raw_reaction_add(payload):
	if payload.channel.id == 832269492582612992: #insert payed channel id
		if payload.emoji == "💰":
			payloadChannel = client.get_channel(payload.channel_id)
			if payload.emoji.name == "📩":
				if payload.channel_id == 830523406348845066:
					userMention = f'<@{payload.member.id}>'
					requestSupportChannel = client.get_channel(830523406348845066)
					requestSupportMessage = await requestSupportChannel.fetch_message(830526877566763058)
					buyinCategory = discord.utils.get(client.guild.categories, id=832601089936326666) #Put id in
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
					embed = discord.Embed(title='EURT Support', description=f"A {staff.mention} member will be with you shortly")
					embed.add_field(name="\nClosing the ticket", value="To close the ticket react with 🔒 and then ✅", inline=False)
					embed.set_footer(text='EU Rust Tournaments', icon_url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
					ticketChannel = await guild.create_text_channel(name=f'ticket-{payload.member.name}', category=buyinCategory)
					ticketEmbed = await ticketChannel.send(embed=embed)
					await ticketEmbed.add_reaction("🔒")
					await ticketChannel.set_permissions(verified, view_channel=False)
					await ticketChannel.set_permissions(everyone, view_channel=False)
					await ticketChannel.set_permissions(payload.member, view_channel=True)
					await requestSupportMessage.remove_reaction(emoji=payload.emoji,member=payload.member)
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
						await payloadChannel.delete()

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


@client.command()
async def signup(ctx):
	if ctx.message.channel.id == 811690381590790215:
		if "-" in ctx.message.content:	
			global team_limit
			string = ctx.message.content
			substring = "@"
			count = string.count(substring)
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
				embed = discord.Embed(description=f'Error! Remove subs/make sure you only @ {team_limit} members')
				await ctx.send(embed=embed)
				return
			signup = client.get_channel(812836000228311125)
			signupc = client.get_channel(811690381590790215)
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
					if count2 == team_limit:
						await signup.send(f'***{ctx.message.author}({ctx.message.author.id}) has applied! \nTeam: {user1}***')
						embed = discord.Embed(description=f'Succes! The bot will dm you when staff has approved your team!')
						await ctx.send(embed=embed)
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
	if ctx.message.channel.id == 811690381590790215: #Insert new signup channel id 
		if "-" in ctx.message.content:	
			string = ctx.message.content
			substring = "@"
			count = string.count(substring)
			tl = open("payed_tlimit.txt", "r")
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
				embed = discord.Embed(description=f'Error! Remove subs/make sure you only @ {team_limit} members')
				await ctx.send(embed=embed)
				return
			signup = client.get_channel(812836000228311125) # Insert new signup accept channel
			signupc = client.get_channel(811690381590790215)
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
					if count2 == team_limit:
						await signup.send(f'***{ctx.message.author}({ctx.message.author.id}) has applied! \nTeam: {user1}***') # Insert new signup accept channel
						embed = discord.Embed(description=f'Succes! The bot will dm you when staff has approved your team!\n React with 💰 when your ready to pay, this needs to be done, otherwise your team wont be accepted')
						reactEmbed = await ctx.send(embed=embed)
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
	else:
		return

    

client.run('ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.KO5zzXVpmAYKOhv11OvIS2xBOqI')
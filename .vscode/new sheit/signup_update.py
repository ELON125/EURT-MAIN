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
from datetime import timedelta
from discord.ext.commands import CommandNotFound

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)

wait = 0

#LAV UNDER if roles in member.roles
#--comand--
#break
#else if x = 65 channel.send(something went wrong/ur not in a team  )

@client.event
async def on_ready():
	print('EURT bot online!')

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
				x = msg.content 
				start = "("
				end = ")"
				userIdStr = ((s.split(start))[1].split(end)[0])
				userId = int(userIdStr)
				mentions = ""
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
								channel2 = await userId.create_dm()
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
					await accept.send('```Im proccessing previous commands | Wait!```')	
					await msg.remove_reaction(emoji=payload.emoji,member=payload.member)
					return																															
			if payload.emoji.name == "❎":
				mentions = ""
				x = msg.content
				start = "("
				end = ")"
				userIdStr = ((s.split(start))[1].split(end)[0])
				userId = int(userIdStr)
				try:
					channel2 = await mention.create_dm()
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

@client.command()
async def signup(ctx):
	if ctx.message.channel.id == 811690381590790215:
		if "-" in ctx.message.content:	
			global team_limit
			string = ctx.message.content
			substring = "@"
			count = string.count(substring)
			tl = open("tlimit.txt", "r")
			team_limit = tl.read()
			guild = client.get_guild(810954832583852083)
			signedRole = discord.utils.get(guild.roles, name="Signed")
			bannedRole = discord.utils.get(guild.roles, name="Tournament banned")
			msg = ctx.message
			signupAccept = client.get_channel(812836000228311125)
			signupChannel = client.get_channel(811690381590790215)
			a_string = user1
			a_string_lowercase = a_string.lower()
			contains_letters = a_string_lowercase.islower()	
			try:
				x = ctx.message.content
				user2, user1 = x.split("-", 2)
			except Exception:
				embed=discord.Embed(title="Error!")
				embed.add_field(name="User error:", value=f"```Remove subs/make sure you only @ {team_limit} members```", inline=False)
				embed.set_footer(text="EU Rust Tournaments")
				await ctx.send(embed=embed)
				return
			if ctx.message.author in ctx.message.mentions:
				for mention in msg.mentions:
					mentions = mentions + " " + mention.mention
				for mention in msg.mentions:
					member = mention
					if signedRole in member.roles:
						embed=discord.Embed(title="Error!")
						embed.add_field(name="User error:", value=f"```{member} is already in a team!```", inline=False)
						embed.set_footer(text="EU Rust Tournaments")
						await ctx.send(embed=embed)
						return
					else:
						if bannedRole in member.roles:
							embed=discord.Embed(title="Error!")
							embed.add_field(name="User error:", value=f"```{member} is Tournament banned!```", inline=False)
							embed.set_footer(text="EU Rust Tournaments")
							await ctx.send(embed=embed)
							return
						else:
							pass
				if contains_letters == False:
					if count == team_limit:
						await signupAccept.send(f'***{ctx.message.author}({ctx.message.author.id}) has applied! \nTeam: {user1}***')
						embed=discord.Embed(title="Succes!")
						embed.add_field(name="Team applied", value="```The bot will dm you when staff has approved your team!```", inline=False)
						embed.set_footer(text="EU Rust Tournaments")
						await signupChannel.send(embed=embed)
					else:
						embed2=discord.Embed(title="Error!")
						embed2.add_field(name="Too many/not enough users tagged", value=f"```Do not @ more/less than {team_limit} members```", inline=False)
						embed2.set_footer(text="EU Rust Tournaments")
						await signupChannel.send(embed=embed2)
				else:
					embed=discord.Embed(title="Wrong format!")
					embed.add_field(name="Format:", value="```Make sure to @ all your members/remove subs from your sign-up message```", inline=False)
					embed.set_footer(text="EU Rust Tournaments")
					await signupChannel.send(embed=embed)
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
				signupChannel = client.get_channel(811690381590790215)
				embed=discord.Embed(title="Wrong format!")
				embed.add_field(name="Format:", value="```.signup - @member1@member2@member3....```", inline=False)
				embed.set_footer(text="EU Rust Tournaments")
				await signupChannel.send(embed=embed)
	else:
		return
	
client.run('ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.3jMwdiwaJo5W8iC5Eotf86lQTGk')
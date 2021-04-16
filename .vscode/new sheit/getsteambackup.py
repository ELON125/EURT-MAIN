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
		embed.set_footer(text=f"Requested by: {ctx.message.author}\nEU Rust Tournaments")
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(description='ID not in database')
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
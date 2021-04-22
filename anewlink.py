import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import CommandNotFound
import discord.ext.commands
import pymongo 
import steam
from pymongo import MongoClient

dbClient = MongoClient("mongodb+srv://D1P:D1P9812@hokuspokusdb.gehgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = dbClient["EURTDatabase"]
collection = db["steamLink"]
newcollection = db["newSteamLink"]
wait = 0


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all(),
            description="EURT bot",
        )
        self.client = steam.Client()

    async def on_ready(self) -> None:
        await self.client.wait_until_ready()
        print("Ready")

    async def start(self, token: str, username: str, password: str) -> None:
        await asyncio.gather(
            super().start(token),
            self.client.start(username, password),
        )

    async def close(self) -> None:
        await self.client.close()
        await super().close()

client = DiscordBot()

@client.command()
async def link(ctx):
    if "verify" in ctx.message.channel.name:
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
        if ifSteamId64 == True:
            embed = discord.Embed(description='This is not an id64')
            await ctx.send(embed=embed)
            return
        else:
            if newcollection.count_documents({"SteamID":f"{steamid64}"}) > 0:
                embed = discord.Embed(description='This account is already linked')
                await ctx.send(embed=embed)
                return
            else:
                user = await ctx.bot.client.fetch_user((int(steamid64)))
                if user == None:
                    embed = discord.Embed(description='Error! User not found, make sure the id64 is correct')
                    await ctx.send(embed=embed)
                    return
                else:
                    if user.is_private() == True:
                        embed = discord.Embed(description='Make sure the steam profile is public\nWe use this to collect information to prevent scripters/cheaters to play')
                        await ctx.send(embed=embed)
                    else:
                        rust_game = steam.utils.get(await user.games(), title='Rust')
                        if rust_game == None:
                            embed = discord.Embed(description='This steam account does not own rust')
                            await ctx.send(embed=embed)
                            return
                        if user.created_at == None:
                            embed = discord.Embed(description='Make sure the steam profile is public\nWe use this to collect information to prevent scripters/cheaters to play')
                            await ctx.send(embed=embed)
                            return
                        user.profile_url = f"https://steamcommunity.com/profiles/{steamid64}/"
                        post = {"DiscordName": f"{member.name}", "DiscordAvatar": f"{member.avatar_url}", "DiscordID": f"{member.id}", "DiscordCreationDate": f"{member.created_at}", "SteamName": f"{user.name}", "SteamProfileUrl": f"{user.profile_url}", "SteamID": f"{user.id64}", "SteamAvatar": f"{user.avatar_url}", "SteamCreatedAt": f"{user.created_at}", "RustHours":f"{rust_game.total_play_time}"}
                        newcollection.insert_one(post)
                        embed = discord.Embed(description='Your steam account has been linked')
                        await ctx.author.add_roles(verified)
                        await ctx.send(embed=embed)
    else:
        return

client.run("ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.KO5zzXVpmAYKOhv11OvIS2xBOqI", "mattiasms7", "EURTbot4321")
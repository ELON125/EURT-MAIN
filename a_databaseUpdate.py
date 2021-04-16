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
import steam
from pymongo import MongoClient

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')
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
async def test(ctx):
    count = 0
    notWorked = []
    guild = client.get_guild(810954832583852083)
    for document in collection.find():
        discordName = document["DiscordName"]
        discordID = document["DiscordID"]
        steamID = document["SteamID"]
        print(discordID, steamID)
        try:
            user = await ctx.bot.client.fetch_user((int(steamID)))
            member = await guild.fetch_member(int(discordID))
            user.profile_url = f"https://steamcommunity.com/profiles/{steamID}/"
            post = {"DiscordName": f"{member.name}", "DiscordAvatar": f"{member.avatar_url}", "DiscordID": f"{member.id}", "DiscordCreationDate": f"{member.created_at}", "SteamName": f"{user.name}", "SteamProfileUrl": f"{user.profile_url}", "SteamID": f"{user.id64}", "SteamAvatar": f"{user.avatar_url}"}
            newcollection.insert_one(post)
            count +=1
        except Exception:
            print('Passed')
            notWorked.append(discordName)
    for name in notWorked:
        print(name)
    print(count)

client.run("ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.KO5zzXVpmAYKOhv11OvIS2xBOqI", "mattiasms7", "EURTbot4321")
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

@client.event
async def on_ready():
	print('EURT bot online!')       

@client.command()
async def send(ctx):
    embed = discord.Embed(title="Arena Settings",description="**Map:**\nDeadmans\n\n**EURT**")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
    await ctx.send(embed=embed)


client.run('ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.KO5zzXVpmAYKOhv11OvIS2xBOqI')   
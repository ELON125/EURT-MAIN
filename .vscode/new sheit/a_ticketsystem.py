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
from steam.webapi import WebAPI
import discord.ext.commands
import steam
from steam.steamid import SteamID
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
async def test(ctx):
    embed = discord.Embed(title='EURT Support', description="This ticket is for general support/questions about the event\n Please be patient while waiting for response as we might be busy")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
    embed.add_field(name="\u200b", value="To create a ticket react with 📩")
    embed.set_footer(text='EU Rust Tournaments', icon_url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
    message = await ctx.send(embed=embed)
    await message.add_reaction("📩")

@client.event
async def on_raw_reaction_add(payload):
    guild = client.get_guild(810954832583852083)
    payloadChannel = client.get_channel(payload.channel_id)
    if payload.emoji.name == "📩":
        if payload.channel_id == 830523406348845066:
            for channel in guild.channels:
                userMention = f'<@{payload.member.id}>'
                try:
                    channelNameSplit = channel.name
                    ticket, name = channelNameSplit.split("-", 1)
                except ValueError:
                    pass
                userName = payload.member.name
                if userName.lower() == name:
                    await channel.send(userMention)
                    embed = discord.Embed(description='You need to close this ticket to open another one!')
                    await channel.send(embed=embed)
                    return
                else:
                    pass
            requestSupportChannel = client.get_channel(830523406348845066)
            requestSupportMessage = await requestSupportChannel.fetch_message(830526877566763058)
            verified = discord.utils.get(guild.roles, name=f"Verified")
            everyone = discord.utils.get(guild.roles, name=f"@everyone")
            staff = discord.utils.get(guild.roles, name="Staff")
            embed = discord.Embed(title='EURT Support', description=f"A {staff.mention} member will be with you shortly")
            embed.add_field(name="\u200b", value="While you wait, please describe you issue in detal with you team name\nSupport will be with you shortly", inline=False)
            embed.add_field(name="Closing the ticket", value="To close the ticket react with 🔒 and then ✅", inline=False)
            embed.set_footer(text='EU Rust Tournaments', icon_url="https://cdn.discordapp.com/attachments/737852831838633984/830488037603409960/RUST_TOURNAMENTS.gif")
            ticketChannel = await guild.create_text_channel(name=f'ticket-{payload.member.name}')
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

        



client.run('ODE2NzAwOTgzODk5ODQ4NzM1.YD-yEA.17qfGDV2yd3Uygp77b4nOi_ifKY')
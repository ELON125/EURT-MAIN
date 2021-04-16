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
from discord.ext.commands import MissingRole
import fivem;

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

server = fivem.getServer("88.214.59.183:30120")

wait = 0

@client.event
async def on_ready():
    print(server.players)
    print('Vores community bot online!')
    print(datetime.datetime.today())
    guild = client.get_guild(823299886451261520)
    for emotes in guild.emojis:
        print(emotes)

@client.event
async def on_command_error(ctx, error):
    await ctx.send("Du har ikke høj nok rang til at bruge denne command!")

@client.command(name='clear')
@commands.has_role('Staff')
async def slet(ctx, amount = 10):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_role('Staff')
async def whois(ctx):
    try:
        user = ctx.message.mentions[0]
    except Exception:
        embed=discord.Embed(title="Wrong format!", color=0xfa6819)
        embed.add_field(name="Format:", value="```.whois (@user)```", inline=False)
        embed.set_footer(text="Vores Community")
        await ctx.send(embed=embed)
    rolesname = []
    for role in user.roles:
        if role.name != "@everyone":
            rolesname.append(role.name)
    b = " | ".join(rolesname)
    embed=discord.Embed(title=f"<:512x512:823539138300084254> {ctx.message.mentions[0]} info:", color=0xfa6819)
    embed.add_field(name="Name/id:", value=f"```{user.name} | {user.id}```", inline=True)
    embed.add_field(name="Profile creation time:", value=f"```{user.created_at}```", inline=True)
    embed.add_field(name="Guild joined date:", value=f"```{user.joined_at}```", inline=True)
    embed.add_field(name="Member roles:", value=f"```{b}```", inline=True)
    embed.set_footer(text=f"Requested by {ctx.message.author}\nVores Community")
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
    embed=discord.Embed(title="<:512x512:823539138300084254> Top inviters!", color=0xfa6819)
    embed.add_field(name="1st:", value=f"```{top1inv} with {top1} invites!```", inline=False)
    embed.add_field(name="2nd:", value=f"```{top2inv} with {top2} invites!```", inline=False)
    embed.add_field(name="3rd:", value=f"```{top3inv} with {top3} invites!```", inline=False)
    embed.set_footer(text="Vores Community")
    await ctx.send(embed=embed)

@client.command()
async def support(ctx):
    if ctx.message.channel.id == 823333086304403487:
        message = ctx.message
        messagecontent = ctx.message.content
        cmd, message = messagecontent.split(" ", 1)
        hjælper = discord.utils.get(ctx.guild.roles, id=823323526776881162)
        staff = discord.utils.get(ctx.guild.roles, id=823317559297310761)
        await ctx.send(f"{staff.mention}{hjælper.mention} {ctx.message.author} har brug for hjælp!")
        embed=discord.Embed(title=f"<:512x512:823539138300084254> Vores Community ©", color=0xfa6819)
        embed.add_field(name="Vores Community Support ❗", value=f"Du har nu tilkaldt en staff og de er orienteret om at du behøver hjælp.", inline=False)
        embed.add_field(name=f"{ctx.message.author.name} Skal bruge hjælp til:", value=f"{message}", inline=False)
        embed.add_field(name="Svartid:", value=f"Vores primetime i support er i hverdagene fra 10:00 til 23:00", inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}\nVores Community © {ctx.message.created_at}")
        await ctx.send(embed=embed)
        await ctx.message.delete()

@client.command()
@commands.has_role('Staff')
async def call(ctx):
    channel = await ctx.message.mentions[0].create_dm()
    await ctx.send(f'<@{ctx.message.mentions[0].id}> {ctx.message.author} Skal snakke med dig i support')
    await channel.send(f"<@{ctx.message.mentions[0].id}> {ctx.message.author} Skal snakke med dig i support")
    await ctx.message.delete()



    #message = ctx.message.content
    #channel = await ctx.message.mentions[0].create_dm()
    #cmd, at, message = message.split(" ", 2)
    #embed=discord.Embed(title=f"<:512x512:823539138300084254> Besked fra {ctx.message.author}:", description=f"{message}", color=0xfa6819)
    #embed.set_footer(text="Vores Community")
    #await channel.send(embed=embed)
    #await ctx.send(f'Besked sent til {ctx.message.mentions[0]}')

    	
client.run('ODIzNTM3NzE1MjczOTI0NjE4.YFiRQw.QSfnlNuWHlPg01ukCEoNro2FvG0')
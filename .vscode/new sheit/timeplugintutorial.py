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
from time import ctime
from replit import db
from datetime import timedelta
from discord.ext.commands import CommandNotFound
import pytz
import zoneinfo
from pytz import timezone	
    
    
    
    
    Europe = timezone('Europe/Copenhagen')
	sa_time = datetime.datetime.now(Europe)
	print(sa_time.hour)
	tz = pytz.timezone('Europe/Copenhagen')
	my_ct = datetime.datetime.now(tz=pytz.UTC)
	now = datetime.datetime.today()
	now2 = f"{now.hour}:{now.minute}:{now.second}"
	print(now.year/month/day/hour/minute/second)
	print(my_ct)
	print(now)
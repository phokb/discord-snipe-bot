import os
import time
import os.path
import discord
import datetime
import json
from discord.ext import commands
from discord.ext.commands import *
from discord.ext import tasks

### USER CONFIGURATION ###

prefix = '-' ## Default prefix is -, you can replace it with your preferred prefix ##
owner = 'EMPTY_USERNAME#0000' ## Replace 'EMPTY_USERNAME#0000' with your Discord username ##
bot_token = '' ## Add the bot token in this variable. For more info check README.md ##

### USER CONFIGURATION END ###

intents = discord.Intents.all()
botVer = 'v1.0'
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')
client = commands.Bot(command_prefix=str(prefix), intents=intents) ## READ COMMENT AT LINE 12 FOR MORE INFO ##
global startTime
startTime = time.time()
client.remove_command('help')
homedir = os.getcwd()

if os.name == 'nt':
    with open(f'{homedir}\\config.json', 'r') as f:
        global config
        config = json.load(f)
else:
    with open(f'{homedir}/config.json', 'r') as f:
        global config
        config = json.load(f)

snipe_log:bool = config[str(config)][str(logs)][snipe]
editsnipe_log:bool = config[str(config)][str(logs)][editsnipe]
        
def randColor():
    return discord.Color.random()

@client.command()
async def help(ctx):
    e = discord.Embed(title='Command Help', description=f'Prefix: `{prefix}`\n\n`{str(prefix)}snipe`: See the most recently deleted message in this channel.\n`{str(prefix)}editsnipe`: See the most recently edited message in this channel.', color=randColor())
    await ctx.send(embed=e)

@client.event
async def on_ready():
    print(f'Logged on to Discord as {client.user.name}')
    print('====================')
    print('Some client info:')
    print('------------------')
    print(f'  Latency: {round(client.latency * 1000)}ms')
    print(f'  Startup time: {round(startTime)}')
    print(f'  Owner: {str(owner)}')
    print('------------------')
    print('====================')

snipe_message_content = {}
snipe_message_author = {}
editsnipe_message_before_content = {}
editsnipe_message_after_content = {}
editsnipe_message_author = {}

@client.event
async def on_message_delete(message):
    if not message.author.bot:
        guild = client.guilds[0]
        channel = message.channel
        snipe_message_author[message.channel.id] = message.author
        snipe_message_content[message.channel.id] = message.content
        if bool(snipe_log) == True:
            print(f"Message deleted in #{channel.name} ({guild.name}):\n   Message content: {message.content}")
        else:
            pass

@client.event
async def on_message_edit(message_before, message_after):
    if not message_after.author.bot:
        editsnipe_message_author[message_before.channel.id] = message_before.author
        guild = message_before.guild.id
        channel = message_before.channel
        editsnipe_message_before_content[channel.id] = message_before.content
        editsnipe_message_after_content[channel.id] = message_after.content
        if bool(editsnipe_log) == True:
            print(f"Message edited in #{channel.name} ({guild.name}):\n   Old message: {message_before.content}\n   New message: {message_after.content}")
        else:
            pass

@client.command()
async def snipe(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id], color=randColor())
        em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}")
        await ctx.send(embed = em)
    except:
        await ctx.send(f"There are no recently deleted messages in <#{channel.id}>")

@client.command()
async def editsnipe(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(description=f'**Message before**:```{editsnipe_message_before_content[ctx.channel.id]}```\n**Message after**:```{editsnipe_message_after_content[ctx.channel.id]}```', color=randColor())
        em.set_footer(text=f'This message was edited by {editsnipe_message_author[channel.id]}')
        await ctx.send(embed = em)
    except:
        await ctx.reply(f'There are no recently edited messages in <#{ctx.channel.id}>')

client.run(str(bot_token))

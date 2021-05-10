from config import discordToken, osuKey
import discord                              # type: ignore
from discord.ext import commands            # type: ignore
from osuapi import OsuApi, ReqConnector     # type: ignore
import requests
import os

connector = connector=ReqConnector()
osuApiCall = OsuApi(osuKey,connector=ReqConnector())

description = '''ex'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='m!', description=description, intents=intents)
bot.remove_command('help')


@bot.event
async def on_message(message):
    bot.ctx = await bot.get_context(message)
    if bot.ctx.prefix is not None:
        message.content = message.content.lower()
        return await bot.process_commands(message)


@bot.command(hidden=True)
async def reload(ctx, name=None):
    if name:
        bot.reload_extension(f'commands.{name}')
        await ctx.send("command reloaded!")


for filename in os.listdir(r'C:\Users\DELL\Desktop\osu-mocha\commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')

bot.run(discordToken)

import discord                      # type: ignore
from discord.ext import commands    # type: ignore

def setup(bot):
    bot.add_cog(utils(bot))



class utils(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        #set activity to prefix

    #need a listener for ping and give back the prefix 


    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")

    # will complete next time
    @commands.command()
    async def botInfo(self, ctx):
        await ctx.send(f'''Bot info : \n latency: {round((self.bot.latency * 1000),0) }
                                      \n''')

    @commands.command()
    async def help(self, ctx,arg):
        await ctx.send("help command soon")

    @commands.command()
    async def prefix(self, ctx, arg=None):
        if (arg == None):
            await ctx.send("no prefix put")
        else:
            await ctx.send("Changing " + self.bot.command_prefix +" to " + arg + " **(actually this doesn't work yet)**")

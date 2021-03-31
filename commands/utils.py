import discord                      # type: ignore
from discord.ext import commands    # type: ignore
from embedHandler import embedHandler
def setup(bot):
    bot.add_cog(utils(bot))



class utils(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print('----------------')
        print("")
        #set activity to prefix

    #need a listener for ping and give back the prefix


    @commands.command(hidden=True)
    async def ping(self, ctx):
        await ctx.send("pong!")

    # will complete next time
    @commands.command(hidden=True)
    async def botInfo(self, ctx):
        await ctx.send(f'''Bot info : \n latency: {round((self.bot.latency * 1000),0) }
                                      \n''')


    @commands.command(brief="utils command",description="check the prefix/change it",aliases=["Prefix"], usage="m!prefix {New Prefix}")
    async def prefix(self, ctx, arg=None):
        if (arg == None):
            await ctx.send("no prefix put")
        else:
            await ctx.send("Changing " + self.bot.command_prefix +" to " + arg + " **(actually this doesn't work yet)**")

    @commands.command(hidden=True)
    async def help(self,ctx, arg=None):
        commandsList = []

        for v in self.bot.commands:
            if not v.hidden:
                commandsList.append(v)

        if arg==None:

            elementList = {}

            i = 0
            j = 0
            while i<len(commandsList):

                if str(commandsList[i].brief).startswith("osu"):

                    if j==0:
                        elementList["Osu"]=commandsList[i].name
                    else:
                        elementList["NaN_"+str(j)]=commandsList[i].name

                    j = j + 1
                i = i + 1

            i = 0
            j = 0
            while i<len(commandsList):

                if str(commandsList[i].brief).startswith("utils"):

                    if j==0:
                        elementList["Utils"]=commandsList[i].name
                    else:
                        elementList["NaN_"+str(i)]=commandsList[i].name

                    j = j + 1
                i = i + 1

            elementList["newline"]=""
            elementList["You can use m!help [command] for more info"]="exemple : m!help osu"
            newEmbed = embedHandler(elementList,embedType=1,color=0xFF748C)

            # will add url to the author for online documentation!!!
            newEmbed.setAuthor(name= "osu!mocha commands!", icon_url=ctx.bot.user.avatar_url)
            newEmbed.setFooter(text = "join the support discord when it will be created:")

            await ctx.send(embed = newEmbed.getEmbed())
        else:
            argEqualCommand = False

            for v in commandsList:
                if str(v) == arg:
                    argEqualCommand = True
                    command = v
                    break

            if argEqualCommand == False:
                await ctx.send("The command is not found")
            else:
                elementList = {
                        "Command name":command.name,
                        "Usage": command.usage,
                        "Aliases": command.aliases,
                        "Description": command.description,
                        "newline":"",
                        "Check out the other commands with":"m!help"
                }


                newEmbed = embedHandler(elementList,embedType=1,color=0xFF748C)

                # will add url to the author for online documentation!!!
                newEmbed.setAuthor(name= "osu!mocha commands!", icon_url=ctx.bot.user.avatar_url)
                newEmbed.setFooter(text = "join the support discord when it will be created:")

                await ctx.send(embed = newEmbed.getEmbed())

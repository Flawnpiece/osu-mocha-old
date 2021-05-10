import discord                      # type: ignore
from discord.ext import commands    # type: ignore
from embedHandler import embedHandler
import sqlite3
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
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for m!help'))

    #need a listener for ping and give back the prefix

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        '''
        Listen for errors related commands.

        Parameters:
            ctx (obj): The bot context
            error (obj): The error the listener catched

        Return:
            message, inform the user of the error and how to "solve" it
        '''
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send("The command you entered is missing arguments, please use ``m!help {command}``")
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send("You dont have all the requirements or permissions for using this command :angry:")

            
    @commands.command(hidden=True)
    async def ping(self, ctx):
        await ctx.send("pong!")

    # will complete next time
    @commands.command(hidden=True)
    async def botInfo(self, ctx):
        await ctx.send(f'''Bot info : \n latency: {round((self.bot.latency * 1000),0) }
                                      \n''')

    @commands.command(brief="utils command",aliases=["suggest"])
    async def suggestion(self,ctx, *args):

        connection = sqlite3.connect('data/Users.db')
        cursor = connection.cursor()

        cursor.execute("SELECT discord_id FROM blacklist")
        databaseSection = cursor.fetchall()
        blacklisted = False
        for v in databaseSection:
            if v[0] == ctx.author.id:
                blacklisted = True

        if blacklisted == False:

            desc = ""
            for v in args:
                desc = desc + " " + v
            elementList = {"NaN_1":desc}

            newEmbed = embedHandler(elementList,embedType=1,color=0x748CFF)
            newEmbed.setAuthor(name= "✦ New suggestion!")
            newEmbed.setFooter(text = "Suggested by " + str(ctx.author.id))
            channel = self.bot.get_channel(839950960469213224)
            return await channel.send(embed = newEmbed.getEmbed())
        else:
            pass

    @commands.command(brief="utils command",aliases=["report"])
    async def bug(self,ctx, *args):

                connection = sqlite3.connect('data/Users.db')
                cursor = connection.cursor()

                cursor.execute("SELECT discord_id FROM blacklist")
                databaseSection = cursor.fetchall()
                blacklisted = False
                for v in databaseSection:
                    if v[0] == ctx.author.id:
                        blacklisted = True

                if blacklisted == False:

                    desc = ""
                    for v in args:
                        desc = desc + " " + v
                    elementList = {"NaN_1":desc}

                    newEmbed = embedHandler(elementList,embedType=1,color=0x748CFF)
                    newEmbed.setAuthor(name= "✦ New bug report!")
                    newEmbed.setFooter(text = "Bug reported by " + str(ctx.author.id))
                    channel = self.bot.get_channel(839950960469213224)
                    return await channel.send(embed = newEmbed.getEmbed())
                else:
                    pass

    @commands.command(hidden=True,aliases=["bl"])
    async def blacklist(self,ctx, arg):

        if ctx.author.id == 246110201785090049:
            connection = sqlite3.connect('data/Users.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO blacklist VALUES (?)',(arg,))
            connection.commit()
            connection.close()
            return await ctx.send("This user got blacklisted!")

    @commands.command(hidden=True, brief="utils command",description="check the prefix/change it",aliases=["Prefix"], usage="m!prefix {New Prefix}")
    async def prefix(self, ctx, arg=None):
        if (arg == None):
            await ctx.send("no prefix put")
        else:
            await ctx.send("Changing " + self.bot.command_prefix +" to " + arg + " **(actually this doesn't work yet)**")

    @commands.command(hidden=True)
    async def help(self,ctx, arg=None):
        commandsList = []

        for v in self.bot.commands:
            print(v.hidden, v)
            if not v.hidden:
                commandsList.append(v)

        if arg==None:

            elementList = {}

            i = 0
            j = 0
            while i<len(commandsList):

                if str(commandsList[i].brief).startswith("osu"):

                    if j==0:
                        elementList["Osu"]="``"+commandsList[i].name+"``"
                    else:
                        elementList["NaN_"+str(j)]="``"+commandsList[i].name+"``"

                    j = j + 1
                i = i + 1

            i = 0
            j = 0
            while i<len(commandsList):

                if str(commandsList[i].brief).startswith("utils"):

                    if j==0:
                        elementList["Utils_box"]=commandsList[i].name
                    else:
                        elementList["NaN_"+str(i)+"_box"]=commandsList[i].name

                    j = j + 1
                i = i + 1

            elementList["newline"]=""
            elementList["NaN"]="You can do ``m!help {command}`` to get more information!"
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
                if len(command.aliases)>0:
                    aliasesString = ""
                    for v in command.aliases:
                        aliasesString = aliasesString  + v+ ", "
                    elementList = {
                            "Command name":command.name,
                            "Usage_box": command.usage,
                            "Aliases_box": aliasesString,
                            "Description": command.description,
                            "newline":"",
                            "NaN":"You can do ``m!help`` to check the other commands!"
                    }

                else :
                    elementList = {
                            "Command name":command.name,
                            "Usage_box": command.usage,
                            "Description": command.description,
                            "newline":"",
                            "NaN":"You can do ``m!help`` to check the other commands!"
                    }


                newEmbed = embedHandler(elementList,embedType=1,color=0xFF748C)

                # will add url to the author for online documentation!!!
                newEmbed.setAuthor(name= "osu!mocha commands!", icon_url=ctx.bot.user.avatar_url)
                newEmbed.setFooter(text = "join the support discord when it will be created:")

                await ctx.send(embed = newEmbed.getEmbed())

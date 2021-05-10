import discord                      # type: ignore
from discord.ext import commands    # type: ignore
from main import osuApiCall          # type: ignore
from embedHandler import embedHandler
import osuapi
import sqlite3
import math

def setup(bot):
    bot.add_cog(profile(bot))


class profile(commands.Cog):

    def __init__(self,bot):
        '''
        The constructor of the profile cog.

        Parameters:
            bot (obj): instance of the bot
        '''
        self.bot = bot

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

    def osusetVerification(self, discordID):
        '''
        If the user don't provide an username, it search if he has an osu account tied to his discord.

        Parameters:
            username (str/int): The username of the osu profile

        Return:
            username (str/int), if
        '''

        connection = sqlite3.connect('data/Users.db')
        cursor = connection.cursor()

        cursor.execute("SELECT osu_id FROM osuset WHERE discord_id=?", (discordID,))
        databaseSection = cursor.fetchone()

        # If we find an element in the database
        if databaseSection!= None:
            username=databaseSection[0]
            return username

    def userProfile(self,arg,gamemode):

        if type(arg) == int:
            pass
        else:
            if arg.isdigit():
                arg = int(arg)

        if gamemode == "standard":
            res = osuApiCall.get_user(username=arg)[0]
            gamemodeUrl = "https://osu.coffee/mode-osu2x.png"

        if gamemode == "taiko":
            res = osuApiCall.get_user(username=arg, mode=osuapi.enums.OsuMode.taiko)[0]
            gamemodeUrl = "https://osu.coffee/mode-taiko2x.png"
        if gamemode == "ctb":
            res = osuApiCall.get_user(username=arg, mode=osuapi.enums.OsuMode.ctb)[0]
            gamemodeUrl = "https://osu.coffee/mode-fruits2x.png"
        if gamemode == "mania":
            res = osuApiCall.get_user(username=arg, mode=osuapi.enums.OsuMode.mania)[0]
            gamemodeUrl = "https://osu.coffee/mode-mania2x.png"

        elementList = {
                    "Rank_prefix:#": res.pp_rank,
                    "NaN_1_parenthesisLeft":res.country,
                    "NaN_2_parenthesisRight_prefix:#":res.pp_country_rank,
                    "Accuracy_suffix:%":round(res.accuracy,2),
                    "Playcount": res.playcount,
                    "NaN_3_parenthesis_suffix:h": (res.total_seconds_played//60)//60,
                    "Level":math.trunc(res.level),
                    "separator:+":"",
                    "NaN_PercentageLevel_suffix:%":res.accuracy_percentage,
                    "Hit per play":res.hit_per_play,
                    "Playstyle":"need api2",
                    "Ranks":"",
                    "<:rankingSSH:840008774034391041>_noNewline_noDecorator_box":res.count_rank_ssh,
                    "<:rankingSS:840263037621501993>_noNewline_noDecorator_box":res.count_rank_ss,
                    "<:rankingSH:840263061248278550>_noNewline_noDecorator_box":res.count_rank_sh,
                    "<:rankingS:840263078674825257>_noNewline_noDecorator_box":res.count_rank_s,
                    "<:rankingA:840263110228312114>_noNewline_noDecorator_box":res.count_rank_a,
                }

        newEmbed = embedHandler(elementList,embedType=1,color=0xFF748C)
        newEmbed.setAuthor(name = str(res.username) + "'s " + gamemode + " profile", icon_url=gamemodeUrl, url=res.url)
        newEmbed.setThumbnail(res.profile_image)
        newEmbed.setFooter(text = "Joined on the " + str(res.join_date))
        return newEmbed.getEmbed()

    # Basic version of their profiles
    @commands.group(invoke_without_command=True, brief="osu command",description="give info about the user",aliases=["standard","Standard","std", "Std"], usage="m!osu")
    async def osu(self, ctx, username=None):
        '''
        Provide an embed containing basic osu!standard profile information.

        Parameters:
            ctx (obj): The context of the bot
            username (str/int/None): Argument that correspond to the username of the osu profile

        Return:
            embed: discord embed containing basic informaiton about the osu profile
        '''

        if username==None:
            username = self.osusetVerification(ctx.author.id)

        if username != None:
            return await ctx.send(embed = self.userProfile(username, "standard"))
        else:
            return await ctx.send("Enter your username or set your profile using the osuset command: ``m!osuset {username}``")

    @commands.group(invoke_without_command=True,brief="osu command",description="give info about the user",aliases=["fuits","catch", "Catch"], usage="m!ctb")
    async def ctb(self, ctx, username=None):
        '''
        Provide an embed containing basic osu!ctb profile information.

        Parameters:
            ctx (obj): The context of the bot
            username (str/int/None): Argument that correspond to the username of the osu profile

        Return:
            embed: discord embed containing basic informaiton about the osu profile
        '''

        if username==None:
            username = self.osusetVerification(ctx.author.id)

        if username != None:
            return await ctx.send(embed = self.userProfile(username, "ctb"))
        else:
            return await ctx.send("Enter your username or set your profile using the osuset command: ``m!osuset {username}``")

    @commands.group(invoke_without_command=True,brief="osu command",description="give info about the user",aliases=["Taiko"], usage="m!taiko")
    async def taiko(self, ctx, username=None):
        '''
        Provide an embed containing basic osu!taiko profile information.

        Parameters:
            ctx (obj): The context of the bot
            username (str/int/None): Argument that correspond to the username of the osu profile

        Return:
            embed: discord embed containing basic informaiton about the osu profile
        '''

        if username==None:
            username = self.osusetVerification(ctx.author.id)

        if username != None:
            return await ctx.send(embed = self.userProfile(username, "taiko"))
        else:
            return await ctx.send("Enter your username or set your profile using the osuset command: ``m!osuset {username}``")

    @commands.group(invoke_without_command=True,brief="osu command",description="give info about the user",aliases=["Mania"], usage="m!mania")
    async def mania(self, ctx, username=None):
        '''
        Provide an embed containing basic osu!mania profile information.

        Parameters:
            ctx (obj): The context of the bot
            username (str/int/None): Argument that correspond to the username of the osu profile

        Return:
            embed: discord embed containing basic informaiton about the osu profile
        '''

        if username==None:
            username = self.osusetVerification(ctx.author.id)

        if username != None:
            return await ctx.send(embed = self.userProfile(username, "mania"))
        else:
            return await ctx.send("Enter your username or set your profile using the osuset command: ``m!osuset {username}``")

    # Detailled version of their profiles
    @osu.command(name="d",description="Give detailled about the user",aliases=["-d"], usage="m!osu -d")
    async def osuDetailled(self,ctx):
        return await ctx.send("detailled ver of your profile (comming soon to you o!)")

    @ctb.command(name="d",description="Give detailled about the user",aliases=["-d"], usage="m!osu -d")
    async def ctbDetailled(self,ctx):
        return await ctx.send("detailled ver of your profile (comming soon to you c!)")

    @taiko.command(name="d",description="Give detailled about the user",aliases=["-d"], usage="m!osu -d")
    async def taikoDetailled(self,ctx):
        return await ctx.send("detailled ver of your profile (comming soon to you t!)")

    @mania.command(name="d",description="Give detailled about the user",aliases=["-d"], usage="m!osu -d")
    async def maniaDetailled(self,ctx):
        return await ctx.send("detailled ver of your profile (comming soon to you m!)")

    # Statistics version of their profiles
    @osu.command(name="s",description="Give detailled about the user",aliases=["-s"], usage="m!osu -d")
    async def osuStatistics(self,ctx):
        return await ctx.send("statistics ver of your profile (comming soon to you o!)")

    @ctb.command(name="s",description="Give detailled about the user",aliases=["-s"], usage="m!osu -d")
    async def ctbStatistics(self,ctx):
        return await ctx.send("statistics ver of your profile (comming soon to you c!)")

    @taiko.command(name="s",description="Give detailled about the user",aliases=["-s"], usage="m!osu -d")
    async def taikoStatistics(self,ctx):
        return await ctx.send("statistics ver of your profile (comming soon to you t!)")

    @mania.command(name="s",description="Give detailled about the user",aliases=["-s"], usage="m!osu -d")
    async def maniaStatistics(self,ctx):
        return await ctx.send("statistics ver of your profile (comming soon to you m!)")


    @commands.group(brief="osu command",description="link your discord with an osu profile", usage="m!osuset {user}")
    async def osuset(self, ctx, username):
        '''
        Associate a discord account with an osu! profile.

        Parameters:
            ctx (obj): The context of the bot
            username (str/int): Argument that correspond to the username of the osu profile

        Return:
            message (str), message saying wheter the osu profile has been set or has been updated.
        '''
        res = osuApiCall.get_user(username)[0]

        username = self.osusetVerification(ctx.author.id)

        if username != None:
            connection = sqlite3.connect('data/Users.db')
            cursor = connection.cursor()
            cursor.execute('UPDATE osuset SET osu_id=? WHERE discord_id=?',(res.user_id,ctx.author.id))
            connection.commit()
            connection.close()

            await ctx.send("Your osu! profile has been updated.")
        else:
            connection = sqlite3.connect('data/Users.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO osuset VALUES (?,?,?)',(ctx.author.id,res.user_id,"standard"))
            connection.commit()
            connection.close()

            return await ctx.send("Your osu! profile has been set.")

    @osuset.command(name="-gamemode")
    async def gamemode(self,ctx, arg):
        return await ctx.send("soonTM")

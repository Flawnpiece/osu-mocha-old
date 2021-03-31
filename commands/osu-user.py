import discord                      # type: ignore
from discord.ext import commands    # type: ignore
from main import osuApiCall          # type: ignore
from embedHandler import embedHandler
import osuapi
import sqlite3
import math
def setup(bot):
    bot.add_cog(osu(bot))



class osu(commands.Cog):

    def __init__(self,bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("missing args as osuset isn't there yet")

    def userProfile(self,arg,gamemode):
        if type(arg) == int:
            pass
        else:
            if arg.isdigit():
                arg = int(arg)

        if gamemode == "standard":
            res = osuApiCall.get_user(username=arg)[0]
        if gamemode == "taiko":
            res = osuApiCall.get_user(arg,mode=osuapi.enums.OsuMode.taiko)[0]
        if gamemode == "ctb":
            res = osuApiCall.get_user(arg,mode=osuapi.enums.OsuMode.ctb)[0]
        if gamemode == "mania":
            res = osuApiCall.get_user(arg,mode=osuapi.enums.OsuMode.mania)[0]



        elementList = {
                    "Rank_prefix:#": res.pp_rank,
                    "NaN_1_parenthesisLeft":res.country,
                    "NaN_2_parenthesisRight_prefix:#":res.pp_country_rank,
                    "Accuracy_suffix:%":round(res.accuracy,2),
                    "Playcount": res.playcount,
                    "NaN_3_parenthesis_suffix:h": (res.total_seconds_played//60)//60,
                    "Level":math.trunc(res.level),
                    "NaN_PercentageLevel_prefix:+_suffix:%":res.accuracy_percentage,
                    "Hit per play":res.hit_per_play

                }

        newEmbed = embedHandler(elementList,embedType=1,color=0xFF748C)


        newEmbed.setAuthor(name= str(res.username) + "'s " + gamemode + " profile", url=res.url, icon_url=res.profile_image)
        newEmbed.setFooter(text = "Joined on the " + str(res.join_date))
        return newEmbed.getEmbed()

    @commands.command(brief="osu command",description="give info about the user",aliases=["standard","Standard","std", "Std"], usage="m!osu")
    async def osu(self,ctx, arg=None):

        if arg==None:
            connection = sqlite3.connect('data/Users.db')
            cursor = connection.cursor()
            cursor.execute("SELECT osu_id FROM osuset WHERE discord_id=?", (ctx.author.id,))
            databaseSection = cursor.fetchone()
            if databaseSection!= None:
                arg=databaseSection[0]
            else:
                await ctx.send("Enter your username or set your profile using the osuset command!")

        await ctx.send(embed = self.userProfile(arg, "standard"))

    @commands.command(brief="osu command",description="give info about the user",aliases=["fuits","catch", "Catch"], usage="m!ctb")
    async def ctb(self,ctx, arg=None):
        if arg==None:
            connection = sqlite3.connect('data/Users.db')
            cursor = connection.cursor()
            cursor.execute("SELECT osu_id FROM osuset WHERE discord_id=?", (ctx.author.id,))
            databaseSection = cursor.fetchone()
            if databaseSection!= None:
                arg=databaseSection[0]
            else:
                await ctx.send("Enter your username or set your profile using the osuset command!")

        await ctx.send(embed = self.userProfile(arg, "ctb"))

    @commands.command(brief="osu command",description="give info about the user",aliases=["Taiko"], usage="m!taiko")
    async def taiko(self,ctx, arg=None):
        if arg==None:
            connection = sqlite3.connect('data/Users.db')
            cursor = connection.cursor()
            cursor.execute("SELECT osu_id FROM osuset WHERE discord_id=?", (ctx.author.id,))
            databaseSection = cursor.fetchone()
            if databaseSection!= None:
                arg=databaseSection[0]
            else:
                await ctx.send("Enter your username or set your profile using the osuset command!")

        await ctx.send(embed = self.userProfile(arg, "taiko"))

    @commands.command(brief="osu command",description="give info about the user",aliases=["Mania"], usage="m!mania")
    async def mania(self,ctx, arg=None):
        if arg==None:
            connection = sqlite3.connect('data/Users.db')
            cursor = connection.cursor()
            cursor.execute("SELECT osu_id FROM osuset WHERE discord_id=?", (ctx.author.id,))
            databaseSection = cursor.fetchone()
            if databaseSection!= None:
                arg=databaseSection[0]
            else:
                await ctx.send("Enter your username or set your profile using the osuset command!")

        await ctx.send(embed = self.userProfile(arg, "mania"))

    @commands.command(brief="osu command",description="link your discord with an osu profile", usage="m!osuset {user}")
    async def osuset(self,ctx,arg):


        res = osuApiCall.get_user(arg)[0]

        connection = sqlite3.connect('data/Users.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM osuset WHERE discord_id=?", (ctx.author.id,))
        databaseSection = cursor.fetchone()

        if databaseSection != None:
            cursor.execute("UPDATE osuset SET osu_id=? WHERE discord_id=?",(res.user_id,ctx.author.id))
            connection.commit()
            connection.close()

            await ctx.send("Your osu profile has been updated")
        else:
            cursor.execute("INSERT INTO osuset VALUES (?,?,?)",(ctx.author.id,res.user_id,"standard"))
            connection.commit()
            connection.close()

            await ctx.send("Your osu profile has been set")

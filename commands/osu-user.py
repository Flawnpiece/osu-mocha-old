import discord                      # type: ignore
from discord.ext import commands    # type: ignore
from main import osuApiCall          # type: ignore
from embedHandler import embedHandler
import osuapi
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
        if gamemode == "standard":
            res = osuApiCall.get_user(arg)[0]
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
                    "Level":round(res.level,0),
                    "NaN_PercentageLevel_prefix:+_suffix:%":round((res.level-round(res.level,0))*100,2),
                    "Hit per play":round(res.total_hits/res.playcount,2)

                }

        newEmbed = embedHandler(elementList,embedType=1,color=0xFF748C)


        newEmbed.setAuthor(name= str(res.username) + "'s " + gamemode + " profile", url=res.url, icon_url=res.profile_image)
        newEmbed.setFooter(text = "Joined on the " + str(res.join_date))
        return newEmbed.getEmbed()

    @commands.command()
    async def osu(self,ctx, arg):

        await ctx.send(embed = self.userProfile(arg, "standard"))

    @commands.command()
    async def ctb(self,ctx, arg):

        await ctx.send(embed = self.userProfile(arg, "ctb"))

    @commands.command()
    async def taiko(self,ctx, arg):

        await ctx.send(embed = self.userProfile(arg, "taiko"))

    @commands.command()
    async def mania(self,ctx, arg):

        await ctx.send(embed = self.userProfile(arg, "mania"))

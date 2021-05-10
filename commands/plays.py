import discord                      # type: ignore
from discord.ext import commands    # type: ignore
from main import osuApiCall          # type: ignore
from embedHandler import embedHandler
import osuapi
import sqlite3
import math
from datetime import datetime
def setup(bot):
    bot.add_cog(plays(bot))



class plays(commands.Cog):
    '''
    This cog regroup commands related to an user plays

    Commands :
        - top plays
        - recent
        - compare
    '''
    def __init__(self,bot):
        '''
        The constructor of the plays cog.

        Parameters:
            bot (obj): instance of the bot
        '''
        self.bot = bot

    @commands.command(aliases=["c","Compare"], description="Showcase your score on a certain map", usage="m!compare | m!c")
    async def compare(self,ctx, arg=None):
        '''
        Give the user scores on the lastest beatmap in the chat.

        Parameters:
            ctx (obj): context for the bot
            arg (int/str): username or id of the play to compare (can be blank if username was already set)

        Returns:
            embed : Contains every information for the score
        '''
        if arg==None:
            connection = sqlite3.connect('data/Users.db')
            cursor = connection.cursor()

            cursor.execute("SELECT osu_id FROM osuset WHERE discord_id=?", (ctx.author.id,))
            databaseSection = cursor.fetchone()
            if databaseSection!= None:
                arg=databaseSection[0]
            else:
                await ctx.send("Enter your username or set your osu profile using the osuset command! : m!osuset {username}")

        res = osuApiCall.get_scores(beatmap_id=self.beatmap_id, username=arg)
        score = res[0]

        res2 = osuApiCall.get_beatmaps(beatmap_id=self.beatmap_id)
        beatmap = res2[0]

        mapLink= "https://osu.ppy.sh/beatmapsets/" + str(beatmap.beatmapset_id) + "#osu/" + str(beatmap.beatmap_id)

        elementList = {}
        i = 0
        elementList["NaN_decorator:✦"+str(i)]=str(i+1)+"."
        elementList["NaN_noDecoration_bracketLeft_"+str(i)]=beatmap.artist
        elementList["separator:-"+str(i)]=""
        elementList["NaN_title"+str(i)]=beatmap.title
        elementList["separator:|"+str(i)]=""
        elementList["NaN_beatmapVersion_bracketRight"+str(i)]=beatmap.version
        elementList["link"+str(i)]=mapLink
        elementList["NaN_modsUsed_decorator:▸_"+str(i)]=res[i].enabled_mods
        elementList["NaN_pp_newline_decorator:▸"+str(i)]=str(int(round(res[i].pp,0)))+"pp"
        elementList["NaN_owncombo_decorator:▸"+str(i)]=res[i].maxcombo
        elementList["NaN_comboseparator:/"+str(i)]:""
        elementList["NaN_mapcombo_"+str(i)]=beatmap.max_combo
        elementList["NaN_accuracy_decorator:▸_suffix:%"+str(i)]=round(score.accuracy(mode=osuapi.enums.OsuMode.osu)*100,2)
        elementList["NaN_count300_bracketLeft_decorator:▸"+str(i)]=score.count300
        elementList["NaN_300/100parator:/"+str(i)]:""
        elementList["NaN_count100"+str(i)]=score.count100
        elementList["NaN_100/50parator:/"+str(i)]:""
        elementList["NaN_count50"+str(i)]=score.count50
        elementList["NaN_50/missparator:/"+str(i)]:""
        elementList["NaN_countmiss+bracketRight"+str(i)]=score.countmiss
        elementList["newline_"+str(i)]=""

        newEmbed = embedHandler(elementList,embedType=1,color=0xFF748C)

        newEmbed.setAuthor(name= "Top osu plays for "+ str(arg))
        newEmbed.setFooter(text="ill see")

        DaEmbed = newEmbed.getEmbed()
        await ctx.send(embed = DaEmbed)
        
    def userRecent(self,arg,gamemode):

        def playedOn(dateInUTC):
            now = datetime.now()
            hours = now.hour + 4
            minutes = now.minute
            secondes = now.second
            print(hours, minutes, secondes)
            d = 24 - dateInUTC.hour

            print(hours + d)
            return "4"

        if type(arg) == int:
            pass
        else:
            if arg.isdigit():
                arg = int(arg)

        if gamemode == "standard":
            recent = osuApiCall.get_user_recent(username=arg)[0]
            user = osuApiCall.get_user(username=arg)[0]
            beatmap = osuApiCall.get_beatmaps(beatmap_id=recent.beatmap_id)[0]
            print("user : ", user)

        if gamemode == "taiko":
            res = osuApiCall.get_user_recent(arg,mode=osuapi.enums.OsuMode.taiko)
        if gamemode == "ctb":
            res = osuApiCall.get_user_recent(arg,mode=osuapi.enums.OsuMode.ctb)
        if gamemode == "mania":
            res = osuApiCall.get_user_recent(arg,mode=osuapi.enums.OsuMode.mania)

        mapLink= "https://osu.ppy.sh/beatmapsets/" + str(beatmap.beatmapset_id) + "#osu/" + str(beatmap.beatmap_id)

        cogMap = self.bot.get_cog("map")
        cogMap.setBeatmapInformation(mapLink)

        #need a separator without space between, meanwhile :
        combo = str(recent.maxcombo) + "/" + str(beatmap.max_combo)
        count = "[" + str(recent.count300) + "/" + str(recent.count100) + "/" + str(recent.count50) + "/" + str(recent.countmiss) + "]"

        print(len("M2U & Gentle Stick - Hades in the Heaven [Aquosity]"))

        elementList = {

                    "NaN_decorator:✦":"",
                    "NaN_noDecoration_bracketLeft":beatmap.artist,
                    "separator:-":"",
                    "NaN_title":beatmap.title,
                    "NaN_beatmapVersion_bracketRight":"["+str(beatmap.version)+"]",
                    "link":mapLink,
                    "NaN_modsUsed_decorator:▸":recent.enabled_mods,
                    "NaN_rank_newline_decorator:▸":recent.rank,
                    "NaN_score_decorator:▸":recent.score,
                    "NaN_pp_decorator:▸":str(round(cogMap.oppaiMapInfo.getPP(n300 = recent.count300, n100= recent.count100, n50 = recent.count50, misses=recent.countmiss, combo=recent.maxcombo).total_pp,2))+"pp",
                    "NaN_combo_decorator:▸":combo,
                    "NaN_accuracy_decorator:▸_suffix:%":round(recent.accuracy(mode=osuapi.enums.OsuMode.osu)*100,2),
                    "NaN_count300m!_decorator:▸_box":count,
                    "Played on ":playedOn(recent.date),
                      }

        newEmbed = embedHandler(elementList,embedType=1,color=0xFF748C)

        newEmbed.setAuthor(name= str(user.username) + "'s " + gamemode + " most recent play", url=user.url, icon_url=user.profile_image)
        newEmbed.setFooter(text = "gg bg")
        newEmbed.setThumbnail(url=beatmap.cover_thumbnail)
        return newEmbed.getEmbed()
    def userTop(self,arg,gamemode):
        if type(arg) == int:
            pass
        else:
            if arg.isdigit():
                arg = int(arg)

        if gamemode == "standard":
            res = osuApiCall.get_user_best(username=arg)
            user = osuApiCall.get_user(username=arg)[0]
            print("user : ", user)

        if gamemode == "taiko":
            res = osuApiCall.get_user_best(arg,mode=osuapi.enums.OsuMode.taiko)
        if gamemode == "ctb":
            res = osuApiCall.get_user_bestr(arg,mode=osuapi.enums.OsuMode.ctb)
        if gamemode == "mania":
            res = osuApiCall.get_user_best(arg,mode=osuapi.enums.OsuMode.mania)

        elementList = {}
        i = 0
        while i<5:
            beatmap = osuApiCall.get_beatmaps(beatmap_id=res[i].beatmap_id)[0]
            score = osuApiCall.get_scores(username=arg,beatmap_id=res[i].beatmap_id)[0]
            mapLink= "https://osu.ppy.sh/beatmapsets/" + str(beatmap.beatmapset_id) + "#osu/" + str(beatmap.beatmap_id)

            elementList["NaN_decorator:✦"+str(i)]=str(i+1)+"."
            elementList["NaN_noDecoration_bracketLeft_"+str(i)]=beatmap.artist
            elementList["separator:-"+str(i)]=""
            elementList["NaN_title"+str(i)]=beatmap.title
            elementList["separator:|"+str(i)]=""
            elementList["NaN_beatmapVersion_bracketRight"+str(i)]=beatmap.version
            elementList["link"+str(i)]=mapLink
            elementList["NaN_modsUsed_decorator:▸_"+str(i)]=res[i].enabled_mods.shortname
            elementList["NaN_pp_newline_decorator:▸"+str(i)]=str(int(round(res[i].pp,0)))+"pp"
            elementList["NaN_owncombo_decorator:▸"+str(i)]=res[i].maxcombo
            elementList["NaN_comboseparator:/"+str(i)]:""
            elementList["NaN_mapcombo_"+str(i)]=beatmap.max_combo
            elementList["NaN_accuracy_decorator:▸_suffix:%"+str(i)]=round(score.accuracy(mode=osuapi.enums.OsuMode.osu)*100,2)
            elementList["NaN_count300_bracketLeft_decorator:▸"+str(i)]=score.count300
            elementList["NaN_300/100parator:/"+str(i)]:""
            elementList["NaN_count100"+str(i)]=score.count100
            elementList["NaN_100/50parator:/"+str(i)]:""
            elementList["NaN_count50"+str(i)]=score.count50
            elementList["NaN_50/missparator:/"+str(i)]:""
            elementList["NaN_countmiss+bracketRight"+str(i)]=score.countmiss
            elementList["newline_"+str(i)]=""

            i = i + 1




        newEmbed = embedHandler(elementList,embedType=1,color=0xFF748C)



        newEmbed.setAuthor(name= str(user.username) + "'s " + gamemode + " toplays", url=user.url, icon_url=user.profile_image)
        newEmbed.setFooter(text = "yea")
        return newEmbed.getEmbed()


    @commands.command(brief="osu command",description="give osu top plays", usage="m!osutop")
    async def osutop(self,ctx, username=None):
        '''
        Provide an embed containing basic osu!standard profile information.

        Parameters:
            ctx (obj): The context of the bot
            username (str/int/None): Argument that correspond to the username of the osu profile

        Return:
            embed: discord embed containing basic informaiton about the osu profile
        '''

        if username==None:
            username = osusetVerification(ctx.author.id)

        if username != None:
            return await ctx.send(embed = self.userProfile(username, "standard"))

    @commands.command(brief="osu command",description="give osu top plays", aliases=["rs"],usage="m!recent")
    async def recent(self,ctx, username=None):
        '''
        Provide an embed containing basic osu!standard profile information.

        Parameters:
            ctx (obj): The context of the bot
            username (str/int/None): Argument that correspond to the username of the osu profile

        Return:
            embed: discord embed containing basic informaiton about the osu profile
        '''

        if username==None:

            cogProfile = self.bot.get_cog("profile")
            username = cogProfile.osusetVerification(ctx.author.id)

        if username != None:
            return await ctx.send(embed = self.userRecent(username, "standard"))

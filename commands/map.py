import discord                      # type: ignore
from discord.ext import commands    # type: ignore
from main import osuApiCall          # type: ignore
from embedHandler import embedHandler
import osuapi
import sqlite3
import oppadc
from zipfile import ZipFile
import wget
import os

def setup(bot):
    bot.add_cog(map(bot))

class map(commands.Cog):

    def __init__(self,bot):
        '''
        The constructor of the map cog.

        Parameters:
            bot (obj): instance of the bot
        '''
        self.bot = bot

    def setBeatmapInformation(self, message):
        '''
        Set the beatmap_id and OppaiMapInfo as an class attribute.

        Parameters:
            message (obj): The message with the associated information

        Return:
            Nothing, this function simply sets attributes
        '''
        index = message.content.rindex("/")

        # set beatmap_id as an attribute for the whole class
        self.beatmap_id = message.content[index+1:]

        res = osuApiCall.get_beatmaps(beatmap_id=self.beatmap_id)
        beatmap = res[0]


        # Before downloading the mapset we will remove the existing files
        for file in os.listdir('C:/Users/DELL/Desktop/osu-mocha/map_cache/'):
            os.remove(os.path.join('C:/Users/DELL/Desktop/osu-mocha/map_cache/', file))

        #Downloading the mapset
        url = 'https://nerina.pw/d/' + str(beatmap.beatmapset_id)
        wget.download(url, 'C:/Users/DELL/Desktop/osu-mocha/map_cache/' + self.beatmap_id + ".osz")

        # osz are compressed files, we can basically open them with zip
        pathFile = ""
        with ZipFile('C:/Users/DELL/Desktop/osu-mocha/map_cache/' + self.beatmap_id + '.osz', 'r') as zip:

                for filename in zip.namelist():
                    # Search for the map itself
                    if filename.endswith('.osu') and filename.find(beatmap.version) != -1:
                        zip.extract(filename,'C:/Users/DELL/Desktop/osu-mocha/map_cache/')
                        pathFile = 'C:/Users/DELL/Desktop/osu-mocha/map_cache/' + filename
                        break

        # set oppaiMapInfo as an attribute for the whole class
        self.oppaiMapInfo = oppadc.OsuMap(file_path=pathFile)

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        print("on_command_error : ", error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("some error")

    @commands.Cog.listener()
    async def on_message(self,message):
        '''
        Add a reaction to the message an call setBeatmapInformation().

        Parameters:
            message (obj): The message with the associated information

        Return:
            Reaction on the initial message
        '''

        if message.content.find("https://osu.ppy.sh/beatmapsets/") == 0:

            self.setBeatmapInformation(message)

            return await message.add_reaction('☄️')

    @commands.command(aliases=["m"], description="Showcase your score on a certain map", usage="m!compare | m!c")
    async def map(self,ctx):
        return await ctx.send("not there yet")

    def mapEmbed(self):
        def diffEmote(starRating):
            '''
            Apply the correct difficulty emote depending on the star rating of the map.

            Parameters:
                starRating (float): Star rating of the current map

            Returns:
                emote (str): discord emote reprensting the difficulty of the map
            '''
            if starRating < 2:
                return "<:easy:837747972099014717>"
            elif starRating < 2.70:
                return "<:normal:837748258838544474>"
            elif starRating < 4.00:
                return "<:hard:837748285690871871>"
            elif starRating < 5.30:
                return "<:insane:837748311573397546>"
            elif starRating < 6.50:
                return "<:expert:837748338501353532>"
            elif starRating >= 6.5:
                return "<:expertplus:837748363797200927>"

        def lengthFormat(length):
            '''
            Convert the map length from seconds to minutes and seconds

            Parameters:
                length (int): Lenght of the map in seconds

            Returns:
                minute:seconds (str): Lenght displayed as minutes:seconds
            '''
            min = length //60
            sec = length - min*60

            return "{}:{}".format(min,sec)

        def statusOnDate(status,date):
            '''
            Output the status of the map alongside the date corresponding to that status.

            Parameters:
                status (obj): the status of the map
                date (obj): a date format

            Returns:
                status:date (str): status of the map alongside the date
            '''
            approvedStatus = {4:"Loved", 3:"Qualified", 2:"Approved", 1 : "Ranked", 0 : "Pending", -1 : "WIP", -2 :" Graveyard"}
            print(type(status))
            status = approvedStatus[status.value]

            return "{} on {}".format(status, date.date())

        res = osuApiCall.get_beatmaps(beatmap_id=self.beatmap_id)
        beatmap = res[0]

        mapLink= "https://osu.ppy.sh/beatmapsets/" + str(beatmap.beatmapset_id) + "#osu/" + str(beatmap.beatmap_id)

        elementList = {"NaN_artist_bracketLeft_decorator:✦":beatmap.artist,
        "separator:-":"",
        "NaN_title":beatmap.title,
        "NaN_by":"by",
        "NaN_mapper_bracketRight":beatmap.creator,
        "link":mapLink,
        "newline":"",
        "NaN_diffemote":diffEmote(beatmap.difficultyrating),
        "separator:-_1":"",
        "NaN_diffname":beatmap.version,
        "Difficulty":round(beatmap.difficultyrating,2),
        "Length_noNewline":lengthFormat(beatmap.total_length),
        "BPM":beatmap.bpm,
        "Maxcombo_noNewline":beatmap.max_combo,
        "AR":beatmap.diff_approach,
        "OD_noDecoration_noNewline":beatmap.diff_overall,
        "HP_noDecoration_noNewline":beatmap.diff_drain,
        "CS_noDecoration_noNewline":beatmap.diff_size,
        "PP":" ",
        "95%_noNewline_noDecorator":str(round(self.oppaiMapInfo.getPP(accuracy=95.00).total_pp,2)),
        "97%_noNewline_noDecorator":str(round(self.oppaiMapInfo.getPP(accuracy=97.00).total_pp,2)),
        "99%_noNewline_noDecorator":str(round(self.oppaiMapInfo.getPP(accuracy=99.00).total_pp,2)),
        "100%_noNewline_noDecorator":str(round(self.oppaiMapInfo.getPP(accuracy=100.00).total_pp,2))}

        newEmbed = embedHandler(elementList,embedType=1,color=0xFF748C)

        newEmbed.setAuthor(name= "Map information")
        newEmbed.setFooter(text=" {0} | {1} ♡".format(statusOnDate(beatmap.approved,beatmap.approved_date),beatmap.favourite_count))
        newEmbed.setImage(url=beatmap.cover_image)

        return newEmbed.getEmbed()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        '''
        When a reaction is added an embed is sent with the map property

        Parameters:
            reaction (obj): The reaction itself and its attributes
            user (obj): *not used, but it is required.

        Returns:
            The embed containing all the information
        '''
        reactions = reaction.message.reactions[0]
        message = reaction.message

        if reactions.count>1 :

            await message.channel.send(embed = self.mapEmbed())

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

    @commands.command(aliases=["a","acc"], description="Showcase your score on a certain map", usage="m!compare | m!c")
    async def accuracy(self,ctx, acc=None):
        '''
        Give the amount of pp for a map based on the accuracy the user provides.

        Parameters:
            ctx (obj): context for the bot
            acc (int/float): The accuracy to base the pp on

        Returns:
            message (str): the amount of pp for the acc provided
        '''
        if acc != None:
            await ctx.send("Amount of pp for " + acc + "% is " + str(round(self.oppaiMapInfo.getPP(accuracy=float(acc)).total_pp,2)))
        else:
            await ctx.send("Enter an accuracy!")


    @commands.command(description="Showcase your score on a certain map", usage="m!compare | m!c")
    async def pp(self,ctx, arg=None):
        '''
        Give the amount of acc for a map based on the pp the user provides.

        Parameters:
            ctx (obj): context for the bot
            arg (int/float): the pp corresponding to the accuracy this command search

        Returns:
            message (str): the amount of acc needed for the pp provided
        '''
        if arg != None:
            minAcc = 0.00
            maxAcc = 100.00

            maxPP = round(self.oppaiMapInfo.getPP().total_pp,2)
            if float(arg) < 0:
                await ctx.send("send correct value pls")
            elif float(arg) > maxPP:
                await ctx.send("The pp value you entered is bigger than the max acheviable")
            else :

                while minAcc < maxAcc-00.01:
                    midAcc = (minAcc + maxAcc) / 2
                    pp = round(self.oppaiMapInfo.getPP(accuracy=float(midAcc)).total_pp,2)
                    if float(arg) > pp:
                        minAcc = midAcc
                    elif float(arg) < pp:
                        maxAcc = midAcc

                await ctx.send("To get " +  arg + "pp, you need to fc the map with " + str(round(maxAcc,2)) + "%")
        else:
            await ctx.send("Enter an pp!")

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
    '''
    This cog regroup commands related to maps

    Commands :
        - map (also as an event) : output information concerning the map that was linked
        - pp : gives the accuracy you need to achieve the pp the user entered.
        - acc : gives the amount of pp for the entered accuracy
    '''
    def __init__(self,bot):
        '''
        The constructor of the map cog.

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

    @commands.Cog.listener()
    async def on_message(self,message):
        '''
        If the message is a beatmap link, it add a reaction to the message and call setBeatmapInformation().

        Parameters:
            message (obj): The message with the associated information

        Return:
            Reaction on the initial message
        '''

        if message.content.find("https://osu.ppy.sh/beatmapsets/") == 0:
            self.setBeatmapInformation(message.content)

            return await message.add_reaction('☄️')

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

    def setBeatmapInformation(self, message, redownload=None):
        '''
        Set the beatmap_id and OppaiMapInfo as an class attribute.

        Parameters:
            message* (obj): The message with the associated information
                    *need to be a link

            redownloa : by default it set to None, so each map get download, if it's set to something
                        the mapset don't get redownloaded
        Return:
            Nothing, this function simply sets attributes
        '''

        # Detects if modes where added after the link
        space = message.find(" ")

        if space != -1:
            self.mods = message[space+1:]
            self.mods = self.mods.upper()
            space = 1
        else:
            self.mods = None
            space = 0

        # set beatmap_id as an attribute for the whole class
        index = message.rindex("/")

        if self.mods != None:
            self.beatmap_id = message[index+1:-len(self.mods)-space]
        else :
            self.beatmap_id = message[index+1:]

        res = osuApiCall.get_beatmaps(beatmap_id=self.beatmap_id)
        beatmap = res[0]

        resMapset= osuApiCall.get_beatmaps(beatmapset_id=beatmap.beatmapset_id)

        mapsetUnsorted = {}
        for v in resMapset:
            mapsetUnsorted[v]=v.difficultyrating

        self.mapset=list(dict(sorted(mapsetUnsorted.items(),key= lambda x:x[1])))

        # Before downloading the mapset we will remove the existing files and then we'll download the mapset
        if redownload == None:
            for file in os.listdir('C:/Users/DELL/Desktop/osu-mocha/map_cache/'):
                os.remove(os.path.join('C:/Users/DELL/Desktop/osu-mocha/map_cache/', file))

            url = 'https://nerina.pw/d/' + str(beatmap.beatmapset_id)
            wget.download(url, 'C:/Users/DELL/Desktop/osu-mocha/map_cache/' + str(beatmap.beatmapset_id) + ".osz")

        # osz are compressed files, we can basically open them with zip
        pathFile = ""
        with ZipFile('C:/Users/DELL/Desktop/osu-mocha/map_cache/' + str(beatmap.beatmapset_id) + '.osz', 'r') as zip:
            for filename in zip.namelist():
                if  filename.endswith('.osu') and filename.find(beatmap.version) != -1:
                    zip.extract(filename,'C:/Users/DELL/Desktop/osu-mocha/map_cache/')
                    pathFile = 'C:/Users/DELL/Desktop/osu-mocha/map_cache/' + filename

        self.oppaiMapInfo = oppadc.OsuMap(file_path=pathFile)

    def mapEmbed(self):
        '''
        Create the embed containg the beatmap informations.

        Returns:
             Embed, containing the beatmap informations.
        '''

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
            if self.mods != None:
                if self.mods.find("DT") != -1 or self.mods.find("NC") != -1:
                    length = length * 2/3
                elif self.mods.find("HT") != -1:
                    length = length * 4/3


            min = length //60
            sec = length - min*60
            sec = round(sec,0)

            # to avoid having .0
            if type(min) != int:
                if min.is_integer():
                    min = int(min)
            if type(sec) != int:
                if sec.is_integer():
                    sec = int(sec)

            if sec == 0:
                sec = "00"
            if sec < 10:
                sec = "0" + str(sec)

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
            status = approvedStatus[status.value]

            return "{} on {}".format(status, date.date())

        def showMods(mods):
            '''
            Output the mods applied to the map. (it's to avoid displaying mods that dont exist)

            Parameters:
                mods (str/None): the mods used

            Returns:
                mods (string): the mods that will show on the embed.

            * Known issues, if multiple mods are combined and one have an error it still shows them
                ex: FLAE --> map will be calculated with FL but it still shows "AE"
            '''
            if type(mods) != str:
                return "NM"
            else:
                modsDisplay = ["NF", "EZ", "HD", "HR", "DT", "NC" "SD", "FL", "SO"]
                for v in modsDisplay:
                    if mods.find(v) != -1:
                        return "+" + mods
                else:
                    return "NM"

        res = osuApiCall.get_beatmaps(beatmap_id=self.beatmap_id)
        beatmap = res[0]

        mapLink= "https://osu.ppy.sh/beatmapsets/" + str(beatmap.beatmapset_id) + "#osu/" + str(beatmap.beatmap_id)

        # *this is needed, we can't set specifics mods for the getStats so I'm putting it here and the sr takes it with the mods applied.
        self.oppaiMapInfo.getPP(Mods=self.mods)

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
        "NaN_box":showMods(self.mods),
        "Difficulty":round(self.oppaiMapInfo.getStats().total,2),
        "Length_noNewline":lengthFormat(beatmap.total_length),
        "BPM":beatmap.bpm,
        "Max Combo_noNewline":beatmap.max_combo,
        "AR":round(self.oppaiMapInfo.getDifficulty().ar,2),
        "OD_noDecoration_noNewline":round(self.oppaiMapInfo.getDifficulty().od,2),
        "HP_noDecoration_noNewline":round(self.oppaiMapInfo.getDifficulty().hp,2),
        "CS_noDecoration_noNewline":round(self.oppaiMapInfo.getDifficulty().cs,2),
        "PP":" ",
        "95%_noNewline_noDecorator":str(round(self.oppaiMapInfo.getPP(Mods=self.mods, accuracy=95.00).total_pp,2)),
        "99%_noNewline_noDecorator":str(round(self.oppaiMapInfo.getPP(Mods=self.mods, accuracy=99.00).total_pp,2)),
        "100%_noNewline_noDecorator":str(round(self.oppaiMapInfo.getPP(Mods=self.mods, accuracy=100.00).total_pp,2))}

        newEmbed = embedHandler(elementList,embedType=1,color=0xFF748C)

        i = 0
        while i < len(self.mapset):
            if self.mapset[i].version == beatmap.version:
                break
            i = i + 1

        newEmbed.setAuthor(name= "Map information")
        newEmbed.setFooter(text=" {0} | {1} ♡ | {2}".format(statusOnDate(beatmap.approved,beatmap.approved_date),beatmap.favourite_count, "Map " + str(i+1) + " on " + str(len(self.mapset))))
        newEmbed.setImage(url=beatmap.cover_image)

        return newEmbed.getEmbed()

    @commands.command(brief="osu command",aliases=["m"], description="Showcase a beatmap information", usage="m!map {mods}")
    async def map(self,ctx,arg=None):
        '''
        Showcase a beatmap information.

        Parameters:
            message (ctx): The bot context
            arg (string): the mods that should be applied (by default it is bound to None aka NoMod)

        Return:
            Embed, output an embed that was defined in mapEmbed()
        '''

        if arg!=None:

            if arg.find("+") != -1 or arg.find("-") != -1:
                i = 0

                while i < len(self.mapset):
                    if str(self.mapset[i].beatmap_id) == self.beatmap_id:
                        break
                    i = i + 1

                if arg.find("+") != -1:
                    mapLink = "https://osu.ppy.sh/beatmapsets/" + str(self.mapset[i+1].beatmapset_id) + "#osu/" + str(self.mapset[i+1].beatmap_id)
                    self.setBeatmapInformation(mapLink, redownload="dontRedownload")
                if arg.find("-") != -1:
                    mapLink= "https://osu.ppy.sh/beatmapsets/" + str(self.mapset[i-1].beatmapset_id) + "#osu/" + str(self.mapset[i-1].beatmap_id)
                    self.setBeatmapInformation(mapLink, redownload="dontRedownload")

            else:
                self.mods = arg.upper()

        else:
            self.mods = None

        return await ctx.send(embed = self.mapEmbed())

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

            if float(acc) < 0:
                return await ctx.send("Send a correct accuracy.")
            elif float(acc) > 100:
                return await ctx.send("The accuracy you entered is bigger than the maximum acheviable.")
            else :
                return await ctx.send("The amount of pp for " + acc + "% is " + str(round(self.oppaiMapInfo.getPP(Mods=self.mods,accuracy=float(acc)).total_pp,2)))
        else:
            return await ctx.send("Enter an accuracy!")

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

        print(arg)
        if arg != None:
            minAcc = 0.00
            maxAcc = 100.00
            maxPP = round(self.oppaiMapInfo.getPP(Mods=self.mods).total_pp,2)

            if float(arg) < 0:
                await ctx.send("Send a correct pp value.")
            elif float(arg) > maxPP:
                await ctx.send("The pp value you entered is bigger than the maximum acheviable on this map.")
            else :

                while minAcc < maxAcc-00.01:

                    midAcc = (minAcc + maxAcc) / 2
                    print(minAcc, maxAcc,midAcc)
                    pp = round(self.oppaiMapInfo.getPP(Mods=self.mods,accuracy=float(midAcc)).total_pp,2)
                    if float(arg) > pp:
                        minAcc = midAcc
                    elif float(arg) < pp:
                        maxAcc = midAcc

                return await ctx.send("To get " + arg + "pp, you need to fc the map with " + str(round(maxAcc,2)) + "%")
        else:
            return await ctx.send("Enter the requested pp value!")

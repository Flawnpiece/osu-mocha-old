import discord # type: ignore

class embedHandler:
    def __init__(self,elementList,embedType,color):
        self.elementList = elementList
        self.embedType = embedType
        self.color = color

        self.embed = discord.Embed(description = self.setDescription(), color = discord.Color(self.color))


    def setDescription(self):
        ''' always 2 elements per line
        '''
        keys = list(self.elementList.keys())
        
        i=0
        keysFormat1 = []
        while i <len(keys):
            if keys[i].find("prefix") != -1 and keys[i].find("suffix") == -1:
                prefix = keys[i][keys[i].find("prefix")+7]
                keysFormat1.append(f"{prefix}{self.elementList.get(keys[i])}")

            elif keys[i].find("suffix") != -1 and keys[i].find("prefix") == -1 :
                suffix = keys[i][keys[i].find("suffix")+7]
                keysFormat1.append(f"{self.elementList.get(keys[i])}{suffix}")
            elif keys[i].find("prefix") != -1 and keys[i].find("suffix") != -1:
                prefix = keys[i][keys[i].find("prefix")+7]
                suffix = keys[i][keys[i].find("suffix")+7]
                keysFormat1.append(f"{prefix}{self.elementList.get(keys[i])}{suffix}")
            else :
                keysFormat1.append(f"{self.elementList.get(keys[i])}")
            i = i + 1

        keysFormat2 = []
        i = 0
        while i <len(keys):
            if keys[i].find("parenthesisLeft") != -1:

                keysFormat2.append(f"({keysFormat1[i]}")

            elif keys[i].find("parenthesisRight") != -1:

                keysFormat2.append(f"{keysFormat1[i]})")
            elif keys[i].find("parenthesis")!=-1 and (keys[i].find("Left") and keys[i].find("parenthesisRight")==-1):
                keysFormat2.append(f"({keysFormat1[i]})")
            else :
                keysFormat2.append(f"{keysFormat1[i]}")
            i = i + 1



        descriptionFormat = f""


        i = 0
        while i< len(keys):

            if keys[i].startswith("NaN"):

                descriptionFormat = descriptionFormat + f" {keysFormat2[i]}"

            else :
                word = keys[i].find("_")
                if word == -1:
                    lineName = keys[i]

                else:
                    lineName = keys[i][:word]
                descriptionFormat = descriptionFormat + f"\n ▸ **{lineName}: ** {keysFormat2[i]} "
            i = i + 1

        return descriptionFormat



    def setAuthor(self, name, url=None, icon_url=None):
        ''' Name is always needed
            url and icon_url are optionnal
        '''

        if url==None and icon_url==None:
            self.embed.set_author(name = name)

        if url!=None and icon_url==None:
            self.embed.set_author(name = name, url = url)

        if icon_url!=None and url==None:
            self.embed.set_author(name = name, icon_url = icon_url)

        if url!=None and icon_url!=None:
            self.embed.set_author(name = name, url = url, icon_url = icon_url)


    def setFooter(self, text, icon_url=None):
        ''' Name is always needed
            url is optionnal
        '''

        if icon_url==None:
            self.embed.set_footer(text = text)

        if icon_url!=None:
            self.embed.set_footer(text = text, icon_url = icon_url)


    def getDict(self):
        return self.elementList

    def getType(self):
        return self.embedType

    def getColor(self):
        return self.color



    def getEmbed(self):
        return self.embed

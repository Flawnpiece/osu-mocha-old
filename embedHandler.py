import discord # type: ignore

class embedHandler:
    ''' Create an embed with an uniform format
    '''
    def __init__(self,elementList,embedType,color):
        ''' elementList : A list of all the elements that will figure in the embed description
            embedType : For now it's useless since there is only one type
            color : the color border of the embed, execemple : 0xFF748C
        '''
        self.elementList = elementList
        self.embedType = embedType
        self.color = color

        self.embed = discord.Embed(description = self.setDescription(), color = discord.Color(self.color))


    def setDescription(self):
        ''' Call the embedFormatter class that handle the format of the description
        '''

        keys = list(self.elementList.keys())

        embedFormat = embedFormatter(keys, self.elementList)

        # set prefix and suffix
        # exemple : "title_prefix:~"
        embedFormat.prefixAndSuffix()

        # set brackets [(}])
        embedFormat.brackets()

        # set the lines, decorator and newlines
        embedDescription = embedFormat.descriptionFormatting()

        return embedDescription



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


    def setImage(self, url):
        ''' Url is needed
        '''

        self.embed.set_image(url=url)

    def getEmbed(self):
        return self.embed


class embedFormatter:
    ''' Format the description embed

        It is done following layers: 1. prefix and suffix
                                     2. brackets/box/parenthesis
                                     3. lines mangement (newline, decorator)
    '''
    def __init__(self,keys, elementList):
        self.keys = keys
        self.elementList = elementList
        self.keysFormat1 = []
        self.keysFormat2 = []
        self.descriptionFormat = ""


    def prefixAndSuffix(self):
        ''' Usage :
                prefix:?
                suffix:?

            Exemple :
                Input  : "Difficulty_suffix:✰":5.00
                Output :  Difficulty: 5.00✰

            *It directly put the element (?) beside without any spaces
        '''

        keysFormat1 = []

        i = 0
        while i <len(self.keys):
            if self.keys[i].find("prefix") != -1 and self.keys[i].find("suffix") == -1:
                prefix = self.keys[i][self.keys[i].find("prefix")+7]
                keysFormat1.append(f"{prefix}{self.elementList.get(self.keys[i])}")

            elif self.keys[i].find("suffix") != -1 and self.keys[i].find("prefix") == -1 :
                suffix = self.keys[i][self.keys[i].find("suffix")+7]
                keysFormat1.append(f"{self.elementList.get(self.keys[i])}{suffix}")

            elif self.keys[i].find("prefix") != -1 and self.keys[i].find("suffix") != -1:
                prefix = self.keys[i][self.keys[i].find("prefix")+7]
                suffix = self.keys[i][self.keys[i].find("suffix")+7]
                keysFormat1.append(f"{prefix}{self.elementList.get(self.keys[i])}{suffix}")

            else :
                keysFormat1.append(f"{self.elementList.get(self.keys[i])}")
            i = i + 1

        self.keysFormat1 = keysFormat1

    def brackets(self):
        ''' Elements : parenthesis/bracket/box/curlybrackets

            Usage :
                If the element is simply written, ex : "parenthesis"
                it puts parenthesis all around the element, ex : (5.00✰)

                if the keyword Left/Right is added, it only add the element on the
                specified side, ex : "bracketLeft" --> [5.00✰

        '''
        keysFormat2 = []
        i = 0

        while i <len(self.keys):

            # parenthesis
            if self.keys[i].find("parenthesisLeft") != -1:
                keysFormat2.append(f"({self.keysFormat1[i]}")

            elif self.keys[i].find("parenthesisRight") != -1:

                keysFormat2.append(f"{self.keysFormat1[i]})")
            elif self.keys[i].find("parenthesis")!=-1 and (self.keys[i].find("Left") and self.keys[i].find("parenthesisRight")==-1):
                keysFormat2.append(f"({self.keysFormat1[i]})")


            # brackets
            elif self.keys[i].find("bracketLeft") != -1:
                keysFormat2.append(f"[{self.keysFormat1[i]}")

            elif self.keys[i].find("bracketRight") != -1:
                keysFormat2.append(f"{self.keysFormat1[i]}]")

            elif self.keys[i].find("bracket")!=-1 and (self.keys[i].find("Left") and self.keys[i].find("bracketRight")==-1):
                keysFormat2.append(f"[{self.keysFormat1[i]}]")

            # box
            elif self.keys[i].find("boxLeft") != -1:
                keysFormat2.append(f"``{self.keysFormat1[i]}")

            elif self.keys[i].find("boxRight") != -1:
                keysFormat2.append(f"{self.keysFormat1[i]}``")

            elif self.keys[i].find("box")!=-1 and (self.keys[i].find("Left") and self.keys[i].find("boxRight")==-1):
                keysFormat2.append(f"``{self.keysFormat1[i]}``")

            # CurlyBrackets
            elif self.keys[i].find("curlybracketsLeft") != -1:
                element = f"{self.keysFormat1[i]}"
                keysFormat2.append("{" + element)

            elif self.keys[i].find("curlybracketsRight") != -1:
                element = f"{self.keysFormat1[i]}"
                keysFormat2.append(element + "}")

            elif self.keys[i].find("curlybrackets")!=-1 and (self.keys[i].find("Left") and self.keys[i].find("boxRight")==-1):
                element = f"{self.keysFormat1[i]}"
                keysFormat2.append("{" + element + "}")


            else :
                keysFormat2.append(f"{self.keysFormat1[i]}")
            i = i + 1


        self.keysFormat2 = keysFormat2

    def descriptionFormatting(self):
        ''' The descripion formatting is devided in two,
            first of it checks the begenning of the key.

            There is four options : NaN, newline, separator, link :

            - NaN : Simply add the element
                options :
                 - decorator : add ✦ at the start
                 - newline : add \n at the start

            - newline : Simply skip a line

            - separator : take the element specified and use it as a separator
                usage : separator:?

            - link : simply put the ( ) to make it as a link*

            *the previous element(s) need to be with brackets

            if none of those 4 options where used, it will take the format :
                key - value

            - Options : noDecoration, noNewline


        '''
        i = 0
        while i< len(self.keys):

            # If it starts with a ceratin keyword
            if self.keys[i].startswith("NaN"):

                if self.keys[i].find("decorator") != -1 and self.keys[i].find("newline") == -1:
                    position = self.keys[i].find("decorator")
                    decorator = self.keys[i][position+10:position+11]


                    self.descriptionFormat = self.descriptionFormat + f" {decorator} {self.keysFormat2[i]}"

                elif self.keys[i].find("decorator") == -1 and self.keys[i].find("newline") != -1:
                        self.descriptionFormat = self.descriptionFormat + f" \n {self.keysFormat2[i]}"

                elif self.keys[i].find("decorator") != -1 and self.keys[i].find("newline") != -1:
                    position = self.keys[i].find("decorator")
                    decorator = self.keys[i][position+10:position+11]
                    self.descriptionFormat = self.descriptionFormat + f" \n {decorator} {self.keysFormat2[i]}"
                else:
                    self.descriptionFormat = self.descriptionFormat + f" {self.keysFormat2[i]}"

            elif self.keys[i].startswith("newline"):
                self.descriptionFormat = self.descriptionFormat + "\n\n"

            elif self.keys[i].startswith("separator"):
                print("separator was called : ", self.keys[i])
                separator = self.keys[i][10:11]
                print("separator : " + separator)

                self.descriptionFormat = self.descriptionFormat + f" {separator}"

            elif self.keys[i].startswith("link"):
                link = self.keysFormat2[i]
                self.descriptionFormat = self.descriptionFormat + f"({link})"

            else :
                decorator = "▸"
                newline = "\n"

                word = self.keys[i].find("_")
                if word == -1:
                    lineName =self.keys[i]

                else:
                    lineName =self.keys[i][:word]

                if self.keys[i].find("noDecorator") != -1:
                    decorator = ""
                if self.keys[i].find("noNewline") != -1:
                    newline = ""

                self.descriptionFormat = self.descriptionFormat + f"{newline} {decorator} **{lineName}: ** {self.keysFormat2[i]}"

            i = i + 1

        return self.descriptionFormat

# Data class: Retrieves responses from file responses.csv
import csv

class Data:
    # Constructor:
    def __init__(self):

        # Response data FVs
        self.spamMessages = []
        self.niceMessages = []
        self.meanMessages = []
        self.botMessages = []
        self.subsistingMessages = []
        self.provokedMessages = []

        # Lobby data FVs
        self.lobbyCustomWords = []
        self.lobbyCustomRounds = 0
        self.lobbyDrawTime = 0
        self.lobbyCustomOnly = False

        # File reading FVs
        self.fileName = "responses.csv"
        self.readFile()

    def readFile(self):
        # CSV editing extension: https://marketplace.visualstudio.com/items?itemName=janisdd.vscode-edit-csv
        # python docs csv reader: https://docs.python.org/3/library/csv.html?highlight=read%20file

        # what datatype is csvfile?
        with open(self.fileName, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Read in the response rows
                if (row['SPAM'] != ""): self.spamMessages.append(row['SPAM'])
                if (row['NICE'] != ""): self.niceMessages.append(row['NICE'])
                if (row['MEAN'] != ""): self.meanMessages.append(row['MEAN'])
                if (row['BOT'] != ""): self.botMessages.append(row['BOT'])
                if (row['SUBSISTING'] != ""): self.subsistingMessages.append(row['SUBSISTING'])
                if (row['PROVOKED'] != ""): self.provokedMessages.append(row['PROVOKED'])

                # Read in the private lobby rows
                # Ternary syntax: [on_true] if [expression] else [on_false] 
                if (row['LOBBY CUSTOM WORDS'] != ""): self.lobbyCustomWords.append(row['LOBBY CUSTOM WORDS'])
                if (row['LOBBY CUSTOM ROUNDS'] != ""): self.lobbyCustomRounds = int(row['LOBBY CUSTOM ROUNDS'])
                if (row['LOBBY DRAW TIME'] != ""): self.lobbyDrawTime = int(row["LOBBY DRAW TIME"])
                if (row['LOBBY CUSTOM ONLY'] != ""): self.lobbyCustomOnly = True if row['LOBBY CUSTOM ONLY'] == "TRUE" else False

    def getSpamMessages(self):
        return self.spamMessages
    
    def getNiceMessages(self):
        return self.niceMessages
    
    def getMeanMessages(self):
        return self.meanMessages
    
    def getBotMessages(self):
        return self.botMessages
    
    def getSubsistingMessages(self):
        return self.subsistingMessages

    def getProvokedMessages(self):
        return self.provokedMessages

    # Private lobby data
    def getLobbyCustomWords(self):
        return self.lobbyCustomWords

    def getLobbyRounds(self):
        return self.lobbyCustomRounds
    
    def getLobbyDrawTime(self):
        return self.lobbyDrawTime

    def getLobbyCustomOnly(self):
        return self.lobbyCustomOnly


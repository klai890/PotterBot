from selenium import webdriver # webdriver to open chrome and interact w/ the browser
from LocalStorage import LocalStorage # file LocalStorage.py in same directory
from Data import Data # file Data.py in same directory as this one
import time # intervals
import random # randomness

class SkribblBot:
    # Constructor: 
    def __init__(self, interval, private):
        self.SITE = "https://skribbl.io/" # FV: self.website (skribbl link); public server player
        self.PRIVATE = private # for private room creation (true or false)

        self.INTERVAL = interval
        self.name = "POTTER BOT" # FV: Name
        self.avatarCoords = "[2,8,8]" # FV: avatar (yellow XD face)

        # Retrieve responses from data class; arrays, and we select a random element from each array,
        # when the time is appropropriate

        self.data = Data() # Data instance
        self.spamMessages = self.data.getSpamMessages() # messages to spam (advertisements)
        self.niceMessages = self.data.getNiceMessages() # nice messages
        self.meanMessages = self.data.getMeanMessages() # mean messages
        self.botMessages = self.data.getBotMessages() # come out as a bot
        self.subsistingMessages = self.data.getSubsistingMessages() # the occasional lol and whatnot

        self.provokedMessages = self.data.getProvokedMessages() # check for anger directed towards POTTERBOT
        self.chatHistory = [] # used for detecting provoking messages
        self.numberOfProvokations = 0 # used to track new provokations
        self.provokationType = ""

        # Private room variables: all private room variables start with lobby
        self.lobbyCustomWords = self.data.getLobbyCustomWords() # custom words
        self.lobbyRounds = self.data.getLobbyRounds() # number of rounds for private room
        self.lobbyDrawTime = self.data.getLobbyDrawTime() # lobby draw time
        self.lobbyCustomOnly = self.data.getLobbyCustomOnly()

        self.driver = webdriver.Chrome()
        self.localStorage = ""

    # calls all the other methods
    def run(self):
        self.start()

        # If in private room creation mode
        if (self.PRIVATE == True):
            self.privateSetup()

        self.gameLoop()

    # retrieves the website: if not already retrieved, navigates; if already retrieved, reloads
    def load(self):
        self.driver.get(self.SITE)
        self.localStorage = LocalStorage(self.driver)

    # navigates to skribbl, sets the name and avatar color, and starts game
    def start(self):
        self.load() # navigate to the site
        
        # set local storage: name & avatar
        self.localStorage.set("name", self.name)
        self.localStorage.set("avatar", self.avatarCoords)

        # reload, because once we do, name and avatar will be set (from local storage)
        self.load()

        # presses the play button, if we're in public server mode
        if (self.PRIVATE == False):
            playBtn = self.driver.find_element_by_css_selector(".btn-success.btn-lg.btn-block")
            playBtn.click()

        if (self.PRIVATE == True):
            roomCreateBtn = self.driver.find_element_by_id("buttonLoginCreatePrivate")
            roomCreateBtn.click()
        
    # sets up a private room
    def privateSetup(self):
        
        # Wait for page to load
        time.sleep(10)

        # Change number of rounds to the one in FV self.lobbyRounds
        roundsSelectOptions = self.driver.find_elements_by_css_selector("#lobbySetRounds option")
        for opt in roundsSelectOptions:
            optValue = int(opt.get_attribute("innerText"))
            if (optValue == self.lobbyRounds):
                opt.click()

        # Change the amount of drawing time to the one in FV self.lobbyDrawTime
        timeSelectOptions = self.driver.find_elements_by_id("#lobbySetDrawTime option")
        for opt in timeSelectOptions:
            optValue = int(opt.get_attribute("innerText"))
            if(optValue == self.lobbyDrawTime):
                opt.click()

        # Convert array into string, place into customWordsBox
        customWordsBox = self.driver.find_element_by_id("lobbySetCustomWords")
        customWords = ""
        for word in self.lobbyCustomWords:
            customWords += f"{word},"
        customWordsBox.send_keys(customWords)

        # Use custom words exclusively, if field variable dictates
        exclusivelyBox = self.driver.find_element_by_id("lobbyCustomWordsExclusive")
        if (self.lobbyCustomOnly == True):
            exclusivelyBox.click() 

        # open up a terminal prompt, asking the runner of the program to verify when to start (when we actually have players)
        # pause program until user dictates
        # Stack Overflow, regarding this topic: https://stackoverflow.com/questions/11552320/correct-way-to-pause-a-python-program#11552350

        wait = input("Press the <ENTER> key to continue...")
        playBtn = self.driver.find_element_by_id("buttonLobbyPlay")
        playBtn.click()

    # The main game loop, calls other methods
    def gameLoop(self):
        while True:
            self.saySpam() # places an ad in the chat every so often
            time.sleep(self.INTERVAL)
            
            provoked = self.checkProvoked()
            # myTurn = checkTurn() # only if I want to work this AFK

            self.sayNice() # say something nice
            time.sleep(self.INTERVAL)

            if (provoked):
                self.sayBotReveal()
                time.sleep(self.INTERVAL)

            # if (myTurn):
            #     self.sayBotReveal()
            #     time.sleep(self.iNTERVAL)

            self.saySubsisting()
            time.sleep(self.INTERVAL)
    
    # Generates a random spam message (then calls function say to say it)
    def saySpam(self):
        randomInt = random.randint(0, len(self.spamMessages) - 1)
        self.say(self.spamMessages[randomInt])
    
    # Generates a random nice message (then calls function say to say it)
    def sayNice(self):
        randomInt = random.randint(0, len(self.niceMessages) - 1)
        self.say(self.niceMessages[randomInt])

    # Generates a random mean message (then calls function say to say it) 
    def sayMean(self):
        randomInt = random.randint(0, len(self.meanMessages) - 1)
        self.say(self.meanMessages[randomInt])

    # Generates a bot message, depending on the provokation type
    def sayBotReveal(self):
        indexResponse = 0 if self.provokationType == "fuck" else 1 # indices of response
        self.say(self.botMessages[indexResponse])

    # Generates a random subsisting message (then calls function say to say it)
    def saySubsisting(self):
        randomInt = random.randint(0, len(self.subsistingMessages) - 1)
        self.say(self.subsistingMessages[randomInt])

    # Says a message
    def say(self, message):
        # Gets the input chat text field, enters the message, then submits the form
        self.driver.implicitly_wait(5)
        inputChat = self.driver.find_element_by_id("inputChat")

        # Selenium's send keys in order to enter text into the field
        # Documentation: https://selenium-python.readthedocs.io/api.html?highlight=send%20keys#selenium.webdriver.common.alert.Alert.send_keys
        inputChat.send_keys(message)

        # Send the message
        # Reference (some random guy's code): https://github.com/4n4nk3/skribbl-io-guesser/blob/master/guesser.py
        inputChat.submit()

    # Checks if a user has said something provoking
    def checkProvoked(self):
        # Grab the last ten messages
        # Return them in an array: ["EndBruh: cheats", "Pine guessed the word!"]
        # messages = document.querySelectorAll("#boxMessages p") -> JS Code
        # can i just grab the last ten?
        # i just need to grab the messages which happened in the ten seconds I was gone
        # approximately three messages?
        # okay, how about we grab each time, then say the last index we left off at?
        # and also count how many provocations total; and count the number in the new one, compare, and
        # if there are more in the new one, yes, provoked; else, nope
        # also, filter out the irrelevants
        #   filter out all of my own messages (includes f'{name}:')
        #   filter out messages which include "guessed the word!"
        #   filter out messages which include "The word was"
        #   filter out messages which include "voting to kick"
        #   filter out messages which include "is drawing now"
        #   filter out messages which include " left"
        #   filter out messages which include " joined"
        #   filter out messages which include " is close!
        # python filter syntax: filter(FUNCTION, ITERABLE)

        messagesRaw = self.driver.find_elements_by_css_selector("#boxMessages p")
        messagesFiltered = list(filter(self.trimChat, messagesRaw)) # returns a filter object, so wrap in list()
        messages = []
        for msg in messagesFiltered:
            messages.append(msg.get_attribute("innerText"))

        
        # Find number of times provoked in the new chat; loop through 
        # each provokation and check if its in the chat history
        numProvokations = 0
        for provokation in self.provokedMessages:
            for msg in messages:
                if provokation in msg:
                    self.provokationType = "fuck" if "fuck" in msg or "f u" in msg else "shut up"
                    numProvokations += 1
        
        if numProvokations != self.numberOfProvokations: # new provokation
            self.numberOfProvokations = numProvokations
            return True
        
        else: # no new provokation
            self.numberOfProvokations = numProvokations
            return False

    # removes all skribbl system generated stuff, and stuff bot said
    def trimChat(self, msg):
        # https://docs.python.org/3/library/functions.html#filter
        # basically, return True if you want it in the array
        #   filter out all of my own messages (includes f'{name}:')
        #   filter out messages which include "guessed the word!"
        #   filter out messages which include "The word was"
        #   filter out messages which include "voting to kick"
        #   filter out messages which include "is drawing now"
        #   filter out messages which include " left"
        #   filter out messages which include " joined"
        #   filter out messages which include " is close!

        removalMsgs = [f'{self.name}:', "guessed the word!", "The word was", "voting to kick", "was kicked!", 
            "is drawing now", " left", " joined", " is close!"]

        for removalMsg in removalMsgs:
            msgText = msg.get_attribute("innerText")
            if removalMsg in msgText:
                return False # out of array

        return True # include in array

    # def checkTurn(self):

INTERVAL = 10 # seconds
sb = SkribblBot(interval=INTERVAL, private=False)
sb.run()
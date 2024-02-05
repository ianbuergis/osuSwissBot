from discord.ext import tasks, commands
from src.osuFeatures.osuHandler import OsuHandler
from ossapi import GameMode
from datetime import datetime


class Automation(commands.Cog):
    __bot: commands.Bot

    __osuHandler: OsuHandler

    __usersUpdated: bool = False

    __getScoresLoop: int = 1

    def __init__(self, bot: commands.Bot, osuHandler: OsuHandler, checkPlays: bool = True):
        self.__bot = bot
        self.__osuHandler = osuHandler

        if checkPlays:
            print('Recent scores are getting checked')
            self.updateUsers.start()
        else:
            print('Recent scores are not getting checked')

    @tasks.loop(hours=12)
    async def updateUsers(self):
        print(f"[{datetime.now()}]", 'updating users...')
        await self.__osuHandler.updateUsers(gamemode=GameMode.OSU)
        if not self.__usersUpdated:
            self.getScores.start()
            self.__usersUpdated = True
        print(f"[{datetime.now()}]", 'users are updated')

    #@tasks.loop(hours=12) #uncomment when the feature is actually implemented. which won't be for a while. for now we can keep the function around though
    async def updateTaikoUsers(self):
        print(f"[{datetime.now()}]", 'updating taiko users...')
        await self.__osuHandler.updateUsers(gamemode=GameMode.TAIKO)
        if not self.__usersUpdated:
            self.getScores.start()
            self.__usersUpdated = True
        print(f"[{datetime.now()}]", 'taiko users are updated')

    @tasks.loop(minutes=2)
    async def getScores(self, gamemode: GameMode = GameMode.OSU):
        rankRange = [self.__getScoresLoop, self.__getScoresLoop + 1]
        strRankRange = [str(self.__getScoresLoop), str(self.__getScoresLoop + 1)]
        print(f"[{datetime.now()}]", 'updating players: ' + ", ".join(strRankRange))
        self.__getScoresLoop = (self.__getScoresLoop + 2) % 50

        await self.__osuHandler.getRecentPlays(self.__bot, gamemode, rankRange)

        print(f"[{datetime.now()}]", 'finished updating plays')

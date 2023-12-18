from discord.ext import tasks, commands
from src.osuFeatures.osuHandler import OsuHandler
from ossapi import GameMode


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
        print('updating users...')
        await self.__osuHandler.updateUsers()
        if not self.__usersUpdated:
            self.getScores.start()
            self.__usersUpdated = True
        print('users are updated')

    @tasks.loop(minutes=2)
    async def getScores(self):
        rankRange = [self.__getScoresLoop, self.__getScoresLoop + 1]
        strRankRange = [str(self.__getScoresLoop), str(self.__getScoresLoop + 1)]
        print('updating players: ' + ", ".join(strRankRange))
        self.__getScoresLoop = self.__getScoresLoop + 2 % 20

        await self.__osuHandler.getRecentPlays(self.__bot, GameMode.OSU, rankRange)

        print('finished updating plays')

import os

import discord
from discord.ext import commands
from discord import Option
import shutil
import hashlib

from src.database.entities import Skin
from src.database.objectManager import ObjectManager
from src.helper import Validator
from src.helper.osuUserHelper import OsuUserHelper

from src.tempfiles import uploadFile


class SkinCommands(commands.Cog):
    bot: commands.Bot

    om: ObjectManager

    validator: Validator

    osuUserHelper: OsuUserHelper

    commandGroup = discord.SlashCommandGroup("skin", "commands used to manage skins")

    def __init__(self, bot, om, validator, osuUserHelper):
        self.bot = bot
        self.om = om
        self.validator = validator
        self.osuUserHelper = osuUserHelper

    @commandGroup.command(description="get the skin from a player")
    async def get(
        self,
        ctx: discord.ApplicationContext,
        *,
        user: Option(str, description='userID or username'),  # noqa
        forcebyuserid: Option(bool,
                              description='It will skip the search via username and will find by userid: default checks for both.', # noqa
                              default=False),  # noqa

    ):
        await ctx.response.defer()
        osuUser = await self.osuUserHelper.getOsuUser(user, createIfNone=False, forceById=forcebyuserid)

        if osuUser is None or osuUser.skin is None:
            await ctx.respond('user has no skin saved')
        else:
            skin: Skin = self.om.get(Skin, osuUser.skin)
            skinName = osuUser.username if osuUser.skinName is None else osuUser.skinName
            try:
                tempFilePath = shutil.copy(
                    os.getcwd() + '//data//skins//' + skin.hash + '.osk',
                    os.getcwd() + '//data//temp//' + skinName + '.osk'
                )
                file = open(tempFilePath, 'rb')
            except FileNotFoundError:
                await ctx.respond('user has no skin saved')
                return None
            link = uploadFile(file)
            await ctx.respond(link)
            file.close()
            os.remove(tempFilePath)

    @commandGroup.command(description="add a skin to a player")
    async def add(
            self,
            ctx: discord.ApplicationContext,
            *,
            user: Option(str, description='userID or username'),  # noqa
            skinfile: Option(discord.Attachment, description='add the replay file'),  # noqa
            forcebyuserid: Option(bool, description='It will skip the search via username and will find by userid: default checks for both.', default=False),  # noqa
    ):
        await ctx.response.defer()
        osuUser = await self.osuUserHelper.getOsuUser(user, createIfNone=True, forceById=forcebyuserid)
        skinfile: discord.Attachment
        data = await skinfile.read()
        hash = hashlib.sha256(data).hexdigest()

        if osuUser is None:
            await ctx.respond('username or userid ```' + user + '``` doesnt exist!')
            return None

        if osuUser.skin is not None:
            skin = self.om.get(Skin, osuUser.skin)
            if len(skin.osuUsers) <= 1:
                try:
                    os.remove(os.getcwd() + '//data//skins//' + skin.hash + '.osk')
                except FileNotFoundError:
                    pass
                self.om.delete(skin)

        cutSkinName = skinfile.filename.split('.')
        if 'osk' != cutSkinName[len(cutSkinName) - 1]:
            await ctx.respond('filetype should be osk')
            return None

        del cutSkinName[len(cutSkinName) - 1]
        skinName = ".".join(cutSkinName)

        skin = self.om.getOneBy(Skin, Skin.hash, hash)

        if skin is None:
            with open(os.getcwd() + '//data//skins//' + hash + '.osk', 'wb+') as f:
                f.write(data)
                f.close()

            skin = Skin(hash=hash)
            self.om.add(skin)
            self.om.flush()

        osuUser.skin = skin.id
        osuUser.skinName = skinName
        self.om.flush()
        await ctx.respond('added the skin "' + skinName + '" to ' + osuUser.username)

    @commandGroup.command(description="remove a skin from a player")
    async def remove(
            self,
            ctx: discord.ApplicationContext,
            *,
            user: Option(str, description='userID or username'),  # noqa
            forcebyuserid: Option(bool, description='It will skip the search via username and will find by userid: default checks for both.', default=False),  # noqa
    ):
        await ctx.response.defer()
        osuUser = await self.osuUserHelper.getOsuUser(user, createIfNone=True, forceById=forcebyuserid)

        if osuUser is None:
            await ctx.respond('username or userid ```' + user + '``` doesnt exist!')
            return None

        skin = self.om.get(Skin, osuUser.skin)
        if len(skin.osuUsers) <= 1:
            try:
                os.remove(os.getcwd() + '//data//skins//' + skin.hash + '.osk')
            except FileNotFoundError:
                pass
            self.om.delete(skin)

        osuUser.skin = None
        osuUser.skinName = None

        self.om.flush()
        await ctx.respond('Skin removed for ' + osuUser.username)

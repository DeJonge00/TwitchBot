from twitchio import Context
from twitchio.ext.commands import command
from twitchio.ext.commands.core import cog

from config.constants import TEXT
from core.bot import TwitchBot
from obs.change_theme import change_theme
from obs.constants import COLORS, SCENES
from obs.obs_websocket import request
from obs.scenes import set_scene


async def command_theme(bot: TwitchBot, args: [str]) -> dict:
    if len(args) < 1 or args[0].lower() not in COLORS:
        return {TEXT: "Color not found, please choose one of: {}".format(', '.join(COLORS))}
    color = args[0].lower()
    await request(bot.obs_websocket, change_theme, color)
    # bot.loop.run_until_complete(request(bot.obs_websocket, change_theme, color))
    return {TEXT: "Theme changed to {}!".format(color)}


async def command_scene(bot: TwitchBot, scene: [str]) -> dict:
    scene = ' '.join(scene)
    if len(scene) < 1 or scene not in SCENES:
        return {TEXT: "Scene not found, please choose one of: '{}'".format("', '".join(SCENES))}
    await request(bot.obs_websocket, set_scene, scene)
    # bot.loop.run_until_complete(request(bot.obs_websocket, change_theme, color))
    return {TEXT: "Scene changed to '{}'!".format(scene)}


@cog()
class OBSCommands:
    def __init__(self, bot: TwitchBot):
        self.bot = bot

    @command(name='theme')
    async def theme(self, ctx: Context, *args):
        if not self.bot.pre_command(ctx, command='theme', mod_check=True, timeout=1):
            return
        r = (await command_theme(self.bot, args=args)).get(TEXT)
        if r:
            await ctx.send(r.replace('*', ''))

    @command(name='scene')
    async def scene(self, ctx: Context, *args):
        if not self.bot.pre_command(ctx, command='scene', mod_check=True, timeout=1):
            return
        r = (await command_scene(self.bot, scene=args)).get(TEXT)
        if r:
            await ctx.send(r.replace('*', ''))

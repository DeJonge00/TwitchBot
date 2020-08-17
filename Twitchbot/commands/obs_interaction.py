from simpleobsws import obsws
from twitchio import Context
from twitchio.ext.commands import command
from twitchio.ext.commands.core import cog

from config.constants import TEXT
from core.bot import TwitchBot
from obs.obs_websocket import request
from obs.change_theme import change_theme
from obs.constants import COLORS


async def command_theme(bot: TwitchBot, args: [str]) -> dict:
    if len(args) < 1 or args[0].lower() not in COLORS:
        return {TEXT: "Color not found, please choose one of: {}".format(', '.join(COLORS))}
    color = args[0].lower()
    await request(bot.obs_websocket, change_theme, color)
    # bot.loop.run_until_complete(request(bot.obs_websocket, change_theme, color))
    return {TEXT: "Theme changed to {}!".format(color)}


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

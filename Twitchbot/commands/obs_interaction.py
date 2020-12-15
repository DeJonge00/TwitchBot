from asyncio import sleep

from simpleobsws import obsws
from twitchio import Context
from twitchio.ext.commands import command
from twitchio.ext.commands.core import cog

from config.constants import TEXT
from core.bot import TwitchBot
from obs.change_theme import change_theme
from obs.constants import COLORS, SCENES
from obs.obs_websocket import request, multi_request
from obs.scrolling_announcement import setup_scrolling_announcement, scrolling_announcement
from obs.types.filters.scroll import remove_scroll_filter
from obs.types.scenes import set_scene, get_curent_scene
from obs.types.source import get_source_settings, set_source_settings
from obs.types.sources.text import change_text


async def command_announce(ws: obsws, args: [str], author_name: str):
    if len(args) <= 0:
        return {TEXT: '???'}
    text = ' '.join(args)
    text = "{}: {}".format(author_name, text)
    source = 'AnnouncementLabel'
    await multi_request(ws, [setup_scrolling_announcement, scrolling_announcement], [[source], [source, text]])
    await sleep(30)
    await request(ws, remove_scroll_filter, source)


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


async def command_meme(bot: TwitchBot, text: str = 'POG'):
    if not text:
        return {TEXT: "Text not found, aborting"}
    scene = await request(ws=bot.obs_websocket, function=get_curent_scene)
    name = scene.get('name', 'Just Chatting')
    if scene.get('sources', None):
        type = scene.get('sources', [])[0].get('type')
    await multi_request(bot.obs_websocket,
                        [change_text, set_source_settings, set_scene],
                        [
                            ['BlackBorderMemeTopLabel', text],
                            ['SceneMirror', 'streamfx-source-mirror', {
                                'Source.Mirror.Source': name
                            }],
                            ['BlackBorderTextMeme']
                        ])
    await sleep(8)
    await request(bot.obs_websocket, set_scene, name)
    return {TEXT: "Meme activated with text '{}'!".format(text)}


@cog()
class OBSCommands:
    def __init__(self, bot: TwitchBot):
        self.bot = bot

    @command(name='announce')
    async def announce(self, ctx: Context, *args: [str]):
        if not self.bot.pre_command(ctx, command='announce', timeout=60):
            return
        await command_announce(ws=self.bot.obs_websocket, args=args, author_name=ctx.author.display_name)

    @command(name='theme')
    async def theme(self, ctx: Context, *args):
        if not self.bot.pre_command(ctx, command='theme', mod_check=False, timeout=180):
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

    @command(name='meme')
    async def scene(self, ctx: Context, *args):
        if not self.bot.pre_command(ctx, command='meme', mod_check=True, timeout=1):
            return
        r = (await command_meme(self.bot, text=' '.join(args))).get(TEXT)
        if r:
            await ctx.send(r.replace('*', ''))

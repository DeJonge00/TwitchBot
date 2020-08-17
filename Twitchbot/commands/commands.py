from twitchio import Context
from twitchio.ext.commands import command
from twitchio.ext.commands.core import cog

from commands.basic_commands import TEXT, command_cast, command_compliment, command_kiss, command_kill, command_nice, \
    command_quote, command_face, command_hug, command_uptime
from config.config import discord_invite_link
from core.bot import TwitchBot


@cog()
class Commands:
    def __init__(self, bot: TwitchBot):
        self.bot = bot

    @command(name='discord')
    async def discord(self, ctx: Context):
        if not self.bot.pre_command(ctx, command='discord'):
            return
        await ctx.send('Discord server: {}'.format(discord_invite_link))

    @command(name='cast')
    async def cast(self, ctx: Context, *args):
        if not self.bot.pre_command(ctx, command='cast'):
            return
        r = command_cast(args, ctx.author.display_name).get(TEXT)
        if r:
            await ctx.send(r.replace('*', ''))

    @command(name='compliment')
    async def compliment(self, ctx: Context):
        if not self.bot.pre_command(ctx, command='compliment'):
            return
        r = command_compliment(ctx.author.display_name).get(TEXT)
        if r:
            await ctx.send(r.replace('*', ''))

    @command(name='face')
    async def face(self, ctx: Context):
        if not self.bot.pre_command(ctx, command='face'):
            return
        r = command_face().get(TEXT)
        if r:
            await ctx.send(r)

    @command(name='hug')
    async def hug(self, ctx: Context, *args):
        if not self.bot.pre_command(ctx, command='hug'):
            return
        r = command_hug(ctx.author.display_name, ' '.join(args)).get(TEXT)
        if r:
            await ctx.send(r.replace('*', ''))

    @command(name='kiss')
    async def kiss(self, ctx: Context, *args):
        if not self.bot.pre_command(ctx, command='kiss'):
            return
        r = command_kiss(ctx.author.display_name, ' '.join(args)).get(TEXT)
        if r:
            await ctx.send(r.replace('*', ''))

    @command(name='kill')
    async def kill(self, ctx: Context, *args):
        if not self.bot.pre_command(ctx, command='kill'):
            return
        r = command_kill(ctx.author.display_name, ' '.join(args)).get(TEXT)
        if r:
            await ctx.send(r.replace('*', ''))

    @command(name='nice')
    async def nice(self, ctx: Context):
        if not self.bot.pre_command(ctx, command='nice'):
            return
        r = command_nice(ctx.author.display_name, ctx.author.id).get(TEXT)
        if r:
            await ctx.send(r)

    @command(name='quote')
    async def quote(self, ctx: Context):
        if not self.bot.pre_command(ctx, command='quote'):
            return
        r = command_quote().get(TEXT)
        if r:
            await ctx.send(r)

    @command(name='uptime')
    async def uptime(self, ctx: Context):
        if not self.bot.pre_command(ctx, command='uptime'):
            return
        r = command_uptime(self.bot.start_time).get(TEXT)
        if r:
            await ctx.send(r)

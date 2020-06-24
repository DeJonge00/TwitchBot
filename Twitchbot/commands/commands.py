from twitchio import Context
from twitchio.ext.commands import command
from twitchio.ext.commands.core import cog

from TwitchBot import TwitchBot
from commands.basic_commands import TEXT, command_cast, command_compliment, command_kiss, command_kill, command_nice, \
    command_quote
from config.config import discord_invite_link


@cog()
class Commands:
    def __init__(self, bot: TwitchBot):
        self.bot = bot

    @command(name='test')
    async def test(self, ctx: Context):
        if not self.bot.pre_command(ctx, command='test', owner_check=True):
            return
        await ctx.send('test passed!')

    @command(name='discord')
    async def discord(self, ctx: Context):
        if not self.bot.pre_command(ctx, command='discord'):
            return
        await ctx.send('Discord server: {}'.format(discord_invite_link))

    @command(name='cast')
    async def cast(self, ctx: Context, *args):
        if not self.bot.pre_command(ctx, command='cast', owner_check=True):
            return
        r = command_cast(args, ctx.author.display_name).get(TEXT)
        if r:
            await ctx.send(r.replace('*', ''))

    @command(name='compliment')
    async def compliment(self, ctx: Context):
        if not self.bot.pre_command(ctx, command='compliment', owner_check=True):
            return
        r = command_compliment(ctx.author.display_name).get(TEXT)
        if r:
            await ctx.send(r.replace('*', ''))

    @command(name='kiss')
    async def kiss(self, ctx: Context, *args):
        if not self.bot.pre_command(ctx, command='kiss', owner_check=True):
            return
        r = command_kiss(ctx.author.display_name, ' '.join(args)).get(TEXT)
        if r:
            await ctx.send(r.replace('*', ''))

    @command(name='kill')
    async def kill(self, ctx: Context, *args):
        if not self.bot.pre_command(ctx, command='kill', owner_check=True):
            return
        r = command_kill(ctx.author.display_name, ' '.join(args)).get(TEXT)
        if r:
            await ctx.send(r.replace('*', ''))

    @command(name='nice')
    async def nice(self, ctx: Context):
        if not self.bot.pre_command(ctx, command='nice', owner_check=True):
            return
        r = command_nice(ctx.author.display_name, ctx.author.id).get(TEXT)
        if r:
            await ctx.send(r)

    @command(name='quote')
    async def quote(self, ctx: Context):
        if not self.bot.pre_command(ctx, command='quote', owner_check=True):
            return
        r = command_quote().get(TEXT)
        if r:
            await ctx.send(r)


def commands_setup(bot):
    bot.add_cog(Commands(bot))

from twitchio import Context
from twitchio.ext.commands import command
from twitchio.ext.commands.core import cog
from twitchio.errors import HTTPException

from config import constants
from TwitchBot import TwitchBot


@cog()
class Admin:
    def __init__(self, bot: TwitchBot):
        self.bot = bot

    @command(name='test')
    async def test(self, ctx: Context):
        if not self.bot.pre_command(ctx, command='test', owner_check=True):
            return
        await ctx.send('test passed!')

    @command(name='id')
    async def id(self, ctx: Context, *args):
        if not self.bot.pre_command(ctx, command='id', owner_check=True):
            return
        try:
            print([(p.display_name, p.id) for p in await self.bot.get_users(*[x.lower() for x in args])])
        except HTTPException:
            print('Error retrieving users')


def commands_setup(bot):
    bot.add_cog(Admin(bot))

from twitchio import Context
from twitchio.ext.commands import Bot

from config.config import nickname, prefix, channels, owner_ids
from core.listeners import listener_setup
from secret.secrets import client_id, password, secret


class TwitchBot(Bot):
    def __init__(self):
        listener_setup(self)
        super(TwitchBot, self).__init__(
            irc_token=password,
            client_id=client_id,
            client_secret=secret,
            nick=nickname,
            prefix=prefix,
            initial_channels=channels
        )

    def pre_command(self, ctx: Context, command: str, owner_check=False):
        print("Command '{}' used by '{}'".format(command, ctx.author.display_name))
        if owner_check and ctx.author.id not in owner_ids:
            return False
        return True

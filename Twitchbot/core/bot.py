from datetime import datetime, timedelta

from twitchio import Context
from twitchio.ext.commands import Bot

from config.config import nickname, prefix, active_channels, owner_ids, blacklist
from secret.secrets import client_id, password, secret


class TwitchBot(Bot):
    def __init__(self):
        self.start_time = datetime.utcnow()
        self.command_timeouts = {}

        super(TwitchBot, self).__init__(
            irc_token=password,
            client_id=client_id,
            client_secret=secret,
            nick=nickname,
            prefix=prefix,
            initial_channels=active_channels
        )

    def in_timeout(self, channel_id, command) -> bool:
        channel = self.command_timeouts.get(channel_id)
        if not channel:
            channel = {}
            self.command_timeouts[channel_id] = channel
        time = datetime.utcnow()
        min_time = (time - timedelta(minutes=1)).timestamp()
        if min_time < channel.get(command, 0):
            return True
        channel[command] = time.timestamp()
        return False

    def pre_command(self, ctx: Context, command: str, owner_check=False, mod=False) -> bool:
        print("Command '{}' used by '{}': {}".format(command, ctx.author.display_name, ctx.content))
        if self.in_timeout(ctx.channel.name, command):
            return False
        if ctx.author.id not in owner_ids:
            if owner_check:
                return False
            if mod and not ctx.author.is_mod:
                return False
            if command in blacklist.get(ctx.channel.name):
                return False
        return True

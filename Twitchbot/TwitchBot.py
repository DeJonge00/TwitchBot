from config.config import active_channels
from core.bot import TwitchBot
from widget.update import update_html

START_COG_MESSAGE = 'Cog started: {}'
cogs = [
    'core.listeners',
    'commands.commands',
    'commands.admin',
    'commands.update_stream_score'
]


def bot_loop(bot: TwitchBot):
    update_html(bot=bot, channel=active_channels[0])


def create_bot():
    bot = TwitchBot()

    for cog in cogs:
        bot.load_module(cog)
        print(START_COG_MESSAGE.format(cog))

    bot.loop.create_task(bot_loop(bot=bot))
    return bot


if __name__ == "__main__":
    create_bot().run()

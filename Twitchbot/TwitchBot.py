from core.bot import TwitchBot

START_COG_MESSAGE = 'Cog started: {}'
cogs = [
    'commands.commands',
    'commands.admin'
]


def create_bot():
    bot = TwitchBot()

    for cog in cogs:
        bot.load_module(cog)
        print(START_COG_MESSAGE.format(cog))

    return bot


if __name__ == "__main__":
    create_bot().run()

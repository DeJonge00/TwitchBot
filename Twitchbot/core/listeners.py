from twitchio import Message
from twitchio.errors import HTTPException

from config.config import nickname, owner, prefix
from config.constants import TEXT
from core.reactions import react_with_text, talk


def listener_setup(bot):
    @bot.event
    async def event_ready():
        'Called once when the bot goes online.'
        print("{} is online!".format(nickname))
        ws = bot._ws  # this is only needed to send messages within event_ready
        await ws.send_privmsg(owner, f"/me has landed!")

    @bot.event
    async def event_message(message: Message):
        'Runs every time a message is sent in chat.'

        # make sure the bot ignores itself and the streamer
        if message.author.name.lower() == nickname.lower():
            return

        await bot.handle_commands(message)

        if message.content.startswith('>'):
            return

        try:
            channel_id = (await bot.get_users(message.channel.name))[0]
        except HTTPException:
            channel_id = 0
        r = react_with_text(message.content, channel_id, message.author.id) or \
            talk(message.content, channel_id, prefix, message.author.id)
        t = r.get(TEXT)
        if t:
            await message.channel.send(t)

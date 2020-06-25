import asyncio
from datetime import datetime

from twitchio import Message, Channel, User
from twitchio.errors import HTTPException
from twitchio.ext.commands.core import cog

from config.config import nickname, owner, prefix, active_channels
from config.constants import TEXT, BIRIid
from core.reactions import react_with_text, talk


async def water_reminder(channel):
    await channel.send('Stay hydrated! Drink some water.. please..')



@cog()
class Listeners:
    def __init__(self, bot):
        self.bot = bot
        self.viewers = [BIRIid]

    async def loop(self):
        print('Time-loop started')
        while True:
            time = datetime.utcnow()
            if (time.minute - self.bot.start_time.minute) % 15 == 0:
                for channel in [self.bot.get_channel(c) for c in active_channels]:
                    await water_reminder(channel=channel)
            end_time = datetime.utcnow()
            await asyncio.sleep(60 - end_time.second)

    async def event_ready(self):
        """Called once when the bot goes online."""
        print("\nStarted bot")
        print('Name:', nickname)
        print('ID:', BIRIid)
        print("Active in channels:", ', '.join(active_channels))
        print("Started at: " + datetime.utcnow().strftime("%H:%M:%S") + "\n")

        ws = self.bot._ws  # this is only needed to send messages within event_ready
        await ws.send_privmsg(owner, f"/me has landed!")
        self.bot.loop.create_task(self.loop())

    async def event_message(self, message: Message):
        """Runs every time a message is sent in chat."""

        # make sure the bot ignores itself and the streamer
        if message.author.name.lower() == nickname.lower():
            return

        await self.bot.handle_commands(message)

        if message.content.startswith('>'):
            return

        try:
            channel_id = (await self.bot.get_users(message.channel.name))[0]
        except HTTPException:
            channel_id = 0
        r = react_with_text(message.content, channel_id, message.author.id) or \
            talk(message.content, channel_id, prefix, message.author.id, message.author.display_name)
        t = r.get(TEXT)
        if t:
            await message.channel.send(t)

    async def event_join(self, user: User):
        if not user.id:
            return
        if user.id not in self.viewers:
            await user.channel.send('Welcome, {}, to the stream!'.format(user.display_name))
            self.viewers.append(user.id)

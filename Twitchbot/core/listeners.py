import asyncio
from datetime import datetime
from random import choice

from playsound import playsound
from twitchio import Message, User
from twitchio.ext.commands.core import cog

from config.command_text import water_notification, announcements
from config.config import nickname, owner, prefix, active_channels, sound_files_path
from config.constants import TEXT, BIRIid, AUDIO, NYAid
from core.reactions import react_with_text, talk
from core.sound_reactions import react_with_audio


async def water_reminder(channel):
    await channel.send(water_notification)


async def random_announcement(channel):
    await channel.send(choice(announcements))


@cog()
class Listeners:
    def __init__(self, bot):
        self.bot = bot
        self.viewers = [BIRIid]

    async def loop(self):
        print('Time-loop started')
        while True:
            time = datetime.utcnow()
            if (time.minute - self.bot.start_time.minute) % 10 == 0:
                for channel in [self.bot.get_channel(c) for c in active_channels]:
                    await random_announcement(channel=channel)
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

        if not message.content or message.content[0] in ['>', '!']:
            return

        # TODO See if this can be fixed?
        # try:
        #     channel_id = (await self.bot.get_users(message.channel.name))[0]
        # except HTTPException:
        channel_id = NYAid
        r = react_with_text(message.content, channel_id, message.author.id) or \
            talk(message.content, channel_id, prefix, message.author.id, message.author.display_name) or \
            react_with_audio(self.bot, message.content, channel_id, message.author.id)
        t = r.get(TEXT)
        a = r.get(AUDIO)
        if t:
            await message.channel.send(t)
        if a:
            await self.bot.timer.get('semaphore').acquire()
            playsound(sound_files_path + a)
            self.bot.timer['time'] = datetime.utcnow()
            self.bot.timer.get('semaphore').release()

    async def event_join(self, user: User):
        if not user.id:
            return
        if user.id not in self.viewers:
            await user.channel.send('Welcome, {}, to the stream!'.format(user.display_name))
            self.viewers.append(user.id)

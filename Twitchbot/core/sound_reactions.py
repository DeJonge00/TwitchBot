from datetime import datetime

from config.constants import AUDIO, audio_whitelist
from core.bot import TwitchBot


def react_with_audio(bot: TwitchBot, message: str, streamer_channel: int, author_id: int):
    if bot.playing_audio.get('semaphore').locked() or \
            (datetime.utcnow() - bot.playing_audio.get('time')).seconds < 10:
        return {}

    if streamer_channel not in audio_whitelist:
        return {}

    message = message.lower().strip('!?')

    if message in ['fbi', 'fbi open up']:
        return {AUDIO: 'fbi-open-up.mp3'}
    if message in ['honk', 'goose']:
        return {AUDIO: 'honk.mp3'}
    if message in ['illuminati', 'illuminati coonfirmed']:
        return {AUDIO: 'illuminati.mp3'}
    if message in ['yeah', 'yeeaah', 'yeeaahh', 'yeaah', 'yeaahh']:
        return {AUDIO: 'yeaaahh.mp3'}

    return {}
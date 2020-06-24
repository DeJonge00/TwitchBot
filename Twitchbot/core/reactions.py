import random
import string

from config import command_text
from config import constants
from config.config import bot_names
from config.constants import TEXT


def react_with_text(message: str, streamer_channel: int, author_id: int):
    """
    React to a message with a text response.
    :param message: The contents of the message
    :param streamer_channel: The name of the channel the message was send in.
    :param author_id: The id of the author of the message.
    :return: {TEXT: The text to respond with.} or {} if there is nothing to respond to.
    """
    if (streamer_channel in constants.s_to_ringels_whitelist) and \
            author_id == constants.DOGEid and "s" in message:
        return {TEXT: "*" + message.replace("s", "ß")}

    if (streamer_channel not in constants.ayy_lmao_blacklist or author_id == constants.NYAid) and \
            (message.lower() == "ayy"):
        return {TEXT: "Lmao"}

    if author_id in [constants.NYAid] and message.lower() == "qyy":
        return {TEXT: 'Kmao'}

    if message.lower() == "lmao" and author_id == constants.NYAid:
        return {TEXT: 'Ayy'}

    if (streamer_channel not in constants.lenny_blacklist) and "lenny" in message.split(" "):
        return {TEXT: "( ͡° ͜ʖ ͡°)"}

    if (streamer_channel not in constants.table_unflip_blacklist) and message == "(╯°□°）╯︵ ┻━┻":
        return {TEXT: "┬─┬﻿ ノ( ゜-゜ノ)"}
    return {}


def talk(message: str, guild_id: int, prefix: str, author_id: int):
    """
    React to a message that talks to me using a name from the secrets file.
    :param message: The message to respond to.
    :param guild_id: The id of the channel the message was send in.
    :param author_id: The id of the author of the message.
    :param prefix: The prefix of the bot.
    :return: {TEXT: The test to respond with.} or {} if there is nothing to respond to.
    """
    if not (len(message) < 2 or (message[:2] == '<@') or (
            message[0].isalpha() and message[1].isalpha())) or guild_id in constants.bot_talk_blacklist:
        return {}

    if (len(set(message.lower().translate(str.maketrans('', '', string.punctuation)).split(" ")).intersection(
            set(bot_names))) > 0):
        if 'prefix' in message.lower():
            return {TEXT: 'My prefix is \'{}\', darling'.format(prefix)}

        if (author_id in [constants.NYAid]) and any(word in message.lower() for word in ['heart', 'pls', 'love']):
            return {TEXT: ":heart:"}

        if message[len(message) - 1] == "?":
            return {TEXT: random.choice(command_text.qa)}
        return {TEXT: random.choice(command_text.response)}
    return {}

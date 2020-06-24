from config import constants
from config.constants import TEXT


def react_with_text(message: str, streamer_channel: str, author_id: int):
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

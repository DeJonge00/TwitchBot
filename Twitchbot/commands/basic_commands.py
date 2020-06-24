import hashlib
import random

import requests

from config import command_text
from config.constants import TEXT


def command_cast(args, author_name):
    """
    Casts a random spell to a target
    :param args: The text of the message, excluding the command and split by spaces
    :param author_name: The username of the sender of the command
    :return: The response string
    """
    # Exceptions
    if len(args) <= 0:
        return {TEXT: "{}, you cannot cast without a target...".format(author_name)}

    # Casting spell
    target = ' '.join(args)
    chosen_spell = random.choice(command_text.spell)
    chosen_result = random.choice(command_text.spellresult)

    return {TEXT: "**{}** casted **{}** on {}.\n{}".format(author_name, chosen_spell, target, chosen_result)}


def command_compliment(author: str):
    return random.choice(command_text.compliments).format(u=[author])


englishyfy_numbers = {
    '0': 'zero',
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine'
}


def command_emojify(args: [str]):
    """
    The command that emojifies a string
    :param args: The string to be emojified
    :return: The emojfied string
    """
    text = " ".join(args).lower()
    if not text:
        return {TEXT: 'Please give me a string to emojify...'}

    def convert_char(c: str):
        if c.isalpha():
            return ' ' if c == ' ' else ":regional_indicator_" + c + ":"
        if c in englishyfy_numbers.keys():
            return ':{}:'.format(englishyfy_numbers.get(c))
        return ":question:" if c == '?' else ":exclamation:" if c == "!" else c

    return {TEXT: ' '.join([convert_char(c) for c in text])}


def command_face():
    return {TEXT: random.choice(command_text.faces)}


def command_hug(author: str, target: str):
    return {TEXT: random.choice(command_text.hug).format(u=[author, target])}


def command_kill(author: str, target: str):
    if author is target:
        return {TEXT: "Suicide is not the answer, 42 is"}
    return {TEXT: random.choice(command_text.kill).format(u=[target])}


def command_kiss(author: str, target: str):
    if author is target:
        return {TEXT: "{0} Trying to kiss yourself? Let me do that for you...\n*kisses {0}*".format(author)}
    return {TEXT: random.choice(command_text.kisses).format(u=[author, target])}


def command_nice(author: str, author_id: int):
    n = (int(hashlib.sha1(str(author_id).encode()).hexdigest(), 16) + 80) % 100
    return {TEXT: '{}, it has been determined you are {}% nice'.format(author, n)}


def command_quote():
    params = {'method': 'getQuote', 'format': 'json', 'lang': 'en'}
    r = requests.get('http://api.forismatic.com/api/1.0/', params=params)
    if not isinstance(r, dict):
        if r.status_code != 200:
            print('Error code', r.status_code)
            return {}
        r = r.json()
    m = '`{}`'.format(r.get('quoteText'))
    if r.get('quoteAuthor'):
        m += '({})'.format(r.get('quoteAuthor'))
    return {TEXT: m}

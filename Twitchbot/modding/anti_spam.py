from string import ascii_letters


def message_is_spam(message: str) -> bool:
    return emoji_wall(message=message)


def copy_pasta(message: str) -> bool:
    pass


def emoji_wall(message: str) -> bool:
    return len(list(filter(lambda l: l in ascii_letters, message))) > 25

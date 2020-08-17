from twitchio import User, Channel

from commands.update_stream_score import Score
from config.config import widget_file, widget_path, widget_template
from core.bot import TwitchBot


def update_html(bot: TwitchBot, channel: str):
    format_vars = {}
    if bot.scores:
        score = bot.scores.get(channel)
        if score:
            for k, v in [
                ("team_1", score.team1.name),
                ("team_2", score.team2.name),
                ("score_1", score.team1.score),
                ("score_2", score.team2.score)
            ]:
                format_vars[k] = v

    # format_vars["followers_nr"] = len(await bot.get_followers(channel))
    # format_vars["subscribers_nr"] = len(await bot.get_chatters(channel))

    # Apply vars to html
    # with open(widget_path + widget_template, 'r') as f:
    #     text = f.read()
    # text = text.format(*format_vars)
    # with open(widget_path + widget_file, 'w') as f:
    #     f.write(text)

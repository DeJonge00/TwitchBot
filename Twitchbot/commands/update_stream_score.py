import re

from twitchio import Context
from twitchio.ext.commands import cog, command

from config.config import prefix, widget_path, widget_template, widget_file
from config.constants import TEXT
from core.bot import TwitchBot


class Team:
    def __init__(self, name, score=0):
        self.name = name
        self.score = score

    def __str__(self):
        return '{}: {}'.format(self.name, self.score)


class Score:
    def __init__(self, team1='team1', team2='team2'):
        self.team1 = Team(name=team1)
        self.team2 = Team(name=team2)

    def __str__(self):
        return '{} -- {}'.format(self.team1, self.team2)


@cog()
class WidgetCommands:
    def __init__(self, bot: TwitchBot):
        self.bot = bot
        self.bot.scores = {}

    def command_reset_score(self, channel_id: int):
        if self.bot.scores.get(channel_id):
            del self.bot.scores[channel_id]
            return {TEXT: 'Scores have been reset'}
        return {TEXT: 'No scores present to reset'}

    def command_score_name(self, channel_id: int, message_content):
        m = re.match("\'(.+)\'.*\'(.+)\'", message_content)
        if not m:
            return {TEXT: 'Arguments not accepted! Provide 2 names in string marks'}
        team1, team2 = m.groups()
        self.bot.scores[channel_id] = Score(team1=team1, team2=team2)
        return {TEXT: "Initialized scores for teams '{}' and '{}'".format(team1, team2)}

    def command_score_set(self, channel_id: int, args: [str]):
        if len(args) < 2:
            return {TEXT: "Not enough arguments given, 2 new scores needed"}
        if not re.match("[0-9]+", args[0]) or not re.match("[0-9]+", args[1]):
            return {TEXT: "Could not figure out which numbers you meant"}
        s = self.bot.scores.get(channel_id)
        if not s:
            return {TEXT: "No teams found, please use `{}score \"name1\" \"name2\"`".format(prefix)}
        s.team1.score = int(args[0])
        s.team2.score = int(args[1])
        return {TEXT: "The score is now: {}".format(s)}

    @command(name='score')
    async def score(self, ctx: Context, *args):
        # Display curent score
        if len(args) <= 0:
            if not self.bot.pre_command(ctx, command='score'):
                return
            s = self.bot.scores.get(ctx.channel.name, "There is no active score at the moment")
            await ctx.send(s)
            return
        if not self.bot.pre_command(ctx, command='score', mod=True):
            return

        if len(args) <= 0:
            return

        if args[0] in ['reset', 'zero']:
            r = self.command_reset_score(self.bot.start_time).get(TEXT)
        elif args[0] in ['set', 'make']:
            r = self.command_score_set(ctx.channel.name, args[1:]).get(TEXT)
        else:
            r = self.command_score_name(ctx.channel.name, ' '.join(args)).get(TEXT)

        if r:
            await ctx.send(r)


if __name__ == '__main__':
    team_1_name = 'TEAM!'
    team_2_name = 'TEAM@'
    score_1 = 1
    score_2 = 3
    s = Score(team_1_name, team_2_name)
    s.team1.score = score_1
    s.team2.score = score_2

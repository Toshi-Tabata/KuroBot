import discord
from discord.ext import commands
import database_helper as db
import random

from datetime import datetime
import pytz

tz = pytz.timezone('CST6CDT')

# a datetime with timezone
dt_with_tz = tz.localize(datetime(2012, 8, 28, 19, 33, 50), is_dst=None)

# get timestamp
ts = (dt_with_tz - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
# -> 1346200430.0


class Times(commands.Cog):
    """Time conversion stuffs"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def convert(self, ctx, *msgs):
        """convert from time zone to local time zone"""
        print(msgs)
        timezone = msgs
        if len(timezone) != 3:
            print("worng number of args")
            await ctx.send("Usage: 'dd/mm/yyyy hh:mm timezone'")
            return
        timezone = timezone[2]

        if "GMT+" in timezone:
            timezone = timezone.replace("+", "-")
            timezone = "etc/" + timezone
        elif "GMT-" in timezone:
            timezone = timezone.replace("-", "+")
            timezone = "etc/" + timezone
        elif "PST" in timezone:
            timezone = 'America/Los_Angeles'

        elif "PDT" in timezone:
            timezone = "US/Pacific"


        try:
            gmt = pytz.timezone(timezone)

        except pytz.exceptions.UnknownTimeZoneError:
            await ctx.send("uhhh idk that timezone check here https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568")
            return

        
        time = f"{msgs[0]} {msgs[1]}"
        fmt = "%d/%m/%Y %H:%M"
        print(time)

        try:
            date = datetime.strptime(time, fmt)
        except ValueError:
            await ctx.send("Usage: 'dd/mm/yyyy hh:mm timezone'")
            return
        
        dategmt = gmt.localize(date)

        ts = (dategmt - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()

        print(f"<t:{int(ts)}:F>")

        quotes = [
            f"uhh here <t:{int(ts)}:F>",
            f"uhh, that's <t:{int(ts)}:F> in your time.. i think",
            f"that is <t:{int(ts)}:F> fool",
            f"ok <t:{int(ts)}:F>",
            f"stop asking me <t:{int(ts)}:F>"


        ]
        await ctx.send(random.choice(quotes))
    

    @commands.command()
    async def timezones(self, ctx, *msgs):
        """convert from time zone to local time zone"""

        await ctx.send("https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568")
        


def setup(client):
    client.add_cog(Times(client))
import discord
from discord.ext import commands
import database_helper as db

class Innocent(commands.Cog):
    """Prints a graphic detailing that pickle was innocent"""

    def __init__(self, client):
        self.client = client


    # Actual command definition
    @commands.command()
    async def innocent(self, ctx, *msgs):
        """will send a graphic"""
        print(msgs)

        foo = f"""
. 　　　。　　　　•　 　ﾟ　　。 　　.

　　　.　　　 　　.　　　　　。　　 。　. 　

.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•

　　ﾟ         {msgs[0]} was not an Impostor.　 。　.

　　'　　　 1 Impostor remains. 　 　　。

　　ﾟ　　　.　　　. ,　　　　.　 .
"""
        await ctx.send(foo)

    # Actual command definition
    @commands.command()
    async def imposter(self, ctx, *msgs):
        """will send a graphic"""
        print(msgs)

        foo = f"""
. 　　　。　　　　•　 　ﾟ　　。 　　.

　　　.　　　 　　.　　　　　。　　 。　. 　

.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•

　　ﾟ         {msgs[0]} was an Impostor.　 。　.

　　'　　　 0 Impostor remains. 　 　　。

　　ﾟ　　　.　　　. ,　　　　.　 .
"""
        await ctx.send(foo)


def setup(client):
    client.add_cog(Innocent(client))
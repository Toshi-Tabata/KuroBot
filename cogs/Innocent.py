import discord
from discord.ext import commands
import database_helper as db

class Innocent(commands.Cog):
    """Prints a graphic detailing that the person was innocent"""

    def __init__(self, client):
        self.client = client


    # Actual command definition
    @commands.command()
    async def innocent(self, ctx, *msgs):
        """will send a graphic with the given person as innocent"""
        try:
            person = msgs[0]
        except IndexError:
            person = "Nobody"
        graphic = f"""
. 　　　。　　　　•　 　ﾟ　　。 　　.

　　　.　　　 　　.　　　　　。　　 。　. 　

.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•

　　ﾟ         {person} was not an Impostor.　 。　.

　　'　　　 1 Impostor remains. 　 　　。

　　ﾟ　　　.　　　. ,　　　　.　 .
"""
        await ctx.send(graphic)

    # Actual command definition
    @commands.command()
    async def imposter(self, ctx, *msgs):
        """will send a graphic with the given person as imposter"""
        try:
            person = msgs[0]
        except IndexError:
            person = "Nobody"
        graphic = f"""
. 　　　。　　　　•　 　ﾟ　　。 　　.

　　　.　　　 　　.　　　　　。　　 。　. 　

.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•

　　ﾟ         {person} was an Impostor.　 。　.

　　'　　　 0 Impostor remains. 　 　　。

　　ﾟ　　　.　　　. ,　　　　.　 .
"""
        await ctx.send(graphic)


def setup(client):
    client.add_cog(Innocent(client))
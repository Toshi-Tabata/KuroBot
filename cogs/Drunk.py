import discord
from discord.ext import commands
import database_helper as db

class Drunk(commands.Cog):
    """Quote from kuro when he was drunk"""

    def __init__(self, client):
        self.client = client


    # Actual command definition
    @commands.command()
    async def drunk(self, ctx, *msgs):
        """This is what kuro said when he was clearly drunk"""

        await ctx.send("inm not drunk")
        await ctx.send("opr tispyu")

def setup(client):
    client.add_cog(Drunk(client))
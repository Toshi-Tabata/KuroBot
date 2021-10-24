import discord
from discord.ext import commands


class BDSM(commands.Cog):
    """What kuro got for his bdsm test"""

    def __init__(self, client):
        self.client = client


    # Actual command definition
    @commands.command()
    async def bdsm(self, ctx, *msgs):
        """This is what kuro got for his BDSM test"""

        await ctx.send("https://cdn.discordapp.com/attachments/704320774734872580/710851511697145866/unknown.png")

        


def setup(client):
    client.add_cog(BDSM(client))
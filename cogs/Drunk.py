import discord
from discord.ext import commands
import database_helper as db
import random

COUNT = 0

class Drunk(commands.Cog):
    """Quote from kuro when he was drunk"""

    def __init__(self, client):
        self.client = client


    # Actual command definition
    @commands.command()
    async def drunk(self, ctx, *msgs):
        """This is what kuro said when he was clearly drunk"""
        quotes = ["noootttttttttttt drunkl", "inm not drunk\nopr tispyu"]
        choice = random.choice(quotes)
        choice = choice.split("\\n")
        for text in choice:
            await ctx.send(text)
        # await ctx.send("inm not drunk")
        # await ctx.send("opr tispyu")
    
    @commands.command()
    async def swear(self, ctx, *msgs):
        """increases the kuro swear counter"""
        global COUNT
        await ctx.send(f"Kuro as sworn {COUNT} times tonight")

    @commands.command()
    async def addSwear(self, ctx, *msgs):
        """increases the kuro swear counter"""
        global COUNT
        COUNT += 1
        await ctx.send(f"Added. Kuro has sworn {COUNT} times tonight")

        


def setup(client):
    client.add_cog(Drunk(client))
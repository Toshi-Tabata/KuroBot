import discord
from discord.ext import commands
import database_helper as db

class Debugging(commands.Cog):
    """Debugging and Testing Functions"""

    def __init__(self, client):
        self.client = client

    # Creates an event within a cog
    @commands.Cog.listener()
    async def on_ready(self):
        "testing this stuff out"
        print("Bot Ready")

    # Actual command definition
    @commands.command()
    async def ping(self, ctx, *msgs):
        """will send a "Pong!" message back"""
        print(msgs)
        print(Debugging.on_ready.__doc__)
        await ctx.send("WHO DOTH PING ME <:yesdaddy:719927492890198087>")


def setup(client):
    client.add_cog(Debugging(client))


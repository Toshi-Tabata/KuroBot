import discord
from discord.ext import commands
import database_helper as db

class HelloWorld(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Creates an event within a cog
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot Ready")

    # Actual command definition
    @commands.command()
    async def ping(self, ctx, *msgs):
        """
        Sends a "Pong!" message back to the channel the command was called from
        :param ctx:
        :return:
        """
        print(msgs)
        await ctx.send("WHO DOTH PING ME <:yesdaddy:719927492890198087>")


def setup(client):
    client.add_cog(HelloWorld(client))


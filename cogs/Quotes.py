import discord
import random
from discord.ext import commands
import database_helper as db
from cogs.reply_helper.quoteHelper import get_quote

class Quotes(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Function that replies with a random quote from kuro
    @commands.command()
    async def quote(self, ctx, *args):
        """will send a random quote or the desired quote back"""
        db.increase_stat(ctx.author.id, "quote")
        parsed_quote = get_quote(args)
        for q in parsed_quote:
            await ctx.send(q)

def setup(client):
    client.add_cog(Quotes(client))


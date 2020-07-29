import discord
import random
from discord.ext import commands
import database_helper as db

class Quotes(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Function that replies with a random quote from kuro
    @commands.command()
    async def quote(self, ctx, *args):
        db.increase_stat(ctx.author.id, "quote")
        
        with open("KuroQuotes.txt") as file:
            quotes = list(file)
            quoteToSend = []
            for arg in args:
                try:
                    index = int(arg)
                    quote = quotes[index].split("\\n")

                except (ValueError, IndexError):
                    quote = random.choice(quotes)
                    quote = quote.split("\\n")
                
                for q in quote:
                    quoteToSend.append(q)

            # Send the list of quotes if we managed to get any
            if quoteToSend:
                for q in quoteToSend:
                    await ctx.send(q)
            else:
                # We didn't get any valid args
                quote = random.choice(quotes)
                parsed_quote = quote.split("\\n")
                for q in parsed_quote:
                    await ctx.send(q)

def setup(client):
    client.add_cog(Quotes(client))


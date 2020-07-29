import discord
import json
from discord.ext import commands
import database_helper as db

class Stats(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Actual command definition
    @commands.command()
    async def stats(self, ctx, *msgs):
        """
        Returns stats about Kuro Bot
        :param ctx:
        :return:
        """
        db.increase_stat(ctx.author.id, "checked_stats")

        def stat_to_text(stat, value, author_id):
            stat_to_string = {
                "times_talked": f"You've talked to me {value} times",
                "owo": f"you hwave owo'd mwe {value} twimes uwu",
                "quote": f"You have asked for a quote {value} times",
                "checked_stats": f"You have checked our stats {value} times",
                "pinged_kuro": f"You have pinged kuro {value} times",
            }
            if stat not in stat_to_string:
                return f"{stat}: {value}"
            elif author_id == "109590357276098560" and stat == "times_talked":
                return f"You have talked to yourself {value} times"
            else:
                return stat_to_string[stat]

        with open("stats.json", "r") as stats:
            stats_obj = json.load(stats)
            author = str(ctx.author.id)
            # author_name = discord.get_user(author)
            author_stats = ""

            if author not in stats_obj:
                author_stats = "You haven't talked to me recently"
            else:
                for key in stats_obj[author]:
                    author_stats += f"{stat_to_text(key, stats_obj[author][key], author)}\n"

            embeded = discord.Embed(title="Here are your stats with me!", description=author_stats, color=0x00ff00)
            embeded.set_thumbnail(url="https://cdn.discordapp.com/icons/704320774734872577/ce8bfd35ce8598e5792533b1a45c875c.png?size=128")
            await ctx.send(embed=embeded)


def setup(client):
    client.add_cog(Stats(client))


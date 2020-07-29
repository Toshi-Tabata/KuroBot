import discord
import json
import random
import re
import database_helper as db
from discord.ext import commands
from discord.utils import get
import asyncio
import shlex
# screen -d -m python3 ~/programming/python/kurobot/kurobot/main.py

class Poll(commands.Cog):

    def __init__(self, client):
        self.client = client
        # polls = {"msg_id": [list of reactions we have set]}
        self.polls = {}

    def create_poll_embed(self, poll_question, poll_string):
        # Create an embed for the poll
        embeded = discord.Embed(title=poll_question, description=poll_string, color=0x00ff00)
        embeded.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/728197164676808747/728242568394965045/0adc0fbc5fed89147179591d5abb428600acf8a4_hq_1.jpg")

        return embeded

    async def get_poll_react_message(self, message, msg_id):
        user_string = "Users who have reacted: \n"
        for reaction in message.reactions:

            if msg_id in self.polls and str(reaction) in self.polls[msg_id]:
                reaction_string = f"{reaction} "
                reaction_users = set()
                async for user in reaction.users():
                    if not user.bot:

                        reaction_users.add(user.nick)

                reaction_string += ", ".join(reaction_users)

                user_string += f"{reaction_string} \n"

        return user_string

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, ctx):
        msg_id = str(ctx.message_id)
        channel = self.client.get_channel(ctx.channel_id)
        message = await channel.fetch_message(ctx.message_id)

        user_string = await self.get_poll_react_message(message, msg_id)

        # Check that the new react is a valid react
        if msg_id in self.polls and ctx.emoji.name in self.polls[msg_id]:
            await message.edit(content=user_string)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):
        msg_id = str(ctx.message_id)
        channel = self.client.get_channel(ctx.channel_id)
        message = await channel.fetch_message(ctx.message_id)

        user_string = await self.get_poll_react_message(message, msg_id)

        # Check that the new react is a valid react
        if msg_id in self.polls and ctx.emoji.name in self.polls[msg_id]:
            await message.edit(content=user_string)

    @commands.command()
    async def poll(self, ctx, *args):
        """
        Creates a poll with the given options
        Usage: !poll "option_one" "option_two" "option_three" ... "option_twenty"
        :param ctx:
        :return:
        """

        if not args:
            await ctx.send("Please provide a poll question and poll options! (Usage: !poll <question> <options...>)")
            return
        elif len(args) < 2:
            await ctx.send("Please provide poll options! (Usage: !poll <question> <options...>)")
            return

        react_options = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹"]

        message = await ctx.send("Creating your poll!")
        poll_question = shlex.split(ctx.message.clean_content)[1]
        args = args[1:]
        poll_string = ""

        # Loop through all the poll options given, up to a maximum of 20 (the limit for reactions on messages)
        num_options = min(len(args), 20)
        for idx in range(0, num_options):
            reaction = react_options[idx]
            arg = args[idx]

            await message.add_reaction(emoji=reaction)
            poll_string += f"{reaction}: {arg}\n"

        embeded = self.create_poll_embed(poll_question, poll_string)

        await message.edit(embed=embeded)
        await message.edit(content="")
        self.polls[str(message.id)] = react_options[:num_options]


def setup(client):
    client.add_cog(Poll(client))

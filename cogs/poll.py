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
from discord.ext.commands import Bot
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import threading


class Poll(commands.Cog):

    def __init__(self, client):
        self.client = client
        # polls = {"msg_id": {choices:  choice_id: {user_id: username}  }}
        """
        polls = {
            msg_id1: {
                choice1_id: {
                    choice_name: name,
                    users: {
                        user_id1: username, 
                        user_id2: username
                    }

                },
                choice2_id: {
                    choice_name: name, 
                    user_id1: username, 
                    user_id2: username
                }
            },
        }


        """
        self.polls = {}

    def create_poll_embed1(self, poll_question, username):
        # Create an embed for the poll
        embeded = discord.Embed(title=poll_question, color=0x00ff00)
        embeded.add_field(name="Started By", value=username, inline=False)
        embeded.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/728197164676808747/728242568394965045/0adc0fbc5fed89147179591d5abb428600acf8a4_hq_1.jpg")

        return embeded


    def get_poll_react_message1(self, msg_id):
        user_string = "Users who have reacted: \n"

        ans = ""
        if msg_id in self.polls:
            
            for choice_key in self.polls[msg_id]:
                choice = self.polls[msg_id][choice_key]

                name = choice["choice_name"]
                user_names = map(lambda user_id: choice["users"][user_id], choice["users"])
                ans = ans + "\n" + name + ": " + str(list(user_names))

        return user_string + ans

    async def delete_poll(self, poll_id, ctx, duration):
        await asyncio.sleep(duration)
        res = self.get_poll_react_message1(poll_id)
        await ctx.send("Poll Completed.\n" + res)
        del self.polls[poll_id]
    
    @commands.command()
    async def poll(self, ctx, *args):
        if not args:
            await ctx.send("Please provide a poll question and poll options! (Usage: !poll <question> <duration in seconds> <options...>)")
            return
        elif len(args) < 3:
            await ctx.send("Please provide poll options! (Usage: !poll <question> <duration in seconds> <options...>)")
            return

        duration = shlex.split(ctx.message.clean_content)[2]
        if (not duration.isnumeric() or 0 > int(duration) > 60):
            await ctx.send("Duration must be a whole number between 0 and 3600")
            return

        duration = int(duration)

        message = await ctx.send("Creating your poll!")
        poll_question = shlex.split(ctx.message.clean_content)[1]
        

        args = args[2:]


        poll_options = []
        # Loop through all the poll options given, up to a maximum of 20 (the limit for reactions on messages)
        num_options = min(len(args), 20)
        for idx in range(0, num_options):

            arg = args[idx]
            colour = random.choice([ButtonStyle.grey, ButtonStyle.green, ButtonStyle.blue, ButtonStyle.red])
            poll_options.append(Button(label=arg, style=colour))

        print(ctx)
        print(ctx.message)

        embeded = self.create_poll_embed1(poll_question, ctx.message.author.name) 

        await message.edit(embed=embeded)
        await message.edit(content="",
            components=[poll_options]
        )

        self.polls[str(message.id)] = {} # users who have reacted to the message, with which one they reacted to
        
    
        await self.delete_poll(str(message.id), ctx, duration)

    @commands.Cog.listener()
    async def on_button_click(self, ctx):

        
        # print(dir(ctx))
        # print(dir(ctx.message))
        # print(ctx.user.name)  # username
        # print(ctx.message.id)  # ctx.message.id == message_id stored inside polls dictionary key
        # print(dir(ctx.component))
        # print(ctx.component.id)  # unique identifier for which button got pressed

        msg_id = str(ctx.message.id)

        if msg_id not in self.polls:
            return

        user_id = ctx.user
        username = ctx.user.name
        choice_id = ctx.component.id

        if choice_id not in self.polls[msg_id]:
            self.polls[msg_id][choice_id] = {"choice_name": ctx.component.label, "users": {}}

        if user_id in self.polls[msg_id][choice_id]["users"]:
            del self.polls[msg_id][choice_id]["users"][user_id]
        else:
            self.polls[msg_id][choice_id]["users"][user_id] = username

        res = self.get_poll_react_message1(msg_id)
        await ctx.message.edit(content=res)
        await ctx.respond(type=7)


    # async def get_poll_react_message(self, message, msg_id):
    #     user_string = "Users who have reacted: \n"
    #     for reaction in message.reactions:

    #         if msg_id in self.polls and str(reaction) in self.polls[msg_id]:
    #             reaction_string = f"{reaction} "
    #             reaction_users = set()
    #             async for user in reaction.users():
    #                 if not user.bot:

    #                     reaction_users.add(user.nick)

    #             reaction_string += ", ".join(reaction_users)

    #             user_string += f"{reaction_string} \n"

    #     return user_string

    # @commands.Cog.listener()
    # async def on_raw_reaction_remove(self, ctx):
    #     msg_id = str(ctx.message_id)
    #     channel = self.client.get_channel(ctx.channel_id)
    #     message = await channel.fetch_message(ctx.message_id)

    #     user_string = await self.get_poll_react_message(message, msg_id)

    #     # Check that the new react is a valid react
    #     if msg_id in self.polls and ctx.emoji.name in self.polls[msg_id]:
    #         await message.edit(content=user_string)

    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, ctx):
    #     msg_id = str(ctx.message_id)
    #     channel = self.client.get_channel(ctx.channel_id)
    #     message = await channel.fetch_message(ctx.message_id)

    #     user_string = await self.get_poll_react_message(message, msg_id)

    #     # Check that the new react is a valid react
    #     if msg_id in self.polls and ctx.emoji.name in self.polls[msg_id]:
    #         await message.edit(content=user_string)

    # @commands.command()
    # async def poll(self, ctx, *args):
    #     """
    #     Usage: !poll question "option_two" "option_three" etc. 20 max
    #             will create a poll with the given options
    #     """

    #     if not args:
    #         await ctx.send("Please provide a poll question and poll options! (Usage: !poll <question> <options...>)")
    #         return
    #     elif len(args) < 2:
    #         await ctx.send("Please provide poll options! (Usage: !poll <question> <options...>)")
    #         return

    #     react_options = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹"]

    #     message = await ctx.send("Creating your poll!")
    #     poll_question = shlex.split(ctx.message.clean_content)[1]
    #     args = args[1:]
    #     poll_string = ""

    #     # Loop through all the poll options given, up to a maximum of 20 (the limit for reactions on messages)
    #     num_options = min(len(args), 20)
    #     for idx in range(0, num_options):
    #         reaction = react_options[idx]
    #         arg = args[idx]

    #         await message.add_reaction(emoji=reaction)
    #         poll_string += f"{reaction}: {arg}\n"

    #     embeded = self.create_poll_embed(poll_question, poll_string)

    #     await message.edit(embed=embeded)
    #     await message.edit(content="")
    #     self.polls[str(message.id)] = react_options[:num_options]


def setup(client):
    client.add_cog(Poll(client))

import discord
import random
import re
import json
from discord.ext import commands
from datetime import datetime

import database_helper as db

"""
Module for listening to all messages and replying accordingly
"""

BOT_ID = 729244809021358141

class Reply(commands.Cog):

    def __init__(self, client):
        self.client = client

    # # Actual command definition
    # @commands.command()
    # async def test(self, ctx):
    #     """Function made to be overwritten for testing purposes"""
    #     await ctx.send("Pong!")

    def message_contains(self, word, currMessage):
        return re.search(f".*{word}.*", currMessage, re.IGNORECASE)

    # ctx.guild/message/author/send()
    # Listens to the chat and replies when it hears certain lines
    @commands.Cog.listener()
    async def on_message(self, ctx):

        currMessage = ctx.content
        did_talk = False  # Flag to check if the author talked with kuro bot

        # TODO: refactor this whole if statement chain, probably functionalise this to avoid yandere simulator memery
        if ctx.author.id != BOT_ID:
            if ctx.guild is None:
                did_talk = True
                with open("log.txt", 'a+') as file:
                    timestamp = datetime.now().strftime("[%d/%m/%Y][%H:%M:%S]")
                    print(ctx.content)
                    file.write(f"{timestamp} {ctx.author}: {ctx.content}\n")

            if self.message_contains("kuro", currMessage):
                did_talk = True
                dialogue = random.choice(["yes", "hmm", "indeed", "i see", "wait what", "ooooookaaaaaaayyyy", "mmhmm", "ok", "correct", "uuuuuuh"])
                await ctx.channel.send(dialogue)

            elif self.message_contains("kuwo", currMessage):
                db.increase_stat(ctx.author.id, "owo")
                did_talk = True
                dialogue = random.choice(["yes :3", "hmm owo", "indeed >\\<", "i see uwu", "ooookayyy owo", "wwwait what", "uuuuuuuh.."])
                await ctx.channel.send(dialogue)

            elif self.message_contains("aiya|aya", currMessage):
                did_talk = True
                await ctx.channel.send("ayayayayayaya")
            
            if self.message_contains(">V|>:V", currMessage):
                did_talk = True
                await ctx.add_reaction(emoji="<:bertV:732834829040877640>")

            if self.message_contains("is gay|daddy", currMessage):
                did_talk = True
                await ctx.channel.send("<:yesdaddy:719927492890198087>")

            for user in ctx.mentions:
                print(f"user(s) mentioned were {user}")
                
                if user.id == 729244809021358141 or user.id == 109590357276098560: 
                    db.increase_stat(ctx.author.id, "pinged_kuro")
                    await ctx.channel.send("<:yesdaddy:719927492890198087>")

            if did_talk:
                db.increase_stat(ctx.author.id, "times_talked")
    
        msgs = []
        async for message in ctx.channel.history(limit=3):
            msgs.append(message.content)

        last_msg = msgs[1]
        second_last = msgs[0]
        if last_msg == "wtf i'm scared" and second_last == "hi scared":
            await ctx.channel.send("eeeeeeeeeeeeeeeeeeeeee")


def setup(client):
    client.add_cog(Reply(client))


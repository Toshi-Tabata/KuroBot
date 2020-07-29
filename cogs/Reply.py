import discord
import random
import re
import json
from discord.ext import commands
from datetime import datetime

import database_helper as db
import cogs.reply_helper.responses as r
"""
Module for listening to all messages and replying accordingly
"""

BOT_ID = 729244809021358141
KURO_ID = 109590357276098560

class Reply(commands.Cog):


    def __init__(self, client):
        self.client = client


    async def handle_pings(self, ctx):
        # Check if people have pinged kuro
        for user in ctx.mentions:
            if user.id == BOT_ID or user.id == KURO_ID: 
                db.increase_stat(ctx.author.id, "pinged_kuro")
                await ctx.channel.send("<:yesdaddy:719927492890198087>")


    # Records my direct messages to Kuro Bot so I can just copy and paste chunks of messages
    def debugging_logs(self, ctx):
        with open("log.txt", 'a+') as file:
            timestamp = datetime.now().strftime("[%d/%m/%Y][%H:%M:%S]")
            file.write(f"{timestamp} {ctx.author}: {ctx.content}\n")


    # ctx.guild/message/author/send()
    # Listens to the chat and replies when it hears certain lines
    @commands.Cog.listener()
    async def on_message(self, ctx):

        currMessage = ctx.content
        did_talk = False  # Flag to check if the author talked with kuro bot

        if ctx.author.id != BOT_ID:
            if ctx.guild is None:
                self.debugging_logs(ctx)
                did_talk = True

            did_talk = await r.match_message(ctx, currMessage)
            await self.handle_pings(ctx)

            if did_talk:
                db.increase_stat(ctx.author.id, "times_talked")
        
        await r.check_prev_msg(ctx)


def setup(client):
    client.add_cog(Reply(client))

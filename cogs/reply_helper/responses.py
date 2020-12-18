import database_helper as db
import re
import random

"""
Helper file to handle responses by Kuro Bot
"""
async def kuro(ctx):
    dialogue = random.choice(["yes", "hmm", "indeed", "i see", "wait what", "ooooookaaaaaaayyyy", "mmhmm", "ok", "correct", "uuuuuuh"])
    await ctx.channel.send(dialogue)
    return True

async def kuwo(ctx):
    db.increase_stat(ctx.author.id, "owo")
    dialogue = random.choice(["yes :3", "hmm owo", "indeed >\\<", "i see uwu", "ooookayyy owo", "wwwait what", "uuuuuuuh.."])
    await ctx.channel.send(dialogue)
    return True

async def aiya(ctx):
    await ctx.channel.send("ayayayayayaya")
    return True

async def grr(ctx):
    await ctx.add_reaction(emoji="<:bertV:732834829040877640>")
    return True

async def daddy(ctx):
    await ctx.channel.send("<:yesdaddy:719927492890198087>")
    return True

def message_contains(word, currMessage):
    return re.search(f".*{word}.*", currMessage, re.IGNORECASE)

async def match_message(ctx, currMessage):
    # Loop through array to simulate if/else statements
    message_to_match = [
        ["kuro", "kuwo", "aiya|aya"],   # Nested list elements are mutually exclusive to each other (basically an if else)
        ">V|>:V",                       # Unnested items can be executed alongside other items (pure if statement)
        "is gay|daddy",
        ]

    get_response = {
        "kuro":         kuro,
        "kuwo":         kuwo,
        "aiya|aya":     aiya,
        ">V|>:V":       grr,
        "is gay|daddy": daddy,
    }
    did_talk = False
    # Find the function matching the message that we want to match (the mask)
    for mask in message_to_match:
        if isinstance(mask, list):
            for m in mask:
                if message_contains(m, currMessage):
                    did_talk = await get_response[m](ctx)
                    break
        else:
            if message_contains(mask, currMessage):
                did_talk = await get_response[mask](ctx)

    return did_talk


# Handle cases where we want to match multiple messages
# I don't think matching more than just the previous message is necessary (since I don't think we'd use it ever)
#   also we can chain checks for the previous message if we did want to match more than just the previous message
async def check_prev_msg(ctx):
    msgs = []
    async for message in ctx.channel.history(limit=3):
        msgs.append(message.content)

    last_msg = msgs[1]
    second_last = msgs[0]

    messages_to_match = {
        ("wtf i'm scared", "hi scared"): "eeeeeeeeeeeeeeeeeeeeee"
    }

    try:
        resp = messages_to_match[(last_msg, second_last)]
        await ctx.channel.send(resp)
    except KeyError:
        pass
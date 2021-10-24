import database_helper as db
import re
import random

PITY_COUNT = 89
IS_SECOND_PITY = True

"""
Helper file to handle responses by Kuro Bot
"""
async def kuro(ctx):
    dialogue = random.choice(["yes", "hmm", "indeed", "i see", "wait what", "ooooookaaaaaaayyyy", "mmhmm", "ok", "correct", "uuuuuuh", "shut up fool"])
    await ctx.channel.send(dialogue)
    return True

async def kuwo(ctx):
    db.increase_stat(ctx.author.id, "owo")
    dialogue = random.choice(["yes :3", "hmm owo", "indeed >\\<", "i see uwu", "ooookayyy owo", "wwwait what", "uuuuuuuh..", "shut up baka"])
    await ctx.channel.send(dialogue)
    return True

async def aiya(ctx):
    global PITY_COUNT, IS_SECOND_PITY
    ayakaPic = [
        "https://www.dexerto.com/wp-content/uploads/2021/07/12/Ayaka-banner-Genshin-Impact-Inazuma-update.jpg",
        "https://progameguides.com/wp-content/uploads/2021/03/Genshin-Impact-Character-Ayaka-1.jpg",
        "https://www.pcgamesn.com/wp-content/uploads/2021/05/genshin-impact-ayaka-banner-release-date.jpg",
        "https://media.tenor.com/images/63b9d5d8ce338ca6d42d26d5ef64f445/tenor.gif",
        "https://upload-os-bbs.hoyolab.com/upload/2020/03/27/5789515/29c2a289a87a66732d8418b911656251_5076537097905967477.gif?x-oss-process=image/resize,s_740/quality,q_80/auto-orient,0/interlace,1/format,gif",
        "https://gfycat.com/unfinishednastydavidstiger"
    ]
    if random.random() < 0.006 or (PITY_COUNT >= 90 and IS_SECOND_PITY):
        PITY_COUNT = 0
        IS_SECOND_PITY = False

        await ctx.channel.send(random.choice(ayakaPic))
    elif PITY_COUNT >= 90:
        PITY_COUNT = 0
        IS_SECOND_PITY = True
        if random.random() < 0.5:
            await ctx.channel.send("https://imgur.com/zhLrqtT")
        else:
            await ctx.channel.send("https://gfycat.com/unfinishednastydavidstiger")

    else:
        PITY_COUNT += 1
        print(f"pity count: {PITY_COUNT}, second {IS_SECOND_PITY}")

        if random.random() < 0.01:
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
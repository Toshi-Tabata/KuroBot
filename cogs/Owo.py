import discord
from discord.ext import commands
import database_helper as db
import random
from cogs.reply_helper.quoteHelper import get_quote

def insert_between(text):
    # Omit the 'w' since it looks better not inserting an additional 'w'
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 's', 't', 'v', 'y', 'z']
    vowels = ['a', 'e', 'i', 'o', 'u']

    inserted_text = text[0]

    # Loop pairwise through each piece of text
    for idx, letter in enumerate(text[:-1]):
        if letter.lower() in consonants and text[idx + 1].lower() in vowels:
            w = "w" if letter.islower() else "W"
            inserted_text += w

        inserted_text += text[idx + 1]

    return inserted_text


def replace_letters(text, which_letter):
    """
    Replaces l's with w's only if they are between two vowels
    :param text: String
    :return: new String with l's replaced
    """
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'y', 'z']
    vowels = ['a', 'e', 'i', 'o', 'u', " "]

    idx_to_replace = []
    is_between = True

    curr_idx = []
    for idx, letter in enumerate(text):
        letter = letter.lower()
        if is_between and letter == which_letter:
            curr_idx.append(idx)
        elif letter in vowels:
            idx_to_replace += curr_idx
        else:
            curr_idx = []

        is_between = letter in vowels or letter == which_letter

    for idx in idx_to_replace:
        w = "w" if text[idx].islower() else "W"
        text = text[:idx] + w + text[idx + 1:]

    return text


def owowify(text):
    """
    Given text, "owowifies" it.
    Inserts w's to mwake thwe twext cwutwer owo
    :param text: String
    :return: Owowified text
    """

    text = replace_letters(text, "l")
    text = replace_letters(text, "r")

    return insert_between(text)


def handle_redirection(commands):
    if commands[0] == "!quote":
        return get_quote(commands[1:])


class Owo(commands.Cog):
    """Debugging and Testing Functions"""

    def __init__(self, client):
        self.client = client


    # Actual command definition
    @commands.command()
    async def owo(self, ctx, *msgs):
        """Owoify text. Owoify quotes by combining them !owo < !quote 52"""
        print(msgs)

        owotext = ""
        new_texts = None
        for idx, text in enumerate(msgs):
            print(text)
            if text == "<" and msgs[idx + 1] == "!quote":
                new_texts = handle_redirection(msgs[idx + 1:])
                break
            else:
                owotext += owowify(text) + " "

        if owotext:
            await ctx.send(owotext)

        if new_texts:
            for text1 in new_texts:
                await ctx.send(owowify(text1))


def setup(client):
    client.add_cog(Owo(client))










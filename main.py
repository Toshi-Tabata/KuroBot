import discord, os, json
from discord.ext import commands
from discord_components import DiscordComponents

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    DiscordComponents(client)

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        file_name = f"cogs.{file[:-3]}"
        client.load_extension(file_name)


if __name__ == "__main__":
    with open("token.json") as f:
        token = json.load(f)["token"]
        client.run(token)

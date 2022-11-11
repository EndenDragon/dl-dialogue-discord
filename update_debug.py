from config import config
from dldialogue import discord

if __name__ == "__main__":
    discord.update_commands(guild_id=config["TESTING_GUILD"])
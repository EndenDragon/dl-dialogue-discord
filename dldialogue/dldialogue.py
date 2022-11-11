from config import config
from flask import Flask

from flask_discord_interactions import (
    DiscordInteractions,
    Message,
    Modal,
    TextInput,
    TextStyles,
    ActionRow,
    Button,
)

app = Flask(__name__)
discord = DiscordInteractions(app)

app.config["DISCORD_CLIENT_ID"] = config["DISCORD_CLIENT_ID"]
app.config["DISCORD_PUBLIC_KEY"] = config["DISCORD_PUBLIC_KEY"]
app.config["DISCORD_CLIENT_SECRET"] = config["DISCORD_CLIENT_SECRET"]

@discord.command(name="ping", description="Pings the server")
def ping(ctx):
    return Message(
        content="Pong!"
    )

discord.set_route("/discord")

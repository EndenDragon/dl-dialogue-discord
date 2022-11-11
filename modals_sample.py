import os
import sys

from config import config
from flask import Flask

# This is just here for the sake of examples testing
# to make sure that the imports work
# (you don't actually need it in your code)
#sys.path.insert(1, ".")

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


#discord.update_commands()


@discord.custom_handler("example_modal")
def modal_callback(ctx):
    msg = (
        f"Hello {ctx.get_component('name').value}! "
        f"So you are {ctx.get_component('age').value} years old "
        "and this is how you describe yourself: "
        f"{ctx.get_component('description').value}"
    )
    return Message(msg, ephemeral=True)


@discord.command(name="test_modal", description="Opens a Modal window")
def modal(ctx):
    fields = [
        ActionRow(
            [
                TextInput(
                    custom_id="name",
                    label="What's your name?",
                    placeholder="John Doe",
                    style=TextStyles.SHORT,
                    required=True,
                )
            ]
        ),
        ActionRow(
            [
                TextInput(
                    custom_id="age",
                    label="What's your age?",
                    style=TextStyles.SHORT,
                    min_length=1,
                    max_length=5,
                    required=False,
                )
            ]
        ),
        ActionRow(
            [
                TextInput(
                    custom_id="description",
                    label="Describe yourself:",
                    value="A very interesting person",
                    style=TextStyles.PARAGRAPH,
                    min_length=10,
                    max_length=2000,
                )
            ]
        ),
    ]
    return Modal("example_modal", "Tell me about yourself", fields)


@discord.custom_handler()
def example_modal_2(ctx):
    return Message(f"Hello {ctx.get_component('name').value}!", update=True)


@discord.custom_handler()
def launch_modal(ctx):
    return Modal(
        example_modal_2,
        "Tell me about yourself",
        [
            ActionRow(
                [
                    TextInput(
                        custom_id="name",
                        label="What's your name?",
                        placeholder="John Doe",
                        style=TextStyles.SHORT,
                        required=True,
                    )
                ]
            )
        ],
    )


@discord.command()
def launch_modal_from_button_yes(ctx):
    return Message(
        content="Launch Modal",
        components=[ActionRow([Button(custom_id=launch_modal, label="Launch Modal")])],
    )


discord.set_route("/discord")
#discord.update_commands(guild_id=config["TESTING_GUILD"])
#discord.update_commands()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, ssl_context=('keys/fullchain.pem', 'keys/privkey.pem'))